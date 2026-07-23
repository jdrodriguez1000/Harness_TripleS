# Idea: Harness propio (Python, basado en suscripciones)

## Qué se busca

Construir, paso a paso (estilo tutorial), un arnés de IA propio en **Python** que orqueste
varios agentes usando **suscripciones** (Claude Pro/Max, ChatGPT Plus, etc.) en lugar de
API de pago por token.

## Puntos clave

1. **Sin API, con suscripción**: los modelos se invocan a través de sus CLIs oficiales
   (`claude`, `codex`, y en el futuro `gemini`, etc.) como subprocesos, no vía SDK + API key.
2. **Tres agentes definidos**:
   - `sesion-starter` — arranca/prepara la sesión de trabajo.
   - `agent-worker` — ejecuta el trabajo principal.
   - `sesion-closer` — cierra/consolida la sesión.
3. **Herramientas como archivos independientes**, asignables por agente (no todos los
   agentes tienen acceso a las mismas tools).
4. **Multi-proveedor**: unos agentes trabajando con Claude Code y otros con OpenAI,
   diseñado para poder añadir Gemini, MiniMax, Kimi K2, etc. más adelante sin rehacer la
   arquitectura.
5. **Observabilidad y evaluación** de los agentes: registro de lo que hace cada agente y
   forma de evaluar su desempeño (ligero, sin depender de plataformas externas por ahora).

## Distinción clave: harness (dev) vs. app en producción

El harness se usa para **construir** aplicaciones de software. Hay dos contextos de uso
de los modelos que no se deben mezclar:

- **Mientras se construye la app** (agentes del harness: `sesion-starter`,
  `agent-worker`, `sesion-closer`): se usan **suscripciones** vía CLI, como ya se definió.
- **La app ya en producción**: si esa app incluye sus propios agentes de IA como parte de
  su funcionalidad (ej. una app para aprender inglés donde un agente elige una palabra
  clave de las 1000 más usadas, arma una frase con ella y evalúa 3 frases que el usuario
  escribe/dice), esos agentes de producción deben usar **API con key**, no la suscripción
  personal, porque atienden tráfico real de usuarios finales.

Implicación de diseño: el `Provider` del harness debe soportar dos modos de backend por
proveedor (CLI/suscripción para desarrollo, API/key para producción), sin que el resto del
arnés tenga que cambiar para pasar de un modo a otro.

## Reutilización y cambio de modelo/proveedor

El harness debe ser **totalmente reutilizable** (no atado a un proyecto concreto) y debe
ser **muy fácil cambiar de modelo**, tanto entre modelos de un mismo proveedor (ej. Sonnet
↔ Opus) como entre proveedores distintos (ej. Claude ↔ OpenAI ↔ Gemini), sin tocar la
lógica de los agentes ni de las tools.

Para esto se debe considerar un **gateway/capa de enrutamiento de modelos**: un punto único
de acceso que abstrae "a qué proveedor y modelo específico" se le manda cada request,
similar al concepto de model gateway mencionado en la serie de vídeos. Esto se suma (no
reemplaza) a la abstracción de Provider ya definida.

## Inicialización de nuevos proyectos ("init")

El harness vive separado de los proyectos que ayuda a construir. Debe existir un
script/comando de **inicialización (scaffold)** que permita instanciar el harness en una
carpeta nueva para arrancar un proyecto distinto, sin duplicar código a mano ni volver a
configurar todo desde cero.

## Memoria del proyecto: carpetas `900_persistence` / `_persistence`

Hay dos contextos, cada uno con su propia carpeta de memoria, pero con los mismos 6 archivos:

- **`900_persistence`** — memoria del propio proyecto Harness_TripleS mientras lo
  construimos paso a paso (este repositorio).
- **`_persistence`** — memoria de cada aplicación que se construya usando el harness ya
  terminado.

Los 6 archivos fijos, en ambos casos:

1. **progress.md** — estado actual del proyecto: dónde estamos y qué sigue a grandes rasgos.
2. **tasks.md** — tareas realizadas y próximas, cada una con código de seguimiento y
   estado (`Implementada` / `No implementada` / `Cancelada-Suspendida`).
3. **lessons.md** — lecciones aprendidas durante la ejecución del proyecto.
4. **decisions.md** — decisiones tomadas durante la ejecución del proyecto.
5. **constraints.md** — limitaciones o restricciones para la ejecución del proyecto.
6. **assumptions.md** — supuestos del proyecto.

Esta carpeta es la que probablemente lean/escriban los agentes `sesion-starter` (para
retomar contexto al iniciar) y `sesion-closer` (para dejar todo actualizado al cerrar).

## Enfoque de construcción

Igual que en la serie de vídeos de Harness Engineering: ir capa por capa, empezando por lo
mínimo indispensable y añadiendo piezas (proveedores, agentes, tools, observabilidad)
de forma incremental y verificable en cada paso. Los pasos deben ser **lo más pequeños
posible**: mejor muchos pasos pequeños y bien entendidos que pocos pasos grandes, para
poder verificar cada uno antes de avanzar al siguiente.
