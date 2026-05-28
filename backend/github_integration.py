from __future__ import annotations

import os
from typing import Any

import httpx


GITHUB_API_BASE = "https://api.github.com"
GITHUB_API_VERSION = "2022-11-28"


class GitHubIntegrationError(RuntimeError):
    pass


def github_token() -> str:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT") or ""


def is_configured() -> bool:
    return bool(github_token())


def auth_headers() -> dict[str, str]:
    token = github_token()
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
        "User-Agent": "lua-bim-labs-local-orchestrator",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def safe_user_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "login": payload.get("login"),
        "id": payload.get("id"),
        "name": payload.get("name"),
        "type": payload.get("type"),
        "plan": payload.get("plan", {}).get("name") if isinstance(payload.get("plan"), dict) else None,
    }


def parse_rate_limit(headers: httpx.Headers) -> dict[str, Any]:
    return {
        "limit": headers.get("x-ratelimit-limit"),
        "remaining": headers.get("x-ratelimit-remaining"),
        "reset": headers.get("x-ratelimit-reset"),
        "resource": headers.get("x-ratelimit-resource"),
    }


def parse_scopes(headers: httpx.Headers) -> list[str]:
    raw = headers.get("x-oauth-scopes", "")
    return sorted(scope.strip() for scope in raw.split(",") if scope.strip())


async def github_get(path: str, params: dict[str, Any] | None = None) -> tuple[dict[str, Any] | list[Any], httpx.Headers]:
    if not path.startswith("/"):
        path = f"/{path}"
    async with httpx.AsyncClient(timeout=12) as client:
        response = await client.get(f"{GITHUB_API_BASE}{path}", headers=auth_headers(), params=params)
    if response.status_code >= 400:
        detail = response.json().get("message", response.text) if response.content else response.text
        raise GitHubIntegrationError(f"GitHub API error {response.status_code}: {detail}")
    return response.json(), response.headers


async def check_connection() -> dict[str, Any]:
    if not is_configured():
        public_payload, public_headers = await github_get("/rate_limit")
        return {
            "configured": False,
            "authenticated": False,
            "status": "missing_token",
            "message": "GITHUB_TOKEN 또는 GITHUB_PAT 환경변수가 필요합니다.",
            "rate_limit": parse_rate_limit(public_headers),
            "resources": public_payload.get("resources", {}) if isinstance(public_payload, dict) else {},
        }

    payload, headers = await github_get("/user")
    return {
        "configured": True,
        "authenticated": True,
        "status": "ok",
        "user": safe_user_payload(payload if isinstance(payload, dict) else {}),
        "scopes": parse_scopes(headers),
        "rate_limit": parse_rate_limit(headers),
    }


async def list_repositories(limit: int = 20) -> dict[str, Any]:
    if not is_configured():
        return {
            "configured": False,
            "repositories": [],
            "message": "저장소 조회에는 GITHUB_TOKEN 또는 GITHUB_PAT 환경변수가 필요합니다.",
        }
    limit = max(1, min(limit, 100))
    payload, headers = await github_get(
        "/user/repos",
        params={"per_page": limit, "sort": "updated", "direction": "desc", "affiliation": "owner,collaborator,organization_member"},
    )
    repositories = []
    if isinstance(payload, list):
        for repo in payload:
            repositories.append({
                "full_name": repo.get("full_name"),
                "private": repo.get("private"),
                "default_branch": repo.get("default_branch"),
                "html_url": repo.get("html_url"),
                "updated_at": repo.get("updated_at"),
                "permissions": repo.get("permissions", {}),
            })
    return {
        "configured": True,
        "repositories": repositories,
        "rate_limit": parse_rate_limit(headers),
    }
