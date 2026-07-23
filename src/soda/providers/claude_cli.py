"""Proveedor que habla con Claude a través del CLI oficial `claude`.

Usa la suscripción (Claude Pro/Max) en vez de API de pago por token: invoca el
binario `claude` en modo no interactivo (`--print`) como subproceso y devuelve
lo que escriba en stdout.

El prompt se entrega por stdin, no como argumento, porque los prompts del arnés
(system prompt + contexto) superan con facilidad el límite de longitud de línea
de comandos de Windows.
"""

import shutil
import subprocess

from soda.core.provider import (
    Provider,
    ProviderExecutionError,
    ProviderNotFoundError,
    ProviderTimeoutError,
)

__all__ = ["ClaudeCLIProvider"]

DEFAULT_EXECUTABLE = "claude"
DEFAULT_TIMEOUT = 300.0


class ClaudeCLIProvider(Provider):
    """Provider respaldado por el CLI `claude` en modo `--print`."""

    def __init__(
        self,
        executable: str = DEFAULT_EXECUTABLE,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Args:
            executable: Nombre o ruta del binario del CLI. Se resuelve en PATH.
            timeout: Segundos máximos de espera por una respuesta.
        """
        self.executable = executable
        self.timeout = timeout

    def send(self, prompt: str) -> str:
        resolved = shutil.which(self.executable)
        if resolved is None:
            raise ProviderNotFoundError(
                f"No se encontró el ejecutable '{self.executable}' en el PATH. "
                "Instala el CLI de Claude Code o indica la ruta completa."
            )

        try:
            completed = subprocess.run(
                [resolved, "--print"],
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=self.timeout,
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
