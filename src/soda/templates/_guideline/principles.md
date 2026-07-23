# Principios y Reglas del Sistema de Agentes

> **Rol de este archivo.** Es **producto**: viaja con `soda` al proyecto destino y se instala en
> `_guideline/principles.md`. Gobierna el **comportamiento** de los agentes del arnés en cualquier
> proyecto que el arnés construya. No es la metodología con la que se construye `soda` mismo.

Fuente canónica de comportamiento del sistema de agentes. Sus compañeros son `methodology.md`
—**proceso** de construcción: fases, gates, madurez, persistencia (§0–§4, §6, §7)— y
`agents-and-evaluation.md` —**arquetipos, evaluación y observabilidad** (§3.1, §5, §8, §9, §10)—; entre
esos dos la numeración de secciones es continua y única. Ante conflicto sobre **cómo debe comportarse
un agente**, manda este documento; ante conflicto sobre **qué paso viene ahora en el flujo**, mandan
ellos.

---

## 0. Cómo se lee este documento

### 0.1 Tres audiencias, no una

La versión anterior declaraba las tres secciones "restricciones que todo agente debe seguir durante su
ejecución". Era falso y producía contradicciones: un agente no puede "cumplir en ejecución" que los
roles estén separados (eso lo decide quien diseña la flota), ni "cumplir" que se corran cinco
subagentes en paralelo (eso lo decide el orquestador). Al declararlo todo vinculante para todo agente,
las reglas de ejecución se leían como absolutos sin excepción y las recomendaciones de diseño se leían
como obligaciones.

Cada ítem declara ahora **a quién obliga**:

| § | Sección | Audiencia | Carácter |
|---|---|---|---|
| **1** | Diseño del arnés | Quien **diseña** la flota y el arnés | Vinculante al diseñar; orientativo en ejecución |
| **2** | Operación del orquestador | La **sesión principal** | Guía con criterio; se aplica o no según el caso, y la elección se justifica |
| **3** | Reglas de ejecución del agente | **Todo agente**, en cada invocación | **Vinculante y verificable**, sin excepción |

### 0.2 Orden de precedencia

Ante conflicto, en este orden:

1. **Instrucción explícita del humano** en la sesión en curso.
2. **Reglas de ejecución (NC)** — §3. Vinculantes; solo las levanta el humano.
3. **Principios de diseño (P)** — §1.1.
4. **Requisitos de diseño y guía de operación (E)** — §1.2 y §2. Ceden ante NC y P.

Si dos reglas de §3 chocan entre sí, **gana la más restrictiva**: la que detiene al agente. Detenerse
de más cuesta una reinvocación; seguir de más produce un artefacto que nadie audita.

### 0.3 Convención de códigos

Los códigos son **identificadores permanentes de tres dígitos**, no posiciones: `P-001`, `E-001`,
`NC-001`. Un código **nunca se reutiliza ni se renumera**, y **no cambia** aunque el ítem se mueva de
sección — la sección declara la audiencia, el código identifica la regla. Los códigos retirados se
listan en §4 con su destino, para que ninguna referencia externa quede colgando.

### 0.4 Estado de verificabilidad

Las reglas de §3 llevan un **predicado verificable** y una **consecuencia**. El predicado se escribe
**solo contra evidencia disponible hoy**: artefactos en disco y `git log`. Lo que exige saber *en qué
orden ocurrieron las cosas dentro de una invocación* («¿leyó el contrato antes de escribir?», «¿un solo
`Write`?») necesita un **motor de traza** que aún no existe, y se declara en §5 con su gatillo de
adopción, en vez de escribirse como si ya aplicara.

> **Por qué.** Escribir predicados que nadie puede ejecutar es exactamente el fallo que
> `agents-and-evaluation.md` §10.2 documenta haber cometido: perfiles de conformidad vivos en los prompts durante
> tres corridas completas sin que nadie los corriera nunca. Una regla inejecutable no es una regla a
> medias; es decoración.

---

## 1. Diseño del arnés

**Audiencia:** quien diseña la flota, los prompts y la arquitectura. Vinculante al diseñar.

### 1.1 Principios (P)

- **P-001 — Separación de roles.** Roles separados, no un agente todopoderoso.
- **P-002 — Trabajo incremental con artefactos de handoff.** Trabajo pequeño, contexto transferido como
  artefactos persistentes y no como resumen conversacional.
