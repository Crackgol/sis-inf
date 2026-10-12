"""
Módulo para realizar consultas GraphQL y REST a la API de GitHub para obtener

aportes (PRs y lenguajes/issues).
"""

from typing import Any, Dict, List, Tuple


def obtener_aportes(
    cliente: Any, usuario: str, nombres_repos: List[str]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Obtiene los PRs fusionados y los commits directos del usuario."""
    pass


def obtener_lenguajes(
    cliente: Any, usuario: str, nombres_repos: List[str]
) -> Dict[str, Dict[str, int]]:
    """Obtiene los lenguajes y bytes correspondientes por repositorio."""
    pass


def obtener_primeras_issues(
    cliente: Any, usuario: str
) -> Dict[str, Any]:
    """Busca las primeras issues abiertas etiquetadas como 'good first issue'."""
    pass
