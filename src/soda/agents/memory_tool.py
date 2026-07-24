"""La lectura de `_persistence/` expuesta como herramienta del Agent SDK.

La mitad Python de la lectura de memoria ya existe (`soda.agents.memory`,
T-012). Este módulo la envuelve como una **herramienta in-process** del Claude
Agent SDK: una función registrada que el orquestador REPL puede invocar durante
la sesión para consultar la memoria del proyecto de forma estructurada, en vez
de rastrear el disco por su cuenta con herramientas genéricas de archivos —el
comportamiento que el spike de T-022 dejó a la vista.

Dos decisiones deliberadas:

- **La raíz del proyecto no la elige el modelo (C-002).** El `project_root` se
  captura en el cierre al construir la herramienta, no viaja como argumento que
  el modelo pudiera inventar. Por eso el esquema de entrada es vacío: la
  herramienta no recibe nada del modelo, solo devuelve la memoria del proyecto
  con el que se armó la sesión.
- **Read-only.** La herramienta lee y formatea; nunca escribe. La escritura de
  memoria (y el commit/push de Git, NC-007) es trabajo de T-024, no de aquí.

El nombre completo que ve el modelo lo fija el SDK a partir del servidor y la
herramienta: `mcp__<servidor>__<herramienta>`. Se expone como `ALLOWED_TOOL`
para que quien arme la flota lo añada a `allowed_tools` sin volver a componerlo a
mano y arriesgarse a un desajuste silencioso.
"""

from pathlib import Path
from typing import Any

from claude_agent_sdk import McpSdkServerConfig, SdkMcpTool, create_sdk_mcp_server, tool

from soda.agents.memory import MemoriaAusenteError, MemoriaProyecto, leer_memoria

__all__ = [
    "ALLOWED_TOOL",
    "SERVER_NAME",
    "TOOL_NAME",
    "create_memory_server",
    "format_memory",
    "make_memory_tool",
]

#: Identificador del servidor MCP in-process en el dict `mcp_servers`.
SERVER_NAME = "memory"

#: Identificador de la herramienta de lectura dentro del servidor.
TOOL_NAME = "read"

#: Nombre completo que el modelo invoca y que va en `allowed_tools`. El SDK lo
#: compone como `mcp__<servidor>__<herramienta>`; se deja escrito aquí una sola
#: vez para que nadie lo teclee mal en dos sitios.
ALLOWED_TOOL = f"mcp__{SERVER_NAME}__{TOOL_NAME}"

_DESCRIPTION = (
    "Lee la memoria del proyecto en `_persistence/` y la devuelve: los archivos "
    "de lectura obligatoria (`progress.md`, `tasks.md`) íntegros y el resto solo "
    "con su índice. No recibe parámetros: siempre lee el proyecto de esta sesión."
)


def format_memory(memory: MemoriaProyecto) -> str:
    """Convierte lo que leyó `leer_memoria` en el texto que recibe el modelo.

    Los obligatorios viajan íntegros y los demás solo con su índice, respetando
    la misma economía de contexto que el prompt del `sesion-starter`. Los
    archivos ausentes se listan al final como aviso, no como error.

    Args:
        memory: Lo que `leer_memoria` encontró en el proyecto destino.

    Returns:
        El texto de la memoria, listo para devolver como contenido de la tool.
    """
    parts: list[str] = []

    for name, content in memory.completos.items():
        parts.append(f"## {name} (íntegro)\n\n{content.strip()}")

    for name, index in memory.indices.items():
        body = index or "_(este archivo no tiene sección de índice)_"
        parts.append(f"## {name} (solo índice)\n\n{body}")

    if memory.faltantes:
        ausentes = "\n".join(f"- `{name}`" for name in memory.faltantes)
        parts.append(f"## Archivos ausentes\n\n{ausentes}")

    return "\n\n".join(parts)


def make_memory_tool(project_root: Path) -> SdkMcpTool[Any]:
    """Construye la herramienta de lectura atada a un proyecto concreto.

    El `project_root` queda capturado en el cierre (C-002): la herramienta no lo
    recibe del modelo, así que este no puede apuntarla a otro proyecto.

    Args:
        project_root: Raíz del proyecto destino cuya memoria leerá la tool.

    Returns:
        La `SdkMcpTool` lista para pasar a `create_sdk_mcp_server`.
    """

    @tool(TOOL_NAME, _DESCRIPTION, {})
    async def read(args: dict[str, Any]) -> dict[str, Any]:
        try:
            memory = leer_memoria(project_root)
        except MemoriaAusenteError as exc:
            return {"content": [{"type": "text", "text": str(exc)}], "is_error": True}
        return {"content": [{"type": "text", "text": format_memory(memory)}]}

    return read


def create_memory_server(project_root: Path) -> McpSdkServerConfig:
    """Crea el servidor MCP in-process con la única herramienta de lectura.

    Args:
        project_root: Raíz del proyecto destino cuya memoria leerá la tool.

    Returns:
        La configuración del servidor para `ClaudeAgentOptions.mcp_servers`.
    """
    return create_sdk_mcp_server(SERVER_NAME, tools=[make_memory_tool(project_root)])
