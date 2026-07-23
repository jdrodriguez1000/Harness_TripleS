# Metodología de Construcción

> **Rol de este archivo.** Es **producto**: viaja con `soda` al proyecto destino y se instala en
> `_guideline/methodology.md`. Describe el **proceso** con el que se construyen las aplicaciones que el
> arnés ayuda a levantar. **No** es la metodología con la que se construye `soda` mismo — por eso habla
> de `_persistence/`, `_context/` y `_increments/`, que son carpetas del proyecto destino.

Esta es la **metodología de ingeniería** del harness: **cómo** un proyecto construye sus entregables
de forma disciplinada, trazable y reanudable, avanzando siempre **de menos a más** —desde un
**prototipo de alto nivel** hasta un **MVP** y luego hasta un **producto evolucionado/final**.

> **Agnóstica.** No asume dominio, lenguaje, stack ni framework. Cubre dos familias de proyecto:
> **(1) Desarrollo de software** y **(2) Ciencia de datos / Machine Learning**, con una **espina
> común** y adaptaciones por tipo.

> **Relación con el comportamiento.** Este documento desarrolla el *cómo* del trabajo; el *qué* del
> comportamiento de los agentes lo fija `_guideline/principles.md` (principios de diseño `P-`,
> requisitos y guía de operación `E-`, reglas de ejecución `NC-`). Ante conflicto sobre **cómo debe
> comportarse un agente**, manda `principles.md`; sobre **qué paso viene ahora en el flujo**, manda este
> documento.

---

## Tabla de contenidos

La navegación interna del documento usa los **números de sección** (§X) que aparecen en las
referencias cruzadas.

| § | Sección | Qué contiene |
|---|---|---|
| **0** | Propósito y Mapa de fuentes | Para qué existe la metodología y qué tiene dueño canónico fuera de aquí |
| **1** | Los dos ejes del trabajo | Madurez (macro) e incremento (micro): el avance "de menos a más" |
| **2** | Tipos de proyecto y su adaptación | Espina común de fases; software vs Ciencia de datos/ML |
| **3** | Ciclo de vida de un incremento | Las 11 fases del ciclo, gates humanos y trazabilidad end-to-end |
| 3.1 | · Observabilidad y evaluación del ciclo TDD | Cómo el test es contrato, evidencia y oráculo en código |
| **4** | Estadios de madurez | Prototipo de alto nivel → MVP → Producto final |
| 4.1 | · Los tres estadios | Objetivo, alcance y criterio de salida de cada uno |
| 4.2 | · Deseabilidad vs factibilidad | Los dos tipos de prototipo y cuál va primero |
| 4.3 | · Disciplina de alcance | Control de *scope creep* en el prototipo |
| 4.4 | · Frontera Prototipo → MVP | El gate de madurez duro |
| 4.5 | · Reglas de transición | Cómo se pasa de un estadio al siguiente |
| **5** | Agentes: arquetipos y responsabilidades | Familias de arquetipos y coordinación (flota agnóstica) |
| 5.1 | · Contrato de un constructor de entregables | Plantilla → instancia → relleno → gate |
| 5.2 | · Revisor de código | Evaluador independiente de calidad/seguridad (adoptar por E-004) |
| 5.3 | · Especialización de flota | Frontend/backend y otras variantes de instanciación |
| **6** | Gates de aprobación | Gates automáticos vs humanos (GateKeeper) |
| **7** | Persistencia y trazabilidad | Filesystem como fuente de verdad; Single Writer |
| 7.1 | · Estado por incremento (`state.yaml`) | Máquina de estado de la slice: espina única + capas etiquetadas |
| 7.2 | · Traza de ejecución (`_trace/trace.md`) | Log único append-only: qué hizo cada agente y en qué orden |
| **8** | Evaluación | Cómo se evalúa el **producto** según la naturaleza de la salida |
| 8.1 | · Flujo de evaluación (ejemplo) | Las tres capas de evaluación de un entregable |
| **9** | Evolución del harness | Mínima complejidad (E-004) y prueba de remoción |
| **10** | Observabilidad y conformidad | Cómo se audita el **comportamiento** de los agentes |
| 10.1 | · Flujo end-to-end (ejemplo) | Recorrido desde la invocación hasta la conformidad |
| — | Apéndice | Estándares de ingeniería (commits, ramas, modelos) |

> **Gatillo de división (pendiente).** Mientras el documento quepa cómodo en un archivo, se mantiene
> unido con esta tabla. Si el bloque de **agentes/evaluación/observabilidad** (§5, §8, §9, §10, +§3.1)
> supera por sí solo ~250 líneas, o si casi siempre editas solo ese bloque, **dividir** en
> `methodology.md` (proceso: §1–§4, §6, §7) + `agents-and-evaluation.md` (§5, §8, §9, §10; §3.1 se
> mueve con un puntero desde §3).

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
| **Metodología de construcción** (este archivo): flujo, madurez, gates, roles, evaluación | **este documento** |

> **Comportamiento vinculante.** Todo agente que participe en la construcción cumple los P/E/NC de
> `principles.md` como restricciones inmutables.

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

## 2. Tipos de proyecto y su adaptación

Los dos tipos comparten la **misma espina** de fases; cambian los artefactos y la naturaleza de la
validación.

