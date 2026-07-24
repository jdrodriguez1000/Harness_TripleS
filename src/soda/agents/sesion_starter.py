"""`sesion-starter`: reconstruye el contexto de un proyecto y lo resume.

Primer agente del harness (D-028). Es el de menor riesgo de todos: solo lee, y
su peor caso es un informe equivocado en pantalla.

Cómo funciona: `soda.agents.memory` lee `_persistence/` en Python puro, esta
clase compone el prompt con lo leído y se lo pasa a un `Provider`. El agente no
recibe herramientas, no navega el disco y no sabe qué modelo hay detrás — quien
construye la flota decide eso al inyectarle el `Provider`. De ahí que cambiar de
`haiku` a otro modelo, o de Claude a otro CLI, no toque este archivo.

El caso de proyecto vacío no llega hasta aquí. Detectarlo es leer dos archivos y
compararlos con su plantilla, algo que Python resuelve gratis; y lo que sigue
—bootstrap de Git, pedirle al humano la URL del remoto— ni siquiera es posible
desde un `claude -p`, que no tiene canal con el humano (C-007). El agente que
reconstruye contexto de sesiones anteriores no tiene nada que hacer cuando no
hay ninguna.
"""

from pathlib import Path

from soda.agents.memory import MemoriaProyecto, leer_memoria
from soda.agents.prompts import read_prompt
from soda.core.provider import Provider

__all__ = ["PROMPT", "MemoriaVaciaError", "SesionStarter", "componer_prompt"]

PROMPT = "sesion_starter.md"


class MemoriaVaciaError(Exception):
    """Se invocó al starter sobre un proyecto sin memoria escrita."""


def _bloque(titulo: str, cuerpo: str) -> str:
    """Envuelve el contenido de un archivo con su nombre y una cerca literal.

    La cerca evita que los encabezados del archivo se lean como estructura del
    prompt: la memoria está llena de `##` y de tablas, y sin delimitar sería
    imposible distinguir una instrucción de un dato.
    """
    return f"## {titulo}\n\n````markdown\n{cuerpo.strip()}\n````"


def componer_prompt(memoria: MemoriaProyecto) -> str:
    """Arma el prompt completo: instrucciones del agente + memoria leída.

    Args:
        memoria: Lo que `leer_memoria` encontró en el proyecto destino.

    Returns:
        El texto que se le envía al modelo.
    """
    partes = [read_prompt(PROMPT).strip(), "# Memoria del proyecto"]

    for nombre, contenido in memoria.completos.items():
        partes.append(_bloque(f"{nombre} (íntegro)", contenido))

    for nombre, indice in memoria.indices.items():
        cuerpo = indice or "_(este archivo no tiene sección de índice)_"
        partes.append(_bloque(f"{nombre} (solo índice)", cuerpo))

    if memoria.faltantes:
        partes.append(
            "## Archivos ausentes\n\n"
            "Estos archivos que la convención declara no están en el disco. "
            "Repórtalo como alerta:\n\n"
            + "\n".join(f"- `{nombre}`" for nombre in memoria.faltantes)
        )

    return "\n\n".join(partes) + "\n"


class SesionStarter:
    """Agente que entrega el informe de reanudación de un proyecto."""

    def __init__(self, provider: Provider) -> None:
        """
        Args:
            provider: Proveedor ya configurado con su modelo. El agente no lo
                elige ni lo construye.
        """
        self.provider = provider

    def informe(self, project_root: Path) -> str:
        """Lee la memoria de `project_root` y devuelve el informe del modelo.

        Args:
            project_root: Raíz del proyecto destino (C-002: siempre explícita).

        Returns:
            El informe de reanudación, tal como lo escribió el modelo.

        Raises:
            MemoriaAusenteError: Si el proyecto no tiene `_persistence/`.
            MemoriaVaciaError: Si la memoria obligatoria sigue sin escribir; ese
                caso lo resuelve `soda start` en Python, no este agente.
            ProviderError: Si no se pudo obtener respuesta del modelo.
        """
        memoria = leer_memoria(project_root)

        if memoria.vacia:
            raise MemoriaVaciaError(
                f"La memoria de '{project_root}' está sin escribir: no hay sesiones "
                "anteriores que reconstruir. Este caso lo resuelve `soda start`."
            )

        return self.provider.send(componer_prompt(memoria))
