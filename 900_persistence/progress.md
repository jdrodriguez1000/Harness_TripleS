# Progress

## Índice
- [Estado actual](#estado-actual)
- [Qué sigue](#qué-sigue)
- [Historial de hitos](#historial-de-hitos)

## Estado actual

Sesión de diseño puro, sin código nuevo, posterior al cierre de T-009/T-011. Se resolvió la
pregunta de diseño que quedaba abierta sobre `agents-and-evaluation.md` §5: `agent-worker`
no se construye (era un placeholder genérico), en su lugar el harness construye agentes
especializados (Probador, Implementador, Refactorizador, Revisor de código, etc., D-022), y
§5 pasa de descripción a hoja de ruta de esos agentes (D-023). Se corrigió un supuesto de
diseño equivocado: `soda` no corre dentro de una sesión de Claude Code/Codex, es un script
de Python en terminal, así que el orquestador es el script mismo (D-024, L-010); se decidió
posponer un orquestador LLM porque el camino feliz de un incremento ya es mecánico contra
`methodology.md` §3 y no necesita juicio de coordinación (D-025). Se descubrió una
restricción técnica: `claude -p` no tiene canal con el humano, así que los gates y todo
diálogo con el usuario viven en Python (C-007). Se diseñó la interfaz de comandos completa
(`init`/`start`/`step`/`status`/`close`, D-026), se estableció que `state.yaml` es
prerrequisito de `soda step`/`soda status` y no un rodeo (D-027), y se fijó el orden de
construcción con `sesion-starter` como primer agente por ser el único de solo lectura
(D-028). Quedan registradas cinco tareas nuevas (T-013 a T-017) para ese orden y T-012
ajustada con su lugar fijado (segundo paso). El usuario verificó además por su cuenta que
`soda init` (instalado con pipx) siembra tanto `_persistence/` como `_guideline/` en un
proyecto real, confirmando T-009. No hay agentes propios de `soda` todavía.

## Qué sigue

- [T-013](tasks.md#t-013--soda-start-rama-de-proyecto-vacío-bootstrap-git-en-python-puro) — `soda start`, rama de proyecto vacío: bootstrap Git en Python puro (`git init`, `.gitignore`, URL de GitHub, remote, commit, push). Es el punto de entrada de la siguiente sesión.
- [T-012](tasks.md#t-012--implementar-sesion-starter-como-agente-de-soda) — `sesion-starter`, segundo paso del orden de construcción (D-028): único agente de solo lectura, con prototipo ya probado (`harness-starter` + skill `session-startup`, seis sesiones) y consumidor real de `Provider`/`ClaudeCLIProvider`.
- [T-014](tasks.md#t-014--stateyaml-formato-mínimo-del-estado-del-incremento) — `state.yaml`, prerrequisito de `soda step`/`soda status` (D-027).
- [T-015](tasks.md#t-015--soda-status-lectura-del-estado-cero-cuota) — `soda status`, lectura del estado, cero cuota.
- [T-016](tasks.md#t-016--soda-step-invocar-al-agente-especializado-que-corresponda) — `soda step`, agentes especializados (D-022).
- [T-017](tasks.md#t-017--soda-close-invocar-a-sesion-closer) — `soda close`, invoca a `sesion-closer`.
- Descartada explícitamente como alternativa: implementar `CodexCLIProvider` antes de tener consumidor del primer proveedor.

## Historial de hitos

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
