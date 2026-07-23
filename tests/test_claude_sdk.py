"""Tests de T-021: `ClaudeSDKProvider` y `SesionClaudeSDK`.

El `ClaudeSDKClient` real nunca se abre aquí; se sustituye por un cliente falso
inyectado en el namespace del módulo (igual que `test_provider.py` sustituye
`subprocess.run`). La verificación contra la suscripción real —los 2-3 turnos que
mantienen contexto— es el script en vivo `scripts/probar_sesion_sdk.py`.

Las corrutinas se ejecutan con `asyncio.run` dentro de tests sync, para no añadir
un plugin async a la suite.
"""

import asyncio

import pytest
from claude_agent_sdk import AssistantMessage, TextBlock

from soda.core.provider import ProviderError
from soda.core.sesion import Sesion
from soda.providers import ClaudeSDKProvider


class ClienteFalso:
    """Doble del `ClaudeSDKClient`: registra su ciclo de vida y los turnos.

    `receive_response` devuelve un `AssistantMessage` real (con un `TextBlock`
    real) para que los `isinstance` del provider se cumplan sin monkeypatch de los
    tipos del SDK. El texto ecoa el prompt y el número de turno, lo que permite
    comprobar que el contexto (la cuenta de turnos) se conserva en el mismo cliente.
    """

    #: Todas las instancias creadas, en orden, para verificar reuso entre turnos.
    instancias: list["ClienteFalso"] = []

    def __init__(self, options):
        self.options = options
        self.conectado = False
        self.prompts: list[str] = []
        ClienteFalso.instancias.append(self)

    async def connect(self, prompt=None):
        self.conectado = True

    async def disconnect(self):
        self.conectado = False

    async def query(self, prompt, session_id="default"):
        self.prompts.append(prompt)

    async def receive_response(self):
        texto = f"turno {len(self.prompts)}: {self.prompts[-1]}"
        yield AssistantMessage(
            content=[TextBlock(text=texto)],
            model="falso",
        )


@pytest.fixture(autouse=True)
def cliente_falso(monkeypatch):
    ClienteFalso.instancias = []
    monkeypatch.setattr(
        "soda.providers.claude_sdk.ClaudeSDKClient",
        ClienteFalso,
    )
    return ClienteFalso


# --- Tipos y contrato ------------------------------------------------------


def test_la_sesion_es_una_sesion():
    assert isinstance(ClaudeSDKProvider().abrir_sesion(), Sesion)


def test_enviar_fuera_de_contexto_falla():
    async def escenario():
        sesion = ClaudeSDKProvider().abrir_sesion()
        with pytest.raises(ProviderError):
            await sesion.enviar("hola")

    asyncio.run(escenario())


# --- Multi-turno: el contexto vive en el mismo cliente ---------------------


def test_mantiene_el_mismo_cliente_entre_turnos(cliente_falso):
    async def escenario():
        async with ClaudeSDKProvider().abrir_sesion() as sesion:
            await sesion.enviar("primero")
            await sesion.enviar("segundo")

    asyncio.run(escenario())

    # Un solo cliente para los dos turnos: eso es la persistencia de contexto.
    assert len(cliente_falso.instancias) == 1
    assert cliente_falso.instancias[0].prompts == ["primero", "segundo"]


def test_conecta_al_entrar_y_desconecta_al_salir(cliente_falso):
    async def escenario():
        async with ClaudeSDKProvider().abrir_sesion():
            assert cliente_falso.instancias[0].conectado is True

    asyncio.run(escenario())
    assert cliente_falso.instancias[0].conectado is False


def test_enviar_devuelve_solo_el_texto(cliente_falso):
    async def escenario():
        async with ClaudeSDKProvider().abrir_sesion() as sesion:
            return await sesion.enviar("hola")

    assert asyncio.run(escenario()) == "turno 1: hola"


# --- Opciones: suscripción y L-016 -----------------------------------------


def _opciones_de(provider) -> object:
    return provider._opciones()


def test_neutraliza_las_credenciales_de_api():
    opciones = _opciones_de(ClaudeSDKProvider())
    assert opciones.env["ANTHROPIC_API_KEY"] == ""
    assert opciones.env["ANTHROPIC_AUTH_TOKEN"] == ""


def test_sin_solo_suscripcion_no_toca_el_entorno():
    opciones = _opciones_de(ClaudeSDKProvider(solo_suscripcion=False))
    assert opciones.env == {}


def test_fija_bypass_permissions_y_toolsearch():
    opciones = _opciones_de(ClaudeSDKProvider())
    assert opciones.permission_mode == "bypassPermissions"
    assert "ToolSearch" in opciones.allowed_tools


def test_el_modelo_y_el_cwd_viajan_en_las_opciones(tmp_path):
    opciones = _opciones_de(ClaudeSDKProvider(model="haiku", cwd=tmp_path))
    assert opciones.model == "haiku"
    assert opciones.cwd == str(tmp_path)
