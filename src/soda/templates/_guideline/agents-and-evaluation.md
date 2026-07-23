# Agentes y Evaluación

> **Rol de este archivo.** Es **producto**: viaja con `soda` al proyecto destino y se instala en
> `_guideline/agents-and-evaluation.md`. Es la **segunda mitad de la metodología de construcción** —su
> primera mitad es `_guideline/methodology.md`—, y se separó de ella cuando el bloque de
> agentes/evaluación/observabilidad superó el umbral que la propia metodología fijaba (~250 líneas).

Aquí vive **quién hace el trabajo y cómo se juzga**: los **arquetipos** de agente y su contrato (§5), la
**evaluación del producto** (§8), la **evolución del harness** (§9) y la **observabilidad del
comportamiento** de los agentes (§10). El **proceso** —los ejes, la espina, el ciclo de incremento, los
estadios de madurez, los gates y la persistencia— vive en `methodology.md`.

> **Un solo documento en dos archivos.** La numeración de secciones es **continua y única entre los
> dos**: `§8` significa lo mismo se lea donde se lea, y ninguna referencia cruzada necesita decir en qué
> archivo está. Este es el mapa:
>
> | Secciones | Archivo |
> |---|---|
> | §0 (propósito, mapa de fuentes, **§0.3 estado de aplicación**), §1, §2, §3, §4, §6, §7, Apéndice | **`methodology.md`** |
> | **§3.1**, **§5**, **§8**, **§9**, **§10** | **este archivo** |

> **Prerrequisito de lectura: `methodology.md` §0.3.** Define las tres marcas de estado que este archivo
> usa por todas partes. En resumen: *(sin marca)* = **NORMATIVO**, rige desde la primera sesión;
> **`[DIFERIDO]`** = decidido **no** adoptar aún, lleva **gatillo de adopción**; **`[PENDIENTE]`** =
> se quiere pero **falta la pieza** que lo hace posible, y esa pieza se nombra. Las dos últimas **no son
> intercambiables**: una se revierte con evidencia, la otra entregando código. **Casi todo §5 y §10
> están `[PENDIENTE]`** — descríbenlo como destino, no como inventario disponible.

> **Relación con el comportamiento.** El *qué* del comportamiento de los agentes lo fija
> `_guideline/principles.md` (`P-`, `E-`, `NC-`). Ante conflicto sobre **cómo debe comportarse un
> agente**, manda `principles.md`; sobre **qué paso viene ahora en el flujo**, manda `methodology.md`.

---
---

## Tabla de contenidos

| § | Sección | Qué contiene |
|---|---|---|
| **3.1** | Observabilidad y evaluación del ciclo TDD | Cómo el test es contrato, evidencia y oráculo en código |
| **5** | Agentes: arquetipos y responsabilidades `[PENDIENTE]` | Familias de arquetipos y coordinación — la flota no se entrega |
| 5.1 | · Contrato de un constructor de entregables | Plantilla → instancia → relleno → gate |
| 5.2 | · Revisor de código `[DIFERIDO]` | Evaluador independiente de calidad/seguridad |
| 5.3 | · Especialización de flota `[DIFERIDO]` | Frontend/backend y otras variantes de instanciación |
| **8** | Evaluación | Cómo se evalúa el **producto** según la naturaleza de la salida |
| 8.1 | · Flujo de evaluación (ejemplo) | Las tres capas de evaluación de un entregable |
| **9** | Evolución del harness | Mínima complejidad (E-004) y prueba de remoción |
| **10** | Observabilidad y conformidad `[PENDIENTE]` | Cómo se audita el **comportamiento** de los agentes |
| 10.1 | · Flujo end-to-end (ejemplo) | Recorrido desde la invocación hasta la conformidad |
| 10.2 | · Capa barata de conformidad `[PENDIENTE]` | Lo auditable sin motor de traza: artefactos en disco + `git log` |

