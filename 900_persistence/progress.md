# Progress

## Índice
- [Estado actual](#estado-actual)
- [Qué sigue](#qué-sigue)
- [Historial de hitos](#historial-de-hitos)

## Estado actual

T-010 quedó resuelta: `methodology.md` recibió una revisión de fondo en tres pasos. (1) El
usuario acotó el harness a trabajar exclusivamente proyectos de desarrollo de software,
recortando toda referencia a Ciencia de datos/ML preservando la distinción entre "producto
ML" (se fue) y "agente LLM probabilístico" (tesis central del harness, se quedó). (2) Se
introdujo un marcado de tres estados —normativo (sin marca), `[DIFERIDO]`, `[PENDIENTE]`—
en una nueva §0.3 con el núcleo normativo y una tabla de 8 piezas de infraestructura
ausentes. (3) El archivo se dividió en `methodology.md` (607 líneas, el proceso) y el nuevo
`src/soda/templates/_guideline/agents-and-evaluation.md` (483 líneas, agentes y evaluación),
sin renumerar ninguna sección: los números quedaron únicos globalmente entre ambos archivos
y ninguna referencia cruzada se rompió (verificado por script). Verificado con 57 tests
(`pytest`, `ruff` limpio) y wheel construido con los tres `.md` presentes. `soda init` sigue
funcional y globalmente instalado desde la sesión anterior; la capa de proveedores
(`Provider` + `ClaudeCLIProvider`) sigue funcionando de extremo a extremo. Los tres
documentos de `_guideline/` viajan dentro del paquete instalado pero ningún comando los
siembra todavía en el proyecto destino (T-009, bloqueada por D-012). Detectada tarea nueva
T-011: `principles.md` §5 usa un vocabulario de estado distinto del recién introducido en
§0.3 y hay que unificarlos. No hay agentes propios de `soda` todavía.

## Qué sigue

- [T-009](tasks.md#t-009--soda-init-debe-sembrar-_guideline-en-el-proyecto-destino) — `soda init` debe sembrar `_guideline/` en el proyecto destino; tal como está planteada contradice D-012, hay que revisar esa decisión primero (opciones: ampliar D-012, subcomando `soda guideline`, o flag `--with-guideline`; recomendada la primera). Es la tarea recomendada para la próxima sesión: convierte trabajo ya hecho (1.474 líneas de `_guideline/`) en valor entregado.
- [T-011](tasks.md#t-011--unificar-taxonomía-de-estado-entre-principlesmd-5-y-el-03-nuevo) — Unificar la taxonomía de estado entre `principles.md` §5 y el §0.3 de `agents-and-evaluation.md`
- Queda sobre la mesa, sin comprometer, la alternativa de implementar `CodexCLIProvider` antes de avanzar con agentes.
- Queda como decisión de diseño abierta, no como edición pendiente: si `agents-and-evaluation.md` §5 (~12 arquetipos de agente) describe el destino o especifica ya lo que se construye; su urgencia bajó al quedar marcada `[PENDIENTE]`, pero el punto de fondo sigue sin resolver.
- Sin tareas registradas todavía para el diseño de los agentes propios del harness (`sesion-starter`, `agent-worker`, `sesion-closer`); depende de que T-009/T-011 avancen o se decida posponerlas.

## Historial de hitos

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
