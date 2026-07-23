"""CLI del harness: un solo comando `soda` con subcomandos (D-002).

Por ahora expone dos. `init` siembra en un proyecto destino las dos plantillas
del paquete: `_persistence/` (memoria vacía) y `_guideline/` (los documentos
normativos, que son producto — D-014). `start` arranca una sesión de trabajo,
eligiendo rama según lo que diga la memoria (ver `soda.start`).

Las dos se siembran, pero no se tratan igual, porque no son la misma clase de
archivo. La memoria es del proyecto destino: si ya existe, se salta y punto —
sobrescribirla borraría trabajo. La guía es del paquete: si ya existe y es
idéntica no hay nada que decir, pero si difiere de la versión instalada eso es
información que el usuario necesita (típicamente, una copia vieja de una
actualización anterior de `soda`). Tampoco se toca sin `--force`, pero se
reporta como DIFIERE en vez de esconderse bajo "saltado".

Sobre C-002: la restricción exige que toda función del harness reciba
`project_root` de forma explícita, y así es —`init_persistence` e
`init_guideline` lo piden siempre. El valor por defecto (el directorio actual)
se resuelve aquí, en la frontera de la CLI, y se convierte en ruta absoluta
antes de llamar a nada. La comodidad vive en la interfaz; el código de dentro
sigue siendo explícito.
"""

import argparse
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

import anyio

from soda.agents.memoria import MemoriaAusenteError, leer_memoria
from soda.agents.sesion_starter import SesionStarter
from soda.core import git
from soda.core.flota import ORQUESTADOR, proveedor_de_sesion_para, proveedor_para
from soda.core.provider import ProviderError
from soda.repl import correr_repl
from soda.start import SinCanalConElHumanoError, bootstrap
from soda.templates import (
    GUIDELINE_DIRNAME,
    GUIDELINE_FILENAMES,
    PERSISTENCE_DIRNAME,
    PERSISTENCE_FILENAMES,
    read_guideline_template,
    read_persistence_template,
)

__all__ = [
    "CREADO",
    "DIFIERE",
    "SALTADO",
    "SOBRESCRITO",
    "init_guideline",
    "init_persistence",
    "main",
]

AGENTE_STARTER = "sesion-starter"

CREADO = "creado"
SALTADO = "existe, saltado"
SOBRESCRITO = "sobrescrito"
DIFIERE = "difiere, saltado"


def _exigir_directorio(project_root: Path) -> None:
    if not project_root.is_dir():
        raise NotADirectoryError(
            f"'{project_root}' no existe o no es un directorio. "
            "`init` siembra la memoria dentro de un proyecto ya existente; "
            "no crea el proyecto."
        )


def _sembrar(
    project_root: Path,
    dirname: str,
    filenames: Sequence[str],
    leer_plantilla: Callable[[str], str],
    force: bool,
    marcar_diferencias: bool,
) -> list[tuple[str, str]]:
    """Copia `filenames` a `project_root / dirname` sin destruir nada sin `force`."""
    _exigir_directorio(project_root)

    destino = project_root / dirname
    destino.mkdir(exist_ok=True)

    resultados: list[tuple[str, str]] = []
    for nombre in filenames:
        ruta = destino / nombre
        plantilla = leer_plantilla(nombre)
        ya_estaba = ruta.exists()

        if ya_estaba and not force:
            difiere = (
                marcar_diferencias and ruta.read_text(encoding="utf-8") != plantilla
            )
            resultados.append((nombre, DIFIERE if difiere else SALTADO))
            continue

        ruta.write_text(plantilla, encoding="utf-8")
        resultados.append((nombre, SOBRESCRITO if ya_estaba else CREADO))

    return resultados


