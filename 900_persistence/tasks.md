# Tasks

## Índice

| Código | Título | Estado |
|--------|--------|--------|
| [T-001](#t-001--estructura-base-del-proyecto-python) | Estructura base del proyecto Python | Implementada |
| [T-002](#t-002--provider-abstracto--claudecliprovider) | `Provider` abstracto + `ClaudeCLIProvider` | Implementada |
| [T-003](#t-003--script-de-prueba-manual-end-to-end-del-provider) | Script de prueba manual end-to-end del provider | Implementada |
| [T-004](#t-004--plantilla-de-contenido-de-_persistence) | Definir el contenido de la plantilla `_persistence` | No implementada |
| [T-005](#t-005--srcsodaclipy-con-el-subcomando-init) | Escribir `src/soda/cli.py` con el subcomando `init` | No implementada |
| [T-006](#t-006--habilitar-entry-point-e-instalar-con-pipx) | Habilitar el entry point e instalar con pipx | No implementada |

> Estados posibles: `Implementada` / `No implementada` / `Cancelada-Suspendida`

## Detalle de tareas

### T-001 — Estructura base del proyecto Python

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Crear el esqueleto instalable del paquete `soda` con layout `src/`, entorno virtual y verificación básica de empaquetado.
- **Resultado:** Creados `pyproject.toml`, `src/soda/__init__.py` (`__version__ = "0.1.0"`), `src/soda/core/__init__.py`, `src/soda/templates/_persistence/.gitkeep`, `tests/test_smoke.py` (3 tests). `.venv/` con Python 3.12.10. `[project.scripts]` queda comentado a propósito hasta que exista `soda.cli`. Verificado: `pip install -e ".[dev]"` OK, `pytest` 3 passed, `import soda` imprime `0.1.0`, `ruff check .` sin hallazgos.

### T-002 — `Provider` abstracto + `ClaudeCLIProvider`

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Definir una clase base `Provider` abstracta y una implementación `ClaudeCLIProvider` que invoque el CLI `claude` como subproceso y devuelva el texto de respuesta.
- **Resultado:** `src/soda/core/provider.py` con la clase abstracta `Provider` (ABC, método único `send(prompt: str) -> str`) y jerarquía de excepciones `ProviderError` / `ProviderNotFoundError` / `ProviderTimeoutError` / `ProviderExecutionError`. `src/soda/providers/__init__.py` y `src/soda/providers/claude_cli.py` con `ClaudeCLIProvider`: resuelve el ejecutable con `shutil.which`, invoca `[claude, --print]` vía `subprocess.run`, prompt por stdin, timeout configurable (300 s por defecto), sin dependencias nuevas. `tests/test_provider.py` con 11 tests (mocks de `shutil.which`/`subprocess.run`). Verificado: `pytest` 14 passed, `ruff check .` sin hallazgos.

### T-003 — Script de prueba manual end-to-end del provider

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Script manual que envíe un prompt a través del provider (T-002) y muestre la respuesta, para validar la integración con el CLI `claude` fuera de los tests automatizados.
- **Resultado:** `scripts/probar_provider.py` (fuera de `src/soda/`, ver C-003), con prompt por argumento posicional y flags `--archivo`, `--timeout`, `--ejecutable`. Ejecutado contra el CLI real: verificación básica ("OK", 3.2 s), prompt largo de 13.109 caracteres devuelto correctamente por stdin (validando la decisión de no usar argumentos de línea de comandos), ida y vuelta UTF-8 perfecta con acentos/eñes/signos, stdout limpio sin ruido de banners, y los tres caminos de error (`ProviderNotFoundError`, `ProviderTimeoutError`) verificados en real con exit code 1.

### T-004 — Plantilla de contenido de `_persistence`

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Definir qué archivos siembra `soda init` en un proyecto destino, presumiblemente los seis archivos de memoria (`progress.md`, `tasks.md`, `lessons.md`, `decisions.md`, `constraints.md`, `assumptions.md`) con sus índices vacíos, en `src/soda/templates/_persistence/`.
- **Pendiente:** Todo el diseño e implementación. Primer paso de la ruta acordada hacia `soda init`.

### T-005 — `src/soda/cli.py` con el subcomando `init`

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Escribir la CLI única con subcomandos (D-002); `soda init` copia la plantilla de T-004 a un `project_root` explícito (C-002), nunca a una ruta fija ni relativa implícita al directorio actual.
- **Pendiente:** Depende de T-004. No iniciado.

### T-006 — Habilitar entry point e instalar con pipx

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Descomentar `[project.scripts]` en `pyproject.toml` (`soda = "soda.cli:main"`) e instalar con `pipx install -e <ruta del repo>` (D-003), para que `soda` quede disponible en el PATH y se pueda invocar desde cualquier proyecto destino.
- **Pendiente:** Depende de T-005. No iniciado.
