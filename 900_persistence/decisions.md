# Decisions

## Índice

| Código | Título | Fecha |
|--------|--------|-------|
| [D-001](#d-001--nombre-del-paquete-y-producto-soda) | Nombre del paquete y producto: `soda` | 2026-07-23 |
| [D-002](#d-002--cli-unica-con-subcomandos-en-vez-de-comandos-separados) | CLI única con subcomandos en vez de comandos separados | 2026-07-23 |
| [D-003](#d-003--modelo-de-distribución-instalación-única-vía-pipx) | Modelo de distribución: instalación única vía `pipx` | 2026-07-23 |
| [D-004](#d-004--layout-src-en-vez-de-flat-layout) | Layout `src/` en vez de flat layout | 2026-07-23 |
| [D-005](#d-005--build-backend-hatchling-python-312-y-dependencias-mínimas) | Build backend hatchling, Python 3.12 y dependencias mínimas | 2026-07-23 |
| [D-006](#d-006--implementaciones-concretas-de-provider-en-srcsodaproviders-no-en-core) | Implementaciones concretas de `Provider` en `src/soda/providers/`, no en `core/` | 2026-07-23 |
| [D-007](#d-007--el-prompt-se-entrega-al-cli-por-stdin-no-como-argumento) | El prompt se entrega al CLI por stdin, no como argumento | 2026-07-23 |
| [D-008](#d-008--interfaz-de-provider-deliberadamente-mínima) | Interfaz de `Provider` deliberadamente mínima | 2026-07-23 |
| [D-009](#d-009--las-plantillas-se-acceden-con-importlibresources-no-con-pathfile__parent) | Las plantillas se acceden con `importlib.resources`, no con `Path(__file__).parent` | 2026-07-23 |
| [D-010](#d-010--soda-init-acepta-project_root-como-argumento-opcional-en-la-cli) | `soda init` acepta `project_root` como argumento opcional en la CLI | 2026-07-23 |
| [D-011](#d-011--init-es-no-destructivo-por-defecto-con-relleno-parcial-y---force-para-sobrescribir) | `init` es no destructivo por defecto, con relleno parcial, y `--force` para sobrescribir | 2026-07-23 |
| [D-012](#d-012--init-solo-siembra-los-seis-archivos-de-memoria-no-crea-claudemd-ni-toca-gitignore) | `init` solo siembra los seis archivos de memoria; no crea `CLAUDE.md` ni toca `.gitignore` | 2026-07-23 |
| [D-013](#d-013--init-crea-_persistence-pero-exige-que-project_root-ya-exista) | `init` crea `_persistence/` pero exige que `project_root` ya exista | 2026-07-23 |
| [D-014](#d-014--principlesmd-y-methodologymd-son-producto-no-andamiaje-mudados-a-srcsodatemplates_guideline) | `principles.md` y `methodology.md` son producto, no andamiaje; mudados a `src/soda/templates/_guideline/` | 2026-07-23 |
| [D-015](#d-015--los-códigos-de-principlesmd-son-identificadores-permanentes-de-3-dígitos) | Los códigos de `principles.md` son identificadores permanentes de 3 dígitos | 2026-07-23 |
| [D-016](#d-016--los-predicados-de-conformidad-se-escriben-solo-contra-evidencia-disponible-hoy) | Los predicados de conformidad se escriben solo contra evidencia disponible hoy | 2026-07-23 |
| [D-017](#d-017--el-harness-trabaja-exclusivamente-proyectos-de-desarrollo-de-software) | El harness trabaja exclusivamente proyectos de desarrollo de software | 2026-07-23 |
| [D-018](#d-018--tres-estados-de-aplicación-normativo-diferido-y-pendiente-no-dos) | Tres estados de aplicación (normativo, `[DIFERIDO]` y `[PENDIENTE]`), no dos | 2026-07-23 |
| [D-019](#d-019--dividir-methodologymd-sin-renumerar-secciones) | Dividir `methodology.md` sin renumerar secciones | 2026-07-23 |
| [D-020](#d-020--enmienda-a-d-012-init-también-siembra-_guideline) | Enmienda a D-012: `init` también siembra `_guideline/` | 2026-07-23 |
| [D-021](#d-021--_persistence-y-_guideline-se-siembran-igual-pero-se-reportan-distinto) | `_persistence/` y `_guideline/` se siembran igual pero se reportan distinto | 2026-07-23 |
| [D-022](#d-022--agent-worker-no-se-construye-en-su-lugar-agentes-especializados) | `agent-worker` no se construye; en su lugar, agentes especializados | 2026-07-23 |
| [D-023](#d-023--agents-and-evaluationmd-5-pasa-de-descripción-a-hoja-de-ruta) | `agents-and-evaluation.md` §5 pasa de descripción a hoja de ruta | 2026-07-23 |
| [D-024](#d-024--el-orquestador-es-el-script-de-python-no-una-sesión-de-claude-code-o-codex) | El orquestador es el script de Python, no una sesión de Claude Code o Codex | 2026-07-23 |
| [D-025](#d-025--posponer-el-orquestador-llm-se-resuelve-cuando-duela) | Posponer el orquestador LLM: se resuelve cuando duela | 2026-07-23 |
| [D-026](#d-026--diseño-de-la-interfaz-de-comandos-init-start-step-status-close) | Diseño de la interfaz de comandos: `init` / `start` / `step` / `status` / `close` | 2026-07-23 |
| [D-027](#d-027--stateyaml-deja-de-ser-opcional-es-prerrequisito-de-soda-step-y-soda-status) | `state.yaml` deja de ser opcional: es prerrequisito de `soda step` y `soda status` | 2026-07-23 |
| [D-028](#d-028--orden-de-construcción-soda-start-sesion-starter-stateyaml-status-step-close) | Orden de construcción: `soda start` → `sesion-starter` → `state.yaml` → `status` → `step` → `close` | 2026-07-23 |
| [D-029](#d-029--los-agentes-del-harness-corren-sin-herramientas-python-les-inyecta-el-contexto) | Los agentes del harness corren sin herramientas; Python les inyecta el contexto | 2026-07-23 |
| [D-030](#d-030--el-modelo-es-argumento-del-constructor-del-provider-no-de-send) | El modelo es argumento del constructor del `Provider`, no de `send` | 2026-07-23 |
| [D-031](#d-031--la-suscripción-se-garantiza-borrando-las-variables-de-entorno-de-api-no-confiando-en-que-no-estén) | La suscripción se garantiza borrando las variables de entorno de API, no confiando en que no estén | 2026-07-23 |
| [D-032](#d-032--los-archivos-de-memoria-bajo-demanda-viajan-solo-con-su-índice) | Los archivos de memoria bajo demanda viajan solo con su índice | 2026-07-23 |
| [D-033](#d-033--modelos-es-un-diccionario-en-código-no-un-archivo-de-configuración) | `MODELOS` es un diccionario en código, no un archivo de configuración | 2026-07-23 |
| [D-034](#d-034--se-adelanta-el-cableado-de-soda-start-con-sesion-starter) | Se adelanta el cableado de `soda start` con `sesion-starter` | 2026-07-23 |
| [D-035](#d-035--pivote-soda-repl-persistente-con-delegación-a-subagentes-sobre-suscripción-no-orquestador-script--subprocesos-sin-estado) | Pivote: `soda` REPL persistente con delegación a subagentes sobre suscripción, no orquestador-script + subprocesos sin estado | 2026-07-23 |
| [D-036](#d-036--el-bucle-interior-del-orquestador-usa-tool_use-estructurado-del-claude-agent-sdk-no-la-convención-de-marcador-llamar) | El bucle interior del orquestador usa `tool_use` estructurado del Claude Agent SDK, no la convención de marcador `[[LLAMAR:...]]` | 2026-07-23 |
| [D-037](#d-037--la-espina-de-control-de-soda-es-híbrida-python-determinista--sesión-llm-persistente-para-el-juicio) | La espina de control de `soda` es híbrida: Python determinista + sesión LLM persistente para el juicio | 2026-07-23 |

## Detalle de decisiones

### D-001 — Nombre del paquete y producto: `soda`

- **Fecha:** 2026-07-23
- **Contexto:** El repo se llama Harness_TripleS, pero se necesitaba un nombre de paquete Python importable y un nombre de producto.
- **Decisión:** El paquete importable y el producto se llaman `soda` ("Software Development Agentic"). El repositorio conserva el nombre Harness_TripleS.
- **Alternativas descartadas:** Usar directamente `harness_triples` o similar como nombre de paquete (descartado por ser menos memorable como nombre de producto).
- **Consecuencias:** Todo el código vive bajo `src/soda/`; la documentación y la memoria de construcción siguen usando "Harness_TripleS" para referirse al repo.

### D-002 — CLI única con subcomandos en vez de comandos separados

- **Fecha:** 2026-07-23
- **Contexto:** Definir cómo se expondrá la herramienta al usuario final en la línea de comandos.
- **Decisión:** Un solo comando `soda` con subcomandos (`soda init`, `soda start`, `soda close`), no comandos independientes tipo `soda-init`.
- **Alternativas descartadas:** Comandos separados por acción (`soda-init`, `soda-start`, etc.), descartados por multiplicar entradas en PATH y fragmentar la ayuda.
- **Consecuencias:** Una sola entrada en PATH, ayuda unificada (`soda --help`), y añadir subcomandos nuevos no requiere reinstalar el paquete.

### D-003 — Modelo de distribución: instalación única vía `pipx`

- **Fecha:** 2026-07-23
- **Contexto:** Decidir si `soda` se instala como dependencia de cada proyecto destino o como herramienta de desarrollo global.
- **Decisión:** `soda` es una herramienta de desarrollo, no una librería que la app importe. Se instala una sola vez a nivel de máquina con `pipx install -e <ruta del repo>` y se invoca desde la carpeta de cada proyecto destino.
- **Alternativas descartadas:** Instalar `soda` en el venv de cada proyecto destino, descartado porque mezclaría dependencias del harness con las de la app y obligaría a reinstalar por proyecto.
- **Consecuencias:** El código de `soda` nunca debe asumir que corre dentro del venv del proyecto destino; debe operar sobre un `project_root` explícito.

### D-004 — Layout `src/` en vez de flat layout

- **Fecha:** 2026-07-23
- **Contexto:** Elegir la disposición de carpetas del paquete Python.
- **Decisión:** Usar layout `src/` (`src/soda/...`) en vez de flat layout.
- **Alternativas descartadas:** Flat layout (paquete en la raíz del repo), descartado porque permite que los tests importen accidentalmente el código sin pasar por la instalación, ocultando errores de empaquetado.
- **Consecuencias:** Los tests importan siempre el paquete instalado (`pip install -e`), detectando errores de empaquetado desde el inicio.

### D-005 — Build backend hatchling, Python 3.12 y dependencias mínimas

- **Fecha:** 2026-07-23
- **Contexto:** Configurar `pyproject.toml` del paquete `soda`.
- **Decisión:** Build backend `hatchling`, Python objetivo `>=3.12` (entorno local verificado en 3.12.10), sin dependencias de runtime; `pytest` y `ruff` como extra opcional `[dev]`.
- **Alternativas descartadas:** No se evaluaron otros build backends en esta sesión; se eligió hatchling directamente por simplicidad.
- **Consecuencias:** Instalar el paquete en producción no arrastra dependencias externas; el extra `[dev]` es necesario para testear y lintear.

### D-006 — Implementaciones concretas de `Provider` en `src/soda/providers/`, no en `core/`

- **Fecha:** 2026-07-23
- **Contexto:** Al crear `ClaudeCLIProvider`, decidir dónde vive el código de cada proveedor concreto respecto a la abstracción `Provider`.
- **Decisión:** `core/` guarda solo abstracciones compartidas (coherente con su docstring); las implementaciones concretas viven en `src/soda/providers/` (`ClaudeCLIProvider` en `providers/claude_cli.py`).
- **Alternativas descartadas:** Meter `ClaudeCLIProvider` directamente en `core/`, descartado porque mezclaría la abstracción con una implementación concreta y dificultaría añadir proveedores nuevos.
- **Consecuencias:** Añadir un proveedor nuevo (p. ej. `CodexCLIProvider`) es añadir un módulo en `providers/` sin tocar `core/` ni nada más.

### D-007 — El prompt se entrega al CLI por stdin, no como argumento

- **Fecha:** 2026-07-23
- **Contexto:** Definir cómo `ClaudeCLIProvider` pasa el prompt al ejecutable `claude`.
- **Decisión:** El prompt se entrega por stdin (`subprocess.run(..., input=prompt)`), nunca como argumento de línea de comandos.
- **Alternativas descartadas:** Pasar el prompt como argumento posicional del CLI, descartado por el límite de ~8191 caracteres de la línea de comandos de Windows, que los prompts del arnés (system prompt + contexto de `_persistence`) superarán con facilidad.
- **Consecuencias:** Validado en real con un prompt de 13.109 caracteres devuelto correctamente. Cualquier proveedor nuevo basado en CLI debe seguir el mismo patrón de entrada por stdin.

### D-008 — Interfaz de `Provider` deliberadamente mínima

- **Fecha:** 2026-07-23
- **Contexto:** Diseñar la superficie de la clase abstracta `Provider`.
- **Decisión:** Un solo método abstracto, `send(prompt: str) -> str`.
- **Alternativas descartadas:** Añadir de entrada parámetros para modelo configurable, system prompt, streaming, y modo API/key para producción (mencionado en `idea.md:38-40`); descartados hasta que exista un caso de uso real que los pida.
- **Consecuencias:** La interfaz crecerá solo cuando haya necesidad concreta; cualquier extensión futura debe justificarse con un caso de uso real, no anticiparse.

### D-009 — Las plantillas se acceden con `importlib.resources`, no con `Path(__file__).parent`

- **Fecha:** 2026-07-23
- **Contexto:** Diseñar cómo `soda` lee los archivos de `src/soda/templates/_persistence/` en tiempo de ejecución (T-004).
- **Decisión:** El acceso pasa siempre por `importlib.resources.files()` (`persistence_root()` en `src/soda/templates/__init__.py`), nunca por una ruta relativa al árbol de fuentes.
- **Alternativas descartadas:** Resolver la ruta con `Path(__file__).parent`, descartado porque el paquete puede quedar instalado comprimido (zip import) o en una ruta que no corresponde al árbol de fuentes; `files()` funciona en ambos casos.
- **Consecuencias:** El accesor de `src/soda/templates/__init__.py` es la única vía legítima para leer plantillas. Verificado instalando el wheel en un venv limpio fuera del árbol de fuentes.

### D-010 — `soda init` acepta `project_root` como argumento opcional en la CLI

- **Fecha:** 2026-07-23
- **Contexto:** Definir la ergonomía de `soda init`: si `project_root` debe ser obligatorio o puede asumir el directorio actual por defecto, sin violar C-002.
- **Decisión:** En la CLI, `project_root` es opcional y usa el directorio actual por defecto. La función interna `init_persistence()` sigue exigiendo `project_root` explícito siempre; el valor por defecto se resuelve a ruta absoluta en `main()` antes de llamar a nada.
- **Alternativas descartadas:** Exigir `project_root` obligatorio en la CLI (p. ej. `soda init .`), descartado por ergonomía a petición del usuario.
- **Consecuencias:** La comodidad vive solo en la interfaz; el código interno cumple C-002 al pie de la letra. Cubierto por el test `test_siembra_dentro_de_project_root_y_no_en_el_directorio_actual` (chdir a otra carpeta, comprueba que la siembra va donde dice el argumento). La CLI imprime siempre la ruta absoluta resuelta.

### D-011 — `init` es no destructivo por defecto, con relleno parcial, y `--force` para sobrescribir

- **Fecha:** 2026-07-23
- **Contexto:** Decidir el comportamiento de `soda init` cuando `_persistence/` ya existe total o parcialmente en el destino.
- **Decisión:** Por defecto, `init` nunca sobrescribe un archivo existente; completa solo lo que falta (relleno parcial, idempotente). `--force` sobrescribe, nombrando cada archivo reemplazado.
- **Alternativas descartadas:** Fallar en seco si `_persistence/` ya existe, descartado porque el relleno parcial es idempotente y permite que un séptimo archivo de memoria futuro se complete en proyectos existentes sin tocar el resto.
- **Consecuencias:** Ningún archivo con contenido se pierde sin `--force` escrito a mano, y ni siquiera entonces en silencio (se reporta qué se sobrescribió).

### D-012 — `init` solo siembra los seis archivos de memoria; no crea `CLAUDE.md` ni toca `.gitignore`

- **Fecha:** 2026-07-23
- **Contexto:** Definir el alcance exacto de lo que `soda init` toca en el proyecto destino.
- **Decisión:** `init` siembra únicamente los seis archivos de memoria en `_persistence/`; no crea `CLAUDE.md` en el destino ni modifica `.gitignore`.
- **Alternativas descartadas:** Añadir `_persistence/` al `.gitignore` del destino, descartado como activamente incorrecto: E1 de `905_guideline/principles.md` establece Git como registro de estado entre sesiones, así que `_persistence/` debe versionarse, no ignorarse.
- **Consecuencias:** `_persistence/` queda siempre trackeable por Git en el proyecto destino; cualquier necesidad futura de generar `CLAUDE.md` en destino sería una tarea separada. **Enmendada en D-020** (2026-07-23): `init` pasó a sembrar también `_guideline/`; la parte de esta decisión sobre no crear `CLAUDE.md` ni tocar `.gitignore` sigue vigente sin cambios.

### D-013 — `init` crea `_persistence/` pero exige que `project_root` ya exista

- **Fecha:** 2026-07-23
- **Contexto:** Decidir qué hace `init` si el `project_root` recibido no existe en disco.
- **Decisión:** `init` crea `_persistence/` si falta, pero falla con `NotADirectoryError` si `project_root` no existe o no es un directorio.
- **Alternativas descartadas:** Crear también `project_root` si no existe, descartado porque sembrar memoria dentro de un proyecto es el trabajo de `init`, pero crear un árbol de directorios completo a partir de una ruta mal tecleada es cómo se termina sembrando memoria en un destino equivocado.
- **Consecuencias:** Un typo en `project_root` falla ruidosamente (exit 1, mensaje accionable) en vez de crear silenciosamente una carpeta nueva no intencionada.

### D-014 — `principles.md` y `methodology.md` son producto, no andamiaje; mudados a `src/soda/templates/_guideline/`

- **Fecha:** 2026-07-23
- **Contexto:** `principles.md` y `methodology.md` vivían en `905_guideline/` en la raíz del repo. El usuario confirmó explícitamente que ambos documentos viajan con `soda` al proyecto destino (se instalan como `_guideline/`), no son andamiaje de construcción de este repo.
- **Decisión:** Mudar ambos archivos con `git mv` a `src/soda/templates/_guideline/`, junto al resto de plantillas del paquete (`_persistence/`).
- **Alternativas descartadas:** Dejarlos en la raíz como andamiaje, descartado porque contradice su naturaleza real de producto y no encaja con C-003 (frontera producto/andamiaje).
- **Consecuencias:** No hizo falta tocar `pyproject.toml` (`packages = ["src/soda"]` ya arrastra los `.md`). Verificado con wheel instalado en venv limpio. Deja abierta T-009 (sembrar `_guideline/` en el destino), que hoy nadie ejecuta.

### D-015 — Los códigos de `principles.md` son identificadores permanentes de 3 dígitos

- **Fecha:** 2026-07-23
- **Contexto:** Al reorganizar `principles.md` por audiencia (T-007), había que decidir si los códigos (`P-`, `E-`, `NC-`) se renumeran según su nueva posición en el documento o se conservan.
- **Decisión:** Los códigos son identificadores permanentes que no cambian aunque el ítem cambie de sección, misma convención que `T-`/`L-`/`D-` de `900_persistence`. Se pasó la numeración a 3 dígitos.
- **Alternativas descartadas:** Renumerar según la nueva ubicación por audiencia, descartado porque habría invalidado las 44 referencias cruzadas ya existentes en `methodology.md`.
- **Consecuencias:** Permitió reorganizar el documento por audiencia sin invalidar ninguna de las 44 referencias de `methodology.md`; solo hubo que rellenar ceros y remapear las 3 referencias a NC-6 (retirada) hacia NC-001.

### D-016 — Los predicados de conformidad se escriben solo contra evidencia disponible hoy

- **Fecha:** 2026-07-23
- **Contexto:** Al reescribir NC-005 y otras reglas verificables de `principles.md`, surgió la tentación de describir predicados que requieren infraestructura que no existe (motor de traza, umbral de ventana de contexto cuantificado, cuota medida).
- **Decisión:** Los predicados de conformidad se escriben solo contra evidencia disponible hoy (artefactos en disco + git log); lo que requiere infraestructura futura se declara como pendiente con gatillo explícito (§5 de `principles.md`), no se escribe como si ya aplicara.
- **Alternativas descartadas:** Escribir predicados aspiracionales asumiendo infraestructura futura, descartado porque produce reglas que ningún agente puede cumplir verificablemente hoy — el mismo defecto que `methodology.md` confiesa en su §10.2 (perfiles de conformidad vivos en prompts sin que nadie los ejecutara).
- **Consecuencias:** `principles.md` §5 lista explícitamente los pendientes declarados (motor de traza, umbral de ventana de contexto, cuota cuantificada); `methodology.md` no aplica todavía esta disciplina de forma consistente (queda como parte de T-010).

### D-017 — El harness trabaja exclusivamente proyectos de desarrollo de software

- **Fecha:** 2026-07-23
- **Contexto:** `methodology.md` declaraba cubrir dos familias de proyecto (desarrollo de software y Ciencia de datos/ML), con una tabla comparativa y adaptaciones específicas para ML en varios puntos del documento (umbrales de métrica, notebooks, evaluación).
- **Decisión:** El usuario acotó explícitamente el alcance del harness a proyectos de desarrollo de software exclusivamente; ningún soporte especial para Ciencia de datos/ML. El documento sigue siendo agnóstico de lenguaje/stack/framework, pero no de dominio.
- **Alternativas descartadas:** Mantener las dos familias de proyecto como se tenía, descartado por decisión explícita del usuario de acotar el alcance del producto.
- **Consecuencias:** T-010 paso 1 recortó `methodology.md` (cabecera, §2, ~10 puntos, §8) eliminando referencias a ML/notebook/umbral de métrica, preservando con cuidado la distinción entre "producto ML" (se fue) y "agente LLM probabilístico" (se quedó, tesis central del harness). Cualquier trabajo futuro de soporte a ML quedaría fuera de alcance salvo decisión nueva que revierta esta.

### D-018 — Tres estados de aplicación (normativo, `[DIFERIDO]` y `[PENDIENTE]`), no dos

- **Fecha:** 2026-07-23
- **Contexto:** Al marcar `methodology.md`/`agents-and-evaluation.md` con qué rige hoy y qué no (T-010 paso 2), el pedido inicial era distinguir solo dos estados (normativo vs. diferido). El inventario del repo mostró que "diferido" tapaba dos situaciones distintas que se revierten de forma distinta.
- **Decisión:** Se usan tres estados: *(sin marca)* = normativo, rige desde la primera sesión sin infraestructura previa; `[DIFERIDO]` = decidido no adoptar aún, lleva gatillo de adopción, se revierte con evidencia (ver D-016); `[PENDIENTE]` = se quiere pero falta una pieza nombrada, se revierte entregando esa pieza.
- **Alternativas descartadas:** Dos estados (normativo/diferido) tal como se pidió inicialmente, descartado porque mezclaba "decidido no adoptar" con "falta construir la pieza", que requieren reversión y evidencia de tipos distintos.
- **Consecuencias:** Nueva §0.3 en `agents-and-evaluation.md` con el núcleo normativo y una tabla de 8 piezas ausentes ("qué se hace sin ella"); 9 marcas `[DIFERIDO]` y 14 `[PENDIENTE]` colocadas. Detectada tarea nueva T-011: `principles.md` §5 usa un vocabulario distinto ("Gatillo de adopción" para ítems que en realidad son `[PENDIENTE]`) y queda sin unificar con esta taxonomía.

### D-019 — Dividir `methodology.md` sin renumerar secciones

- **Fecha:** 2026-07-23
- **Contexto:** El gatillo de división propio de `methodology.md` ya estaba disparado (418 líneas contra un umbral de ~250 para el bloque §5+§8+§9+§10+§3.1), forzando a partir el documento en dos archivos (T-010 paso 3).
- **Decisión:** Dividir en `methodology.md` (§0-§4, §6, §7, Apéndice) y `agents-and-evaluation.md` (§3.1, §5, §8, §9, §10) sin renumerar ninguna sección; los números quedan únicos globalmente entre ambos archivos, así que "§8" significa lo mismo se lea donde se lea.
- **Alternativas descartadas:** Renumerar las secciones movidas para que cada archivo tuviera numeración correlativa propia, descartado porque habría obligado a reescribir referencias cruzadas en ambos documentos y en `principles.md` sin ninguna ganancia real (mismo problema que evitó D-015 con los códigos de `principles.md`).
- **Consecuencias:** Cero referencias cruzadas rotas (verificado por script: 28 secciones definidas, 0 referencias `§N` rotas). Cada archivo lleva en cabecera un mapa de qué § vive dónde. `principles.md` (que citaba `methodology.md §10.2`, mudada a `agents-and-evaluation.md`) tuvo que corregirse igual, porque la mudanza de sección entre archivos sí cambia cuál documento hay que citar, aunque el número de sección no cambie.

### D-020 — Enmienda a D-012: `init` también siembra `_guideline/`

- **Fecha:** 2026-07-23
- **Contexto:** T-009 quedó bloqueada porque, tal como estaba planteada, contradecía D-012 (`init` solo siembra los seis archivos de memoria). Había tres opciones sobre la mesa: ampliar D-012, un subcomando `soda guideline` aparte, o un flag `--with-guideline`. El usuario decidió explícitamente ampliar D-012.
- **Decisión:** `soda init` siembra en una sola pasada tanto `_persistence/` (memoria, D-012 original) como `_guideline/` (doctrina, T-008/T-009), reportando cada carpeta en su propio bloque de salida.
- **Alternativas descartadas:** Subcomando `soda guideline` separado, descartado por fragmentar un flujo que el usuario quiere de un solo paso; flag `--with-guideline` opt-in, descartado porque dejaría la doctrina fuera por defecto, contrario al objetivo de que ningún proyecto destino se quede sin ella al iniciar.
- **Consecuencias:** `init_guideline()` (nueva, `src/soda/cli.py`) y `_sembrar()` (helper común factorizado de `init_persistence()`) implementan la siembra. La parte de D-012 sobre no crear `CLAUDE.md` ni tocar `.gitignore` sigue vigente sin cambios. Ver D-021 para cómo se reporta cada carpeta.

### D-021 — `_persistence/` y `_guideline/` se siembran igual pero se reportan distinto

- **Fecha:** 2026-07-23
- **Contexto:** Al implementar D-020, surgió la pregunta de si un archivo existente en destino que no coincide con la plantilla del paquete debía tratarse igual en `_persistence/` que en `_guideline/`. No son la misma clase de archivo: la memoria es del proyecto destino (que diverja de la plantilla es lo esperado) y la doctrina la posee la versión instalada de `soda` (que diverja es una señal de desfase).
- **Decisión:** Ambas carpetas se siembran con la misma regla no destructiva de D-011 (nunca se toca un archivo existente sin `--force`), pero se reportan distinto: en `_persistence/`, un archivo existente siempre se salta como `SALTADO`, sin compararlo; en `_guideline/`, un archivo existente que no coincide byte a byte con el del paquete se reporta con la constante nueva `DIFIERE` ("difiere, saltado") en vez de `SALTADO`, avisando del desfase y sugiriendo `--force`.
- **Alternativas descartadas:** Reportar ambas carpetas igual (todo `SALTADO`), descartado porque un destino que instaló una versión vieja de `soda` se quedaría con una `methodology.md` desactualizada para siempre y en silencio, sin ninguna señal de que existe una versión más nueva.
- **Consecuencias:** Ninguna de las dos carpetas se toca sin `--force` (D-011 sigue rigiendo intacto); lo único que cambia es que el desfase deja de ser silencioso. Cubierto por un test explícito de que la memoria nunca se marca `DIFIERE` (T-009).

### D-022 — `agent-worker` no se construye; en su lugar, agentes especializados

- **Fecha:** 2026-07-23
- **Contexto:** `idea.md` menciona tres agentes de ejemplo: `sesion-starter`, `agent-worker`, `sesion-closer`. El usuario aclaró explícitamente que esa lista es de ejemplo, no un catálogo cerrado a implementar tal cual.
- **Decisión:** `sesion-starter` y `sesion-closer` sí se implementan como agentes reales del harness. `agent-worker` NO se va a crear: era un placeholder genérico de "el que hace el trabajo". En su lugar se construyen agentes especializados (revisor de código, probador, implementador, refactorizador, etc.).
- **Alternativas descartadas:** Implementar `agent-worker` como agente genérico único que absorbe todo el trabajo de construcción, descartado explícitamente por el usuario a favor de agentes con oficio acotado.
- **Consecuencias:** Los arquetipos con nombre ya listados en `agents-and-evaluation.md` §5 (Probador, Implementador, Refactorizador, Revisor de código, Verificador, Especificador, Definidor, Planificador, Integrador de pruebas, Descubridor, Prototipador) son los agentes especializados que hay que construir. Ver D-023.

### D-023 — `agents-and-evaluation.md` §5 pasa de descripción a hoja de ruta

- **Fecha:** 2026-07-23
- **Contexto:** Quedaba abierta desde T-010/T-011 la pregunta de si `agents-and-evaluation.md` §5 (los ~12 arquetipos de agente) describe el destino del harness o especifica ya lo que se va a construir.
- **Decisión:** §5 especifica lo que se va a construir, no solo lo describe. Queda formalmente como hoja de ruta de los agentes especializados del harness (ver D-022).
- **Alternativas descartadas:** Dejar §5 como descripción aspiracional sin compromiso de construcción, descartado porque el usuario confirmó que esos arquetipos son exactamente los agentes especializados que reemplazan a `agent-worker`.
- **Consecuencias:** Resuelve la precondición de diseño que tenía T-012 pendiente. El orden de construcción (D-028) usa estos arquetipos como catálogo de referencia para `soda step` (T-016).

### D-024 — El orquestador es el script de Python, no una sesión de Claude Code o Codex

- **Fecha:** 2026-07-23
- **Contexto:** Se asumía que `soda` corría dentro de un harness de Claude Code o Codex, y que la frase de la doctrina "el orquestador es la sesión principal" (`principles.md` §2, `agents-and-evaluation.md` §5) aplicaba tal cual. El usuario corrigió: `soda` es un script de Python que se ejecuta en una terminal (`python main.py` / `soda <comando>`); no hay sesión principal de Claude Code, hay un proceso de Python.
- **Decisión:** El orquestador es el script de `soda`. Quién invoca a los agentes siempre es Python: en el instante en que arranca el script, lo único vivo es Python, ningún LLM existe todavía y un agente no puede autoinvocarse desde la nada.
- **Alternativas descartadas:** Ninguna real; se aclara que "quién invoca" no era una pregunta de diseño con alternativas, sino un supuesto equivocado que corregir. La pregunta de diseño genuina era otra: quién decide a quién invocar (ver D-025).
- **Consecuencias:** Corrige la lectura de `principles.md` §2 y `agents-and-evaluation.md` §5 para este proyecto: "sesión principal" se traduce como "el script `soda`". Ver también L-010.

### D-025 — Posponer el orquestador LLM: se resuelve cuando duela

- **Fecha:** 2026-07-23
- **Contexto:** Separadas dos preguntas antes confundidas: (a) quién invoca a los agentes (siempre Python, D-024, sin alternativa) y (b) quién decide a quién invocar. El camino feliz de un incremento ya tiene su secuencia escrita en `methodology.md` §3 (11 pasos con gates) y criterios de avance mecánicos (`pytest` rojo/verde, NC-005, §3.1). El juicio real de coordinación solo aparece en tres sitios: qué slice va primero (ya es "Humano + sesión principal" en §3), conducir la entrevista de descubrimiento (es hacer el trabajo, no orquestar) y qué hacer cuando algo falla (Verificador NO CONFORME, reinvocación con consigna corregida de E-014).
- **Decisión:** El orquestador LLM se pospone. Solo se justifica en el camino infeliz (fallos); mientras no exista, el fallo escala al humano, que es lo que E-014 manda de todos modos.
- **Alternativas descartadas:** Construir un orquestador LLM que decida a qué agente invocar en cada paso del camino feliz, descartado porque gastaría cuota releyendo una tabla ya escrita en el documento (§3), sin aportar juicio real.
- **Consecuencias:** `soda step` (T-016) resuelve el camino feliz de forma mecánica contra `state.yaml` (T-014) y §3, sin invocar un LLM coordinador. El diseño de un orquestador LLM para el camino infeliz queda diferido hasta que el escalado manual al humano resulte doloroso en la práctica.

### D-026 — Diseño de la interfaz de comandos: `init` / `start` / `step` / `status` / `close`

- **Fecha:** 2026-07-23
- **Contexto:** El usuario propuso partir el trabajo del harness en comandos ejecutados desde la terminal del proyecto destino. Hallazgo de fondo: al partir el trabajo en comandos, los gates humanos salen gratis (el humano es el bucle; entre un comando y el siguiente revisa lo producido, que es lo que piden los gates de §3 pasos 5, 7 y 11); además cada comando es una unidad acotada de cuota (E-014).
- **Decisión:** Cinco comandos. `soda init` (ya existe: siembra `_persistence/` y `_guideline/`). `soda start` (dos ramas: bootstrap Git en Python puro si el proyecto está vacío, o invocar a `sesion-starter` si ya hay memoria escrita). `soda step` (nombre preferido sobre `soda continue`: hace UN paso y devuelve el control, no corre hasta terminar). `soda status` (verbo nuevo, solo lectura, cero cuota: "¿dónde estoy y qué haría el próximo `step`?"). `soda close` (invoca a `sesion-closer`; el commit y el push los hace Python).
- **Alternativas descartadas:** `soda continue` en vez de `soda step`, descartado porque "continue" sugiere avanzar hasta el final en vez de un paso acotado con gate. Omitir `soda status`, descartado porque faltaba un comando de solo lectura y sin riesgo para verificar la detección de estado antes de que `soda step` dependiera de ella.
- **Consecuencias:** Fija el orden de construcción (D-028) y el prerrequisito de `state.yaml` (D-027). El bootstrap de proyecto vacío dentro de `soda start` es 100% Python sin agentes (ver justificación en D-028/T-013): es determinista, requiere hablar con el humano para pedir la URL de GitHub (imposible para un `claude -p`, ver C-007) y toca Git, la única operación con consecuencia PARADA (NC-007).

### D-027 — `state.yaml` deja de ser opcional: es prerrequisito de `soda step` y `soda status`

- **Fecha:** 2026-07-23
- **Contexto:** Detectar en qué punto está un incremento parece fácil en principio (¿hay spec?, ¿aprobada?, ¿hay plan?, ¿tests en rojo o verde?) combinando el disco con la tabla de §3. Pero hoy no hay dónde leerlo de forma fiable: `methodology.md` §0.3 lista `_increments/<id>/state.yaml` como pieza `[PENDIENTE]`, y su sustituto declarado es que el estado se lleva en `_persistence/tasks.md` en narrativa, que no se parsea de forma determinista.
- **Decisión:** `soda step` es el comando que obliga a construir `state.yaml`; no es un rodeo, es su prerrequisito.
- **Alternativas descartadas:** Que un LLM lea la narrativa de `tasks.md` y deduzca el punto del incremento, descartado porque pagaría cuota en cada invocación para reconstruir algo que un archivo pequeño diría gratis y sin error.
- **Consecuencias:** T-014 (`state.yaml`) queda como paso 3 del orden de construcción, antes de `soda status` (T-015) y `soda step` (T-016), que dependen de él.

### D-028 — Orden de construcción: `soda start` → `sesion-starter` → `state.yaml` → `status` → `step` → `close`

- **Fecha:** 2026-07-23
- **Contexto:** Se había propuesto un orden que dejaba a `sesion-starter` al final; al preguntarse dónde entraba, se corrigió. Trace del primer run: en un proyecto vacío, `sesion-starter` no tiene trabajo (su oficio es reconstruir contexto de sesiones anteriores y no hay ninguna; Python detecta "memoria vacía" leyendo el disco sin LLM). El primer agente que se invoca en la vida de un proyecto es el Descubridor, no el starter; el starter sirve del segundo run en adelante.
- **Decisión:** Orden final: (1) `soda start`, rama de proyecto vacío — bootstrap Git puro en Python, sin agentes (T-013, próximo paso de la siguiente sesión); (2) `sesion-starter`, rama de proyecto con memoria — primer agente del harness (T-012); (3) `state.yaml`, formato mínimo del estado del incremento (T-014); (4) `soda status`, lee el estado, cero cuota (T-015); (5) `soda step`, los agentes especializados (T-016); (6) `soda close`, `sesion-closer` (T-017).
- **Alternativas descartadas:** Construir primero `sesion-closer` con el argumento de que "el starter lee lo que el closer escribe" (dependencia lógica), descartado como criterio de orden de *construcción* porque la memoria de este mismo repo (`900_persistence/`) ya existe y está llena de seis sesiones de contenido auténtico: no hace falta construir el closer antes para tener con qué probar el starter. Razón positiva de que `sesion-starter` vaya segundo y no al final: es el único agente que no puede romper nada (solo lectura, el peor caso es un resumen equivocado en pantalla), ya tiene banco de pruebas real y su prompt ya está escrito y probado (skill `session-startup`, ejercitada seis veces).
- **Consecuencias:** Fija el punto de entrada de la próxima sesión (T-013). Cada comando se termina como unidad antes de pasar al siguiente.

### D-029 — Los agentes del harness corren sin herramientas; Python les inyecta el contexto

- **Fecha:** 2026-07-23
- **Contexto:** Al construir `sesion-starter` (T-012), había que decidir si el agente recibe herramientas de lectura (`Read`/`Glob`) para navegar `_persistence/` por su cuenta, o si Python le entrega ya compuesto todo lo que necesita.
- **Decisión:** `ClaudeCLIProvider` invoca siempre con `--tools ""` por defecto (parámetro `tools: Sequence[str] | None = ()`); el agente recibe el contexto ya armado en el prompt.
- **Alternativas descartadas:** Darle `Read`+`Glob` y dejar que el agente navegue la memoria, descartado por tres razones: `Read`/`Glob` son herramientas de Claude Code y atarían el prompt a un CLI concreto (rompiendo la portabilidad entre proveedores); se gastaría cuota en descubrir rutas que el script ya conoce por convención; y aparecerían diálogos de permiso y riesgo de escritura que un agente de solo lectura no necesita.
- **Consecuencias:** Todo agente del harness es texto que entra, texto que sale. Cambiar de proveedor o de CLI no exige reescribir ningún prompt de agente. `memoria.py` hace en Python puro (gratis) lo que de otro modo el modelo tendría que descubrir con herramientas (pagando cuota).

### D-030 — El modelo es argumento del constructor del `Provider`, no de `send`

- **Fecha:** 2026-07-23
- **Contexto:** `ClaudeCLIProvider` necesitaba saber qué modelo usar (`haiku`, `sonnet`, `opus`) para que `src/soda/core/flota.py` pudiera asignar un modelo distinto a cada agente.
- **Decisión:** El modelo se fija en el constructor del `Provider` (`ClaudeCLIProvider(model=...)`); la interfaz `Provider.send(prompt) -> str` no se toca.
- **Alternativas descartadas:** Pasar el modelo como parámetro de `send(prompt, model=...)`, descartado porque el modelo es configuración del proveedor (quién construye la flota decide qué modelo usa cada agente), no configuración del mensaje; el agente recibe el `Provider` ya construido por inyección y no sabe qué hay detrás.
- **Consecuencias:** `flota.proveedor_para(agente, project_root)` es el único sitio que decide el modelo; el agente (`SesionStarter`) nunca elige ni conoce el modelo que usa.

### D-031 — La suscripción se garantiza borrando las variables de entorno de API, no confiando en que no estén

- **Fecha:** 2026-07-23
- **Contexto:** El CLI `claude` prefiere `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN` si están presentes en el entorno y factura por token, justo lo que el proyecto existe para evitar (C-006).
- **Decisión:** `ClaudeCLIProvider` (con `solo_suscripcion=True`, por defecto) borra `ANTHROPIC_API_KEY` y `ANTHROPIC_AUTH_TOKEN` del entorno del subproceso antes de invocar el CLI, en vez de asumir que nadie las tiene puestas. Verificado: con una key falsa puesta en el entorno, la llamada sigue funcionando sobre suscripción.
- **Alternativas descartadas:** Confiar en que el entorno de ejecución nunca tenga esas variables, descartado por frágil: cualquier máquina de desarrollo con la API configurada para otro proyecto rompería la premisa central sin ningún aviso. También se descarta usar `--bare` del CLI `claude` (fuerza autenticación por API key) y `--max-budget-usd` como control de gasto (solo aplica a API key, no a suscripción).
- **Consecuencias:** El uso de suscripción queda garantizado por código, no por convención de entorno. Cualquier proveedor nuevo basado en CLI debe replicar este patrón si el CLI subyacente tiene el mismo comportamiento de preferir credenciales de API.

### D-032 — Los archivos de memoria bajo demanda viajan solo con su índice

- **Fecha:** 2026-07-23
- **Contexto:** Al componer el prompt de `sesion-starter`, había que decidir cuánto de `lessons.md`/`decisions.md`/`constraints.md`/`assumptions.md` (los cuatro de lectura bajo demanda) entrar al contexto del modelo.
- **Decisión:** Esos cuatro archivos viajan solo con su sección `## Índice`; `progress.md` y `tasks.md` viajan íntegros. Aplica al pie de la letra la convención ya vigente en el proyecto de que el índice es la interfaz de búsqueda.
- **Alternativas descartadas:** Enviar los seis archivos íntegros, descartado por costo de contexto sin beneficio proporcional: el índice ya dice qué existe y dónde, que es todo lo que el informe de reanudación necesita reportar sin profundizar.
- **Consecuencias:** Efecto medido: 86 KB de memoria completa se convierten en 44 KB de prompt. Si el informe necesitara detalle de un archivo bajo demanda, ese detalle quedaría fuera de esta primera versión (no hay mecanismo de "pedir más" todavía).

### D-033 — `MODELOS` es un diccionario en código, no un archivo de configuración

- **Fecha:** 2026-07-23
- **Contexto:** Definir dónde vive el mapa agente→modelo que usa `src/soda/core/flota.py`.
- **Decisión:** `MODELOS` es un diccionario Python hardcodeado en `flota.py`. `sesion-starter` usa `haiku` porque el criterio de elección de modelo es el trabajo que hace el agente, no su importancia: resume archivos que ya tiene delante, no razona sobre código ni decide nada, y eso lo hace bien un modelo pequeño (relacionado con C-006, la cuota es el presupuesto real).
- **Alternativas descartadas:** Un archivo de configuración (YAML/TOML) para el mapa agente→modelo, descartado por ahora: con un solo agente registrado, construir formato, lectura, validación y errores de un archivo de configuración resuelve un problema que todavía no existe.
- **Consecuencias:** Cambiar el modelo de un agente es editar una línea de `MODELOS`. Se convierte en archivo cuando el usuario necesite cambiar de modelo sin editar el paquete instalado.

### D-034 — Se adelanta el cableado de `soda start` con `sesion-starter`

- **Fecha:** 2026-07-23
- **Contexto:** El orden de construcción (D-028) había diferido a un "paso 6" no especificado el momento de conectar `soda start` con `sesion-starter` una vez ambos existieran por separado.
- **Decisión:** Al construir T-013 (`soda start`) en esta misma sesión, con T-012 (`sesion-starter`) ya implementado, se cableó la bifurcación completa en `cli.py` en vez de dejar un stub pendiente para más adelante.
- **Alternativas descartadas:** Dejar `soda start` con la rama de memoria como un `TODO`/stub hasta una sesión futura, descartado porque ambas piezas ya existían y dejarlas sin conectar habría sido peor que completar el cableado mientras el contexto de ambas estaba fresco.
- **Consecuencias:** `soda start` queda funcional de punta a punta en esta sesión (las dos ramas), verificado en real por el usuario, sin dejar trabajo a medias entre T-012 y T-013.

### D-035 — Pivote: `soda` REPL persistente con delegación a subagentes sobre suscripción, no orquestador-script + subprocesos sin estado

- **Fecha:** 2026-07-23
- **Contexto:** `transcript.md` (video de referencia) describe un arnés construido con bucle REPL, un agente orquestador persistente, delegación a subagentes y memoria como tools. El usuario detectó que este modelo resuelve de raíz un problema recurrente del diseño actual: "¿cómo sabe `sesion-closer` qué pasó realmente en la sesión?" (D-024/D-025/D-026 asumían orquestador = script de Python + agentes = subprocesos `claude -p` sin estado entre turnos, así que el closer tiene que reconstruir la sesión leyendo memoria en disco). En el modelo REPL, el agente orquestador está presente durante toda la sesión, así que no hay nada que reconstruir al cierre.
- **Decisión:** `soda` pivota a un agente orquestador PERSISTENTE al estilo del video (bucle REPL, delega en subagentes), pero corriendo sobre suscripción, no sobre API de pago por token. Verificado con `ctx7` contra la documentación del Claude Agent SDK for Python (`anthropics/claude-agent-sdk-python`): el SDK autentica igual que el CLI (OAuth de `claude /login`, credenciales en `~/.claude/.credentials.json` en Windows, o `CLAUDE_CODE_OAUTH_TOKEN`), sin requerir `ANTHROPIC_API_KEY` (su precedencia de autenticación borra el uso de API si no hay key puesta), y trae de fábrica bucle agéntico, tools propias (`@tool` + `create_sdk_mcp_server`) y subagentes (`AgentDefinition`). El pivote se validó además empíricamente sin usar siquiera el SDK: dos spikes (T-018, `scripts/chat.py` y `scripts/chat_delegacion.py`) demuestran que tanto el bucle exterior (REPL multi-turno) como el bucle interior (delegación a un subagente) funcionan sobre suscripción usando solo el CLI `claude` como subproceso, verificados en real por el usuario en su máquina.
- **Alternativas descartadas:** Mantener el modelo orquestador = script de Python + agentes = subprocesos `claude -p` sin estado (D-024 a D-026), descartado porque el problema de fondo (reconstruir qué pasó en la sesión al cerrar) se resuelve mejor con un proceso persistente que estuvo presente todo el tiempo que con memoria en disco leída después del hecho.
- **Consecuencias:** REABRE y SUPERA a D-025 (orquestador LLM pospuesto) y D-026 (interfaz de cinco comandos `init`/`start`/`step`/`status`/`close`) — no se borran ni se renumeran, quedan documentadas como el diseño previo al pivote, con esta entrada como referencia cruzada de por qué quedaron superadas. También reabre el orden de construcción D-028. Buena parte del diseño de `state.yaml`/`soda step` discutido antes del pivote (T-014) queda supeditada a la reevaluación de T-019. Se registra T-019 como próxima tarea: reevaluar qué sobrevive del trabajo hecho (doctrina `_guideline/`, memoria `_persistence/`, `soda init`, `soda start`) y definir el nuevo orden de construcción.

### D-036 — El bucle interior del orquestador usa `tool_use` estructurado del Claude Agent SDK, no la convención de marcador `[[LLAMAR:...]]`

- **Fecha:** 2026-07-23
- **Contexto:** T-019 dejó abierto (tras el pivote D-035) cómo señalizar la delegación a subagentes. Los spikes de T-018 validaron la convención de marcador de texto `[[LLAMAR:fecha]]`, pero C-008 la documentó como frágil (depende de que el modelo emita el marcador limpio) y con doble costo de cuota por delegación. El usuario propuso un flujo de arranque esperado para `soda` y de su análisis se separaron cuatro decisiones de diseño que ese flujo escondía (ver hallazgos en el hito de esta sesión, `progress.md`).
- **Decisión:** El bucle interior se construye con el **Claude Agent SDK for Python** (`claude-agent-sdk`), usando `tool_use` estructurado (herramientas `@tool` y subagentes `AgentDefinition`) en vez de la convención de marcador. Motivo: `tool_use` da un bloque estructurado del protocolo (nombre + input JSON validado contra esquema, detección por `stop_reason == "tool_use"`), determinista, en vez del texto frágil de C-008. Punto crítico verificado: el `tool_use` estructurado sobre SUSCRIPCIÓN (sin `ANTHROPIC_API_KEY`, respetando C-006/D-031) llega por el Agent SDK, no por la Messages API (que factura por token); el Agent SDK autentica por OAuth de `claude /login`, ya verificado en D-035/L-014. Es decir: "decidir `tool_use`" equivale a "decidir el Camino B (Agent SDK)"; no son decisiones separadas. El SDK se encapsula detrás de la abstracción `Provider` para no clausurar `codex` ni otros CLIs (protege D-006 y D-008); no debe filtrarse más allá de la frontera del proveedor.
- **Alternativas descartadas:** Mantener la convención de marcador `[[LLAMAR:...]]` de C-008 para el producto (Camino A, REPL a mano sobre `ClaudeCLIProvider`). Descartada porque la convención es frágil y duplica la cuota (C-006); el `tool_use` estructurado resuelve C-008 de raíz. El Camino A conserva portabilidad entre proveedores, pero se prefirió resolver bien la delegación donde importa (Claude) sin tirar la abstracción `Provider`.
- **Consecuencias:** (1) Reabre/supera parcialmente a C-008: la convención de marcador queda como diseño previo explorado en T-018, no como camino de producto (ver nota añadida en C-008). (2) `Provider.send(prompt) -> str` (D-008, interfaz de un solo disparo) evoluciona a un objeto sesión/conversación multi-turno; se registra como decisión superada por el pivote, en la misma línea que D-025/D-026. (3) El arranque en camino feliz NO necesita que el LLM decida a quién invocar: Python detecta el estado en disco y Python invoca; el marcador/`tool_use` frágil no toca el primer build. (4) Se registra T-020 como próxima tarea: spike de delegación con `tool_use` estructurado usando el Agent SDK sobre suscripción, equivalente a los spikes de T-018 pero validando el Camino B antes de comprometerlo en el orden de construcción de T-019.
- **Actualización (T-020, 2026-07-23):** Decisión CONFIRMADA por evidencia en vivo, no solo por documentación. `scripts/probar_agent_sdk.py` y `scripts/chat_delegacion_sdk.py` verificaron en la máquina real del usuario, sobre suscripción, los tres puntos críticos: `tool_use` estructurado gestionado por el propio SDK (sin bucle a mano), autenticación por OAuth sin `ANTHROPIC_API_KEY`, y delegación automática a un subagente `AgentDefinition` con enrutado correcto. Ver L-015 a L-017 para los hallazgos de configuración y observabilidad que salieron del spike.

### D-037 — La espina de control de `soda` es híbrida: Python determinista + sesión LLM persistente para el juicio

- **Fecha:** 2026-07-23
- **Contexto:** T-019 quedó completa de análisis (D-036) pero abierta en un punto: D-035 propone un orquestador vivo (sesión LLM persistente sobre `ClaudeSDKClient`) mientras que D-025/D-026 (reabiertas por D-035) fijaban que el camino feliz del incremento (`methodology.md` §3, tabla mecánica de 11 pasos) NO necesita juicio LLM, para no pagar cuota releyendo algo que un archivo ya dice gratis (C-006). Retomar T-019 exigía resolver esa tensión antes de fijar el nuevo orden de construcción: ¿quién decide el siguiente paso, Python o la sesión viva?
- **Decisión:** La espina de control se reparte explícitamente entre Python y la sesión LLM persistente, sin que ninguno absorba al otro. **Python (`soda`, el proceso)** posee todo lo determinista y barato: detección de estado en disco, git (NC-007, nunca lo decide el LLM), los gates humanos / canal con el humano (C-007), y qué fase toca según la tabla ya escrita en `methodology.md` §3 — cero cuota. **La sesión LLM persistente** (el orquestador vivo sobre `ClaudeSDKClient`, D-035) posee solo el juicio y la delegación a subagentes (D-036). La bifurcación "¿Python o LLM decide el siguiente paso?" solo aparece dentro de la maquinaria del MVP (la tabla de §3); durante el estadio de prototipado (`methodology.md` §4) no hay nada mecánico que dirigir, así que el frente de un proyecto nuevo es puro juicio humano + materialización de subagentes sobre la sesión viva (Descubridor → `discovery.md`, Prototipador, bucle P3↔P4, con el juicio de producto/UX y el "mago de Oz" reservados al humano, §4.2).
- **Alternativas descartadas:** Que la sesión LLM persistente decida también el camino feliz mecánico del incremento (todo bajo D-035), descartada porque violaría C-006/D-025: pagaría cuota en cada paso para releer una tabla que Python ya puede leer gratis. Que Python siga decidiendo todo y la sesión persistente quede solo como canal de E/S sin juicio (mantener D-024/D-025 intactas sin honrar D-035), descartada porque no resuelve el problema de fondo que motivó el pivote (reconstruir qué pasó en la sesión al cerrar) ni aprovecha la delegación estructurada ya validada en vivo (T-020).
- **Consecuencias:** Resuelve la tensión que D-035 dejó abierta al reabrir D-025/D-026: ambas siguen vigentes dentro de su dominio (Python decide el camino feliz mecánico), pero ya no describen la totalidad del control (la sesión persistente decide el juicio y delega). Fija el nuevo orden de construcción (T-021 a T-027, ver `progress.md`), con la incógnita de sesión persistente (`ClaudeSDKClient` multi-turno detrás de `Provider`) como primer paso a resolver. Confirma que el arranque de un proyecto nuevo empieza siempre por el estadio de prototipado (`methodology.md` §4), no por la maquinaria del incremento.
