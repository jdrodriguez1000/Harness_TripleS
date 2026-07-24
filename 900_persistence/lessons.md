# Lessons

## Índice

| Código | Título | Fecha |
|--------|--------|-------|
| [L-001](#l-001--las-carpetas-numeradas-no-sirven-como-convención-para-módulos-python) | Las carpetas numeradas no sirven como convención para módulos Python | 2026-07-23 |
| [L-002](#l-002--github-rechaza-el-push-si-el-email-del-commit-está-protegido-por-privacidad) | GitHub rechaza el push si el email del commit está protegido por privacidad | 2026-07-23 |
| [L-003](#l-003--al-diagnosticar-manejo-de-texto-en-windows-descartar-primero-la-herramienta-de-diagnóstico) | Al diagnosticar manejo de texto en Windows, descartar primero la herramienta de diagnóstico | 2026-07-23 |
| [L-004](#l-004--verificar-el-empaquetado-instalando-en-un-entorno-limpio-no-solo-listando-el-wheel) | Verificar el empaquetado instalando en un entorno limpio, no solo listando el wheel | 2026-07-23 |
| [L-005](#l-005--la-prueba-manual-encuentra-defectos-que-los-tests-no-buscan) | La prueba manual encuentra defectos que los tests no buscan | 2026-07-23 |
| [L-006](#l-006--un-documento-heredado-de-otro-proyecto-arrastra-referencias-colgantes) | Un documento heredado de otro proyecto arrastra referencias colgantes | 2026-07-23 |
| [L-007](#l-007--un-archivo-importante-puede-llevar-sesiones-sin-estar-en-git) | Un archivo importante puede llevar sesiones sin estar en git | 2026-07-23 |
| [L-008](#l-008--estimar-una-reducción-de-líneas-falla-cuando-el-contenido-a-quitar-vive-dentro-de-otras-líneas) | Estimar una reducción de líneas falla cuando el contenido a quitar vive dentro de otras líneas | 2026-07-23 |
| [L-009](#l-009--un-recorte-por-palabra-clave-puede-destruir-contenido-con-un-referente-distinto-que-comparte-la-misma-palabra) | Un recorte por palabra clave puede destruir contenido con un referente distinto que comparte la misma palabra | 2026-07-23 |
| [L-010](#l-010--no-asumir-el-entorno-de-ejecución-del-orquestador-sin-verificarlo-con-el-usuario) | No asumir el entorno de ejecución del orquestador sin verificarlo con el usuario | 2026-07-23 |
| [L-011](#l-011--un-test-que-consulta-git-puede-leer-la-configuración-global-de-la-máquina) | Un test que consulta git puede leer la configuración global de la máquina | 2026-07-23 |
| [L-012](#l-012--la-prueba-manual-volvió-a-encontrar-lo-que-la-suite-no-buscaba) | La prueba manual volvió a encontrar lo que la suite no buscaba | 2026-07-23 |
| [L-013](#l-013--validar-una-url-de-remoto-con-una-regex-estricta-rechaza-remotos-legítimos) | Validar una URL de remoto con una regex estricta rechaza remotos legítimos | 2026-07-23 |
| [L-014](#l-014--el-agent-sdk-for-python-es-en-la-práctica-la-única-vía-a-un-bucle-agéntico-con-toolssubagentes-estructurados-sobre-suscripción-sin-api) | El Agent SDK for Python es, en la práctica, la única vía a un bucle agéntico con tools/subagentes estructurados sobre suscripción sin API | 2026-07-23 |
| [L-015](#l-015--observabilidad-de-la-delegación-anidada-vía-parent_tool_use_id) | Observabilidad de la delegación anidada vía `parent_tool_use_id` | 2026-07-23 |
| [L-016](#l-016--el-agent-sdk-exige-permission_mode-y-toolsearch-explícitos-para-que-la-delegación-no-se-corte) | El Agent SDK exige `permission_mode` y `ToolSearch` explícitos para que la delegación no se corte | 2026-07-23 |
| [L-017](#l-017--la-herramienta-de-delegación-a-subagentes-cambia-de-nombre-según-el-build-del-cli) | La herramienta de delegación a subagentes cambia de nombre según el build del CLI | 2026-07-23 |
| [L-018](#l-018--el-agent-sdk-mergea-el-entorno-del-subproceso-no-permite-borrar-una-variable-heredada) | El Agent SDK mergea el entorno del subproceso: no permite borrar una variable heredada | 2026-07-23 |
| [L-019](#l-019--declarar-como-dependencia-directa-lo-que-se-importa-directo-aunque-hoy-llegue-transitivamente) | Declarar como dependencia directa lo que se importa directo, aunque hoy llegue transitivamente | 2026-07-23 |
| [L-020](#l-020--api-de-tools-in-process-del-agent-sdk-tool-create_sdk_mcp_server-y-esquema-vacío) | API de tools in-process del Agent SDK: `@tool`, `create_sdk_mcp_server` y esquema vacío | 2026-07-23 |

## Detalle de lecciones

### L-001 — Las carpetas numeradas no sirven como convención para módulos Python

- **Fecha:** 2026-07-23
- **Contexto:** Al diseñar la estructura de `src/soda/`, se consideró reflejar la convención de `900_persistence` (prefijos numéricos) dentro del código del paquete.
- **Lección:** Un módulo Python no puede empezar por un dígito, así que la numeración tipo `900_persistence` no es trasladable al código fuente.
- **Aplicación:** La numeración se mantiene únicamente en la documentación y en carpetas de andamiaje (como `900_persistence/`); el código bajo `src/soda/` usa nombres de módulo convencionales sin prefijos numéricos.

### L-002 — GitHub rechaza el push si el email del commit está protegido por privacidad

- **Fecha:** 2026-07-23
- **Contexto:** El push inicial del bootstrap del repositorio falló porque el email real del usuario (`jdrodriguez1000@gmail.com`) está protegido por la configuración de privacidad de GitHub.
- **Lección:** GitHub bloquea pushes cuyo commit use un email protegido; hay que usar la dirección `noreply` asociada a la cuenta (`<id>+<usuario>@users.noreply.github.com`).
- **Aplicación:** Se configuró `user.email` LOCAL al repo con `110043648+jdrodriguez1000@users.noreply.github.com`, evitando exponer el email real y desbloqueando el push sin tocar la configuración global de Git.

### L-003 — Al diagnosticar manejo de texto en Windows, descartar primero la herramienta de diagnóstico

- **Fecha:** 2026-07-23
- **Contexto:** Al ejecutar `scripts/probar_provider.py` contra el CLI real con prompts en español (acentos, eñes) y con un em-dash, la salida se veía corrompida (`�nicamente`) y un caso llegó a reventar con `UnicodeEncodeError`.
- **Lección:** Python en Windows escribe stdout en cp1252 por defecto; el `ClaudeCLIProvider` estaba devolviendo el texto UTF-8 correctamente, el problema era solo del propio script de diagnóstico al imprimir.
- **Aplicación:** Se corrigió con `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` (y `sys.stderr`) al inicio del script, con el porqué comentado en el código. Antes de concluir que un componente maneja mal el texto en Windows, hay que descartar primero que la propia herramienta de diagnóstico no sea la que corrompe la salida.

### L-004 — Verificar el empaquetado instalando en un entorno limpio, no solo listando el wheel

- **Fecha:** 2026-07-23
- **Contexto:** Verificar que las plantillas de `src/soda/templates/_persistence/` (T-004) viajan realmente en el paquete distribuible, no solo en el árbol de fuentes.
- **Lección:** Que un archivo aparezca en el `zipfile` del wheel no prueba que el código pueda leerlo en tiempo de ejecución desde una instalación real.
- **Aplicación:** La verificación decisiva fue construir el wheel, instalarlo en un venv desechable fuera del árbol de fuentes, y leer la plantilla desde ahí. Cuando un paquete distribuya datos (plantillas, recursos), la prueba válida es leerlos desde una instalación limpia, no solo listarlos en el archivo comprimido.

### L-005 — La prueba manual encuentra defectos que los tests no buscan

- **Fecha:** 2026-07-23
- **Contexto:** Corrida manual real de `soda init` en T-005, con la suite automatizada ya en verde.
- **Lección:** La prueba manual reveló un defecto cosmético ("1 creados", falta de concordancia de número en el resumen) que ningún test cubría porque nadie había pensado en ese caso.
- **Aplicación:** Mantener la prueba manual como paso de verificación aunque la suite esté verde; sirve para descubrir qué falta testear, no solo para confirmar lo que ya se testeó.

### L-006 — Un documento heredado de otro proyecto arrastra referencias colgantes

- **Fecha:** 2026-07-23
- **Contexto:** Al revisar `methodology.md` durante T-007, se encontraron citas a `L-015` y `L-022`, lecciones de otro proyecto que no existen en este repo (`lessons.md` va de L-001 a L-005) ni existirán en el destino, además de inconsistencias de ruta (`_template/` vs `_templates/`).
- **Lección:** Un documento de guía heredado de otro proyecto arrastra referencias colgantes (códigos inexistentes, rutas inconsistentes) que solo se detectan contrastándolo contra el repo real, no leyéndolo de corrido.
- **Aplicación:** Antes de dar por bueno un documento heredado, verificar cada referencia a código o ruta contra el estado real del repo destino; donde el código no exista, conservar la narrativa del hallazgo y quitar el código colgante en vez de dejarlo apuntando a la nada.

### L-007 — Un archivo importante puede llevar sesiones sin estar en git

- **Fecha:** 2026-07-23
- **Contexto:** Al mudar `905_guideline/` con `git mv` (T-008), `git status` reveló que `methodology.md` (876 líneas) aparecía como untracked: nunca había sido versionado, pese a llevar sesiones existiendo en el repo.
- **Lección:** Un archivo puede llevar sesiones de trabajo sin estar bajo control de versiones sin que nadie lo note; un `git clean` en cualquier momento lo habría borrado sin aviso.
- **Aplicación:** Revisar `git status` (no solo `git diff`) al tocar cualquier carpeta antigua o heredada, y tratar cualquier archivo untracked inesperado como una alerta a resolver antes de seguir, no como ruido a ignorar.

### L-008 — Estimar una reducción de líneas falla cuando el contenido a quitar vive dentro de otras líneas

- **Fecha:** 2026-07-23
- **Contexto:** Antes de recortar el alcance de ML en `methodology.md` (T-010 paso 1), se estimó una reducción de 45-60 líneas. El resultado real fue 53 inserciones/54 borrados: casi el doble de cambio de lo esperado, pero con reducción neta similar.
- **Lección:** Una estimación por "bloques a remover" solo es fiable si el contenido a quitar existe como bloques propios (párrafos, filas de tabla completas). Cuando vive como columna dentro de una tabla o como inciso dentro de una línea (p. ej. "(y umbrales, en ML)"), cada línea afectada requiere reescritura, no borrado, y el conteo de líneas netas no refleja el volumen real de ediciones.
- **Aplicación:** Antes de estimar el tamaño de un recorte de alcance, verificar si el contenido a quitar es removible como bloque o si está entrelazado dentro de líneas que hay que reescribir; en el segundo caso, contar ediciones (inserciones + borrados), no solo la reducción neta esperada.

### L-009 — Un recorte por palabra clave puede destruir contenido con un referente distinto que comparte la misma palabra

- **Fecha:** 2026-07-23
- **Contexto:** Al recortar el alcance de ML en `methodology.md` (T-010 paso 1), la palabra "probabilístico" tenía dos referentes distintos: el producto ML que el harness ya no cubre (se retiraba) y el agente LLM que construye el harness (tesis central, se conservaba). Un `grep ML` naíf sobre "probabilístico" habría arrastrado las 4 apariciones del segundo referente.
- **Lección:** Un recorte de alcance guiado por palabra clave o por tema superficial (ej. "todo lo de ML") puede destruir contenido no relacionado que comparte vocabulario con lo que se quiere quitar, si no se distingue antes el referente real de cada aparición.
- **Aplicación:** Antes de aplicar un recorte temático, listar cada aparición de los términos ambiguos y clasificar su referente real, no solo su forma superficial; conservar explícitamente las apariciones que apuntan a un concepto distinto del que se está retirando.

### L-010 — No asumir el entorno de ejecución del orquestador sin verificarlo con el usuario

- **Fecha:** 2026-07-23
- **Contexto:** Durante una sesión de diseño, se asumió que `soda` corría dentro de un harness de Claude Code o Codex, y que la frase de la doctrina "el orquestador es la sesión principal" aplicaba tal cual a ese entorno. El usuario corrigió: `soda` es un script de Python en terminal, sin sesión principal de Claude Code de por medio (ver D-024).
- **Lección:** Un supuesto sobre el entorno de ejecución de una pieza central del diseño (aquí, el orquestador) puede quedar sin verificar durante varias sesiones si nadie lo contrasta explícitamente contra la naturaleza real del producto que se está construyendo (`soda` es un script Python invocado desde terminal, no un agente de Claude Code).
- **Aplicación:** Al leer frases de la doctrina que mencionan "sesión principal" o similares, contrastar primero contra qué es literalmente el proceso que las ejecuta en este proyecto, en vez de asumir que se refieren al entorno donde se está teniendo la conversación de diseño.

### L-011 — Un test que consulta git puede leer la configuración global de la máquina

- **Fecha:** 2026-07-23
- **Contexto:** Los tests de `tests/test_start.py` fallaban de forma desconcertante: el usuario tiene `user.name = "Triple S"` configurado globalmente, así que el flujo de `bootstrap()` no preguntaba la identidad (la daba por resuelta), las respuestas inyectadas del humano falso se desplazaban una posición y fallaban pruebas sin relación aparente entre sí. Peor: los commits de prueba quedaban firmados con la identidad real del usuario.
- **Lección:** Cualquier código de test que invoque `git config --get` (directa o indirectamente) puede leer configuración global o de sistema de la máquina donde corre, no solo la del repositorio de prueba; eso contamina el resultado del test y, en este caso, filtraba datos reales del usuario a commits desechables.
- **Aplicación:** Se añadió una fixture `autouse` que aparta `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM` y `GIT_CONFIG_NOSYSTEM` durante los tests, aislando por completo la configuración de git que ve la suite de la de la máquina anfitriona.

### L-012 — La prueba manual volvió a encontrar lo que la suite no buscaba

- **Fecha:** 2026-07-23
- **Contexto:** Confirma L-005. La suite automatizada de `soda start` estaba en verde, pero al ejecutarlo con la entrada redirigida (no interactivo) reventó con un `EOFError` crudo de `input()` a mitad del arranque.
- **Lección:** Ningún test había ejercitado el camino de "sin terminal interactiva" porque nadie había pensado en ese caso concreto; la prueba manual lo encontró en el primer intento real. Concreta C-007 en la forma exacta en que muerde en la práctica: no solo "el agente no puede preguntar", sino "el propio script revienta feo si no hay con quién hablar".
- **Aplicación:** Se añadió `SinCanalConElHumanoError` con mensaje accionable, envolviendo `input()` para traducir el `EOFError` en un error con nombre y salida. Mantener la prueba manual en máquina real como paso de verificación aunque la suite esté verde sigue siendo la forma de descubrir qué falta testear.

### L-013 — Validar una URL de remoto con una regex estricta rechaza remotos legítimos

- **Fecha:** 2026-07-23
- **Contexto:** La primera versión de `url_valida()` en `src/soda/start.py` rechazaba rutas locales absolutas, que git acepta perfectamente como remoto y que además son lo que usan los tests como "GitHub falso" (un repositorio local en vez de uno real en la nube).
- **Lección:** Una validación de URL de remoto solo debe atrapar el error de tecleo obvio (pegar el nombre del repo en vez de su URL), no intentar decidir si el remoto existe o es "de verdad": eso lo dice el `push` y lo dice mejor, con el error real de git.
- **Aplicación:** Se corrigió la regex en el producto (no en el test) para aceptar también rutas locales absolutas y `file://`, documentando en el propio código por qué la validación es deliberadamente permisiva.

### L-014 — El Agent SDK for Python es, en la práctica, la única vía a un bucle agéntico con tools/subagentes estructurados sobre suscripción sin API

- **Fecha:** 2026-07-23
- **Contexto:** Al evaluar si el bucle interior del modelo del video de referencia (delegación a subagentes con `tool_use` estructurado) se podía construir a mano sobre el CLI `claude -p`, se verificó con `ctx7` la documentación del Claude Agent SDK for Python (`anthropics/claude-agent-sdk-python`), en el marco del pivote de arquitectura (D-035).
- **Lección:** Hand-rollear el bucle interior con `tool_use` estructurado, como hace el video, exige la API de pago por token. El Agent SDK for Python es prácticamente la única vía a un bucle agéntico con subagentes estructurados que además autentica con la suscripción (OAuth de `claude /login`, no `ANTHROPIC_API_KEY`). Sin el SDK, la delegación a subagentes solo se logra con una convención a mano (marcador de texto), verificada viable pero frágil (T-018, ver C-008).
- **Aplicación:** Al decidir el nuevo orden de construcción (T-019), evaluar explícitamente si el bucle interior se construye con el Agent SDK for Python o se mantiene la convención a mano. Matiz a no olvidar: el fallback de Keychain visto en el código del SDK es de macOS; en Windows las credenciales salen de `~/.claude/.credentials.json`.
- **Actualización (T-020, 2026-07-23):** Confirmada en vivo, no solo por documentación. `scripts/probar_agent_sdk.py` y `scripts/chat_delegacion_sdk.py` corrieron sobre la suscripción real del usuario (`is_error=False`, `ANTHROPIC_API_KEY` ausente del entorno).

### L-015 — Observabilidad de la delegación anidada vía `parent_tool_use_id`

- **Fecha:** 2026-07-23
- **Contexto:** Al construir `scripts/chat_delegacion_sdk.py` (T-020) para mostrar en pantalla qué hace la sesión principal y qué hace el subagente `clocker` al delegar.
- **Lección:** En el stream del Claude Agent SDK, cada `AssistantMessage`/`UserMessage` trae `parent_tool_use_id`. Los mensajes que pertenecen a un subagente lo traen apuntando al `id` del bloque `Agent`/`Task` que lo invocó; los de la sesión principal lo traen en `None`. Este campo permite atribuir en pantalla quién produjo cada paso (sesión principal vs. subagente concreto) sin inferencia ni heurística de texto.
- **Aplicación:** Insumo directo para la observabilidad del futuro orquestador REPL persistente (D-035): cualquier interfaz que muestre el trabajo de la sesión y sus subagentes puede apoyarse en `parent_tool_use_id` en vez de inventar un mecanismo de atribución propio.

### L-016 — El Agent SDK exige `permission_mode` y `ToolSearch` explícitos para que la delegación no se corte

- **Fecha:** 2026-07-23
- **Contexto:** Al construir `scripts/chat_delegacion_sdk.py` (T-020), la delegación a un subagente con herramienta `@tool` fallaba o se cortaba en modo no interactivo hasta ajustar dos parámetros del SDK.
- **Lección:** (a) Sin `permission_mode="bypassPermissions"`, el diálogo de permiso por herramienta interrumpe el turno porque no hay con quién dialogar en modo no interactivo (relacionado con C-007: `claude -p`/el SDK tampoco tienen canal con el humano a mitad de turno salvo que se le diga explícitamente que no lo pida). (b) El CLI difiere el esquema de las herramientas MCP: el modelo hace primero un paso `ToolSearch` para cargarlo antes de poder llamar a la herramienta real; si `ToolSearch` no está en `allowed_tools`, ese primer paso falla y la delegación nunca llega a ejecutar la herramienta. Este comportamiento se observó también en la terminal directa del usuario, no es artefacto de una sesión anidada.
- **Aplicación:** Cualquier uso futuro del Agent SDK con herramientas `@tool`/subagentes en modo no interactivo debe fijar `permission_mode="bypassPermissions"` y permitir `ToolSearch` en `allowed_tools`, o la delegación se corta silenciosamente o falla en el primer paso.

### L-017 — La herramienta de delegación a subagentes cambia de nombre según el build del CLI

- **Fecha:** 2026-07-23
- **Contexto:** Al observar en el stream cómo la sesión principal delega en el subagente `clocker` (T-020).
- **Lección:** La herramienta que la sesión principal usa para delegar en un subagente definido con `AgentDefinition` aparece como `Agent` o como `Task` según el build del CLI instalado, no con un nombre único y estable.
- **Aplicación:** Cualquier código que necesite reconocer o filtrar la herramienta de delegación en el stream (por ejemplo, para la observabilidad de L-015) debe aceptar ambos nombres, no asumir uno solo.

### L-018 — El Agent SDK mergea el entorno del subproceso: no permite borrar una variable heredada

- **Fecha:** 2026-07-23
- **Contexto:** Al construir `ClaudeSDKProvider` (T-021), había que forzar suscripción (D-031) neutralizando `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN` como ya hacía `ClaudeCLIProvider` sobre `subprocess.run`, pero pasando por `ClaudeAgentOptions.env` en vez de construir el entorno del subproceso a mano.
- **Lección:** El Claude Agent SDK arma el entorno del subproceso como `{**os.environ, **options.env}` (mergea sobre el entorno heredado); no existe forma de "eliminar" una variable ya presente pasando `options.env`, porque el merge nunca la quita, solo puede sobreescribir su valor. Verificado en la fuente del SDK (`_internal/transport/subprocess_cli.py`) y confirmado en vivo.
- **Aplicación:** Para neutralizar una variable de entorno heredada al usar el Agent SDK, hay que sobrescribirla a cadena vacía (`""`) en `options.env`, no intentar borrarla del diccionario; el CLI subyacente trata la cadena vacía como ausencia de credencial. Cualquier código futuro que arme `ClaudeAgentOptions.env` para excluir una variable del entorno debe seguir este mismo patrón.

### L-019 — Declarar como dependencia directa lo que se importa directo, aunque hoy llegue transitivamente

- **Fecha:** 2026-07-23
- **Contexto:** Al construir T-022 (bucle REPL), `src/soda/cli.py` empezó a importar `anyio` directamente para la frontera sync→async (`anyio.run`), pero `anyio` no estaba en `dependencies` de `pyproject.toml`: solo llegaba de rebote porque `claude-agent-sdk` lo arrastra como dependencia suya. Los tests en el `.venv` del repo pasaron sin problema (ahí `anyio` ya estaba instalado transitivamente), pero el `soda` global instalado con pipx en un entorno distinto falló con `ModuleNotFoundError: No module named 'anyio'` al correr `soda init`, hasta reinstalar con `pip install -e ".[dev]"`.
- **Lección:** Que un módulo esté disponible en el entorno de desarrollo no prueba que esté declarado como dependencia; si llega solo transitivamente vía otra librería, cualquier cambio futuro en esa librería (o cualquier entorno de instalación distinto al que se probó primero) puede romper el import sin ningún aviso previo.
- **Aplicación:** Todo módulo que el código de producto (`src/soda/`) importe directamente debe declararse en `dependencies` de `pyproject.toml`, sin importar si hoy llega gratis por una dependencia transitiva. Detectarlo requiere probar la instalación en un entorno distinto del que se usó para desarrollar (aquí, el `soda` global de pipx, no el `.venv` del repo), en la línea de L-004.

### L-020 — API de tools in-process del Agent SDK: `@tool`, `create_sdk_mcp_server` y esquema vacío

- **Fecha:** 2026-07-23
- **Contexto:** Al construir `src/soda/agents/memory_tool.py` (T-023), había que exponer `leer_memoria` como herramienta del Agent SDK sin dejar que el modelo elija la ruta del proyecto (C-002). API confirmada contra la documentación vigente vía `ctx7`.
- **Lección:** `@tool(name, description, input_schema)` devuelve un `SdkMcpTool` (dataclass con campos `name`/`description`/`input_schema`/`handler`/`annotations`; el `handler` es async e invocable directamente en tests). `create_sdk_mcp_server(name, tools=[...])` devuelve un servidor tipo dict (`{'type': 'sdk', 'name': ..., 'instance': Server}`), no una instancia de clase. Se registra pasando ese dict en `ClaudeAgentOptions(mcp_servers={nombre: server}, allowed_tools=["mcp__<servidor>__<tool>"])`; sin añadir el nombre completo a `allowed_tools`, la tool queda registrada pero inalcanzable. Un esquema de entrada vacío (`{}`) es válido para una tool sin parámetros.
- **Aplicación:** Para no dejar que el modelo elija una ruta u otro dato sensible (C-002), capturar el valor fijo (aquí, `project_root`) en un cierre de Python al construir la tool y dejar el esquema de entrada vacío, en vez de pedírselo como argumento al modelo. Cualquier tool in-process futura del harness debe seguir este mismo patrón de registro (servidor + `allowed_tools` con el nombre completo `mcp__<servidor>__<tool>`).
