"""Proveedor que habla con Claude a través del CLI oficial `claude`.

Usa la suscripción (Claude Pro/Max) en vez de API de pago por token: invoca el
binario `claude` en modo no interactivo (`--print`) como subproceso y devuelve
lo que escriba en stdout.

El prompt se entrega por stdin, no como argumento, porque los prompts del arnés
(system prompt + contexto) superan con facilidad el límite de longitud de línea
de comandos de Windows.

Tres decisiones de invocación merecen explicación:

- **Suscripción garantizada, no esperada.** Si el entorno tiene
  `ANTHROPIC_API_KEY`, el CLI la prefiere y factura por token — justo lo que el
  proyecto existe para evitar. En vez de confiar en que nadie la tenga puesta,
  se elimina del entorno del subproceso. Si de verdad no hay suscripción, el CLI
  falla pidiendo login, que es un error honesto y accionable.
- **Sin herramientas por defecto.** Los agentes del arnés son texto que entra,
  texto que sale: Python les inyecta el contexto que necesitan y no hay razón
  para que el modelo navegue el disco. Cero herramientas significa además cero
  diálogos de permiso y un prompt portable a otro proveedor, que es lo que
  permite cambiar de modelo o de CLI sin reescribir el agente.
- **Sin persistir la sesión.** El subproceso corre dentro del proyecto destino;
  guardar cada invocación de agente en su historial lo ensuciaría sin que nadie
  vaya a reanudar ninguna de esas sesiones.

El modelo es argumento del constructor y no de `send` porque es configuración
del proveedor, no del mensaje: quien construye la flota decide qué modelo usa
cada agente, y el agente ni se entera.
"""

import os
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

from soda.core.provider import (
    Provider,
    ProviderExecutionError,
    ProviderNotFoundError,
    ProviderTimeoutError,
)

__all__ = ["ClaudeCLIProvider"]

DEFAULT_EXECUTABLE = "claude"
DEFAULT_TIMEOUT = 300.0

#: Variables de entorno que desviarían el CLI a facturación por token.
VARIABLES_DE_API = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")


class ClaudeCLIProvider(Provider):
    """Provider respaldado por el CLI `claude` en modo `--print`."""

    def __init__(
        self,
        executable: str = DEFAULT_EXECUTABLE,
        timeout: float = DEFAULT_TIMEOUT,
        model: str | None = None,
        tools: Sequence[str] | None = (),
        cwd: Path | None = None,
        solo_suscripcion: bool = True,
    ) -> None:
        """
        Args:
            executable: Nombre o ruta del binario del CLI. Se resuelve en PATH.
            timeout: Segundos máximos de espera por una respuesta.
            model: Alias (`haiku`, `sonnet`, `opus`) o nombre completo del
                modelo. `None` deja decidir al CLI.
            tools: Herramientas habilitadas. `()` —el valor por defecto— las
                desactiva todas; una secuencia de nombres habilita esos; `None`
                no toca el flag y deja el conjunto por defecto del CLI.
            cwd: Directorio de trabajo del subproceso. Normalmente la raíz del
                proyecto destino.
            solo_suscripcion: Si es verdadero, borra las credenciales de API del
                entorno del subproceso para forzar el uso de la suscripción.
        """
        self.executable = executable
        self.timeout = timeout
        self.model = model
        self.tools = tools
        self.cwd = cwd
        self.solo_suscripcion = solo_suscripcion

    def _argumentos(self, ejecutable: str) -> list[str]:
        """Arma el argv de la invocación, sin el prompt (va por stdin)."""
        argv = [ejecutable, "--print", "--no-session-persistence"]

        if self.model is not None:
            argv += ["--model", self.model]

        if self.tools is not None:
            argv += ["--tools", ",".join(self.tools)]

        return argv

    def _entorno(self) -> dict[str, str] | None:
        """Entorno del subproceso; `None` significa heredarlo tal cual."""
        if not self.solo_suscripcion:
            return None

        entorno = dict(os.environ)
        for variable in VARIABLES_DE_API:
            entorno.pop(variable, None)
        return entorno

    def send(self, prompt: str) -> str:
        resolved = shutil.which(self.executable)
        if resolved is None:
            raise ProviderNotFoundError(
                f"No se encontró el ejecutable '{self.executable}' en el PATH. "
                "Instala el CLI de Claude Code o indica la ruta completa."
            )

        try:
            completed = subprocess.run(
                self._argumentos(resolved),
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=self.timeout,
                cwd=self.cwd,
                env=self._entorno(),
            )
        except subprocess.TimeoutExpired as exc:
            raise ProviderTimeoutError(
                f"'{self.executable}' no respondió en {self.timeout} segundos."
            ) from exc
        except OSError as exc:
            raise ProviderNotFoundError(
                f"No se pudo ejecutar '{resolved}': {exc}"
            ) from exc

        if completed.returncode != 0:
            detalle = (completed.stderr or "").strip() or "sin salida en stderr"
            raise ProviderExecutionError(
                f"'{self.executable}' terminó con código {completed.returncode}: {detalle}"
            )

        return (completed.stdout or "").strip()
