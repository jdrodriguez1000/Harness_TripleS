"""Tests de T-005: CLI `soda` y el subcomando `init`.

El foco está en el contrato con el usuario, no en la copia: que el destino sea
el correcto, que nunca se pierda memoria sin `--force`, y que los códigos de
salida distingan éxito de fallo.
"""

import pytest

from soda.cli import (
    CREADO,
    DIFIERE,
    SALTADO,
    SOBRESCRITO,
    init_guideline,
    init_persistence,
    main,
)
from soda.templates import (
    GUIDELINE_DIRNAME,
    GUIDELINE_FILENAMES,
    PERSISTENCE_DIRNAME,
    PERSISTENCE_FILENAMES,
    read_guideline_template,
    read_persistence_template,
)


def _persistence(raiz):
    return raiz / PERSISTENCE_DIRNAME


def _guideline(raiz):
    return raiz / GUIDELINE_DIRNAME


# --- init_persistence: siembra ---------------------------------------------


def test_crea_los_seis_archivos(tmp_path):
    resultados = init_persistence(tmp_path)

    assert [accion for _, accion in resultados] == [CREADO] * 6
    presentes = {p.name for p in _persistence(tmp_path).iterdir()}
    assert presentes == set(PERSISTENCE_FILENAMES)


def test_el_contenido_coincide_con_la_plantilla(tmp_path):
    init_persistence(tmp_path)

    for nombre in PERSISTENCE_FILENAMES:
        escrito = (_persistence(tmp_path) / nombre).read_text(encoding="utf-8")
        assert escrito == read_persistence_template(nombre)


def test_siembra_dentro_de_project_root_y_no_en_el_directorio_actual(tmp_path, monkeypatch):
    """C-002: el destino depende del argumento, nunca del cwd."""
    otro = tmp_path / "cwd"
    otro.mkdir()
    destino = tmp_path / "proyecto"
    destino.mkdir()
    monkeypatch.chdir(otro)

    init_persistence(destino)

    assert _persistence(destino).is_dir()
    assert not _persistence(otro).exists()


def test_conserva_los_acentos_al_escribir(tmp_path):
    init_persistence(tmp_path)
    contenido = (_persistence(tmp_path) / "tasks.md").read_text(encoding="utf-8")

    assert "## Índice" in contenido
    assert "_(vacío)_" in contenido


# --- init_persistence: no destruir -----------------------------------------


def test_no_sobrescribe_lo_que_ya_existe(tmp_path):
    init_persistence(tmp_path)
    memoria = _persistence(tmp_path) / "tasks.md"
    memoria.write_text("# Tasks\n\nT-001 memoria acumulada\n", encoding="utf-8")

    resultados = init_persistence(tmp_path)

    assert dict(resultados)["tasks.md"] == SALTADO
    assert "memoria acumulada" in memoria.read_text(encoding="utf-8")


def test_completa_solo_los_archivos_que_faltan(tmp_path):
    init_persistence(tmp_path)
    (_persistence(tmp_path) / "lessons.md").unlink()

    resultados = dict(init_persistence(tmp_path))

    assert resultados["lessons.md"] == CREADO
    assert resultados["tasks.md"] == SALTADO


def test_es_idempotente(tmp_path):
    init_persistence(tmp_path)
    resultados = init_persistence(tmp_path)

    assert [accion for _, accion in resultados] == [SALTADO] * 6


def test_force_sobrescribe(tmp_path):
    init_persistence(tmp_path)
    memoria = _persistence(tmp_path) / "tasks.md"
    memoria.write_text("contenido viejo", encoding="utf-8")

    resultados = init_persistence(tmp_path, force=True)

    assert [accion for _, accion in resultados] == [SOBRESCRITO] * 6
    assert memoria.read_text(encoding="utf-8") == read_persistence_template("tasks.md")


# --- init_persistence: errores ---------------------------------------------


