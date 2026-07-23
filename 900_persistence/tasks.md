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
| [T-007](#t-007--actualizar-905_guidelineprinciplesmd-antes-de-escribir-el-primer-agente) | Actualizar `905_guideline/principles.md` antes de escribir el primer agente | Implementada |
| [T-008](#t-008--mudar-905_guideline-a-srcsodatemplates_guideline) | Mudar `905_guideline/` a `src/soda/templates/_guideline/` | Implementada |
| [T-009](#t-009--soda-init-debe-sembrar-_guideline-en-el-proyecto-destino) | `soda init` debe sembrar `_guideline/` en el proyecto destino | No implementada |
| [T-010](#t-010--revisión-de-fondo-de-methodologymd) | Revisión de fondo de `methodology.md` | No implementada |

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

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Resolver las contradicciones internas detectadas en `principles.md` (entonces en `905_guideline/`, hoy en `src/soda/templates/_guideline/`, ver T-008) y dejarlo operable antes de redactar el prompt del primer agente del harness. El documento es la fuente canónica de comportamiento y se traducirá en las Reglas Vinculantes de cada agente; una regla contradictoria produce un agente incoherente.
- **Resultado:** Los 8 puntos pendientes quedaron resueltos. `principles.md` pasó de 125 a 384 líneas y se reorganizó en tres secciones por audiencia (§1 Diseño del arnés, §2 Operación del orquestador, §3 Reglas de ejecución del agente), corrigiendo la raíz común de 5 de los 8 choques: el documento mezclaba tres audiencias declarándolas todas "vinculantes para todo agente". Resoluciones concretas: E-007 invertida a default secuencial (paralelizar exige tres condiciones explícitas; C-006); NC-001 fusiona NC-1/NC-6 con tabla de umbral (reversible+bajo impacto → decide y documenta, irreversible o cambia el resultado → escala al ORQUESTADOR, no al humano); NC-005 pasa a evidencia proporcional a la naturaleza del artefacto (tabla de cuatro casos, con T-003 y T-004 de este proyecto como ejemplos); E-002 sustituye la auto-observación por tabla de señales externas; E-014 nueva (presupuesto de sesión y límite de pérdida); NC-007 nueva (frontera de operaciones destructivas, única regla con consecuencia PARADA); §0.2 fija precedencia humano > NC > P > E; códigos a 3 dígitos permanentes; E-008 absorbida en P-006, E-011 retirada, NC-006 retirada (tabla §4 de retirados con destino); §5 nueva de pendientes declarados. `methodology.md` (883 líneas, citaba esos códigos 44 veces) se resincronizó: ceros rellenados, 3 referencias a NC-6 remapeadas a NC-001, verificado por script que cero códigos citados no existen en `principles.md`. Cabecera de rol añadida a ambos documentos declarando que son producto. Arreglos mecánicos en `methodology.md`: `_template/` unificado a `_templates/` (8 usos), typo `constrains`→`constraints`, y citas colgantes a `L-015`/`L-022` (lecciones de otro proyecto inexistentes aquí) reemplazadas conservando la narrativa sin el código.
- **Dependencia / momento:** Quedaron identificados dos frentes nuevos no cubiertos por esta tarea: T-009 (sembrar `_guideline/` en destino) y T-010 (revisión de fondo de `methodology.md`, 883 líneas).

### T-008 — Mudar `905_guideline/` a `src/soda/templates/_guideline/`

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** `principles.md` y `methodology.md` son producto (viajan con `soda` al proyecto destino, se instalan como `_guideline/`), no andamiaje de este repo (C-003); mudarlos de la raíz (`905_guideline/`) a `src/soda/templates/_guideline/` con `git mv`.
- **Resultado:** `905_guideline/` movida con `git mv` a `src/soda/templates/_guideline/`. Verificado: wheel construido e instalado en venv desechable fuera del árbol de fuentes, ambos archivos legibles desde la instalación vía `importlib.resources` (`methodology.md` 883 líneas, `principles.md` 384). No hizo falta tocar `pyproject.toml` (`packages = ["src/soda"]` ya arrastra los `.md`). 57 tests en verde, `ruff` limpio, el `soda` global (pipx editable) sigue funcionando. `README.md` actualizado: el árbol de estructura ya no lista `905_guideline/` en la raíz y desglosa `templates/` en `_persistence/` y `_guideline/`. Hallazgo colateral: `methodology.md` nunca había estado en git (untracked, 876 líneas); quedó incorporado al índice en esta mudanza.

### T-009 — `soda init` debe sembrar `_guideline/` en el proyecto destino

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Hoy `principles.md` y `methodology.md` viajan dentro del paquete instalado (verificado con el wheel, T-008) pero ningún comando los coloca en el proyecto destino: son carga muerta. Falta un accesor en `src/soda/templates/__init__.py` análogo a `persistence_root()`, y decidir si lo hace `init` o un subcomando aparte.
- **Pendiente:** Todo el diseño e implementación. Nota importante: esta tarea, tal como está planteada, contradice D-012 (`init` solo siembra los seis archivos de memoria); habría que revisar esa decisión o superarla con una decisión nueva antes de implementar.

### T-010 — Revisión de fondo de `methodology.md`

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** `methodology.md` (883 líneas) recibió en esta sesión solo arreglos mecánicos y de sincronización de códigos (ver T-007); quedan defectos de fondo verificados y aún vivos.
- **Pendiente:** (1) Nada marca qué es normativo hoy vs. qué está diferido — lo que sí se aplicó en `principles.md` §5, pese a que `methodology.md` confiesa ese fallo en su propia §10.2 (perfiles de conformidad vivos en los prompts durante tres corridas sin que nadie los ejecutara); §5.2 aplica bien la disciplina de gatillo de adopción, pero solo en esa sección. (2) Su propio gatillo de división ya se disparó: la cabecera dice dividir si el bloque §5+§8+§9+§10+§3.1 supera ~250 líneas; hoy ronda las 375. (3) Referencias hacia adelante a artefactos que `soda` aún no entrega (`AGENTS.md` x3, `_context/project.yaml` x3, `git-protocol.md` x3, `_tools/conformance.sh`, `client_brief` x4): no son defectos, pero constituyen backlog a explicitar. (4) Tensión de fondo: el documento especifica ~12 arquetipos de agente y varias capas de evaluación antes de que exista un solo agente del harness, lo que roza E-004 (mínima complejidad).
