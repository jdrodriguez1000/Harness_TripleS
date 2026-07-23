#!/usr/bin/env python3
"""Spike de verificación (C-003, no producto): ¿conversa el REPL manteniendo contexto?

Criterio de aceptación de T-022. `correr_repl` enciende la sesión persistente del
orquestador (T-021), lee lo que tecleas, se lo envía y muestra la respuesta,
turno a turno, hasta que cierras con `/salir`, EOF (Ctrl-Z + Enter en Windows) o
Ctrl-C. Este script lo corre sobre la SUSCRIPCIÓN real leyendo de stdin de verdad.

Cómo verificarlo a mano: teclea un dato en el primer turno y pregúntalo en el
segundo. Si lo recuerda, el REPL sostiene el contexto vivo de la sesión.

  Tú> me llamo Juan y trabajo en el proyecto Harness
  Tú> ¿cómo me llamo y en qué proyecto trabajo?   → debe recordarlo
  Tú> /salir                                        → cierra sin traza

Requiere `claude /login` (suscripción, D-031); no usa `ANTHROPIC_API_KEY`.

Uso:
    .venv\\Scripts\\python.exe scripts\\probar_repl.py
"""

import os
import sys

# Política de suscripción: fuera credenciales de API del entorno de este proceso
# antes de tocar el SDK (D-031). El provider además las neutraliza en el subproceso.
for _variable in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
    os.environ.pop(_variable, None)

from pathlib import Path  # noqa: E402

import anyio  # noqa: E402

from soda.core.flota import ORQUESTADOR, proveedor_de_sesion_para  # noqa: E402
from soda.repl import correr_repl  # noqa: E402

SALUDO = (
    "Sesión del orquestador abierta. Escribe un turno y pulsa Enter; `/salir` cierra.\n"
    "Prueba: da un dato en un turno y pregúntalo en el siguiente para ver si lo recuerda."
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
    proveedor = proveedor_de_sesion_para(ORQUESTADOR, Path.cwd())
    async with proveedor.abrir_sesion() as sesion:
        await correr_repl(sesion, saludo=SALUDO)


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
