#!/usr/bin/env python3
"""Chat interactivo mínimo contra la suscripción, vía el binario `claude`.

Spike de exploración (C-003), no producto: valida que se puede construir un
bucle REPL **propio** —nuestro código controla el bucle, la entrada de terminal
y el historial de la conversación— usando la **suscripción** a través de
`claude -p`, sin SDK, sin API de pago por token y sin construir sobre el harness
de Claude Code como orquestador.

El binario `claude` es la única vía a la suscripción; aquí se usa solo como
"conexión al modelo" (un turno, sin herramientas). El bucle, la interacción y la
memoria de conversación viven en este script. Reutiliza `ClaudeCLIProvider`, que
ya fuerza la suscripción borrando las credenciales de API del entorno.

Uso:
    python scripts/chat.py                 # modelo sonnet por defecto
    python scripts/chat.py --modelo haiku
    (Ctrl-D o /salir para terminar.)
"""

import argparse
import sys

from soda.core.provider import ProviderError
from soda.providers import ClaudeCLIProvider

PREAMBULO = (
    "Eres un asistente conversacional. Responde en español al último turno del "
    "Humano, teniendo en cuenta la conversación previa si la hay. Responde solo "
    "con tu mensaje, sin prefijos ni etiquetas."
)

SALIDAS = {"/salir", "/exit", "/quit"}


def _forzar_utf8() -> None:
    """Fuerza UTF-8 en los flujos estándar (necesario en Windows, ver L-003)."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass


def componer(historial: list[tuple[str, str]], mensaje: str) -> str:
    """Arma el prompt de un turno: preámbulo + historial + mensaje nuevo.

    El historial se re-envía completo cada turno —el bucle es nuestro, no del
    binario— porque `claude -p` es de un solo disparo y no recuerda nada.
    """
    lineas = [PREAMBULO, "", "## Conversación"]
    for quien, texto in historial:
        etiqueta = "Humano" if quien == "humano" else "Asistente"
        lineas.append(f"{etiqueta}: {texto}")
    lineas.append(f"Humano: {mensaje}")
    lineas.append("")
    lineas.append("Responde ahora, como Asistente, al último turno del Humano.")
    return "\n".join(lineas)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Chat interactivo sobre la suscripción."
    )
    parser.add_argument(
        "--modelo", default="sonnet", help="Alias del modelo (por defecto: sonnet)."
    )
    parser.add_argument(
        "--timeout", type=float, default=300.0, help="Segundos máximos por respuesta."
    )
    args = parser.parse_args(argv)

    _forzar_utf8()

    provider = ClaudeCLIProvider(model=args.modelo, timeout=args.timeout, tools=())
    historial: list[tuple[str, str]] = []

    print(
        f"Chat sobre la suscripción · modelo {args.modelo} · "
        "Ctrl-D o /salir para terminar.\n"
    )

    while True:
        try:
            mensaje = input("Tú> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not mensaje:
            continue
        if mensaje in SALIDAS:
            break

        try:
            respuesta = provider.send(componer(historial, mensaje))
        except ProviderError as exc:
            print(f"\n[error] {exc}\n")
            continue

        print(f"\nClaude> {respuesta}\n")
        historial.append(("humano", mensaje))
        historial.append(("asistente", respuesta))

    print("Hasta luego.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
