"""Bucle REPL del orquestador: el canal en vivo entre el humano y `soda` (T-022).

`SesionClaudeSDK` (T-021) mantiene el contexto entre turnos, pero por sí sola no
habla con nadie: es una sesión que hay que alimentar. Este módulo es quien la
alimenta. Enciende la conversación, lee lo que teclea el humano, se lo pasa a la
sesión, escribe la respuesta y espera el siguiente turno. Eso es lo que cierra la
parte de C-007 que seguía abierta para el orquestador: un `claude -p` de un
disparo no puede sostener este ida y vuelta; un proceso vivo con stdin, sí.

El diálogo entra por `leer` y sale por `escribir` en vez de llamar a `input()` y
`print()` directamente, igual que `soda.start` usa `preguntar`/`informar`. No es
ceremonia: es lo que permite probar el bucle entero —incluida la salida por EOF o
por comando— sin que ningún test se quede esperando a que alguien teclee, y sin
abrir una sesión real contra la suscripción.

Sobre por qué es async: la `Sesion` lo es (un `ClaudeSDKClient` vivo necesita un
bucle de eventos vivo), así que el REPL también. La lectura de stdin es
bloqueante y no pasa nada: en el bucle no corre nada en paralelo con la espera
del humano, de modo que bloquear ahí no le roba tiempo a nadie.
"""

from collections.abc import Callable

from soda.core.provider import ProviderError
from soda.core.sesion import Sesion

__all__ = ["COMANDOS_DE_SALIDA", "correr_repl"]

Leer = Callable[[str], str]
Escribir = Callable[[str], None]

#: Formas explícitas de pedir el fin de la conversación. En minúsculas: la
#: comparación normaliza antes de mirar aquí.
COMANDOS_DE_SALIDA = frozenset({"/salir", "/exit", "/quit"})

PROMPT_TURNO = "> "


async def correr_repl(
    sesion: Sesion,
    leer: Leer = input,
    escribir: Escribir = print,
    saludo: str | None = None,
) -> None:
    """Conversa con `sesion` turno a turno hasta que el humano cierra.

    La sesión debe entrar **ya abierta** (`async with proveedor.abrir_sesion()`):
    este bucle usa el contexto vivo, no gestiona su ciclo de vida. Así el cierre
    de la sesión ocurre siempre, incluso si el bucle sale por una excepción, y
    queda en manos de quien la abrió.

    Termina de forma ordenada de tres maneras, todas sin traza: un comando de
    salida (`COMANDOS_DE_SALIDA`), el fin de la entrada (`EOFError`, típico al
    redirigir stdin o al pulsar Ctrl-Z/Ctrl-D), o una interrupción
    (`KeyboardInterrupt`, Ctrl-C).

    Un fallo al hablar con el modelo (`ProviderError`) se reporta pero no tumba la
    conversación: un turno que falla no debería tirar el contexto acumulado de
    todos los anteriores.

    Args:
        sesion: Sesión persistente ya abierta.
        leer: Cómo se le pide un turno al humano. Recibe el prompt y devuelve la
            línea tecleada.
        escribir: Cómo se muestra cada respuesta o aviso.
        saludo: Texto a mostrar antes del primer turno (p. ej. el informe de
            reanudación). `None` no muestra nada.
    """
    if saludo:
        escribir(saludo)

    while True:
        try:
            entrada = leer(PROMPT_TURNO)
        except (EOFError, KeyboardInterrupt):
            escribir("")
            escribir("Sesión cerrada.")
            return

        turno = entrada.strip()
        if not turno:
            continue
        if turno.lower() in COMANDOS_DE_SALIDA:
            escribir("Sesión cerrada.")
            return

        try:
            respuesta = await sesion.enviar(turno)
        except ProviderError as exc:
            escribir(f"[error] el modelo no pudo responder: {exc}")
            continue

        escribir(respuesta)
