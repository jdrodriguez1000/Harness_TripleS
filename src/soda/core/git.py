"""Plomería mínima sobre el binario `git`. Python puro, sin modelo.

Git es la única operación del arnés con consecuencia irreversible, así que este
módulo se escribe con dos reglas encima:

- **Nunca destruye.** Aquí no hay `--force`, ni `reset --hard`, ni `clean`. Lo
  que este módulo no puede hacer, no puede hacerlo nadie del arnés por accidente.
- **El error viaja entero.** Cuando `git` falla, lo que dice en stderr suele ser
  la instrucción exacta para arreglarlo (una rama divergente, un remoto que no
  existe, un email bloqueado por privacidad). Traducirlo a "no se pudo hacer
  push" destruye justo la parte útil, así que `GitError` lo conserva.

Se invoca el binario como subproceso en vez de usar una biblioteca porque el
paquete no tiene dependencias (D-005) y porque el usuario puede reproducir a
mano cualquier comando que el arnés ejecute, que es lo que hace auditable una
operación irreversible.
"""

import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

__all__ = [
    "EJECUTABLE",
    "GitError",
    "GitNoDisponibleError",
    "commit",
    "configuracion",
    "ejecutar",
    "es_repositorio",
    "esta_disponible",
    "fijar_configuracion",
    "hay_algo_que_confirmar",
    "intentar",
    "rama_actual",
    "url_del_remoto",
]

EJECUTABLE = "git"
TIMEOUT = 120.0


class GitError(Exception):
    """Un comando de `git` no se pudo ejecutar o terminó en error."""

    def __init__(
        self,
        mensaje: str,
        *,
        comando: Sequence[str] = (),
        returncode: int | None = None,
        stderr: str = "",
    ) -> None:
        super().__init__(mensaje)
        self.comando = tuple(comando)
        self.returncode = returncode
        self.stderr = stderr


class GitNoDisponibleError(GitError):
    """No hay binario `git` en el PATH."""


def esta_disponible() -> bool:
    """¿Existe el binario `git` en el PATH?"""
    return shutil.which(EJECUTABLE) is not None


def intentar(project_root: Path, *argumentos: str) -> subprocess.CompletedProcess[str]:
    """Ejecuta `git <argumentos>` y devuelve el resultado sin juzgarlo.

    Para los casos en que fallar es una respuesta legítima y no un problema
    (preguntar por un remoto que quizá no existe, por ejemplo).

    Raises:
        GitNoDisponibleError: Si no hay `git` o el sistema no puede ejecutarlo.
        GitError: Si el comando no terminó dentro del tiempo permitido.
    """
    resolved = shutil.which(EJECUTABLE)
    if resolved is None:
        raise GitNoDisponibleError(
            "No se encontró `git` en el PATH. Instálalo para poder inicializar "
            "el repositorio del proyecto."
        )

    try:
        return subprocess.run(
            [resolved, *argumentos],
            cwd=project_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired as exc:
        raise GitError(
            f"`git {' '.join(argumentos)}` no terminó en {TIMEOUT} segundos.",
            comando=argumentos,
        ) from exc
    except OSError as exc:
        raise GitNoDisponibleError(f"No se pudo ejecutar `git`: {exc}") from exc


def ejecutar(project_root: Path, *argumentos: str) -> str:
    """Ejecuta `git <argumentos>` y devuelve stdout, o falla con el error de git.

    Args:
        project_root: Directorio donde se ejecuta el comando.
        argumentos: Argumentos de `git`, ya separados.

    Returns:
        Lo que git escribió en stdout, sin espacio sobrante.

    Raises:
        GitError: Si el comando terminó con código distinto de cero.
        GitNoDisponibleError: Si no hay `git` disponible.
    """
    completado = intentar(project_root, *argumentos)

    if completado.returncode != 0:
        detalle = (completado.stderr or completado.stdout or "").strip()
        raise GitError(
            f"`git {' '.join(argumentos)}` falló con código "
            f"{completado.returncode}: {detalle or 'sin detalle'}",
            comando=argumentos,
            returncode=completado.returncode,
            stderr=detalle,
        )

    return (completado.stdout or "").strip()


def es_repositorio(project_root: Path) -> bool:
    """¿`project_root` está dentro de un árbol de trabajo de git?"""
    completado = intentar(project_root, "rev-parse", "--is-inside-work-tree")
    return completado.returncode == 0 and completado.stdout.strip() == "true"


def rama_actual(project_root: Path) -> str:
    """Devuelve el nombre de la rama actual, incluso sin commits todavía."""
    return ejecutar(project_root, "branch", "--show-current")


def url_del_remoto(project_root: Path, nombre: str = "origin") -> str | None:
    """Devuelve la URL del remoto `nombre`, o `None` si no está configurado."""
    completado = intentar(project_root, "remote", "get-url", nombre)
    if completado.returncode != 0:
        return None
    return completado.stdout.strip() or None


def configuracion(project_root: Path, clave: str) -> str | None:
    """Devuelve el valor de `clave` en la configuración efectiva, o `None`."""
    completado = intentar(project_root, "config", "--get", clave)
    if completado.returncode != 0:
        return None
    return completado.stdout.strip() or None


def fijar_configuracion(project_root: Path, clave: str, valor: str) -> None:
    """Fija `clave` en la configuración **local** del repositorio.

    Local y no global a propósito: el arnés arregla el repositorio que está
    creando, no la máquina del usuario (así se resolvió L-002).
    """
    ejecutar(project_root, "config", "--local", clave, valor)


def hay_algo_que_confirmar(project_root: Path) -> bool:
    """¿Hay cambios en el índice o en el árbol de trabajo?"""
    return bool(ejecutar(project_root, "status", "--porcelain"))


def commit(project_root: Path, mensaje: str) -> None:
    """Crea un commit con `mensaje`.

    El mensaje va por `--file -` y no por `-m` para que los saltos de línea y
    los acentos sobrevivan sin depender de cómo el shell del sistema trate las
    comillas.
    """
    resolved = shutil.which(EJECUTABLE)
    if resolved is None:
        raise GitNoDisponibleError("No se encontró `git` en el PATH.")

    completado = subprocess.run(
        [resolved, "commit", "--file", "-"],
        cwd=project_root,
        input=mensaje,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=TIMEOUT,
    )

    if completado.returncode != 0:
        detalle = (completado.stderr or completado.stdout or "").strip()
        raise GitError(
            f"`git commit` falló con código {completado.returncode}: {detalle}",
            comando=("commit",),
            returncode=completado.returncode,
            stderr=detalle,
        )
