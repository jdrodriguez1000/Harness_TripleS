"""Prompts de los agentes del harness, uno por archivo Markdown.

Viven en archivos y no en cadenas dentro del código por dos razones. Un prompt
es texto que se lee, se discute y se corrige como cualquier otro documento del
producto, y empotrarlo en un `.py` lo vuelve incómodo de las tres cosas. Y
porque el prompt es lo único del agente que no depende del proveedor: el mismo
archivo tiene que servir cuando detrás haya Claude, Codex o una API.

El acceso va por `importlib.resources`, igual que en `soda.templates` y por el
mismo motivo: el paquete puede quedar instalado comprimido o fuera del árbol de
fuentes.
"""

from importlib.resources import files

__all__ = ["PROMPT_FILENAMES", "read_prompt"]

#: Los prompts que trae el paquete.
PROMPT_FILENAMES: tuple[str, ...] = ("sesion_starter.md",)


def read_prompt(nombre: str) -> str:
    """Devuelve el contenido UTF-8 del prompt `nombre`.

    Args:
        nombre: Nombre del archivo, uno de `PROMPT_FILENAMES`.

    Returns:
        El texto del prompt.

    Raises:
        KeyError: Si `nombre` no es un prompt conocido.
    """
    if nombre not in PROMPT_FILENAMES:
        raise KeyError(
            f"'{nombre}' no es un prompt del paquete. "
            f"Conocidos: {', '.join(PROMPT_FILENAMES)}"
        )
    return (files(__package__) / nombre).read_text(encoding="utf-8")