- **P-003 — Evaluador externo independiente.** Quien genera no evalúa. El evaluador corre en contexto
  fresco y es crítico por defecto.
- **P-004 — Context resets sobre compactación continua.** Reiniciar con contexto limpio es mejor que
  compactar el historial. Condiciones de activación en E-002.
- **P-005 — Contratos explícitos antes de la ejecución.** Se acuerda "terminado" antes de empezar.
  Ningún agente cruza un gate por su cuenta.
- **P-006 — Escalamiento proporcional a la complejidad.** El esfuerzo —capacidad del modelo, número de
  trabajadores, profundidad de razonamiento— se ajusta a la exigencia de la tarea.
  **Absorbe E-008** (*extended thinking*): razonar extendidamente es una forma de escalar esfuerzo, y se
  reserva para los pasos donde la calidad del razonamiento decide el resultado —definición, spec,
  verificación—, no para ejecución mecánica. Aplicarlo de forma indiscriminada gasta cuota sin mejorar
  la salida.
- **P-007 — Herramientas como extensiones críticas.** El diseño de las herramientas disponibles pesa
  tanto como el del prompt. Un agente sin la herramienta adecuada improvisa.
- **P-008 — Observabilidad y depuración como requisito.** Trazabilidad de cada decisión, para poder
  depurar. Se operacionaliza en E-013.

### 1.2 Requisitos de diseño (E)

Qué debe **proveer** el arnés para que los principios sean posibles.

#### E-001. Persistencia de estado entre sesiones
- Un archivo de progreso que registre el historial de lo ejecutado.
- Git como registro de estado: commits descriptivos al cerrar cada sesión, `git log` para reorientarse
  al abrirla, y repositorio remoto enlazado desde el principio.
- Sin este mecanismo cada sesión empieza ciega y el agente desperdicia contexto reorientándose.

#### E-003. Calibración del evaluador
P-003 requiere calibración explícita: sin ella, los evaluadores LLM son sistemáticamente **lenientes**
incluso ante salidas malas.
- Pocos ejemplos con desglose de puntajes detallados.
- Rúbrica 0.0–1.0 por dimensión (precisión factual, completitud, calidad de fuentes, eficiencia).
- Una sola llamada juez, más consistente que varios jueces.
- **El juez se contrasta contra etiquetas humanas y defectos sembrados, y se usa solo donde coincide con
  el humano.** Un juez sin calibrar no es una medición: es una opinión con decimales.

#### E-004. Mínima complejidad y evolución continua
- Empezar con el sistema más simple posible; añadir componentes solo con **evidencia** de que su
  ausencia degrada la calidad.
- Cada componente codifica una suposición sobre una limitación del modelo, y esa suposición caduca.
- **Prueba de remoción periódica:** quitar un componente a la vez y medir. Si la calidad no cae, se
  elimina y se registra la lección.
- Los sistemas de agentes no son estáticos: conforme los modelos mejoran, unos componentes se vuelven
  obsoletos y otros nuevos se justifican.

#### E-005. Ejecución durable: reanudar desde checkpoint
- Los fallos son inevitables en ejecuciones largas.
- El sistema reanuda desde el punto de fallo; no reinicia desde cero.
- Un agente cuya herramienta falla adapta su comportamiento —reintento, alternativa o escalamiento—
  dentro del límite de pérdida de E-014.

#### E-009. Evaluación temprana con muestras pequeñas
- No esperar al sistema completo: ~20 casos representativos sobre el primer componente funcional.
- Los cambios tempranos tienen efectos desproporcionados; pocas pruebas revelan mucho.
- Si la calidad es baja, se ajusta **la spec o el prompt del agente**, no el artefacto concreto.
- La evaluación humana es complemento indispensable de la automatizada, no su sustituto.

#### E-013. Observabilidad y conformidad por subagente
Operacionaliza P-008 sobre los **agentes que construyen**, no solo sobre el producto.
- **Traza por invocación.** Secuencia de herramientas, entradas, salidas y costo. La traza es la fuente
  de verdad de *qué hizo*; **el auto-reporte del agente es narrativa, no evidencia.**
- **Conformidad determinista.** Las reglas de §3 se evalúan como checks automáticos sobre
  (traza + artefacto): responden *¿siguió el procedimiento?*.
- **Conformidad ≠ calidad.** El procedimiento se mide aparte del juicio semántico (E-003). Un agente
  puede ser conforme y entregar un mal producto, y al revés.
