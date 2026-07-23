"""Tests de T-013: `soda start`, rama de proyecto vacío (bootstrap de Git).

Aquí se usa `git` de verdad sobre directorios temporales, no un doble. Es
deliberado: lo que esta tarea promete —que no destruye nada, que es idempotente
y que deja un repositorio con un commit— solo lo puede desmentir git. Un mock
confirmaría que llamamos a los comandos que creemos, que es justo lo que no
está en duda.

Lo único que no se ejerce contra un servidor real es el push; para eso el remoto
apunta a un repositorio local `--bare`, que se comporta igual sin salir a la red.

Ningún test invoca un modelo: toda esta rama es Python puro (D-026).
"""

from pathlib import Path

import pytest

from soda.core import git
from soda.start import (
    MENSAJE_COMMIT_INICIAL,
    SinCanalConElHumanoError,
    bootstrap,
    reglas_que_faltan,
    url_valida,
)
from soda.templates import GITIGNORE_FILENAME, read_gitignore_template

pytestmark = pytest.mark.skipif(
    not git.esta_disponible(), reason="requiere el binario `git` en el PATH"
)


class Humano:
    """Doble del humano: responde de una cola y registra lo que le preguntaron."""

    def __init__(self, *respuestas: str) -> None:
        self.pendientes = list(respuestas)
        self.preguntas: list[str] = []

    def __call__(self, pregunta: str) -> str:
        self.preguntas.append(pregunta)
        return self.pendientes.pop(0) if self.pendientes else ""


class Salida:
    """Doble de `print` que acumula las líneas reportadas."""

    def __init__(self) -> None:
        self.lineas: list[str] = []

    def __call__(self, linea: str = "") -> None:
        self.lineas.append(linea)

    @property
    def texto(self) -> str:
        return "\n".join(self.lineas)


@pytest.fixture(autouse=True)
def git_aislado(tmp_path, monkeypatch):
    """Aparta la configuración global de git de quien corre los tests.

    Sin esto los tests dependen de la máquina: si el desarrollador tiene
    `user.name` global, el flujo no pregunta la identidad, las respuestas del
    humano falso se desplazan una posición y fallan pruebas que no tienen nada
    que ver. Peor todavía, los commits de prueba se firmarían con su identidad
    real. El subproceso hereda estas variables de entorno.
    """
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(tmp_path / "sin-config-global"))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(tmp_path / "sin-config-sistema"))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


@pytest.fixture
def proyecto(tmp_path) -> Path:
    """Un directorio de proyecto con un archivo, sin repositorio git."""
    raiz = tmp_path / "proyecto"
    raiz.mkdir()
    (raiz / "README.md").write_text("# Proyecto\n", encoding="utf-8")
    return raiz


@pytest.fixture
def identidad() -> Humano:
    """Humano que contesta nombre y email si se los piden, y omite el remoto."""
    return Humano("Prueba", "prueba@ejemplo.invalid", "")


@pytest.fixture
def remoto_local(tmp_path) -> Path:
    """Un repositorio `--bare` que hace de GitHub sin salir a la red."""
    ruta = tmp_path / "remoto.git"
    ruta.mkdir()
    git.ejecutar(ruta, "init", "--bare")
    return ruta


# --- Validación de la URL -------------------------------------------------


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/usuario/repo.git",
        "https://github.com/usuario/repo",
        "git@github.com:usuario/repo.git",
        "ssh://git@github.com/usuario/repo.git",
        "https://gitlab.com/grupo/sub/repo.git",
        "file:///home/usuario/repos/repo.git",
        r"C:\Users\usuario\repos\repo.git",
        "/home/usuario/repos/repo.git",
    ],
)
def test_urls_validas(url):
    assert url_valida(url)


@pytest.mark.parametrize(
    "url",
    ["", "   ", "usuario/repo", "no es una url", "ftp://github.com/u/r"],
)
def test_urls_invalidas(url):
    assert not url_valida(url)


