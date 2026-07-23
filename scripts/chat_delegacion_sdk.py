#!/usr/bin/env python3
"""Spike (C-003, no producto): delegación por tool_use ESTRUCTURADO del Agent SDK.

Camino B de D-036 y equivalente estructural de `chat_delegacion.py` (Camino A,
que usaba el marcador frágil `[[LLAMAR:fecha]]`, C-008). Aquí NO hay marcador ni
regex: el protocolo de herramientas lo gestiona el propio SDK. Verifica dos de
los tres puntos críticos de T-020:

  Punto 1 — tool_use estructurado. Se define `fecha` con `@tool`. La sesión
    principal, cuando el humano pide la hora, decide llamarla; el SDK la ejecuta
    y le devuelve el resultado al modelo por su cuenta. El dato factual (la hora
    real) lo pone CÓDIGO Python vía `datetime.now()`, no el modelo, que la
    inventaría. Observamos el `ToolUseBlock` en el stream: eso es el "bucle
    interior" que en el Camino A hacíamos a mano.

  Punto 3 — subagente. Se define un `clocker` con `AgentDefinition`, dueño de la
    herramienta del reloj. La sesión principal le delega la tarea completa. En el
    stream distinguimos QUIÉN hace cada paso con `parent_tool_use_id`: los mensajes
    de un subagente lo traen apuntando al `id` del bloque `Agent`/`Task` que lo
    invocó; los de la sesión principal lo traen en `None`. Así la pantalla muestra
    la invocación del agente y sus pasos internos, que es la mecánica central del
    orquestador (D-035).

Diferencia deliberada con `chat_delegacion.py`: allí Python detectaba el
marcador y ramificaba con un `if`; aquí Python solo define herramientas y agente,
y OBSERVA lo que el SDK orquesta. Decisión de alcance de T-020: cada turno es un
`query()` nuevo (sin persistencia de contexto entre turnos); la persistencia de
sesión viva (ClaudeSDKClient, D-035) se prueba aparte en T-019.

Uso:
    .venv\\Scripts\\python.exe scripts\\chat_delegacion_sdk.py
    (Escribe "dame la hora y fecha" para forzar la delegación. /salir para salir.)
"""

import os
import sys
from datetime import datetime

# Borrar las credenciales de API antes de importar el SDK (L-014, política de
# ClaudeCLIProvider): la suscripción debe ser garantizada, no esperada.
for _variable in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
    os.environ.pop(_variable, None)

import anyio  # noqa: E402
from claude_agent_sdk import (  # noqa: E402
    AgentDefinition,
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
    create_sdk_mcp_server,
    query,
    tool,
)

SALIDAS = {"/salir", "/exit", "/quit"}

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
    "septiembre", "octubre", "noviembre", "diciembre",
]

PROMPT_PRINCIPAL = (
    "Eres la sesión principal de un asistente en español. NO conoces la hora ni "
    "la fecha y NUNCA las inventes. Tienes un subagente al que delegar:\n"
    "- `clocker`: se encarga de averiguar y comunicar la fecha y hora reales.\n\n"
    "Cuando el humano pida la fecha o la hora, delega la tarea COMPLETA en el "
    "subagente `clocker` y transmite su respuesta al usuario. Para cualquier otra "
    "cosa, responde tú directamente sin delegar."
)

