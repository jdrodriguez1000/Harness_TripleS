"""`soda start`: arranca una sesión de trabajo sobre un proyecto destino.

Tiene dos ramas y las decide Python leyendo el disco, sin gastar un token:

- **Proyecto vacío** —la memoria sigue igual que la sembró `soda init`—: no hay
  sesiones anteriores que reconstruir, así que lo que toca es dejar el proyecto
  listo para trabajar. Eso es el bootstrap de Git de este módulo, y es 100%
  determinista: `git init`, `.gitignore`, remoto, commit inicial y push. No
  interviene ningún modelo (D-026), y no podría: el paso central es pedirle al
  humano la URL de su repositorio, y un `claude -p` no tiene con quién hablar
  (C-007). El script sí, porque tiene stdin.
- **Proyecto con memoria**: invoca a `sesion-starter` (T-012), que entrega el
  informe de reanudación.

El diálogo con el humano entra por `preguntar` y la salida por `informar` en vez
de llamar a `input()` y `print()` directamente. No es ceremonia: es lo que
permite probar entero un flujo interactivo e irreversible sin que ningún test
se quede esperando a que alguien teclee.

Sobre destruir cosas: aquí no se sobrescribe nada. Un repositorio que ya existe
se respeta, un `.gitignore` que ya existe se conserva y se reportan las reglas
que le faltan, y un remoto `origin` distinto del que se pide se cambia solo
después de preguntar. Ningún push lleva `--force`, ni aquí ni en ningún sitio.
"""

import re
from collections.abc import Callable
from pathlib import Path

from soda.core import git
from soda.templates import GITIGNORE_FILENAME, read_gitignore_template

__all__ = [
    "MENSAJE_COMMIT_INICIAL",
    "RAMA_POR_DEFECTO",
    "SinCanalConElHumanoError",
    "bootstrap",
    "reglas_que_faltan",
    "url_valida",
]

RAMA_POR_DEFECTO = "main"
REMOTO = "origin"
MENSAJE_COMMIT_INICIAL = "chore: commit inicial del proyecto"
INTENTOS_DE_URL = 3

#: Formas de remoto que se aceptan sin preguntar dos veces. La validación
#: existe para atrapar el error de tecleo obvio —pegar el nombre del repo en vez
#: de su URL—, no para decidir si el remoto existe: eso lo dice el push y lo
#: dice mejor. De ahí que la lista incluya rutas locales absolutas y `file://`,
#: que son remotos perfectamente válidos para git.
_URL = re.compile(
    r"""^(
        (https?|ssh|git|file)://\S+     # https://host/repo.git, file:///ruta
        | [\w.\-]+@[\w.\-]+:\S+         # git@github.com:usuario/repo.git
        | [A-Za-z]:[\\/].+              # C:\ruta\repo.git
        | /.+                           # /ruta/repo.git
    )$""",
    re.VERBOSE,
)

Preguntar = Callable[[str], str]
Informar = Callable[[str], None]


class SinCanalConElHumanoError(Exception):
    """Se necesitaba preguntar algo y no había nadie al otro lado de stdin."""


def _con_canal(preguntar: Preguntar) -> Preguntar:
    """Convierte el fin de stdin en un error con nombre.

    Sin esto, ejecutar `soda start` con la entrada redirigida —en un script, en
    CI, o simplemente con una tubería— revienta con el `EOFError` crudo de
    `input()` a mitad del arranque. El arranque de un proyecto es justamente el
    flujo que no puede continuar sin el humano (C-007): hay que decirlo, no
    volcar una traza.
    """

    def envuelto(texto: str) -> str:
        try:
            return preguntar(texto)
        except EOFError as exc:
            raise SinCanalConElHumanoError(
                "`soda start` necesita una terminal interactiva: el arranque de "
                "un proyecto pregunta la URL de tu repositorio y no puede "
                "inventarla. Ejecútalo sin redirigir la entrada."
            ) from exc

    return envuelto


def url_valida(url: str) -> bool:
    """¿`url` tiene forma de remoto de git (URL, `usuario@host:ruta` o ruta absoluta)?"""
    return bool(_URL.match(url.strip()))


def reglas_que_faltan(existente: str, plantilla: str) -> list[str]:
    """Devuelve las reglas de `plantilla` que no están ya en `existente`.

    Compara línea a línea ignorando comentarios y líneas en blanco: sirve para
    proponerle al usuario lo que le falta sin tocarle el archivo.
    """
    presentes = {linea.strip() for linea in existente.splitlines()}
    return [
        linea.strip()
        for linea in plantilla.splitlines()
        if linea.strip() and not linea.startswith("#") and linea.strip() not in presentes
    ]


