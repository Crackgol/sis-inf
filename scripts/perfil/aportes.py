"""
Módulo para el conteo de aportes de colaboradores.
"""

from typing import Any, Dict, List


def contar_aportes(
    prs: List[Dict[str, Any]],
    commits: List[Dict[str, Any]],
    config: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Calcula y ordena los aportes de PRs y commits por colaborador.

    Args:
        prs (List[Dict[str, Any]]): Lista de Pull Requests aceptados.
        commits (List[Dict[str, Any]]): Lista de commits directos.
        config (Dict[str, Any]): Diccionario de configuración con cuentas excluidas.

    Returns:
        List[Dict[str, Any]]: Lista con los aportes calculados.
    """
    return []
