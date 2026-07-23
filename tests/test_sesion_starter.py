"""Tests de T-012 (paso 4): el agente `sesion-starter`.

Ningún test invoca un modelo: el agente recibe un `Provider` falso que guarda el
prompt y devuelve un informe fijo. Esa es justamente la ventaja de que el agente
no lea el disco ni elija su proveedor — se puede probar entero sin gastar cuota.
La verificación contra el CLI real es el paso 5 (`scripts/probar_sesion_starter.py`).
"""

from pathlib import Path

import pytest

from soda.agents.memoria import leer_memoria
from soda.agents.prompts import PROMPT_FILENAMES, read_prompt
from soda.agents.sesion_starter import (
    MemoriaVaciaError,
    SesionStarter,
    componer_prompt,
)
from soda.cli import init_persistence
from soda.core.provider import Provider
from soda.templates import PERSISTENCE_DIRNAME


class ProviderEspia(Provider):
    """Guarda el prompt recibido y devuelve una respuesta fija."""

    def __init__(self, respuesta: str = "informe de prueba") -> None:
        self.respuesta = respuesta
        self.prompts: list[str] = []

    def send(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.respuesta


@pytest.fixture
def proyecto_con_estado(tmp_path) -> Path:
    """Proyecto destino con memoria escrita: dos tareas y un hito."""
    init_persistence(tmp_path)
    raiz = tmp_path / PERSISTENCE_DIRNAME

    (raiz / "progress.md").write_text(
        "# Progress\n\n## Estado actual\n\nSe implementó el lector de memoria.\n",
        encoding="utf-8",
    )
    (raiz / "tasks.md").write_text(
        "# Tasks\n\n## Índice\n\n"
        "| Código | Título | Estado |\n|---|---|---|\n"
        "| T-001 | Lector de memoria | Implementada |\n"
        "| T-002 | Agente starter | No implementada |\n\n"
        "## Detalle de tareas\n\n### T-001 — Lector de memoria\n\n- **Estado:** Implementada\n",
        encoding="utf-8",
    )
    (raiz / "decisions.md").write_text(
        "# Decisions\n\n## Índice\n\n| D-001 | Cero herramientas |\n\n"
        "## Detalle de decisiones\n\n### D-001 — Cero herramientas\n\n"
        "- **Contexto:** RELLENO QUE NO DEBE VIAJAR EN EL PROMPT.\n",
        encoding="utf-8",
    )
    return tmp_path


# --- Composición del prompt -----------------------------------------------


def test_el_prompt_lleva_las_instrucciones_del_paquete(proyecto_con_estado):
    prompt = componer_prompt(leer_memoria(proyecto_con_estado))

    assert read_prompt("sesion_starter.md").strip() in prompt


def test_el_prompt_lleva_los_obligatorios_integros(proyecto_con_estado):
    prompt = componer_prompt(leer_memoria(proyecto_con_estado))

    assert "Se implementó el lector de memoria." in prompt
    assert "T-002 | Agente starter | No implementada" in prompt


def test_el_prompt_lleva_solo_el_indice_de_los_de_bajo_demanda(proyecto_con_estado):
    prompt = componer_prompt(leer_memoria(proyecto_con_estado))

    assert "D-001 | Cero herramientas" in prompt
    assert "RELLENO QUE NO DEBE VIAJAR" not in prompt


def test_cada_archivo_va_delimitado_para_no_confundirse_con_instrucciones(
    proyecto_con_estado,
):
    prompt = componer_prompt(leer_memoria(proyecto_con_estado))

    assert "## progress.md (íntegro)" in prompt
    assert "## decisions.md (solo índice)" in prompt
    assert prompt.count("````markdown") == prompt.count("````") / 2


def test_los_archivos_ausentes_se_declaran_en_el_prompt(proyecto_con_estado):
    (proyecto_con_estado / PERSISTENCE_DIRNAME / "lessons.md").unlink()

    prompt = componer_prompt(leer_memoria(proyecto_con_estado))

    assert "Archivos ausentes" in prompt
    assert "`lessons.md`" in prompt


def test_sin_ausentes_no_aparece_esa_seccion(proyecto_con_estado):
    assert "Archivos ausentes" not in componer_prompt(leer_memoria(proyecto_con_estado))


# --- El agente ------------------------------------------------------------


def test_devuelve_lo_que_responde_el_provider(proyecto_con_estado):
    provider = ProviderEspia(respuesta="## Estado actual\n\nTodo en orden.")

    assert SesionStarter(provider).informe(proyecto_con_estado) == (
        "## Estado actual\n\nTodo en orden."
    )


def test_invoca_al_provider_una_sola_vez(proyecto_con_estado):
    provider = ProviderEspia()
    SesionStarter(provider).informe(proyecto_con_estado)

    assert len(provider.prompts) == 1


def test_no_invoca_al_modelo_si_la_memoria_esta_vacia(tmp_path):
    init_persistence(tmp_path)
    provider = ProviderEspia()

    with pytest.raises(MemoriaVaciaError, match="soda start"):
        SesionStarter(provider).informe(tmp_path)

    assert provider.prompts == []


# --- Contrato con el paquete ----------------------------------------------


def test_el_prompt_viaja_en_el_paquete():
    assert "sesion_starter.md" in PROMPT_FILENAMES
    assert read_prompt("sesion_starter.md").startswith("Eres `sesion-starter`")


def test_un_prompt_desconocido_falla_claro():
    with pytest.raises(KeyError, match="no es un prompt"):
        read_prompt("inventado.md")
