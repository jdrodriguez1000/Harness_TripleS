"""Lectura de la memoria de un proyecto destino. Python puro, sin modelo.

Es la mitad barata de `sesion-starter`: saber qué dicen los seis archivos de
`_persistence/` no requiere un LLM, porque sus nombres y su estructura son
convención fijada por `soda init`. Darle herramientas de lectura al agente para
que descubra rutas que el script ya conoce sería pagar cuota por nada.

Los seis archivos no se tratan igual, siguiendo el protocolo del prototipo:

- `progress.md` y `tasks.md` son **lectura obligatoria** y viajan íntegros.
- Los otros cuatro viajan solo con su **sección de índice**. Es deliberado y
  barato a la vez: por convención del proyecto el índice es la interfaz de
  búsqueda —debe bastar leerlo para localizar información sin recorrer el
  archivo entero—, así que enviar el índice le dice al agente qué existe sin
  gastar el contexto que costaría enviar el detalle. Los cuatro archivos suman
  varias decenas de miles de caracteres; sus índices, unos pocos miles.

Detectar que la memoria está **vacía** también es trabajo de aquí, y también sin
modelo: un archivo idéntico a la plantilla que sembró `soda init` es un archivo
que nadie ha escrito. Ante cualquier duda el resultado se inclina a "hay
estado", porque tratar un proyecto con historia como si fuera nuevo es el error
caro y tratar uno nuevo como si tuviera historia solo produce un informe que
dice que no hay nada.

Sobre C-002: `project_root` es siempre explícito y nunca se deduce.
"""

from dataclasses import dataclass
from pathlib import Path

from soda.templates import (
    PERSISTENCE_DIRNAME,
    PERSISTENCE_FILENAMES,
    read_persistence_template,
)

__all__ = [
    "BAJO_DEMANDA",
    "OBLIGATORIOS",
    "MemoriaAusenteError",
    "MemoriaProyecto",
    "extraer_indice",
    "leer_memoria",
]

#: Los que el protocolo de inicio manda leer siempre, íntegros.
OBLIGATORIOS: tuple[str, ...] = ("progress.md", "tasks.md")

#: El resto, en el orden canónico: viajan solo con su índice.
BAJO_DEMANDA: tuple[str, ...] = tuple(
    nombre for nombre in PERSISTENCE_FILENAMES if nombre not in OBLIGATORIOS
)

TITULO_INDICE = "## Índice"


class MemoriaAusenteError(Exception):
    """El proyecto destino no tiene carpeta de memoria."""


@dataclass(frozen=True)
class MemoriaProyecto:
    """Lo que el arnés sabe de un proyecto destino antes de invocar a nadie."""

    project_root: Path
    #: Contenido íntegro de los archivos de lectura obligatoria.
    completos: dict[str, str]
    #: Sección de índice de los archivos de lectura bajo demanda.
    indices: dict[str, str]
    #: Archivos declarados por la convención que no están en el disco.
    faltantes: tuple[str, ...]
    #: Verdadero solo si nadie ha escrito todavía la memoria obligatoria.
    vacia: bool


def _normalizar(texto: str) -> str:
    """Deja el texto comparable entre plataformas y editores.

    Unifica los finales de línea (Windows entrega CRLF donde el paquete guarda
    LF) y descarta el espacio final de cada línea y del archivo, que ningún
    editor mantiene de forma consistente y que no cambia lo que el archivo dice.
    """
    lineas = texto.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    return "\n".join(linea.rstrip() for linea in lineas).strip()


def extraer_indice(contenido: str) -> str:
    """Devuelve la sección `## Índice` de un archivo de memoria.

    La sección va desde su encabezado hasta el siguiente encabezado de nivel 2,
    que por convención es el detalle. Si el archivo no tiene índice —porque el
    proyecto destino se salió de la convención— se devuelve cadena vacía en vez
    de fallar: un índice ausente es información para el informe, no un motivo
    para tumbar el arranque de la sesión.

    Args:
        contenido: Texto completo de un archivo de memoria.

    Returns:
        La sección de índice sin espacio sobrante, o `""` si no la hay.
    """
    lineas = _normalizar(contenido).split("\n")

    try:
        inicio = next(
            i for i, linea in enumerate(lineas) if linea.strip() == TITULO_INDICE
        )
    except StopIteration:
        return ""

    fin = len(lineas)
    for i in range(inicio + 1, len(lineas)):
        if lineas[i].startswith("## "):
            fin = i
            break

    return "\n".join(lineas[inicio:fin]).strip()


def _es_plantilla(nombre: str, contenido: str) -> bool:
    """¿Este archivo sigue siendo la plantilla que sembró `soda init`?"""
    try:
        plantilla = read_persistence_template(nombre)
    except KeyError:
        return False
    return _normalizar(contenido) == _normalizar(plantilla)


def leer_memoria(project_root: Path) -> MemoriaProyecto:
    """Lee `_persistence/` dentro de `project_root` y resume lo que hay.

    Args:
        project_root: Raíz del proyecto destino.

    Returns:
        Una `MemoriaProyecto` con los obligatorios íntegros, los índices de los
        demás, los archivos que falten y si la memoria está sin escribir.

    Raises:
        MemoriaAusenteError: Si no existe `_persistence/` en `project_root`.
        OSError: Si un archivo existe pero no se puede leer.
    """
    raiz = project_root / PERSISTENCE_DIRNAME
    if not raiz.is_dir():
        raise MemoriaAusenteError(
            f"'{project_root}' no tiene carpeta '{PERSISTENCE_DIRNAME}'. "
            "Ejecuta `soda init` en el proyecto antes de arrancar una sesión."
        )

    completos: dict[str, str] = {}
    indices: dict[str, str] = {}
    faltantes: list[str] = []
    sin_escribir: list[bool] = []

    for nombre in PERSISTENCE_FILENAMES:
        ruta = raiz / nombre
        if not ruta.is_file():
            faltantes.append(nombre)
            continue

        contenido = ruta.read_text(encoding="utf-8")
        if nombre in OBLIGATORIOS:
            completos[nombre] = contenido
            sin_escribir.append(_es_plantilla(nombre, contenido))
        else:
            indices[nombre] = extraer_indice(contenido)

    # Vacía solo si están los dos obligatorios y ninguno se ha tocado. Que falte
    # uno es una anomalía, no un proyecto nuevo: se reporta y se sigue por la
    # rama de "hay estado", que es la que no destruye nada.
    vacia = len(sin_escribir) == len(OBLIGATORIOS) and all(sin_escribir)

    return MemoriaProyecto(
        project_root=project_root,
        completos=completos,
        indices=indices,
        faltantes=tuple(faltantes),
        vacia=vacia,
    )
