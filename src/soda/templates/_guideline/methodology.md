# Metodología de Construcción

> **Rol de este archivo.** Es **producto**: viaja con `soda` al proyecto destino y se instala en
> `_guideline/methodology.md`. Describe el **proceso** con el que se construyen las aplicaciones que el
> arnés ayuda a levantar. **No** es la metodología con la que se construye `soda` mismo — por eso habla
> de `_persistence/`, `_context/` y `_increments/`, que son carpetas del proyecto destino.
>
> **Es la primera mitad de un documento en dos archivos.** La segunda —agentes, evaluación,
> observabilidad— es **`_guideline/agents-and-evaluation.md`**. La numeración de secciones es
> **continua y única entre los dos**: `§8` significa lo mismo se lea donde se lea, así que ninguna
> referencia cruzada dice en qué archivo está. El mapa está en la Tabla de contenidos.

Esta es la **metodología de ingeniería** del harness: **cómo** un proyecto construye sus entregables
de forma disciplinada, trazable y reanudable, avanzando siempre **de menos a más** —desde un
**prototipo de alto nivel** hasta un **MVP** y luego hasta un **producto evolucionado/final**.

> **Alcance: desarrollo de software.** Esta metodología cubre **exclusivamente proyectos de desarrollo
> de software**. Es **agnóstica de lenguaje, stack y framework** —no de dominio—: la espina de fases,
> los gates, el bucle TDD y la trazabilidad son los mismos en cualquier tecnología, y la tecnología
> concreta se elige al instanciar el proyecto.

> **Relación con el comportamiento.** Este documento desarrolla el *cómo* del trabajo; el *qué* del
> comportamiento de los agentes lo fija `_guideline/principles.md` (principios de diseño `P-`,
> requisitos y guía de operación `E-`, reglas de ejecución `NC-`). Ante conflicto sobre **cómo debe
> comportarse un agente**, manda `principles.md`; sobre **qué paso viene ahora en el flujo**, manda este
> documento.

---
---

## Tabla de contenidos

La navegación interna del documento usa los **números de sección** (§X) que aparecen en las
referencias cruzadas.

| § | Sección | Qué contiene |
|---|---|---|
| **0** | Propósito y Mapa de fuentes | Para qué existe la metodología y qué tiene dueño canónico fuera de aquí |
| 0.3 | · **Estado de aplicación** | **Qué rige hoy, qué está `[DIFERIDO]` y qué está `[PENDIENTE]`** — leer antes que nada |
| **1** | Los dos ejes del trabajo | Madurez (macro) e incremento (micro): el avance "de menos a más" |
| **2** | La espina de un incremento | Las seis fases y su relación con los 11 pasos de §3 |
| **3** | Ciclo de vida de un incremento | Las 11 fases del ciclo, gates humanos y trazabilidad end-to-end |
| 3.1 | · Observabilidad y evaluación del ciclo TDD | → **`agents-and-evaluation.md`** |
| **4** | Estadios de madurez | Prototipo de alto nivel → MVP → Producto final |
| 4.1 | · Los tres estadios | Objetivo, alcance y criterio de salida de cada uno |
| 4.2 | · Deseabilidad vs factibilidad | Los dos tipos de prototipo y cuál va primero |
| 4.3 | · Disciplina de alcance | Control de *scope creep* en el prototipo |
| 4.4 | · Frontera Prototipo → MVP | El gate de madurez duro |
| 4.5 | · Reglas de transición | Cómo se pasa de un estadio al siguiente |
| **5** | Agentes: arquetipos y responsabilidades | → **`agents-and-evaluation.md`** (con §5.1, §5.2, §5.3) |
| **6** | Gates de aprobación | Gates automáticos vs humanos (GateKeeper) |
| **7** | Persistencia y trazabilidad | Filesystem como fuente de verdad; Single Writer |
| 7.1 | · Estado por incremento (`state.yaml`) `[PENDIENTE]` | Máquina de estado de la slice: espina única + capas etiquetadas |
| 7.2 | · Traza de ejecución (`_trace/trace.md`) `[PENDIENTE]` | Log único append-only: qué hizo cada agente y en qué orden |
| **8** | Evaluación | → **`agents-and-evaluation.md`** (con §8.1) |
| **9** | Evolución del harness | → **`agents-and-evaluation.md`** |
| **10** | Observabilidad y conformidad | → **`agents-and-evaluation.md`** (con §10.1, §10.2) |
| — | Apéndice | Estándares de ingeniería (commits, ramas, modelos) |

> **División ejecutada.** El gatillo que este documento se fijó —dividir si el bloque de
> **agentes/evaluación/observabilidad** (§3.1, §5, §8, §9, §10) superaba por sí solo ~250 líneas— se
> disparó al alcanzar ese bloque **418 líneas**. Las secciones se movieron a
> **`agents-and-evaluation.md`** conservando su número, y aquí quedó un **puntero** en el lugar de cada
> una con lo que sigue rigiendo aunque no se lea el otro archivo. Este archivo cubre el **proceso**:
> §0–§4, §6, §7 y el Apéndice.

---
---

## 0. Propósito y Mapa de fuentes

### 0.1 Propósito
Reducir el espacio de decisiones probabilísticas durante la **construcción**, encuadrando el trabajo
de los agentes mediante **prototipado, especificación, planificación, validación y verificación
independiente**, con el **humano como GateKeeper**. Primero se **explora** (prototipo de alto nivel) y
luego se **consolida** el entregable, incremento a incremento.

