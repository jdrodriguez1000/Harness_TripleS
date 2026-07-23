# Progress

## Índice
- [Estado actual](#estado-actual)
- [Qué sigue](#qué-sigue)
- [Historial de hitos](#historial-de-hitos)

## Estado actual

La capa de proveedores del harness ya funciona de extremo a extremo: `Provider` (ABC) en
`src/soda/core/provider.py` y `ClaudeCLIProvider` en `src/soda/providers/claude_cli.py`
invocan el CLI `claude` real por subproceso, con el prompt entregado por stdin (validado con
prompts de más de 13.000 caracteres y con texto UTF-8 con acentos). Verificado con 14 tests
automatizados (`pytest`, `ruff` limpio) y con `scripts/probar_provider.py` corriendo contra
el CLI instalado en la máquina. Aún no existe ninguna CLI propia del harness (`soda init` no
funciona todavía): falta la plantilla de `_persistence`, el módulo `soda.cli` y habilitar el
entry point con pipx. Esa es la ruta acordada para la próxima sesión.

## Qué sigue

- [T-004](tasks.md#t-004--plantilla-de-contenido-de-_persistence) — Definir el contenido de la plantilla `_persistence`
- [T-005](tasks.md#t-005--srcsodaclipy-con-el-subcomando-init) — Escribir `src/soda/cli.py` con el subcomando `init`
- [T-006](tasks.md#t-006--habilitar-entry-point-e-instalar-con-pipx) — Habilitar el entry point e instalar con pipx
- Queda sobre la mesa, sin comprometer, la alternativa de implementar `CodexCLIProvider` antes de subir a la CLI; se eligió priorizar la ruta hacia `soda init`.

## Historial de hitos

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
