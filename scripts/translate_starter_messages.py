#!/usr/bin/env python3
"""Translate Starter Plan messages from English to target languages using Claude API.

Translates:
  - data/starter_plan/messages/en/day_001.txt ~ day_060.txt
  - data/starter_plan/messages/en/{discipline}/day_061.txt ~ day_090.txt
  - data/starter_plan/friday_quiz/en/week_01.txt ~ week_13.txt
  - data/starter_plan/milestone_messages/en/day_030.txt, day_060.txt, day_090.txt

Usage:
  python scripts/translate_starter_messages.py --lang ja
  python scripts/translate_starter_messages.py --lang zh
  python scripts/translate_starter_messages.py --lang ar
  python scripts/translate_starter_messages.py --lang ja zh ar   # all at once
  python scripts/translate_starter_messages.py --lang ja --force  # re-translate existing
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STARTER_DIR = PROJECT_ROOT / "data" / "starter_plan"
MESSAGES_EN = STARTER_DIR / "messages" / "en"
FRIDAY_EN = STARTER_DIR / "friday_quiz" / "en"
MILESTONE_EN = STARTER_DIR / "milestone_messages" / "en"

DISCIPLINES = ["hvac", "piping", "plumbing", "fire", "electrical"]

LANGUAGE_NAMES = {
    "ja": "Japanese (日本語)",
    "zh": "Simplified Chinese (简体中文)",
    "ar": "Arabic (العربية)",
}

LANGUAGE_INSTRUCTIONS = {
    "ja": (
        "日本語のみで作成してください。BIM、MEP、HVAC、Revit などの"
        "専門用語（英字略語）はそのまま英語で使用してください。"
        "自然で読みやすい日本語にしてください。"
    ),
    "zh": (
        "仅使用简体中文写作。BIM、MEP、HVAC、Revit 等专业术语（英文缩写）"
        "保留英文原文。请使用自然流畅的简体中文。"
    ),
    "ar": (
        "اكتب باللغة العربية فقط. يمكن الإبقاء على المصطلحات التقنية مثل "
        "BIM وMEP وHVAC وRevit باللغة الإنجليزية كما هي. "
        "استخدم لغة عربية واضحة وطبيعية."
    ),
}


def _load_env_key() -> str | None:
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"

_claude_exhausted = False


def _build_prompt(text: str, lang: str, strict: bool = False) -> str:
    instruction = LANGUAGE_INSTRUCTIONS[lang]
    lang_name = LANGUAGE_NAMES[lang]
    strict_note = (
        "\nCRITICAL: The previous attempt returned the original English unchanged. "
        f"You MUST translate every sentence into {lang_name}. "
        "Returning the original English text is NOT acceptable.\n"
        if strict else ""
    )
    return f"""Translate the following MEP BIM educational message into {lang_name}.
{strict_note}
Translation rules:
- {instruction}
- Keep all formatting, line breaks, emojis, and structural markers (✓, →, etc.) exactly as in the original.
- Keep placeholder tokens like {{{{name}}}} and {{{{discipline_name}}}} unchanged.
- Keep "LUA BIM LABS" unchanged.
- Keep "Personal Tutor", "Starter Plan", "Coming Soon" in English (they are product names).
- Keep day numbers and USD prices as-is.
- Do NOT add explanations or commentary — output only the translated message.
- The output MUST be written in {lang_name}, not in English.

Original message:
---
{text}
---

