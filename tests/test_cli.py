"""Tests de T-005: CLI `soda` y el subcomando `init`.

El foco está en el contrato con el usuario, no en la copia: que el destino sea
el correcto, que nunca se pierda memoria sin `--force`, y que los códigos de
salida distingan éxito de fallo.
"""

import pytest

from soda.cli import (
    CREADO,
    SALTADO,
    SOBRESCRITO,
    init_persistence,
    main,
)
from soda.templates import (
    PERSISTENCE_DIRNAME,
    PERSISTENCE_FILENAMES,
    read_persistence_template,
)


def _persistence(raiz):
    return raiz / PERSISTENCE_DIRNAME


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


# --- main: contrato de línea de comandos -----------------------------------


def test_main_init_con_ruta_explicita(tmp_path, capsys):
    codigo = main(["init", str(tmp_path)])

    assert codigo == 0
    assert _persistence(tmp_path).is_dir()
    assert "6 creados" in capsys.readouterr().out


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
