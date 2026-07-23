"""Tests de T-022: el bucle REPL del orquestador.

Ninguna sesión real se abre aquí: se inyecta una `SesionEco` que "recuerda" el
contexto contando turnos, y las entradas del humano se guionizan con una lista
que hace de stdin. Así se prueba el bucle entero —contexto, comandos de salida,
EOF, errores— sin tocar la suscripción y sin que ningún test se bloquee. La
verificación contra el modelo real es el script en vivo `scripts/probar_repl.py`.

Las corrutinas se ejecutan con `asyncio.run` dentro de tests sync, igual que en
`test_sesion.py` y `test_claude_sdk.py`, para no añadir un plugin async a la suite.
"""

import asyncio

from soda.core.provider import ProviderError
from soda.core.sesion import Sesion
from soda.repl import correr_repl


class SesionEco(Sesion):
    """Doble de sesión: ecoa el turno con la cuenta acumulada (contexto simulado)."""

    def __init__(self, fallar_en: set[str] | None = None):
        self.turnos: list[str] = []
        self.fallar_en = fallar_en or set()
        self.abierta = False

    async def enviar(self, prompt: str) -> str:
        if prompt in self.fallar_en:
            raise ProviderError(f"fallo simulado en '{prompt}'")
        self.turnos.append(prompt)
        return f"eco {len(self.turnos)}: {prompt}"

    async def __aenter__(self):
        self.abierta = True
        return self

    async def __aexit__(self, *exc):
        self.abierta = False


class Guion:
    """stdin guionizado: entrega líneas en orden y luego levanta lo que se le diga.

    Al agotar la lista lanza `agota_con` (por defecto `EOFError`, el fin natural de
    stdin). Registra cada prompt recibido para poder afirmar sobre la interacción.
    """

    def __init__(self, lineas, agota_con=EOFError):
        self._lineas = list(lineas)
        self._agota_con = agota_con
        self.prompts: list[str] = []

    def __call__(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if not self._lineas:
            raise self._agota_con()
        return self._lineas.pop(0)


class Salida:
    """Acumula lo que el REPL escribe, para inspeccionarlo."""

    def __init__(self):
        self.lineas: list[str] = []

    def __call__(self, texto: str) -> None:
        self.lineas.append(texto)

    @property
    def texto(self) -> str:
        return "\n".join(self.lineas)


def _correr(sesion, leer, escribir, saludo=None):
    asyncio.run(correr_repl(sesion, leer=leer, escribir=escribir, saludo=saludo))


# --- Conversación y contexto ------------------------------------------------


def test_pasa_cada_turno_a_la_sesion_en_orden():
    sesion = SesionEco()
    _correr(sesion, Guion(["hola", "otra vez"]), Salida())

    assert sesion.turnos == ["hola", "otra vez"]


def test_escribe_la_respuesta_de_cada_turno():
    salida = Salida()
    _correr(SesionEco(), Guion(["hola", "adiós"]), salida)

    assert "eco 1: hola" in salida.lineas
    assert "eco 2: adiós" in salida.lineas


def test_muestra_el_saludo_antes_del_primer_turno():
    salida = Salida()
    _correr(SesionEco(), Guion([]), salida, saludo="informe de reanudación")

    assert salida.lineas[0] == "informe de reanudación"


def test_sin_saludo_no_escribe_nada_antes_de_leer():
    salida = Salida()
    _correr(SesionEco(), Guion([]), salida)

    # Solo el cierre por EOF, ninguna cabecera espuria.
    assert "informe" not in salida.texto


# --- Salida ordenada --------------------------------------------------------


def test_un_comando_de_salida_cierra_el_bucle():
    sesion = SesionEco()
    leer = Guion(["hola", "/salir", "no debería llegar"])
    _correr(sesion, leer, Salida())

    assert sesion.turnos == ["hola"]


def test_el_comando_de_salida_no_distingue_mayusculas():
    sesion = SesionEco()
    _correr(sesion, Guion(["/SALIR"]), Salida())

    assert sesion.turnos == []


def test_el_comando_de_salida_no_se_envia_como_turno():
    sesion = SesionEco()
    _correr(sesion, Guion(["/exit"]), Salida())

    assert sesion.turnos == []


def test_el_fin_de_stdin_cierra_sin_traza():
    salida = Salida()
    _correr(SesionEco(), Guion(["hola"], agota_con=EOFError), salida)

    assert "Sesión cerrada." in salida.lineas


def test_ctrl_c_cierra_sin_traza():
    salida = Salida()
    _correr(SesionEco(), Guion(["hola"], agota_con=KeyboardInterrupt), salida)

    assert "Sesión cerrada." in salida.lineas


# --- Entradas vacías y errores ----------------------------------------------


def test_una_linea_en_blanco_se_ignora_y_no_es_turno():
    sesion = SesionEco()
    _correr(sesion, Guion(["", "   ", "hola"]), Salida())

    assert sesion.turnos == ["hola"]


def test_un_error_del_modelo_no_tumba_el_bucle():
    sesion = SesionEco(fallar_en={"malo"})
    salida = Salida()
    _correr(sesion, Guion(["malo", "bueno"]), salida)

    # El turno bueno se procesa pese al fallo anterior: el contexto sobrevive.
    assert sesion.turnos == ["bueno"]
    assert any("[error]" in linea for linea in salida.lineas)
    assert "eco 1: bueno" in salida.lineas
