#!/usr/bin/env python3
"""Spike (C-003, no producto): ¿autentica el Claude Agent SDK con la SUSCRIPCIÓN?

Punto crítico 2 de T-020. Antes de comprometer la arquitectura del Camino B
(D-036) hay que verificar en real que el `claude-agent-sdk` habla con el modelo
usando el OAuth de `claude /login` —la suscripción Pro/Max— y NO la API de pago
por token. La documentación del SDK confirma la precedencia de credenciales: si
no hay `ANTHROPIC_API_KEY` ni `CLAUDE_CODE_OAUTH_TOKEN` ni un `CLAUDE_CONFIG_DIR`
propio, cae en las credenciales OAuth de `~/.claude/.credentials.json`.

Este script hace lo mínimo: un solo `query()` trivial e imprime cada mensaje del
stream con su tipo. Si responde sin `ANTHROPIC_API_KEY` en el entorno, la
suscripción quedó verificada. Reutiliza la política de `ClaudeCLIProvider`
(L-014): borrar las variables de API del entorno antes de invocar al SDK, para
que la suscripción sea garantizada y no meramente esperada.

Uso:
    .venv\\Scripts\\python.exe scripts\\probar_agent_sdk.py
"""

import os
import sys

# Borrar las credenciales de API ANTES de importar el SDK, por si las leyera al
# cargarse. Misma política que ClaudeCLIProvider.VARIABLES_DE_API.
for _variable in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
    os.environ.pop(_variable, None)

import anyio  # noqa: E402
from claude_agent_sdk import (  # noqa: E402
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)


def _forzar_utf8() -> None:
    """Fuerza UTF-8 en los flujos estándar (necesario en Windows, ver L-003)."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass


async def _correr() -> None:
    tenia_api_key = "ANTHROPIC_API_KEY" in os.environ  # ya la borramos; debe ser False
    print(f"ANTHROPIC_API_KEY presente en el entorno: {tenia_api_key}")
    print("Enviando un query() trivial al SDK…\n")

    options = ClaudeAgentOptions(model="haiku")

    async for mensaje in query(prompt="Responde solo con: hola", options=options):
        tipo = type(mensaje).__name__
        if isinstance(mensaje, AssistantMessage):
            for bloque in mensaje.content:
                if isinstance(bloque, TextBlock):
                    print(f"[{tipo}] texto: {bloque.text!r}")
                else:
                    print(f"[{tipo}] bloque: {type(bloque).__name__}")
        elif isinstance(mensaje, ResultMessage):
            print(f"[{tipo}] fin. is_error={mensaje.is_error}")
        else:
            print(f"[{tipo}]")

    print("\nOK: el SDK respondió usando la suscripción (sin ANTHROPIC_API_KEY).")


def main() -> int:
    _forzar_utf8()
    try:
        anyio.run(_correr)
    except Exception as exc:  # noqa: BLE001 — spike: queremos ver cualquier fallo
        print(f"\n[error] {type(exc).__name__}: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
