# Lessons

## Índice

| Código | Título | Fecha |
|--------|--------|-------|
| [L-001](#l-001--las-carpetas-numeradas-no-sirven-como-convención-para-módulos-python) | Las carpetas numeradas no sirven como convención para módulos Python | 2026-07-23 |
| [L-002](#l-002--github-rechaza-el-push-si-el-email-del-commit-está-protegido-por-privacidad) | GitHub rechaza el push si el email del commit está protegido por privacidad | 2026-07-23 |
| [L-003](#l-003--al-diagnosticar-manejo-de-texto-en-windows-descartar-primero-la-herramienta-de-diagnóstico) | Al diagnosticar manejo de texto en Windows, descartar primero la herramienta de diagnóstico | 2026-07-23 |
| [L-004](#l-004--verificar-el-empaquetado-instalando-en-un-entorno-limpio-no-solo-listando-el-wheel) | Verificar el empaquetado instalando en un entorno limpio, no solo listando el wheel | 2026-07-23 |
| [L-005](#l-005--la-prueba-manual-encuentra-defectos-que-los-tests-no-buscan) | La prueba manual encuentra defectos que los tests no buscan | 2026-07-23 |
| [L-006](#l-006--un-documento-heredado-de-otro-proyecto-arrastra-referencias-colgantes) | Un documento heredado de otro proyecto arrastra referencias colgantes | 2026-07-23 |
| [L-007](#l-007--un-archivo-importante-puede-llevar-sesiones-sin-estar-en-git) | Un archivo importante puede llevar sesiones sin estar en git | 2026-07-23 |

## Detalle de lecciones

### L-001 — Las carpetas numeradas no sirven como convención para módulos Python

- **Fecha:** 2026-07-23
- **Contexto:** Al diseñar la estructura de `src/soda/`, se consideró reflejar la convención de `900_persistence` (prefijos numéricos) dentro del código del paquete.
- **Lección:** Un módulo Python no puede empezar por un dígito, así que la numeración tipo `900_persistence` no es trasladable al código fuente.
- **Aplicación:** La numeración se mantiene únicamente en la documentación y en carpetas de andamiaje (como `900_persistence/`); el código bajo `src/soda/` usa nombres de módulo convencionales sin prefijos numéricos.

### L-002 — GitHub rechaza el push si el email del commit está protegido por privacidad

- **Fecha:** 2026-07-23
- **Contexto:** El push inicial del bootstrap del repositorio falló porque el email real del usuario (`jdrodriguez1000@gmail.com`) está protegido por la configuración de privacidad de GitHub.
- **Lección:** GitHub bloquea pushes cuyo commit use un email protegido; hay que usar la dirección `noreply` asociada a la cuenta (`<id>+<usuario>@users.noreply.github.com`).
- **Aplicación:** Se configuró `user.email` LOCAL al repo con `110043648+jdrodriguez1000@users.noreply.github.com`, evitando exponer el email real y desbloqueando el push sin tocar la configuración global de Git.

### L-003 — Al diagnosticar manejo de texto en Windows, descartar primero la herramienta de diagnóstico

- **Fecha:** 2026-07-23
- **Contexto:** Al ejecutar `scripts/probar_provider.py` contra el CLI real con prompts en español (acentos, eñes) y con un em-dash, la salida se veía corrompida (`�nicamente`) y un caso llegó a reventar con `UnicodeEncodeError`.
- **Lección:** Python en Windows escribe stdout en cp1252 por defecto; el `ClaudeCLIProvider` estaba devolviendo el texto UTF-8 correctamente, el problema era solo del propio script de diagnóstico al imprimir.
- **Aplicación:** Se corrigió con `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` (y `sys.stderr`) al inicio del script, con el porqué comentado en el código. Antes de concluir que un componente maneja mal el texto en Windows, hay que descartar primero que la propia herramienta de diagnóstico no sea la que corrompe la salida.

### L-004 — Verificar el empaquetado instalando en un entorno limpio, no solo listando el wheel

- **Fecha:** 2026-07-23
- **Contexto:** Verificar que las plantillas de `src/soda/templates/_persistence/` (T-004) viajan realmente en el paquete distribuible, no solo en el árbol de fuentes.
- **Lección:** Que un archivo aparezca en el `zipfile` del wheel no prueba que el código pueda leerlo en tiempo de ejecución desde una instalación real.
- **Aplicación:** La verificación decisiva fue construir el wheel, instalarlo en un venv desechable fuera del árbol de fuentes, y leer la plantilla desde ahí. Cuando un paquete distribuya datos (plantillas, recursos), la prueba válida es leerlos desde una instalación limpia, no solo listarlos en el archivo comprimido.

### L-005 — La prueba manual encuentra defectos que los tests no buscan

- **Fecha:** 2026-07-23
- **Contexto:** Corrida manual real de `soda init` en T-005, con la suite automatizada ya en verde.
- **Lección:** La prueba manual reveló un defecto cosmético ("1 creados", falta de concordancia de número en el resumen) que ningún test cubría porque nadie había pensado en ese caso.
- **Aplicación:** Mantener la prueba manual como paso de verificación aunque la suite esté verde; sirve para descubrir qué falta testear, no solo para confirmar lo que ya se testeó.

### L-006 — Un documento heredado de otro proyecto arrastra referencias colgantes

- **Fecha:** 2026-07-23
- **Contexto:** Al revisar `methodology.md` durante T-007, se encontraron citas a `L-015` y `L-022`, lecciones de otro proyecto que no existen en este repo (`lessons.md` va de L-001 a L-005) ni existirán en el destino, además de inconsistencias de ruta (`_template/` vs `_templates/`).
- **Lección:** Un documento de guía heredado de otro proyecto arrastra referencias colgantes (códigos inexistentes, rutas inconsistentes) que solo se detectan contrastándolo contra el repo real, no leyéndolo de corrido.
- **Aplicación:** Antes de dar por bueno un documento heredado, verificar cada referencia a código o ruta contra el estado real del repo destino; donde el código no exista, conservar la narrativa del hallazgo y quitar el código colgante en vez de dejarlo apuntando a la nada.

### L-007 — Un archivo importante puede llevar sesiones sin estar en git

- **Fecha:** 2026-07-23
- **Contexto:** Al mudar `905_guideline/` con `git mv` (T-008), `git status` reveló que `methodology.md` (876 líneas) aparecía como untracked: nunca había sido versionado, pese a llevar sesiones existiendo en el repo.
- **Lección:** Un archivo puede llevar sesiones de trabajo sin estar bajo control de versiones sin que nadie lo note; un `git clean` en cualquier momento lo habría borrado sin aviso.
- **Aplicación:** Revisar `git status` (no solo `git diff`) al tocar cualquier carpeta antigua o heredada, y tratar cualquier archivo untracked inesperado como una alerta a resolver antes de seguir, no como ruido a ignorar.
