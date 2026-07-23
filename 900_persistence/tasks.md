# Tasks

## Índice

| Código | Título | Estado |
|--------|--------|--------|
| [T-001](#t-001--estructura-base-del-proyecto-python) | Estructura base del proyecto Python | Implementada |
| [T-002](#t-002--provider-abstracto--claudecliprovider) | `Provider` abstracto + `ClaudeCLIProvider` | No implementada |
| [T-003](#t-003--script-de-prueba-manual-end-to-end-del-provider) | Script de prueba manual end-to-end del provider | No implementada |

> Estados posibles: `Implementada` / `No implementada` / `Cancelada-Suspendida`

## Detalle de tareas

### T-001 — Estructura base del proyecto Python

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Crear el esqueleto instalable del paquete `soda` con layout `src/`, entorno virtual y verificación básica de empaquetado.
- **Resultado:** Creados `pyproject.toml`, `src/soda/__init__.py` (`__version__ = "0.1.0"`), `src/soda/core/__init__.py`, `src/soda/templates/_persistence/.gitkeep`, `tests/test_smoke.py` (3 tests). `.venv/` con Python 3.12.10. `[project.scripts]` queda comentado a propósito hasta que exista `soda.cli`. Verificado: `pip install -e ".[dev]"` OK, `pytest` 3 passed, `import soda` imprime `0.1.0`, `ruff check .` sin hallazgos.

### T-002 — `Provider` abstracto + `ClaudeCLIProvider`

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Definir una clase base `Provider` abstracta y una implementación `ClaudeCLIProvider` que invoque el CLI `claude` como subproceso y devuelva el texto de respuesta.
- **Pendiente:** Todo el diseño e implementación. Es el siguiente paso acordado para la próxima sesión.

### T-003 — Script de prueba manual end-to-end del provider

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Script manual que envíe un prompt a través del provider (T-002) y muestre la respuesta, para validar la integración con el CLI `claude` fuera de los tests automatizados.
- **Pendiente:** Depende de T-002. No iniciado.