**Espina común (un incremento):**
`Definir → Especificar → Planear → Construir → Verificar → Integrar`

| Fase | Software | Ciencia de datos / ML |
|---|---|---|
| Definir | Intención + historias de la funcionalidad | Pregunta/objetivo, métrica de éxito, disponibilidad de datos |
| Especificar | Criterios de aceptación verificables | Criterios + **umbrales de métrica** y protocolo de evaluación |
| Planear | Tareas + casos de test | Tareas + pipeline de datos/entrenamiento + casos de evaluación |
| Construir | Bucle TDD (RED → GREEN → REFACTOR) | Pipeline determinista con tests **+ entrenamiento/evaluación** de la parte probabilística |
| Verificar | Auditoría independiente contra la spec | Auditoría independiente: métricas alcanzan umbrales + consistencia |
| Integrar | PR → gate humano → merge | PR → gate humano → merge (modelo/artefacto versionado) |

**Diferencia clave (NC-005, "orientado a comportamiento").**
- En **software determinista**, "Terminado" = **test en verde**.
- En **ML/probabilístico**, "Terminado" combina **tests** (para el código determinista: pipeline,
  features, I/O) **con un arnés de evaluación** que mide **umbrales de métrica** sobre un conjunto de
  validación, corrido **N veces** para medir consistencia (no una sola pasada). La parte que no es
  verificable mecánicamente se somete a evaluación calibrada (E-003, §8).

> **El prototipo ocurre una sola vez, al inicio.** "Prototipar" **no** es una fase del ciclo de
> incremento: cuando se construye una vertical slice se produce **funcionalidad real** (con
> tests/evaluación) que se suma poco a poco, no un prototipo. La exploración desechable
> —notebook/EDA/PoC que informa el enfoque— pertenece al **estadio de Prototipo de alto nivel** (§4),
> que se hace una vez antes del MVP. En DS/ML, esa exploración es el **prototipo de factibilidad**
> (§4.2). El notebook/PoC no se copia-pega al entregable: la spec y el ciclo de construcción reescriben
> la lógica con rigor; queda como artefacto de referencia/demo.

> **Spikes de excepción (opcional).** En un incremento avanzado puede surgir una incógnita técnica
> nueva que amerite un *spike* desechable puntual. Es una **herramienta de excepción**, no una fase del
> flujo: su código no se gradúa; solo informa la spec de ese incremento.

---

## 3. Ciclo de vida de un incremento

Ninguna pieza se produce sin una definición previa, una spec aprobada y un mecanismo de
validación. El ciclo de un incremento, con sus **gates humanos** (🚦):

| # | Fase | Responsable (arquetipo, §5) | Artefacto / Acción |
|---|---|---|---|
| 1 | Definir el incremento | Humano + sesión principal | Acuerdo de intención + rama de trabajo |
| 2 | Escribir el contrato | Sesión principal | Contrato del incremento ("estrella polar" / definición de Terminado) |
| 3 | Definir | *Definidor* | Definición (necesidades / historias) |
| 4 | Especificar | *Especificador* | Spec con criterios verificables (y umbrales, en ML) |
| 5 | **🚦 Gate humano** | Humano | Aprueba / rechaza la spec |
| 6 | Planear | *Planificador* | Plan de tareas + casos de test/evaluación |
| 7 | **🚦 Gate humano** | Humano | Aprueba / rechaza el plan |
| 8 | Construir | *Probador* → *Implementador* → *Refactorizador* | RED → GREEN → REFACTOR (+ evaluación en ML) |
| 9 | Probar integración | *Integrador de pruebas* (contexto fresco) | Suite end-to-end con fixtures |
| 10 | Verificar | *Verificador* (contexto fresco) | Veredicto CONFORME / NO CONFORME + matriz de trazabilidad |
| 11 | Integrar | Sesión principal abre PR → **🚦 Gate humano** | El humano prueba y **mergea** |

**Invariantes:**
- **Independencia (P-001/P-003):** quien construye ≠ quien prueba ≠ quien verifica; los evaluadores corren
  en **contexto fresco**.
- **Definición antes de construir:** el criterio de éxito (test/umbral que falla) se escribe **antes**
  del código o del modelo.
- **Gates humanos** en spec, plan y cierre (P-005). **Ningún agente cruza un gate por su
  cuenta**: lo hace la sesión principal tras la aprobación humana.

**Trazabilidad end-to-end.** La columna vertebral que une los artefactos:
```
necesidad/historia  →  criterio de aceptación  →  tarea de plan  →  evidencia en verificación
```
Toda necesidad debe estar cubierta por ≥1 criterio; todo criterio por ≥1 tarea; todo criterio con
evidencia en la verificación. Si algo no traza, el artefacto está incompleto.

> **Modelo por defecto: sin bandas.** Un incremento = una construcción completa. Endurecer por
> pasadas sucesivas (*bandas*) queda **disponible pero diferido**: se adopta solo si un incremento
> resulta demasiado grande para un ciclo.

### 3.1 Observabilidad y evaluación del ciclo TDD (código)

En **código bajo TDD**, el **test cumple tres papeles a la vez** —contrato de forma, evidencia de
conformidad y oráculo de evaluación—, así que observabilidad (§10) y evaluación (§8) **se entrelazan**
en el bucle en vez de ir por capas separadas. Intervienen tres agentes en cadena, distintos entre sí
(P-001/P-003): *Probador* (RED), *Implementador* (GREEN), *Refactorizador* (REFACTOR); luego, en **contexto
fresco**, *Integrador de pruebas* y *Verificador*.

