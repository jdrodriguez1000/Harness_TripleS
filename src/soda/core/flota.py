"""Qué modelo usa cada agente. El único sitio donde eso está escrito.

Los agentes no eligen su proveedor: lo reciben ya construido. Esa inversión es
lo que hace barato cambiar de modelo —o de proveedor entero— sin tocar ningún
agente, y aquí es donde se cobra el beneficio: cambiar `sesion-starter` de
`haiku` a otro modelo es editar una línea de `MODELOS`, y moverlo a otro CLI es
cambiar la clase que construye `proveedor_para`.

El mapa es un diccionario en código y no un archivo de configuración a
propósito. Hoy hay un agente; inventar un formato de configuración, su lectura,
su validación y sus errores para un diccionario de una entrada sería construir
la solución de un problema que todavía no existe. Se convierte en archivo
cuando el usuario necesite cambiar el modelo sin editar el paquete.

Criterio para elegir modelo: el trabajo que hace el agente, no su importancia.
`sesion-starter` resume archivos que ya tiene delante —no razona sobre código ni
decide nada— y eso lo hace bien un modelo pequeño. La cuota de suscripción es el
presupuesto real del arnés (C-006), y gastarla en un modelo grande para resumir
seis archivos es gastarla mal.
"""

from pathlib import Path

from soda.core.provider import Provider
from soda.providers import ClaudeCLIProvider

__all__ = ["MODELOS", "proveedor_para"]

#: Agente → modelo. Cambiar de modelo es cambiar el valor.
MODELOS: dict[str, str] = {
    "sesion-starter": "haiku",
}


def proveedor_para(agente: str, project_root: Path) -> Provider:
    """Construye el proveedor que le toca a `agente`.

    Args:
        agente: Nombre del agente, una clave de `MODELOS`.
        project_root: Raíz del proyecto destino; el subproceso corre ahí.

    Returns:
        Un `Provider` listo para usar, sin herramientas y sobre la suscripción.

    Raises:
        KeyError: Si `agente` no tiene modelo asignado.
    """
    if agente not in MODELOS:
        raise KeyError(
            f"'{agente}' no tiene modelo asignado. Conocidos: {', '.join(MODELOS)}"
        )

    return ClaudeCLIProvider(model=MODELOS[agente], cwd=project_root)