- Sin esta capa, un fallo de comportamiento solo se detecta por inspección humana ad hoc.

---

## 2. Operación del orquestador

**Audiencia:** la sesión principal. Son guías con criterio: se aplican o no según el caso, pero **la
elección se justifica**, no se omite en silencio.

#### E-002. Cuándo hacer context reset
Los modelos exhiben *ansiedad contextual*: cierran trabajo prematuramente cuando anticipan el límite de
contexto. El reset es superior a la compactación cuando aparece.

**El disparador no puede ser auto-observación.** La versión anterior activaba el reset "si el agente
empieza a cerrar tareas sin completarlas" — pero si quien lo detecta es el propio agente, choca de
frente con E-013: el auto-reporte no es evidencia, y un modelo con ansiedad contextual es justamente el
peor juez de si la tiene. El disparador es **externo o mecánico**:

| Señal | Disponible hoy |
|---|---|
| Porcentaje de ventana de contexto consumido, sobre un umbral | Sí — lo mide el arnés, no el modelo |
| Reintentos fallidos consecutivos sobre el mismo paso | Sí |
| Pasos declarados en el plan vs. pasos con artefacto en disco | Sí |
| Divergencia entre lo que la traza registra y lo que el agente reporta | No — requiere motor de traza (§5) |
| Juicio del humano | Siempre |

Hasta que el arnés mida la primera señal, la decisión de reset es del **orquestador o del humano**,
nunca del agente sobre sí mismo.

#### E-006. Outputs al filesystem, no al orquestador
Para evitar el teléfono descompuesto entre agentes:
- Los subagentes escriben su salida directamente al filesystem.
- El orquestador recibe **referencias ligeras** (rutas, identificadores), no el contenido completo.
- Mejora la fidelidad, reduce tokens y evita que el orquestador sea el cuello de botella.

#### E-007. Paralelización, condicionada al presupuesto de cuota
La recomendación original —3–5 subagentes en paralelo, porque "la paralelización escala el uso de tokens
eficientemente"— proviene de investigación sobre **API de pago por token**, donde más tokens se compran.
**Este arnés corre sobre suscripciones** (`idea.md`): no se compran tokens, se consume una **ventana de
cuota con límite de tasa**. Lanzar cinco subagentes quema esa ventana cinco veces más rápido y puede
dejar la sesión bloqueada a mitad de un incremento — el recurso escaso no es el dinero, es el **derecho
a seguir trabajando hoy**.

**Por defecto: secuencial.** Se paraleliza solo si se cumplen las tres condiciones:

1. Las subtareas son **genuinamente independientes** (ninguna consume la salida de otra).
2. Queda **holgura de cuota** suficiente para terminar el incremento en curso si todas corren.
3. El fallo de una **no invalida** el trabajo de las demás.

Y no se paraleliza nunca entre agentes de etapa que escriben la traza compartida: `methodology.md` §7
admite la única excepción a Single Writer **precisamente porque corren uno a la vez**. Paralelizarlos
reintroduce la condición de carrera que esa excepción da por imposible.

#### E-010. Secuencia de inicio de sesión
Arranque explícito y siempre el mismo:
- Verificar directorio y ambiente.
- Leer `git log` y el archivo de progreso.
- Revisar los contratos activos.
- Prueba básica de sanidad del ambiente.
- Seleccionar la siguiente tarea según el backlog.

#### E-012. Arquitectura orquestador–trabajador
- El orquestador analiza el objetivo, fija la estrategia y crea subagentes especializados.
- **Guarda su plan en memoria persistente ANTES de crear subagentes**, para no perderlo si el contexto
  crece.
- Los subagentes operan con ventanas de contexto propias y frescas.
- Cada consigna incluye: objetivo, formato de salida esperado, herramientas disponibles y **límites**.
  Sin esos cuatro, los subagentes duplican trabajo o toman caminos equivocados.
- El orquestador es **dueño del canal con el humano**; los subagentes no lo tienen (ver NC-001).

#### E-014. Presupuesto de sesión y límite de pérdida
Un agente que falla no falla gratis: consume cuota, y bajo suscripción la cuota es el presupuesto real.
Todo trabajo corre con un tope declarado de antemano.

- **Reintentos:** un subagente que falla se reinvoca **como máximo una vez**, y solo con la consigna
  **corregida**. Un tercer intento idéntico no es persistencia, es gastar cuota esperando otro dado.
  Tras el segundo fallo se **escala al humano** con lo aprendido de ambos intentos.
