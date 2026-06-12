---
type: knowledge-note
domain: 엑셀자동화
sub: BIM리포트
date: 2026-05-22
tags: [엑셀자동화, BIM, Navisworks, Revit, openpyxl, 리포트]
---

# 엑셀 자동화 — BIM 리포트 자동화

---

## 1. Navisworks 간섭 리포트 → Excel

### 1-1. XML 파싱 → 표준 간섭 데이터 추출

Navisworks Clash Detective의 XML 내보내기 결과를 파싱한다.

```python
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date

@dataclass
class ClashItem:
    clash_id: str
    name: str
    status: str          # New / Active / Reviewed / Approved / Resolved
    discipline_a: str
    discipline_b: str
    level: str
    zone: str
    distance_mm: float
    priority: str        # 긴급 / 보통 / 낮음
    assigned_to: str = ""
    due_date: Optional[date] = None
    description: str = ""

def parse_clash_xml(xml_path: str) -> List[ClashItem]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    items = []
    for clash in root.iter("clashresult"):
        distance = float(clash.get("distance", 0)) * 1000  # m → mm
        if distance > 50:
            priority = "긴급"
        elif distance > 10:
            priority = "보통"
        else:
            priority = "낮음"

        # 공종 추출: 첫 번째 클래시 오브젝트의 경로에서 파싱
        paths = [c.get("path", "") for c in clash.findall(".//clashobject")]
        disc_a = _extract_discipline(paths[0] if paths else "")
        disc_b = _extract_discipline(paths[1] if len(paths) > 1 else "")

        items.append(ClashItem(
            clash_id=clash.get("guid", ""),
            name=clash.get("name", ""),
            status=_map_status(clash.get("status", "new")),
            discipline_a=disc_a,
            discipline_b=disc_b,
            level=clash.get("level", "미상"),
            zone=clash.get("zone", "미상"),
            distance_mm=round(distance, 1),
            priority=priority,
            description=clash.findtext("description", ""),
        ))
    return items

def _map_status(raw: str) -> str:
    mapping = {
        "new": "신규", "active": "검토중", "reviewed": "검토중",
        "approved": "조치완료", "resolved": "조치완료",
    }
    return mapping.get(raw.lower(), "신규")

def _extract_discipline(path: str) -> str:
    parts = path.split("\\")
    return parts[1] if len(parts) > 1 else "미상"
```

### 1-2. 간섭 리포트 Excel 생성

