# Progress

## Índice
- [Estado actual](#estado-actual)
- [Qué sigue](#qué-sigue)
- [Historial de hitos](#historial-de-hitos)

## Estado actual

Sesión de análisis y decisión pura sobre T-019, sin cambios de código. El usuario propuso un
flujo de arranque esperado para `soda` y, del análisis de ese flujo, salió D-036: el bucle
interior del orquestador se construye con el **Claude Agent SDK for Python** usando
`tool_use` estructurado (Camino B), no con la convención de marcador `[[LLAMAR:...]]`
validada en T-018 (Camino A, que queda documentada como diseño previo, C-008 superada para
producto). El SDK se encapsula detrás de `Provider` para no clausurar `codex`/otros CLIs
(protege D-006/D-008). Del análisis quedaron ordenados cuatro hallazgos que acotan el resto
de T-019: (1) la detección de estado del proyecto es Python puro, con **tres** estados en
disco —VACÍO, SEMBRADO_SIN_TRABAJO, CON_MEMORIA—, no dos; (2) el Descubridor, no
`sesion-starter`, es el primer agente en un proyecto estrictamente nuevo (confirma D-028); (3)
el REPL persistente desbloquea la parte de C-007 que seguía abierta (la entrevista de
arranque del Descubridor deja de necesitar andamiaje especial); (4) `sesion-starter` sigue
siendo un subagente haiku separado, pero lo invoca Python al detectar CON_MEMORIA, no el LLM.
T-019 sigue `No implementada` (avanzada parcialmente); se registra T-020 como próximo paso
concreto antes de cerrar T-019 del todo.

## Qué sigue

- [T-020](tasks.md#t-020--spike-de-delegación-con-tool_use-estructurado-claude-agent-sdk-sobre-suscripción) — Spike de delegación con `tool_use` estructurado usando el Claude Agent SDK sobre suscripción, equivalente a los spikes de T-018 pero validando el Camino B (D-036) antes de comprometerlo en el orden de construcción.
- [T-019](tasks.md#t-019--reevaluar-el-orden-de-construcción-de-soda-a-la-luz-del-pivote-replsuscripción) — Completar la reevaluación del orden de construcción con el REPL/orquestador persistente en el centro, usando los cuatro hallazgos de esta sesión como base.
- El resto del orden de construcción anterior (T-014 a T-017) queda en suspenso, pendiente de lo que resuelva T-019; no se cancela, pero probablemente cambie de forma.

## Historial de hitos

### 2026-07-23 — Sesión de análisis y decisión sobre T-019: el bucle interior usa `tool_use` estructurado del Agent SDK (D-036)

Sesión 100% análisis, sin código. Retomó T-019 a partir de un flujo de arranque propuesto por
el usuario; de su análisis salió D-036, decisión firme sobre el bucle interior del
orquestador: se construye con el Claude Agent SDK for Python (`tool_use` estructurado,
herramientas `@tool` y subagentes `AgentDefinition`), no con la convención de marcador
`[[LLAMAR:...]]` de T-018, que queda como diseño previo (C-008 anotada como superada para
producto). Punto crítico verificado en el análisis: el `tool_use` estructurado sobre
suscripción llega por el Agent SDK, no por la Messages API de pago por token; "decidir
`tool_use`" es lo mismo que "decidir el Camino B (Agent SDK)". El SDK se encapsula detrás de
`Provider` para proteger D-006/D-008 y no clausurar `codex`. Del mismo análisis salieron
cuatro hallazgos que ordenan el resto de T-019 (detección de estado en tres pasos por Python
puro; el Descubridor como primer agente real en proyecto nuevo, confirmando D-028; el REPL
persistente desbloqueando la parte abierta de C-007; `sesion-starter` invocado por Python, no
por el LLM). Se registra T-020 como próximo paso: spike del Camino B con el Agent SDK.

### 2026-07-23 — Pivote de arquitectura: orquestador persistente tipo REPL sobre suscripción, validado con dos spikes (D-035, T-018)

Sesión que abrió discutiendo T-014 (`state.yaml`) y derivó en un replanteamiento de fondo,
disparado por `transcript.md`. Se registra D-035: `soda` pivota a un agente orquestador
persistente (bucle REPL, delega en subagentes) sobre suscripción, no sobre API de pago por
token; reabre y supera D-025/D-026/D-028 (no se borran, quedan documentadas como diseño
previo). Verificado con `ctx7` (documentación del Claude Agent SDK for Python) que el SDK
autentica con la suscripción (OAuth de `claude /login`, sin requerir `ANTHROPIC_API_KEY`) y
trae bucle agéntico, tools y subagentes de fábrica (L-014); construir el bucle interior a
mano, como el video, exige la API si no se usa el SDK. Construidos y verificados en real dos
spikes en `scripts/` (T-018, fuera de producto, C-003): `chat.py` (REPL multi-turno,
reenviando historial completo) y `chat_delegacion.py` (delegación a un subagente `fecha` vía
marcador de convención `[[LLAMAR:fecha]]`, con el dato real calculado por Python y modelo por
agente, `sonnet` decide / `haiku` redacta). Ambos verificados en vivo por el usuario en su
máquina sobre la suscripción. Se registra C-008 (la convención de marcador es frágil y cada
delegación cuesta 2 llamadas contra la cuota). T-014 (`state.yaml`) queda sin implementar,
con el diseño de avance anotado en su detalle pero supeditado a la reevaluación de T-019,
registrada como próxima tarea.

### 2026-07-23 — `soda start` y `sesion-starter` implementados y verificados (T-012, T-013)

`src/soda/agents/` nuevo: `memoria.py` (lectura de `_persistence/` en Python puro, con
detección de "memoria vacía" por comparación contra la plantilla), `prompts/sesion_starter.md`
(portado de la skill `session-startup`) y `sesion_starter.py` (clase `SesionStarter`, falla
antes de invocar al modelo si la memoria está vacía). `ClaudeCLIProvider` ampliado con
`model`/`tools`/`cwd`/`solo_suscripcion`. `src/soda/core/flota.py` nuevo: único punto
agente→modelo. `src/soda/core/git.py` y `src/soda/start.py` nuevos: bootstrap de Git 100%
Python, sin operaciones destructivas, con diálogo inyectado (`preguntar`/`informar`) para
poder testearlo sin bloquear en `input()`. `soda start` en `cli.py` bifurca entre ambas
ramas leyendo la memoria. Se registran D-029 a D-034, L-011 a L-013. Verificado con 145
tests, `ruff` limpio y dos pruebas manuales del usuario en máquina real: bootstrap completo
(init → start → GitHub → idempotencia) y reanudación con informe de haiku sobre memoria real.

### 2026-07-23 — Sesión de diseño: alcance de agentes, naturaleza del orquestador e interfaz de comandos (D-022 a D-028, C-007, L-010)

Sin código nuevo. Se resolvió que `agent-worker` no se construye (era ejemplo genérico) y en
su lugar se construyen agentes especializados según los arquetipos de
`agents-and-evaluation.md` §5, que pasa de descripción a hoja de ruta (D-022, D-023). Se
corrigió el supuesto de que `soda` corre dentro de una sesión de Claude Code/Codex: es un
script de Python en terminal y es el propio orquestador (D-024, lección L-010); se decidió
posponer un orquestador LLM porque el camino feliz ya es mecánico (D-025). Se descubrió que
`claude -p` no tiene canal con el humano, así que gates y diálogo viven en Python (C-007).
Se diseñó la interfaz de cinco comandos (`init`/`start`/`step`/`status`/`close`, D-026), se
fijó `state.yaml` como prerrequisito de `step`/`status` (D-027) y se estableció el orden de
construcción completo con `sesion-starter` como primer agente (D-028). Registradas T-013 a
T-017; T-012 ajustada con su lugar fijado en el orden. El usuario verificó `soda init` en un
proyecto real, confirmando T-009.

### 2026-07-23 — `soda init` siembra `_guideline/` y taxonomía de estado unificada (T-009, T-011)

`soda init` pasó de sembrar solo memoria a sembrar memoria y doctrina en una sola pasada:
`init_guideline()` nueva, junto con `guideline_root()`/`read_guideline_template()` en
`templates/__init__.py`, apoyadas en helpers comunes factorizados de la implementación de
`_persistence` (D-020, enmienda a D-012). Introducida la distinción `SALTADO`/`DIFIERE` al
reportar archivos existentes (D-021): la memoria diverge por diseño y se salta sin
comparar, la doctrina la posee la versión instalada del paquete y un desfase se reporta en
vez de esconderse. `principles.md` §5 y `methodology.md` §0.3 quedaron con un solo
vocabulario de estado (normativo / `[DIFERIDO]` / `[PENDIENTE]`, D-018), citado por
referencia desde una nueva §0.5 en `principles.md`. Suite subió de 57 a 82 tests, `ruff`
limpio, wheel verificado y ejecución real confirmando siembra y detección de desfase.
Detectada y registrada T-012 (`sesion-starter`), acordada con el usuario como siguiente
tarea.

### 2026-07-23 — Revisión de fondo de `methodology.md`: alcance exclusivo de software, marcado normativo/diferido/pendiente y división del archivo (T-010)

`methodology.md` pasó por tres pasos de fondo. Recorte de alcance a desarrollo de software
exclusivo (53 inserciones/54 borrados, D-017), preservando con cuidado la distinción entre
el producto ML retirado y el agente LLM probabilístico que construye el harness (L-009).
Marcado de tres estados de aplicación —normativo, `[DIFERIDO]`, `[PENDIENTE]`— en nueva
§0.3, con 9+14 marcas colocadas y dos afirmaciones de fondo corregidas (D-018). División en
dos archivos sin renumerar secciones, aprovechando que los números quedan únicos entre
ambos documentos (D-019); `methodology.md` bajó de 979 a 607 líneas, nuevo
`agents-and-evaluation.md` con 483. Verificado con 57 tests, `ruff` limpio, wheel con los
tres `.md`, y validación por script de cero referencias `§N` rotas. Se registran D-017 a
D-019, L-008 y L-009. Se detecta y registra T-011 como tarea nueva.

### 2026-07-23 — `905_guideline` mudado a producto y `principles.md` reescrito por audiencia (T-007, T-008)

`905_guideline/` (andamiaje en la raíz) se mudó con `git mv` a
`src/soda/templates/_guideline/` (producto, viaja con `soda`), verificado instalando el
wheel en venv limpio. `principles.md` pasó de 125 a 384 líneas: reorganizado en tres
secciones por audiencia (diseño del arnés, operación del orquestador, reglas de ejecución
del agente), resolviendo los 8 puntos pendientes de T-007 (paralelización condicionada al
presupuesto de cuota, umbral de escalado al orquestador, evidencia proporcional por tipo de
artefacto, señales externas para el context reset, presupuesto de sesión, frontera de
operaciones destructivas, precedencia humano > NC > P > E, códigos a 3 dígitos permanentes).
`methodology.md` (883 líneas, hallado sin versionar) se resincronizó con los nuevos códigos
y se corrigieron typos y referencias colgantes. Se registran D-014 a D-016, L-006, L-007 y
C-006. Se detectaron y registran como tareas nuevas T-009 y T-010.

### 2026-07-23 — `soda init` funcional y publicado en el PATH vía pipx

Implementadas y verificadas T-004, T-005 y T-006: plantilla de `_persistence` empaquetada y
accesible vía `importlib.resources`, CLI `soda init` no destructiva con relleno parcial y
`--force`, y entry point habilitado e instalado con `pipx install -e`, dejando `soda`
disponible globalmente en modo editable. Se creó `README.md`. Se registran D-009 a D-013,
L-004, L-005, C-005 y A-001. Se detectaron contradicciones internas en
`905_guideline/principles.md`, registradas como T-007.

### 2026-07-23 — Capa de proveedores: `Provider` + `ClaudeCLIProvider` verificados en real

Implementadas y verificadas T-002 y T-003: la abstracción `Provider` y `ClaudeCLIProvider`
quedan probadas contra el CLI `claude` real (prompts largos, UTF-8, caminos de error), no
solo con mocks. Se registran las decisiones de ubicación de proveedores concretos, entrega
del prompt por stdin, e interfaz mínima del `Provider` (D-006 a D-008), y la lección sobre
la codificación de stdout en Windows (L-003).

### 2026-07-23 — Bootstrap del repositorio y esqueleto del paquete `soda`

Proyecto inicializado desde cero: Git local, remoto GitHub enlazado y push inicial
(commit `987864b`). Se resolvió un bloqueo de privacidad de email de GitHub configurando
`user.email` local del repo con la dirección `noreply`. Se creó y verificó la estructura
base instalable del paquete `soda` (T-001).