def _iniciar_repositorio(project_root: Path, informar: Informar) -> None:
    if git.es_repositorio(project_root):
        informar(f"  Git         ya era un repositorio, no se toca "
                 f"(rama '{git.rama_actual(project_root) or 'sin commits'}')")
        return

    # `-b` fija el nombre de la rama inicial y evita depender de la
    # configuración de la máquina. No está en versiones de git anteriores a
    # 2.28, así que su ausencia no puede ser un fallo del arranque.
    completado = git.intentar(project_root, "init", "-b", RAMA_POR_DEFECTO)
    if completado.returncode != 0:
        git.ejecutar(project_root, "init")

    informar(f"  Git         repositorio creado (rama '{git.rama_actual(project_root)}')")


def _sembrar_gitignore(project_root: Path, informar: Informar) -> None:
    ruta = project_root / GITIGNORE_FILENAME
    plantilla = read_gitignore_template()

    if not ruta.exists():
        ruta.write_text(plantilla, encoding="utf-8")
        informar("  .gitignore  creado")
        return

    faltantes = reglas_que_faltan(ruta.read_text(encoding="utf-8"), plantilla)
    if not faltantes:
        informar("  .gitignore  ya existe y cubre las reglas base, no se toca")
        return

    informar(f"  .gitignore  ya existe, no se toca. Le faltan {len(faltantes)} reglas base:")
    for regla in faltantes:
        informar(f"                {regla}")


def _asegurar_identidad(project_root: Path, preguntar: Preguntar, informar: Informar) -> bool:
    """Comprueba que git sabe quién firma; si no, lo pregunta.

    Sin esto el `commit` falla con un mensaje largo y desconcertante justo
    después de que el usuario haya hecho todo bien. Preguntar cuesta dos líneas
    y es exactamente el tipo de diálogo que solo el script puede tener (C-007).

    Lo que se fije se fija **local** al repositorio: el arnés no reconfigura la
    máquina de nadie.
    """
    for clave, pregunta in (
        ("user.name", "Nombre para los commits"),
        ("user.email", "Email para los commits"),
    ):
        if git.configuracion(project_root, clave):
            continue

        valor = preguntar(f"{pregunta} ({clave} no está configurado): ").strip()
        if not valor:
            informar(f"  Identidad   falta '{clave}'; sin ella git no puede confirmar.")
            return False

        git.fijar_configuracion(project_root, clave, valor)
        informar(f"  Identidad   {clave} = {valor} (local a este repositorio)")

    return True


def _commit_inicial(project_root: Path, informar: Informar) -> bool:
    git.ejecutar(project_root, "add", "-A")

    if not git.hay_algo_que_confirmar(project_root):
        informar("  Commit      no hay cambios pendientes, nada que confirmar")
        return True

    try:
        git.commit(project_root, MENSAJE_COMMIT_INICIAL)
    except git.GitError as exc:
        informar(f"  Commit      FALLÓ: {exc}")
        return False

    informar(f"  Commit      '{MENSAJE_COMMIT_INICIAL}'")
    return True


def _pedir_url(preguntar: Preguntar, informar: Informar) -> str | None:
    """Pide la URL del remoto al humano. `None` si decide omitirla."""
    for intento in range(INTENTOS_DE_URL):
        url = preguntar(
            "URL del repositorio remoto (Enter para dejar el proyecto solo en local): "
        ).strip()

        if not url:
            return None
        if url_valida(url):
            return url

        quedan = INTENTOS_DE_URL - intento - 1
        informar(
            f"  '{url}' no tiene forma de URL de repositorio. "
            f"Se espera algo como 'https://github.com/usuario/repo.git' o "
            f"'git@github.com:usuario/repo.git'."
            + (f" Quedan {quedan} intentos." if quedan else "")
        )

    return None


def _configurar_remoto(
    project_root: Path, url: str, preguntar: Preguntar, informar: Informar
) -> bool:
    actual = git.url_del_remoto(project_root, REMOTO)

    if actual == url:
        informar(f"  Remoto      '{REMOTO}' ya apunta ahí, no se toca")
        return True

    if actual is not None:
        informar(f"  Remoto      '{REMOTO}' ya existe y apunta a {actual}")
        respuesta = preguntar(f"¿Reapuntarlo a {url}? [s/N]: ").strip().lower()
        if respuesta not in ("s", "si", "sí"):
            informar("  Remoto      se conserva el actual; no se hará push")
            return False
        git.ejecutar(project_root, "remote", "set-url", REMOTO, url)
        informar(f"  Remoto      '{REMOTO}' reapuntado a {url}")
        return True

    git.ejecutar(project_root, "remote", "add", REMOTO, url)
    informar(f"  Remoto      '{REMOTO}' → {url}")
    return True


