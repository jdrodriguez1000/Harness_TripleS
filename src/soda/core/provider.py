"""Contrato mínimo que todo proveedor de modelo debe cumplir.

Un `Provider` traduce "mándale este prompt a un modelo y devuélveme el texto" a
lo que sea que necesite el backend concreto: invocar un CLI de suscripción como
subproceso (desarrollo) o llamar a una API con key (producción). Los agentes y
las tools programan contra esta interfaz y nunca contra un backend concreto.

La interfaz arranca deliberadamente pequeña: un solo método `send`. Modelo
configurable, system prompt, streaming y demás se añaden cuando haya un caso de
uso real que los pida.
"""

from abc import ABC, abstractmethod

__all__ = [
    "Provider",
    "ProviderError",
    "ProviderNotFoundError",
    "ProviderTimeoutError",
    "ProviderExecutionError",
]


class ProviderError(Exception):
    """Fallo al obtener una respuesta de un proveedor."""


class ProviderNotFoundError(ProviderError):
    """El backend del proveedor no está disponible (CLI no instalado, no en PATH)."""


class ProviderTimeoutError(ProviderError):
    """El proveedor no respondió dentro del tiempo permitido."""


class ProviderExecutionError(ProviderError):
    """El proveedor se ejecutó pero terminó en error."""


class Provider(ABC):
    """Interfaz común a todos los proveedores de modelo."""

    @abstractmethod
    def send(self, prompt: str) -> str:
        """Envía `prompt` al modelo y devuelve el texto de la respuesta.

        Args:
            prompt: Texto a enviar al modelo.

        Returns:
            El texto de la respuesta, sin decoración añadida por el backend.

        Raises:
            ProviderError: Si no se pudo obtener una respuesta.
        """
        raise NotImplementedError
