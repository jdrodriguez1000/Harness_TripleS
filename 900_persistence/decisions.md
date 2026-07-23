# Decisions

## Índice

| Código | Título | Fecha |
|--------|--------|-------|
| [D-001](#d-001--nombre-del-paquete-y-producto-soda) | Nombre del paquete y producto: `soda` | 2026-07-23 |
| [D-002](#d-002--cli-unica-con-subcomandos-en-vez-de-comandos-separados) | CLI única con subcomandos en vez de comandos separados | 2026-07-23 |
| [D-003](#d-003--modelo-de-distribución-instalación-única-vía-pipx) | Modelo de distribución: instalación única vía `pipx` | 2026-07-23 |
| [D-004](#d-004--layout-src-en-vez-de-flat-layout) | Layout `src/` en vez de flat layout | 2026-07-23 |
| [D-005](#d-005--build-backend-hatchling-python-312-y-dependencias-mínimas) | Build backend hatchling, Python 3.12 y dependencias mínimas | 2026-07-23 |

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
