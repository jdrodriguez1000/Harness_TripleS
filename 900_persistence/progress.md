# Progress

## Índice
- [Estado actual](#estado-actual)
- [Qué sigue](#qué-sigue)
- [Historial de hitos](#historial-de-hitos)

## Estado actual

Primera sesión real del proyecto. Se hizo el bootstrap de Git + GitHub (remoto
`https://github.com/jdrodriguez1000/Harness_TripleS.git`, rama `master`) y se construyó el
esqueleto Python instalable del paquete `soda` ("Software Development Agentic"), con layout
`src/`, `pyproject.toml`, entorno virtual y una suite de smoke tests que pasa. El repo está
publicado y sincronizado con GitHub. Aún no existe ningún código funcional de orquestación
de agentes; el siguiente frente es la capa de proveedores (invocación de CLIs de IA como
subproceso).

## Qué sigue

- [T-002](tasks.md#t-002--provider-abstracto--claudecliprovider) — `Provider` abstracto + `ClaudeCLIProvider`
- [T-003](tasks.md#t-003--script-de-prueba-manual-end-to-end-del-provider) — Script de prueba manual end-to-end del provider
- Más adelante: módulo `soda.cli` con subcomandos (`soda init`, `soda start`, `soda close`), plantillas reales de los 6 archivos de `_persistence`, y activar la instalación con `pipx install -e` una vez exista el entry point.

## Historial de hitos

### 2026-07-23 — Bootstrap del repositorio y esqueleto del paquete `soda`

Proyecto inicializado desde cero: Git local, remoto GitHub enlazado y push inicial
(commit `987864b`). Se resolvió un bloqueo de privacidad de email de GitHub configurando
`user.email` local del repo con la dirección `noreply`. Se creó y verificó la estructura
base instalable del paquete `soda` (T-001).
