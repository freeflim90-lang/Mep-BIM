#!/usr/bin/env python3
"""Validate GitHub integration wiring without printing secrets."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import backend.github_integration as github_integration  # noqa: E402


async def main() -> int:
    status = await github_integration.check_connection()
    print(f"configured={status.get('configured')} authenticated={status.get('authenticated')} status={status.get('status')}")
    if status.get("user"):
        user = status["user"]
        print(f"user={user.get('login')} type={user.get('type')}")
    if status.get("scopes") is not None:
        print(f"scopes_count={len(status.get('scopes', []))}")
    repos = await github_integration.list_repositories(limit=5)
    print(f"repos_configured={repos.get('configured')} repo_count={len(repos.get('repositories', []))}")
    for repo in repos.get("repositories", []):
        print(f"- {repo.get('full_name')} private={repo.get('private')} branch={repo.get('default_branch')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
