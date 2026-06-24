#!/usr/bin/env python3
"""Generate PDF reference cards from Markdown source files.

Reads products/starter_plan/reference_cards/*.md and writes PDF files
to the same directory. Called once when reference cards are updated.

Usage:
  python3 scripts/generate_reference_card_pdfs.py
  python3 scripts/generate_reference_card_pdfs.py --force   # re-generate existing
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    print("fpdf2 not installed. Run: pip3 install fpdf2 --break-system-packages")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys as _sys  # noqa: E402
if str(PROJECT_ROOT) not in _sys.path:
    _sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import STARTER_PLAN_DIR  # noqa: E402

CARDS_DIR = STARTER_PLAN_DIR / "reference_cards"

# 폰트: 기본은 코어 라틴(Helvetica). 한국어 등 CJK는 유니코드 TTF 필요.
# main()에서 --lang 에 따라 _FONT_FAMILY/_FONT_PATH 를 교체한다.
_FONT_FAMILY = "Helvetica"
_FONT_PATH: str | None = None  # None이면 코어 폰트 사용(등록 불필요)

# 언어별 CJK 폰트 후보 (존재하는 첫 번째 사용). Arial Unicode가 ja/zh/ko
# 글리프를 모두 포함하므로 공통 폴백으로 둔다. (아랍어는 RTL+shaping이
# 필요해 이 생성기로는 미지원 — arabic_reshaper/bidi 별도 작업 필요)
_ARIAL_UNICODE = "/Library/Fonts/Arial Unicode.ttf"
_ARIAL_UNICODE_SYS = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
_CJK_FONT_CANDIDATES = {
    "ko": ["/System/Library/Fonts/AppleSDGothicNeo.ttc",
           _ARIAL_UNICODE_SYS, _ARIAL_UNICODE],
    "ja": ["/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
           "/System/Library/Fonts/Hiragino Sans GB.ttc",
           _ARIAL_UNICODE_SYS, _ARIAL_UNICODE],
    "zh": ["/System/Library/Fonts/STHeiti Medium.ttc",
           "/System/Library/Fonts/Hiragino Sans GB.ttc",
           _ARIAL_UNICODE_SYS, _ARIAL_UNICODE],
}

# LUA BIM LABS brand colors (approximate in RGB)
COLOR_BRAND_DARK = (15, 23, 42)       # slate-900
COLOR_BRAND_ACCENT = (14, 165, 233)   # sky-500
COLOR_TEXT = (30, 41, 59)             # slate-800
COLOR_MUTED = (100, 116, 139)         # slate-500
COLOR_BG_LIGHT = (241, 245, 249)      # slate-100
COLOR_WHITE = (255, 255, 255)
COLOR_BORDER = (203, 213, 225)        # slate-300
COLOR_TABLE_HEADER = (30, 58, 138)    # blue-900
COLOR_TABLE_ROW_ALT = (239, 246, 255) # blue-50

CARD_FILENAMES = [
    ("card_01_mep_bim_roles_lod.md",      "card_01_roles_lod.pdf"),
    ("card_02_revit_mep_setup.md",        "card_02_revit_setup.pdf"),
    ("card_03_mep_drawing_reading.md",    "card_03_drawing_reading.pdf"),
    ("card_04_model_quality_checklist.md","card_04_model_quality.pdf"),
    ("card_05_clash_types_priority.md",   "card_05_clash_types.pdf"),
    ("card_06_mep_data_schedule.md",      "card_06_data_schedule.pdf"),
    ("card_07_site_readiness_guide.md",   "card_07_site_readiness.pdf"),
    ("card_08_bim_learning_path.md",      "card_08_learning_path.pdf"),
]


class CardPDF(FPDF):
    def __init__(self, card_title: str, card_subtitle: str):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.card_title = card_title
        self.card_subtitle = card_subtitle
        # CJK 등 유니코드 TTF가 지정되면 일반/볼드 모두 같은 파일로 등록
        # (전용 볼드 페이스가 없어도 set_font(..,"B")가 예외 없이 동작하도록)
        if _FONT_PATH:
            self.add_font(_FONT_FAMILY, "", _FONT_PATH)
            self.add_font(_FONT_FAMILY, "B", _FONT_PATH)
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self._draw_header()

    def _draw_header(self):
        # Brand bar
        self.set_fill_color(*COLOR_BRAND_DARK)
        self.rect(0, 0, 210, 22, "F")

        self.set_font(_FONT_FAMILY, "B", 10)
        self.set_text_color(*COLOR_BRAND_ACCENT)
        self.set_xy(10, 4)
        self.cell(0, 6, "LUA BIM LABS", ln=False)

        self.set_font(_FONT_FAMILY, "", 8)
        self.set_text_color(*COLOR_WHITE)
        self.set_xy(10, 11)
        self.cell(0, 5, "MEP BIM Starter Plan  |  Quick Reference Card", ln=False)

        # Card title block
        self.set_fill_color(*COLOR_BG_LIGHT)
        self.rect(0, 22, 210, 18, "F")

        self.set_font(_FONT_FAMILY, "B", 14)
        self.set_text_color(*COLOR_TEXT)
        self.set_xy(10, 25)
        self.cell(0, 7, _sanitize(self.card_title), ln=True)

        self.set_font(_FONT_FAMILY, "", 8)
        self.set_text_color(*COLOR_MUTED)
        self.set_xy(10, 33)
        self.cell(0, 5, _sanitize(self.card_subtitle), ln=True)

        self.set_y(44)

    def footer(self):
        self.set_y(-12)
        self.set_draw_color(*COLOR_BORDER)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_font(_FONT_FAMILY, "", 7)
        self.set_text_color(*COLOR_MUTED)
        self.cell(0, 6,
                  "LUA BIM LABS  |  Educational reference only - not project specification or code compliance guidance.",
                  align="C")


def _parse_table(lines: list[str]) -> list[list[str]]:
    rows = []
    for line in lines:
        if re.match(r"^\|[-| :]+\|$", line.strip()):
            continue
        if line.strip().startswith("|"):
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cols)
    return rows


def _render_table(pdf: CardPDF, rows: list[list[str]]) -> None:
    if not rows:
        return
    header = rows[0]
    body = rows[1:]
    n_cols = len(header)
    page_w = 190
    col_w = page_w / n_cols

    # Header row
    pdf.set_fill_color(*COLOR_TABLE_HEADER)
    pdf.set_text_color(*COLOR_WHITE)
    pdf.set_font(_FONT_FAMILY, "B", 8)
    for col in header:
        pdf.cell(col_w, 6, _sanitize(col), border=0, align="L", fill=True)
    pdf.ln()

    # Body rows
    pdf.set_font(_FONT_FAMILY, "", 7.5)
    for i, row in enumerate(body):
        fill = i % 2 == 1
        if fill:
            pdf.set_fill_color(*COLOR_TABLE_ROW_ALT)
        pdf.set_text_color(*COLOR_TEXT)
        for j, cell in enumerate(row):
            pdf.multi_cell(col_w, 5, _sanitize(cell), border=0,
                           align="L", fill=fill, new_x="RIGHT" if j < n_cols - 1 else "LMARGIN",
                           new_y="TOP" if j < n_cols - 1 else "NEXT")
    pdf.ln(2)


def _render_checklist_item(pdf: CardPDF, text: str) -> None:
    pdf.set_text_color(*COLOR_BRAND_ACCENT)
    pdf.set_font(_FONT_FAMILY, "B", 9)
    pdf.set_x(12)
    pdf.cell(6, 5, "[v]", ln=False)
    pdf.set_font(_FONT_FAMILY, "", 8.5)
    pdf.set_text_color(*COLOR_TEXT)
    pdf.multi_cell(174, 5, _sanitize(text))


_UNICODE_REPLACEMENTS = [
    ("—", "-"),    # em dash
    ("–", "-"),    # en dash
    ("'", "'"),    # right single quotation mark
    ("'", "'"),    # left single quotation mark
    (""", '"'),    # left double quotation mark
    (""", '"'),    # right double quotation mark
    ("✓", "[v]"),  # check mark
    ("•", "-"),    # bullet
    ("→", "->"),   # right arrow
    ("↓", "v"),    # down arrow
    ("×", "x"),    # multiplication sign
    ("✗", "x"),    # ballot x
    ("✅", "[OK]"), # white heavy check mark
    ("⚠", "[!]"),  # warning sign
    ("️", ""),     # variation selector
]


def _sanitize(text: str) -> str:
    for src, dst in _UNICODE_REPLACEMENTS:
        text = text.replace(src, dst)
    return text


def render_markdown(pdf: CardPDF, md_text: str) -> None:
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip frontmatter / horizontal rules
        if stripped in ("---", "===") or stripped.startswith("---"):
            i += 1
            continue

        # Skip title (already in header) and subtitle lines
        if stripped.startswith("# ") and i < 5:
            i += 1
            continue
        if stripped.startswith("**LUA BIM LABS Starter") or stripped.startswith("*Track completion"):
            i += 1
            continue

        # H2 section heading
        if stripped.startswith("## "):
            heading = stripped[3:].strip()
            pdf.ln(3)
            pdf.set_fill_color(*COLOR_BRAND_DARK)
            pdf.set_text_color(*COLOR_WHITE)
            pdf.set_font(_FONT_FAMILY, "B", 9)
            pdf.set_x(10)
            pdf.cell(190, 6, "  " + _sanitize(heading), fill=True, ln=True)
            pdf.ln(1)
            i += 1
            continue

        # H3 sub-heading
        if stripped.startswith("### ") or stripped.startswith("**") and stripped.endswith("**"):
            heading = re.sub(r"\*+", "", stripped.lstrip("#")).strip()
            pdf.set_font(_FONT_FAMILY, "B", 9)
            pdf.set_text_color(*COLOR_BRAND_DARK)
            pdf.set_x(10)
            pdf.cell(0, 5, _sanitize(heading), ln=True)
            i += 1
            continue

        # Table
        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = _parse_table(table_lines)
            _render_table(pdf, rows)
            continue

        # Checklist item: - [ ] text
        m = re.match(r"^- \[[ x]\] (.+)", stripped)
        if m:
            _render_checklist_item(pdf, m.group(1))
            i += 1
            continue

        # Bullet list item
        if stripped.startswith("- "):
            bullet_text = stripped[2:]
            bullet_text = re.sub(r"\*+([^*]+)\*+", r"\1", bullet_text)
            pdf.set_font(_FONT_FAMILY, "", 8.5)
            pdf.set_text_color(*COLOR_TEXT)
            pdf.set_x(13)
            pdf.cell(4, 5, "-", ln=False)
            pdf.set_x(17)
            pdf.multi_cell(173, 5, _sanitize(bullet_text))
            i += 1
            continue

        # Footer / scope note lines
        if stripped.startswith("*LUA BIM LABS") or stripped.startswith("*Educational"):
            i += 1
            continue

        # Blank line
        if not stripped:
            pdf.ln(2)
            i += 1
            continue

        # Bold inline text as paragraph (e.g., **Section Header**)
        clean = re.sub(r"\*+([^*]+)\*+", r"\1", stripped)
        clean = re.sub(r"`([^`]+)`", r"\1", clean)
        if clean:
            pdf.set_font(_FONT_FAMILY, "", 8.5)
            pdf.set_text_color(*COLOR_TEXT)
            pdf.set_x(10)
            pdf.multi_cell(190, 5, _sanitize(clean))
        i += 1


def generate_pdf(src: Path, dst: Path) -> None:
    md = src.read_text(encoding="utf-8")

    # Extract title from first # heading
    title_match = re.search(r"^# (.+)$", md, re.MULTILINE)
    card_title = title_match.group(1) if title_match else src.stem.replace("_", " ").title()

    # Extract subtitle from **LUA BIM LABS Starter - ...** line
    sub_match = re.search(r"\*\*LUA BIM LABS Starter[^*]+\*\*", md)
    sub_raw = sub_match.group(0) if sub_match else ""
    subtitle = _sanitize(re.sub(r"\*+", "", sub_raw).strip())

    track_match = re.search(r"\*Track completion card[^*]+\*", md)
    if track_match:
        track_note = _sanitize(re.sub(r"\*+", "", track_match.group(0)).strip())
        subtitle = f"{subtitle}  |  {track_note}" if subtitle else track_note

    pdf = CardPDF(card_title, subtitle)
    render_markdown(pdf, md)
    dst.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(dst))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reference card PDFs from Markdown")
    parser.add_argument("--force", action="store_true", help="Overwrite existing PDFs")
    parser.add_argument("--lang", default="en",
                        help="언어 코드. en=기본(라틴), ko=한국어(reference_cards/ko/ 에서 읽고 쓰며 CJK 폰트 사용)")
    args = parser.parse_args()

    global _FONT_FAMILY, _FONT_PATH
    src_dir = dst_dir = CARDS_DIR
    if args.lang != "en":
        src_dir = dst_dir = CARDS_DIR / args.lang
        # CJK 폰트 탐색·등록
        candidates = _CJK_FONT_CANDIDATES.get(args.lang)
        if not candidates:
            print(f"  ✗ {args.lang}: 이 생성기는 ko/ja/zh만 지원합니다 "
                  f"(아랍어 등 RTL은 미지원)")
            sys.exit(1)
        font = next((p for p in candidates if Path(p).exists()), None)
        if not font:
            print(f"  ✗ {args.lang} 용 CJK 폰트를 찾지 못했습니다: {candidates}")
            sys.exit(1)
        _FONT_FAMILY = f"CJK_{args.lang}"
        _FONT_PATH = font
        print(f"  ℹ️  {args.lang} CJK 폰트: {font}")
        if not src_dir.exists():
            print(f"  ✗ 원문 디렉터리 없음: {src_dir} (먼저 translate_reference_cards.py 실행)")
            sys.exit(1)

    done = skipped = failed = 0
    for md_name, pdf_name in CARD_FILENAMES:
        src = src_dir / md_name
        dst = dst_dir / pdf_name
        if not src.exists():
            print(f"  ⚠️  {md_name} not found - skip")
            continue
        if dst.exists() and not args.force:
            print(f"  - {pdf_name} (already exists, skip)")
            skipped += 1
            continue
        try:
            generate_pdf(src, dst)
            print(f"  ✓ {pdf_name}")
            done += 1
        except Exception as e:
            print(f"  ✗ {pdf_name}: {e}")
            failed += 1

    print(f"\n완료: {done}개 생성, {skipped}개 스킵, {failed}개 실패")


if __name__ == "__main__":
    main()
