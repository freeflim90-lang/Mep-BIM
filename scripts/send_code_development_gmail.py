#!/usr/bin/env python3
"""Send a Gmail report for code development changes.

Required .env values for actual sending:
- GMAIL_ADDRESS or CODE_DEV_GMAIL_FROM
- GMAIL_APP_PASSWORD or CODE_DEV_GMAIL_APP_PASSWORD
- GMAIL_TO or CODE_DEV_GMAIL_TO (default: jycompany90@naver.com)

Without credentials, the script writes a local log and exits successfully so
development workflows are not blocked.

Default policy:
- Mac mini does not store code development bodies.
- This script sends summary by default.
- Use --include-diff only when intentionally sending code diff to the external
  development computer.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.email_notifications import send_gmail


LOG_FILE = PROJECT_ROOT / "logs" / "code_development_gmail.log"
CODE_SUFFIXES = {
    ".py", ".cs", ".xaml", ".js", ".jsx", ".ts", ".tsx", ".html", ".css",
    ".json", ".yml", ".yaml", ".ps1", ".sh", ".bat", ".csproj", ".sln",
}


def run_git(args: list[str]) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=PROJECT_ROOT,
            check=False,
            text=True,
            capture_output=True,
            timeout=20,
        )
    except Exception as exc:  # noqa: BLE001
        return f"git {' '.join(args)} failed: {type(exc).__name__}: {exc}"
    return (result.stdout or result.stderr or "").strip()


def changed_code_files() -> list[str]:
    status = run_git(["status", "--short"])
    files = []
    for line in status.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        suffix = Path(path).suffix.lower()
        if suffix in CODE_SUFFIXES or path.startswith(("backend/", "frontend/", "scripts/", "tests/")):
            files.append(path)
    return files


def build_report(reason: str, include_diff: bool) -> tuple[str, str]:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    files = changed_code_files()
    status = run_git(["status", "--short"])
    branch = run_git(["branch", "--show-current"]) or "(detached)"
    last_commit = run_git(["log", "-1", "--oneline"])
    diff_stat = run_git(["diff", "--stat"])
    staged_stat = run_git(["diff", "--cached", "--stat"])
    diff_text = ""
    if include_diff:
        diff_text = run_git(["diff", "--", *files[:30]])[:12000] if files else ""
    subject = f"[LUA BIM LABS] 코드 개발 보고 - {now}"
    body = f"""LUA BIM LABS 코드 개발 보고

생성 시각: {now}
사유: {reason}
브랜치: {branch}
최근 커밋: {last_commit or '-'}

코드 변경 파일:
{chr(10).join(f'- {path}' for path in files) or '- 코드 변경 파일 없음'}

Git status:
{status or '- 변경 없음'}

Diff stat:
{diff_stat or '- 없음'}

Staged diff stat:
{staged_stat or '- 없음'}

운영 기준:
- 코드 개발 결과는 Gmail로 발송한다.
- Mac mini에는 코드 개발 본문을 저장하지 않는다.
- 민감정보, 토큰, 고객 데이터는 코드/메일 본문에 포함하지 않는다.
- 실제 Revit API write 작업은 검증 게이트를 통과한 뒤 확정한다.
"""
    if diff_text:
        body += f"\nDiff preview (truncated):\n{diff_text}\n"
    return subject, body


def append_log(message: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(message.rstrip() + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Send code development summary via Gmail.")
    parser.add_argument("--reason", default="code-development", help="Reason shown in the email body.")
    parser.add_argument("--include-diff", action="store_true", help="Include truncated unstaged diff preview.")
    args = parser.parse_args()

    subject, body = build_report(args.reason, args.include_diff)
    result = send_gmail(subject, body)
    stamp = dt.datetime.now().isoformat(timespec="seconds")
    if result.get("ok"):
        append_log(f"[{stamp}] sent subject={subject}")
        print("gmail=sent")
        return 0
    append_log(f"[{stamp}] skipped reason={result.get('reason')} subject={subject}")
    print(f"gmail=skipped reason={result.get('reason')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
