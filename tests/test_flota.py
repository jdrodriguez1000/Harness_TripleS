"""Tests de la flota: qué proveedor y qué modelo recibe cada agente.

`proveedor_para` (un disparo) y `proveedor_de_sesion_para` (sesión persistente,
T-022) construyen el backend sin abrirlo: aquí solo se comprueba la elección de
modelo, proveedor y opciones, no ninguna llamada real.
"""

import pytest

from soda.agents.memory_tool import ALLOWED_TOOL, SERVER_NAME
from soda.core.flota import (
    MODELOS,
    ORQUESTADOR,
    PROMPT_ORQUESTADOR,
    proveedor_de_sesion_para,
    proveedor_para,
)
from soda.providers import ClaudeCLIProvider, ClaudeSDKProvider


def test_el_orquestador_usa_opus():
    assert MODELOS[ORQUESTADOR] == "opus"


def test_sesion_starter_sigue_en_haiku():
    assert MODELOS["sesion-starter"] == "haiku"


# --- proveedor_para: un disparo (contrato existente) ------------------------


def test_proveedor_para_devuelve_un_cli_provider(tmp_path):
    proveedor = proveedor_para("sesion-starter", tmp_path)
    assert isinstance(proveedor, ClaudeCLIProvider)


def test_proveedor_para_falla_con_agente_desconocido(tmp_path):
    with pytest.raises(KeyError):
        proveedor_para("no-existe", tmp_path)


# --- proveedor_de_sesion_para: sesión persistente (T-022) -------------------


def test_devuelve_un_proveedor_de_sesion(tmp_path):
    proveedor = proveedor_de_sesion_para(ORQUESTADOR, tmp_path)
    assert isinstance(proveedor, ClaudeSDKProvider)


def test_el_orquestador_lleva_su_modelo_cwd_y_system_prompt(tmp_path):
    proveedor = proveedor_de_sesion_para(ORQUESTADOR, tmp_path)
    assert proveedor.model == "opus"
    assert proveedor.cwd == tmp_path
    assert proveedor.system_prompt == PROMPT_ORQUESTADOR


def test_un_agente_no_orquestador_no_recibe_system_prompt(tmp_path):
    proveedor = proveedor_de_sesion_para("sesion-starter", tmp_path)
    assert proveedor.system_prompt is None


def test_proveedor_de_sesion_falla_con_agente_desconocido(tmp_path):
    with pytest.raises(KeyError):
        proveedor_de_sesion_para("no-existe", tmp_path)


# --- Memoria como herramienta del orquestador (T-023) ----------------------


def test_el_orquestador_recibe_la_memoria_como_servidor_y_herramienta(tmp_path):
    proveedor = proveedor_de_sesion_para(ORQUESTADOR, tmp_path)
    assert SERVER_NAME in proveedor.mcp_servers
    assert ALLOWED_TOOL in proveedor.tools
    assert "ToolSearch" in proveedor.tools  # L-016 sigue en pie


def test_el_prompt_del_orquestador_nombra_la_herramienta_de_memoria():
    assert ALLOWED_TOOL in PROMPT_ORQUESTADOR


def test_un_agente_no_orquestador_no_recibe_servidores_mcp(tmp_path):
    proveedor = proveedor_de_sesion_para("sesion-starter", tmp_path)
    assert proveedor.mcp_servers == {}
    assert ALLOWED_TOOL not in proveedor.tools
