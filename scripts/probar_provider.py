"""Prueba manual end-to-end del provider contra el CLI `claude` real (T-003).

Los tests de `tests/test_provider.py` mockean el subproceso: verifican que el
código hace lo que asumimos, no que la asunción sea cierta. Este script cierra
ese hueco invocando el CLI de verdad.

No es parte de la suite automatizada a propósito: consume la suscripción, tarda
segundos, exige el CLI instalado y autenticado, y su salida no es determinista.

Es andamiaje de construcción, no producto: vive en la raíz del repo, fuera de
`src/soda/` (C-003).

Uso:
    python scripts/probar_provider.py
    python scripts/probar_provider.py "explícame qué es un subproceso en una frase"
    python scripts/probar_provider.py --archivo prompt_largo.txt --timeout 120
"""

import argparse
import sys
import time
from pathlib import Path

# En Windows, Python escribe stdout en cp1252 por defecto: sin esto el propio
# script corrompe (o hace reventar con UnicodeEncodeError) el texto que está
# intentando verificar. El provider entrega UTF-8 correcto; el problema es solo
# de presentación, pero una herramienta de diagnóstico no puede mentir.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Permite ejecutar el script sin instalar el paquete (`python scripts/...`).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from soda.core.provider import ProviderError  # noqa: E402
from soda.providers import ClaudeCLIProvider  # noqa: E402

PROMPT_POR_DEFECTO = "Responde únicamente con la palabra OK, sin nada más."


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Envía un prompt a través de ClaudeCLIProvider y muestra la respuesta.",
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default=PROMPT_POR_DEFECTO,
        help="Prompt a enviar. Por defecto, una verificación corta y barata.",
    )
    parser.add_argument(
        "--archivo",
        type=Path,
        help="Lee el prompt de un archivo UTF-8 en vez del argumento. "
        "Útil para probar prompts largos (límite de línea de comandos de Windows).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="Segundos máximos de espera (por defecto: 60).",
    )
    parser.add_argument(
        "--ejecutable",
        default="claude",
        help="Nombre o ruta del CLI a invocar (por defecto: claude).",
    )
    return parser


def main() -> int:
    args = construir_parser().parse_args()

    if args.archivo:
        try:
            prompt = args.archivo.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"[ERROR] No se pudo leer {args.archivo}: {exc}", file=sys.stderr)
            return 2
    else:
        prompt = args.prompt

    provider = ClaudeCLIProvider(executable=args.ejecutable, timeout=args.timeout)

    print(f"Ejecutable : {provider.executable}")
    print(f"Timeout    : {provider.timeout} s")
    print(f"Prompt     : {len(prompt)} caracteres")
    print("-" * 72)
    print(prompt if len(prompt) <= 500 else prompt[:500] + "\n[... truncado ...]")
    print("-" * 72)

    inicio = time.monotonic()
    try:
        respuesta = provider.send(prompt)
    except ProviderError as exc:
        transcurrido = time.monotonic() - inicio
        print(f"[FALLO] {type(exc).__name__} tras {transcurrido:.1f} s", file=sys.stderr)
        print(f"        {exc}", file=sys.stderr)
        return 1

    transcurrido = time.monotonic() - inicio
    print(respuesta)
    print("-" * 72)
    print(f"[OK] {len(respuesta)} caracteres en {transcurrido:.1f} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
