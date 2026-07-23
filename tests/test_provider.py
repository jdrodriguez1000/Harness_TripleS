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


@pytest.fixture
def espia(monkeypatch):
    """Sustituye `subprocess.run` y acumula `(cmd, kwargs)` de cada llamada."""
    llamadas = []

    def run_espia(cmd, **kwargs):
        llamadas.append((cmd, kwargs))
        return _resultado(stdout="ok")

    monkeypatch.setattr("soda.providers.claude_cli.subprocess.run", run_espia)
    return llamadas


def test_invoca_el_cli_en_modo_print_con_el_prompt_por_stdin(cli_disponible, espia):
    ClaudeCLIProvider(timeout=42.0).send("mi prompt")

    cmd, kwargs = espia[0]
    assert cmd[:2] == ["/ruta/ficticia/claude", "--print"]
    assert kwargs["input"] == "mi prompt"
    assert kwargs["timeout"] == 42.0


def test_no_persiste_la_sesion_en_el_proyecto_destino(cli_disponible, espia):
    ClaudeCLIProvider().send("hola")
    assert "--no-session-persistence" in espia[0][0]


# --- Modelo (intercambiable) ----------------------------------------------


def test_sin_modelo_no_pasa_el_flag(cli_disponible, espia):
    ClaudeCLIProvider().send("hola")
    assert "--model" not in espia[0][0]


def test_el_modelo_viaja_como_flag(cli_disponible, espia):
    ClaudeCLIProvider(model="haiku").send("hola")

    cmd = espia[0][0]
    assert cmd[cmd.index("--model") + 1] == "haiku"


# --- Herramientas ---------------------------------------------------------


def test_por_defecto_desactiva_todas_las_herramientas(cli_disponible, espia):
    ClaudeCLIProvider().send("hola")

    cmd = espia[0][0]
    assert cmd[cmd.index("--tools") + 1] == ""


def test_una_lista_de_herramientas_viaja_separada_por_comas(cli_disponible, espia):
    ClaudeCLIProvider(tools=["Read", "Glob"]).send("hola")

    cmd = espia[0][0]
    assert cmd[cmd.index("--tools") + 1] == "Read,Glob"


def test_tools_none_deja_el_conjunto_por_defecto_del_cli(cli_disponible, espia):
    ClaudeCLIProvider(tools=None).send("hola")
    assert "--tools" not in espia[0][0]


# --- Suscripción y directorio de trabajo ----------------------------------


def test_borra_las_credenciales_de_api_del_subproceso(monkeypatch, cli_disponible, espia):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-no-usar")
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "tampoco")
    monkeypatch.setenv("PATH_DE_PRUEBA", "se-conserva")

    ClaudeCLIProvider().send("hola")

    entorno = espia[0][1]["env"]
    assert "ANTHROPIC_API_KEY" not in entorno
    assert "ANTHROPIC_AUTH_TOKEN" not in entorno
    assert entorno["PATH_DE_PRUEBA"] == "se-conserva"


def test_sin_solo_suscripcion_hereda_el_entorno_tal_cual(cli_disponible, espia):
    ClaudeCLIProvider(solo_suscripcion=False).send("hola")
    assert espia[0][1]["env"] is None


def test_el_subproceso_corre_en_el_directorio_indicado(tmp_path, cli_disponible, espia):
    ClaudeCLIProvider(cwd=tmp_path).send("hola")
    assert espia[0][1]["cwd"] == tmp_path


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