```python
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation

HEADERS = [
    "번호", "공종A", "공종B", "레벨", "구역",
    "간섭거리(mm)", "우선순위", "상태", "담당자", "조치기한", "비고"
]

STATUS_OPTIONS = "신규,검토중,조치완료,보류,제외"
PRIORITY_OPTIONS = "긴급,보통,낮음"

def build_clash_report(items: List[ClashItem], output_path: str, title: str = "간섭 리포트") -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "전체"

    # 헤더
    ws.append(HEADERS)
    _apply_header_style(ws, row=1)
    ws.freeze_panes = "A2"

    # 데이터
    for i, item in enumerate(items, 1):
        ws.append([
            i,
            item.discipline_a, item.discipline_b,
            item.level, item.zone,
            item.distance_mm,
            item.priority,
            item.status,
            item.assigned_to,
            item.due_date,
            item.description,
        ])

    last_row = ws.max_row
    last_col = get_column_letter(len(HEADERS))

    # 테이블
    table = Table(displayName="간섭리포트", ref=f"A1:{last_col}{last_row}")
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium9", showRowStripes=True
    )
    ws.add_table(table)

    # 상태 드롭다운
    dv_status = DataValidation(
        type="list", formula1=f'"{STATUS_OPTIONS}"',
        allow_blank=False, showErrorMessage=True,
        errorTitle="상태 오류", error="목록에서 선택하세요."
    )
    ws.add_data_validation(dv_status)
    dv_status.add(f"H2:H{last_row}")

    # 우선순위 드롭다운
    dv_priority = DataValidation(
        type="list", formula1=f'"{PRIORITY_OPTIONS}"',
        allow_blank=False, showErrorMessage=True,
        errorTitle="우선순위 오류", error="목록에서 선택하세요."
    )
    ws.add_data_validation(dv_priority)
    dv_priority.add(f"G2:G{last_row}")

    # 조건부 서식 — 긴급 행 강조
    red_fill = PatternFill(fill_type="solid", fgColor="FF9999")
    ws.conditional_formatting.add(
        f"A2:{last_col}{last_row}",
        FormulaRule(formula=['$G2="긴급"'], fill=red_fill)
    )

    # 숫자/날짜 서식
    for row in ws.iter_rows(min_row=2, max_row=last_row, min_col=6, max_col=6):
        for cell in row:
            cell.number_format = "#,##0.0"
    for row in ws.iter_rows(min_row=2, max_row=last_row, min_col=10, max_col=10):
        for cell in row:
            cell.number_format = "YYYY-MM-DD"

    # 열 너비
    _auto_fit_columns(ws)

    # 공종별 요약 시트
    _add_summary_sheet(wb, items)

    # 인쇄 설정
    ws.print_title_rows = "1:1"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = 9
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.oddHeader.center.text = f"LUA BIM LABS — {title}"
    ws.oddFooter.right.text = "페이지 &P / &N"
    ws.oddFooter.left.text = "&D"

    wb.save(output_path)

def _add_summary_sheet(wb: Workbook, items: List[ClashItem]) -> None:
    ws = wb.create_sheet("요약", 0)
    ws.append(["공종조합", "전체", "긴급", "보통", "낮음", "조치완료", "조치율"])
    _apply_header_style(ws, row=1)

    from collections import defaultdict
    grouped = defaultdict(list)
    for item in items:
        key = f"{item.discipline_a} ↔ {item.discipline_b}"
        grouped[key].append(item)

    for key, group in sorted(grouped.items()):
        total = len(group)
        urgent = sum(1 for x in group if x.priority == "긴급")
        normal = sum(1 for x in group if x.priority == "보통")
        low = sum(1 for x in group if x.priority == "낮음")
        done = sum(1 for x in group if x.status == "조치완료")
        rate = done / total if total else 0
        ws.append([key, total, urgent, normal, low, done, rate])

    last = ws.max_row
    ws[f"G{last+1}"] = f"=AVERAGE(G2:G{last})"
    for row in ws.iter_rows(min_row=2, max_row=last+1, min_col=7, max_col=7):
        for cell in row:
            cell.number_format = "0.0%"
    ws.freeze_panes = "A2"
    _auto_fit_columns(ws)
```

---

## 2. Revit Schedule → Excel (물량 산출)

### 2-1. Revit Schedule CSV 내보내기 처리

```python
import csv
from pathlib import Path

def read_revit_schedule(csv_path: str) -> tuple[list[str], list[list]]:
    """
    Revit Schedule CSV 특성:
    - UTF-16 LE BOM or CP1252 인코딩
    - 1~3행: 프로젝트 정보 헤더 (스킵)
    - 탭 구분자
    - 빈 행으로 그룹 구분
    """
    rows = []
    headers = []
    for enc in ("utf-16", "utf-8-sig", "cp1252"):
        try:
            with open(csv_path, newline="", encoding=enc) as f:
                reader = csv.reader(f, delimiter="\t")
                all_rows = list(reader)
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    else:
        raise ValueError(f"인코딩 감지 실패: {csv_path}")

    # 헤더 행 찾기 (첫 번째 비어 있지 않은 행)
    header_idx = next(
        (i for i, row in enumerate(all_rows) if any(cell.strip() for cell in row)),
        0
    )
    headers = [cell.strip() for cell in all_rows[header_idx]]

    for row in all_rows[header_idx + 1:]:
        cleaned = [cell.strip() for cell in row]
        # 완전 빈 행 스킵
        if not any(cleaned):
            continue
        # 합계/소계 행 스킵 (Revit 자동 생성 행)
        if cleaned[0] in ("합계", "Totals", "Grand total", "소계"):
            continue
        rows.append(cleaned)

    return headers, rows
```

### 2-2. 물량 산출 Excel 생성

