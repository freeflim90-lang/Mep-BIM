from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

from fastapi import HTTPException


def contract_safe(value: str, fallback: str = "검토 필요") -> str:
    value = str(value or "").strip()
    return value if value else fallback


def contract_slug(value: str) -> str:
    value = re.sub(r"[^\w가-힣.-]+", "-", str(value or "").strip(), flags=re.UNICODE)
    value = re.sub(r"-{2,}", "-", value).strip("-._")
    return value[:60] or "project"


def parse_krw_budget(value: str) -> int | None:
    text = str(value or "").strip().replace(",", "")
    if not text:
        return None
    total = 0
    matched = False
    for amount, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(억|만원|원)?", text):
        number = float(amount)
        if unit == "억":
            total += int(number * 100_000_000)
        elif unit == "만원":
            total += int(number * 10_000)
        elif unit == "원":
            total += int(number)
        elif not matched:
            total += int(number)
        matched = True
    return total if matched and total > 0 else None


def parse_area_m2(value: str) -> float | None:
    match = re.search(r"\d+(?:\.\d+)?", str(value or "").replace(",", ""))
    return float(match.group(0)) if match else None


def parse_lod_level(value: str) -> int | None:
    match = re.search(r"LOD\s*(\d{3})", str(value or ""), flags=re.I)
    return int(match.group(1)) if match else None


def duration_days(start_date: str, end_date: str) -> int | None:
    if not start_date or not end_date:
        return None
    try:
        start = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
        end = dt.datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return None
    return max((end - start).days + 1, 0)


def validate_project_date(value: str, field_label: str) -> str:
    value = str(value or "").strip()
    if not value:
        return ""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise HTTPException(status_code=400, detail=f"{field_label} must use YYYY-MM-DD format")
    try:
        parsed = dt.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"{field_label} is not a valid calendar date") from exc
    if parsed.year < 2020 or parsed.year > 2100:
        raise HTTPException(status_code=400, detail=f"{field_label} year must be between 2020 and 2100")
    return value


def contract_scope_items(disciplines: str, lod: str, formats: str) -> list[tuple[str, str, str]]:
    discipline_text = disciplines or "요청 공종 검토 필요"
    lod_text = lod or "LOD 수준 협의 필요"
    format_text = formats or "납품 형식 협의 필요"
    return [
        ("BIM 수행 범위 검토", discipline_text, lod_text),
        ("모델링 / 코디네이션", "MEP 모델링, 간섭 검토, 품질 검토 범위는 착수 전 SOW에서 확정", lod_text),
        ("납품물", f"납품 형식: {format_text}", "납품 일정 및 버전 협의 필요"),
        ("변경 관리", "문의 범위를 초과하는 추가 요청은 별도 견적 또는 변경 계약으로 처리", "서면 합의 기준"),
    ]


