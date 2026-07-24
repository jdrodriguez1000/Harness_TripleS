"""Tests de T-023 (paso 2): la lectura de memoria expuesta como tool del SDK.

Todo aquí es Python puro: se invoca el `handler` de la herramienta a mano con
`asyncio.run`, igual que el resto de tests async del proyecto. Ningún test abre
una sesión real ni gasta cuota.
"""

import asyncio
from pathlib import Path

import pytest

from soda.agents.memory import leer_memoria
from soda.agents.memory_tool import (
    ALLOWED_TOOL,
    SERVER_NAME,
    TOOL_NAME,
    create_memory_server,
    format_memory,
    make_memory_tool,
)
from soda.cli import init_persistence
from soda.templates import PERSISTENCE_DIRNAME


@pytest.fixture
def proyecto_con_estado(tmp_path) -> Path:
    """Proyecto destino con memoria escrita: obligatorios e índice en un archivo."""
    init_persistence(tmp_path)
    raiz = tmp_path / PERSISTENCE_DIRNAME
    (raiz / "progress.md").write_text(
        "# Progress\n\n## Estado actual\n\nHito reciente: T-023.\n", encoding="utf-8"
    )
    (raiz / "tasks.md").write_text(
        "# Tasks\n\n## Índice\n\n| T-023 | La tool | En curso |\n", encoding="utf-8"
    )
    (raiz / "decisions.md").write_text(
        "# Decisions\n\n## Índice\n\n| D-036 | Agent SDK |\n\n## Detalle\n\ntexto\n",
        encoding="utf-8",
    )
    return tmp_path


def _invocar(tool, args=None):
    return asyncio.run(tool.handler(args or {}))


# --- Nombres y registro ----------------------------------------------------


def test_allowed_tool_se_compone_del_servidor_y_la_herramienta():
    assert ALLOWED_TOOL == f"mcp__{SERVER_NAME}__{TOOL_NAME}"


def test_make_memory_tool_devuelve_la_herramienta_con_su_nombre(tmp_path):
    tool = make_memory_tool(tmp_path)
    assert tool.name == TOOL_NAME
    assert tool.description.strip()
    assert tool.input_schema == {}


def test_create_memory_server_es_un_servidor_sdk_con_ese_nombre(tmp_path):
    server = create_memory_server(tmp_path)
    assert server["type"] == "sdk"
    assert server["name"] == SERVER_NAME


# --- Lectura ---------------------------------------------------------------


def test_la_tool_devuelve_los_obligatorios_integros_y_los_indices(proyecto_con_estado):
    resultado = _invocar(make_memory_tool(proyecto_con_estado))

    assert "is_error" not in resultado
    texto = resultado["content"][0]["text"]
    assert "Hito reciente: T-023." in texto  # progress.md íntegro
    assert "| T-023 | La tool | En curso |" in texto  # índice de tasks.md
    assert "D-036 | Agent SDK" in texto  # solo el índice de decisions.md
    assert "texto" not in texto  # el detalle de decisions.md no viaja


def test_la_tool_ignora_los_argumentos_del_modelo(proyecto_con_estado):
    """C-002: el project_root está en el cierre; el modelo no puede reapuntarla."""
    con_ruido = _invocar(
        make_memory_tool(proyecto_con_estado), {"project_root": "/otro/sitio"}
    )
    sin_ruido = _invocar(make_memory_tool(proyecto_con_estado))
    assert con_ruido == sin_ruido


def test_la_tool_reporta_error_si_no_hay_carpeta_de_memoria(tmp_path):
    resultado = _invocar(make_memory_tool(tmp_path))
    assert resultado["is_error"] is True
    assert PERSISTENCE_DIRNAME in resultado["content"][0]["text"]


# --- Formato ---------------------------------------------------------------


def test_format_memory_lista_los_archivos_ausentes_como_aviso(proyecto_con_estado):
    raiz = proyecto_con_estado / PERSISTENCE_DIRNAME
    (raiz / "lessons.md").unlink()

    texto = format_memory(leer_memoria(proyecto_con_estado))

    assert "Archivos ausentes" in texto
    assert "`lessons.md`" in texto