**Observabilidad — la disciplina TDD es verificable por la traza:**
```
 PROBADOR (RED)             escribe test → CORRE → ✗ FALLA
   conformidad: el test FALLA antes de existir código · NO tocó código de producción
 IMPLEMENTADOR (GREEN)      escribe código → CORRE → ✓ PASA
   conformidad: el test ahora PASA · solo tocó producción (no el test) · alcance mínimo · Single Writer
 REFACTORIZADOR (REFACTOR)  limpia → CORRE → ✓ SIGUE VERDE
   conformidad: verde antes y después · sin nuevos tests ni cambio de comportamiento
```
El check imposible de falsear: **hubo una corrida en ROJO antes de la corrida en VERDE**. Si el test
pasó a la primera, no se siguió TDD → **NO CONFORME** aunque el resultado final sea verde.

**Evaluación — el test es el oráculo objetivo (sin juez LLM):**
```
 1. DETERMINISTA: suite en VERDE · cada criterio → ≥1 test (matriz §3) · linters + complejidad (refactor)
 2. ¿LOS TESTS VALEN?  mutation testing / DEFECTOS SEMBRADOS: inyecta bugs → ¿la suite se pone roja?
       (equivalente en código a "calibrar el juez" de los documentos, §8.1)
 3. INTEGRACIÓN:  Integrador de pruebas (contexto fresco) — ¿lo nuevo rompe lo existente?
 4. VERIFICACIÓN: Verificador (contexto fresco) — CONFORME/NO CONFORME vs spec + matriz de trazabilidad
 5. GATE HUMANO 🚦 — el humano prueba y mergea (solo vía PR, P-005)
```
Un **test verde puede mentir** (un test que no afirma nada pasa siempre); por eso la **capa 2**
(mutantes) evalúa que los tests **valgan**, no solo que existan.

> **Documento vs código.** En documentos el contrato de forma es la **plantilla** (§5.1) y el oráculo es
> un **juez LLM** calibrado (semántico); en código el contrato es el **test que falla** y el oráculo son
> los **tests** (binario, objetivo, sin LLM). En ambos, "**defectos sembrados**" valida al evaluador
> (juez LLM ↔ mutation testing) y la **independencia** (evaluador ≠ constructor, contexto fresco) es
> idéntica.

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
| Forma típica | Simulación **no funcional**: mockups, wireframes, no-code, "mago de Oz" | **Spike / notebook / PoC**: lógica real sobre datos sintéticos o de muestra, código desechable |
| Mide | Comprensión del valor, interés, usabilidad, disposición a usar/pagar | Que el algoritmo/enfoque/integración produce resultados aceptables |
| Backend / datos | Falsos / simulados | Reales o de muestra, pero **sin robustez** |

**Cuál hacer primero** depende del **riesgo dominante** y del tipo de proyecto:
- Domina el **riesgo de mercado** (¿alguien lo quiere?) → **deseabilidad primero**.
- Domina el **riesgo técnico** (¿es siquiera posible?) → **factibilidad primero**. En **Ciencia de
  datos/ML** suele mandar aquí: si un modelo no alcanza utilidad mínima, lo demás no importa.
- A menudo se hacen **ambos en secuencia**: deseabilidad → factibilidad → MVP.

> **Frontera humano ↔ agente.** No corre por *deseabilidad vs factibilidad*, sino por **juicio vs.
> materialización**. El **juicio de producto/UX** —qué validar, qué se le muestra a quién, con qué
> usuarios se prueba— y la **simulación viva del "mago de Oz"** (una persona finge en vivo ser el
> sistema/backend) son **humanos**: el humano es dueño del riesgo de mercado. La **materialización** del
> prototipo la construye el **agente** *Prototipador* (§5), guiado por el `discovery.md` y la dirección
> de diseño del humano: **wireframes / mockups / HTML clicable** cuando domina la **deseabilidad**, o
> **spike / notebook / PoC** cuando domina la **factibilidad** (§3 del discovery). El **descubrimiento**
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
  (p. ej. "N usuarios objetivo, ≥X% de comprensión del valor" o "el baseline alcanza ≥Y de métrica")
  que decide si se pasa al MVP.
- **Exclusiones explícitas.** Declarar por escrito qué queda fuera del prototipo, para evitar la
  parálisis por diseño.

> Agnóstico por tipo de proyecto: en software/producto el "camino feliz" son flujos de UI; en DS/ML es
> la **hipótesis de valor central** (p. ej. que la señal existe en los datos y un baseline la captura).

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

## 5. Agentes: arquetipos y responsabilidades

La metodología define **arquetipos** (roles agnósticos), no una flota concreta. La flota real —con
nombres y modelos— se define **al instanciar cada proyecto**, respetando estos arquetipos.

**Dos familias, según lo que producen** (como planteó el encuadre del proyecto):

- **Constructores de ENTREGABLES** — producen artefactos de definición/documentación:
  *Definidor* (definición/historias), *Especificador* (spec + criterios/umbrales), *Planificador*
  (plan de tareas), *Verificador* (auditoría contra la spec).
