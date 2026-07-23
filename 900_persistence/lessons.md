# Lessons

## Índice

| Código | Título | Fecha |
|--------|--------|-------|
| [L-001](#l-001--las-carpetas-numeradas-no-sirven-como-convención-para-módulos-python) | Las carpetas numeradas no sirven como convención para módulos Python | 2026-07-23 |
| [L-002](#l-002--github-rechaza-el-push-si-el-email-del-commit-está-protegido-por-privacidad) | GitHub rechaza el push si el email del commit está protegido por privacidad | 2026-07-23 |

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