> **§3.1 conserva su número.** Pertenece conceptualmente al ciclo de incremento (§3, en
> `methodology.md`) y se mudó aquí porque trata de evaluación y observabilidad. Renumerarla habría roto
> las referencias cruzadas sin ganar nada.

---

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
 2. ¿LOS TESTS VALEN?  [DIFERIDO] mutation testing / DEFECTOS SEMBRADOS: inyecta bugs → ¿la suite se
       pone roja?  (equivalente en código a "calibrar el juez" de los documentos, §8.1)
       gatillo: escapan defectos que la suite debió atrapar, de forma repetida
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

---
---

## 5. Agentes: arquetipos y responsabilidades

La metodología define **arquetipos** (roles agnósticos), no una flota concreta. La flota real —con
nombres y modelos— se define **al instanciar cada proyecto**, respetando estos arquetipos.

> **`[PENDIENTE]` La flota no se entrega.** *Requiere: agentes de construcción en el harness.* Hoy solo
> existen los **agentes de sesión** (*starter*, *closer*). Esta sección describe **el destino**, no un
> inventario disponible: la sesión principal ejecuta los pasos de §3 con **subagentes ad hoc**, y lo que
> sigue siendo obligatorio es la **disciplina** —quien construye ≠ quien evalúa, contexto fresco, gates
> humanos—, no el nombre del arquetipo. Un arquetipo sin construir **no es excusa para saltarse su
> paso**: es un subagente sin nombre propio haciendo ese paso.

**Dos familias, según lo que producen** (como planteó el encuadre del proyecto):

- **Constructores de ENTREGABLES** — producen artefactos de definición/documentación:
  *Definidor* (definición/historias), *Especificador* (spec + criterios de aceptación), *Planificador*
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

> **`[PENDIENTE]` Realización concreta del Descubridor (instanciación).** *Requiere: los tres
> subagentes de onboarding y `_context/client_brief.*`.* Ninguno se entrega hoy; lo que sigue describe
> la forma acordada para cuando se construyan. En su ausencia, el descubrimiento lo conduce el humano
> con la sesión principal, y el `discovery.md` se escribe igual —es insumo del prototipo, no opcional—.
> El Descubridor se materializa como **tres agentes** que separan *ingerir*, *elicitar* y *estructurar*
> (E-004):
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
> **spike/PoC** si domina la factibilidad (§3 del discovery)—, en el **medio de ese actor**
> (app móvil, web, escritorio, CLI…) declarado en §6 del discovery y con la tecnología **más barata que valide la
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
1. **`[PENDIENTE]` Plantilla = contrato de forma.** *Requiere: `_templates/`.* Cada tipo de entregable
   tiene un **esqueleto versionado** en `_templates/` (una plantilla por artefacto: definición, spec,
   plan…). El esqueleto fija la **estructura obligatoria** —secciones, campos, marcadores de relleno—:
   es el contrato de *forma*. El *qué* de contenido lo fijan el contrato del incremento y la spec.
2. **`[PENDIENTE]` Instanciar antes de rellenar.** *Requiere: `_templates/`.* El agente **copia** el esqueleto a la ubicación de trabajo del
   incremento con el **nombre canónico** del artefacto — **nunca escribe desde cero**. Así todo
   artefacto **nace conforme** a su plantilla y la conformidad de estructura es verificable por **diff**
   contra el esqueleto.

   > **Sin `_templates/`** (hoy): los pasos 1–2 no se pueden ejecutar. El agente estructura el artefacto
   > según la spec y **declara** que lo hizo sin plantilla. Los pasos **0, 3 y 4 rigen igual**: la
   > ausencia de esqueleto no libera de verificar el insumo, respetar Single Writer ni ceder el gate.

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
- **`[DIFERIDO]` Evaluación de calidad (§8):** *gatillo: existe un dataset de fixtures con etiquetas
  humanas.* *Juez LLM* calibrado **solo** para el juicio **semántico** del contenido (¿las historias son
  correctas, completas y trazables?), offline y por lotes. Hasta entonces, el juicio de calidad lo hace
  el **gate humano**. **Conformidad (procedimiento) y calidad (contenido) se miden por separado.**