- **Constructores y evaluadores de CÓDIGO / artefactos técnicos** — producen y validan lo ejecutable:
  *Probador* (tests que fallan primero), *Implementador* (código mínimo), *Refactorizador* (limpieza
  sin cambiar comportamiento), *Integrador de pruebas* (suite end-to-end), *Revisor de código*
  (evaluación independiente de calidad/seguridad/diseño — §5.2).

> **Descubridor (estadio de Prototipo, fuera del ciclo de incremento).** Antes de prototipar, alguien
> tiene que **preguntar** —pero solo lo que aún no se sabe—. El *Descubridor* elicita qué quiere el
> cliente, los **stakeholders**, los **actores** (taxonomía de §4.3) y el **camino feliz de cada actor**.
> Se distingue del resto en que su insumo principal no es un artefacto previo sino el **diálogo con el
> humano**. **Aprovecha lo ya escrito (crítico):** cuando el cliente entrega un **documento** describiendo
> lo que quiere, el Descubridor lo **lee primero** y entrevista **solo los huecos**; repreguntar lo que el
> cliente ya redactó le dice que no lo leyeron y quema el timebox. Sin documento, la entrevista se conduce
> completa. **Alcance acotado (crítico):** busca un entendimiento **rápido y suficiente para arrancar**
> —lo justo para prototipar el camino feliz del **generador**—, no un relevamiento exhaustivo; evita el
> cuestionario infinito que lleva a la **parálisis por diseño** (§4.3). **Produce** un *entregable de
> descubrimiento* (actores clasificados con ausencias/colapsos declarados, camino feliz por actor,
> stakeholders y el **Gatekeeper** de §4.3), que es el **insumo del Prototipador**. Como constructor de
> entregables sigue el contrato de §5.1 y es **observable y evaluable** (perfil de conformidad §10 +
> rúbrica §8).

> **Realización concreta del Descubridor (instanciación).** En el harness base el Descubridor se
> materializa como **tres agentes** que separan *ingerir*, *elicitar* y *estructurar* (E-004):
>
> 1. **`onboarding-reader`** *(condicional)* — busca `_context/client_brief.*`, el documento con que el
>    cliente describe lo que quiere. Si existe, extrae **citas textuales** mapeadas a las áreas §1–§10 en
>    `document_extract.md`, con una **tabla de cobertura** (*cubierta / parcial / ausente / n/a* —
>    `n/a` para las áreas que no vienen del cliente, canónicamente §3, que deduce el Descubridor) y las
>    **ambigüedades** que no resuelve a propósito. Si no existe, **no produce nada** y el flujo sigue por
>    la entrevista completa: la ausencia de documento es el caso normal, no un error.
> 2. **`onboarding-interviewer`** — conduce la entrevista y registra crudo cada pregunta/respuesta en
>    `interview_document.md` (append-only, por eso la entrevista es **reanudable**: el log es el estado).
>    Si hay extracto, su tabla de cobertura **fija la agenda**: solo pregunta las áreas *parciales* y
>    *ausentes* más las ambigüedades.
> 3. **`onboarding-writer`** — sintetiza el `discovery.md` estructurado a partir de **ambos** artefactos
>    (log + extracto, cuando este existe). Ante conflicto **manda la entrevista** —es posterior y el
>    humano hablaba conociendo su documento—, pero la discrepancia se **declara**, no se silencia.
>
> El reader y el writer son **subagentes autónomos** (su insumo es un archivo; el reader solo dialoga en
> un turno único de confirmación); el interviewer es **interactivo**. Cada artefacto tiene **un solo
> autor**, y el material del documento **no se duplica** en el log: por eso el writer necesita leer los
> dos. La flota real puede fundir o renombrar los tres al instanciar (§5).
>
> **Flujo del estadio:** `_context/client_brief.*` → *(reader)* → `document_extract.md` →
> *(interviewer)* → `interview_document.md` → *(writer)* → `discovery.md` → **Prototipador**. Salvo el
> brief —que aporta el humano en `_context/`—, todos viven en **`_prototype/`**. La **condición de
> entrada** al estadio se deduce de qué artefactos existen: la comprueba el protocolo de inicio, y el
> encadenamiento está documentado en `AGENTS.md` (*Arranque de proyecto*).

> **Prototipador (fuera del ciclo de incremento).** El **estadio de Prototipo de alto nivel** (§4) usa
> un *Prototipador* que toma el *entregable de descubrimiento* y **materializa** el **camino feliz
> desechable** del actor —**wireframe/mockup/HTML clicable** si domina la deseabilidad, o
> **spike/notebook/PoC** si domina la factibilidad (§3 del discovery)—, en el **medio de ese actor**
> (app, web, notebook…) declarado en §6 del discovery y con la tecnología **más barata que valide la
> hipótesis**. **Empieza por el generador**; los demás actores, bajo demanda (§4.3). El **juicio de UX y
> el mago de Oz** siguen siendo humanos (§4.2). Es un arquetipo del **estadio inicial**, desechable, **no
> del ciclo de incremento**: las slices se construyen con los arquetipos de arriba, no con el
> Prototipador. Orden del estadio: **Descubridor → Prototipador**.

**Coordinación:**
- **Sesión principal (orquestador):** analiza el objetivo, fija la estrategia, guarda su plan en la
  memoria persistente **antes** de crear subagentes (E-012), y crea cada subagente con una consigna
  clara (objetivo, formato de salida, herramientas, límites).
