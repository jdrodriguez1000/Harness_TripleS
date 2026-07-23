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
from soda.providers import ClaudeCLIProvider, ClaudeSDKProvider

__all__ = [
    "MODELOS",
    "ORQUESTADOR",
    "PROMPT_ORQUESTADOR",
    "proveedor_de_sesion_para",
    "proveedor_para",
]

#: Nombre del orquestador REPL persistente en `MODELOS`. No es un agente de un
#: disparo como `sesion-starter`: es la sesión viva con la que conversa el humano
#: (T-022). Constante para que nadie lo teclee mal en dos sitios.
ORQUESTADOR = "orquestador"

#: Agente → modelo. Cambiar de modelo es cambiar el valor.
#:
#: El criterio sigue siendo el trabajo, no la importancia (ver cabecera): el
#: `orquestador` sí razona y decide —conduce la conversación y, más adelante,
#: delega en subagentes—, así que se le da el modelo grande. `sesion-starter`
#: solo resume y le basta uno pequeño.
MODELOS: dict[str, str] = {
    "sesion-starter": "haiku",
    ORQUESTADOR: "opus",
}

#: System prompt mínimo del orquestador. Hoy solo fija idioma y tono: en T-022 el
#: orquestador es un interlocutor coherente sin herramientas. La memoria como tool
#: (T-023/T-024) y la delegación en subagentes (T-025/T-026) ampliarán este prompt;
#: por eso vive aquí, junto al modelo, y no incrustado en el bucle REPL.
PROMPT_ORQUESTADOR = (
    "Eres el orquestador de `soda`, un arnés de IA que acompaña la construcción de "
    "software paso a paso. Conversas en español con la persona que dirige el "
    "proyecto. Responde con claridad y sin rodeos, y pregunta cuando te falte "
    "información en vez de suponer."
)


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


def proveedor_de_sesion_para(agente: str, project_root: Path) -> ClaudeSDKProvider:
    """Construye el proveedor de sesión persistente que le toca a `agente`.

    Hermano de `proveedor_para`, pero para el otro contrato: donde aquel entrega
    un `Provider` de un disparo, este entrega un `ClaudeSDKProvider` que abre
    sesiones multi-turno con memoria de contexto (D-038). Lo usa el orquestador
    REPL (T-022); los agentes de un solo turno siguen con `proveedor_para`.

    Args:
        agente: Nombre del agente, una clave de `MODELOS`.
        project_root: Raíz del proyecto destino; el subproceso corre ahí.

    Returns:
        Un `ClaudeSDKProvider` sobre la suscripción, con el modelo del agente y,
        para el orquestador, su system prompt.

    Raises:
        KeyError: Si `agente` no tiene modelo asignado.
    """
    if agente not in MODELOS:
        raise KeyError(
            f"'{agente}' no tiene modelo asignado. Conocidos: {', '.join(MODELOS)}"
        )

    system_prompt = PROMPT_ORQUESTADOR if agente == ORQUESTADOR else None
    return ClaudeSDKProvider(
        model=MODELOS[agente],
        system_prompt=system_prompt,
        cwd=project_root,
    )
