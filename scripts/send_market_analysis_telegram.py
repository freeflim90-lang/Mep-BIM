#!/usr/bin/env python3
"""Claude로 완성한 Autodesk Marketplace 갭 분석 결과를 Telegram으로 발송.

사용법:
    # 파일에서 읽어 발송
    python3 scripts/send_market_analysis_telegram.py path/to/analysis.txt

    # 표준 입력에서 읽어 발송
    echo "분석 내용" | python3 scripts/send_market_analysis_telegram.py

    # 인터랙티브 입력 (EOF=Ctrl+D)
    python3 scripts/send_market_analysis_telegram.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR   = PROJECT_ROOT / "docs" / "autodesk_market"

HEADER = "🤖 <b>Autodesk Marketplace 갭 분석 결과</b>"
MAX_TELEGRAM_LEN = 4000  # Telegram 메시지 최대 길이


def send_telegram(text: str) -> bool:
    token   = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        print("오류: TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID 환경변수 없음")
        return False

    url  = f"https://api.telegram.org/bot{token}/sendMessage"
    safe = text.replace("<", "&lt;").replace(">", "&gt;")

    # HTML bold/italic 복원 (단순 패턴만)
    import re
    safe = re.sub(r"&lt;b&gt;(.*?)&lt;/b&gt;", r"<b>\1</b>", safe, flags=re.DOTALL)
    safe = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", safe)
    safe = re.sub(r"### (.*)", r"<b>\1</b>", safe)
    safe = re.sub(r"## (.*)",  r"<b>\1</b>", safe)
    safe = re.sub(r"# (.*)",   r"<b>\1</b>", safe)

    chunks = [safe[i:i+MAX_TELEGRAM_LEN] for i in range(0, len(safe), MAX_TELEGRAM_LEN)]
    success = True
    for idx, chunk in enumerate(chunks):
        if idx == 0:
            chunk = f"{HEADER}\n{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n" + chunk
        body = json.dumps({"chat_id": chat_id, "text": chunk, "parse_mode": "HTML"}).encode()
        req  = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                print(f"  발송 완료 ({idx+1}/{len(chunks)}) status={r.status}")
        except Exception as exc:
            print(f"  발송 실패: {exc}")
            success = False
    return success


def save_analysis_to_report(analysis: str) -> None:
    today = datetime.now().strftime("%Y%m%d")
    # 오늘 날짜 리포트가 있으면 분석 내용 추가
    report_candidates = sorted(REPORT_DIR.glob(f"{today}_market_analysis.md"), reverse=True)
    if report_candidates:
        report_path = report_candidates[0]
        content = report_path.read_text(encoding="utf-8")
        # "## 분석 대기" 섹션 교체
        if "## 분석 대기" in content:
            content = content.replace(
                "## 분석 대기\n\n_Claude로 분석 후 `python3 scripts/send_market_analysis_telegram.py <분석파일>` 실행_",
                f"## Claude 갭 분석\n\n{analysis}"
            )
        else:
            content += f"\n\n## Claude 갭 분석\n\n{analysis}"
        report_path.write_text(content, encoding="utf-8")
        print(f"  리포트 업데이트: {report_path.name}")


def main() -> None:
    # 분석 텍스트 읽기
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        if not path.exists():
            print(f"파일 없음: {path}")
            sys.exit(1)
        analysis = path.read_text(encoding="utf-8").strip()
        print(f"파일 읽기: {path.name} ({len(analysis)}자)")
    elif not sys.stdin.isatty():
        analysis = sys.stdin.read().strip()
        print(f"stdin 읽기 완료 ({len(analysis)}자)")
    else:
        print("분석 내용을 입력하세요 (완료: Ctrl+D):")
        lines = []
        try:
            while True:
                lines.append(input())
        except EOFError:
            pass
        analysis = "\n".join(lines).strip()

    if not analysis:
        print("분석 내용이 없습니다.")
        sys.exit(1)

    # 리포트 파일에 저장
    save_analysis_to_report(analysis)

    # Telegram 발송
    print("Telegram 발송 중...")
    ok = send_telegram(analysis)
    if ok:
        print("완료.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
