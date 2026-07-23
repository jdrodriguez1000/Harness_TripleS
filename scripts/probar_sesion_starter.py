"""Prueba manual end-to-end de `sesion-starter` contra el CLI real (T-012).

Los tests de `tests/test_sesion_starter.py` usan un `Provider` falso: verifican
que el agente compone el prompt correcto, no que un modelo produzca un informe
útil con él. Este script cierra ese hueco.

El banco de pruebas por defecto es la memoria de este mismo repositorio
(`900_persistence/`), que es contenido auténtico de varias sesiones de trabajo
— exactamente la razón por la que D-028 puso a este agente el segundo. Es el
único uso legítimo de `900_persistence/` desde código que toca `soda`, y es
legítimo porque este script es andamiaje de construcción y no producto (C-001,
C-003): vive fuera de `src/soda/` y nada del paquete lo importa.

Para leerlo, el script copia la memoria a un directorio temporal con el nombre
que la convención espera (`_persistence/`). Así el agente ve un proyecto destino
normal y no hay ninguna ruta del harness cableada en el paquete.

No es parte de la suite automatizada: consume la suscripción y su salida no es
determinista.

Uso:
    python scripts/probar_sesion_starter.py
    python scripts/probar_sesion_starter.py --modelo sonnet
    python scripts/probar_sesion_starter.py --proyecto C:/ruta/a/otro/proyecto
    python scripts/probar_sesion_starter.py --solo-prompt
"""

import argparse
import shutil
import sys
import tempfile
import time
from pathlib import Path

# Ver L-003: en Windows el propio script corrompería el texto que intenta
# verificar si escribe stdout en cp1252.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Permite ejecutar el script sin instalar el paquete.
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from soda.agents.memoria import leer_memoria  # noqa: E402
from soda.agents.sesion_starter import SesionStarter, componer_prompt  # noqa: E402
from soda.core.provider import ProviderError  # noqa: E402
from soda.providers import ClaudeCLIProvider  # noqa: E402
from soda.templates import PERSISTENCE_DIRNAME  # noqa: E402

MEMORIA_DEL_HARNESS = RAIZ / "900_persistence"
MODELO_POR_DEFECTO = "haiku"


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ejecuta sesion-starter contra el CLI real y muestra el informe.",
    )
    parser.add_argument(
        "--proyecto",
        type=Path,
        help="Raíz de un proyecto destino con `_persistence/`. "
        "Por defecto usa una copia de la memoria de este repositorio.",
    )
    parser.add_argument(
        "--modelo",
        default=MODELO_POR_DEFECTO,
        help=f"Modelo a usar (por defecto: {MODELO_POR_DEFECTO}).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=180.0,
        help="Segundos máximos de espera (por defecto: 180).",
    )
    parser.add_argument(
        "--solo-prompt",
        action="store_true",
        help="Muestra el prompt compuesto y termina, sin invocar al modelo ni gastar cuota.",
    )
    return parser


def _banco_de_pruebas(destino: Path) -> Path:
    """Copia la memoria de este repo a `destino` como un proyecto destino normal."""
    if not MEMORIA_DEL_HARNESS.is_dir():
        raise FileNotFoundError(f"No existe {MEMORIA_DEL_HARNESS}")

    shutil.copytree(MEMORIA_DEL_HARNESS, destino / PERSISTENCE_DIRNAME)
    return destino


def _ejecutar(project_root: Path, args: argparse.Namespace) -> int:
    memoria = leer_memoria(project_root)
    prompt = componer_prompt(memoria)

    print(f"Proyecto   : {project_root}")
    print(f"Memoria    : {len(memoria.completos)} íntegros, {len(memoria.indices)} índices")
    if memoria.faltantes:
        print(f"Ausentes   : {', '.join(memoria.faltantes)}")
    print(f"Vacía      : {memoria.vacia}")
    print(f"Modelo     : {args.modelo}")
    print(f"Prompt     : {len(prompt)} caracteres")
    print("-" * 72)

    if args.solo_prompt:
        print(prompt)
        return 0

    provider = ClaudeCLIProvider(
        model=args.modelo,
        timeout=args.timeout,
        cwd=project_root,
    )

    inicio = time.monotonic()
    try:
        informe = SesionStarter(provider).informe(project_root)
    except ProviderError as exc:
        transcurrido = time.monotonic() - inicio
        print(f"[FALLO] {type(exc).__name__} tras {transcurrido:.1f} s", file=sys.stderr)
        print(f"        {exc}", file=sys.stderr)
        return 1

    transcurrido = time.monotonic() - inicio
    print(informe)
    print("-" * 72)
    print(f"[OK] {len(informe)} caracteres en {transcurrido:.1f} s")
    return 0


def main() -> int:
    args = construir_parser().parse_args()

    if args.proyecto:
        return _ejecutar(args.proyecto.resolve(), args)

    with tempfile.TemporaryDirectory(prefix="soda-starter-") as tmp:
        return _ejecutar(_banco_de_pruebas(Path(tmp)), args)


if __name__ == "__main__":
    raise SystemExit(main())