def init_persistence(project_root: Path, force: bool = False) -> list[tuple[str, str]]:
    """Siembra la plantilla de `_persistence` dentro de `project_root`.

    Nunca destruye contenido: un archivo que ya existe se salta, salvo que
    `force` sea verdadero. Es idempotente — repetir la llamada solo completa lo
    que falte.

    Un archivo de memoria existente se reporta siempre como saltado, sin
    compararlo con la plantilla: que difiera es lo normal y lo deseable, porque
    la memoria la escribe el proyecto destino.

    Args:
        project_root: Raíz del proyecto destino. Debe existir y ser directorio.
        force: Si es verdadero, sobrescribe los archivos existentes.

    Returns:
        Una lista de `(nombre de archivo, acción)` en el orden canónico.

    Raises:
        NotADirectoryError: Si `project_root` no existe o no es un directorio.
        OSError: Si no se pudo crear o escribir en el destino.
    """
    return _sembrar(
        project_root,
        PERSISTENCE_DIRNAME,
        PERSISTENCE_FILENAMES,
        read_persistence_template,
        force=force,
        marcar_diferencias=False,
    )


def init_guideline(project_root: Path, force: bool = False) -> list[tuple[str, str]]:
    """Siembra los documentos normativos (`_guideline`) dentro de `project_root`.

    Mismas garantías que `init_persistence` —no destruye sin `force`, es
    idempotente— con una diferencia: un documento que ya existe pero no coincide
    con el que trae el paquete se reporta como `DIFIERE`, no como `SALTADO`. La
    guía la posee la versión instalada de `soda`, así que una copia divergente
    en el destino es casi siempre una copia vieja, y saltarla en silencio la
    dejaría desactualizada para siempre.

    Args:
        project_root: Raíz del proyecto destino. Debe existir y ser directorio.
        force: Si es verdadero, sobrescribe los documentos existentes.

    Returns:
        Una lista de `(nombre de archivo, acción)` en el orden canónico.

    Raises:
        NotADirectoryError: Si `project_root` no existe o no es un directorio.
        OSError: Si no se pudo crear o escribir en el destino.
    """
    return _sembrar(
        project_root,
        GUIDELINE_DIRNAME,
        GUIDELINE_FILENAMES,
        read_guideline_template,
        force=force,
        marcar_diferencias=True,
    )


def _resumir(resultados: Sequence[tuple[str, str]]) -> str:
    """Arma la línea de resumen a partir de las acciones ejecutadas."""
    partes = []
    for accion, singular, plural in (
        (CREADO, "creado", "creados"),
        (SOBRESCRITO, "sobrescrito", "sobrescritos"),
    ):
        cuantos = sum(1 for _, hecho in resultados if hecho == accion)
        if cuantos:
            partes.append(f"{cuantos} {singular if cuantos == 1 else plural}")

    saltados = sum(1 for _, hecho in resultados if hecho in (SALTADO, DIFIERE))
    if saltados:
        partes.append(f"{saltados} sin tocar")

    return ", ".join(partes) if partes else "nada que hacer"