```python
def build_quantity_report(
    csv_path: str,
    output_path: str,
    sheet_name: str = "물량",
    numeric_cols: list[str] = None,
) -> None:
    headers, rows = read_revit_schedule(csv_path)
    if numeric_cols is None:
        numeric_cols = ["수량", "길이", "면적", "체적", "Quantity", "Length", "Area", "Volume"]

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name[:31]

    ws.append(headers)
    _apply_header_style(ws, row=1)
    ws.freeze_panes = "A2"

    # 숫자 컬럼 인덱스 파악
    num_col_indices = {
        i for i, h in enumerate(headers)
        if any(nc in h for nc in numeric_cols)
    }

    for row_data in rows:
        typed_row = []
        for j, val in enumerate(row_data):
            if j in num_col_indices:
                try:
                    typed_row.append(float(val.replace(",", "")))
                except ValueError:
                    typed_row.append(val)
            else:
                typed_row.append(val)
        ws.append(typed_row)

    last_row = ws.max_row

    # 합계 행
    ws.append([])
    sum_row = ws.max_row
    ws.cell(sum_row, 1, "합계")
    ws.cell(sum_row, 1).font = Font(bold=True)
    for j in num_col_indices:
        col_letter = get_column_letter(j + 1)
        ws.cell(sum_row, j + 1, f"=SUM({col_letter}2:{col_letter}{last_row})")
        ws.cell(sum_row, j + 1).font = Font(bold=True)

    # 숫자 서식
    for row in ws.iter_rows(min_row=2, max_row=sum_row):
        for j in num_col_indices:
            cell = row[j]
            if isinstance(cell.value, (int, float)):
                cell.number_format = "#,##0.00"

    # 테이블 (합계 행 제외)
    last_col = get_column_letter(len(headers))
    table = Table(displayName="물량산출", ref=f"A1:{last_col}{last_row}")
    table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
    ws.add_table(table)

    _auto_fit_columns(ws)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = 9
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.print_title_rows = "1:1"

    wb.save(output_path)
```

---

## 3. MEP 스케줄 Excel Sync (BCC P1/P2)

### 3-1. Phase 1: CSV 내보내기 → 검증 → 임포트 파이프라인

```python
import json
from pathlib import Path

REQUIRED_COLS = ["UniqueId", "Family", "Type", "Level"]
READ_ONLY_PARAMS = {"UniqueId", "Category", "BuiltInParameter"}

def export_mep_schedule(schedule_rows: list[dict], output_csv: str) -> None:
    """Revit API에서 호출: UniqueId 포함 CSV 내보내기"""
    fieldnames = list(schedule_rows[0].keys()) if schedule_rows else []
    with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(schedule_rows)

def validate_mep_import(csv_path: str, original_ids: set[str]) -> dict:
    """임포트 전 CSV 검증"""
    errors = []
    warnings = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        return {"ok": False, "errors": ["빈 파일"], "warnings": []}

    # 필수 컬럼 확인
    missing = [c for c in REQUIRED_COLS if c not in rows[0]]
    if missing:
        errors.append(f"필수 컬럼 누락: {missing}")

    # UniqueId 보존 확인
    csv_ids = {r["UniqueId"] for r in rows if r.get("UniqueId")}
    orphans = csv_ids - original_ids
    missing_ids = original_ids - csv_ids
    if orphans:
        warnings.append(f"원본에 없는 UniqueId {len(orphans)}개 (신규 추가 시도)")
    if missing_ids:
        warnings.append(f"CSV에서 누락된 UniqueId {len(missing_ids)}개 (삭제됨)")

    # 읽기 전용 파라미터 수정 감지는 Revit 측에서 처리
    return {"ok": not errors, "errors": errors, "warnings": warnings, "rows": rows}

def build_mep_sync_excel(rows: list[dict], output_path: str) -> None:
    """편집 가능한 MEP 스케줄 Excel — UniqueId 열 잠금"""
    wb = Workbook()
    ws = wb.active
    ws.title = "MEP_Schedule"

    if not rows:
        wb.save(output_path)
        return

    headers = list(rows[0].keys())
    ws.append(headers)
    _apply_header_style(ws, row=1)
    ws.freeze_panes = "B2"  # UniqueId(A) 고정

    for row in rows:
        ws.append([row.get(h, "") for h in headers])

    last_row = ws.max_row

    # 시트 보호 — UniqueId 열 잠금, 나머지 편집 허용
    from openpyxl.styles.protection import Protection
    ws.protection.sheet = True
    ws.protection.password = "lbl_mep"
    ws.protection.enable()

    # 읽기 전용 파라미터 열 잠금 (기본값으로 이미 잠김)
    # UniqueId (A 열), 읽기 전용 컬럼 식별 후 잠금 유지

    # 편집 허용: UniqueId 제외한 모든 셀
    uid_col = headers.index("UniqueId") + 1 if "UniqueId" in headers else None
    ro_cols = {
        i + 1 for i, h in enumerate(headers)
        if any(ro in h for ro in READ_ONLY_PARAMS)
    }
    ro_cols.add(uid_col)

    for row in ws.iter_rows(min_row=2, max_row=last_row):
        for cell in row:
            if cell.column not in ro_cols:
                cell.protection = Protection(locked=False)

    _auto_fit_columns(ws)
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.print_title_rows = "1:1"

    wb.save(output_path)
```

