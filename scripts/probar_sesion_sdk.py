#!/usr/bin/env python3
"""Spike de verificación (C-003, no producto): ¿mantiene contexto la sesión?

Criterio de aceptación de T-021. `SesionClaudeSDK` (detrás de `ClaudeSDKProvider`)
envuelve un `ClaudeSDKClient` vivo que debería conservar el contexto entre turnos.
Este script lo demuestra sobre la SUSCRIPCIÓN real: encadena tres turnos donde los
dos últimos solo se pueden responder recordando el primero.

  Turno 1: se le da un nombre y un color.
  Turno 2: se le pregunta el nombre  → debe responder "Juan".
  Turno 3: se le pregunta el color   → debe responder "verde".

Si los turnos 2 y 3 aciertan, la persistencia de sesión quedó verificada. A
diferencia del spike de T-020 (`chat_delegacion_sdk.py`, un `query()` por turno,
sin memoria), aquí es un único cliente reusado: eso es lo que se prueba.

Requiere `claude /login` (suscripción, D-031); no usa `ANTHROPIC_API_KEY`.

Uso:
    .venv\\Scripts\\python.exe scripts\\probar_sesion_sdk.py
"""

import os
import sys

# Coherente con la política de suscripción: fuera credenciales de API del entorno
# de este proceso antes de tocar el SDK (D-031). El provider además las neutraliza
# en el subproceso, pero limpiar aquí evita cualquier lectura temprana.
for _variable in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
    os.environ.pop(_variable, None)

import anyio  # noqa: E402

from soda.providers import ClaudeSDKProvider  # noqa: E402

PROMPT_SISTEMA = (
    "Eres un asistente en español. Responde siempre breve y al grano, en una sola "
    "frase corta."
)

TURNOS = [
    "Recuerda estos datos: me llamo Juan y mi color favorito es el verde.",
    "¿Cómo me llamo?",
    "¿Y cuál es mi color favorito?",
]


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
    print(f"ANTHROPIC_API_KEY presente: {'ANTHROPIC_API_KEY' in os.environ}")
    print("Abriendo una sesión persistente y encadenando 3 turnos…\n")

    provider = ClaudeSDKProvider(model="haiku", system_prompt=PROMPT_SISTEMA)
    async with provider.abrir_sesion() as sesion:
        for i, turno in enumerate(TURNOS, start=1):
            print(f"Tú (turno {i})> {turno}")
            respuesta = await sesion.enviar(turno)
            print(f"Claude> {respuesta}\n")

    print(
        "Verificación: si el turno 2 dijo 'Juan' y el turno 3 dijo 'verde', "
        "la sesión mantuvo el contexto. T-021 OK."
    )


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
