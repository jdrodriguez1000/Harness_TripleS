"""Plantillas que `soda init` siembra en un proyecto destino.

La plantilla de `_persistence/` es la forma vacía de los seis archivos de
memoria: la misma estructura que el harness usa para su propia construcción,
sin contenido.

El acceso va por `importlib.resources` y no por `Path(__file__).parent` porque
el paquete puede quedar instalado comprimido (zip import) o en una ruta que no
corresponde al árbol de fuentes; `files()` funciona en ambos casos.
"""

from importlib.resources import files
from importlib.resources.abc import Traversable

__all__ = [
    "PERSISTENCE_DIRNAME",
    "PERSISTENCE_FILENAMES",
    "persistence_root",
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


def persistence_root() -> Traversable:
    """Devuelve la raíz de la plantilla `_persistence` dentro del paquete."""
    return files(__package__) / PERSISTENCE_DIRNAME


def read_persistence_template(nombre: str) -> str:
    """Devuelve el contenido UTF-8 de una plantilla de `_persistence`.

    Args:
        nombre: Nombre del archivo, uno de `PERSISTENCE_FILENAMES`.

    Returns:
        El contenido del archivo como texto.

    Raises:
        KeyError: Si `nombre` no es una plantilla conocida.
    """
    if nombre not in PERSISTENCE_FILENAMES:
        conocidas = ", ".join(PERSISTENCE_FILENAMES)
        raise KeyError(
            f"'{nombre}' no es una plantilla de _persistence. Conocidas: {conocidas}"
        )
    return (persistence_root() / nombre).read_text(encoding="utf-8")