Translated message (in {lang_name} only):"""


def _is_untranslated(original: str, result: str) -> bool:
    """원문과 결과가 동일하면 번역 실패로 판단."""
    orig = original.strip()
    res = result.strip()
    if orig == res:
        return True
    # 영문 비율이 80% 이상이면 번역 실패
    ascii_chars = sum(1 for c in res if c.isascii() and c.isalpha())
    total_alpha = sum(1 for c in res if c.isalpha())
    if total_alpha > 0 and ascii_chars / total_alpha > 0.80 and len(res) > 200:
        return True
    return False


def _translate_with_claude(prompt: str, api_key: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def _translate_with_ollama(prompt: str) -> str:
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.4, "num_predict": 2048},
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result.get("response", "").strip()


def translate_text(text: str, lang: str, api_key: str | None, max_retries: int = 2) -> str:
    global _claude_exhausted

    for attempt in range(max_retries):
        strict = attempt > 0
        prompt = _build_prompt(text, lang, strict=strict)

        try:
            if api_key and not _claude_exhausted:
                try:
                    result = _translate_with_claude(prompt, api_key)
                except Exception as e:
                    err = str(e).lower()
                    if any(k in err for k in ("credit", "balance", "quota", "overloaded", "limit", "too low")):
                        print(f"\n  ⚠️  Claude 크레딧 부족 → Ollama({OLLAMA_MODEL})로 전환")
                        _claude_exhausted = True
                        result = _translate_with_ollama(prompt)
                    else:
                        raise
            else:
                result = _translate_with_ollama(prompt)

            if _is_untranslated(text, result):
                if attempt < max_retries - 1:
                    print(f" [번역 실패 감지, 재시도 {attempt+1}]", end="", flush=True)
                    time.sleep(1)
                    continue
                else:
                    print(f" [재시도 후도 실패 — 원문 영어 저장됨]", end="", flush=True)
            return result

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise

    return text  # 모든 재시도 실패 시 원문 반환


def translate_file(src: Path, dst: Path, lang: str, api_key: str | None, force: bool) -> bool:
    if dst.exists() and not force:
        return False
    text = src.read_text(encoding="utf-8").strip()
    translated = translate_text(text, lang, api_key)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(translated + "\n", encoding="utf-8")
    return True


def translate_all(lang: str, api_key: str | None, force: bool) -> None:
    lang_name = LANGUAGE_NAMES[lang]
    print(f"\n{'='*60}")
    print(f"번역 대상 언어: {lang_name} ({lang})")
    print(f"{'='*60}")

    messages_dst = STARTER_DIR / "messages" / lang
    friday_dst = STARTER_DIR / "friday_quiz" / lang
    milestone_dst = STARTER_DIR / "milestone_messages" / lang

    total = done = skipped = failed = 0

    # 1. Day 001~060
    print(f"\n[1/3] 일반 레슨 (day_001 ~ day_060)")
    for src in sorted(MESSAGES_EN.glob("day_*.txt")):
        dst = messages_dst / src.name
        total += 1
        try:
            translated = translate_file(src, dst, lang, api_key, force)
            if translated:
                done += 1
                print(f"  ✓ {src.name}")
                time.sleep(0.3)
            else:
                skipped += 1
                print(f"  — {src.name} (기존 파일 유지)")
        except Exception as e:
            failed += 1
            print(f"  ✗ {src.name}: {e}")
            time.sleep(2)

    # 2. Discipline 레슨 (day_061~090)
    print(f"\n[2/3] 전문 트랙 레슨 (day_061 ~ day_090 × {len(DISCIPLINES)} disciplines)")
    for discipline in DISCIPLINES:
        src_dir = MESSAGES_EN / discipline
        dst_dir = messages_dst / discipline
        if not src_dir.exists():
            print(f"  ⚠️  {discipline}/ 디렉토리 없음, 건너뜀")
            continue
        for src in sorted(src_dir.glob("day_*.txt")):
            dst = dst_dir / src.name
            total += 1
            try:
                translated = translate_file(src, dst, lang, api_key, force)
                if translated:
                    done += 1
                    print(f"  ✓ {discipline}/{src.name}")
                    time.sleep(0.3)
                else:
                    skipped += 1
                    print(f"  — {discipline}/{src.name} (기존 파일 유지)")
            except Exception as e:
                failed += 1
                print(f"  ✗ {discipline}/{src.name}: {e}")
                time.sleep(2)

    # 3. Friday Quiz
    print(f"\n[3/4] BIM Check Friday 퀴즈 (week_01 ~ week_13)")
    for src in sorted(FRIDAY_EN.glob("week_*.txt")):
        dst = friday_dst / src.name
        total += 1
        try:
            translated = translate_file(src, dst, lang, api_key, force)
            if translated:
                done += 1
                print(f"  ✓ {src.name}")
                time.sleep(0.3)
            else:
                skipped += 1
                print(f"  — {src.name} (기존 파일 유지)")
        except Exception as e:
            failed += 1
            print(f"  ✗ {src.name}: {e}")
            time.sleep(2)

    # 4. Milestone Messages
    print(f"\n[4/4] 마일스톤 메시지 (day_030, day_060, day_090)")
    for src in sorted(MILESTONE_EN.glob("day_*.txt")):
        dst = milestone_dst / src.name
        total += 1
        try:
            translated = translate_file(src, dst, lang, api_key, force)
            if translated:
                done += 1
                print(f"  ✓ {src.name}")
                time.sleep(0.3)
            else:
                skipped += 1
                print(f"  — {src.name} (기존 파일 유지)")
        except Exception as e:
            failed += 1
            print(f"  ✗ {src.name}: {e}")
            time.sleep(2)

    print(f"\n{lang_name} 번역 완료: {done}개 생성, {skipped}개 스킵, {failed}개 실패 (총 {total}개)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Starter Plan 메시지 다국어 번역")
    parser.add_argument("--lang", nargs="+", choices=list(LANGUAGE_NAMES.keys()),
                        required=True, help="번역할 언어 코드 (ja zh ar)")
    parser.add_argument("--force", action="store_true", help="기존 번역 파일도 재번역")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY") or _load_env_key()
    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY 없음 → Ollama 전용 모드로 실행")

    backend = "Claude Haiku + Ollama fallback" if api_key else f"Ollama ({OLLAMA_MODEL})"
    print(f"✅ 번역 엔진: {backend}")
    print(f"대상 언어: {', '.join(LANGUAGE_NAMES[l] for l in args.lang)}")

    for lang in args.lang:
        translate_all(lang, api_key, args.force)

    print("\n\n✅ 모든 번역 완료")


if __name__ == "__main__":
    main()