- **Agentes de sesión:** *starter* (protocolo de inicio, solo lectura) y *closer* (protocolo de
  cierre, escribe memoria) — ya provistos por el harness.

**Independencia (P-001/P-003):** el arquetipo que **genera** nunca es el que **evalúa**; verificación e
integración corren en **contexto fresco**.

> La correspondencia con el ciclo de §3: *Especificador*→el *Qué* · *Probador*→criterio de éxito
> (RED) · *Implementador*→código mínimo (GREEN) · *Refactorizador*→limpieza (REFACTOR) ·
> *Integrador de pruebas* + *Verificador*→auditoría independiente (VERIFY).

### 5.1 Contrato de trabajo de un constructor de entregables

Todo arquetipo que produce un **entregable documental** (definición, spec, plan, informe) opera bajo el
mismo **contrato de trabajo**: un paso de **entrada** (verificar el insumo) y cuatro de **producción**. Es agnóstico al proyecto: las rutas físicas concretas se
fijan al instanciar (ver nota final). Este contrato es lo que hace **observable y verificable** a un
agente que, por ser probabilístico, no se puede dar por bueno solo con su palabra.

0. **Verificar el insumo antes de consumirlo (contrato de entrada).** Todo artefacto producido por una
   etapa anterior declara su estado en la cabecera (`Estado: borrador | cerrado`, y donde exista,
   `Confirmado por el humano: no | sí`). Antes de trabajar sobre él, el agente **lee ese campo** y, si
   el insumo viene **en borrador o sin confirmar**, lo **avisa explícitamente** en su primera
   comunicación y lo **hace constar en el artefacto que produzca**. No bloquea ni corrige por su
   cuenta: la autoridad para decidir si se sigue es del humano (NC-001). Un insumo sin campo de estado
   legible se trata como **no confirmado**.
   **`_context/project.yaml` es insumo declarado de todo agente que escriba metadatos de proyecto**
   (nombre, descripción, repo): se lee en este paso, no se busca a mitad de camino ni se sustituye por
   una deducción. Rige la **regla de procedencia** (§0.2): cada valor de salida sale de la fuente de su
   clase y declara cuál es.
1. **Plantilla = contrato de forma.** Cada tipo de entregable tiene un **esqueleto versionado** en
   `_templates/` (una plantilla por artefacto: definición, spec, plan…). El esqueleto fija la
   **estructura obligatoria** —secciones, campos, marcadores de relleno—: es el contrato de *forma*. El
   *qué* de contenido lo fijan el contrato del incremento y la spec.
2. **Instanciar antes de rellenar.** El agente **copia** el esqueleto a la ubicación de trabajo del
   incremento con el **nombre canónico** del artefacto — **nunca escribe desde cero**. Así todo
   artefacto **nace conforme** a su plantilla y la conformidad de estructura es verificable por **diff**
   contra el esqueleto.
3. **Rellenar sin alterar la estructura.** El agente completa/actualiza **solo el contenido** de las
   secciones; no reordena ni elimina la estructura. Rige **Single Writer** (§7): cada artefacto tiene
   **un único agente** responsable de su escritura.
4. **Reportar y ceder el gate.** Al terminar, el agente **informa** que terminó — **no cruza gates**. La
   sesión principal presenta el artefacto al **humano** para aprobación (P-005). El auto-reporte es
   *narrativa, no evidencia* (§10): lo que cuenta es la **traza + el artefacto**.

> **Ejemplo (definición).** Esqueleto de `definición` en `_templates/` → el *Definidor* lo **copia** como
> la definición del incremento en su ubicación de trabajo → **rellena** necesidades/historias respetando
> las secciones → **informa**; la sesión principal lo lleva al **gate humano**.

**Observabilidad y evaluación de este agente** (por ser **probabilístico**):
- **Traza por invocación (§10):** su secuencia de herramientas, entradas/salidas, tiempos y costo quedan
  registrados; es la fuente de verdad de *qué hizo*.
- **Perfil de conformidad determinista (§10):** checks automáticos sobre (traza + artefacto) que
  responden *¿siguió el procedimiento?* — p. ej.: **leyó** el contrato/insumos antes de escribir;
  **instanció** desde la plantilla (no desde cero); **respeta la estructura** del esqueleto (diff);
  **un solo `Write`** a su artefacto; **Single Writer** (no tocó artefactos ajenos).
- **Evaluación de calidad (§8):** *juez LLM* calibrado **solo** para el juicio **semántico** del
  contenido (¿las historias son correctas, completas y trazables?), offline y por lotes, cuando exista
  dataset de fixtures. **Conformidad (procedimiento) y calidad (contenido) se miden por separado.**

> El mismo contrato aplica, con su plantilla propia, a *Especificador* (spec), *Planificador* (plan) y
> al informe del *Verificador*. Los **constructores de código** (§5) no usan plantilla-esqueleto: su
> "forma" la fijan los tests y la spec, y su conformidad se audita igual vía traza (§10).

### 5.2 Revisor de código (evaluador independiente, adoptar por E-004)

