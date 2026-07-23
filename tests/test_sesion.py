"""Tests del contrato abstracto `Sesion` (T-021).

Solo el contrato: que la ABC no se instancie, que una subclase incompleta
tampoco, y que una subclase completa (eco) funcione y mantenga contexto simulado
entre turnos. La sesión real sobre el SDK se prueba en `test_claude_sdk.py`.
"""

import asyncio

import pytest

from soda.core.sesion import Sesion


def test_sesion_no_es_instanciable():
    with pytest.raises(TypeError):
        Sesion()


def test_subclase_sin_enviar_no_es_instanciable():
    class SesionIncompleta(Sesion):
        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return None

    with pytest.raises(TypeError):
        SesionIncompleta()


def test_subclase_completa_funciona_como_context_manager_async():
    class SesionEco(Sesion):
        def __init__(self):
            self.turnos = []

        async def enviar(self, prompt: str) -> str:
            self.turnos.append(prompt)
            # "Recuerda" el contexto: eco con la cuenta de turnos vistos.
            return f"eco {len(self.turnos)}: {prompt}"

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return None

    async def escenario():
        async with SesionEco() as sesion:
            assert isinstance(sesion, Sesion)
            assert await sesion.enviar("hola") == "eco 1: hola"
            assert await sesion.enviar("otra vez") == "eco 2: otra vez"

    asyncio.run(escenario())
