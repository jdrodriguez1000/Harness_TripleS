# Constraints

## Índice

| Código | Título |
|--------|--------|
| [C-001](#c-001--separación-estricta-entre-construir-el-harness-y-usar-el-harness) | Separación estricta entre "construir el harness" y "usar el harness" |
| [C-002](#c-002--_persistence-siempre-relativo-a-un-project_root-explícito) | `_persistence/` siempre relativo a un `project_root` explícito |
| [C-003](#c-003--frontera-física-del-repo-srcsoda-es-el-producto-la-raíz-es-andamiaje) | Frontera física del repo: `src/soda/` es el producto, la raíz es andamiaje |
| [C-004](#c-004--no-confundir-agentes-del-harness-con-agentes-de-claude-code-de-este-repo) | No confundir agentes del harness con agentes de Claude Code de este repo |
| [C-005](#c-005--la-instalación-editable-acopla-el-comando-global-soda-al-repo-en-disco) | La instalación editable acopla el comando global `soda` al repo en disco |
| [C-006](#c-006--la-cuota-de-suscripción-es-el-presupuesto-real-no-el-dinero) | La cuota de suscripción es el presupuesto real, no el dinero |

## Detalle de restricciones

### C-001 — Separación estricta entre "construir el harness" y "usar el harness"

- **Tipo:** Técnica
- **Descripción:** Existen dos mundos separados: (1) construir el harness, que es este repo, con memoria en `900_persistence/`; (2) usar el harness sobre una app destino, que es otro repo, con memoria en `_persistence/`.
- **Impacto:** El código de `src/soda/` nunca debe leer ni escribir `900_persistence/`. Si lo hace, es un bug a corregir de inmediato.
- **Origen:** Definido explícitamente al planificar la arquitectura durante esta sesión.

### C-002 — `_persistence/` siempre relativo a un `project_root` explícito

- **Tipo:** Técnica
- **Descripción:** La carpeta `_persistence/` de un proyecto destino nunca es una ruta fija ni se asume relativa al directorio actual de ejecución implícitamente.
- **Impacto:** Toda función del harness que trabaje con `_persistence/` debe recibir `project_root` como parámetro explícito.
- **Origen:** Definido al diseñar el modelo de distribución (ver D-003).

### C-003 — Frontera física del repo: `src/soda/` es el producto, la raíz es andamiaje

- **Tipo:** Técnica
- **Descripción:** Todo lo que está bajo `src/soda/` es el producto que se distribuye; todo lo que está en la raíz del repo (`900_persistence/`, `idea.md`, `CLAUDE.md`, `transcript.md`) es andamiaje de construcción y no forma parte del paquete instalable.
- **Impacto:** Ningún archivo de la raíz debe importarse ni empaquetarse dentro de `soda`; mantiene limpia la distinción entre el proyecto que construye y el producto construido.
- **Origen:** Definido al establecer la estructura del proyecto (T-001).

### C-004 — No confundir agentes del harness con agentes de Claude Code de este repo

- **Tipo:** Técnica
- **Descripción:** Los agentes que el harness `soda` orquestará en tiempo de ejecución (`sesion-starter`, `agent-worker`, `sesion-closer`) son conceptualmente distintos de los agentes de Claude Code usados para construir este repo (`harness-starter`, `harness-closer`), aunque cumplan roles análogos.
- **Impacto:** Evitar mezclar nombres, prompts o configuración entre ambos conjuntos de agentes al diseñar `soda`.
- **Origen:** Aclarado explícitamente durante la planificación de esta sesión.

### C-005 — La instalación editable acopla el comando global `soda` al repo en disco

- **Tipo:** Entorno
- **Descripción:** `soda` está instalado con `pipx install -e <ruta del repo>` (D-003, T-006). Si `Harness_TripleS` se mueve, renombra o borra, el comando `soda` deja de funcionar. Además, un bug introducido en `src/soda/cli.py` afecta de inmediato al `soda` instalado globalmente.
- **Impacto:** Es el precio correcto durante la construcción del harness. La suite de tests es la única protección contra regresiones que se propagan de inmediato al comando global. Cuando el harness se estabilice, conviene reinstalar sin `-e` para desacoplarlo.
- **Origen:** Verificación manual de T-006, confirmando que `soda.cli.__file__` resuelve dentro de `src/` del repo.

### C-006 — La cuota de suscripción es el presupuesto real, no el dinero

- **Tipo:** Suscripción
- **Descripción:** El arnés corre sobre suscripciones (CLIs oficiales como `claude`, `codex`), no sobre API de pago por token (`idea.md`). El recurso escaso es la ventana de cuota con límite de tasa, no el costo en tokens.
- **Impacto:** Toda decisión de diseño que multiplique invocaciones de agente (por ejemplo, paralelizar subagentes) debe justificarse contra la cuota disponible, no contra el costo en tokens. Obligó a reescribir E-007 de `principles.md` (paralelización condicionada, default secuencial) y a crear E-014 (presupuesto de sesión y límite de pérdida).
- **Origen:** Detectado al revisar E-007 de `principles.md` durante T-007: la recomendación original de 3-5 subagentes en paralelo venía de research sobre API de pago por token, incompatible con el modelo de suscripción del proyecto.
