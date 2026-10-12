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
    prs: List[Dict[str, Any]],
    commits: List[Dict[str, Any]],
    config: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Cuenta los aportes totales (PRs fusionados y commits directos) por usuario,

    aplicando los filtros de exclusión y ordenamiento requeridos.

    Args:
        prs (List[Dict[str, Any]]): Lista de Pull Requests fusionados.
        commits (List[Dict[str, Any]]): Lista de commits directos.
        config (Dict[str, Any]): Diccionario de configuración con 'cuentas_excluidas'.

    Returns:
        List[Dict[str, Any]]: Lista de aportes por usuario ordenada según el contrato.
    """
    # Obtener cuentas excluidas de la configuración (normalizadas a minúsculas o tal cual se definan)
    cuentas_excluidas = set(config.get("cuentas_excluidas", []))

    # Estructura temporal para llevar el conteo: {login: {"prs": int, "commits": int}}
    estadisticas: Dict[str, Dict[str, int]] = {}

    def debe_excluirse(login_usuario: str) -> bool:
        """Determina si un usuario debe ser excluido según las reglas del issue."""
        if not login_usuario or login_usuario == "ghost":
            return True
        if login_usuario.endswith("[bot]"):
            return True
        if login_usuario in cuentas_excluidas:
            return True
        return False

    # Procesar PRs fusionados
    for pr in prs:
        if not isinstance(pr, dict):
            continue
        autor_raw = pr.get("autor")
        login = obtener_login(autor_raw)

        if debe_excluirse(login):
            continue

        if login not in estadisticas:
            estadisticas[login] = {"prs": 0, "commits": 0}
        estadisticas[login]["prs"] += 1

    # Procesar commits directos
    for commit in commits:
        if not isinstance(commit, dict):
            continue
        autor_raw = commit.get("autor")
        login = obtener_login(autor_raw)

        if debe_excluirse(login):
            continue

        if login not in estadisticas:
            estadisticas[login] = {"prs": 0, "commits": 0}
        estadisticas[login]["commits"] += 1

    # Construir la lista de resultados en el formato requerido
    resultado: List[Dict[str, Any]] = []
    for login, datos in estadisticas.items():
        total_prs = datos["prs"]
        total_commits = datos["commits"]
        aportes = total_prs + total_commits

        resultado.append({
            "login": login,
            "prs": total_prs,
            "commits": total_commits,
            "aportes": aportes
        })

    # Ordenar según el contrato:
    # 1. aportes (descendente)
    # 2. prs (descendente)
    # 3. login (ascendente / alfabético)
    resultado.sort(key=lambda x: (-x["aportes"], -x["prs"], x["login"]))

    return resultado
