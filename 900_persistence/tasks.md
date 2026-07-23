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
| [T-012](#t-012--implementar-sesion-starter-como-agente-de-soda) | Implementar `sesion-starter` como agente de `soda` | Implementada |
| [T-013](#t-013--soda-start-rama-de-proyecto-vacío-bootstrap-git-en-python-puro) | `soda start`, rama de proyecto vacío: bootstrap Git en Python puro | Implementada |
| [T-014](#t-014--stateyaml-formato-mínimo-del-estado-del-incremento) | `state.yaml`: formato mínimo del estado del incremento | No implementada |
| [T-015](#t-015--soda-status-lectura-del-estado-cero-cuota) | `soda status`: lectura del estado, cero cuota | No implementada |
| [T-016](#t-016--soda-step-invocar-al-agente-especializado-que-corresponda) | `soda step`: invocar al agente especializado que corresponda | No implementada |
| [T-017](#t-017--soda-close-invocar-a-sesion-closer) | `soda close`: invocar a `sesion-closer` | No implementada |
| [T-018](#t-018--spike-bucle-repl-exterior--delegación-a-subagente-sobre-suscripción) | Spike: bucle REPL exterior + delegación a subagente sobre suscripción | Implementada |
| [T-019](#t-019--reevaluar-el-orden-de-construcción-de-soda-a-la-luz-del-pivote-replsuscripción) | Reevaluar el orden de construcción de `soda` a la luz del pivote REPL+suscripción | Implementada |
| [T-020](#t-020--spike-de-delegación-con-tool_use-estructurado-claude-agent-sdk-sobre-suscripción) | Spike de delegación con `tool_use` estructurado (Claude Agent SDK) sobre suscripción | Implementada |
| [T-021](#t-021--sesión-persistente-detrás-de-provider) | Sesión persistente detrás de `Provider` | Implementada |
| [T-022](#t-022--bucle-repl-de-soda--canal-con-el-humano) | Bucle REPL de `soda` + canal con el humano | Implementada |
| [T-023](#t-023--memoria-como-tool-de-lectura--sesion-starter-portado-a-la-sesión) | Memoria como tool de lectura + `sesion-starter` portado a la sesión | No implementada |
| [T-024](#t-024--memoria-como-tool-de-escritura--sesion-closer) | Memoria como tool de escritura + `sesion-closer` | No implementada |
| [T-025](#t-025--descubridor-como-subagente-agentdefinition) | `Descubridor` como subagente `AgentDefinition` | No implementada |
| [T-026](#t-026--prototipador-como-subagente--bucle-p3p4) | `Prototipador` como subagente + bucle P3↔P4 | No implementada |
| [T-027](#t-027--gate-de-madurez--feature-freeze-cierre-del-estadio-de-prototipo) | Gate de madurez / feature freeze: cierre del estadio de prototipo | No implementada |

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

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Con T-009 cerrada, el proyecto destino ya recibe memoria (`_persistence/`) y doctrina (`_guideline/`), pero nada las lee: el paquete siembra y se va. `sesion-starter` cierra ese lazo. Es el de menor riesgo de los agentes propios de `soda` porque ya existe un prototipo probado: el agente `harness-starter` de este repo con su skill `session-startup`, ejercitado durante cinco sesiones; la especificación se porta, no se inventa. Es además el primer consumidor real de la capa de proveedores (`Provider` + `ClaudeCLIProvider`, T-002/T-003).
- **Resultado:** `src/soda/agents/memoria.py`: `leer_memoria(project_root)` en Python puro (cero LLM), devuelve `MemoriaProyecto` con `progress.md`/`tasks.md` íntegros (`OBLIGATORIOS`), los otros cuatro solo con su sección `## Índice` (`extraer_indice`), archivos ausentes por convención (`faltantes`) y la bandera `vacia` (compara cada obligatorio contra la plantilla del paquete, normalizando CRLF con `_normalizar`; ante duda se inclina a "hay estado"). `src/soda/agents/prompts/sesion_starter.md`: prompt portado de la skill `session-startup`, sin el Caso A (bootstrap, que quedó en Python) y sin instrucciones de leer archivos (Python ya se los entrega). `src/soda/agents/sesion_starter.py`: clase `SesionStarter(provider)`, método `informe(project_root)` que compone el prompt (`componer_prompt`, cada archivo entre cercas literales para no confundir sus `##`/tablas con estructura del prompt) y lo envía; lanza `MemoriaVaciaError` antes de invocar al modelo si la memoria sigue vacía. `src/soda/providers/claude_cli.py` ampliado con `model`, `tools` (`()` por defecto, sin herramientas), `cwd` y `solo_suscripcion` (ver D-029 a D-031); añade siempre `--no-session-persistence`. `src/soda/core/flota.py`: `MODELOS = {"sesion-starter": "haiku"}` y `proveedor_para(agente, project_root)`, punto único agente→modelo (D-033). `scripts/probar_sesion_starter.py`: prueba manual end-to-end contra el CLI real, usando `900_persistence/` de este repo como banco de pruebas. Verificado: `tests/test_memoria.py` y `tests/test_sesion_starter.py` nuevos, `tests/test_provider.py` ampliado, 145 tests en verde, `ruff check` limpio, y prueba manual del usuario en máquina real (informe de haiku sobre la memoria real del proyecto).

### T-013 — `soda start`, rama de proyecto vacío: bootstrap Git en Python puro

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** `soda start` tiene dos ramas internas. Esta tarea cubre la rama de proyecto vacío: `git init`, `.gitignore`, pedir al humano la URL del repo de GitHub, `git remote add`, primer commit, push. Todo en Python puro, sin invocar ningún LLM (D-026).
- **Resultado:** `src/soda/core/git.py`: plomería sobre el binario `git` (`es_repositorio`, `rama_actual`, `url_del_remoto`, `configuracion`/`fijar_configuracion` —siempre local, nunca global—, `hay_algo_que_confirmar`, `commit`, `intentar`/`ejecutar`); sin `--force`, `reset --hard` ni `clean` en el módulo; `GitError` conserva el stderr entero. `src/soda/templates/gitignore-base.txt`: plantilla de `.gitignore` (nombre distinto de `.gitignore` dentro del paquete a propósito, para no ser ignorada ella misma); no ignora `_persistence/` ni `_guideline/`. `src/soda/start.py`: `bootstrap(project_root, preguntar=input, informar=print)` — inicia repositorio, siembra `.gitignore` (o reporta reglas faltantes sin tocar uno existente), asegura identidad de git preguntando si falta (local al repo), commit inicial, pide la URL del remoto (hasta 3 intentos, `Enter` la omite), configura o repregunta si `origin` ya apunta a otro sitio, hace push y traduce los fallos de push ya conocidos (email de privacidad L-002, repo inexistente, rama divergente) a instrucciones concretas; nunca usa `--force`. `SinCanalConElHumanoError` si `input()` revienta por EOF (entrada redirigida). `src/soda/templates/__init__.py` ampliado con `GITIGNORE_FILENAME`, `GITIGNORE_TEMPLATE`, `read_gitignore_template()`. `src/soda/cli.py`: subcomando `start`, que lee la memoria con `leer_memoria` y bifurca a `bootstrap()` (memoria vacía) o a `SesionStarter` con el agente `sesion-starter` (memoria con estado). Verificado: `tests/test_start.py` nuevo, 145 tests en verde, `ruff check` limpio, y prueba manual del usuario en carpeta nueva real: `init` → `start` → repo publicado en GitHub con `_persistence/`/`_guideline/` versionados → repetición idempotente → rama con memoria devolviendo el informe de haiku.

### T-014 — `state.yaml`: formato mínimo del estado del incremento

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Definir el formato mínimo de `_increments/<id>/state.yaml`, hoy listado como pieza `[PENDIENTE]` en `methodology.md` §0.3. Es prerrequisito de `soda step` y `soda status` (D-027): sin él no hay dónde leer de forma determinista en qué punto está un incremento (spec, plan, rojo/verde), y la narrativa en prosa de `tasks.md` no se puede parsear.
- **Pendiente:** Todo el diseño e implementación. Antes de que la sesión pivotara a D-035, se avanzó diseño que conviene no perder para cuando T-019 lo retome: (a) construir y verificar quedan fuera del modelo de `state.yaml` por ahora (bloques `[PENDIENTE]` declarados, no omitidos), porque su contenido lo escribirían agentes de la flota que aún no existen — volver a ellos cuando `soda step` deba ejecutar el paso 8/10 caso por caso, o cuando una interrupción a mitad del paso 8 obligue a releer el código; (b) no se crea un comando `soda increment`: el paso 1 (abrir incremento) lo haría `soda step` cuando no hay incremento abierto, misma figura de dos ramas que `soda start`, y `soda status` anunciaría esa rama; (c) el prototipado no iría en el `state.yaml` del incremento — si acaso llevara estado, sería un archivo aparte (su espina es de 5 pasos con bucle P3↔P4, distinta de los 11 pasos del incremento); se decidió no construirlo ahora; (d) esquema propuesto: 11 pasos de §3, `paso_actual` derivado del disco (no almacenado, para no desincronizar), `veredicto` presente pero desglose por evaluador fuera. Con el pivote a REPL+suscripción (D-035), buena parte de esta discusión queda supeditada a la reevaluación de T-019.

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
- **Pendiente:** Todo el diseño e implementación. **Absorbida/reformulada por T-019 (2026-07-23):** con el nuevo orden de construcción, `sesion-closer` deja de ser un `soda close` de un solo disparo invocado sobre `claude -p`; se reconstruye como paso 4 del nuevo orden (T-024, "Memoria como tool de escritura + `sesion-closer`"), redactando sobre la sesión persistente que presenció (no reconstruyendo desde disco, el pago real de D-035), con Python haciendo el commit+push. Esta entrada T-017 se conserva como registro histórico del diseño previo al pivote; el trabajo vivo continúa en T-024.

### T-018 — Spike: bucle REPL exterior + delegación a subagente sobre suscripción

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Validar empíricamente si el modelo del video de referencia (`transcript.md`: bucle REPL, agente orquestador persistente, delegación a subagentes) es viable sobre suscripción (no API de pago por token) antes de comprometer el pivote de arquitectura de `soda` (D-035). Dos spikes exploratorios en `scripts/`, fuera de `src/soda/` (C-003), no producto.
- **Resultado:** `scripts/chat.py`: REPL interactivo mínimo (bucle exterior), reutiliza `ClaudeCLIProvider` (solo suscripción, sin herramientas), multi-turno reenviando el historial completo cada turno porque `claude -p` es de un solo disparo; sale con `/salir`, `/exit`, `/quit`, Ctrl-D o Ctrl-C. `scripts/chat_delegacion.py`: spike del bucle interior — la sesión principal (`sonnet`) decide por su cuenta delegar en un subagente `fecha` (`haiku`) cuando el humano pide la hora, señalizado con la convención a mano `[[LLAMAR:fecha]]` (`claude -p` no expone `tool_use` estructurado sin el Agent SDK, ver L-014); el dato de fecha/hora lo calcula código Python (`datetime.now`), nunca el LLM, que lo inventaría — el subagente solo lo redacta; demuestra además modelo-por-agente (`sonnet` decide, `haiku` redacta). Ambos compilan, `ruff check` limpio, y el usuario los ejecutó en vivo en su propia máquina: `chat.py` responde en tiempo real sobre la suscripción; `chat_delegacion.py` delega y devuelve la hora real correcta al pedirla, y no delega ante una pregunta normal ("hola", "dime un color").
- **Pendiente:** No se promovió nada a producto (`src/soda/`) en esta tarea; eso es T-019.

### T-019 — Reevaluar el orden de construcción de `soda` a la luz del pivote REPL+suscripción

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Con el pivote registrado en D-035 y validado empíricamente en T-018, reevaluar todo el trabajo previo del harness: qué sobrevive (doctrina `_guideline/`, memoria `_persistence/`, `soda init`, `soda start`), qué queda superado (D-025/D-026 reabiertas, la interfaz de 5 comandos, `sesion-starter` como invocación de un solo disparo vía `claude -p`), y definir el nuevo orden de construcción con el REPL/orquestador persistente en el centro. Incluye decidir si el bucle interior de delegación se construye con el Agent SDK for Python (tools/subagentes estructurados, L-014) o se mantiene la convención a mano validada en T-018 (C-008).
- **Resultado:** Sesión de análisis y decisión (2026-07-23, sin código; retoma la sesión previa que había producido D-036 y dejado T-019 con la incógnita de persistencia de sesión abierta). Se resolvió la tensión pendiente entre D-035 (orquestador vivo con juicio) y D-025/D-026 (camino feliz mecánico sin LLM): D-037 fija la espina de control HÍBRIDA — Python posee lo determinista y barato (detección de estado en disco, git/NC-007, gates humanos/C-007, qué fase toca según `methodology.md` §3), la sesión LLM persistente posee solo el juicio y la delegación (D-036). Se confirmó además que el arranque de un proyecto nuevo empieza por el estadio de PROTOTIPADO (`methodology.md` §4: Descubridor → `discovery.md`, Prototipador, bucle P3↔P4, juicio de producto/UX y "mago de Oz" reservados al humano), antes de la maquinaria del incremento de 11 pasos; el prototipo no usa `state.yaml` ni tests. Se construyeron y validaron con el usuario dos flujos de trabajo (proyecto nuevo / proyecto en marcha) etiquetando qué parte actúa en cada paso ([PY]/[LLM]/[SUB]/[HUM]/[MEM]/[GIT]). Entregable: el nuevo orden de construcción, registrado como tareas T-021 a T-027 (ver detalle de cada una), ordenado por fundación → validar la espina con lo de menor riesgo → agentes de trabajo, en pasos pequeños y verificables uno a uno. T-017 (`soda close`/`sesion-closer`) queda absorbida/reformulada por T-024 (paso 4 del nuevo orden); T-014 a T-016 (`state.yaml`, `soda status`, `soda step`) siguen en suspenso, diferidas hasta después del prototipado (son del MVP en adelante), sin cancelarse.
- **Pendiente:** Ninguno propio de esta tarea; el trabajo vivo continúa en T-021 (próximo paso a ejecutar).

### T-020 — Spike de delegación con `tool_use` estructurado (Claude Agent SDK) sobre suscripción

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Con D-036 decidido (el bucle interior de delegación usa el Claude Agent SDK for Python con `tool_use` estructurado, no la convención de marcador de C-008/T-018), construir y verificar en real un spike equivalente a `scripts/chat_delegacion.py` pero usando el Agent SDK sobre suscripción: herramientas `@tool` / subagentes `AgentDefinition`, delegación detectada por el propio SDK, corriendo sin `ANTHROPIC_API_KEY` (autenticación por OAuth de `claude /login`).
- **Resultado:** `pyproject.toml`: nuevo grupo opcional `[project.optional-dependencies] spike = ["claude-agent-sdk"]` (no dependencia dura del producto, solo para `scripts/`, hasta que el Camino B se promueva). `scripts/probar_agent_sdk.py`: smoke test no interactivo de autenticación por suscripción con el Agent SDK (punto 2). `scripts/chat_delegacion_sdk.py`: spike de delegación con `@tool` + `create_sdk_mcp_server` + `AgentDefinition` (agente `clocker`, dueño de la herramienta del reloj), con visualización en pantalla de la invocación del agente y sus pasos internos vía `parent_tool_use_id` (ver L-015). Los tres puntos críticos quedaron verificados EN VIVO por el usuario en su propia terminal, sobre suscripción (`ANTHROPIC_API_KEY` ausente, `is_error=False`): (1) `tool_use` estructurado — el SDK gestiona el bucle interior automáticamente (nada de `if stop_reason == "tool_use"` a mano, corrige la formulación inicial de la descripción de esta tarea), el dato factual (fecha/hora real) lo calcula Python (`datetime.now()`), nunca el modelo, y se observa el `ToolUseBlock` en el stream; (2) autenticación por suscripción confirmada, reutilizando la política de borrar variables de entorno de API de `ClaudeCLIProvider` (D-031); (3) subagente `clocker` definido con `AgentDefinition`, delegación automática desde la sesión principal vía la herramienta `Agent`/`Task` (ver L-017) ante una petición de hora, y ausencia de delegación ante una pregunta que no la necesita ("capital de Francia"). D-036 y L-014 quedan confirmadas por evidencia en vivo, no solo por documentación (ver notas de actualización en `decisions.md` y `lessons.md`). Registradas L-015 a L-017 con los hallazgos concretos de observabilidad y configuración del SDK.
- **Pendiente:** Ninguno propio de esta tarea. Queda pendiente para T-019 la incógnita de persistencia de sesión viva con `ClaudeSDKClient` (dejada fuera del spike deliberadamente).

### T-021 — Sesión persistente detrás de `Provider`

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Paso 1 del nuevo orden de construcción (T-019, D-037). Resuelve la incógnita que T-020 dejó deliberadamente fuera: `ClaudeSDKClient` multi-turno sobre suscripción, encapsulado detrás de una nueva abstracción para no filtrar el SDK más allá de esa frontera (protege D-006/D-008). Recicla la política de borrado de `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN` (D-031) y los ajustes de configuración de L-016 (`permission_mode="bypassPermissions"`, `ToolSearch` permitido en `allowed_tools`).
- **Resultado:** Nueva abstracción async `Sesion` en `src/soda/core/sesion.py` (ABC: gestor de contexto async `__aenter__`/`__aexit__` + `async def enviar(prompt) -> str`), simétrica a `Provider` pero para el contrato multi-turno; reutiliza la jerarquía `ProviderError` (ver D-038). `Provider.send()` de un disparo queda intacto: los agentes de un solo turno (p. ej. `SesionStarter`) no se tocan. `SesionClaudeSDK` + `ClaudeSDKProvider` en `src/soda/providers/claude_sdk.py`: la sesión envuelve un `ClaudeSDKClient` vivo reusado entre turnos (eso da la persistencia), exportados en `providers/__init__.py`. `claude-agent-sdk` promovido de extra `[spike]` a dependencia dura en `pyproject.toml` (D-039): `soda` ya ES un orquestador sobre el SDK. `tests/test_sesion.py` (3, contrato de la ABC) y `tests/test_claude_sdk.py` (9, con un `ClaudeSDKClient` falso); suite total 157 verde (antes 145), `ruff` limpio. Script de verificación en vivo `scripts/probar_sesion_sdk.py` (spike, C-003, no producto): ejecutado por el usuario sobre suscripción, 3 turnos, el turno 2 recordó "Juan" y el turno 3 "verde" (datos solo del turno 1), con `ANTHROPIC_API_KEY presente: False`. Persistencia de contexto y suscripción verificadas en vivo. Hallazgo colateral registrado en L-018: el SDK mergea el entorno del subproceso (`{**os.environ, **options.env}`), no permite borrar una variable heredada, solo sobrescribirla a cadena vacía.
- **Pendiente:** Ninguno propio de esta tarea. Próximo paso: T-022 (bucle REPL de `soda` + canal con el humano), que ya tiene la fundación lista.

### T-022 — Bucle REPL de `soda` + canal con el humano

- **Estado:** Implementada
- **Fecha:** 2026-07-23
- **Descripción:** Paso 2 del nuevo orden de construcción. Enciende la sesión persistente resuelta en T-021, lee stdin y escribe stdout, mantiene la sesión viva entre turnos, y cierra la parte de C-007 que seguía abierta (canal con el humano para gates y diálogo).
- **Resultado:** `src/soda/core/flota.py`: nuevo agente `ORQUESTADOR` (`MODELOS[ORQUESTADOR] = "opus"`, criterio D-033 sin cambiar: el orquestador razona y decide, a diferencia de `sesion-starter` que resume en `haiku`), constante `PROMPT_ORQUESTADOR` (system prompt mínimo, solo idioma/tono, ampliable en T-023/T-025) y `proveedor_de_sesion_para(agente, project_root) -> ClaudeSDKProvider`, hermana de `proveedor_para` pero para el contrato `Sesion` (D-038). `src/soda/repl.py` (nuevo): `correr_repl(sesion, leer, escribir, saludo)`, bucle async sobre una `Sesion` ya abierta, con el mismo patrón inyectable `leer`/`escribir` que ya usaba `soda.start` (facilita testear sin bloquear en `input()`); cierra por `/salir`/`/exit`/`/quit`, por EOF (`EOFError`) o por Ctrl-C (`KeyboardInterrupt`), ignora líneas en blanco, y un `ProviderError` en un turno se reporta sin tumbar el bucle (el contexto acumulado sobrevive). Cierra la parte de C-007 que seguía abierta para el orquestador. `src/soda/cli.py`: `_ejecutar_start` deja de imprimir el informe de `sesion-starter` y terminar; ese informe pasa a ser el `saludo` del REPL. Nuevas `_conversar` (frontera sync→async con `anyio.run`, mismo patrón validado en el spike de T-021) y `_repl_del_orquestador` (abre/cierra la `Sesion` con `async with` y le entrega el bucle). `pyproject.toml`: `anyio` pasa a dependencia directa (antes solo llegaba transitivamente vía `claude-agent-sdk`, ver L-019). Tests nuevos `tests/test_repl.py` y `tests/test_flota.py`; `tests/test_cli.py` ampliado con el flujo `start` → REPL con dobles. `scripts/probar_repl.py` (spike de verificación en vivo, C-003, no producto).
- **Verificación decisiva:** verificada DOS veces sobre la suscripción real (`opus`, sin `ANTHROPIC_API_KEY`). (1) Por el spike: un dato dado en el turno 1 ("Juan", "verde") se recordó en el turno 2; `/salir` cerró limpio. (2) Por el usuario en vivo con el producto real (`soda init` + `soda start` en un proyecto de prueba nuevo): `sesion-starter` dio el informe de reanudación, el REPL se abrió con ese informe como saludo, y el orquestador recordó "Tampa" entre turnos. Suite en 178 tests verdes (antes 157), `ruff` limpio; `Provider.send` y `SesionStarter` quedan intactos (D-038).
- **Nota para T-023:** durante el spike (con `cwd` apuntando a este mismo repo), el orquestador con `ToolSearch` + `bypassPermissions` encontró `900_persistence/` y comentó por su cuenta el estado del proyecto y los cambios sin commitear. No es un fallo de T-022 (el canal y el contexto se probaban y funcionan): confirma que darle a la sesión las tools y el prompt de orquestación reales es justo el alcance de T-023/T-024, y que hoy el system prompt del orquestador es deliberadamente mínimo.

### T-023 — Memoria como tool de lectura + `sesion-starter` portado a la sesión

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Paso 3 del nuevo orden de construcción. Expone la lectura de `_persistence/` como tool del Agent SDK (recicla `src/soda/agents/memoria.py`, T-012) y porta `sesion-starter` del modelo de un disparo sobre `claude -p` al modelo de sesión persistente (T-021/T-022). Es read-only y de menor riesgo; ya tiene banco de pruebas real (`900_persistence/` de este mismo repo).
- **Pendiente:** Todo el diseño e implementación. Depende de T-022.

### T-024 — Memoria como tool de escritura + `sesion-closer`

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Paso 4 del nuevo orden de construcción. Añade una tool de escritura de memoria que ejecuta Python por debajo (el commit y el push de git siguen siendo obra de Python, NC-007, nunca del LLM); construye `sesion-closer` (tarea originalmente T-017, nunca implementada bajo el diseño previo) redactando sobre la sesión persistente que presenció, no reconstruyendo desde disco como hacía el diseño anterior — ese es el pago real del pivote D-035. Es el primer flujo end-to-end del nuevo orden: abrir sesión → conversar → cerrar → persistir → la siguiente sesión reanuda con lo escrito.
- **Pendiente:** Todo el diseño e implementación. Depende de T-023. Absorbe/reformula T-017 (ver nota en su detalle).

### T-025 — `Descubridor` como subagente `AgentDefinition`

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Paso 5 del nuevo orden de construcción. Primer agente de trabajo real del harness: entrevista multi-turno con el humano que produce `discovery.md`, aplicando el riesgo dominante y el campo cerrado de actores de `methodology.md` §4.2/§4.3. Se registra como subagente `AgentDefinition` del Agent SDK, aceptando que la herramienta de delegación se llame `Agent` o `Task` según el build del CLI (L-017).
- **Pendiente:** Todo el diseño e implementación. Depende de T-024.

### T-026 — `Prototipador` como subagente + bucle P3↔P4

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Paso 6 del nuevo orden de construcción. Subagente que materializa el prototipo guiado por `discovery.md` (T-025): wireframes/HTML o spike/PoC según lo que el descubrimiento pida, iterando en el bucle P3↔P4 de `methodology.md` §4 con feedback humano en vivo.
- **Pendiente:** Todo el diseño e implementación. Depende de T-025.

### T-027 — Gate de madurez / feature freeze: cierre del estadio de prototipo

- **Estado:** No implementada
- **Fecha:** 2026-07-23
- **Descripción:** Paso 7 del nuevo orden de construcción. Cierra el estadio de prototipado (`methodology.md` §4.4) y marca la transición a la maquinaria del incremento de 11 pasos (MVP en adelante), donde entran en juego `state.yaml` (T-014), `soda status` (T-015) y `soda step` (T-016).
- **Pendiente:** Todo el diseño e implementación. Depende de T-026. Último paso del nuevo orden de construcción definido en esta sesión.