### 0.2 Mapa de fuentes de verdad
Este documento no repite lo que ya tiene dueño canónico:

| Tema | Fuente canónica |
|---|---|
| Comportamiento de agentes: Principios (P), Estándares (E), Normas (NC) | **`_guideline/principles.md`** |
| Marco operativo: memoria, protocolos de sesión, portabilidad | **`AGENTS.md`** (+ `CLAUDE.md`/`GEMINI.md` como punteros) |
| Contexto declarativo del proyecto (metadatos, repo, memoria activa) | **`_context/project.yaml`** |
| Estado y avance entre sesiones | **`_persistence/`** |
| Plantillas de artefactos por incremento | **`_templates/`** (convención) |
| **Metodología de construcción** — proceso: flujo, madurez, gates, persistencia | **este documento** (§0–§4, §6, §7) |
| **Agentes y evaluación** — arquetipos, evaluación del producto, observabilidad | **`_guideline/agents-and-evaluation.md`** (§3.1, §5, §8, §9, §10) |

> **Comportamiento vinculante.** Todo agente que participe en la construcción cumple los P/E/NC de
> `principles.md` como restricciones inmutables.

> **Ojo con el estado de estas fuentes.** Varias de las de arriba **todavía no existen**; cuáles y qué
> hacer sin ellas está en §0.3.

#### Dos clases de dato, dos fuentes (regla de procedencia)

Lo que un agente escribe en un artefacto sale **siempre** de una de estas dos clases, y **cada clase
tiene una sola fuente legítima**:

| Clase | Qué incluye | Fuente única | Si falta |
|---|---|---|---|
| **Metadatos del proyecto** | nombre, descripción, repositorio, rama, memoria activa | **`_context/project.yaml`** | `<no declarado>` |
| **Contenido del cliente** | objetivo, hipótesis de valor, actores, flujos, métricas, exclusiones | **`client_brief.*` / la entrevista** | se **pregunta**, no se deduce |

**Las fuentes no se cruzan.** El nombre del proyecto no se "deduce" del brief aunque aparezca algo
parecido; una métrica de éxito no sale de `project.yaml` aunque estuviera ahí. **Y ningún valor se
rellena con la otra clase ni con una suposición:** si la fuente que le corresponde no lo trae, se
escribe `<no declarado>` o se pregunta al humano (NC-001).

**Todo valor viaja con su procedencia declarada** —qué archivo y dónde—, y la procedencia se **verifica
antes de afirmarla**: decir "esto viene del brief" sin haberlo comprobado es fabricar, aunque el valor
resulte ser correcto.

> **Motivo (fallo observado).** Un agente afirmó que el nombre del proyecto "venía del brief"; la palabra no
> aparecía ni una vez en el brief — estaba en `project.yaml`, que no era insumo declarado de ninguna
> etapa. El valor era correcto y la atribución falsa, que es el caso **más difícil de detectar**: una
> fuente inventada *suena* respaldada y nadie la audita. Fabricar la **fuente** de un dato es tan grave
> como fabricar el dato.

### 0.3 Estado de aplicación: qué rige hoy y qué no

No todo lo que este documento describe está disponible el día que se instala. Escribir en el mismo
presente lo que **rige ahora** y lo que **está por llegar** es un fallo con consecuencia conocida: un
agente lee una regla, asume que puede cumplirla, y al no encontrar la pieza que necesita **inventa un
sustituto o la ignora en silencio** — y nadie se entera.

**Toda regla de los tres documentos de `_guideline/` tiene uno de tres estados.** Esta sección es la
definición única de la taxonomía: `agents-and-evaluation.md` y `principles.md` §0.5 la importan por
referencia y no la redefinen.

| Marca | Significa | Qué hace el agente |
|---|---|---|
| *(sin marca)* | **NORMATIVO** — rige desde la primera sesión, sin infraestructura previa | Lo cumple. Incumplirlo es una violación. |
| **`[DIFERIDO]`** | Decisión consciente de **no adoptarlo aún**. Lleva **gatillo de adopción** | No lo monta. Si el gatillo se dispara, lo **propone al humano** — no lo adopta por su cuenta. |
| **`[PENDIENTE]`** | Se quiere, pero **depende de una pieza que el harness aún no entrega**. Nombra la pieza | No lo simula ni finge cumplirlo: **declara la ausencia** y aplica el sustituto de la tabla de abajo. |

> **Las dos marcas no son intercambiables.** *Diferido* es «decidimos que todavía no vale la pena»: se
> revierte con **evidencia** de que su ausencia degrada la calidad (E-004, §9). *Pendiente* es «lo
> queremos y falta construirlo»: se revierte **entregando la pieza**. Confundirlas lleva a montar lo que
> se decidió no montar, y a esperar lo que nadie está construyendo.

**El núcleo normativo** —lo que rige el primer día, sin depender de nada— son los **gates humanos**
(§3, §6), la **independencia** del evaluador (§3, §8), **definición antes de construir** y el bucle
**RED → GREEN → REFACTOR** (§2, §3.1), la **vertical slice** (§1), los **estadios de madurez** y su
disciplina de alcance (§4), **Single Writer** y el filesystem como fuente de verdad (§7), la **regla de
procedencia** (§0.2) y **mínima complejidad** (§9).

