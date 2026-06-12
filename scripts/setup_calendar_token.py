#!/usr/bin/env python3
"""Google Calendar OAuth 토큰 1회 발급 스크립트.

실행 방법:
    cd "LUA BIM LABS"
    export GOOGLE_CALENDAR_CLIENT_ID="..."
    export GOOGLE_CALENDAR_CLIENT_SECRET="..."
    .dev-venv/bin/python scripts/setup_calendar_token.py

브라우저가 열리면 freeflim90@gmail.com 으로 로그인 후 Calendar 권한을 허용합니다.
완료되면 config/calendar/token.json 이 생성됩니다.
"""

from __future__ import annotations

import subprocess
import webbrowser
import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOKEN_PATH = PROJECT_ROOT / "config" / "calendar" / "token.json"
CLIENT_SECRET_PATH = PROJECT_ROOT / "config" / "calendar" / "client_secret.json"

SCOPES = ["https://www.googleapis.com/auth/calendar"]
PORT = 8085


def load_client_config() -> dict:
    client_id = os.environ.get("GOOGLE_CALENDAR_CLIENT_ID", "").strip()
    client_secret = os.environ.get("GOOGLE_CALENDAR_CLIENT_SECRET", "").strip()

    if client_id and client_secret:
        return {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [f"http://localhost:{PORT}"],
            }
        }

    if CLIENT_SECRET_PATH.exists():
        return json.loads(CLIENT_SECRET_PATH.read_text(encoding="utf-8"))

    raise SystemExit(
        "Google Calendar OAuth 설정이 없습니다. "
        "GOOGLE_CALENDAR_CLIENT_ID/GOOGLE_CALENDAR_CLIENT_SECRET 환경변수를 설정하거나 "
        f"{CLIENT_SECRET_PATH} 파일을 로컬에 두세요."
    )


def _configured_client_id(client_config: dict) -> str:
    section = client_config.get("web") or client_config.get("installed") or {}
    client_id = section.get("client_id", "")
    if not client_id:
        return "unknown"
    return f"{client_id[:8]}...{client_id[-12:]}"


def _ensure_redirect_uri(client_config: dict) -> None:
    section = client_config.get("web") or client_config.get("installed")
    if not isinstance(section, dict):
        return
    redirect_uri = f"http://localhost:{PORT}"
    redirect_uris = section.setdefault("redirect_uris", [])
    if redirect_uri not in redirect_uris:
        redirect_uris.append(redirect_uri)


def _open(url: str, **_) -> bool:
    subprocess.Popen(["open", url])
    return True


def main() -> None:
    from google_auth_oauthlib.flow import InstalledAppFlow

    webbrowser.open = _open  # macOS에서 브라우저 강제 오픈
    client_config = load_client_config()
    _ensure_redirect_uri(client_config)

    print("Google Calendar 권한 인증을 시작합니다...")
    print(f"대상 계정: freeflim90@gmail.com")
    print(f"OAuth 클라이언트: {_configured_client_id(client_config)}")
    print(f"리디렉션 URI: http://localhost:{PORT}")
    print(f"토큰 저장 위치: {TOKEN_PATH}")
    print()

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=PORT, open_browser=True, redirect_uri_trailing_slash=False)

    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    print(f"\n✅ Calendar 토큰 저장 완료: {TOKEN_PATH}")
    print("이제 daily_routine_checklist.py 실행 시 캘린더가 자동으로 업데이트됩니다.")


if __name__ == "__main__":
    main()
