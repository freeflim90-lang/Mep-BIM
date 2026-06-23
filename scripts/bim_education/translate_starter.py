#!/usr/bin/env python3
"""Starter Plan 영어 콘텐츠 → 한국어(ko) 번역 생성기.

en/ 트리를 원문으로 삼아 ko/ 트리를 채운다. 구조·번호·이모지·줄바꿈과
{name}, {discipline_name} 같은 플레이스홀더, "LUA BIM LABS" 브랜드명은
그대로 보존하고 본문만 자연스러운 실무 한국어로 번역한다.

대상:
  messages/en/day_001-060.txt            → messages/ko/day_NNN.txt
  messages/en/<discipline>/day_061-090   → messages/ko/<discipline>/day_NNN.txt
  friday_quiz/en/week_01-13.txt          → friday_quiz/ko/week_NN.txt
  milestone_messages/en/day_030/060/090  → milestone_messages/ko/day_NNN.txt

백엔드 우선순위 (generate.py와 동일 철학):
  1. ANTHROPIC_API_KEY → Claude Haiku
  2. 한도 소진 시 → DEEPSEEK_API_KEY (DeepSeek chat)
  3. 그래도 안 되면 → Ollama qwen2.5:7b

실행:
  python scripts/bim_education/translate_starter.py            # 미생성 항목만
  python scripts/bim_education/translate_starter.py --force    # 전체 재생성
  python scripts/bim_education/translate_starter.py --limit 5  # 앞 5개만 (검수용)
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
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import STARTER_PLAN_DIR  # noqa: E402

SRC_LANG = "en"
DST_LANG = "ko"
DISCIPLINES = ["hvac", "piping", "plumbing", "fire", "electrical"]

MESSAGES_DIR = STARTER_PLAN_DIR / "messages"
FRIDAY_DIR = STARTER_PLAN_DIR / "friday_quiz"
MILESTONE_DIR = STARTER_PLAN_DIR / "milestone_messages"

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

_claude_exhausted = False
_deepseek_exhausted = False


def _load_env() -> None:
    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env()
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")


# ---------------------------------------------------------------------------
# 번역 프롬프트
# ---------------------------------------------------------------------------

def build_prompt(english_text: str) -> str:
    return f"""You are a professional Korean technical translator specializing in MEP BIM (Building Information Modeling) education for construction engineers.

Translate the English lesson below into natural, professional Korean suitable for a paid daily education product aimed at beginner and early-career BIM engineers.

STRICT RULES — follow exactly:
- Translate the body text into fluent, friendly-but-professional Korean (존댓말, 실무체).
- Keep the EXACT line structure, numbering (1. 2. 3. ...), bullet markers (-), emojis (✓, →, 🏅, 🎓, 📚 등), and blank lines as in the source.
- Keep these UNCHANGED, never translate: the brand name "LUA BIM LABS", any placeholder in curly braces such as {{name}} and {{discipline_name}}, prices like "USD 119/month".
- Keep widely-used industry acronyms in English where natural (BIM, MEP, HVAC, AHU, VAV, LOD, QA, Revit, Navisworks, BEP) but you may add a brief Korean gloss only on first use if it reads naturally.
- The "Scope note:" disclaimer at the bottom must be translated faithfully into Korean.
- Translate the "Day N - Title" line: keep "Day N -" and translate only the title text.
- Output ONLY the translated lesson text. No preamble, no notes, no English commentary, no code fences.