PROMPT_CLOCKER = (
    "Eres el agente `clocker`, especialista en tiempo. Para saber la fecha y hora "
    "reales SIEMPRE usas la herramienta `mcp__reloj__fecha` —tú tampoco las "
    "conoces de memoria—. Con ese dato, redacta un saludo breve y cálido en "
    "español que se lo comunique al usuario. Responde solo con el mensaje."
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


def _fecha_hora_real() -> str:
    """La fecha y hora reales, del reloj del sistema (no del modelo)."""
    ahora = datetime.now()
    dia = DIAS[ahora.weekday()]
    mes = MESES[ahora.month - 1]
    return f"{dia} {ahora.day} de {mes} de {ahora.year}, {ahora:%H:%M:%S}"


@tool("fecha", "Devuelve la fecha y hora real actual del sistema.", {})
async def herramienta_fecha(args: dict) -> dict:
    """Herramienta estructurada: el dato factual lo pone Python, no el modelo."""
    dato = _fecha_hora_real()
    print(f"        [tool] Python ejecutó `fecha` → {dato}")
    return {"content": [{"type": "text", "text": dato}]}


def _construir_opciones() -> ClaudeAgentOptions:
    servidor = create_sdk_mcp_server("reloj", tools=[herramienta_fecha])
    return ClaudeAgentOptions(
        model="sonnet",
        system_prompt=PROMPT_PRINCIPAL,
        mcp_servers={"reloj": servidor},
        # `ToolSearch` va permitido porque el CLI puede DIFERIR el esquema de las
        # herramientas MCP: el modelo hace primero un ToolSearch para cargarlo y
        # luego llama a la herramienta. Sin permitirlo, ese primer paso falla.
        # `bypassPermissions` evita el diálogo de permiso por herramienta, que en
        # modo no interactivo cortaría el turno.
        # La herramienta de delegación en subagentes se llama `Task` o `Agent`
        # según el build del CLI; se permiten ambas.
        allowed_tools=["mcp__reloj__fecha", "Task", "Agent", "ToolSearch"],
        permission_mode="bypassPermissions",
        agents={
            "clocker": AgentDefinition(
                description="Averigua y comunica la fecha y hora reales al usuario.",
                prompt=PROMPT_CLOCKER,
                tools=["mcp__reloj__fecha", "ToolSearch"],
                model="haiku",
            )
        },
    )


def _quien(parent_tool_use_id: str | None, agentes: dict[str, str]) -> str:
    """Atribuye un mensaje a su autor.

    Los mensajes de la sesión principal traen `parent_tool_use_id = None`. Los que
    genera un subagente lo traen apuntando al `id` del bloque `Agent`/`Task` que lo
    invocó; ese id lo registramos al ver la delegación. Así distinguimos en pantalla
    quién hace cada paso.
    """
    if parent_tool_use_id and parent_tool_use_id in agentes:
        return f"agente `{agentes[parent_tool_use_id]}`"
    return "SESIÓN PRINCIPAL"


async def _turno(opciones: ClaudeAgentOptions, mensaje: str) -> str:
    """Un turno: envía el mensaje, muestra quién hace cada paso (sesión principal
    vs. subagente) y devuelve el texto final para el usuario."""
    agentes: dict[str, str] = {}  # id del tool_use de delegación -> nombre del agente
    texto_final = ""

    async for msg in query(prompt=mensaje, options=opciones):
        if isinstance(msg, AssistantMessage):
            autor = _quien(msg.parent_tool_use_id, agentes)
            for bloque in msg.content:
                if isinstance(bloque, ToolUseBlock):
                    if bloque.name in ("Task", "Agent"):
                        sub = bloque.input.get("subagent_type", "?")
                        agentes[bloque.id] = sub
                        print(f"\n  ╔═ {autor} ▶ INVOCA al agente `{sub}`")
                    else:
                        print(f"  ║  {autor} ▶ usa la herramienta `{bloque.name}`")
                elif isinstance(bloque, TextBlock) and bloque.text.strip():
                    if msg.parent_tool_use_id:  # texto de un subagente
                        print(f"  ║  {autor} ▶ responde: {bloque.text.strip()}")
                    else:  # texto de la sesión principal: es la respuesta final
                        texto_final = bloque.text
        elif isinstance(msg, UserMessage):
            # Resultado devuelto por una herramienta o por un subagente al padre.
            for bloque in msg.content:
                if isinstance(bloque, ToolResultBlock) and bloque.tool_use_id in agentes:
                    sub = agentes[bloque.tool_use_id]
                    print(f"  ╚═ agente `{sub}` ▶ termina y devuelve el control\n")
        elif isinstance(msg, ResultMessage) and msg.is_error:
            print("  [aviso] el turno terminó con is_error=True")

    return texto_final


async def _correr() -> None:
    opciones = _construir_opciones()
    print(
        "Delegación con Agent SDK (tool_use estructurado) · "
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
            respuesta = await _turno(opciones, mensaje)
        except Exception as exc:  # noqa: BLE001 — spike: queremos ver cualquier fallo
            print(f"\n[error] {type(exc).__name__}: {exc}\n")
            continue

        print(f"\nClaude> {respuesta}\n")

    print("Hasta luego.")


def main() -> int:
    _forzar_utf8()
    anyio.run(_correr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
