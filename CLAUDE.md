# Harness_TripleS

Arnés de IA propio en Python que orquesta varios agentes usando **suscripciones** (CLIs
oficiales: `claude`, `codex`, …) en lugar de API de pago por token. Ver `idea.md` para el
alcance completo.

La memoria del proyecto vive en `900_persistence/` (seis archivos: `progress.md`,
`tasks.md`, `lessons.md`, `decisions.md`, `constraints.md`, `assumptions.md`).

---

## Protocolo de inicio de sesión — OBLIGATORIO

**Toda sesión de trabajo en este proyecto debe comenzar ejecutando el protocolo de inicio
de sesión.** No es opcional y no depende de que el usuario lo pida.

- Agente responsable: `harness-starter`
- Protocolo: skill `session-startup`

Antes de responder cualquier otra cosa en el primer turno de la sesión, lanza el agente
`harness-starter`. Él aplica el protocolo completo (definido en la skill, no aquí): lectura
obligatoria de `progress.md` y `tasks.md`, lectura bajo demanda de los otros cuatro
archivos, y bootstrap de Git + GitHub si el proyecto está vacío.

No reconstruyas el estado del proyecto por tu cuenta, no supongas dónde quedó el trabajo y
no empieces a implementar antes de que el arranque haya terminado. Si crees recordar el
estado de una sesión anterior, el protocolo se ejecuta igual: la memoria en disco es la
única fuente de verdad.

---

## Protocolo de cierre de sesión — OBLIGATORIO

**Toda sesión de trabajo en este proyecto debe terminar ejecutando el protocolo de cierre
de sesión.** No es opcional.

- Agente responsable: `harness-closer`
- Protocolo: skill `session-closing`

Cuando el usuario dé por terminada la sesión ("cerremos", "cierra la sesión", "guarda el
avance", "por hoy ya"), lanza el agente `harness-closer`. Él aplica el protocolo completo
(definido en la skill, no aquí): actualización obligatoria de `progress.md` y `tasks.md`,
actualización condicional de los otros cuatro archivos, sincronización de los índices, y
commit + push a GitHub.

No actualices los archivos de `900_persistence` a mano ni por fuera de este protocolo: los
códigos, los formatos y los índices los gobierna el closer, y editarlos por separado los
desincroniza.

---

## Convenciones del proyecto

- **Idioma:** español para toda la documentación, la memoria y la comunicación con el usuario.
- **Códigos de memoria:** `T-` tareas, `L-` lecciones, `D-` decisiones, `C-` restricciones,
  `A-` supuestos. Numeración de 3 dígitos, permanente, nunca se reutiliza ni se renumera.
- **Índices:** cada archivo de `900_persistence` mantiene una tabla de índice con enlaces
  ancla al detalle. El índice es la interfaz de búsqueda: debe bastar leerlo para localizar
  información sin recorrer el archivo completo.
- **Enfoque de construcción:** pasos lo más pequeños posible, verificables uno a uno antes de
  avanzar al siguiente.
- **Git:** no se hace push sin que el usuario haya entregado y confirmado la URL del remoto.
  Nunca `--force`.