Los tests son un oráculo **binario y objetivo**, pero no juzgan **diseño, seguridad, mantenibilidad ni
casos borde que nadie testeó** (un test verde puede mentir, §3.1). El *Revisor de código* cubre ese
hueco: es el **análogo en código del juez LLM** de los documentos —la capa de **juicio semántico** sobre
lo ejecutable.

- **Independencia (P-003):** corre en **contexto fresco**, distinto del que escribió el código.
- **División con el *Verificador*:** el *Verificador* pregunta *¿cumple la spec? ¿traza?* (binario,
  requisitos); el *Revisor* pregunta *¿es buen código, seguro, completo?* (cualitativo, diseño).
  Complementarios, no redundantes.
- **Sus hallazgos vuelven como tests, no como parches:** un caso borde detectado → se escribe un **test
  que falla** → reingresa al bucle TDD (§3.1). Así el hueco se cierra de forma permanente (§9), no con
  ediciones ad hoc.
- **Adopción por E-004 (§9):** no se monta de entrada. Primero lo hace el **gate humano** (revisión de PR);
  si la evidencia muestra defectos de calidad escapándose de forma sistemática, se **automatiza** como
  arquetipo. Se añade un componente cuando su ausencia degrada la calidad, no antes.

> **Hermano de seguridad.** La **revisión de seguridad** (auditoría de vulnerabilidades del código) es
> un evaluador **transversal análogo**, con las mismas reglas (independiente, contexto fresco, hallazgos
> → tests que fallan, adoptar por E-004). Puede ser el mismo *Revisor* con un perfil de seguridad o un
> arquetipo `security-reviewer` aparte. **La seguridad que es *comportamiento*** (autorización,
> validación de input) **no** es revisión: es un **criterio de aceptación** en la spec (§3, paso 4).

### 5.3 Especialización de flota (instanciación)

Los arquetipos son **agnósticos**; la **flota real** puede especializarlos al instanciar cuando el
*tooling* diverge lo suficiente. Caso típico: **frontend vs backend** en el trío TDD.

- **La disciplina no cambia:** RED → GREEN → REFACTOR, conformidad e independencia son idénticas en FE
  y BE. El **arquetipo** *Probador/Implementador/Refactorizador* es el mismo.
- **Lo que difiere es el tooling y la naturaleza del test:** BE → lógica determinista
  (unit/integración/contrato); FE → suma **regresión visual, interacción/DOM, accesibilidad**, con mayor
  superficie subjetiva que se apoya más en el *Revisor de código* / humano.
- **Regla E-004:** empezar con **un** trío TDD agnóstico; dividir en variantes FE/BE **solo con evidencia**
  de que un agente único rinde mal en ambos. La especialización es decisión de **flota**, no de
  arquetipo.

---

## 6. Gates de aprobación

- **Automáticos:** criterios técnicos medibles (tests en verde, cobertura de criterios, umbrales de
  métrica alcanzados).
- **Humanos (GateKeeper):** el humano aprueba intención y alcance. Gates humanos obligatorios
  **tras la spec**, **tras el plan**, en el **cierre del incremento** y en cada **transición de estadio
  de madurez** (incluida la aprobación del Prototipo de alto nivel, §4.4).

> **La automatización llega hasta el PR; el harness nunca integra a la rama principal por su cuenta.**

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
  límites) vive en **`_guideline/git-protocol.md`**; los skills lo aplican, no lo reimplementan.

### 7.1 Estado por incremento (`state.yaml`)

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

### 7.2 Traza de ejecución (`_trace/trace.md`)

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

## 8. Evaluación (dimensionada a la naturaleza de la salida)

La independencia del evaluador (P-003) se cumple corriendo verificación e integración en contextos
frescos, separados de quien construye.

| Tipo de salida | Naturaleza | Cómo se evalúa |
|---|---|---|
| **Código determinista** | Objetiva | **Tests** + **veredicto binario** (CONFORME/NO CONFORME) + matriz de trazabilidad |
| **Salida de ML / probabilística** | Cuantitativa/estadística | **Umbrales de métrica** sobre validación + **N corridas** midiendo consistencia (pass-rate + varianza) + rúbrica **0.0–1.0** calibrada (E-003) donde no haya métrica objetiva |
| **Entregables documentales** (spec, plan, informe) | Semiestructurada | **Conformidad determinista** (¿sigue la plantilla y traza?) + **juez LLM** calibrado solo donde el juicio es semántico |

**Evaluación temprana (E-009).** Al completar el primer componente funcional, evaluar una muestra de
**~20 casos representativos** (sintéticos, incl. **defectos sembrados** en ML); si la calidad es baja,
ajustar la spec **antes** de continuar.

> **Regla de corte:** la **conformidad determinista** (¿siguió el procedimiento?) es en vivo, por
> invocación, sin LLM; la **evaluación con juez** (¿el resultado es bueno?) es offline y por lotes, y
> solo arranca cuando la capa determinista es confiable y existe un dataset de fixtures.

### 8.1 Flujo de evaluación (ejemplo: la *definición* de una slice)

Paralelo al flujo de observabilidad (§10.1). **Observabilidad ≠ evaluación:** la observabilidad valida
*¿siguió el procedimiento?* (el *cómo*); la evaluación valida *¿el trabajo quedó bien hecho?* (el
*qué*). Un agente puede ser **CONFORME** y aun así entregar un mal producto — eso lo caza la evaluación.

