#!/usr/bin/env python3
"""Publish an HTML post to Blogger using OAuth.

First run opens a Google login page and stores an OAuth token locally.
Keep client secret and token files private.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


SCOPES = ["https://www.googleapis.com/auth/blogger"]


def oauth_config_from_env(client_id_env: str, client_secret_env: str) -> dict[str, Any]:
    client_id = os.environ.get(client_id_env)
    client_secret = os.environ.get(client_secret_env)
    if not client_id or not client_secret:
        raise ValueError(
            f"Missing OAuth env vars. Set {client_id_env} and {client_secret_env}, "
            "or provide --client-secrets."
        )
    return {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }


def load_credentials(
    client_secrets: Path,
    token_path: Path,
    client_id_env: str,
    client_secret_env: str,
    oauth_port: int,
) -> Any:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except ValueError:
            creds = None

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        if client_secrets.exists():
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets), SCOPES)
        else:
            flow = InstalledAppFlow.from_client_config(
                oauth_config_from_env(client_id_env, client_secret_env),
                SCOPES,
            )
        creds = flow.run_local_server(
            host="localhost",
            port=oauth_port,
            open_browser=True,
            prompt="consent",
            access_type="offline",
        )
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding="utf-8")

    return creds


def resolve_blog_id(service: Any, blog_id: str | None, blog_url: str | None) -> str:
    if blog_id:
        return blog_id
    if not blog_url:
        raise ValueError("Provide either --blog-id or --blog-url.")
    blog = service.blogs().getByUrl(url=blog_url).execute()
    return blog["id"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a Blogger post.")
    parser.add_argument("--client-secrets", default="config/blogger/client_secret.json")
    parser.add_argument("--client-id-env", default="BLOGGER_CLIENT_ID")
    parser.add_argument("--client-secret-env", default="BLOGGER_CLIENT_SECRET")
    parser.add_argument("--token", default="config/blogger/token.json")
    parser.add_argument("--oauth-port", type=int, default=8080)
    parser.add_argument("--blog-id")
    parser.add_argument("--blog-url")
    parser.add_argument("--title")
    parser.add_argument("--content-file", required=True)
    parser.add_argument("--labels", nargs="*", default=[])
    parser.add_argument("--meta-json")
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    meta: dict[str, Any] = {}
    if args.meta_json:
        meta = json.loads(Path(args.meta_json).read_text(encoding="utf-8"))

    title = args.title or meta.get("title")
    if not title:
        raise ValueError("Missing post title. Use --title or --meta-json.")

    labels = args.labels or meta.get("labels", [])
    blog_url = args.blog_url or meta.get("blogUrl")
    draft = args.draft or bool(meta.get("draft", False))
    content = Path(args.content_file).read_text(encoding="utf-8")

    body = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": labels,
    }

    if args.dry_run:
        print(json.dumps({"blogUrl": blog_url, "draft": draft, **body}, ensure_ascii=False, indent=2))
        return

    from googleapiclient.discovery import build

    creds = load_credentials(
        Path(args.client_secrets),
        Path(args.token),
        args.client_id_env,
        args.client_secret_env,
        args.oauth_port,
    )
    service = build("blogger", "v3", credentials=creds)
    blog_id = resolve_blog_id(service, args.blog_id, blog_url)

    post = service.posts().insert(blogId=blog_id, body=body, isDraft=draft).execute()
    print(f"Published: {post.get('url')}")


if __name__ == "__main__":
    main()