- **Avance verificable:** si un ciclo termina sin artefacto nuevo en disco ni test que cambie de estado,
  cuenta como fallo aunque el agente reporte progreso (E-013).
- **Agotamiento de cuota:** al detectar límite de tasa, la sesión **se cierra ordenadamente** por el
  protocolo de cierre —memoria actualizada y commit— en vez de seguir degradada. Media hora de trabajo
  perdido por no cerrar cuesta más que la ventana que se quería aprovechar.

---

## 3. Reglas de ejecución del agente

**Audiencia:** todo agente, en cada invocación. **Vinculantes y verificables.** Cada regla lleva
enunciado, predicado comprobable y consecuencia cuando falla.

Consecuencias posibles: **NO CONFORME** (la corrida no es confiable; la sesión principal reinvoca o
escala, y **nunca lleva una corrida no conforme a un gate humano**), **AVISO** (merece mirada humana sin
ser violación) y **PARADA** (se detiene la sesión).

---

### NC-001 — Decisión consultada por umbral

**Enunciado.** El agente decide por su cuenta lo **reversible y de bajo impacto**, dejándolo por
escrito; se detiene y escala lo **irreversible o lo que cambia materialmente el resultado**. Nunca
decide en silencio, y nunca se paraliza ante una ambigüedad trivial.

**Umbral.** La regla anterior ("ante cualquier ambigüedad, detente y consulta") era inaplicable: un
subagente no tiene canal con el humano, así que o paralizaba el sistema o se ignoraba en la práctica. El
umbral la vuelve operable:

| Situación | Qué hace el agente |
|---|---|
| Reversible **y** no cambia el resultado | Decide, lo registra como supuesto, continúa |
| Irreversible (borra, publica, integra, gasta cuota grande) | **Se detiene y escala** |
| Cambia materialmente el resultado del artefacto | **Se detiene y escala** |
| Falta un dato cuya fuente no lo trae | Escribe `<no declarado>`; **no lo deduce de otra fuente** |

**A quién se escala.** Un subagente **no** escala al humano: escala **al orquestador**, que es dueño de
ese canal (E-012). Escalar es **detenerse, dejar por escrito qué encontró, qué alternativas había y por
qué no eligió, y devolver el control**. Escalar nunca es esperar en silencio ni preguntar al vacío.

**Predicado (hoy, sobre artefacto).** El artefacto producido contiene una sección de supuestos y
decisiones tomadas, no vacía o con "ninguno" explícito. Si el agente se detuvo, su reporte nombra el
punto exacto y la alternativa que no eligió. No quedan marcadores de plantilla sin sustituir.

**Consecuencia.** NO CONFORME.

> Absorbe la antigua NC-6, que enunciaba la misma regla con otras palabras.

---

### NC-002 — Simplicidad primero

**Enunciado.** Código mínimo con interfaces simples. Sin abstracciones, parámetros ni configurabilidad
que nadie pidió.

**Predicado (hoy, sobre artefacto).** Toda opción de configuración, parámetro opcional o punto de
extensión presente en el diff aparece **pedido** en el plan o en la spec. Lo que no está pedido, sobra.

**Consecuencia.** AVISO, con revisión en el gate humano.

---

### NC-003 — Cambios quirúrgicos

**Enunciado.** Solo se toca lo necesario para la tarea. No se refactoriza lo que funciona. No se borra
código muerto preexistente sin autorización.

**Predicado (hoy, sobre git).** `git diff --name-only` del commit de etapa está **contenido** en el
conjunto de archivos declarados en el plan de la tarea. Ningún archivo fuera de ese alcance.

**Consecuencia.** NO CONFORME.

---

### NC-004 — Slices verticales

**Enunciado.** Una funcionalidad completa de punta a punta (datos → interfaz) a la vez. La integración se
valida con un *Tracer Bullet* antes de ampliar.

**Predicado (hoy, sobre artefacto).** El estado de la slice no se bifurca por capa técnica: las capas son
tareas etiquetadas dentro de Construir, no pasos del ciclo. Existe **al menos un caso end-to-end en
verde** antes de que se abran casos adicionales.

**Consecuencia.** NO CONFORME en el gate de plan.

---

### NC-005 — Terminado = evidencia proporcional a la naturaleza del artefacto