> El mismo contrato aplica, con su plantilla propia, a *Especificador* (spec), *Planificador* (plan) y
> al informe del *Verificador*. Los **constructores de código** (§5) no usan plantilla-esqueleto: su
> "forma" la fijan los tests y la spec, y su conformidad se audita igual vía traza (§10).

### 5.2 `[DIFERIDO]` Revisor de código (evaluador independiente)

> *Gatillo de adopción: la evidencia muestra defectos de calidad escapándose de forma sistemática al
> gate humano de PR.* Hasta entonces esta función la cumple el humano revisando el PR.

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

### 5.3 `[DIFERIDO]` Especialización de flota (instanciación)

> *Gatillo de adopción: evidencia de que un trío TDD único rinde mal en frontend y backend a la vez.*

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

---
---

## 8. Evaluación (dimensionada a la naturaleza de la salida)

La independencia del evaluador (P-003) se cumple corriendo verificación e integración en contextos
frescos, separados de quien construye.

| Tipo de salida | Naturaleza | Cómo se evalúa |
|---|---|---|
| **Código** (el entregable) | Objetiva | **Tests** + **veredicto binario** (CONFORME/NO CONFORME) + matriz de trazabilidad |
| **Entregables documentales** (definición, spec, plan, informe) | Semiestructurada | **Conformidad determinista** (¿sigue la plantilla y traza?) + `[DIFERIDO]` **juez LLM** con rúbrica **0.0–1.0** calibrada (E-003), solo donde el juicio es semántico, y **N corridas** midiendo consistencia (pass-rate + varianza) |

**Evaluación temprana (E-009).** Al completar el primer componente funcional, evaluar una muestra de
**~20 casos representativos** (sintéticos, incluidos **defectos sembrados**); si la calidad es baja,
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
 3. [DIFERIDO] JUEZ DE CALIDAD (LLM) — agente DISTINTO del que escribió, contexto fresco (P-003)
       gatillo: existe un dataset de fixtures con etiquetas humanas
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

> **Por tipo de salida (§8).** Cambia la **capa 3**: en un **entregable documental** es el **juez LLM**
> calibrado (semántico); en **código** son los **tests** y el *mutation testing* (binario, objetivo, sin
> LLM — §3.1). El gate humano y la independencia son iguales en ambos.

---
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
---

## 10. `[PENDIENTE]` Observabilidad y conformidad de los agentes (E-013, P-008)

> *Requiere: el motor de traza (§7.2).* Toda esta sección describe una capa que **hoy no corre**. La
> consecuencia práctica está en §0.3: sin traza, la conformidad **no se puede afirmar**, y el único
> control real sobre el comportamiento de un agente es el **gate humano**. Los perfiles de conformidad
> se escriben igual —son el contrato que el motor ejecutará—, pero un agente **no puede declararse
> CONFORME por su cuenta**: eso sería exactamente el auto-reporte que esta sección rechaza.

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

### 10.2 `[PENDIENTE]` Capa barata de conformidad — `_tools/conformance.sh`

> *Requiere: el script `_tools/conformance.sh`, que el harness aún no entrega.* Lo que sigue es su
> especificación, no una herramienta disponible.

El flujo de §10.1 depende de un **motor de traza** que todavía no existe. Esperarlo dejó, en un
proyecto anterior, los perfiles de conformidad escritos en los prompts durante tres corridas completas
**sin que nadie los ejecutara nunca** — el fallo exacto que §0.3 previene. La capa barata se especifica
para cerrar ese hueco **sin instrumentar nada**, con lo que ya está disponible en cualquier proyecto:
los **artefactos en disco** y el **`git log`**.

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