**Piezas que `_guideline/` asume y que hoy no se entregan.** Es el **inventario único**: todo lo
marcado `[PENDIENTE]` en cualquiera de los tres documentos cuelga de esta tabla, y la última columna es
lo que se hace mientras tanto:

| Pieza ausente | La invocan | Qué se hace sin ella |
|---|---|---|
| `AGENTS.md` | §0.2, §5 | El marco operativo lo suple el archivo de instrucciones del proyecto (`CLAUDE.md` o equivalente) |
| `_context/project.yaml` | §0.2, §5.1 | Los metadatos de proyecto se escriben `<no declarado>` — **nunca** se deducen del brief (§0.2) |
| `_templates/` (plantillas de artefacto, `state_temp.yaml`, `trace_temp.md`) | §5.1, §7.1, §7.2, §10.1 | No hay contrato de forma verificable por diff: el agente estructura según la spec y **lo hace constar**; de §5.1 no aplican los pasos 1–2, sí los pasos 0, 3 y 4 |
| `_increments/<id>/state.yaml` | §7.1 | El estado del incremento se lleva en `_persistence/tasks.md`, en narrativa |
| **Motor de traza** + `_trace/trace.md` | §7.2, §10, `principles.md` §5 | La conformidad **no es auditable**: manda el gate humano, y ningún check del tipo «¿leyó antes de escribir?» puede afirmarse |
| `_tools/conformance.sh` | §10.2 | Igual que la anterior |
| `_guideline/git-protocol.md` | §7, Apéndice | Rige la convención de commits del Apéndice; el procedimiento detallado lo decide la sesión |
| **Flota de arquetipos** (§5) | §3, §5 | La sesión principal ejecuta los 11 pasos con subagentes ad hoc, **respetando independencia, contexto fresco y gates** — normativos aunque el arquetipo con nombre propio no exista |
| **Medición de ocupación de contexto** expuesta por el arnés | `principles.md` §5 (E-002) | El disparador de compactación se evalúa por señales externas; no hay umbral numérico y el corte lo decide el orquestador o el humano |
| **Medición del consumo de cuota** de una sesión típica | `principles.md` §5 (E-014) | El presupuesto de sesión rige sin número: cuánta holgura es "suficiente" es juicio del orquestador |

> **Honestidad de estado.** Que una pieza esté `[PENDIENTE]` no relaja la regla que la acompaña: relaja
> su **verificabilidad**. Sin traza no se puede *demostrar* que se siguió el procedimiento, pero
> seguirlo sigue siendo obligatorio.

---
---

## 1. Los dos ejes del trabajo

El avance "de menos a más" ocurre en **dos ejes simultáneos**:

- **Eje de MADUREZ (macro).** El producto atraviesa estadios: **Prototipo de alto nivel → MVP →
  Producto Evolucionado/Final**. Cada estadio tiene un **objetivo**, un **alcance acotado** y un
  **criterio de salida** (gate de madurez). No se salta de estadio sin cruzarlo. El **Prototipo**
  valida —barato y desechable— *qué vale la pena construir* (deseabilidad y/o factibilidad, §4.2); el
  **MVP** es el primer producto **funcional**.
- **Eje de INCREMENTO (micro).** Dentro de cada estadio, el trabajo se construye por **slices
  verticales** —una funcionalidad o experimento completo de punta a punta— y no por capas
  horizontales. Cada slice se valida antes de ampliar (NC-004, *Tracer Bullet*).

```
MADUREZ →   Prototipo ───▶ MVP ───▶ Evolucionado/Final
              │              │              │
INCREMENTO ▼  slice·slice    slice·slice…   slice·slice…      (cada slice = un ciclo de vida, §3)
```

> El eje de madurez responde *¿cuánto producto?*; el eje de incremento responde *¿cómo se construye
> cada trozo?*. La disciplina de gates aplica a ambos: gate de **incremento** (§3) y gate de
> **madurez** (§4).

---
---

## 2. La espina de un incremento

Todo incremento recorre la misma **espina de seis fases**, sea cual sea el lenguaje o el stack:

`Definir → Especificar → Planear → Construir → Verificar → Integrar`

| Fase | Qué produce |
|---|---|
| Definir | Intención + historias de la funcionalidad |
| Especificar | Criterios de aceptación verificables |
| Planear | Tareas + casos de test |
| Construir | Bucle TDD (RED → GREEN → REFACTOR) |
| Verificar | Auditoría independiente contra la spec |
| Integrar | PR → gate humano → merge |

> **Seis fases y once pasos son el mismo ciclo.** La espina nombra el **trabajo**; los **11 pasos** de
> §3 son ese mismo trabajo desglosado para ejecutarlo: añaden el acuerdo de intención y el contrato al
> principio, intercalan los **gates humanos** y separan la auditoría en integración y verificación. No
> son dos modelos —§3 es la forma operativa de esta espina, y es la que gobierna el `state.yaml` (§7.1)—.

**"Terminado" = test en verde** (NC-005, *orientado a comportamiento*). El criterio de terminación es
mecánico y binario: nunca depende del juicio de un agente sobre su propio trabajo.

> **El prototipo ocurre una sola vez, al inicio.** "Prototipar" **no** es una fase del ciclo de
> incremento: cuando se construye una vertical slice se produce **funcionalidad real** (con tests) que
> se suma poco a poco, no un prototipo. La exploración desechable —el spike/PoC/maqueta que informa el
> enfoque— pertenece al **estadio de Prototipo de alto nivel** (§4), que se hace una vez antes del MVP;
> cuando el riesgo dominante es técnico, esa exploración es el **prototipo de factibilidad** (§4.2). El
> prototipo no se copia-pega al entregable: la spec y el ciclo de construcción reescriben la lógica con
> rigor; queda como artefacto de referencia/demo.