def scope_limit_assessment(
    *,
    budget: str,
    area: str,
    lod: str,
    disciplines: str,
    formats: str,
    start_date: str,
    end_date: str,
) -> dict[str, list[str] | str]:
    budget_krw = parse_krw_budget(budget)
    area_m2 = parse_area_m2(area)
    lod_level = parse_lod_level(lod)
    days = duration_days(start_date, end_date)
    discipline_count = len([d for d in re.split(r"[,/]", disciplines or "") if d.strip()]) or (1 if disciplines else 0)
    feasible: list[str] = []
    excluded: list[str] = []
    risks: list[str] = []
    expansion: list[str] = []
    assumptions: list[str] = []

    if budget_krw is None:
        tier = "예산 미확정"
        feasible.append("자료 검토 후 견적 산정, 업무 범위 분리, 우선순위 제안")
        excluded.append("최종 모델링 착수, 납품 범위 확정, 계약 금액 확정")
        risks.append("희망 예산이 없으므로 LOD, 범위, 납기 간 우선순위 결정이 필요함")
    elif budget_krw < 5_000_000:
        tier = "사전 검토 / 범위 산정"
        feasible += ["도면·모델 자료 검토 및 BIM 수행 범위 산정", "주요 리스크와 견적 기준 정리", "소규모 샘플 또는 검토 보고서 수준의 지원"]
        excluded += ["전체 BIM 모델링 납품", "LOD 300 이상 상세 모델링", "정식 간섭 검토 회차 운영"]
    elif budget_krw < 15_000_000:
        tier = "소규모 / 파일럿 수행"
        feasible += ["단일 공종 또는 우선 구역 중심 모델링", "LOD 200~300 수준의 제한적 모델 검토", "1회 내외 간섭 검토 및 주요 이슈 보고"]
        excluded += ["전 공종 통합 코디네이션", "LOD 350~400 상세 시공 조정", "반복 회의·다회차 보고·현장 상주"]
    elif budget_krw < 30_000_000:
        tier = "단일 공종 중심 수행"
        feasible += ["단일 공종 또는 제한된 복수 공종의 LOD 300 모델링", "우선 구역 중심 간섭 검토 1~2회", "RVT/IFC/NWD 등 합의된 형식의 중간·최종 납품"]
        excluded += ["전체 연면적·전 공종 LOD 350 이상 정밀 코디네이션", "샵드로잉 수준의 상세 시공 도면 전체 납품", "무제한 수정 및 범위 외 설계 변경 대응"]
    elif budget_krw < 70_000_000:
        tier = "중형 BIM 코디네이션"
        feasible += ["복수 공종 또는 주요 구역 중심 LOD 300~350 코디네이션", "정기 간섭 검토와 이슈 리포트 운영", "납품 형식별 모델·보고서 패키지 구성"]
        excluded += ["전 구역 LOD 400 제작·시공 상세 수준", "상주 PM/현장 대응", "대규모 설계 변경의 무상 반영"]
    else:
        tier = "확장형 BIM 수행 검토 가능"
        feasible += ["전 공종 또는 주요 공종의 LOD 350~400 범위 검토 가능", "다회차 간섭 검토, 보고, 품질 관리 체계 운영 가능", "샵드로잉·현장 대응은 별도 SOW로 분리 견적 가능"]
        excluded.append("최종 범위 확정 전 무제한 수정, 인허가 책임, 설계 책임")

    if lod_level and lod_level >= 400 and (budget_krw or 0) < 70_000_000:
        risks.append("LOD 400 요청은 제작·시공 상세 수준이므로 현재 희망 예산에서는 범위 축소 또는 단계 분리가 필요함")
        excluded.append("전체 구역 LOD 400 상세 모델링 및 제작 수준 납품")
    elif lod_level and lod_level >= 350 and (budget_krw or 0) < 30_000_000:
        risks.append("LOD 350 이상은 간섭 조정과 시공성 검토 부담이 커서 우선 구역/단일 공종으로 제한 필요")

    if days is None:
        assumptions.append("착수일과 납품일이 확정되지 않아 실제 가능 범위는 일정 협의 후 재산정")
    elif days < 14:
        risks.append("수행 기간이 14일 미만이므로 모델링 납품보다 자료 검토·긴급 이슈 분석 중심으로 제한 필요")
        excluded.append("정식 BIM 모델 전체 구축 및 다회차 검토")
    elif days < 30:
        risks.append("수행 기간이 30일 미만이므로 우선 구역, 단일 공종, 1회 검토 중심으로 범위 제한 필요")

    if area_m2 and area_m2 >= 30_000 and (budget_krw or 0) < 30_000_000:
        risks.append("연면적 30,000m² 이상 프로젝트에서 3천만원 미만 예산은 전체 범위보다 우선 구역 중심 수행이 적정")
    if area_m2 and area_m2 >= 100_000 and (budget_krw or 0) < 70_000_000:
        risks.append("대형 프로젝트 규모상 전 구역 수행은 예산·기간·공종을 단계별로 분리해야 함")
    if discipline_count >= 3 and (budget_krw or 0) < 30_000_000:
        risks.append("복수 공종 요청 대비 예산이 낮아 공종 우선순위 또는 구역 우선순위 확정 필요")

    if budget_krw is None:
        expansion += ["희망 예산 제시 시 가능한 업무와 제외 업무를 우선 분리 가능", "자료 검토 후 기본 수행안, 확장 수행안, 제외 수행안을 단계별 견적으로 제시 가능"]
    elif budget_krw < 15_000_000:
        expansion += ["예산 1,500만원 이상 확보 시 단일 공종 LOD 300 중심 모델링 검토 가능", "예산 3,000만원 이상 확보 시 복수 공종과 검토 회차 확대 가능"]
    elif budget_krw < 70_000_000:
        expansion += ["예산 7,000만원 이상 확보 시 LOD 350 이상 코디네이션 검토 가능", "샵드로잉, 현장 대응, 반복 설계 변경은 별도 금액과 일정 확정 시 추가 가능"]
    else:
        expansion += ["확장형 BIM 수행 검토가 가능하나 LOD 400·샵드로잉·현장 상주는 별도 SOW로 분리하는 것이 적정"]

    if days and days < 60:
        expansion.append("수행 기간 60일 이상 확보 시 LOD 350 이상 코디네이션과 다회차 이슈 정리에 유리함")
    if not formats:
        assumptions.append("납품 형식은 계약 전 RVT/IFC/NWD/PDF 등으로 확정 필요")
    if not disciplines:
        assumptions.append("요청 공종이 확정되지 않아 수행 범위 산정 전 공종 분류 필요")
    assumptions += [
        "발주자가 최신 도면, 기준층/주요 구역 정보, 기존 모델, 납품 기준을 착수 전 제공하는 것을 전제로 함",
        "희망 예산은 상한 또는 참고 금액으로 보며, 최종 계약 금액은 자료 검토 후 별도 견적으로 확정",
    ]

    return {
        "tier": tier,
        "feasible": feasible,
        "excluded": list(dict.fromkeys(excluded)),
        "risks": list(dict.fromkeys(risks)) or ["현재 입력 기준에서 즉시 치명적인 범위 리스크는 확인되지 않았으나, 자료 검토 후 재산정 필요"],
        "expansion": list(dict.fromkeys(expansion)),
        "assumptions": list(dict.fromkeys(assumptions)),
    }


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def build_contract_draft(payload: dict, *, received_at: str, doc_no: str) -> str:
    company = contract_safe(payload.get("company"), "[고객사명 검토 필요]")
    email = contract_safe(payload.get("email"), "[이메일 검토 필요]")
    phone = contract_safe(payload.get("phone"), "-")
    project = contract_safe(payload.get("project"), "[프로젝트명 검토 필요]")
    building_type = contract_safe(payload.get("building_type"), "-")
    area = contract_safe(payload.get("area"), "")
    budget = contract_safe(payload.get("budget"), "협의 필요")
    disciplines = str(payload.get("disciplines", "")).strip()
    lod = str(payload.get("lod", "")).strip()
    formats = str(payload.get("formats", "")).strip()
    start_date = contract_safe(payload.get("start_date"), "[착수일 협의 필요]")
    end_date = contract_safe(payload.get("end_date"), "[완료 예정일 협의 필요]")
    message = contract_safe(payload.get("message"), "(추가 요청사항 없음)")
    assessment = scope_limit_assessment(
        budget=budget,
        area=area,
        lod=lod,
        disciplines=disciplines,
        formats=formats,
        start_date=start_date if start_date.startswith("20") else "",
        end_date=end_date if end_date.startswith("20") else "",
    )
    scope_rows = "\n".join(
        f"| {idx} | {item} | {desc} | {standard} |"
        for idx, (item, desc, standard) in enumerate(contract_scope_items(disciplines, lod, formats), 1)
    )
    deliverables = "\n".join([
        f"| 1 | BIM 모델 / 코디네이션 산출물 | {formats or 'RVT / IFC / NWD / PDF 등 협의'} | 중간 및 최종 납품 |",
        "| 2 | 검토 리포트 | PDF / XLSX 등 협의 | 검토 회차별 |",
        "| 3 | 최종 납품 패키지 | 계약 범위 확정 후 기재 | 최종 인수 시 |",
    ])
    return f"""# LUA BIM LABS
# BIM 서비스 계약서 초안

> 본 문서는 웹 문의서 입력값을 기반으로 자동 생성된 계약 검토용 초안입니다. 실제 계약 전 당사자 정보, 사업자등록번호, 주소, 최종 금액, 지급 조건, 법무 조항을 반드시 확인해야 합니다.

문서번호: {doc_no}
초안 생성일: {received_at}
계약일: [YYYY-MM-DD]

## 당사자

| 구분 | 내용 |
|---|---|
| 발주자 | {company} |
| 담당자 | {company} / {email} / {phone} |
| 수급자 | LUA BIM LABS |
| 수급자 담당 | LUA BIM LABS / freeflim90@gmail.com |

## 제1조 목적

본 계약은 **{project}**에 관한 BIM 서비스 수행 범위, 대가, 납품 조건 및 양 당사자의 권리·의무를 정하는 것을 목적으로 한다.

## 제2조 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 프로젝트명 | {project} |
| 건물 용도 | {building_type} |
| 연면적 | {(area + ' m²') if area else '-'} |
| 요청 공종 | {disciplines or '검토 필요'} |
| LOD 수준 | {lod or '협의 필요'} |
| 납품 형식 | {formats or '협의 필요'} |
| 문의자 희망 예산 | {budget} |

## 제3조 예산·기간·LOD 기준 수행 가능 범위

| 항목 | 자동 판단 |
|---|---|
| 수행 등급 | {assessment['tier']} |
| 예산 기준 | {budget} |
| 기간 기준 | {start_date} ~ {end_date} |
| LOD 기준 | {lod or '협의 필요'} |

### 3.1 현재 조건에서 가능한 업무
{bullet_list(assessment['feasible'])}

### 3.2 현재 조건에서 제외하거나 별도 견적이 필요한 업무
{bullet_list(assessment['excluded'])}

### 3.3 주요 리스크 및 범위 조정 조건
{bullet_list(assessment['risks'])}

### 3.4 금액·기간 증가 시 확장 가능한 업무
{bullet_list(assessment['expansion'])}

### 3.5 전제 조건
{bullet_list(assessment['assumptions'])}

## 제4조 업무 범위

| No. | 업무 항목 | 내용 | 기준 |
|---:|---|---|---|
{scope_rows}

제외 범위: 설계 책임 및 인허가 책임, 계약 범위 외 신규 요구사항, 현장 상주 지원, 발주자가 제공하지 않은 자료로 인한 재작업은 별도 협의한다.

## 제5조 계약 금액 및 지급

1. 계약 금액: **최종 견적 협의 필요**
2. 문의자 희망 예산: **{budget}**
3. 최종 금액은 도면/모델 자료, 범위, LOD, 납품 형식, 일정 검토 후 확정한다.

| 단계 | 조건 | 비율 | 금액 |
|---|---|---:|---:|
| 착수금 | 계약 체결 후 [N]일 이내 | [협의]% | [협의] |
| 중도금 | 중간 산출물 제출 또는 협의 조건 충족 시 | [협의]% | [협의] |
| 잔금 | 최종 납품·인수 확인 후 [N]일 이내 | [협의]% | [협의] |

## 제6조 계약 기간

- 착수 희망일: {start_date}
- 납품 희망일: {end_date}
- 실제 계약 기간: 자료 수령일, 범위 확정일, 검토 회차에 따라 조정 가능

## 제7조 산출물 및 납품

| No. | 산출물 | 형식 | 납품 시점 |
|---:|---|---|---|
{deliverables}

## 제8조 문의서 원문 메모

```text
{message}
```

## 제9조 범위 변경

범위 변경은 서면 합의 후 변경 계약서 또는 변경 견적서로 처리하며, 미합의 추가 업무는 수행 의무에서 제외된다.

## 제10조 비밀 유지 및 지적재산권

양 당사자는 계약 수행 중 취득한 정보를 계약 목적 외 사용하지 않는다. LUA BIM LABS가 기개발한 라이브러리, 공통 모듈, 자동화 도구의 권리는 LUA BIM LABS에 유지된다.

## 서명

| | 발주자 | 수급자 |
|---|---|---|
| 회사명 | {company} | LUA BIM LABS |
| 대표자 | | |
| 서명/날인 | | |
| 일자 | [YYYY-MM-DD] | [YYYY-MM-DD] |
"""


def write_contract_draft(payload: dict, *, received_at: str, project_root: Path) -> Path:
    date_part = received_at.split()[0].replace("-", "")
    stamp = re.sub(r"[-: ]", "", received_at)
    company_slug = contract_slug(payload.get("company") or payload.get("email") or "client")
    project_slug = contract_slug(payload.get("project") or "project")
    doc_no = f"LBL-CT-{date_part}-{stamp[-4:]}"
    out_dir = project_root / "docs" / "generated_contracts" / date_part[:4]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{doc_no}_{company_slug}_{project_slug}.md"
    out_path.write_text(build_contract_draft(payload, received_at=received_at, doc_no=doc_no), encoding="utf-8")
    return out_path
