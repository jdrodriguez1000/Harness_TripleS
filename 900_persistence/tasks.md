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
| [T-009](#t-009--soda-init-debe-sembrar-_guideline-en-el-proyecto-destino) | `soda init` debe sembrar `_guideline/` en el proyecto destino | Implementada |
| [T-010](#t-010--revisión-de-fondo-de-methodologymd) | Revisión de fondo de `methodology.md` | Implementada |
| [T-011](#t-011--unificar-taxonomía-de-estado-entre-principlesmd-5-y-el-03-nuevo) | Unificar taxonomía de estado entre `principles.md` §5 y el §0.3 nuevo | Implementada |
| [T-012](#t-012--implementar-sesion-starter-como-agente-de-soda) | Implementar `sesion-starter` como agente de `soda` | No implementada |
| [T-013](#t-013--soda-start-rama-de-proyecto-vacío-bootstrap-git-en-python-puro) | `soda start`, rama de proyecto vacío: bootstrap Git en Python puro | No implementada |
| [T-014](#t-014--stateyaml-formato-mínimo-del-estado-del-incremento) | `state.yaml`: formato mínimo del estado del incremento | No implementada |
| [T-015](#t-015--soda-status-lectura-del-estado-cero-cuota) | `soda status`: lectura del estado, cero cuota | No implementada |
| [T-016](#t-016--soda-step-invocar-al-agente-especializado-que-corresponda) | `soda step`: invocar al agente especializado que corresponda | No implementada |
| [T-017](#t-017--soda-close-invocar-a-sesion-closer) | `soda close`: invocar a `sesion-closer` | No implementada |

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

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Hoy `principles.md` y `methodology.md` (y desde T-010, también `agents-and-evaluation.md`) viajan dentro del paquete instalado (verificado con el wheel, T-008) pero ningún comando los coloca en el proyecto destino: eran carga muerta. Faltaba un accesor en `src/soda/templates/__init__.py` análogo a `persistence_root()`, y decidir si lo hace `init` o un subcomando aparte. El usuario decidió ampliar D-012 (enmendada, ver D-020).
- **Resultado:** `src/soda/templates/__init__.py`: añadidos `GUIDELINE_DIRNAME` (`"_guideline"`), `GUIDELINE_FILENAMES` (`principles.md`, `methodology.md`, `agents-and-evaluation.md`, en orden de lectura), `guideline_root()` y `read_guideline_template()`, simétricos a los de `_persistence`; nuevo helper privado `_leer()` que unifica la validación de nombre desconocido. `src/soda/cli.py`: nueva función `init_guideline()` junto a `init_persistence()`, ambas apoyadas en un `_sembrar()` común parametrizado; nueva constante de acción `DIFIERE = "difiere, saltado"` (ver D-021); `init` siembra las dos carpetas en una sola pasada y las reporta en dos bloques independientes, cada uno con su "Destino:" y su resumen. `README.md` actualizado (estado actual, sección de `soda init` con ambas carpetas, nueva sección "Los tres documentos normativos", árbol de estructura). Verificado: la suite pasó de 57 a 82 tests (25 nuevos entre `tests/test_templates.py` y `tests/test_cli.py`: siembra, idempotencia, relleno parcial, `--force`, C-002 vía chdir, detección de desfase, y un test explícito de que la memoria nunca se marca `DIFIERE`), todos en verde; `ruff check` limpio; wheel construido e inspeccionado (3 `.md` de `_guideline/` + 6 de `_persistence/` presentes); ejecución real en proyecto de prueba: primera pasada siembra 6+3, segunda pasada tras corromper `methodology.md` reporta `difiere, saltado` sin tocar el archivo y sugiere `--force`; el `soda` global (pipx editable) ya trae el cambio.

### T-010 — Revisión de fondo de `methodology.md`

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** `methodology.md` (883 líneas) recibió en la sesión anterior solo arreglos mecánicos y de sincronización de códigos (ver T-007); quedaban defectos de fondo verificados y vivos, resueltos aquí en tres pasos.
- **Resultado:** **Paso 1 (recorte de alcance):** el usuario acotó el harness a trabajar exclusivamente proyectos de desarrollo de software, invalidando la premisa fundacional del documento (cubría también Ciencia de datos/ML). Cabecera reescrita, §2 pasó de "Tipos de proyecto y su adaptación" a "La espina de un incremento" (sin renumerar secciones), ~10 puntos limpiados de referencias a ML/notebook/umbral de métrica, §8 de 3 filas a 2 (piezas reutilizables de la fila ML reubicadas en la de entregables documentales). Se preservó la distinción entre "probabilístico" referido al producto ML (se fue) y al agente LLM que construye (se quedó, tesis central del harness). Resultado real: 53 inserciones/54 borrados (no 45-60 como se estimó, ver L-008). Se declaró explícitamente en §2 la equivalencia entre la espina de 6 fases y la espina única de 11 pasos de §3/§7.1, contradicción no detectada antes. **Paso 2 (marcado normativo vs. diferido):** se introdujeron tres estados en vez de dos — sin marca (normativo, rige desde la primera sesión), `[DIFERIDO]` (decidido no adoptar aún, con gatillo de adopción, se revierte con evidencia), `[PENDIENTE]` (se quiere pero falta una pieza nombrada, se revierte entregándola) — ver D-018. Nueva §0.3 "Estado de aplicación: qué rige hoy y qué no", con el núcleo normativo enunciado y una tabla de 8 piezas ausentes con columna "qué se hace sin ella" (`AGENTS.md`, `_context/project.yaml`, `_templates/`, `state.yaml`, motor de traza + `_trace/`, `conformance.sh`, `git-protocol.md`, flota de arquetipos). 9 marcas `[DIFERIDO]` y 14 `[PENDIENTE]` colocadas en encabezado de sección y fila de TOC. Corregidas dos afirmaciones de fondo que mentían en presente: §10.2 (decía que la capa barata "existe hoy"; reescrita como especificación) y §10 (ahora declara que sin traza, un agente no puede declararse CONFORME por su cuenta). **Paso 3 (división del archivo):** el gatillo de división ya estaba disparado (418 líneas contra el umbral ~250). Creado `src/soda/templates/_guideline/agents-and-evaluation.md` (483 líneas, §3.1/§5/§8/§9/§10); `methodology.md` bajó a 607 líneas (§0-§4, §6, §7, Apéndice). Sin renumerar: los números de sección quedaron únicos globalmente entre ambos archivos, así que ninguna referencia cruzada hubo que reescribirse (ver D-019); cada hueco dejó un puntero con lo que sigue rigiendo. `principles.md` corregida (citaba `methodology.md §10.2`, mudada). Verificado: 57 tests + `ruff` limpios, wheel construido con los tres `.md` presentes, validación por script de referencias cruzadas (28 secciones definidas, 0 referencias `§N` rotas; de 6 referencias entre archivos, 5 resuelven y la única que no apunta a `git-protocol.md §4`, ya marcado `[PENDIENTE]`).
- **Pendiente / hallazgos derivados:** (a) el defecto (4) original (~12 arquetipos antes del primer agente) no se resolvió, solo se hizo visible marcando §5 con `[PENDIENTE]`; queda como decisión de diseño abierta. (b) Detectada tarea nueva T-011: `principles.md` §5 usa "Gatillo de adopción" para sus tres pendientes, pero los tres requieren infraestructura ausente — en el vocabulario de esta sesión eso es `[PENDIENTE]`, no `[DIFERIDO]`; hay dos taxonomías de estado conviviendo entre archivos que se citan mutuamente.

### T-011 — Unificar taxonomía de estado entre `principles.md` §5 y el §0.3 nuevo

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** `principles.md` §5 ("Pendientes declarados") etiqueta sus tres ítems (motor de traza, umbral de ventana de contexto, cuota cuantificada) con "Gatillo de adopción", pero los tres requieren infraestructura ausente y no una decisión reversible sobre evidencia. En la taxonomía de tres estados introducida en `agents-and-evaluation.md` §0.3 (T-010, D-018), eso corresponde a `[PENDIENTE]`, no a `[DIFERIDO]`. Hay dos vocabularios de estado conviviendo entre dos documentos que se citan mutuamente.
- **Resultado:** `principles.md` §5 reescrita de lista con "Gatillo de adopción" a tabla marcada `[PENDIENTE]` en el encabezado, con columnas "Pieza que falta" / "Qué se hace mientras tanto"; declara explícitamente que ninguno de los tres ítems es `[DIFERIDO]` (se revierten entregando la pieza, no con evidencia). Nueva §0.5 en `principles.md`: importa la taxonomía de tres estados desde `methodology.md` §0.3 por referencia, sin redefinirla; registra que hoy `principles.md` no tiene ningún ítem `[DIFERIDO]`; incluye advertencia sobre una ambigüedad detectada de paso (`principles.md` §0.3 es "Convención de códigos" mientras que `methodology.md` §0.3 es "Estado de aplicación", así que al citar §0.3 entre archivos hay que nombrar el archivo). No se renumeró nada (D-015, D-019). §0.4 de `principles.md` corregida: donde decía "se declara en §5 con su gatillo de adopción" ahora dice `[PENDIENTE]`. `methodology.md` §0.3: pasa de "Toda regla de este documento" a "Toda regla de los tres documentos de `_guideline/`" y se declara definición única de la taxonomía; su tabla de piezas ausentes pasa de 8 a 10 filas, absorbiendo la medición de ocupación de contexto (E-002) y la medición del consumo de cuota (E-014), que antes solo vivían en `principles.md` §5; la fila del motor de traza cita también `principles.md` §5. Verificado: 82 tests + `ruff check` limpios; cero apariciones huérfanas de "gatillo de adopción" (las 5 restantes cuelgan de un `[DIFERIDO]` legítimo); script ad hoc de validación de referencias cruzadas: 43 secciones definidas entre los tres archivos, 0 referencias rotas reales (7 marcadas por el script eran falsos positivos de su propia regex, y la redacción de la única línea nueva propia se ajustó para quedar inequívoca). Tamaños finales: `principles.md` 410 líneas, `methodology.md` 611, `agents-and-evaluation.md` 482.

### T-012 — Implementar `sesion-starter` como agente de `soda`

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Con T-009 cerrada, el proyecto destino ya recibe memoria (`_persistence/`) y doctrina (`_guideline/`), pero nada las lee: el paquete siembra y se va. `sesion-starter` cierra ese lazo. Es el de menor riesgo de los agentes propios de `soda` porque ya existe un prototipo probado: el agente `harness-starter` de este repo con su skill `session-startup`, ejercitado durante cinco sesiones; la especificación se porta, no se inventa. Sería además el primer consumidor real de la capa de proveedores (`Provider` + `ClaudeCLIProvider`, T-002/T-003), que hoy funciona pero nadie llama.
- **Pendiente:** Todo el diseño e implementación. La precondición original (si `agents-and-evaluation.md` §5 describe el destino o especifica lo que se construye) quedó resuelta en sesión de diseño posterior (ver D-022, D-023): §5 pasa de descripción a hoja de ruta, así que sí especifica lo que se construye. Fijado también el lugar de esta tarea en el orden de construcción (D-028): es el **segundo** paso, justo después de T-013 (bootstrap de proyecto vacío), y antes de `state.yaml`/`soda status`/`soda step`/`soda close`. Razón de ir segundo: es el único agente que no puede romper nada (solo lectura), ya tiene banco de pruebas real (las seis sesiones de contenido auténtico de `900_persistence/` de este repo) y su prompt ya está escrito y probado (skill `session-startup`, ejercitada seis veces). Descartada explícitamente como alternativa de "siguiente tarea": implementar `CodexCLIProvider` primero, porque añadir un segundo proveedor cuando el primero todavía no tiene consumidor profundiza código sin uso.

### T-013 — `soda start`, rama de proyecto vacío: bootstrap Git en Python puro

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** `soda start` tiene dos ramas internas. Esta tarea cubre la rama de proyecto vacío: `git init`, `.gitignore`, pedir al humano la URL del repo de GitHub, `git remote add`, primer commit, push. Todo en Python puro, sin invocar ningún LLM (D-026). Es el punto de entrada de la siguiente sesión.
- **Pendiente:** Todo el diseño e implementación. Depende de detectar "proyecto vacío" (memoria sin escribir) para decidir la rama; la otra rama (proyecto con memoria) invoca a `sesion-starter` (T-012) y no es parte de esta tarea.

### T-014 — `state.yaml`: formato mínimo del estado del incremento

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Definir el formato mínimo de `_increments/<id>/state.yaml`, hoy listado como pieza `[PENDIENTE]` en `methodology.md` §0.3. Es prerrequisito de `soda step` y `soda status` (D-027): sin él no hay dónde leer de forma determinista en qué punto está un incremento (spec, plan, rojo/verde), y la narrativa en prosa de `tasks.md` no se puede parsear.
- **Pendiente:** Todo el diseño e implementación.

### T-015 — `soda status`: lectura del estado, cero cuota

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Comando de solo lectura: "¿dónde estoy y qué haría el próximo `step`?". No invoca ningún LLM, así que no consume cuota ni tiene riesgo. Depende de `state.yaml` (T-014). Sirve además como la forma más barata de verificar que la detección de estado funciona antes de que `soda step` dependa de ella.
- **Pendiente:** Todo el diseño e implementación.

### T-016 — `soda step`: invocar al agente especializado que corresponda

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Detecta el punto del proyecto (vía `state.yaml`, T-014) y ejecuta el siguiente paso con el agente especializado que corresponda (Probador, Implementador, Refactorizador, Revisor de código, etc., ver D-022). Nombre elegido sobre `soda continue` porque la intención es "haz UN paso y devuelve el control", no "sigue hasta terminar"; así funcionan los gates humanos de §3 (D-026).
- **Pendiente:** Todo el diseño e implementación. Depende de que existan agentes especializados que invocar; el camino feliz no necesita juicio de orquestación LLM (D-025), así que la selección del agente es mecánica contra la tabla de §3.

### T-017 — `soda close`: invocar a `sesion-closer`

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Invoca al agente `sesion-closer`: redacta el hito, decide qué va a `lessons.md` y qué a `decisions.md`, mantiene índices (juicio de redacción, no se hardcodea). El commit y el push los hace Python al final, no el agente.
- **Pendiente:** Todo el diseño e implementación. Último paso del orden de construcción (D-028).
