"""Tests de T-012 (paso 2): lectura de la memoria de un proyecto destino.

Todo aquí es Python puro: ningún test invoca un modelo ni necesita cuota.
"""

from pathlib import Path

import pytest

from soda.agents.memory import (
    BAJO_DEMANDA,
    OBLIGATORIOS,
    MemoriaAusenteError,
    extraer_indice,
    leer_memoria,
)
from soda.cli import init_persistence
from soda.templates import PERSISTENCE_DIRNAME, PERSISTENCE_FILENAMES


@pytest.fixture
def proyecto_recien_iniciado(tmp_path) -> Path:
    """Un proyecto destino con la memoria sembrada por `soda init`, sin escribir."""
    init_persistence(tmp_path)
    return tmp_path


def _escribir(project_root: Path, nombre: str, contenido: str) -> None:
    (project_root / PERSISTENCE_DIRNAME / nombre).write_text(contenido, encoding="utf-8")


# --- Reparto de los seis archivos -----------------------------------------


def test_los_dos_repartos_cubren_los_seis_archivos_sin_solaparse():
    assert set(OBLIGATORIOS) | set(BAJO_DEMANDA) == set(PERSISTENCE_FILENAMES)
    assert not set(OBLIGATORIOS) & set(BAJO_DEMANDA)


def test_los_obligatorios_viajan_integros_y_los_demas_solo_con_indice(
    proyecto_recien_iniciado,
):
    memoria = leer_memoria(proyecto_recien_iniciado)

    assert set(memoria.completos) == set(OBLIGATORIOS)
    assert set(memoria.indices) == set(BAJO_DEMANDA)


# --- Extracción del índice ------------------------------------------------


def test_extraer_indice_corta_en_el_siguiente_encabezado():
    contenido = (
        "# Decisions\n\n"
        "## Índice\n\n"
        "| Código | Título |\n"
        "|--------|--------|\n"
        "| D-001 | Nombre del paquete |\n\n"
        "## Detalle de decisiones\n\n"
        "### D-001 — Nombre del paquete\n\n"
        "- **Contexto:** algo largo que no debe viajar.\n"
    )

    indice = extraer_indice(contenido)

    assert indice.startswith("## Índice")
    assert "D-001 | Nombre del paquete" in indice
    assert "Detalle" not in indice
    assert "algo largo" not in indice


def test_extraer_indice_devuelve_vacio_si_el_archivo_no_sigue_la_convencion():
    assert extraer_indice("# Sin índice\n\nTexto suelto.\n") == ""


def test_el_indice_extraido_es_mucho_mas_corto_que_el_archivo(proyecto_recien_iniciado):
    detalle = "\n".join(f"### D-{i:03d} — Algo\n\n- **Contexto:** relleno." for i in range(50))
    _escribir(
        proyecto_recien_iniciado,
        "decisions.md",
        f"# Decisions\n\n## Índice\n\n| D-001 | Uno |\n\n## Detalle\n\n{detalle}\n",
    )

    memoria = leer_memoria(proyecto_recien_iniciado)

    assert len(memoria.indices["decisions.md"]) < len(detalle) / 10


# --- Detección de memoria vacía -------------------------------------------


def test_memoria_recien_sembrada_esta_vacia(proyecto_recien_iniciado):
    assert leer_memoria(proyecto_recien_iniciado).vacia is True


def test_un_solo_obligatorio_escrito_basta_para_que_haya_estado(proyecto_recien_iniciado):
    _escribir(
        proyecto_recien_iniciado, "progress.md", "# Progress\n\n## Estado actual\n\nAlgo.\n"
    )

    assert leer_memoria(proyecto_recien_iniciado).vacia is False


def test_vacia_solo_mira_los_obligatorios(proyecto_recien_iniciado):
    """Escribir un archivo bajo demanda no cambia el veredicto.

    Es deliberado: el protocolo de inicio decide el tipo de sesión mirando
    `progress.md` y `tasks.md`, y una lección apuntada sin ningún avance
    registrado no es una sesión previa de trabajo.
    """
    _escribir(
        proyecto_recien_iniciado, "lessons.md", "# Lessons\n\n## Índice\n\n| L-001 | Algo |\n"
    )

    assert leer_memoria(proyecto_recien_iniciado).vacia is True


def test_los_finales_de_linea_de_windows_no_simulan_estado(proyecto_recien_iniciado):
    for nombre in OBLIGATORIOS:
        ruta = proyecto_recien_iniciado / PERSISTENCE_DIRNAME / nombre
        ruta.write_bytes(ruta.read_text(encoding="utf-8").replace("\n", "\r\n").encode("utf-8"))

    assert leer_memoria(proyecto_recien_iniciado).vacia is True


# --- Anomalías ------------------------------------------------------------


def test_error_si_el_proyecto_no_tiene_carpeta_de_memoria(tmp_path):
    with pytest.raises(MemoriaAusenteError, match=PERSISTENCE_DIRNAME):
        leer_memoria(tmp_path)


def test_un_archivo_ausente_se_reporta_y_no_tumba_la_lectura(proyecto_recien_iniciado):
    (proyecto_recien_iniciado / PERSISTENCE_DIRNAME / "lessons.md").unlink()

    memoria = leer_memoria(proyecto_recien_iniciado)

    assert memoria.faltantes == ("lessons.md",)
    assert "lessons.md" not in memoria.indices


def test_un_obligatorio_ausente_se_trata_como_proyecto_con_estado(proyecto_recien_iniciado):
    (proyecto_recien_iniciado / PERSISTENCE_DIRNAME / "tasks.md").unlink()

    memoria = leer_memoria(proyecto_recien_iniciado)

    assert memoria.faltantes == ("tasks.md",)
    assert memoria.vacia is False


# --- C-001: el harness no lee su propia memoria ---------------------------


def test_no_toca_la_memoria_del_repo_del_harness(proyecto_recien_iniciado):
    memoria = leer_memoria(proyecto_recien_iniciado)

    assert memoria.project_root == proyecto_recien_iniciado
    assert "900_persistence" not in str(memoria.project_root)
