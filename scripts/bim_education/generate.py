#!/usr/bin/env python3
"""BIM 일일 교육 메시지 일괄 생성.

우선순위:
  1. ANTHROPIC_API_KEY 설정 시 → Claude Haiku 사용
  2. API 한도 소진 시 → 자동으로 Ollama qwen2.5:7b 전환

실행:
  python scripts/bim_education/generate.py           # 미생성 항목만
  python scripts/bim_education/generate.py --force   # 전체 재생성
  python scripts/bim_education/generate.py --track 1yr --day 1  # 단일 생성
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "bim_education"))
from topics import TOPICS_1YR, TOPICS_2YR
from topics_extended import (
    TOPICS_3YR, TOPICS_4YR, TOPICS_5YR, TOPICS_6YR,
    TOPICS_7YR, TOPICS_8YR, TOPICS_9YR, TOPICS_10YR,
    TOPICS_11YR, TOPICS_12YR, TOPICS_13YR, TOPICS_14YR, TOPICS_15YR,
    TOPICS_16YR, TOPICS_17YR, TOPICS_18YR, TOPICS_19YR, TOPICS_20YR,
)

ALL_TRACKS = {
    "1yr": TOPICS_1YR, "2yr": TOPICS_2YR, "3yr": TOPICS_3YR,
    "4yr": TOPICS_4YR, "5yr": TOPICS_5YR, "6yr": TOPICS_6YR,
    "7yr": TOPICS_7YR, "8yr": TOPICS_8YR, "9yr": TOPICS_9YR,
    "10yr": TOPICS_10YR, "11yr": TOPICS_11YR, "12yr": TOPICS_12YR,
    "13yr": TOPICS_13YR, "14yr": TOPICS_14YR, "15yr": TOPICS_15YR,
    "16yr": TOPICS_16YR, "17yr": TOPICS_17YR, "18yr": TOPICS_18YR,
    "19yr": TOPICS_19YR, "20yr": TOPICS_20YR,
}

MESSAGES_DIR = PROJECT_ROOT / "data" / "bim_education" / "messages"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"

# Claude 한도 소진 감지 플래그
_claude_exhausted = False


def _load_env_key() -> str | None:
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY") or _load_env_key()


def build_prompt(track_label: str, day: int, phase: str, topic: str, next_topic: str) -> str:
    return f"""당신은 BIM(Building Information Modeling) 전문 교육 강사입니다.
다음 주제로 BIM 엔지니어 {track_label}를 위한 일일 교육 메시지를 작성해주세요.

[과정] {track_label} | [단계] {phase} | [Day] {day}
[오늘 주제] {topic}
[내일 주제] {next_topic}

아래 형식을 정확히 지켜서 작성해주세요:

📚 [BIM 일일 교육] Day {day} — {track_label} 과정

🏗 오늘의 주제: {topic}

💡 핵심 개념
(2~3문장. 핵심 원리나 정의를 명확하게 설명)

🔧 실무 예시
(실제 프로젝트/현장에서 이 지식이 어떻게 쓰이는지 구체적인 예시 1~2개)

💼 오늘의 팁
(바로 써먹을 수 있는 실무 팁 1개. 한 문장으로)

📌 내일 예고: {next_topic}

요구사항:
- 전체 메시지는 400~600자(한국어 기준)
- 실무에서 바로 활용 가능한 내용 위주
- 쉽고 친근한 말투 (딱딱하지 않게)
- 한국어로만 작성
- 이모지 형식은 위의 것을 그대로 사용

위 형식 외의 설명, 주석, 영어 혼용 등은 금지합니다. 메시지 본문만 출력하세요."""


def generate_with_claude(prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def generate_with_ollama(prompt: str) -> str:
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 800},
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=payload,
        headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result.get("response", "").strip()


def generate_message(prompt: str) -> tuple[str, str]:
    """메시지 생성. (content, backend) 반환."""
    global _claude_exhausted

    if ANTHROPIC_API_KEY and not _claude_exhausted:
        try:
            return generate_with_claude(prompt), "claude"
        except Exception as e:
            err = str(e).lower()
            if any(k in err for k in ("credit", "balance", "quota", "overloaded", "limit")):
                print(f"\n  ⚠️  Claude 한도 소진 감지 → Ollama로 전환합니다.")
                _claude_exhausted = True
            else:
                raise

    return generate_with_ollama(prompt), "ollama"


def process_track(track: str, topics: list, force: bool, target_day: int | None) -> None:
    yr_num = track.replace("yr", "")
    track_label = f"{yr_num}년차"
    out_dir = MESSAGES_DIR / track
    out_dir.mkdir(parents=True, exist_ok=True)

    total = len(topics)
    skipped = sum(
        1 for d, _, _ in topics
        if (out_dir / f"day_{d:03d}.txt").exists() and not force
    )
    remaining = total - skipped
    print(f"\n▶ [{track_label}] 총 {total}일 | 생성 필요: {remaining}일")

    for i, (day, phase, topic) in enumerate(topics):
        if target_day is not None and day != target_day:
            continue

        out_file = out_dir / f"day_{day:03d}.txt"
        if out_file.exists() and not force:
            continue

        next_topic = topics[i + 1][2] if i + 1 < total else "완주 축하합니다!"
        prompt = build_prompt(track_label, day, phase, topic, next_topic)

        print(f"  Day {day:03d}/{total} [{phase[:8]}] {topic[:25]}...", end=" ", flush=True)

        try:
            message, backend = generate_message(prompt)
            out_file.write_text(message, encoding="utf-8")
            print(f"✓ ({backend})")
        except Exception as e:
            print(f"✗ ({e})")
            time.sleep(3)

        time.sleep(0.2)


def main() -> None:

    parser = argparse.ArgumentParser(description="BIM 교육 메시지 생성기")
    parser.add_argument("--force", action="store_true", help="기존 파일도 재생성")
    parser.add_argument("--track", choices=list(ALL_TRACKS.keys()), help="특정 트랙만 생성 (1yr~20yr)")
    parser.add_argument("--day", type=int, help="특정 Day만 생성")
    args = parser.parse_args()

    if ANTHROPIC_API_KEY:
        print("✅ Claude Haiku 사용 — 한도 소진 시 Ollama 자동 전환")
    else:
        try:
            urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=3)
            print(f"✅ Ollama({OLLAMA_MODEL}) 사용")
        except Exception:
            print("❌ Claude API 키도 없고 Ollama도 연결 불가. 중단합니다.")
            sys.exit(1)

    if args.track:
        tracks = [(args.track, ALL_TRACKS[args.track])]
    else:
        tracks = list(ALL_TRACKS.items())

    for track, topics in tracks:
        process_track(track, topics, args.force, args.day)

    print("\n✅ 전체 생성 완료")


if __name__ == "__main__":
    main()