# --- Reglas de .gitignore -------------------------------------------------


def test_reglas_que_faltan_ignora_comentarios_y_blancos():
    plantilla = "# comentario\n\n__pycache__/\n.venv/\n"

    assert reglas_que_faltan("__pycache__/\n", plantilla) == [".venv/"]


def test_reglas_que_faltan_vacio_si_ya_esta_todo():
    plantilla = read_gitignore_template()

    assert reglas_que_faltan(plantilla, plantilla) == []


def test_la_plantilla_no_ignora_la_memoria_ni_la_guia():
    plantilla = read_gitignore_template()

    for linea in plantilla.splitlines():
        if linea.strip().startswith("#"):
            continue
        assert "_persistence" not in linea
        assert "_guideline" not in linea


# --- Bootstrap: el camino completo ----------------------------------------


def test_deja_repositorio_con_commit_y_publica(proyecto, remoto_local):
    humano = Humano("Prueba", "prueba@ejemplo.invalid", str(remoto_local))
    salida = Salida()

    assert bootstrap(proyecto, humano, salida) is True

    assert git.es_repositorio(proyecto)
    assert (proyecto / GITIGNORE_FILENAME).exists()
    assert git.url_del_remoto(proyecto) == str(remoto_local)
    assert MENSAJE_COMMIT_INICIAL in git.ejecutar(proyecto, "log", "-1", "--pretty=%s")
    # El remoto recibió la rama: el push ocurrió de verdad. Se consulta la rama
    # por su nombre y no HEAD, porque el HEAD de un repositorio `--bare` recién
    # creado apunta a la rama que le tocara por defecto, no a la que recibe.
    rama = git.rama_actual(proyecto)
    assert git.ejecutar(remoto_local, "log", "-1", "--pretty=%s", rama) == (
        MENSAJE_COMMIT_INICIAL
    )


def test_el_readme_del_proyecto_queda_versionado(proyecto, remoto_local):
    humano = Humano("Prueba", "prueba@ejemplo.invalid", str(remoto_local))

    bootstrap(proyecto, humano, Salida())

    assert "README.md" in git.ejecutar(proyecto, "ls-files")


def test_sin_url_queda_en_local_pero_con_commit(proyecto, identidad):
    salida = Salida()

    assert bootstrap(proyecto, identidad, salida) is False

    assert git.es_repositorio(proyecto)
    assert MENSAJE_COMMIT_INICIAL in git.ejecutar(proyecto, "log", "-1", "--pretty=%s")
    assert git.url_del_remoto(proyecto) is None
    assert "solo en local" in salida.texto or "local" in salida.texto


def test_una_url_con_mala_forma_se_repregunta(proyecto, remoto_local):
    humano = Humano("Prueba", "prueba@ejemplo.invalid", "no-es-url", str(remoto_local))
    salida = Salida()

    assert bootstrap(proyecto, humano, salida) is True
    assert "no tiene forma de URL" in salida.texto


# --- Idempotencia y no destrucción ----------------------------------------


def test_repetirlo_no_rompe_nada(proyecto, remoto_local):
    humano = Humano("Prueba", "prueba@ejemplo.invalid", str(remoto_local))
    bootstrap(proyecto, humano, Salida())
    commit_inicial = git.ejecutar(proyecto, "rev-parse", "HEAD")

    salida = Salida()
    assert bootstrap(proyecto, Humano(str(remoto_local)), salida) is True

    # Ni un commit nuevo (no había cambios) ni un repositorio distinto.
    assert git.ejecutar(proyecto, "rev-parse", "HEAD") == commit_inicial
    assert "ya era un repositorio" in salida.texto


def test_no_sobrescribe_un_gitignore_existente(proyecto, identidad):
    (proyecto / GITIGNORE_FILENAME).write_text("mi-regla-propia/\n", encoding="utf-8")

    salida = Salida()
    bootstrap(proyecto, identidad, salida)

    contenido = (proyecto / GITIGNORE_FILENAME).read_text(encoding="utf-8")
    assert contenido == "mi-regla-propia/\n"
    assert "no se toca" in salida.texto
    assert "__pycache__/" in salida.texto  # propone lo que falta


