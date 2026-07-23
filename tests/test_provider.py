"""Tests de T-002: contrato `Provider` e implementación `ClaudeCLIProvider`.

El CLI real nunca se invoca aquí; se sustituyen `shutil.which` y
`subprocess.run` del módulo bajo prueba. La verificación contra el CLI de
verdad es T-003.
"""

import subprocess

import pytest

from soda.core.provider import (
    Provider,
    ProviderError,
    ProviderExecutionError,
    ProviderNotFoundError,
    ProviderTimeoutError,
)
from soda.providers import ClaudeCLIProvider

# --- Contrato abstracto ---------------------------------------------------


def test_provider_no_es_instanciable():
    with pytest.raises(TypeError):
        Provider()


def test_subclase_sin_send_no_es_instanciable():
    class ProviderIncompleto(Provider):
        pass

    with pytest.raises(TypeError):
        ProviderIncompleto()


def test_subclase_con_send_es_instanciable():
    class ProviderFalso(Provider):
        def send(self, prompt: str) -> str:
            return f"eco: {prompt}"

    assert ProviderFalso().send("hola") == "eco: hola"


def test_jerarquia_de_errores():
    for excepcion in (ProviderNotFoundError, ProviderTimeoutError, ProviderExecutionError):
        assert issubclass(excepcion, ProviderError)


# --- ClaudeCLIProvider ----------------------------------------------------


@pytest.fixture
def cli_disponible(monkeypatch):
    """Hace que `shutil.which` resuelva el ejecutable a una ruta ficticia."""
    monkeypatch.setattr(
        "soda.providers.claude_cli.shutil.which",
        lambda nombre: f"/ruta/ficticia/{nombre}",
    )


def _resultado(returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(
        args=["claude", "--print"], returncode=returncode, stdout=stdout, stderr=stderr
    )


def test_es_un_provider():
    assert isinstance(ClaudeCLIProvider(), Provider)


def test_devuelve_stdout_sin_espacios_sobrantes(monkeypatch, cli_disponible):
    monkeypatch.setattr(
        "soda.providers.claude_cli.subprocess.run",
        lambda *a, **kw: _resultado(stdout="  respuesta del modelo\n"),
    )
    assert ClaudeCLIProvider().send("hola") == "respuesta del modelo"


def test_invoca_el_cli_en_modo_print_con_el_prompt_por_stdin(monkeypatch, cli_disponible):
    llamadas = []

    def run_espia(cmd, **kwargs):
        llamadas.append((cmd, kwargs))
        return _resultado(stdout="ok")

    monkeypatch.setattr("soda.providers.claude_cli.subprocess.run", run_espia)
    ClaudeCLIProvider(timeout=42.0).send("mi prompt")

    cmd, kwargs = llamadas[0]
    assert cmd == ["/ruta/ficticia/claude", "--print"]
    assert kwargs["input"] == "mi prompt"
    assert kwargs["timeout"] == 42.0


def test_error_si_el_ejecutable_no_esta_en_path(monkeypatch):
    monkeypatch.setattr("soda.providers.claude_cli.shutil.which", lambda nombre: None)
    with pytest.raises(ProviderNotFoundError, match="no-existe"):
        ClaudeCLIProvider(executable="no-existe").send("hola")


def test_error_si_el_cli_falla(monkeypatch, cli_disponible):
    monkeypatch.setattr(
        "soda.providers.claude_cli.subprocess.run",
        lambda *a, **kw: _resultado(returncode=1, stderr="credenciales inválidas"),
    )
    with pytest.raises(ProviderExecutionError, match="credenciales inválidas"):
        ClaudeCLIProvider().send("hola")


def test_error_si_el_cli_expira(monkeypatch, cli_disponible):
    def run_que_expira(*a, **kw):
        raise subprocess.TimeoutExpired(cmd="claude", timeout=1.0)

    monkeypatch.setattr("soda.providers.claude_cli.subprocess.run", run_que_expira)
    with pytest.raises(ProviderTimeoutError):
        ClaudeCLIProvider(timeout=1.0).send("hola")


def test_error_si_el_sistema_no_puede_ejecutarlo(monkeypatch, cli_disponible):
    def run_que_falla(*a, **kw):
        raise OSError("Exec format error")

    monkeypatch.setattr("soda.providers.claude_cli.subprocess.run", run_que_falla)
    with pytest.raises(ProviderNotFoundError, match="Exec format error"):
        ClaudeCLIProvider().send("hola")