**Enunciado.** Ninguna tarea se da por terminada sin evidencia. **La forma de la evidencia la fija la
naturaleza del artefacto**, no una regla única.

La versión anterior decía "Definición de Terminado = test en verde. Sin excepción." Era falsa en tres
casos reales y frecuentes:

| Naturaleza del artefacto | Evidencia válida de "terminado" |
|---|---|
| Código determinista | **Test automatizado en verde.** Es el caso por defecto |
| Salida probabilística (prompt de agente) | **Rúbrica calibrada + N corridas** con consistencia medida (E-003). No existe test determinista sobre una salida probabilística — el propio E-013 lo reconoce |
| Verificación que no vive en la suite (empaquetado, script manual, instalación limpia) | **Verificación manual documentada**: qué se hizo, con qué resultado, registrado en el archivo de tareas |
| Documento | Check determinista de completitud y trazabilidad + gate humano |

**Lo inaceptable es "terminado sin evidencia", no "terminado sin pytest".** Forzar un test donde no
aplica produce un test que no afirma nada, y un test que no afirma nada pasa siempre: es peor que no
tenerlo, porque simula cobertura.

**Predicado (hoy, sobre artefacto).** La entrada de la tarea en el archivo de tareas tiene un campo de
resultado no vacío que **nombra la evidencia concreta y dónde vive**. Una tarea marcada como implementada
sin ese campo no está terminada.

**Consecuencia.** La tarea no se marca implementada. NO CONFORME si se marcó.

---

### NC-006 — *(retirado)*

Absorbido por **NC-001**. Ver §4.

---

### NC-007 — Frontera de operaciones destructivas

**Enunciado.** Un agente con acceso a shell y filesystem opera sobre repositorios que no son suyos. Las
siguientes operaciones están **prohibidas sin autorización explícita del humano en la sesión en curso**,
y ninguna se justifica por conveniencia:

- `git push --force` o cualquier reescritura de historial publicado. **Nunca**, ni con autorización.
- Borrar o sobrescribir archivos que el agente no creó, sin confirmación previa.
- Escribir fuera del `project_root` declarado.
- Commitear secretos: claves, tokens, credenciales, `.env`.
- Integrar a la rama principal. La automatización llega hasta el PR; **el arnés nunca mergea**.
- Instalar, desinstalar o modificar software a nivel de máquina.

**Predicado (hoy, sobre git y artefacto).** El historial de la rama no muestra reescritura; el diff no
contiene rutas fuera del `project_root`; un escaneo de secretos sobre el diff no da positivo; la rama del
commit no es la principal.

**Consecuencia.** **PARADA.** Es la única regla cuya violación detiene la sesión en vez de reinvocar: las
demás producen un artefacto malo y recuperable, esta produce daño en el repositorio del usuario.

---

## 4. Códigos retirados

Un código retirado **no se reutiliza**. Esta tabla existe para que ninguna referencia externa quede
colgando.

| Código | Qué era | Destino |
|---|---|---|
| **E-008** | *Extended thinking* para razonamiento complejo | **Absorbido en P-006.** Era un caso particular de escalamiento proporcional, y además le faltaba criterio de cuándo aplicar |
| **E-011** | Estrategia de búsqueda "de amplio a estrecho" | **Retirado.** Es una táctica de investigación, no un estándar de comportamiento del sistema. Su lugar es el prompt del agente investigador |
| **NC-006** | "Sin decisiones silenciosas" | **Absorbido en NC-001.** Era la misma regla que NC-001 enunciada dos veces, y la duplicación escondía que a ninguna de las dos le faltaba umbral |

---

## 5. Pendientes declarados

Lo que este documento **no** resuelve todavía, dicho explícitamente para que no se confunda con algo ya
cubierto:

- **Predicados que exigen orden intra-invocación** («¿leyó el contrato antes de escribir?», «¿un solo
  `Write`?», «¿la confirmación fue posterior al turno del humano?»). Requieren motor de traza (E-013).
  **Gatillo de adopción:** cuando exista `_trace/` y un checker que lo lea.
- **Umbral numérico de ventana de contexto** para el disparador de E-002. Requiere que el arnés exponga
  esa medición. Hoy la decisión es del orquestador o del humano.
- **Presupuesto de cuota cuantificado** en E-014 (cuánta holgura es "suficiente"). Requiere medir el
  consumo real de una sesión típica; hasta entonces es juicio del orquestador.