Para un **entregable documental** (definición, spec, plan) la evaluación tiene **tres capas**, de más
barata a más cara; solo sube de capa lo que la capa anterior no puede juzgar:

```
 definición ya CONFORME (pasó observabilidad §10.1)
        │
        ▼
 1. CHECK DETERMINISTA DE COMPLETITUD/TRAZABILIDAD  (script, SIN LLM, en vivo)
       ✓ ninguna sección vacía / placeholder sin llenar
       ✓ cada necesidad → ≥1 criterio de aceptación (la matriz de trazabilidad cierra, §3)
    → si falla, no llega ni al juez ni al humano
        │
        ▼
 2. GATE HUMANO  🚦  (autoritativo para ESTA instancia, P-005)
        │
 ─ ─ ─ ─│─ ─ ─ ─ ─ ─ ─ ─  (en paralelo / offline, por lotes)  ─ ─ ─ ─ ─ ─ ─ ─
        ▼
 3. JUEZ DE CALIDAD (LLM) — agente DISTINTO del que escribió, contexto fresco (P-003)
       - corre sobre un DATASET DE FIXTURES (casos representativos + defectos sembrados)
       - rúbrica 0.0–1.0, N corridas midiendo consistencia (pass-rate + varianza)
       - CALIBRADO contra etiquetas humanas: solo se confía donde coincide con el humano
    → mide/regresiona al Definidor; NO bloquea esta instancia
```

**Cuatro invariantes de una evaluación confiable:**
- **Independencia (P-003):** quien evalúa **no** es quien escribió; corre en **contexto fresco**.
- **El juez LLM se calibra, no se cree:** se contrasta contra un **golden set** con etiquetas humanas y
  **defectos sembrados**; se usa **solo donde coincide** con el humano. Donde no, decide el humano.
- **Evaluación temprana (E-009):** al primer componente funcional, ~20 casos representativos; si la calidad
  es baja, se ajusta la **spec/prompt del agente** *antes* de continuar.
- **Retroalimenta al agente, no parchea el artefacto:** una mala nota se corrige en el **prompt/spec**
  del agente para que no reaparezca (§9); el gate humano puede rechazar la instancia y pedir
  re-generación.

> **Por tipo de salida (§8).** Cambia la **capa 2**: en **código determinista** son **tests** (veredicto
> binario); en **ML/probabilístico**, **umbrales de métrica + N corridas** midiendo consistencia. El
> gate humano y la independencia son iguales en los tres.

---

## 9. Evolución del harness (E-004: Mínima Complejidad)

El sistema parte del **mínimo viable** y evoluciona:
- Se construye con el **menor número de componentes** que satisfagan el trabajo (E-004, NC-002).
- Cada componente codifica una **suposición explícita** sobre una limitación del modelo; no se agrega
  sin evidencia de que su ausencia degrada la calidad.
- **Prueba de remoción periódica:** quitar un componente a la vez y medir el impacto; si la calidad no
  cae, se elimina y se registra la lección en `lessons.md`.
- Conforme los modelos mejoran, algunos componentes se vuelven obsoletos y emergen nuevas capacidades
  que justifican otros nuevos.

---

## 10. Observabilidad y conformidad de los agentes (E-013, P-008)

Mientras §8 evalúa **el producto**, aquí se observa y audita **el comportamiento de los agentes** que
lo construyen. Aplica a **todo subagente de construcción**.

- **Traza por invocación.** Cada subagente deja registro de su secuencia de herramientas,
  entradas/salidas, tiempos y costo (tokens). La traza es la fuente de verdad de *qué hizo*; el
  auto-reporte del agente es narrativa, **no** evidencia.
- **Conformidad determinista.** Las Reglas Vinculantes del prompt de cada agente se traducen en
  **checks verificables** sobre (traza + artefacto), evaluados automáticamente en cada invocación:
  responden *¿siguió el procedimiento?* (p. ej.: leyó el contrato antes de escribir; un solo `Write`
  al artefacto que le toca; respeta la plantilla; Single Writer).
- **Conformidad ≠ calidad.** La conformidad (procedimiento) se separa del juicio semántico de calidad
  (juez LLM, §8), que solo aplica donde la salida es probabilística y no verificable mecánicamente.

> Sin esta capa, un fallo de comportamiento solo se detecta por inspección humana ad hoc, nunca de
> forma sistemática. El motor de traza/conformidad se construye **una sola vez** y es genérico; a cada
> agente se le añade su **perfil de conformidad**.

### 10.1 Flujo end-to-end (ejemplo: construir la *definición* de una slice)

Quién interviene y en qué orden, desde la invocación hasta la observabilidad. Nota que **traza** y
**conformidad** son deterministas (harness/script, **sin LLM**); el **juez de calidad** es un agente
LLM que corre **aparte, offline**. Distinguen dos preguntas: *¿siguió el procedimiento?* (conformidad)
vs *¿el resultado es bueno?* (calidad).

