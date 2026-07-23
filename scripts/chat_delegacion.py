#!/usr/bin/env python3
"""Spike: la sesión principal delega en un sub-agente 'fecha' (C-003, no producto).

Prueba la incógnita que quedaba abierta tras `chat.py`: ¿puede la **sesión
principal** (un `claude -p` sobre la suscripción) DECIDIR por su cuenta invocar a
otro agente para una tarea que no puede resolver sola?

Se elige "dar la fecha y hora" a propósito: un LLM **no** conoce la hora real —la
inventaría—, así que es el ejemplo canónico de por qué existen las herramientas.
El dato factual lo pone **código Python** (`datetime.now`); el LLM solo decide
delegar, y el sub-agente redacta el saludo.

Cómo se delega sin SDK: `claude -p` es texto-entra-texto-sale, así que no tenemos
el protocolo estructurado de tool-use del video (ese vive dentro del binario o en
el Agent SDK). Lo sustituimos por una convención: si la sesión principal decide
que necesita la fecha, responde EXACTAMENTE con el marcador `[[LLAMAR:fecha]]`.
Python lo detecta, invoca al sub-agente y devuelve su respuesta. Es el "bucle
interior a mano".

Uso:
    .venv\\Scripts\\python.exe scripts\\chat_delegacion.py
    (Escribe "dame la hora y fecha" para forzar la delegación. /salir para salir.)
"""

import sys
from datetime import datetime

from soda.core.provider import ProviderError
from soda.providers import ClaudeCLIProvider

MARCADOR = "[[LLAMAR:fecha]]"
SALIDAS = {"/salir", "/exit", "/quit"}

DIAS = [
    "lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo",
]
MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
    "septiembre", "octubre", "noviembre", "diciembre",
]

PROMPT_PRINCIPAL = (
    "Eres la sesión principal de un asistente. Tienes un ayudante al que puedes "
    "llamar:\n"
    "- `fecha`: devuelve la fecha y hora REAL actual. Tú NO conoces la hora ni la "
    "fecha; nunca las inventes.\n\n"
    "Regla estricta: si el último turno del Humano pide la fecha o la hora "
    "(de hoy, actual, ahora), responde ÚNICAMENTE con este texto exacto y nada "
    f"más:\n{MARCADOR}\n"
    "Para cualquier otra cosa, responde con normalidad en español."
)

PROMPT_FECHA = (
    "Eres el agente `fecha`. Saluda brevemente al usuario y comunícale que la "
    "fecha y hora actual es la que se te indica. Sé cálido y conciso. Responde "
    "solo con el mensaje, sin prefijos."
)


def _forzar_utf8() -> None:
    """Fuerza UTF-8 en los flujos estándar (necesario en Windows, ver L-003)."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass


def fecha_hora_real() -> str:
    """La fecha y hora reales, tomadas del reloj del sistema (no del modelo)."""
    ahora = datetime.now()
    dia = DIAS[ahora.weekday()]
    mes = MESES[ahora.month - 1]
    return f"{dia} {ahora.day} de {mes} de {ahora.year}, {ahora:%H:%M:%S}"


def componer_principal(historial: list[tuple[str, str]], mensaje: str) -> str:
    """Prompt de la sesión principal: instrucciones + historial + turno nuevo."""
    lineas = [PROMPT_PRINCIPAL, "", "## Conversación"]
    for quien, texto in historial:
        etiqueta = "Humano" if quien == "humano" else "Asistente"
        lineas.append(f"{etiqueta}: {texto}")
    lineas.append(f"Humano: {mensaje}")
    lineas.append("")
    lineas.append("Responde ahora al último turno del Humano.")
    return "\n".join(lineas)


def invocar_agente_fecha(agente: ClaudeCLIProvider) -> str:
    """Sub-agente 'fecha': recibe la hora real (de código) y la redacta."""
    dato = fecha_hora_real()
    prompt = f"{PROMPT_FECHA}\n\nFecha y hora actual (real): {dato}"
    return agente.send(prompt)


def main() -> int:
    _forzar_utf8()

    principal = ClaudeCLIProvider(model="sonnet", tools=())
    agente_fecha = ClaudeCLIProvider(model="haiku", tools=())
    historial: list[tuple[str, str]] = []

    print(
        "Sesión principal (sonnet) + agente fecha (haiku) · "
        "prueba: 'dame la hora y fecha' · /salir para terminar.\n"
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
            decision = principal.send(componer_principal(historial, mensaje))
            if MARCADOR in decision:
                print("   … la sesión principal decidió delegar en el agente fecha")
                respuesta = invocar_agente_fecha(agente_fecha)
            else:
                respuesta = decision
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