def test_falla_si_project_root_no_existe(tmp_path):
    with pytest.raises(NotADirectoryError, match="no crea el proyecto"):
        init_persistence(tmp_path / "no-existe")


def test_falla_si_project_root_es_un_archivo(tmp_path):
    archivo = tmp_path / "archivo.txt"
    archivo.write_text("x", encoding="utf-8")

    with pytest.raises(NotADirectoryError):
        init_persistence(archivo)


def test_no_deja_rastro_si_project_root_no_existe(tmp_path):
    inexistente = tmp_path / "no-existe"

    with pytest.raises(NotADirectoryError):
        init_persistence(inexistente)

    assert not inexistente.exists()


# --- init_guideline: siembra (T-009) ---------------------------------------


def test_guideline_crea_los_tres_documentos(tmp_path):
    resultados = init_guideline(tmp_path)

    assert [accion for _, accion in resultados] == [CREADO] * 3
    presentes = {p.name for p in _guideline(tmp_path).iterdir()}
    assert presentes == set(GUIDELINE_FILENAMES)


def test_guideline_el_contenido_coincide_con_el_del_paquete(tmp_path):
    init_guideline(tmp_path)

    for nombre in GUIDELINE_FILENAMES:
        escrito = (_guideline(tmp_path) / nombre).read_text(encoding="utf-8")
        assert escrito == read_guideline_template(nombre)


def test_guideline_siembra_dentro_de_project_root(tmp_path, monkeypatch):
    """C-002: el destino depende del argumento, nunca del cwd."""
    otro = tmp_path / "cwd"
    otro.mkdir()
    destino = tmp_path / "proyecto"
    destino.mkdir()
    monkeypatch.chdir(otro)

    init_guideline(destino)

    assert _guideline(destino).is_dir()
    assert not _guideline(otro).exists()


def test_guideline_es_idempotente_y_no_marca_diferencias(tmp_path):
    """Sembrar dos veces deja copias idénticas: saltado, no DIFIERE."""
    init_guideline(tmp_path)
    resultados = init_guideline(tmp_path)

    assert [accion for _, accion in resultados] == [SALTADO] * 3


def test_guideline_completa_solo_los_documentos_que_faltan(tmp_path):
    init_guideline(tmp_path)
    (_guideline(tmp_path) / "methodology.md").unlink()

    resultados = dict(init_guideline(tmp_path))

    assert resultados["methodology.md"] == CREADO
    assert resultados["principles.md"] == SALTADO


def test_guideline_marca_como_difiere_una_copia_desactualizada(tmp_path):
    """El caso real: soda se actualizó y el destino quedó con la guía vieja."""
    init_guideline(tmp_path)
    vieja = _guideline(tmp_path) / "methodology.md"
    vieja.write_text("# Metodología de Construcción\n\nversión anterior\n", encoding="utf-8")

    resultados = dict(init_guideline(tmp_path))

    assert resultados["methodology.md"] == DIFIERE
    assert resultados["principles.md"] == SALTADO


def test_guideline_no_toca_la_copia_que_difiere_sin_force(tmp_path):
    init_guideline(tmp_path)
    vieja = _guideline(tmp_path) / "principles.md"
    vieja.write_text("editado a mano", encoding="utf-8")

    init_guideline(tmp_path)

    assert vieja.read_text(encoding="utf-8") == "editado a mano"


def test_guideline_force_sobrescribe(tmp_path):
    init_guideline(tmp_path)
    doc = _guideline(tmp_path) / "principles.md"
    doc.write_text("contenido viejo", encoding="utf-8")

    resultados = init_guideline(tmp_path, force=True)

    assert [accion for _, accion in resultados] == [SOBRESCRITO] * 3
    assert doc.read_text(encoding="utf-8") == read_guideline_template("principles.md")


def test_guideline_falla_si_project_root_no_existe(tmp_path):
    with pytest.raises(NotADirectoryError, match="no crea el proyecto"):
        init_guideline(tmp_path / "no-existe")