def _diagnostico_de_push(stderr: str) -> str | None:
    """Traduce los fallos de push que ya nos han mordido antes.

    Solo los que tienen una corrección concreta que ofrecer; para el resto, el
    mensaje de git es mejor que cualquier paráfrasis.
    """
    if "GH007" in stderr or "email privacy" in stderr.lower():
        return (
            "GitHub bloquea los commits que usan un email protegido por privacidad "
            "(L-002). Usa la dirección noreply de tu cuenta:\n"
            "    git config --local user.email <id>+<usuario>@users.noreply.github.com\n"
            "    git commit --amend --reset-author --no-edit\n"
            "    git push -u origin <rama>"
        )
    if "Repository not found" in stderr or "repository not found" in stderr.lower():
        return (
            "El repositorio remoto no existe o la cuenta no tiene acceso. "
            "Créalo vacío en GitHub (sin README) y repite `soda start`."
        )
    if "rejected" in stderr and "fetch first" in stderr:
        return (
            "El remoto tiene commits que este repositorio no conoce. Intégralos con "
            "`git pull --rebase origin <rama>` y repite. No se fuerza el push."
        )
    return None


def _push(project_root: Path, informar: Informar) -> bool:
    rama = git.rama_actual(project_root)
    completado = git.intentar(project_root, "push", "-u", REMOTO, rama)

    if completado.returncode == 0:
        informar(f"  Push        rama '{rama}' publicada en '{REMOTO}'")
        return True

    stderr = (completado.stderr or "").strip()
    informar(f"  Push        FALLÓ (código {completado.returncode}):")
    for linea in stderr.splitlines():
        informar(f"                {linea}")

    pista = _diagnostico_de_push(stderr)
    if pista:
        informar("")
        informar(pista)

    return False


def bootstrap(
    project_root: Path,
    preguntar: Preguntar = input,
    informar: Informar = print,
) -> bool:
    """Deja un proyecto vacío listo para trabajar: Git, `.gitignore`, remoto y push.

    Idempotente: repetirlo sobre un proyecto ya arrancado no rompe nada, solo
    completa lo que falte. Nada se sobrescribe sin preguntar y ningún paso usa
    `--force`.

    Args:
        project_root: Raíz del proyecto destino (C-002: siempre explícita).
        preguntar: Cómo se le pregunta al humano. Recibe el texto y devuelve la
            respuesta.
        informar: Cómo se reporta cada paso.

    Returns:
        `True` si el proyecto quedó publicado en el remoto; `False` si quedó
        utilizable pero incompleto (sin remoto, o con el push fallido). Un
        `False` no significa que se haya roto nada.

    Raises:
        NotADirectoryError: Si `project_root` no existe o no es un directorio.
        SinCanalConElHumanoError: Si hacía falta preguntar algo y stdin está
            cerrada (entrada redirigida, CI).
        git.GitError: Si falla un paso de git del que no se puede seguir.
    """
    if not project_root.is_dir():
        raise NotADirectoryError(f"'{project_root}' no existe o no es un directorio.")

    if not git.esta_disponible():
        raise git.GitNoDisponibleError(
            "No se encontró `git` en el PATH. Instálalo para arrancar el proyecto."
        )

    informar(f"Arrancando proyecto en {project_root}")
    informar("")

    preguntar = _con_canal(preguntar)

    _iniciar_repositorio(project_root, informar)
    _sembrar_gitignore(project_root, informar)

    if not _asegurar_identidad(project_root, preguntar, informar):
        informar("")
        informar("Repositorio creado, pero sin identidad de git no hay commit inicial.")
        return False

    if not _commit_inicial(project_root, informar):
        return False

    url = _pedir_url(preguntar, informar)
    if url is None:
        informar("  Remoto      omitido")
        informar("")
        informar(
            "Proyecto arrancado en local. Cuando tengas la URL del repositorio, "
            "vuelve a ejecutar `soda start` para enlazarlo y publicarlo."
        )
        return False

    if not _configurar_remoto(project_root, url, preguntar, informar):
        return False

    if not _push(project_root, informar):
        return False

    informar("")
    informar("Proyecto arrancado y publicado. Ya puedes trabajar.")
    return True
