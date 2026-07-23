"""Contrato de una sesión de modelo que mantiene contexto entre turnos.

`Provider.send` (ver `soda.core.provider`) es de un solo disparo: prompt entra,
texto sale, sin memoria de lo anterior. Sirve para agentes que no conversan
—leen algo y emiten un informe— pero no para el orquestador REPL persistente
(D-035), que necesita recordar los turnos previos.

`Sesion` es esa segunda frontera. Un objeto sesión se abre una vez, recibe
varios turnos manteniendo el contexto, y se cierra al final. Igual que
`Provider`, es una abstracción: los consumidores programan contra ella y nunca
contra un backend concreto (protege D-006/D-008), de modo que el SDK que haya
por debajo —hoy el Claude Agent SDK— no se filtra al resto del arnés.

La sesión es **asíncrona** porque el backend que la motiva lo es: un
`ClaudeSDKClient` vivo requiere un bucle de eventos vivo. Se modela como
gestor de contexto async (`async with`) para que abrir y cerrar el recurso sean
explícitos y a prueba de fugas.

Los errores reutilizan la jerarquía `ProviderError` de `soda.core.provider`: un
fallo al hablar con el modelo es el mismo tipo de fallo, venga de un disparo o
de una sesión, y no hay razón para que el consumidor distinga dos familias.
"""

from abc import ABC, abstractmethod

__all__ = ["Sesion"]


class Sesion(ABC):
    """Sesión de modelo multi-turno; gestor de contexto asíncrono.

    Uso:

        async with proveedor.abrir_sesion() as sesion:
            print(await sesion.enviar("primer turno"))
            print(await sesion.enviar("segundo turno, recuerda el primero"))
    """

    @abstractmethod
    async def enviar(self, prompt: str) -> str:
        """Envía un turno y devuelve el texto de la respuesta del modelo.

        El contexto de los turnos anteriores se conserva: cada llamada continúa
        la misma conversación.

        Args:
            prompt: Texto del turno a enviar.

        Returns:
            El texto de la respuesta, sin decoración añadida por el backend.

        Raises:
            ProviderError: Si no se pudo obtener una respuesta.
        """
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> "Sesion":
        """Abre la sesión viva y la devuelve lista para recibir turnos."""
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        """Cierra la sesión y libera el recurso del backend."""
        raise NotImplementedError