ENGLISH SOURCE:
---
{english_text}
---"""


# ---------------------------------------------------------------------------
# 백엔드
# ---------------------------------------------------------------------------

def _with_claude(prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def _with_deepseek(prompt: str) -> str:
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2048,
    }).encode("utf-8")
    req = urllib.request.Request(
        DEEPSEEK_URL, data=payload, method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result["choices"][0]["message"]["content"].strip()


def _with_ollama(prompt: str) -> str:
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 1500},
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result.get("response", "").strip()


def _is_exhaustion(err: str) -> bool:
    # 한도 소진뿐 아니라 인증 오류(무효 키)도 다음 백엔드로 강등시킨다.
    # 키가 잘못돼 매 항목이 401로 죽고 폴백을 못 타는 사고를 방지.
    return any(k in err.lower() for k in
              ("credit", "balance", "quota", "overloaded", "limit", "rate",
               "429", "402", "401", "authentication", "invalid x-api-key",
               "permission"))


def translate(prompt: str) -> tuple[str, str]:
    """(번역문, backend) 반환. 한도 소진 시 다음 백엔드로 자동 강등."""
    global _claude_exhausted, _deepseek_exhausted

    if ANTHROPIC_API_KEY and not _claude_exhausted:
        try:
            return _with_claude(prompt), "claude"
        except Exception as e:
            if _is_exhaustion(str(e)):
                print("\n  ⚠️  Claude 한도/오류 → DeepSeek 전환")
                _claude_exhausted = True
            else:
                raise

    if DEEPSEEK_API_KEY and not _deepseek_exhausted:
        try:
            return _with_deepseek(prompt), "deepseek"
        except Exception as e:
            if _is_exhaustion(str(e)):
                print("\n  ⚠️  DeepSeek 한도/오류 → Ollama 전환")
                _deepseek_exhausted = True
            else:
                raise

    return _with_ollama(prompt), "ollama"


# ---------------------------------------------------------------------------
# 검증
# ---------------------------------------------------------------------------

def validate(src: str, out: str, rel: str) -> list[str]:
    """번역 결과의 구조 보존 여부를 가볍게 점검. 경고 목록 반환."""
    warnings = []
    for token in ("{name}", "{discipline_name}"):
        if token in src and token not in out:
            warnings.append(f"플레이스홀더 누락: {token}")
    if "LUA BIM LABS" in src and "LUA BIM LABS" not in out:
        warnings.append("브랜드명 'LUA BIM LABS' 누락")
    if not out.strip():
        warnings.append("빈 출력")
    # 코드펜스/영어 머리말 혼입 감지
    if out.lstrip().startswith("```") or out.lstrip().lower().startswith("here is"):
        warnings.append("불필요한 머리말/코드펜스 혼입 의심")
    return warnings


# ---------------------------------------------------------------------------
# 작업 목록 구성
# ---------------------------------------------------------------------------

def build_jobs() -> list[tuple[Path, Path, str]]:
    """(src, dst, rel_label) 목록."""
    jobs: list[tuple[Path, Path, str]] = []

    # Foundation 1-60
    for day in range(1, 61):
        fn = f"day_{day:03d}.txt"
        src = MESSAGES_DIR / SRC_LANG / fn
        if src.exists():
            jobs.append((src, MESSAGES_DIR / DST_LANG / fn, f"messages/day_{day:03d}"))

    # Discipline deep-dive 61-90
    for disc in DISCIPLINES:
        for day in range(61, 91):
            fn = f"day_{day:03d}.txt"
            src = MESSAGES_DIR / SRC_LANG / disc / fn
            if src.exists():
                jobs.append((src, MESSAGES_DIR / DST_LANG / disc / fn,
                             f"messages/{disc}/day_{day:03d}"))

    # Friday quiz
    for week in range(1, 14):
        fn = f"week_{week:02d}.txt"
        src = FRIDAY_DIR / SRC_LANG / fn
        if src.exists():
            jobs.append((src, FRIDAY_DIR / DST_LANG / fn, f"friday/week_{week:02d}"))

    # Milestones
    for day in (30, 60, 90):
        fn = f"day_{day:03d}.txt"
        src = MILESTONE_DIR / SRC_LANG / fn
        if src.exists():
            jobs.append((src, MILESTONE_DIR / DST_LANG / fn, f"milestone/day_{day:03d}"))

    return jobs


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Starter Plan en→ko 번역 생성기")
    parser.add_argument("--force", action="store_true", help="기존 ko 파일도 재생성")
    parser.add_argument("--limit", type=int, help="앞 N개만 생성 (검수용)")
    args = parser.parse_args()

    if ANTHROPIC_API_KEY:
        print("✅ Claude Haiku 우선 — 한도 소진 시 DeepSeek → Ollama 자동 전환")
    elif DEEPSEEK_API_KEY:
        print("✅ DeepSeek 우선 — 한도 소진 시 Ollama 전환")
    else:
        print("⚠️  API 키 없음 — Ollama qwen2.5:7b 사용")

    jobs = build_jobs()
    pending = [j for j in jobs if args.force or not j[1].exists()]
    if args.limit:
        pending = pending[:args.limit]

    print(f"전체 {len(jobs)}개 중 생성 대상 {len(pending)}개\n")

    done = 0
    all_warnings: list[str] = []
    for i, (src, dst, rel) in enumerate(pending, 1):
        english = src.read_text(encoding="utf-8").strip()
        print(f"[{i}/{len(pending)}] {rel} ...", end=" ", flush=True)
        try:
            out, backend = translate(build_prompt(english))
        except Exception as e:
            print(f"✗ ({e})")
            time.sleep(3)
            continue

        warns = validate(english, out, rel)
        if "빈 출력" in warns:
            print(f"✗ 빈 출력 — 건너뜀 ({backend})")
            continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(out + "\n", encoding="utf-8")
        done += 1
        if warns:
            print(f"⚠ ({backend}) {'; '.join(warns)}")
            all_warnings.append(f"{rel}: {'; '.join(warns)}")
        else:
            print(f"✓ ({backend})")
        time.sleep(0.2)

    print(f"\n✅ 완료 — {done}개 생성")
    if all_warnings:
        print(f"\n⚠️  검수 필요 {len(all_warnings)}건:")
        for w in all_warnings:
            print(f"  - {w}")


if __name__ == "__main__":
    main()
