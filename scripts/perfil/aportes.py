"""
Módulo para el conteo de aportes de colaboradores (Pull Requests y commits).
"""

from typing import Any, Dict, List


def contar_aportes(
    prs: List[Dict[str, Any]],
    commits: List[Dict[str, Any]],
    config: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Calcula y ordena los aportes de PRs y commits por colaborador,

    excluyendo cuentas excluidas, 'ghost' y cuentas de bots.

    Args:
        prs (List[Dict[str, Any]]): Lista de Pull Requests aceptados.
        commits (List[Dict[str, Any]]): Lista de commits directos.
        config (Dict[str, Any]): Diccionario de configuración que incluye
          'cuentas_excluidas'.

    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con la estructura
        [{'login': str, 'prs': int, 'commits': int, 'aportes': int}]
        ordenada por aportes (descendente), prs (descendente) y login (ascendente).
    """
    cuentas_excluidas = set(config.get("cuentas_excluidas", []))
    conteo: Dict[str, Dict[str, int]] = {}

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

    # Procesar PRs
    for pr in prs:
        login = obtener_login(pr)
        if es_valido(login):
            if login not in conteo:
                conteo[login] = {"prs": 0, "commits": 0}
            conteo[login]["prs"] += 1

    # Procesar commits
    for commit in commits:
        login = obtener_login(commit)
        if es_valido(login):
            if login not in conteo:
                conteo[login] = {"prs": 0, "commits": 0}
            conteo[login]["commits"] += 1

    # Construir lista de resultados
    resultado = []
    for login, datos in conteo.items():
        prs_count = datos["prs"]
        commits_count = datos["commits"]
        resultado.append(
            {
                "login": login,
                "prs": prs_count,
                "commits": commits_count,
                "aportes": prs_count + commits_count,
            }
        )

    # Ordenar por aportes (descendente), luego prs (descendente) y login (ascendente)
    resultado.sort(key=lambda x: (-x["aportes"], -x["prs"], x["login"]))

    return resultado
