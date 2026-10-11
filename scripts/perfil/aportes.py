"""
Módulo para el conteo de aportes de colaboradores.
"""

from typing import Any, Dict, List


def contar_aportes(
    prs: List[Dict[str, Any]],
    commits: List[Dict[str, Any]],
    config: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Calcula y ordena los aportes de PRs y commits por colaborador."""
    cuentas_excluidas = set(config.get("cuentas_excluidas", []))

    def obtener_login(item: Dict[str, Any]) -> str:
        """Extrae el login del autor de forma robusta."""
        if "login" in item and isinstance(item["login"], str):
            return item["login"]
        for key in ("author", "user", "committer"):
            if key in item and isinstance(item[key], dict):
                if "login" in item[key]:
                    return item[key]["login"]
        return item.get("author", "")

    def es_valido(login: str) -> bool:
        """Verifica si el login es válido según las reglas de exclusión."""
        if not login or login in cuentas_excluidas:
            return False
        if login.lower() == "ghost" or login.endswith("[bot]"):
            return False
        return True

    return []