def test_la_memoria_nunca_se_marca_como_difiere(tmp_path):
    """Que la memoria diverja de la plantilla es lo esperado, no una anomalía."""
    init_persistence(tmp_path)
    (_persistence(tmp_path) / "tasks.md").write_text("otra cosa", encoding="utf-8")

    resultados = dict(init_persistence(tmp_path))

    assert resultados["tasks.md"] == SALTADO


# --- main: contrato de línea de comandos -----------------------------------


def test_main_init_con_ruta_explicita(tmp_path, capsys):
    codigo = main(["init", str(tmp_path)])
    salida = capsys.readouterr().out

    assert codigo == 0
    assert _persistence(tmp_path).is_dir()
    assert "6 creados" in salida


def test_main_init_siembra_memoria_y_guia_en_la_misma_pasada(tmp_path, capsys):
    codigo = main(["init", str(tmp_path)])
    salida = capsys.readouterr().out

    assert codigo == 0
    assert _persistence(tmp_path).is_dir()
    assert _guideline(tmp_path).is_dir()
    assert "6 creados" in salida
    assert "3 creados" in salida
    assert str(tmp_path.resolve() / GUIDELINE_DIRNAME) in salida


def test_main_avisa_cuando_la_guia_del_destino_esta_desfasada(tmp_path, capsys):
    main(["init", str(tmp_path)])
    capsys.readouterr()
    (_guideline(tmp_path) / "methodology.md").write_text("vieja", encoding="utf-8")

    codigo = main(["init", str(tmp_path)])
    salida = capsys.readouterr().out

    assert codigo == 0
    assert "difiere" in salida
    assert "versión anterior" in salida
    assert "--force" in salida


def test_main_no_avisa_de_desfase_si_la_guia_esta_al_dia(tmp_path, capsys):
    main(["init", str(tmp_path)])
    capsys.readouterr()

    main(["init", str(tmp_path)])
    salida = capsys.readouterr().out

    assert "difiere" not in salida


def test_main_init_sin_argumento_usa_el_directorio_actual(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    codigo = main(["init"])
    capsys.readouterr()

    assert codigo == 0
    assert _persistence(tmp_path).is_dir()


def test_main_muestra_la_ruta_absoluta_resuelta(tmp_path, monkeypatch, capsys):
    """El usuario escribe `.`; la salida debe decirle dónde cayó de verdad."""
    monkeypatch.chdir(tmp_path)
    main(["init", "."])

    salida = capsys.readouterr().out
    assert str(tmp_path.resolve() / PERSISTENCE_DIRNAME) in salida


def test_main_avisa_como_sobrescribir_si_salto_archivos(tmp_path, capsys):
    main(["init", str(tmp_path)])
    capsys.readouterr()

    main(["init", str(tmp_path)])
    salida = capsys.readouterr().out

    assert "6 sin tocar" in salida
    assert "--force" in salida


def test_main_concuerda_el_numero_en_el_resumen(tmp_path, capsys):
    main(["init", str(tmp_path)])
    capsys.readouterr()
    (_persistence(tmp_path) / "lessons.md").unlink()

    main(["init", str(tmp_path)])
    salida = capsys.readouterr().out

    assert "1 creado," in salida
    assert "1 creados" not in salida


def test_main_con_force(tmp_path, capsys):
    main(["init", str(tmp_path)])
    capsys.readouterr()

    codigo = main(["init", str(tmp_path), "--force"])

    assert codigo == 0
    assert "6 sobrescritos" in capsys.readouterr().out


def test_main_falla_con_codigo_1_si_el_destino_no_existe(tmp_path, capsys):
    codigo = main(["init", str(tmp_path / "no-existe")])

    assert codigo == 1
    assert "Error:" in capsys.readouterr().err


def test_main_sin_subcomando_muestra_ayuda_y_falla(capsys):
    codigo = main([])

    assert codigo == 1
    assert "init" in capsys.readouterr().out
