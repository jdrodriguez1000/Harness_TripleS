# soda — Harness_TripleS

Arnés de IA en Python que orquesta agentes usando **suscripciones** (los CLIs oficiales
`claude`, `codex`, …) en lugar de API de pago por token.

El paquete instalable se llama `soda` (*Software Development Agentic*); el repositorio se
llama `Harness_TripleS`. Es una **herramienta de desarrollo**: se instala una vez en la
máquina y se invoca desde la carpeta de cada proyecto en el que trabajas, no se añade como
dependencia de esos proyectos.

El alcance completo del proyecto está en [`idea.md`](idea.md).

---

## Estado actual

En construcción. Lo que ya funciona:

- **`soda init`** — siembra la memoria (`_persistence/`) y la guía normativa (`_guideline/`)
  en un proyecto destino.
- **Capa de proveedores** — `Provider` (abstracto) y `ClaudeCLIProvider`, que invoca el CLI
  `claude` por subproceso. Todavía no hay agentes que la usen.

Lo que **no** existe todavía: los agentes (`sesion-starter`, `agent-worker`,
`sesion-closer`), la orquestación, y los subcomandos `soda start` / `soda close`.

Probado en Windows 11 con Python 3.12. No se ha verificado en macOS ni Linux; el código no
usa nada específico de Windows, pero eso es una expectativa, no una comprobación.

---

## Requisitos

