"""
Módulo para realizar consultas GraphQL y REST a la API de GitHub para obtener

aportes (PRs y commits), lenguajes de repositorios y primeras issues.
"""

from typing import Any, Dict, List, Tuple


def obtener_aportes(
    cliente: Any, usuario: str, nombres_repos: List[str]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Obtiene los PRs fusionados (MERGED) y los commits directos del usuario en

    los repositorios indicados mediante GraphQL con paginación.

    Args:
        cliente: Cliente GraphQL.
        usuario (str): Nombre de usuario de GitHub.
        nombres_repos (List[str]): Lista de repositorios ('owner/name').

    Returns:
        Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]: (prs, commits)
    """
    query_prs = """
    query($owner: String!, $name: String!, $cursor: String) {
      repository(owner: $owner, name: $name) {
        pullRequests(states: [MERGED], first: 100, after: $cursor) {
          pageInfo { hasNextPage endCursor }
          nodes { author { login } }
        }
      }
    }
    """

    query_commits = """
    query($owner: String!, $name: String!, $cursor: String) {
      repository(owner: $owner, name: $name) {
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 100, after: $cursor) {
                pageInfo { hasNextPage endCursor }
                nodes {
                  oid
                  parents { totalCount }
                  author { user { login } }
                  associatedPullRequests { totalCount }
                }
              }
            }
          }
        }
      }
    }
    """

    prs_resultado: List[Dict[str, Any]] = []
    commits_resultado: List[Dict[str, Any]] = []

    for repo_full_name in nombres_repos:
        if "/" not in repo_full_name:
            continue
        owner, name = repo_full_name.split("/", 1)

        # 1. Obtener PRs MERGED con paginación
        cursor = None
        while True:
            variables = {"owner": owner, "name": name, "cursor": cursor}
            data = cliente.graphql(query_prs, variables)
            repo_data = data.get("data", {}).get("repository") if data else None
            if not repo_data or not repo_data.get("pullRequests"):
                break

            pr_conn = repo_data["pullRequests"]
            for node in pr_conn.get("nodes", []):
                if not node:
                    continue
                author_obj = node.get("author")
                autor = (
                    author_obj.get("login")
                    if author_obj and author_obj.get("login")
                    else "ghost"
                )
                prs_resultado.append({"repo": repo_full_name, "autor": autor})

            page_info = pr_conn.get("pageInfo", {})
            if page_info.get("hasNextPage"):
                cursor = page_info.get("endCursor")
            else:
                break

        # 2. Obtener Commits Directos con paginación y filtros
        cursor = None
        while True:
            variables = {"owner": owner, "name": name, "cursor": cursor}
            data = cliente.graphql(query_commits, variables)
            repo_data = data.get("data", {}).get("repository") if data else None
            if not repo_data or not repo_data.get("defaultBranchRef"):
                break

            target = repo_data["defaultBranchRef"].get("target")
            if not target or "history" not in target:
                break

            history = target["history"]
            for node in history.get("nodes", []):
                if not node:
                    continue

                sha = node.get("oid", "")

                # Descartar si llegaron por un PR
                if node.get("associatedPullRequests", {}).get("totalCount", 0) > 0:
                    continue

                # Descartar commits de fusión (parents.totalCount > 1)
                if node.get("parents", {}).get("totalCount", 0) > 1:
                    continue

                # Descartar si author.user es null
                author_obj = node.get("author")
                if not author_obj or not author_obj.get("user"):
                    continue

                autor = author_obj["user"].get("login", "")
                if not autor:
                    continue

                commits_resultado.append(
                    {"repo": repo_full_name, "autor": autor, "sha": sha}
                )

            page_info = history.get("pageInfo", {})
            if page_info.get("hasNextPage"):
                cursor = page_info.get("endCursor")
            else:
                break

    return prs_resultado, commits_resultado


def obtener_lenguajes(
    cliente: Any, usuario: str, nombres_repos: List[str]
) -> Dict[str, Dict[str, int]]:
    """Obtiene los lenguajes utilizados y sus bytes correspondientes por cada

    repositorio llamando al endpoint REST '/repos/{owner}/{repo}/languages'.

    Args:
        cliente: Cliente REST.
        usuario (str): Nombre de usuario de GitHub.
        nombres_repos (List[str]): Lista de repositorios ('owner/name').

    Returns:
        Dict[str, Dict[str, int]]: Diccionario estructurado como {repo: {lenguaje: bytes}}
    """
    resultado: Dict[str, Dict[str, int]] = {}

    for repo_full_name in nombres_repos:
        endpoint = f"/repos/{repo_full_name}/languages"
        respuesta = cliente.get(endpoint) if hasattr(cliente, "get") else cliente(endpoint)
        if isinstance(respuesta, dict):
            resultado[repo_full_name] = respuesta
        else:
            resultado[repo_full_name] = {}

    return resultado


def obtener_primeras_issues(
    cliente: Any, usuario: str
) -> Dict[str, Any]:
    """Busca las primeras issues abiertas con la etiqueta 'good first issue' del

    usuario usando la búsqueda REST '/search/issues'.

    Args:
        cliente: Cliente REST.
        usuario (str): Nombre de usuario de GitHub.

    Returns:
        Dict[str, Any]: Diccionario con el formato:
        {'total': int, 'items': [{'titulo': str, 'url': str, 'repo': str}]}
    """
    q = f"user:{usuario} label:\"good first issue\" state:open is:issue"
    endpoint = f"/search/issues?q={q}"

    respuesta = cliente.get(endpoint) if hasattr(cliente, "get") else cliente(endpoint)
    if not isinstance(respuesta, dict):
        return {"total": 0, "items": []}

    total_count = respuesta.get("total_count", 0)
    items_raw = respuesta.get("items", [])

    items_procesados = []
    for item in items_raw:
        titulo = item.get("title", "")
        url = item.get("html_url", "")
        repository_url = item.get("repository_url", "")

        repo = ""
        if repository_url:
            parts = repository_url.split("/repos/")
            if len(parts) > 1:
                repo = parts[1]

        items_procesados.append(
            {"titulo": titulo, "url": url, "repo": repo}
        )

    return {"total": total_count, "items": items_procesados}
