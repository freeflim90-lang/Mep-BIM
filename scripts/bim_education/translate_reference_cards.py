#!/usr/bin/env python3
"""Starter Plan 레퍼런스 카드(.md) 영어 → 한국어(ko) 번역기.

reference_cards/*.md 8장을 원문으로 삼아 reference_cards/ko/*.md 를 채운다.
마크다운 구조(표, 헤딩, 수평선, 강조, 이탤릭 푸터)와 "LUA BIM LABS" 브랜드명,
널리 쓰이는 약어(BEP·EIR·CDE·LOD·IFC·NWC·NWD·RFI·HVAC·MEP·QA 등)는
그대로 두고 본문 의미만 실무 한국어로 옮긴다.

백엔드 폴백은 translate_starter 와 동일(Claude→DeepSeek→Ollama).

실행:
  python scripts/bim_education/translate_reference_cards.py          # 미생성만
  python scripts/bim_education/translate_reference_cards.py --force  # 전체 재생성
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.core.paths import STARTER_PLAN_DIR  # noqa: E402
# 백엔드 폴백 로직 재사용
from scripts.bim_education.translate_starter import translate  # noqa: E402

CARDS_DIR = STARTER_PLAN_DIR / "reference_cards"
DST_LANG = "ko"

CARD_MD_FILES = [
    "card_01_mep_bim_roles_lod.md",
    "card_02_revit_mep_setup.md",
    "card_03_mep_drawing_reading.md",
    "card_04_model_quality_checklist.md",
    "card_05_clash_types_priority.md",
    "card_06_mep_data_schedule.md",
    "card_07_site_readiness_guide.md",
    "card_08_bim_learning_path.md",
]


def build_prompt(md_text: str) -> str:
    return f"""You are a professional Korean technical translator specializing in MEP BIM (Building Information Modeling) for construction engineers.

Translate the English Markdown reference card below into natural, professional Korean (존댓말/실무체) for a paid BIM education product.

STRICT RULES — follow exactly:
- Preserve the EXACT Markdown structure: '#'/'##'/'###' headings, '|' table rows and the '|---|' separator rows, horizontal rules '---', '*italic*' lines, blank lines, and the order of everything.
- Translate cell contents and body text, but keep table SHAPE identical (same number of columns and rows).
- Keep these UNCHANGED, never translate: the brand "LUA BIM LABS", and these acronyms — BIM, MEP, HVAC, LOD, BEP, EIR, CDE, IFC, NWC, NWD, RFI, QA, RFI, Revit, Navisworks, AHU, VAV, COBie. You may add a short Korean gloss in parentheses on first use only if it reads naturally.
- Keep the heading 'LOD Definitions', acronym codes (LOD 300, NWC...) and any English software/product names intact.
- The first line '# Title' : translate the title text.
- The '**LUA BIM LABS Starter — ...**' and '*Track completion card — Day NN*' and the two italic footer lines must be translated faithfully (keep 'LUA BIM LABS', 'Day NN', and the em dash).
- Output ONLY the translated Markdown. No preamble, no code fences, no commentary.

ENGLISH MARKDOWN:
---
{md_text}
---"""


def main() -> None:
    parser = argparse.ArgumentParser(description="레퍼런스 카드 en→ko 번역")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    dst_dir = CARDS_DIR / DST_LANG
    dst_dir.mkdir(parents=True, exist_ok=True)

    pending = []
    for name in CARD_MD_FILES:
        src = CARDS_DIR / name
        dst = dst_dir / name
        if not src.exists():
            print(f"  ⚠️  원문 없음: {name}")
            continue
        if dst.exists() and not args.force:
            print(f"  - {name} (이미 있음, 건너뜀)")
            continue
        pending.append((src, dst, name))

    print(f"생성 대상 {len(pending)}장\n")
    done = 0
    for i, (src, dst, name) in enumerate(pending, 1):
        english = src.read_text(encoding="utf-8").strip()
        print(f"[{i}/{len(pending)}] {name} ...", end=" ", flush=True)
        try:
            out, backend = translate(build_prompt(english))
        except Exception as e:
            print(f"✗ ({e})")
            continue
        if not out.strip():
            print(f"✗ 빈 출력 ({backend})")
            continue
        # 표 행수·열수 가벼운 검증
        src_pipes = english.count("|")
        out_pipes = out.count("|")
        warn = ""
        if "LUA BIM LABS" not in out:
            warn += " [브랜드누락]"
        if abs(src_pipes - out_pipes) > 4:
            warn += f" [표구조의심 {src_pipes}->{out_pipes}]"
        dst.write_text(out.rstrip() + "\n", encoding="utf-8")
        done += 1
        print(f"✓ ({backend}){warn}")

    print(f"\n✅ 완료 — {done}장 생성 → {dst_dir}")


if __name__ == "__main__":
    main()