def test_no_reapunta_un_remoto_existente_sin_permiso(proyecto, remoto_local):
    git.ejecutar(proyecto, "init")
    git.ejecutar(proyecto, "remote", "add", "origin", "https://github.com/otro/repo.git")

    # Nombre, email, URL nueva, y "n" a la pregunta de reapuntar.
    humano = Humano("Prueba", "prueba@ejemplo.invalid", str(remoto_local), "n")
    salida = Salida()

    assert bootstrap(proyecto, humano, salida) is False
    assert git.url_del_remoto(proyecto) == "https://github.com/otro/repo.git"
    assert "se conserva el actual" in salida.texto


def test_reapunta_el_remoto_si_el_humano_acepta(proyecto, remoto_local):
    git.ejecutar(proyecto, "init")
    git.ejecutar(proyecto, "remote", "add", "origin", "https://github.com/otro/repo.git")

    humano = Humano("Prueba", "prueba@ejemplo.invalid", str(remoto_local), "s")

    assert bootstrap(proyecto, humano, Salida()) is True
    assert git.url_del_remoto(proyecto) == str(remoto_local)


# --- Identidad de git (L-002) ---------------------------------------------


def test_pregunta_la_identidad_si_falta_y_la_fija_local(proyecto):
    humano = Humano("Ada Lovelace", "ada@ejemplo.invalid", "")

    bootstrap(proyecto, humano, Salida())

    assert git.configuracion(proyecto, "user.name") == "Ada Lovelace"
    assert any("user.name" in p for p in humano.preguntas)


def test_sin_identidad_no_confirma_pero_deja_el_repositorio(proyecto):
    humano = Humano("", "")
    salida = Salida()

    assert bootstrap(proyecto, humano, salida) is False

    assert git.es_repositorio(proyecto)
    assert "sin identidad" in salida.texto
    # No hay commits: `rev-parse HEAD` falla porque HEAD no apunta a nada.
    assert git.intentar(proyecto, "rev-parse", "HEAD").returncode != 0


def test_no_pregunta_la_identidad_si_ya_esta_configurada(proyecto):
    git.ejecutar(proyecto, "init")
    git.fijar_configuracion(proyecto, "user.name", "Ya Configurado")
    git.fijar_configuracion(proyecto, "user.email", "ya@ejemplo.invalid")

    humano = Humano("")
    bootstrap(proyecto, humano, Salida())

    assert not any("user.name" in p for p in humano.preguntas)


# --- Fallos ---------------------------------------------------------------


def test_un_push_fallido_se_reporta_entero_y_no_se_fuerza(proyecto, tmp_path):
    inexistente = tmp_path / "no-existe.git"
    humano = Humano("Prueba", "prueba@ejemplo.invalid", f"https://ejemplo.invalid/{inexistente.name}")
    salida = Salida()

    assert bootstrap(proyecto, humano, salida) is False

    assert "Push        FALLÓ" in salida.texto
    # El commit local sobrevive: un push fallido no deshace el trabajo.
    assert MENSAJE_COMMIT_INICIAL in git.ejecutar(proyecto, "log", "-1", "--pretty=%s")


def test_error_si_el_directorio_no_existe(tmp_path):
    with pytest.raises(NotADirectoryError):
        bootstrap(tmp_path / "no-existe", Humano(), Salida())


def test_sin_terminal_lo_dice_en_vez_de_reventar(proyecto):
    """Con la entrada redirigida, `input()` lanza EOFError; no debe escaparse."""

    def sin_stdin(pregunta: str) -> str:
        raise EOFError("EOF when reading a line")

    with pytest.raises(SinCanalConElHumanoError, match="terminal interactiva"):
        bootstrap(proyecto, sin_stdin, Salida())