- **Python 3.12 o superior**
- **[pipx](https://pipx.pypa.io/)** para instalar la herramienta de forma aislada
- El CLI **[`claude`](https://claude.com/claude-code)** instalado y autenticado, solo si vas
  a usar la capa de proveedores

---

## Instalación

### Windows

```powershell
python -m pip install --user pipx
python -m pipx ensurepath

git clone https://github.com/jdrodriguez1000/Harness_TripleS.git
python -m pipx install -e .\Harness_TripleS
```

### macOS / Linux

```bash
brew install python@3.12 pipx    # en Linux: python3 -m pip install --user pipx
pipx ensurepath

git clone https://github.com/jdrodriguez1000/Harness_TripleS.git
pipx install -e ./Harness_TripleS
```

Si `ensurepath` modificó el PATH, abre una terminal nueva. Comprueba que quedó bien:

```bash
soda --help
```

> **Sobre el `-e` (modo editable).** El comando `soda` apunta al código del repo clonado: un
> cambio en `src/` se refleja al instante sin reinstalar. El precio es que **si mueves o
> borras el repo, `soda` deja de funcionar**. Es lo adecuado mientras el harness se está
> construyendo. Cuando se estabilice, instala sin `-e` para desacoplarlo del repo.

### Actualizar

```bash
cd Harness_TripleS
git pull
```

Con instalación editable no hace falta nada más. Si instalaste sin `-e`:

```bash
pipx reinstall soda
```

### Desinstalar

```bash
pipx uninstall soda
```

---

## Comandos

### `soda init` — sembrar la memoria y la guía de un proyecto

Crea dos carpetas en el proyecto destino: `_persistence/` con los seis archivos de memoria
vacíos, y `_guideline/` con los tres documentos normativos que trae esta versión de `soda`.

```bash
soda init                    # en el directorio actual
soda init ../otro-proyecto   # en una ruta concreta
soda init --force            # reemplaza los archivos que ya existan
```

| Argumento | |
|---|---|
| `project_root` | Raíz del proyecto destino. Por defecto, el directorio actual. Debe existir: `init` siembra dentro de un proyecto, no crea el proyecto. |
| `--force` | Sobrescribe los archivos existentes en ambas carpetas. **Destruye memoria acumulada.** |

| Código de salida | |
|---|---|
| `0` | Sembró lo que faltaba, o no había nada que hacer |
| `1` | El destino no existe, no es un directorio, o no se pudo escribir |

**Es idempotente y no destructivo.** Un archivo que ya existe se salta; repetir `init` solo
completa lo que falte. Ningún archivo con contenido se pierde sin que escribas `--force`, y
ni siquiera entonces en silencio: la salida nombra cada archivo reemplazado.

Las dos carpetas se siembran igual pero no significan lo mismo, y `init` las reporta
distinto. La memoria es del proyecto destino: que diverja de la plantilla es lo esperado, así
que un archivo existente se salta sin más. La guía la posee la versión instalada de `soda`:
si un documento existe pero no coincide con el del paquete —copia vieja de una actualización
anterior, o editada a mano— se reporta como `difiere` en vez de esconderse bajo `saltado`.
Tampoco se toca sin `--force`; solo deja de ser silencioso.

Ejemplo:

```
$ cd mi-proyecto
$ soda init
Destino: C:\Users\tu-usuario\mi-proyecto\_persistence

  creado           progress.md
  creado           tasks.md
  creado           lessons.md
  creado           decisions.md
  creado           constraints.md
  creado           assumptions.md

6 creados.

Destino: C:\Users\tu-usuario\mi-proyecto\_guideline

  creado           principles.md
  creado           methodology.md
  creado           agents-and-evaluation.md

3 creados.
```

### Los seis archivos de memoria

`init` los crea vacíos; los llenan los protocolos de inicio y cierre de sesión.

| Archivo | Contenido | Código |
|---|---|---|
| `progress.md` | Estado actual, qué sigue, historial de hitos | — |
| `tasks.md` | Tareas y su estado | `T-` |
| `lessons.md` | Lecciones aprendidas | `L-` |
| `decisions.md` | Decisiones y sus alternativas descartadas | `D-` |
| `constraints.md` | Restricciones del proyecto | `C-` |
| `assumptions.md` | Supuestos asumidos | `A-` |

Cada archivo mantiene un índice al principio con enlaces al detalle: debe bastar leer el
índice para localizar información sin recorrer el archivo entero. La numeración es de tres
dígitos, permanente, y nunca se reutiliza ni se renumera.

`_persistence/` **debe versionarse en Git**: es el registro de estado entre sesiones. No lo
añadas al `.gitignore`.

### Los tres documentos normativos

`init` los siembra ya escritos: son producto, no plantillas a llenar. Definen cómo se
comportan los agentes y cómo se construye el proyecto.

| Archivo | Contenido |
|---|---|
| `principles.md` | Principios (`P-`), requisitos (`E-`) y normas (`NC-`) del comportamiento de los agentes |
| `methodology.md` | Proceso de construcción: espina del incremento, ciclo, madurez, gates, persistencia |
| `agents-and-evaluation.md` | Arquetipos de agente, evaluación del producto y observabilidad |

No los edites en el proyecto destino: la copia autorizada viaja dentro de `soda` y una
edición local queda marcada como `difiere` en el siguiente `init`, sin forma de reconciliarse
salvo sobrescribiéndola.

---

## Desarrollo

Para trabajar sobre el harness mismo, además de la instalación con pipx:

```bash
cd Harness_TripleS
python -m venv .venv
.venv/Scripts/pip install -e ".[dev]"    # Windows
# ./.venv/bin/pip install -e ".[dev]"    # macOS / Linux
```

```bash
.venv/Scripts/python -m pytest      # suite de tests
.venv/Scripts/python -m ruff check .  # lint
```

### Prueba manual de la capa de proveedores

Los tests mockean el subproceso: verifican que el código hace lo que se asumió, no que la
asunción sea cierta. Este script invoca el CLI `claude` de verdad (consume tu suscripción):

```bash
python scripts/probar_provider.py
python scripts/probar_provider.py "tu prompt"
python scripts/probar_provider.py --archivo prompt_largo.txt --timeout 120
```

---

## Estructura del repositorio

```
src/soda/            El producto: lo que se instala y distribuye
  core/provider.py     Contrato abstracto Provider
  providers/           Implementaciones concretas (ClaudeCLIProvider)
  templates/           Plantillas que viajan al proyecto destino
    _persistence/        Los seis archivos de memoria (los siembra `soda init`)
    _guideline/          Los tres documentos normativos (los siembra `soda init`)
      principles.md        Principios (P), requisitos (E) y normas (NC) del comportamiento
      methodology.md       Proceso de construcción: espina, ciclo, madurez, gates, persistencia
      agents-and-evaluation.md  Arquetipos de agente, evaluación del producto y observabilidad
  cli.py               CLI: `soda` y sus subcomandos
tests/               Suite automatizada
scripts/             Pruebas manuales (andamiaje, no se distribuye)
900_persistence/     Memoria de construcción de ESTE repo
idea.md              Alcance y visión del proyecto
CLAUDE.md            Protocolos de sesión para el asistente
```

Frontera importante: `src/soda/` es el producto; todo lo que está en la raíz es andamiaje de
construcción y no se empaqueta. El código de `soda` nunca lee ni escribe `900_persistence/`
—esa es la memoria de este repo—; solo trabaja con el `_persistence/` del proyecto destino,
siempre a partir de una raíz explícita.
