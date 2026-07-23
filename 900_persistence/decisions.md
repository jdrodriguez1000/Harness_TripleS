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
- **Consecuencias:** `_persistence/` queda siempre trackeable por Git en el proyecto destino; cualquier necesidad futura de generar `CLAUDE.md` en destino sería una tarea separada.

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
