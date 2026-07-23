"""Smoke test de T-001: el paquete se instala y se importa correctamente."""

import soda


def test_paquete_importable():
    assert soda.__name__ == "soda"


def test_version_expuesta():
    assert soda.__version__ == "0.1.0"


def test_subpaquete_core_importable():
    import soda.core  # noqa: F401
