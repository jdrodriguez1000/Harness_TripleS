"""Implementaciones concretas del contrato `soda.core.provider.Provider`.

Cada módulo de este paquete adapta un backend real (un CLI de suscripción, una
API con key) a la interfaz común. Añadir un proveedor nuevo es añadir un módulo
aquí; ni los agentes ni las tools cambian.
"""

from soda.providers.claude_cli import ClaudeCLIProvider
from soda.providers.claude_sdk import ClaudeSDKProvider, SesionClaudeSDK

__all__ = ["ClaudeCLIProvider", "ClaudeSDKProvider", "SesionClaudeSDK"]
