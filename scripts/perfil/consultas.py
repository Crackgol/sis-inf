"""
Módulo para realizar consultas GraphQL y REST a la API de GitHub para obtener

aportes (PRs y lenguajes/issues).
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
    """Obtiene los lenguajes y bytes correspondientes por repositorio."""
    pass


def obtener_primeras_issues(
    cliente: Any, usuario: str
) -> Dict[str, Any]:
    """Busca las primeras issues abiertas etiquetadas como 'good first issue'."""
    pass
