"""Sesión persistente sobre el Claude Agent SDK (`ClaudeSDKClient`).

Hermano de `claude_cli.py`, pero para el otro contrato: donde `ClaudeCLIProvider`
resuelve `send` de un disparo (`--print`, sin memoria), este módulo resuelve la
`Sesion` multi-turno que necesita el orquestador REPL persistente (D-035). Un
`ClaudeSDKClient` vivo mantiene el contexto entre turnos; abrirlo una vez y
reusarlo es lo que da la persistencia.

Todo el SDK (`ClaudeSDKClient`, `ClaudeAgentOptions`, `AssistantMessage`,
`TextBlock`) queda contenido aquí: cruza la frontera de `soda.core.sesion.Sesion`
convertido en texto, nunca como tipos del SDK. Así el resto del arnés no depende
del backend concreto (D-006/D-008).

Tres decisiones de invocación, heredadas de la política del CLI provider y del
spike de T-020:

- **Suscripción garantizada, no esperada (D-031).** Si el entorno tiene
  `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`, el CLI factura por token — lo que el
  proyecto existe para evitar. El SDK arma el entorno del subproceso como
  `{**os.environ, **options.env}`: no permite borrar una variable heredada, solo
  sobrescribirla. Se sobrescriben ambas a cadena vacía, que el CLI trata como
  ausente y lo devuelve a la autenticación por suscripción.
- **`bypassPermissions` + `ToolSearch` (L-016).** En modo no interactivo, sin fijar
  `permission_mode="bypassPermissions"` el turno se corta en el primer diálogo de
  permiso, y sin `ToolSearch` en `allowed_tools` la carga diferida del esquema de
  herramientas MCP falla. Ambos son obligatorios para que la delegación no muera en
  silencio.
- **Ciclo de vida explícito.** La sesión es un gestor de contexto async: `__aenter__`
  conecta el cliente, `__aexit__` lo desconecta. Reusar el mismo cliente entre turnos
  es justo lo que conserva el contexto.

El modelo es argumento del constructor del provider, no de cada turno: es
configuración de quien arma la flota, no del mensaje.
"""

from collections.abc import Sequence
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
)

from soda.core.provider import ProviderError
from soda.core.sesion import Sesion
from soda.providers.claude_cli import VARIABLES_DE_API

__all__ = ["ClaudeSDKProvider", "SesionClaudeSDK"]

#: `ToolSearch` es obligatorio (L-016); el resto se amplía cuando un caso lo pida.
HERRAMIENTAS_POR_DEFECTO: tuple[str, ...] = ("ToolSearch",)


class SesionClaudeSDK(Sesion):
    """Sesión multi-turno respaldada por un `ClaudeSDKClient` vivo."""

    def __init__(self, options: ClaudeAgentOptions) -> None:
        """
        Args:
            options: Opciones ya armadas por `ClaudeSDKProvider`. La sesión no las
                construye ni las conoce en detalle; solo abre el cliente con ellas.
        """
        self._options = options
        self._client: ClaudeSDKClient | None = None

    async def __aenter__(self) -> "SesionClaudeSDK":
        self._client = ClaudeSDKClient(self._options)
        await self._client.connect()
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self._client is not None:
            await self._client.disconnect()
            self._client = None

    async def enviar(self, prompt: str) -> str:
        if self._client is None:
            raise ProviderError(
                "La sesión no está abierta: use `async with proveedor.abrir_sesion()` "
                "antes de enviar turnos."
            )

        await self._client.query(prompt)

        partes: list[str] = []
        async for msg in self._client.receive_response():
            if isinstance(msg, AssistantMessage):
                for bloque in msg.content:
                    if isinstance(bloque, TextBlock):
                        partes.append(bloque.text)

        return "".join(partes).strip()


class ClaudeSDKProvider:
    """Fábrica de sesiones persistentes sobre el Claude Agent SDK."""

    def __init__(
        self,
        model: str | None = None,
        system_prompt: str | None = None,
        cwd: Path | None = None,
        tools: Sequence[str] = HERRAMIENTAS_POR_DEFECTO,
        solo_suscripcion: bool = True,
    ) -> None:
        """
        Args:
            model: Alias (`haiku`, `sonnet`, `opus`) o nombre completo. `None` deja
                decidir al CLI.
            system_prompt: Prompt de sistema de la sesión. `None` usa el del CLI.
            cwd: Directorio de trabajo del subproceso; normalmente la raíz del
                proyecto destino.
            tools: Herramientas habilitadas. El valor por defecto incluye
                `ToolSearch`, obligatorio (L-016).
            solo_suscripcion: Si es verdadero, neutraliza las credenciales de API en
                el entorno del subproceso para forzar el uso de la suscripción.
        """
        self.model = model
        self.system_prompt = system_prompt
        self.cwd = cwd
        self.tools = tuple(tools)
        self.solo_suscripcion = solo_suscripcion

    def _entorno(self) -> dict[str, str]:
        """Overrides de entorno para el subproceso del SDK.

        El SDK mergea esto sobre `os.environ`; sobrescribir las credenciales de API
        a cadena vacía es la única forma de neutralizarlas sin poder borrarlas.
        """
        if not self.solo_suscripcion:
            return {}
        return {variable: "" for variable in VARIABLES_DE_API}

    def _opciones(self) -> ClaudeAgentOptions:
        return ClaudeAgentOptions(
            model=self.model,
            system_prompt=self.system_prompt,
            cwd=str(self.cwd) if self.cwd is not None else None,
            allowed_tools=list(self.tools),
            permission_mode="bypassPermissions",
            env=self._entorno(),
        )

    def abrir_sesion(self) -> SesionClaudeSDK:
        """Devuelve una sesión sin abrir; ábrela con `async with`."""
        return SesionClaudeSDK(self._opciones())
