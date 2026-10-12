"""
Módulo para obtener y filtrar repositorios públicos de un usuario de GitHub.
"""

from typing import Any, Dict, List


def obtener_repos(cliente: Any, usuario: str) -> List[Dict[str, Any]]:
    """Obtiene la lista de repositorios públicos del usuario llamando a la API REST

    de GitHub en el endpoint '/users/{usuario}/repos'.

    Args:
        cliente: Cliente de la API de GitHub que implementa el método rest().
        usuario (str): Nombre de usuario de GitHub.

    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con la información de los repositorios.
    """
    ruta = f"/users/{usuario}/repos"
    params = {"type": "owner", "per_page": 100}
    respuesta = cliente.rest(ruta, params)
    if isinstance(respuesta, list):
        return respuesta
    return []