---

## 4. 전체 파이프라인 통합 예시

```python
from pathlib import Path
from datetime import datetime

BASE = Path("/path/to/project")

def run_clash_pipeline(xml_path: str, project_code: str) -> str:
    today = datetime.today().strftime("%Y-%m-%d")
    output = BASE / f"{today}_간섭리포트_{project_code}_v1.xlsx"

    items = parse_clash_xml(xml_path)
    build_clash_report(items, str(output), title=f"{project_code} 간섭 리포트")
    return str(output)

def run_quantity_pipeline(csv_path: str, discipline: str) -> str:
    today = datetime.today().strftime("%Y-%m-%d")
    output = BASE / f"{today}_물량산출_{discipline}_v1.xlsx"
    build_quantity_report(csv_path, str(output), sheet_name=discipline)
    return str(output)

def run_mep_sync_pipeline(schedule_rows: list[dict], export_path: str) -> dict:
    original_ids = {r["UniqueId"] for r in schedule_rows if r.get("UniqueId")}
    today = datetime.today().strftime("%Y-%m-%d")
    csv_out = BASE / f"{today}_MEP_Schedule_export.csv"
    xlsx_out = BASE / f"{today}_MEP_Schedule_sync.xlsx"

    export_mep_schedule(schedule_rows, str(csv_out))
    build_mep_sync_excel(schedule_rows, str(xlsx_out))

    return {
        "csv": str(csv_out),
        "xlsx": str(xlsx_out),
        "item_count": len(schedule_rows),
    }
```

---

## 5. 공통 헬퍼 함수 (이 파일 전용)

```python
def _apply_header_style(ws, row: int = 1) -> None:
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
    fill = PatternFill(fill_type="solid", fgColor="1F4E79")
    font = Font(bold=True, color="FFFFFF", size=11, name="맑은 고딕")
    align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin = Side(style="thin", color="FFFFFF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for cell in ws[row]:
        cell.fill = fill
        cell.font = font
        cell.alignment = align
        cell.border = border
    ws.row_dimensions[row].height = 30

def _auto_fit_columns(ws, min_w: int = 8, max_w: int = 40) -> None:
    for col in ws.columns:
        letter = col[0].column_letter
        max_len = max((len(str(c.value)) for c in col if c.value), default=0)
        ws.column_dimensions[letter].width = min(max(max_len + 2, min_w), max_w)
```

---

## 6. 파일 명명 규칙

| 리포트 종류 | 파일명 예시 |
|---|---|
| 간섭 리포트 | `2026-05-22_간섭리포트_기계전기_v1.xlsx` |
| 물량 산출 | `2026-05-22_물량산출_구조_v1.xlsx` |
| MEP 동기화 | `2026-05-22_MEP_Schedule_sync.xlsx` |

---

## 연결

- [[지식맵 - 엑셀 자동화]]
- [[엑셀자동화 - openpyxl 심화 패턴]]
- [[엑셀자동화 - 에러처리와 검증]]
- [[Global Knowledge Map]]