> **Spikes de excepción (opcional).** En un incremento avanzado puede surgir una incógnita técnica
> nueva que amerite un *spike* desechable puntual. Es una **herramienta de excepción**, no una fase del
> flujo: su código no se gradúa; solo informa la spec de ese incremento.

---
---

## 3. Ciclo de vida de un incremento

Ninguna pieza se produce sin una definición previa, una spec aprobada y un mecanismo de
validación. El ciclo de un incremento, con sus **gates humanos** (🚦):

| # | Fase | Responsable (arquetipo, §5) | Artefacto / Acción |
|---|---|---|---|
| 1 | Definir el incremento | Humano + sesión principal | Acuerdo de intención + rama de trabajo |
| 2 | Escribir el contrato | Sesión principal | Contrato del incremento ("estrella polar" / definición de Terminado) |
| 3 | Definir | *Definidor* | Definición (necesidades / historias) |
| 4 | Especificar | *Especificador* | Spec con criterios de aceptación verificables |
| 5 | **🚦 Gate humano** | Humano | Aprueba / rechaza la spec |
| 6 | Planear | *Planificador* | Plan de tareas + casos de test |
| 7 | **🚦 Gate humano** | Humano | Aprueba / rechaza el plan |
| 8 | Construir | *Probador* → *Implementador* → *Refactorizador* | RED → GREEN → REFACTOR |
| 9 | Probar integración | *Integrador de pruebas* (contexto fresco) | Suite end-to-end con fixtures |
| 10 | Verificar | *Verificador* (contexto fresco) | Veredicto CONFORME / NO CONFORME + matriz de trazabilidad |
| 11 | Integrar | Sesión principal abre PR → **🚦 Gate humano** | El humano prueba y **mergea** |

**Invariantes:**
- **Independencia (P-001/P-003):** quien construye ≠ quien prueba ≠ quien verifica; los evaluadores corren
  en **contexto fresco**.
- **Definición antes de construir:** el criterio de éxito (el test que falla) se escribe **antes** del
  código.
- **Gates humanos** en spec, plan y cierre (P-005). **Ningún agente cruza un gate por su
  cuenta**: lo hace la sesión principal tras la aprobación humana.

**Trazabilidad end-to-end.** La columna vertebral que une los artefactos:
```
necesidad/historia  →  criterio de aceptación  →  tarea de plan  →  evidencia en verificación
```
Toda necesidad debe estar cubierta por ≥1 criterio; todo criterio por ≥1 tarea; todo criterio con
evidencia en la verificación. Si algo no traza, el artefacto está incompleto.

> **`[DIFERIDO]` Bandas.** *Gatillo de adopción: un incremento resulta demasiado grande para un solo
> ciclo.* Por defecto, un incremento = una construcción completa. Endurecer por pasadas sucesivas
> (*bandas*) está disponible como modelo, pero no se monta hasta que el gatillo se dispare.

### 3.1 Observabilidad y evaluación del ciclo TDD (código) → `agents-and-evaluation.md`

En **código bajo TDD** el test cumple tres papeles a la vez —contrato de forma, evidencia de
conformidad y oráculo de evaluación—, así que observabilidad y evaluación se entrelazan en el bucle.
El desarrollo completo, con los checks de conformidad de cada fase (RED/GREEN/REFACTOR), vive en
**`agents-and-evaluation.md` §3.1**.

> Lo único que hay que retener aquí: el check imposible de falsear es que **hubo una corrida en ROJO
> antes de la corrida en VERDE**. Si el test pasó a la primera, no se siguió TDD → **NO CONFORME**,
> aunque el resultado final sea verde.

---

## 4. Estadios de madurez

Cada estadio del eje macro tiene **objetivo**, **alcance** y **criterio de salida**. Se construye con
los incrementos de §3, aplicando mínima complejidad (E-004).

### 4.1 Los tres estadios

| Estadio | Objetivo | Alcance típico | Criterio de salida (gate de madurez) |
|---|---|---|---|
| **Prototipo de alto nivel** | Validar **qué vale la pena construir** antes de invertir en ingeniería (deseabilidad y/o factibilidad, §4.2) | Simulación/experimento acotado al **camino feliz**; **desechable**, sin robustez | Hipótesis validada con evidencia + **feature freeze** (§4.4) |
| **MVP** | Primer producto **funcional** usable end-to-end que entrega valor real mínimo | **Tracer Bullet a nivel de proyecto**: slice fino que atraviesa todas las capas (datos → salida/interfaz) | El slice funciona de punta a punta y valida uso/retención real |
| **Producto evolucionado/final** | **Endurecer y ampliar**: robustez, más features, escala, calidad | Incrementos sucesivos sobre la base del MVP | Cumple los criterios de calidad/negocio definidos para "final" |

### 4.2 Dos tipos de prototipo: deseabilidad vs factibilidad

El estadio de prototipo mitiga **riesgo**, y hay dos riesgos distintos → dos tipos de prototipo:

| | **Prototipo de DESEABILIDAD** | **Prototipo de FACTIBILIDAD** |
|---|---|---|
| Pregunta | *¿Deberíamos construir esto? ¿Lo quieren?* | *¿Podemos construirlo? ¿Funciona el enfoque?* |
| Riesgo que mitiga | De **mercado / producto** | De **técnica / ejecución** |
| Forma típica | Simulación **no funcional**: mockups, wireframes, no-code, "mago de Oz" | **Spike / PoC**: lógica real de la parte riesgosa, código desechable |
| Mide | Comprensión del valor, interés, usabilidad, disposición a usar/pagar | Que el algoritmo/enfoque/integración produce resultados aceptables |
| Backend / datos | Falsos / simulados | Reales o de muestra, pero **sin robustez** |

**Cuál hacer primero** depende del **riesgo dominante** y del tipo de proyecto:
- Domina el **riesgo de mercado** (¿alguien lo quiere?) → **deseabilidad primero**.
- Domina el **riesgo técnico** (¿es siquiera posible?) → **factibilidad primero**: una integración
  externa incierta, un algoritmo no trivial, un requisito de rendimiento o escala en el límite. Si el
  enfoque no se sostiene, lo demás no importa.
- A menudo se hacen **ambos en secuencia**: deseabilidad → factibilidad → MVP.

> **Frontera humano ↔ agente.** No corre por *deseabilidad vs factibilidad*, sino por **juicio vs.
> materialización**. El **juicio de producto/UX** —qué validar, qué se le muestra a quién, con qué
> usuarios se prueba— y la **simulación viva del "mago de Oz"** (una persona finge en vivo ser el
> sistema/backend) son **humanos**: el humano es dueño del riesgo de mercado. La **materialización** del
> prototipo la construye el **agente** *Prototipador* (§5), guiado por el `discovery.md` y la dirección
> de diseño del humano: **wireframes / mockups / HTML clicable** cuando domina la **deseabilidad**, o
> **spike / PoC** cuando domina la **factibilidad** (§3 del discovery). El **descubrimiento**
> también lo conduce un agente (el *Descubridor*). Regla de medio: el prototipo se materializa en la
> **tecnología más barata que valide la hipótesis** (p. ej. un HTML clicable que simula una pantalla de
> móvil), que **no** tiene por qué ser el medio del producto final. El prototipo es **desechable**:
> informa, no se "gradúa" a producción — los tests y el Tracer Bullet aplican **desde el MVP** (por eso
> el prototipo no contradice NC-004/NC-005).

### 4.3 Disciplina de alcance en el prototipo (control de *scope creep*)

El prototipo se mantiene barato y rápido con reglas estrictas de alcance:

- **Timebox + Feature Freeze.** Duración tope acordada; al cerrarla se **congela** y se pasa al MVP;
  las mejoras estéticas/secundarias se posponen.
- **Camino feliz (Core Path).** Solo los flujos críticos que validan la hipótesis de valor; lo demás
  se excluye.
- **Roles/actores priorizados (taxonomía por defecto).** Clasificar los actores por criticidad y
  diseñar **solo el camino feliz** de cada uno. Como *lente de elicitación* —un **piso, no un techo**—
  todo sistema se examina contra al menos **tres arquetipos de actor**, definidos por su relación con el
  valor (no por su cargo):
  - **Generador** — origina el valor central por su **uso directo**; es la **razón de ser** (sin
    generador no hay sistema).
  - **Operador** — **aprovecha lo que el generador produce** y lo convierte en valor posterior.
  - **Administrador** — **sostiene y gobierna** el sistema (altas/bajas, configuración, métricas) sin
    participar del flujo de valor central.

  **Siempre se pregunta por los tres**, pero pueden **faltar o colapsar** (sin operador, sin
  administrador, ambos en un mismo actor, o los tres concentrados en el generador); se declara
  explícitamente cuáles existen. **Prioridad no lineal:** el camino feliz del **generador es obligatorio**
  para arrancar el proyecto; los de operador y administrador se construyen **bajo demanda** (cuando la
  aplicación lo requiera —días o semanas después—), **no** en una secuencia inmediata tras el generador.
  Esto es el **por defecto**, no una regla que el Prototipador infiera por su cuenta: el `discovery.md`
  declara el conjunto exacto de actores a construir como **campo cerrado** en §5, y el
  Prototipador obedece ese campo — incluido el caso en que el humano prioriza explícitamente operador
  o administrador junto al generador para una ronda concreta.
- **Artefactos segmentados por audiencia (*split*).** En vez de un artefacto monolítico, generar
  validaciones **especializadas por audiencia** (p. ej. una para pruebas de usabilidad con usuarios y
  otra como herramienta de demostración para clientes/aliados), cada una enfocada en su objetivo.
- **Criterio de salida cuantitativo (Gatekeeper).** Definir de antemano una métrica de éxito medible
  (p. ej. "N usuarios objetivo, ≥X% de comprensión del valor") que decide si se pasa al MVP.
- **Exclusiones explícitas.** Declarar por escrito qué queda fuera del prototipo, para evitar la
  parálisis por diseño.

> El "camino feliz" son los flujos que materializan la **hipótesis de valor central**: en una aplicación
> con interfaz, los flujos de UI; en un servicio o una CLI, la secuencia de llamadas que entrega el valor.