def _forzar_utf8() -> None:
    """Evita que Windows corrompa la salida con cp1252 (ver L-003)."""
    for flujo in (sys.stdout, sys.stderr):
        reconfigure = getattr(flujo, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def _ejecutar_init(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()

    try:
        bloques = [
            (PERSISTENCE_DIRNAME, init_persistence(project_root, force=args.force)),
            (GUIDELINE_DIRNAME, init_guideline(project_root, force=args.force)),
        ]
    except NotADirectoryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: no se pudo escribir en '{project_root}': {exc}", file=sys.stderr)
        return 1

    for dirname, resultados in bloques:
        print(f"Destino: {project_root / dirname}")
        print()
        for nombre, accion in resultados:
            print(f"  {accion:<16} {nombre}")
        print()
        print(_resumir(resultados) + ".")
        print()

    todas = [accion for _, resultados in bloques for _, accion in resultados]

    if DIFIERE in todas:
        print(
            f"Algún documento de {GUIDELINE_DIRNAME}/ no coincide con el que trae "
            "esta versión de soda: es una copia editada o de una versión anterior."
        )

    if SALTADO in todas or DIFIERE in todas:
        print("Usa --force para reemplazar los archivos existentes.")

    return 0


def _ejecutar_start(args: argparse.Namespace) -> int:
    """Elige rama según la memoria y ejecuta la que toque.

    La decisión es de Python y cuesta leer dos archivos: un proyecto sin memoria
    escrita no tiene nada que reconstruir, y preguntárselo a un modelo sería
    pagar cuota por una comparación de cadenas.
    """
    project_root = Path(args.project_root).resolve()

    try:
        memoria = leer_memoria(project_root)
    except MemoriaAusenteError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: no se pudo leer la memoria de '{project_root}': {exc}", file=sys.stderr)
        return 1

    if memoria.faltantes:
        print(f"Aviso: faltan archivos de memoria: {', '.join(memoria.faltantes)}")
        print("Ejecuta `soda init` para completarlos.")
        print()

    if memoria.vacia:
        try:
            return 0 if bootstrap(project_root) else 1
        except (SinCanalConElHumanoError, git.GitError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        except (NotADirectoryError, OSError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        except KeyboardInterrupt:
            print("\nArranque interrumpido. Nada quedó a medias en el remoto.")
            return 1

    print(f"Reanudando sesión en {project_root}")
    print(f"Consultando a {AGENTE_STARTER}...")
    print()

    try:
        informe = SesionStarter(proveedor_para(AGENTE_STARTER, project_root)).informe(
            project_root
        )
    except ProviderError as exc:
        print(f"Error: {AGENTE_STARTER} no pudo responder: {exc}", file=sys.stderr)
        return 1

    # El informe de reanudación deja de ser el final del comando y pasa a ser el
    # saludo del REPL: `soda start` ya no imprime y muere, sostiene la
    # conversación con el orquestador hasta que el humano la cierra (T-022).
    try:
        return _conversar(project_root, saludo=informe)
    except ProviderError as exc:
        print(f"Error: no se pudo abrir la sesión del orquestador: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nSesión interrumpida.")
        return 0


async def _repl_del_orquestador(project_root: Path, saludo: str) -> None:
    """Abre la sesión persistente del orquestador y le entrega el bucle REPL.

    La sesión se abre y se cierra aquí (`async with`): `correr_repl` solo la usa.
    Así el recurso del backend se libera pase lo que pase dentro del bucle.
    """
    proveedor = proveedor_de_sesion_para(ORQUESTADOR, project_root)
    async with proveedor.abrir_sesion() as sesion:
        await correr_repl(sesion, leer=input, escribir=print, saludo=saludo)


def _conversar(project_root: Path, saludo: str) -> int:
    """Frontera sync→async: enciende el bucle de eventos y corre el REPL.

    `anyio.run` es el mismo arranque validado en el spike de T-021: el SDK vive
    sobre anyio, y abrir el cliente exige un bucle de eventos vivo.
    """
    anyio.run(_repl_del_orquestador, project_root, saludo)
    return 0


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="soda",
        description="Arnés de IA que orquesta agentes mediante CLIs de suscripción.",
    )
    subcomandos = parser.add_subparsers(dest="comando")

    init = subcomandos.add_parser(
        "init",
        help="Siembra la memoria y la guía normativa en un proyecto destino.",
        description=(
            "Crea `_persistence/` con los seis archivos de memoria vacíos y "
            "`_guideline/` con los documentos normativos que trae soda."
        ),
    )
    init.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Raíz del proyecto destino (por defecto: el directorio actual).",
    )
    init.add_argument(
        "--force",
        action="store_true",
        help="Reemplaza los archivos que ya existan. Destruye memoria acumulada.",
    )

    start = subcomandos.add_parser(
        "start",
        help="Arranca una sesión de trabajo sobre un proyecto.",
        description=(
            "Si la memoria del proyecto sigue vacía, deja el proyecto listo para "
            "trabajar: repositorio git, `.gitignore`, remoto, commit inicial y push. "
            "Si ya hay memoria escrita, entrega el informe de reanudación."
        ),
    )
    start.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Raíz del proyecto destino (por defecto: el directorio actual).",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    _forzar_utf8()
    parser = construir_parser()
    args = parser.parse_args(argv)

    if args.comando == "init":
        return _ejecutar_init(args)

    if args.comando == "start":
        return _ejecutar_start(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
