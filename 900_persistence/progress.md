# Progress

## Índice
- [Estado actual](#estado-actual)
- [Qué sigue](#qué-sigue)
- [Historial de hitos](#historial-de-hitos)

## Estado actual

`soda init` funciona de extremo a extremo y está instalado globalmente: `pipx install -e`
deja el comando `soda` disponible en el PATH en modo editable, y `soda init` siembra los
seis archivos de memoria de `src/soda/templates/_persistence/` en cualquier `project_root`,
de forma no destructiva, con relleno parcial idempotente y `--force` para sobrescribir.
Verificado con 57 tests automatizados (`pytest`, `ruff` limpio), con instalación en venv
limpio, y con pruebas manuales reales incluyendo rutas con caracteres no ASCII. La capa de
proveedores (`Provider` + `ClaudeCLIProvider`) sigue funcionando de extremo a extremo desde
la sesión anterior. T-007 quedó resuelta: `principles.md` y `methodology.md` se mudaron de
`905_guideline/` (raíz, andamiaje) a `src/soda/templates/_guideline/` (producto, T-008) y
`principles.md` se reescribió por audiencia (384 líneas) resolviendo sus 8 contradicciones
internas, con `methodology.md` resincronizado a los nuevos códigos. Los documentos viajan
dentro del paquete instalado pero todavía no los siembra ningún comando en el proyecto
destino (T-009), y `methodology.md` sigue teniendo defectos de fondo no resueltos (T-010).
No hay agentes propios de `soda` todavía.

## Qué sigue

- [T-009](tasks.md#t-009--soda-init-debe-sembrar-_guideline-en-el-proyecto-destino) — `soda init` debe sembrar `_guideline/` en el proyecto destino; nota: tal como está planteada contradice D-012, hay que revisar esa decisión primero
- [T-010](tasks.md#t-010--revisión-de-fondo-de-methodologymd) — Revisión de fondo de `methodology.md` (883 líneas): normativo vs. diferido, gatillo de división ya disparado, backlog de referencias hacia adelante, tensión con E-004
- Queda sobre la mesa, sin comprometer, la alternativa de implementar `CodexCLIProvider` antes de avanzar con agentes.
- Sin tareas registradas todavía para el diseño de los agentes propios del harness (`sesion-starter`, `agent-worker`, `sesion-closer`); depende de que T-009/T-010 avancen o se decida posponerlas.

## Historial de hitos

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
