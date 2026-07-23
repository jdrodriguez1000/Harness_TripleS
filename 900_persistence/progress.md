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
la sesión anterior. Se creó `README.md` en la raíz documentando instalación y uso. Queda
pendiente resolver las contradicciones de `905_guideline/principles.md` (T-007) antes de
escribir el primer prompt de agente del harness; no hay agentes propios de `soda` todavía.

## Qué sigue

- [T-007](tasks.md#t-007--actualizar-905_guidelineprinciplesmd-antes-de-escribir-el-primer-agente) — Actualizar `905_guideline/principles.md`; BLOQUEANTE antes de escribir el primer prompt de agente del harness
- Queda sobre la mesa, sin comprometer, la alternativa de implementar `CodexCLIProvider` antes de avanzar con agentes; se priorizó primero la ruta hacia `soda init` (ya cerrada) y ahora `905_guideline/principles.md`.
- Sin tareas registradas todavía para el diseño de los agentes propios del harness (`sesion-starter`, `agent-worker`, `sesion-closer`); depende de que T-007 quede resuelta primero.

## Historial de hitos

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