> **El generador basta para avanzar.** Un proyecto puede pasar al **MVP con solo el camino feliz del
> generador** construido; las funciones de operador y administrador se cubren provisionalmente con un
> **humano que simula la aplicación (mago de Oz, §4.2)** hasta que su construcción se justifique. Es
> **mínima complejidad (E-004)** aplicada al eje de actores: se construye el actor crítico y se **difiere o
> simula** el resto, sin bloquear la entrega de valor.

### 4.4 Frontera Prototipo → MVP

- El paso de estadio es un **gate de madurez duro**: se cruza solo con la **evidencia** del criterio de
  salida y una **decisión humana** (P-005), y se **congela** el prototipo (feature freeze).
- El **MVP es el primer entregable funcional**: se construye como **Tracer Bullet a nivel de proyecto**
  (slice fino end-to-end, §4.1) siguiendo el ciclo de incremento de §3 (ya con tests/evaluación).
- El prototipo **no se copia-pega** al MVP: queda como **referencia/demo**; la spec y el ciclo de
  construcción reescriben la lógica con rigor (§2).

### 4.5 Reglas de transición
- No se avanza de estadio sin cruzar su **gate de madurez** (decisión humana, P-005).
- Cada estadio **reutiliza** los artefactos del anterior; el prototipo no se "gradúa" tal cual.
- **Mínima complejidad** (E-004, NC-002): se añade estructura/robustez solo cuando el estadio lo exige, no
  antes.

---
---

## 5. Agentes: arquetipos y responsabilidades → `agents-and-evaluation.md`

Los **arquetipos** que ejecutan los pasos de §3 —quiénes son, qué produce cada uno, el contrato de
trabajo de un constructor de entregables y las reglas de instanciación de la flota— viven en
**`agents-and-evaluation.md` §5**. La flota está **`[PENDIENTE]`** (§0.3).

> Lo que rige aquí, y no depende de que exista ningún arquetipo: **quien construye ≠ quien prueba ≠
> quien verifica**, los evaluadores corren en **contexto fresco** (P-001/P-003) y **ningún agente cruza
> un gate por su cuenta** (P-005).

---

## 6. Gates de aprobación

- **Automáticos:** criterios técnicos medibles (tests en verde, cobertura de criterios de aceptación,
  linters y complejidad).
- **Humanos (GateKeeper):** el humano aprueba intención y alcance. Gates humanos obligatorios
  **tras la spec**, **tras el plan**, en el **cierre del incremento** y en cada **transición de estadio
  de madurez** (incluida la aprobación del Prototipo de alto nivel, §4.4).

> **La automatización llega hasta el PR; el harness nunca integra a la rama principal por su cuenta.**

---
---

## 7. Persistencia y trazabilidad

La fuente de verdad reside en el **filesystem**, no en la memoria de los agentes: así se **reanuda**
el trabajo entre sesiones y ante fallos (E-001, E-005).

| Capa | Dónde | Qué guarda |
|---|---|---|
| Proyecto / sesión | `_persistence/` | `progress` · `tasks` · `lessons` · `decisions` · `assumptions` · `constraints` (narrativa, Markdown) |
| Por incremento | `state.yaml` de la slice (§7.1; ruta física según la instanciación) | máquina de estado del ciclo de vida (§3), estructurada |

- **Dos naturalezas distintas.** `_persistence/` es **narrativa** (bitácora en Markdown con `## Índice`);
  el estado de una slice es **estructurado** (§7.1), porque lo lee el orquestador para reanudar y los
  checks de conformidad (§10) para auditar.
- **Single Writer Rule:** cada archivo de estado tiene **un único responsable de escritura** para evitar
  condiciones de carrera. El `state.yaml` lo escribe **solo el orquestador**; cada **artefacto**
  (`definition`, `spec`, `plan`, código, tests) lo escribe **solo su agente productor**.
- **Excepción única: la traza de ejecución** (`_trace/trace.md`, §7.2). Es un **log compartido de
  solo-anexado** al que escriben **todos** los agentes de etapa, y es la **única** excepción admitida a
  Single Writer. No reintroduce condiciones de carrera porque (a) los agentes de etapa corren **uno a
  la vez**, con gates humanos en medio, y (b) la operación permitida es **anexar**, nunca modificar ni
  reordenar lo ya escrito. Un agente que **reescriba** filas ajenas —o propias— sí viola la regla.
- **Git y reanudación:** commit por etapa con prefijo convencional; el **push** se hace en el cierre
  de sesión (agente *closer*, respetando `auto_push`). Para retomar un incremento interrumpido, la
  sesión principal lee su `state.yaml` y reinvoca al arquetipo del paso pendiente con contexto fresco.
  El **procedimiento operativo** (bootstrap del repo, commit por etapa, convención del mensaje y
  límites) vive en **`_guideline/git-protocol.md`** — **`[PENDIENTE]`**, aún no se entrega: mientras
  tanto rige la convención de commits del Apéndice y el resto lo decide la sesión.

### 7.1 `[PENDIENTE]` Estado por incremento (`state.yaml`)

> *Requiere: `_templates/state_temp.yaml` y la convención `_increments/`.* Sin ellos, el estado del
> incremento se lleva en `_persistence/tasks.md` en narrativa. Lo que **no** se relaja: el ciclo sigue
> siendo **uno solo, end-to-end, sin bifurcar por capa**, y los gates siguen dejando constancia escrita
> de qué se decidió y contra qué alternativa.

Cada vertical slice lleva su propia **máquina de estado del ciclo de vida** (§3) en un archivo
**estructurado** (convención `state.yaml`; la ruta física se fija al instanciar). Reglas del modelo:

- **Espina única de 11 pasos.** `state.yaml` modela **un solo** ciclo §3 (Definir → … → Integrar) con el
  estado de cada paso y el resultado de cada gate. **No se bifurca por capa técnica:** una slice es
  end-to-end (NC-004). Si algo es valor de usuario independiente end-to-end, es **otra slice** (otro
  `state.yaml`), no una rama de esta.
- **Las capas viven dentro de Construir.** Frontend, backend y base de datos **no son pasos**: son
  *tareas etiquetadas* dentro de Planear/Construir. Cada caso/tarea lleva su `component` (fe/be/db) y su
  `owner` (agente de la flota, §5.3). `definition`/`spec`/`plan` son **unificadas** para toda la slice;
  el plan las descompone por capa.
- **Construir es un bucle TDD.** Cada caso recorre **RED → GREEN → REFACTOR** (§5.3); el campo `stage`
  marca la fase. Un caso de **caracterización** (`caracterizacion: true`) es un test que **nace verde**:
  fija conducta ya existente, no dirige código nuevo.
- **Las revisiones transversales viven en Verificar.** Calidad de código (§5.2) y seguridad (su
  hermano) son **entradas de evaluación** en Verificar, no pasos nuevos. La seguridad-*comportamiento*
  es un **criterio de aceptación** en la spec.
- **Los gates dejan traza.** Cada gate humano (pasos 5, 7 y 11) registra `status`
  (`PENDIENTE`/`APROBADO`/`APROBADO_CON_CAMBIOS`/`RECHAZADO`), `fecha` y una lista de `resoluciones`
  —qué se decidió y **contra** qué alternativa—. **Ningún agente cruza un gate** (P-005).
- **Escritor único:** el **orquestador** (§7). Los subagentes reportan; él verifica (§10) y transcribe.

**Carpeta del incremento.** El `state.yaml` no vive suelto: encabeza la carpeta de la slice, junto a los
artefactos que produce cada paso. La numeración de carpeta (`_increments/`, `NNN_…`) es convención del
proyecto, no obligación (ver nota del Apéndice); lo fijo es la **relación** entre el estado y sus
artefactos hermanos:

```
_increments/<id>/
├── state.yaml         ← máquina de estado (único que escribe el orquestador)
├── contract.md        ← paso 2 · estrella polar / definición de Terminado
├── definition.md      ← paso 3
├── spec.md            ← paso 4  (gate paso 5)
├── plan.md            ← paso 6  (gate paso 7)
└── verification.md    ← paso 10 · veredicto + matriz de trazabilidad
```

**Plantilla.** La forma completa (espina de 11 pasos, gate reutilizable, bucle TDD en Construir y
evaluadores en Verificar) vive en **`_templates/state_temp.yaml`**: se copia a `_increments/<id>/state.yaml`
al abrir el incremento y se rellena. Estructura esencial:

```yaml
meta:      { incremento: "<id>", rama: "<rama-git>", estado_global: in_progress, paso_actual: 8 }
pasos:                     # espina §3 — un solo ciclo, sin bifurcar por capa (NC-004)
  5_gate_spec: { status: done, gate: { status: APROBADO_CON_CAMBIOS, fecha: "<f>", resoluciones: [
    { punto: "<qué>", decision: "<qué se resolvió>", contra: "<alternativa descartada>" } ] } }
  8_construir: { status: in_progress }
construir:                 # paso 8 — bucle TDD; capas = tareas etiquetadas
  cases:
    - { id: 1, ca: [CA-01], component: backend,  owner: implementador, stage: green,   caracterizacion: false }
    - { id: 7, ca: [CA-10], component: frontend, owner: implementador, stage: pending, caracterizacion: false }
verificar:                 # paso 10 — evaluadores transversales (por E-004)
  spec_verifier:   { status: pending }
  code_review:     { status: pending, archetype: code-reviewer }      # §5.2
  security_review: { status: pending, archetype: security-reviewer }  # hermano de §5.2
```

> **Reanudación y git.** El `state.yaml` vive en la **rama de la slice**; al integrar se **archiva** como
> registro de trazabilidad. Es el mecanismo que hace **reanudable** un incremento interrumpido (§7).

### 7.2 `[PENDIENTE]` Traza de ejecución (`_trace/trace.md`)

> *Requiere: `_templates/trace_temp.md`.* Sin la plantilla no se instancia la traza, y sin traza los
> checks de conformidad del tipo «¿leyó antes de escribir?» son **inverificables** (§0.3): manda el gate
> humano. El idioma de anexado de abajo es la forma acordada para cuando la plantilla exista.

Archivo **único por proyecto**, append-only, con una fila por evento y el agente declarado en cada
fila. Responde *¿qué hizo el agente, y en qué orden?* **dentro de la carpeta del proyecto**, sin
depender del transcript de la herramienta que lo ejecutó —que es propietario, no versionable y se
pierde al cerrar la sesión—. Su forma la fija **`_templates/trace_temp.md`**.

- **Un solo archivo, no uno por agente.** El **orden global entre etapas es en sí mismo la evidencia**:
  checks como *"¿el writer leyó el extracto antes de escribir el discovery?"* solo son verificables si
  todas las etapas viven en una misma secuencia. Un archivo por agente además se rompe cuando un mismo
  agente se invoca varias veces a lo largo del proyecto.
