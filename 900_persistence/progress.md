# Progress

## Índice
- [Estado actual](#estado-actual)
- [Qué sigue](#qué-sigue)
- [Historial de hitos](#historial-de-hitos)

## Estado actual

T-009 y T-011 quedaron resueltas. T-009: `soda init` ahora siembra en una sola pasada tanto
`_persistence/` (memoria) como `_guideline/` (doctrina), reportando cada carpeta en su
propio bloque; el usuario decidió ampliar D-012 (enmendada en D-020) en vez de usar un
subcomando o flag aparte. Se introdujo una distinción deliberada al reportar (D-021): la
memoria existente siempre se salta sin comparar (`SALTADO`), pero un documento de
`_guideline/` que existe y no coincide con el del paquete se reporta como `DIFIERE` en vez
de esconderse bajo `SALTADO`, para que un destino con una versión vieja de `soda` no se
quede con doctrina desactualizada en silencio; ninguna de las dos carpetas se toca sin
`--force` (D-011 intacto). T-011: unificada la taxonomía de estado entre `principles.md` §5
(que usaba "gatillo de adopción") y `methodology.md` §0.3 (los tres estados normativo /
`[DIFERIDO]` / `[PENDIENTE]` de D-018); ahora `principles.md` §0.5 importa esa taxonomía por
referencia sin redefinirla, y §5 quedó marcada `[PENDIENTE]` en tabla. Verificado con 82
tests (`pytest`, `ruff` limpio, subida desde 57), wheel con los tres `.md` de `_guideline/`
más los seis de `_persistence/`, y ejecución real de `soda init` en proyecto de prueba
(siembra inicial y detección de desfase tras corromper un archivo). El `soda` global (pipx
editable) ya trae ambos cambios. Detectada y registrada tarea nueva T-012: implementar
`sesion-starter`, acordada como siguiente con el usuario. No hay agentes propios de `soda`
todavía.

## Qué sigue

- [T-012](tasks.md#t-012--implementar-sesion-starter-como-agente-de-soda) — Implementar `sesion-starter` como agente de `soda`, acordada con el usuario como la siguiente tarea. Es la de menor riesgo de los agentes propios porque ya existe un prototipo probado (`harness-starter` + skill `session-startup` de este mismo repo, ejercitado cinco sesiones); sería también el primer consumidor real de `Provider`/`ClaudeCLIProvider`. Precondición acotada: resolver la pregunta de diseño de `agents-and-evaluation.md` §5 solo para este agente, no para los doce arquetipos.
- Descartada explícitamente como alternativa a T-012: implementar `CodexCLIProvider` antes, porque añadir un segundo proveedor sin consumidor del primero profundiza código sin uso.
- Queda como decisión de diseño abierta, no como edición pendiente: si `agents-and-evaluation.md` §5 (~12 arquetipos de agente) describe el destino o especifica ya lo que se construye; para T-012 basta resolverla para un solo agente.
- Sin tareas registradas todavía para `agent-worker` ni `sesion-closer`; depende de cómo avance T-012.

## Historial de hitos

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