```
 1. SESIÓN PRINCIPAL ──▶ invoca al DEFINIDOR (consigna: objetivo, plantilla, insumos)
                              │
 2. DEFINIDOR (LLM)           ▼
    a) LEE contrato del incremento + insumos
    b) COPIA  _templates/definición  →  definición del incremento (nombre canónico)
    c) RELLENA necesidades/historias respetando la estructura
    d) INFORMA "terminé"                       ◀── narrativa, NO evidencia
                              │
        (durante la corrida el harness graba la TRAZA: herramientas, I/O, tiempos, costo)
                              ▼
 3. CHECKER DE CONFORMIDAD (script determinista, SIN LLM) sobre (traza + artefacto):
       ✓ ¿leyó el contrato ANTES del primer Write?
       ✓ ¿instanció desde la plantilla (no desde cero)?
       ✓ ¿la estructura coincide con el esqueleto?  (diff)
       ✓ ¿un solo Write, y solo a SU artefacto?  (Single Writer)
    → veredicto: CONFORME / NO CONFORME
                              │
              ¿CONFORME? ── NO ──▶ corrida no confiable: la SESIÓN PRINCIPAL
                              │      re-invoca o escala (nunca va al gate humano
                              │      una corrida que no siguió el procedimiento)
                             SÍ
                              ▼
 4. SESIÓN PRINCIPAL ──▶ presenta la definición al  🚦 GATE HUMANO  (aprueba/rechaza, P-005)

 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  aparte, offline, por lotes  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
 5. JUEZ DE CALIDAD (LLM), cuando hay dataset de fixtures:
       evalúa lo SEMÁNTICO (¿historias correctas, completas, trazables?) con rúbrica
       calibrada. NO bloquea el gate; mide/mejora al Definidor y ajusta la spec (§8, §9).
```

Un agente puede ser **CONFORME pero de baja calidad** (siguió el procedimiento, historias flojas) o
**NO CONFORME** (ni copió la plantilla). Por eso conformidad y calidad se miden **por separado**. El
mismo flujo aplica, con su plantilla y su perfil de conformidad, a *Especificador*, *Planificador* y al
informe del *Verificador* (§5.1).

### 10.2 Capa barata de conformidad — `_tools/conformance.sh`

El flujo de §10.1 depende de un **motor de traza** que todavía no existe. Esperarlo dejó los perfiles
de conformidad escritos en los prompts durante tres corridas completas **sin que nadie los ejecutara
nunca**. La capa barata existe para cerrar ese hueco **ahora**, con lo que ya está disponible sin
instrumentar nada: los **artefactos en disco** y el **`git log`**.

**Qué comprueba** (sin traza, en segundos, sin LLM):

| Familia | Responde |
|---|---|
| **A · Artefactos** | procedencia del nombre de proyecto; marcadores sin sustituir; tabla de cobertura completa y con vocabulario válido; `n/a` y `parcial` justificados; coherencia estado↔confirmación; Gatekeeper con umbral cuantitativo; timebox declarado y coherente con el motivo de cierre |
| **B · Git** | rama actual coherente con `repository.default_branch` de `project.yaml`; commit por etapa con el mensaje canónico de `git-protocol.md` §4; artefacto materializado pero **sin confirmar**; doble escritura de la confirmación (borrador `[sin confirmar]` + commit de aprobación) |
| **C · Definiciones** | coherencia **agente↔skill**: si el skill que un agente invoca le exige confirmar en git, ese agente declara `Bash`; los skills referenciados existen |

**Qué NO comprueba, por diseño.** Todo lo que exige saber *en qué orden ocurrieron las cosas dentro de
una invocación*: «¿leyó el contrato antes de escribir?», «¿un solo `Write`?», «¿la confirmación fue
posterior al turno del humano?». Eso es **traza**, y sigue siendo el motor de §10.1. La capa barata no
lo sustituye: le quita de encima la parte que no lo necesitaba.

**Veredicto y autoridad.** Emite `CONFORME` / `NO CONFORME` y código de salida (0 / 1). Los **avisos**
no alteran el veredicto: señalan lo que merece mirada humana sin ser una violación. **Informa, no
bloquea** — la decisión de seguir con una corrida no conforme es del humano (NC-001), igual que en los
gates.

> **Honestidad sobre el alcance.** `CONFORME` significa *«conforme a lo comprobable sin traza»*, no
> *«el proyecto está bien»*. La conformidad nunca fue calidad (§8), y esta capa además es un
> subconjunto de la conformidad.

---

## Apéndice: Estándares de Ingeniería

- **Convención de commits:** `tipo(<incremento>): descripción`
  (`feat`/`spec`/`plan`/`test`/`refactor`/`verify`/`chore`/`docs`).
  Procedimiento y mapeo etapa→mensaje en `_guideline/git-protocol.md`.
- **Estrategia de ramas:** cada incremento se construye en su rama; la integración a la rama principal
  es **solo vía Pull Request** tras el veredicto CONFORME. **El harness nunca integra a la principal
  por su cuenta** (detalle en `AGENTS.md` / `CLAUDE.md`).
- **Selección de modelos (P-006, escalamiento proporcional):** el modelo se ajusta a la exigencia de la
  tarea —modelos más capaces para definición/spec/plan/verificación (razonamiento crítico), modelos de
  ejecución para construir/probar, y modelos ligeros para tareas simples (p. ej. el *starter* de
  sesión). Las asignaciones concretas se fijan al instanciar el proyecto.

> **Pendiente de instanciación.** La estructura física de carpetas para artefactos por incremento y
> plantillas (`_templates/`) se concreta al montar un proyecto real; esta metodología define el
> **flujo, los gates, los artefactos y los roles**, no una numeración de carpetas fija.
