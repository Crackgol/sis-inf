"""
Módulo para procesar y contar aportes (pull requests y commits) de colaboradores
en los repositorios de GitHub.
"""

from typing import Any, Dict, List


def obtener_login(autor: Any) -> str:
    """Extrae de forma segura el login de un autor, manejando valores nulos,

    cadenas, diccionarios o estructuras inesperadas.

    Args:
        autor (Any): Objeto, diccionario o cadena que representa al autor.

    Returns:
        str: El nombre de usuario (login) extraído o 'ghost' por defecto.
    """
    if not autor:
        return "ghost"

    if isinstance(autor, str):
        return autor.strip() or "ghost"

    if isinstance(autor, dict):
        login = autor.get("login") or autor.get("name")
        if login and isinstance(login, str):
            return login.strip()
        return "ghost"

    if hasattr(autor, "login"):
        login = getattr(autor, "login")
        if login:
            return str(login).strip()

    return "ghost"


def contar_aportes(
    prs: List[Dict[str, Any]], commits: List[Dict[str, Any]]
) -> Dict[str, int]:
    """Cuenta los aportes totales (PRs fusionados y commits directos) por usuario.

    Args:
        prs (List[Dict[str, Any]]): Lista de Pull Requests fusionados.
        commits (List[Dict[str, Any]]): Lista de commits directos.

    Returns:
        Dict[str, int]: Diccionario con el conteo de aportes por cada usuario.
    """
    conteo: Dict[str, int] = {}

    # Procesar PRs fusionados
    for pr in prs:
        if not isinstance(pr, dict):
            continue
        autor_raw = pr.get("autor")
        login = obtener_login(autor_raw)
        conteo[login] = conteo.get(login, 0) + 1

    # Procesar commits directos
    for commit in commits:
        if not isinstance(commit, dict):
            continue
        autor_raw = commit.get("autor")
        login = obtener_login(autor_raw)
        conteo[login] = conteo.get(login, 0) + 1

    return conteo
