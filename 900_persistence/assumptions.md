# Assumptions

## Índice

| Código | Título |
|--------|--------|
| [A-001](#a-001--portabilidad-de-soda-a-macoslinux-no-verificada) | Portabilidad de `soda` a macOS/Linux no verificada |

## Detalle de supuestos

### A-001 — Portabilidad de `soda` a macOS/Linux no verificada

- **Supuesto:** `soda` (plantillas, `cli.py`, instalación con pipx) funciona igual en macOS/Linux que en Windows, porque el código no usa nada específico de Windows (rutas con `pathlib`, `shutil.which`, cero dependencias externas, y el `reconfigure` de UTF-8 es inofensivo donde UTF-8 ya es el default). `README.md` documenta la instalación para esas plataformas.
- **Riesgo si es falso:** Instrucciones de instalación incorrectas en `README.md`, o fallos silenciosos de `soda init`/`soda cli` en Mac o Linux que obligarían a depurar y corregir sin haberlo anticipado.
- **Cómo verificarlo:** Ejecutar la instalación con pipx y `soda init` en una máquina macOS o Linux real (o en un contenedor/VM), verificando la suite de tests y una siembra manual.
- **Estado:** Vigente
