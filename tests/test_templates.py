"""Tests de T-004: plantilla de `_persistence` y su accesor.

El riesgo real no es que los archivos existan en el árbol de fuentes, sino que
no viajen en el paquete instalado. Por eso todo se accede vía el paquete
(`importlib.resources`), nunca por ruta relativa al repo.
"""

import pytest

from soda.templates import (
    PERSISTENCE_FILENAMES,
    persistence_root,
    read_persistence_template,
)

# Encabezado y sección de detalle que debe traer cada plantilla.
ESTRUCTURA_ESPERADA = {
    "progress.md": ("# Progress", "## Historial de hitos"),
    "tasks.md": ("# Tasks", "## Detalle de tareas"),
    "lessons.md": ("# Lessons", "## Detalle de lecciones"),
    "decisions.md": ("# Decisions", "## Detalle de decisiones"),
    "constraints.md": ("# Constraints", "## Detalle de restricciones"),
    "assumptions.md": ("# Assumptions", "## Detalle de supuestos"),
}


def test_son_exactamente_los_seis_archivos_de_memoria():
    assert set(PERSISTENCE_FILENAMES) == set(ESTRUCTURA_ESPERADA)
    assert len(PERSISTENCE_FILENAMES) == 6


def test_la_raiz_de_la_plantilla_existe_en_el_paquete():
    assert persistence_root().is_dir()


def test_la_plantilla_no_trae_archivos_de_mas():
    presentes = {hijo.name for hijo in persistence_root().iterdir()}
    assert presentes == set(PERSISTENCE_FILENAMES)


@pytest.mark.parametrize("nombre", PERSISTENCE_FILENAMES)
def test_cada_plantilla_es_legible_desde_el_paquete(nombre):
    assert read_persistence_template(nombre).strip()


@pytest.mark.parametrize("nombre", PERSISTENCE_FILENAMES)
def test_cada_plantilla_tiene_la_estructura_esperada(nombre):
    contenido = read_persistence_template(nombre)
    encabezado, seccion_detalle = ESTRUCTURA_ESPERADA[nombre]

    assert contenido.startswith(encabezado)
    assert "## Índice" in contenido
    assert seccion_detalle in contenido


@pytest.mark.parametrize("nombre", PERSISTENCE_FILENAMES)
def test_cada_plantilla_llega_vacia_de_contenido(nombre):
    """Sin entradas sembradas: `init` no debe inventar memoria en el proyecto."""
    contenido = read_persistence_template(nombre)

    assert "_(vacío)_" in contenido
    for prefijo in ("T-0", "L-0", "D-0", "C-0", "A-0"):
        assert prefijo not in contenido


def test_las_tablas_de_indice_no_traen_filas():
    """Cada índice queda con encabezado y separador, sin filas de datos."""
    for nombre in PERSISTENCE_FILENAMES:
        if nombre == "progress.md":  # su índice es de viñetas, no una tabla
            continue
        filas = [
            linea
            for linea in read_persistence_template(nombre).splitlines()
            if linea.startswith("|")
        ]
        assert len(filas) == 2, f"{nombre} debería tener solo encabezado y separador"


def test_las_plantillas_conservan_los_acentos():
    """UTF-8 sobrevive al empaquetado (ver L-003)."""
    assert "## Índice" in read_persistence_template("tasks.md")
    assert "_(vacío)_" in read_persistence_template("tasks.md")


def test_nombre_desconocido_falla_con_mensaje_util():
    with pytest.raises(KeyError, match="no es una plantilla"):
        read_persistence_template("inventado.md")
