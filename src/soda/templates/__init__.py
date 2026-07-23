"""Plantillas que `soda init` siembra en un proyecto destino.

Son dos, y no significan lo mismo:

- `_persistence/`: la forma vacía de los seis archivos de memoria, la misma
  estructura que el harness usa para su propia construcción, sin contenido. El
  proyecto destino la llena; es suya.
- `_guideline/`: los documentos normativos (`principles.md`, `methodology.md`,
  `agents-and-evaluation.md`), que son producto y viajan con `soda` (D-014). El
  destino los lee, no los escribe: su dueño es la versión instalada del paquete.

Esa asimetría manda en cómo `init` trata cada una (ver `soda.cli`).

El acceso va por `importlib.resources` y no por `Path(__file__).parent` porque
el paquete puede quedar instalado comprimido (zip import) o en una ruta que no
corresponde al árbol de fuentes; `files()` funciona en ambos casos.
"""

from importlib.resources import files
from importlib.resources.abc import Traversable

__all__ = [
    "GITIGNORE_FILENAME",
    "GITIGNORE_TEMPLATE",
    "GUIDELINE_DIRNAME",
    "GUIDELINE_FILENAMES",
    "PERSISTENCE_DIRNAME",
    "PERSISTENCE_FILENAMES",
    "guideline_root",
    "persistence_root",
    "read_gitignore_template",
    "read_guideline_template",
    "read_persistence_template",
]

PERSISTENCE_DIRNAME = "_persistence"

#: Los seis archivos de memoria, en el orden en que se documentan.
PERSISTENCE_FILENAMES: tuple[str, ...] = (
    "progress.md",
    "tasks.md",
    "lessons.md",
    "decisions.md",
    "constraints.md",
    "assumptions.md",
)

GUIDELINE_DIRNAME = "_guideline"

#: Los documentos normativos, en orden de lectura (los principios primero).
GUIDELINE_FILENAMES: tuple[str, ...] = (
    "principles.md",
    "methodology.md",
    "agents-and-evaluation.md",
)


#: Nombre del archivo en el proyecto destino.
GITIGNORE_FILENAME = ".gitignore"

#: Nombre dentro del paquete. No se llama `.gitignore` a propósito: un archivo
#: con ese nombre aquí dentro sería un `.gitignore` de verdad para el propio
#: repositorio del harness, no una plantilla, y afectaría a lo que git ve.
GITIGNORE_TEMPLATE = "gitignore-base.txt"


def _leer(raiz: Traversable, nombre: str, conocidas: tuple[str, ...], que: str) -> str:
    if nombre not in conocidas:
        raise KeyError(
            f"'{nombre}' no es una plantilla de {que}. Conocidas: {', '.join(conocidas)}"
        )
    return (raiz / nombre).read_text(encoding="utf-8")


def persistence_root() -> Traversable:
    """Devuelve la raíz de la plantilla `_persistence` dentro del paquete."""
    return files(__package__) / PERSISTENCE_DIRNAME


def guideline_root() -> Traversable:
    """Devuelve la raíz de la plantilla `_guideline` dentro del paquete."""
    return files(__package__) / GUIDELINE_DIRNAME


def read_persistence_template(nombre: str) -> str:
    """Devuelve el contenido UTF-8 de una plantilla de `_persistence`.

    Args:
        nombre: Nombre del archivo, uno de `PERSISTENCE_FILENAMES`.

    Returns:
        El contenido del archivo como texto.

    Raises:
        KeyError: Si `nombre` no es una plantilla conocida.
    """
    return _leer(persistence_root(), nombre, PERSISTENCE_FILENAMES, PERSISTENCE_DIRNAME)


def read_guideline_template(nombre: str) -> str:
    """Devuelve el contenido UTF-8 de un documento de `_guideline`.

    Args:
        nombre: Nombre del archivo, uno de `GUIDELINE_FILENAMES`.

    Returns:
        El contenido del archivo como texto.

    Raises:
        KeyError: Si `nombre` no es un documento conocido.
    """
    return _leer(guideline_root(), nombre, GUIDELINE_FILENAMES, GUIDELINE_DIRNAME)


def read_gitignore_template() -> str:
    """Devuelve el `.gitignore` base que `soda start` siembra en un proyecto nuevo.

    Es un punto de partida deliberadamente genérico. No ignora `_persistence/`
    ni `_guideline/`: son el estado del proyecto y tienen que viajar con el
    repositorio.
    """
    return (files(__package__) / GITIGNORE_TEMPLATE).read_text(encoding="utf-8")
