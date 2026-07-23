# Tasks

## Índice

| Código | Título | Estado |
|--------|--------|--------|
| [T-001](#t-001--estructura-base-del-proyecto-python) | Estructura base del proyecto Python | Implementada |
| [T-002](#t-002--provider-abstracto--claudecliprovider) | `Provider` abstracto + `ClaudeCLIProvider` | Implementada |
| [T-003](#t-003--script-de-prueba-manual-end-to-end-del-provider) | Script de prueba manual end-to-end del provider | Implementada |
| [T-004](#t-004--plantilla-de-contenido-de-_persistence) | Definir el contenido de la plantilla `_persistence` | Implementada |
| [T-005](#t-005--srcsodaclipy-con-el-subcomando-init) | Escribir `src/soda/cli.py` con el subcomando `init` | Implementada |
| [T-006](#t-006--habilitar-entry-point-e-instalar-con-pipx) | Habilitar el entry point e instalar con pipx | Implementada |
| [T-007](#t-007--actualizar-905_guidelineprinciplesmd-antes-de-escribir-el-primer-agente) | Actualizar `905_guideline/principles.md` antes de escribir el primer agente | No implementada |

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

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Definir qué archivos siembra `soda init` en un proyecto destino, presumiblemente los seis archivos de memoria (`progress.md`, `tasks.md`, `lessons.md`, `decisions.md`, `constraints.md`, `assumptions.md`) con sus índices vacíos, en `src/soda/templates/_persistence/`.
- **Resultado:** Creados los seis archivos de plantilla en `src/soda/templates/_persistence/` (forma vacía exacta de `900_persistence/`, respetando diferencias reales entre archivos: `tasks.md` conserva la línea de estados posibles, `constraints.md`/`assumptions.md` sin columna de fecha, `progress.md` con índice de viñetas y tres secciones fijas; marcador `_(vacío)_` uniforme). Borrado el `.gitkeep`. Creado `src/soda/templates/__init__.py` con `PERSISTENCE_DIRNAME`, `PERSISTENCE_FILENAMES`, `persistence_root()` (vía `importlib.resources.files()`, ver D-009) y `read_persistence_template(nombre)`. `tests/test_templates.py` con 24 tests, todos accediendo vía paquete, nunca por ruta relativa al repo. Verificación decisiva: wheel construido, instalado en venv limpio fuera del árbol de fuentes, y plantilla leída íntegra desde `site-packages/soda/templates/`.

### T-005 — `src/soda/cli.py` con el subcomando `init`

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Escribir la CLI única con subcomandos (D-002); `soda init` copia la plantilla de T-004 a un `project_root` explícito (C-002), nunca a una ruta fija ni relativa implícita al directorio actual.
- **Resultado:** Creado `src/soda/cli.py`: `main(argv)` con `argparse` y subparsers (preparado para `start`/`close`), constantes `CREADO`/`SALTADO`/`SOBRESCRITO`, y `init_persistence(project_root: Path, force: bool)`. No destructivo por defecto (relleno parcial e idempotente, ver D-011), `--force` sobrescribe nombrando cada archivo reemplazado. Falla con `NotADirectoryError` si `project_root` no existe (ver D-013); crea `_persistence/` si falta. Códigos de salida 0/1. Incluye `_forzar_utf8()` (L-003). `tests/test_cli.py` con 19 tests. Verificación manual con carpeta `mi-proyecto-ñ` (estresa L-003), memoria acumulada simulada preservada tras repetir `init`, archivo borrado recreado individualmente, `--force` sobrescribiendo los seis, destino inexistente con exit 1, y ayuda sin subcomando. Corregido defecto cosmético de concordancia de número en el resumen ("1 creados"), con test que lo cubre.

### T-006 — Habilitar entry point e instalar con pipx

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Descomentar `[project.scripts]` en `pyproject.toml` (`soda = "soda.cli:main"`) e instalar con `pipx install -e <ruta del repo>` (D-003), para que `soda` quede disponible en el PATH y se pueda invocar desde cualquier proyecto destino.
- **Resultado:** Descomentado `[project.scripts]`. Verificado primero en venv desechable antes de tocar la máquina. `pipx` instalado con el Python global 3.12.10 (deliberadamente fuera del venv del repo); `pipx ensurepath` no tuvo que modificar nada porque `~/.local/bin` ya estaba en el PATH. Instalado con `pipx install -e <ruta del repo>`. Verificado: `which soda` resuelve correctamente, visible desde PowerShell, `soda init` funciona desde una carpeta cualquiera, y el modo editable es real (`soda.cli.__file__` resuelve a `src/soda/cli.py` del repo, un cambio en `src/` afecta al comando global sin reinstalar). El usuario confirmó las pruebas por su cuenta.

### T-007 — Actualizar `905_guideline/principles.md` antes de escribir el primer agente

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Resolver las contradicciones internas detectadas en `905_guideline/principles.md` y dejarlo operable antes de redactar el prompt del primer agente del harness (`sesion-starter`, `agent-worker`, `sesion-closer`). El documento es la fuente canónica de comportamiento y se traducirá en las Reglas Vinculantes de cada agente; una regla contradictoria produce un agente incoherente.
- **Pendiente:**
  1. **E7 vs. el modelo de suscripción.** E7 recomienda 3–5 subagentes en paralelo argumentando que "la paralelización escala el uso de tokens eficientemente". Ese hallazgo proviene de investigación sobre API de pago por token. El harness corre sobre suscripciones (`idea.md`), donde no se compran tokens sino una cuota con límites de tasa: paralelizar 5 subagentes quema la ventana de uso 5 veces más rápido y puede dejar la sesión rate-limited. Falta condicionar la paralelización al presupuesto de cuota disponible.
  2. **NC-1 y NC-6 vs. la autonomía que describe E12.** Ambas exigen detenerse y consultar ante cualquier ambigüedad, pero un subagente en paralelo (E12) no tiene canal con el humano. Aplicadas literalmente paralizan el sistema; aplicadas con sentido común quedan como letra muerta. Falta un umbral explícito: decisiones reversibles y de bajo impacto se toman y se documentan; decisiones que cambian materialmente el resultado o son difíciles de revertir se escalan. Además NC-1 y NC-6 son casi la misma regla: fusionarlas o diferenciarlas de verdad.
  3. **NC-5 ("Definición de Terminado = test en verde. Sin excepción") vs. E13 y vs. la realidad del proyecto.** T-003 (script manual contra el CLI real) no tiene test por diseño, y la verificación decisiva de T-004 (instalar el wheel en un venv limpio) tampoco vive en pytest. Además no se puede poner en verde un test determinista sobre el prompt de un agente, cuya salida es probabilística — cosa que el propio E13 reconoce. Sustituir por verificación proporcional a la naturaleza del artefacto: test determinista donde se pueda, rúbrica/juez donde la salida sea probabilística, verificación manual documentada donde ninguna aplique. Lo inaceptable es "terminado sin evidencia", no "terminado sin pytest".
  4. **E2 pide una auto-observación que E13 declara inválida.** E2 activa el context reset "si el agente empieza a cerrar tareas sin completarlas", pero si quien lo detecta es el propio agente, choca con E13 (el auto-reporte no es evidencia). Hace falta un observador externo o una señal mecánica (porcentaje de ventana consumido, pasos declarados vs. ejecutados en la traza).
  5. **Reescribir NC-1…NC-6 en forma verificable.** E13 exige traducir las Reglas Vinculantes en checks sobre (traza + artefacto), pero las NC están escritas en prosa y ninguna es chequeable mecánicamente. Cada NC necesita: enunciado, predicado verificable sobre traza o artefacto, y consecuencia cuando falla. Es el prerrequisito para implementar E13.
  6. **Añadir lo que falta:** presupuesto de sesión y límite de pérdida (qué pasa cuando un subagente falla N veces, cuánto puede gastar una tarea antes de escalar); y frontera de permisos y operaciones destructivas para agentes con acceso a shell y filesystem sobre repos ajenos (nada de `--force`, no borrar sin confirmación, no commitear secretos, rutas fuera de límites).
  7. **Orden de precedencia interno** entre P, E y NC cuando entran en conflicto: la cabecera solo resuelve el conflicto con instrucciones externas.
  8. **Menores:** pasar la numeración a 3 dígitos permanentes (`P-001`, `E-001`, `NC-001`) para alinearla con la convención del proyecto y no tener que renumerar al insertar; E11 (búsqueda de amplio a estrecho) es táctica de investigación, no estándar de comportamiento del sistema, y encaja mejor en el prompt del agente investigador; E8 se solapa con P6 y no da criterio de cuándo aplicar extended thinking.
- **Dependencia / momento:** No bloquea T-005 ni T-006 (la CLI de `init` no involucra agentes). Es BLOQUEANTE para el momento en que se escriba el primer prompt de agente del harness. Debe hacerse antes de esa tarea, no después.