- **Se anexa durante la ejecución, no al cerrar.** Una traza redactada al final es el agente
  reconstruyendo de memoria, no un registro. Si el agente muere a mitad, lo ya anexado sigue siendo
  evidencia válida.
- **Es autodeclarada, y por tanto evidencia débil.** El auto-reporte es narrativa, no evidencia (§10).
  Su valor no es ser confiable sino ser **contrastable**: cada fila se coteja contra `git log` y los
  artefactos reales, y una traza que los contradiga es, ella misma, la señal del fallo.
- **Regla de admisión:** si el agente **no puede observarlo**, no va en la traza. Pedirle un dato que no
  conoce —su consumo de tokens, la hora del reloj— produce un número inventado con apariencia de
  medido, que es peor que no tenerlo. Los timestamps se obtienen con `date`, no los escribe el modelo.
- **Única excepción a Single Writer (§7):** escriben todos los agentes de etapa, y solo **anexando**.

> Habilita los checks de conformidad hoy **inverificables** por falta de traza (los del tipo *"¿leyó
> antes de escribir?"*). La capa de evidencia **dura** —producida por hooks, no autodeclarada— es
> posterior y reutiliza este mismo formato y esta misma carpeta.
>
> **Observabilidad ≠ evaluación.** La traza registra *qué pasó*; no dice si estuvo **bien**. Eso lo
> deciden la conformidad (§10), los oráculos de trazabilidad y el gate humano (§8).

**Cómo se anexa (idioma canónico).** Con `Bash` y redirección `>>`, **nunca** con `Edit`: editar exige
releer el archivo entero y abre la puerta a reescribir lo ya anexado, que es justo lo que la regla
prohíbe. El timestamp lo pone `date`, no el modelo. Los skills usan este idioma; no lo reimplementan:

```sh
# 1) ABRIR la traza si aún no existe (idempotente: la crea el primer agente que corra).
#    Instancia desde la plantilla (§5.1) recortando de la cabecera al encabezado de la
#    tabla — deja fuera las filas de EJEMPLO y las notas del final.
[ -f _trace/trace.md ] || { mkdir -p _trace
  sed -n '/^# Traza/,/^|---/p' _templates/trace_temp.md > _trace/trace.md; }
#    Tras crearla: rellenar los <marcadores> de Meta y borrar el comentario guía
#    de "## Registro" (única edición legítima del archivo; ver abajo).

# 2) SIGUIENTE número de secuencia: se cuenta, no se recuerda.
n=$(( $(grep -c '^| [0-9][0-9][0-9] |' _trace/trace.md) + 1 ))

# 3) ANEXAR una fila (agente y modelo son los propios, del frontmatter).
printf '| %03d | %s | %s | %s | %s | %s | %s |\n' \
  "$n" "onboarding-reader" "sonnet" "read" "_context/client_brief.md" "12 páginas" "$(date +%H:%M:%S)" \
  >> _trace/trace.md
```

El número de secuencia es **global y correlativo**, y se **cuenta del archivo** en cada anexado: un
agente no puede llevarlo de memoria porque no sabe cuántas filas escribieron los anteriores. Si dos
filas comparten número, el orden dejó de ser legible y la traza pierde su única función.

**Única edición legítima:** rellenar la Meta al crear el archivo. Desde la primera fila anexada, el
archivo es de solo-anexado para todos.

---
---

## 8, 9 y 10 → `agents-and-evaluation.md`

- **§8 Evaluación** — cómo se evalúa el **producto** según la naturaleza de la salida (código vs
  entregables documentales), y el flujo de evaluación de tres capas.
- **§9 Evolución del harness** — mínima complejidad (E-004) y prueba de remoción.
- **§10 Observabilidad y conformidad** — cómo se audita el **comportamiento** de los agentes.
  **`[PENDIENTE]`**: requiere el motor de traza (§7.2).

> **Evaluación ≠ observabilidad.** §8 pregunta *¿el trabajo quedó bien hecho?*; §10 pregunta *¿siguió el
> procedimiento?*. Un agente puede ser **CONFORME** y aun así entregar un mal producto.

---

## Apéndice: Estándares de Ingeniería

- **Convención de commits:** `tipo(<incremento>): descripción`
  (`feat`/`spec`/`plan`/`test`/`refactor`/`verify`/`chore`/`docs`).
  Procedimiento y mapeo etapa→mensaje en `_guideline/git-protocol.md` (`[PENDIENTE]`, §0.3). La
  **convención de arriba rige igual** sin él.
- **Estrategia de ramas:** cada incremento se construye en su rama; la integración a la rama principal
  es **solo vía Pull Request** tras el veredicto CONFORME. **El harness nunca integra a la principal
  por su cuenta** (detalle en `AGENTS.md` / `CLAUDE.md`).
- **Selección de modelos (P-006, escalamiento proporcional):** el modelo se ajusta a la exigencia de la
  tarea —modelos más capaces para definición/spec/plan/verificación (razonamiento crítico), modelos de
  ejecución para construir/probar, y modelos ligeros para tareas simples (p. ej. el *starter* de
  sesión). Las asignaciones concretas se fijan al instanciar el proyecto.

> **Pendiente de instanciación.** La estructura física de carpetas para artefactos por incremento y
> plantillas (`_templates/`, `[PENDIENTE]` §0.3) se concreta al montar un proyecto real; esta
> metodología define el **flujo, los gates, los artefactos y los roles**, no una numeración de carpetas
> fija.
