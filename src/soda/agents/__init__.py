"""Agentes propios del harness.

Un agente de `soda` es una clase que arma un prompt, se lo pasa a un `Provider`
y devuelve el texto que responde el modelo. No lee el disco por su cuenta: el
contexto que necesita se lo inyecta Python antes de invocar (ver
`soda.agents.memory`). Esa separación es la que permite cambiar de modelo o de
proveedor sin tocar el agente, y probarlo sin gastar cuota.

No confundir con los agentes de Claude Code de este repositorio, que son
andamiaje para construir el harness y no viajan en el paquete (C-004).
"""
