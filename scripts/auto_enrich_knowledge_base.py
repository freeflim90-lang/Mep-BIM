#!/usr/bin/env python3
"""
auto_enrich_knowledge_base.py — KB 파일 자동 성장 파이프라인

실행 조건: 오늘 날짜 섹션이 없는 파일만 업데이트 (idempotent)
방식: Tavily 검색 → Claude Haiku 합성 → 파일 append
"""

from __future__ import annotations

import asyncio
import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import httpx as _httpx
    _HTTPX_AVAILABLE = True
except ImportError:
    _HTTPX_AVAILABLE = False

try:
    import anthropic as _anthropic_module
    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False

# ---------------------------------------------------------------------------
# 환경 초기화
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
KB_DIR = PROJECT_ROOT / "data" / "knowledge_base"
LOG_FILE = PROJECT_ROOT / "logs" / "auto_enrich_knowledge_base.log"
ENV_FILE = PROJECT_ROOT / ".env"

def _load_env() -> None:
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

_load_env()

TODAY = datetime.date.today().isoformat()
NOW = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log(msg: str) -> None:
    line = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# ---------------------------------------------------------------------------
# KB 파일 토픽 매핑 (파일명 → 검색 쿼리 + 합성 프롬프트)
# ---------------------------------------------------------------------------
# prompt: Claude Haiku에게 전달할 지시 (검색 결과 없을 때도 독립 생성 가능)
# queries: Tavily 검색어 (우선순위 순)
# tags: KB 섹션 태그
# title: 섹션 제목

KB_TOPICS: dict[str, dict] = {
    # ── 공종별 ─────────────────────────────────────────────────────────────
    "소방기계": {
        "title": "소방기계 최신 기술 동향 및 실무 기준",
        "tags": "fire-mechanical,sprinkler,standards,update",
        "queries": ["소방기계설비 스프링클러 최신 기준 KCS", "fire suppression BIM Korea 2025"],
        "prompt": (
            "한국 소방기계설비(스프링클러, 소화펌프, 소화수조, 소화전) 실무에서 "
            "오늘 날짜 기준으로 BIM 담당자가 알아야 할 최신 기술 기준 또는 현장 팁을 "
            "250~350자 분량으로 작성하라. KCS 번호나 NFTC 번호를 구체적으로 언급하고, "
            "Revit/Navisworks BIM 모델링과 연관된 실무 포인트를 포함하라."
        ),
    },
    "소방전기": {
        "title": "소방전기 최신 기술 동향 및 실무 기준",
        "tags": "fire-electrical,alarm,detection,update",
        "queries": ["자동화재탐지설비 NFTC 203 최신 개정", "fire alarm BIM Korea KS"],
        "prompt": (
            "한국 소방전기설비(자동화재탐지, 비상방송, 유도등, 비상조명) 실무에서 "
            "BIM 담당자가 알아야 할 최신 기술 기준이나 현장 적용 팁을 "
            "250~350자로 작성하라. NFTC 번호와 KS 규격을 구체적으로 포함하고, "
            "Revit BIM 모델링과 연관된 실무 포인트를 포함하라."
        ),
    },
    "공조덕트": {
        "title": "공조덕트 최신 기술 동향 및 실무 기준",
        "tags": "hvac,duct,standards,update",
        "queries": ["공조덕트 KCS 시공기준 최신 2025", "HVAC ductwork BIM coordination Korea"],
        "prompt": (
            "한국 공조덕트 설비 실무에서 BIM 담당자가 알아야 할 "
            "최신 시공 기준이나 BIM 협업 포인트를 250~350자로 작성하라. "
            "덕트 재질, 두께, 지지간격, 방화댐퍼 관련 KCS 기준을 포함하라."
        ),
    },
    "공조배관": {
        "title": "공조배관 최신 기술 동향 및 실무 기준",
        "tags": "hvac,piping,standards,update",
        "queries": ["냉온수배관 KCS 시공기준 보온 최신", "HVAC piping BIM Korea chilled water"],
        "prompt": (
            "한국 공조배관(냉온수, 냉매, 증기) 실무에서 BIM 담당자가 알아야 할 "
            "최신 시공 기준이나 BIM 협업 포인트를 250~350자로 작성하라. "
            "배관 재질, 지지간격, 보온 두께, 압력시험 기준을 포함하라."
        ),
    },
    "전기": {
        "title": "전기설비 최신 기술 동향 및 실무 기준",
        "tags": "electrical,KEC,standards,update",
        "queries": ["KEC 전기설비기술기준 최신 개정 2025", "electrical BIM coordination Korea KEC"],
        "prompt": (
            "한국 전기설비(저압 배선, 분전반, 접지, 케이블 트레이) 실무에서 "
            "BIM 담당자가 알아야 할 최신 KEC 기준이나 현장 팁을 "
            "250~350자로 작성하라. KEC 조항 번호를 구체적으로 언급하고 "
            "Revit BIM 모델링 연관 포인트를 포함하라."
        ),
    },
    "통신": {
        "title": "통신설비 최신 기술 동향 및 실무 기준",
        "tags": "telecom,communication,standards,update",
        "queries": ["구내통신설비 시공기준 KCS 2025", "building telecom BIM Korea Cat6 fiber"],
        "prompt": (
            "한국 구내통신설비(Cat6A, 광케이블, CCTV, MDF/IDF) 실무에서 "
            "BIM 담당자가 알아야 할 최신 기준이나 현장 팁을 "
            "250~350자로 작성하라. 케이블 트레이 이격, 굴곡 반경 기준을 포함하라."
        ),
    },
    "위생": {
        "title": "위생설비 최신 기술 동향 및 실무 기준",
        "tags": "plumbing,sanitary,standards,update",
        "queries": ["급배수위생설비 KCS 시공기준 최신", "plumbing BIM Korea sanitary"],
        "prompt": (
            "한국 위생설비(급수, 배수, 통기, 위생기구) 실무에서 "
            "BIM 담당자가 알아야 할 최신 KCS 기준이나 현장 팁을 "
            "250~350자로 작성하라. 구배, 청소구 간격, 수압시험 기준을 포함하라."
        ),
    },
    "건축": {
        "title": "건축 최신 기술 동향 및 법규 기준",
        "tags": "architecture,building-code,BIM,update",
        "queries": ["건축법 시행령 최신 개정 2025 방화구획", "architecture BIM Korea building code"],
        "prompt": (
            "한국 건축 설계·시공 실무에서 BIM 담당자가 알아야 할 "
            "최신 건축법·건축기준 변경 사항이나 현장 팁을 "
            "250~350자로 작성하라. 방화구획, 피난, 천장고 관련 기준을 포함하라."
        ),
    },
    "구조": {
        "title": "구조 최신 기술 동향 및 설계 기준",
        "tags": "structure,KDS,reinforced-concrete,update",
        "queries": ["KDS 구조설계기준 최신 개정 2025 콘크리트", "structural BIM Korea KDS"],
        "prompt": (
            "한국 구조 설계·시공 실무에서 BIM 담당자가 알아야 할 "
            "최신 KDS 기준 변경이나 현장 팁을 250~350자로 작성하라. "
            "철근 피복두께, 관통 허용 기준, 내진 설계 관련 내용을 포함하라."
        ),
    },
    "토목": {
        "title": "토목 최신 기술 동향 및 시공 기준",
        "tags": "civil,earthwork,KCS,update",
        "queries": ["토목 KCS 표준시방서 최신 개정 2025 토공", "civil BIM Korea earthwork"],
        "prompt": (
            "한국 토목 시공 실무에서 BIM 담당자가 알아야 할 "
            "최신 KCS 기준이나 현장 팁을 250~350자로 작성하라. "
            "토공 다짐도, 도로포장, 지하매설물 BIM 모델링 기준을 포함하라."
        ),
    },
    "설비기초": {
        "title": "건축설비 기초 지식 업데이트",
        "tags": "mep,fundamentals,update",
        "queries": ["건축설비 MEP BIM 기초 개념 최신 2025", "MEP building services fundamentals BIM"],
        "prompt": (
            "건축설비(MEP) 기초 지식 중 BIM 실무자가 놓치기 쉬운 개념이나 "
            "최근 현장에서 중요해진 포인트를 250~350자로 작성하라. "
            "공종 간 협업 체크포인트와 BIM 데이터 기준을 포함하라."
        ),
    },
    "설비도면해석": {
        "title": "설비 도면 해석 기준 업데이트",
        "tags": "mep,drawing,interpretation,update",
        "queries": ["설비 도면 기호 표준 KS 최신 2025", "MEP drawing symbol standard Korea"],
        "prompt": (
            "건축설비 도면 해석 실무에서 BIM 담당자가 알아야 할 "
            "최신 KS 도면 기호 기준이나 현장 팁을 250~350자로 작성하라. "
            "Revit BIM 모델과 2D 도면 연동 시 주의사항을 포함하라."
        ),
    },
    "설비시공조율": {
        "title": "설비 시공 조율 기준 업데이트",
        "tags": "mep,coordination,construction,update",
        "queries": ["MEP BIM 간섭 조율 현장 적용 2025", "MEP clash coordination BIM Korea"],
        "prompt": (
            "MEP 설비 시공 조율 실무에서 BIM 담당자가 알아야 할 "
            "최신 간섭 조율 기준이나 현장 팁을 250~350자로 작성하라. "
            "Navisworks 간섭 허용 기준, 공종 우선순위, 조율 회의 운영 기준을 포함하라."
        ),
    },
    "설비자동제어": {
        "title": "설비 자동제어(BAS/BMS) 기준 업데이트",
        "tags": "bas,bms,control,update",
        "queries": ["BAS BMS 건물자동제어 최신 기준 2025 Korea", "building automation system BIM integration"],
        "prompt": (
            "건물 설비 자동제어(BAS/BMS) 실무에서 BIM 담당자가 알아야 할 "
            "최신 기준이나 현장 팁을 250~350자로 작성하라. "
            "BIM 모델과 BAS 포인트 리스트 연동, IFC 기반 데이터 전달 기준을 포함하라."
        ),
    },
    "설비장비": {
        "title": "설비 장비 선정 및 BIM 데이터 기준 업데이트",
        "tags": "mep,equipment,specification,update",
        "queries": ["건축설비 장비 BIM 패밀리 표준 2025", "MEP equipment BIM family standard Korea"],
        "prompt": (
            "건축설비 장비(공조기, 펌프, 팬, 열원기기) BIM 모델링 실무에서 "
            "알아야 할 최신 기준이나 팁을 250~350자로 작성하라. "
            "장비 패밀리 파라미터 기준, LOD별 데이터 요구사항을 포함하라."
        ),
    },
    # ── 지침서 / 시방서 ───────────────────────────────────────────────────
    "설계_지침서": {
        "title": "설계 BIM 지침서 최신 업데이트",
        "tags": "design,guideline,BIM,update",
        "queries": ["국토교통부 설계 BIM 지침 최신 2025", "design BIM guideline Korea MOLIT"],
        "prompt": (
            "한국 설계 단계 BIM 지침(국토교통부 기준) 관련 최신 변경 사항이나 "
            "실무 적용 팁을 250~350자로 작성하라. "
            "LOD 기준, 납품물 요건, 설계-시공 연계 기준을 포함하라."
        ),
    },
    "시공_지침서": {
        "title": "시공 BIM 지침서 최신 업데이트",
        "tags": "construction,guideline,BIM,update",
        "queries": ["시공 BIM 지침서 국토부 2025 as-built", "construction BIM guideline Korea"],
        "prompt": (
            "한국 시공 단계 BIM 지침 관련 최신 변경 사항이나 현장 적용 팁을 "
            "250~350자로 작성하라. Shop Drawing BIM 연계, 4D 공정, As-Built BIM "
            "납품 기준을 포함하라."
        ),
    },
    "BIM_지침서": {
        "title": "BIM 지침서 최신 동향 및 표준 업데이트",
        "tags": "BIM,guideline,IFC,openBIM,update",
        "queries": ["openBIM IFC IDS buildingSMART Korea 2025", "BIM standard update ISO 19650 Korea"],
        "prompt": (
            "국제 BIM 표준(ISO 19650, IFC4, IDS) 및 한국 BIM 지침 최신 동향을 "
            "250~350자로 작성하라. openBIM, IDS 적용 실무, "
            "Revit→IFC 내보내기 최신 기준을 포함하라."
        ),
    },
    "설계_시방서": {
        "title": "설계 시방서 최신 기준 업데이트",
        "tags": "design,specification,KCS,update",
        "queries": ["KCS 표준시방서 설계 최신 개정 2025", "design specification standard Korea KCS"],
        "prompt": (
            "한국 설계 시방서(KCS 기준) 최신 개정 사항이나 실무 적용 팁을 "
            "250~350자로 작성하라. 특기시방서 작성 기준, BIM 파라미터 연계 방법을 포함하라."
        ),
    },
    "시공_시방서": {
        "title": "시공 시방서 최신 기준 업데이트",
        "tags": "construction,specification,KCS,update",
        "queries": ["KCS 표준시방서 시공 최신 개정 2025 콘크리트", "construction specification KCS Korea update"],
        "prompt": (
            "한국 시공 표준시방서(KCS) 최신 개정 사항이나 현장 적용 팁을 "
            "250~350자로 작성하라. 콘크리트, 철골, 방수 공종 관련 핵심 변경 사항을 포함하라."
        ),
    },
    "BIM_시방서": {
        "title": "BIM 시방서 최신 기준 업데이트",
        "tags": "BIM,specification,EIR,COBie,update",
        "queries": ["BIM 시방서 발주처 EIR 요구사항 2025 Korea", "BIM specification COBie FM Korea"],
        "prompt": (
            "한국 BIM 시방서(EIR 기반) 최신 동향이나 실무 적용 팁을 "
            "250~350자로 작성하라. 발주처별 BIM 요구 수준, COBie, "
            "FM 연동 데이터 기준을 포함하라."
        ),
    },
    # ── BIM 프로젝트 관련 ──────────────────────────────────────────────────
    "BEP_수행계획서": {
        "title": "BEP 수행계획서 최신 작성 기준",
        "tags": "BEP,BIM-execution-plan,update",
        "queries": ["BIM 수행계획서 BEP 작성 기준 국토부 2025", "BIM execution plan BEP template Korea"],
        "prompt": (
            "BIM 수행계획서(BEP) 작성 실무에서 최신 기준이나 팁을 "
            "250~350자로 작성하라. 발주처 EIR 대응, "
            "공종별 LOD 계획, 협업 환경 기술 방법을 포함하라."
        ),
    },
    "BIM_건물유형_공사구분_산정로직": {
        "title": "BIM 건물유형·공사구분 산정 기준 업데이트",
        "tags": "BIM,building-type,cost,update",
        "queries": ["BIM 적용 대상 건물유형 공사구분 국토부 2025", "BIM mandatory building type Korea"],
        "prompt": (
            "한국 BIM 의무 적용 대상 건물 유형 및 공사 구분 기준 최신 동향을 "
            "250~350자로 작성하라. 국토부 고시 기준, 공공 발주 BIM 적용 범위 변화를 포함하라."
        ),
    },
    "BIM_등급별_투입일_기준표": {
        "title": "BIM 등급별 투입일 기준 업데이트",
        "tags": "BIM,manday,grade,update",
        "queries": ["BIM 인력 투입 공수 산정 기준 2025 Korea", "BIM labor hours estimation standard Korea"],
        "prompt": (
            "BIM 인력 투입 공수(M/D) 산정 기준 최신 동향이나 실무 팁을 "
            "250~350자로 작성하라. 공종별·단계별 투입 기준, "
            "국내 BIM 용역 시장 공수 현황을 포함하라."
        ),
    },
    "BIM_인력파견_기준": {
        "title": "BIM 인력 파견 기준 업데이트",
        "tags": "BIM,staffing,outsourcing,update",
        "queries": ["BIM 인력 파견 기준 계약 2025 Korea", "BIM staffing outsourcing Korea"],
        "prompt": (
            "BIM 인력 파견·외주 계약 실무 기준 최신 동향이나 팁을 "
            "250~350자로 작성하라. 파견 인력 역량 기준, 계약 조건, "
            "품질 관리 체계를 포함하라."
        ),
    },
    "BIM_제안서": {
        "title": "BIM 제안서 작성 최신 기준",
        "tags": "BIM,proposal,winning,update",
        "queries": ["BIM 용역 제안서 작성 기준 2025 낙찰", "BIM proposal writing Korea public procurement"],
        "prompt": (
            "BIM 용역 제안서 작성 실무에서 최신 트렌드나 팁을 "
            "250~350자로 작성하라. 기술 평가 배점 기준, "
            "수주 성공 전략, 가격 경쟁력 포인트를 포함하라."
        ),
    },
    "BIM_템플릿기획관": {
        "title": "BIM 템플릿 기획 최신 동향",
        "tags": "BIM,template,planning,update",
        "queries": ["Revit 프로젝트 템플릿 표준 2025 Korea", "Revit template BIM standard Korea"],
        "prompt": (
            "Revit BIM 프로젝트 템플릿 기획·관리 실무에서 최신 기준이나 팁을 "
            "250~350자로 작성하라. 공유 파라미터, 뷰 템플릿, "
            "패밀리 표준화 방향을 포함하라."
        ),
    },
    "BIM_프로젝트_견적산정": {
        "title": "BIM 프로젝트 견적 산정 최신 기준",
        "tags": "BIM,cost-estimation,pricing,update",
        "queries": ["BIM 용역 견적 산정 기준 2025 Korea 단가", "BIM service pricing Korea"],
        "prompt": (
            "BIM 용역 견적 산정 실무에서 최신 시장 단가 동향이나 산정 팁을 "
            "250~350자로 작성하라. 공종별·단계별 단가 기준, "
            "추가 비용 항목, 계약 방식별 차이를 포함하라."
        ),
    },
    # ── 도구 / 기술 ────────────────────────────────────────────────────────
    "Dynamo": {
        "title": "Dynamo 최신 기능 및 BIM 자동화 팁",
        "tags": "dynamo,automation,revit,update",
        "queries": ["Dynamo Revit 최신 버전 2025 자동화 팁", "Dynamo BIM automation Revit 2025"],
        "prompt": (
            "Autodesk Dynamo 최신 버전(2025 기준)에서 BIM 실무자가 활용할 수 있는 "
            "자동화 팁이나 새 기능을 250~350자로 작성하라. "
            "MEP 배관/덕트 자동 배치, 일람표 자동화, 물량산출 스크립트 예시를 포함하라."
        ),
    },
    "Navisworks_Addin": {
        "title": "Navisworks Add-in 최신 동향 및 활용 팁",
        "tags": "navisworks,addin,clash-detection,update",
        "queries": ["Navisworks 2025 최신 기능 간섭 검토", "Navisworks API Add-in development 2025"],
        "prompt": (
            "Autodesk Navisworks 2025 최신 기능이나 Add-in 개발 실무 팁을 "
            "250~350자로 작성하라. 간섭 검토 자동화, "
            "보고서 커스터마이징, API 활용 방법을 포함하라."
        ),
    },
    "Revit_Addin": {
        "title": "Revit Add-in 최신 동향 및 개발 팁",
        "tags": "revit,addin,API,update",
        "queries": ["Revit 2025 API 최신 변경사항 Add-in", "Revit API 2025 new features development"],
        "prompt": (
            "Autodesk Revit 2025 API 최신 변경 사항이나 Add-in 개발 팁을 "
            "250~350자로 작성하라. 새 API 메서드, "
            "성능 최적화, Autodesk Store 심사 통과 팁을 포함하라."
        ),
    },
    "엔지니어링계산서": {
        "title": "엔지니어링 계산서 작성 최신 기준",
        "tags": "engineering,calculation,standards,update",
        "queries": ["건축설비 엔지니어링 계산서 작성 기준 2025 Korea", "MEP engineering calculation standard Korea"],
        "prompt": (
            "건축설비 엔지니어링 계산서(냉난방 부하, 덕트 사이징, 배관 사이징) "
            "작성 실무에서 최신 기준이나 팁을 250~350자로 작성하라. "
            "KDS/KCS 기준 적용 방법, BIM 연동 계산 방법을 포함하라."
        ),
    },
    # ── 조직 페르소나 ──────────────────────────────────────────────────────
    "CEO": {
        "title": "CEO 의사결정 인텔리전스 업데이트",
        "tags": "ceo,strategy,market-intel,update",
        "queries": ["BIM 소프트웨어 시장 동향 2025 Autodesk 수익", "AEC tech startup revenue model 2025"],
        "prompt": (
            "BIM/AEC 기술 스타트업 CEO가 오늘 알아야 할 시장 동향이나 전략적 인사이트를 "
            "200~300자로 작성하라. Autodesk 경쟁 동향, SaaS BIM 수익 모델, "
            "국내 공공 BIM 시장 기회를 포함하라."
        ),
    },
    "CFO": {
        "title": "CFO 재무 인텔리전스 업데이트",
        "tags": "cfo,finance,revenue,update",
        "queries": ["AEC SaaS 구독 재무 모델 LTV CAC 2025", "BIM software subscription financial model"],
        "prompt": (
            "BIM/AEC SaaS 회사 CFO가 오늘 알아야 할 재무 관리 팁이나 시장 인사이트를 "
            "200~300자로 작성하라. 구독 수익 인식 기준, LTV/CAC 관리, "
            "환율 리스크 헷지 방법을 포함하라."
        ),
    },
    "COO": {
        "title": "COO 운영 인텔리전스 업데이트",
        "tags": "coo,operations,delivery,update",
        "queries": ["AEC 스타트업 운영 효율화 2025 KPI", "software delivery operations BIM company"],
        "prompt": (
            "BIM 소프트웨어 회사 COO가 오늘 알아야 할 운영 최적화 팁이나 인사이트를 "
            "200~300자로 작성하라. 릴리스 주기 관리, QA 게이트, "
            "고객 지원 SLA 운영 방법을 포함하라."
        ),
    },
    "CS_기술지원관": {
        "title": "기술지원 CS 운영 기준 업데이트",
        "tags": "cs,technical-support,revit,update",
        "queries": ["Revit 기술 지원 FAQ 2025 설치 오류", "Revit troubleshooting common errors 2025"],
        "prompt": (
            "Revit/BIM Add-in 기술지원 담당자가 오늘 알아야 할 "
            "최신 트러블슈팅 팁이나 FAQ를 200~300자로 작성하라. "
            "Revit 버전 호환성 문제, 설치 오류 대응, 고객 응대 스크립트를 포함하라."
        ),
    },
    "HR_인재분석관": {
        "title": "BIM 인재 채용 및 역량 관리 업데이트",
        "tags": "hr,talent,BIM,update",
        "queries": ["BIM 전문가 채용 역량 기준 2025 Korea", "BIM talent skills demand Korea 2025"],
        "prompt": (
            "BIM 인재 채용·역량 관리 담당자가 오늘 알아야 할 시장 동향이나 팁을 "
            "200~300자로 작성하라. BIM 코디네이터·매니저 역량 기준, "
            "채용 시장 동향, 역량 개발 방향을 포함하라."
        ),
    },
    "조율차장": {
        "title": "프로젝트 조율 및 PM 운영 업데이트",
        "tags": "pm,coordination,delivery,update",
        "queries": ["BIM 프로젝트 PM 관리 최신 방법론 2025", "BIM project management coordination 2025"],
        "prompt": (
            "BIM 프로젝트 PM·조율 담당자가 오늘 알아야 할 관리 팁이나 방법론을 "
            "200~300자로 작성하라. 다중 공종 조율 프로세스, "
            "리스크 관리, 일정 지연 대응 방법을 포함하라."
        ),
    },
    "교육컨설팅": {
        "title": "BIM 교육 커리큘럼 최신 동향",
        "tags": "education,curriculum,BIM,update",
        "queries": ["BIM 교육 커리큘럼 2025 Korea 자격증", "BIM training certification Korea 2025"],
        "prompt": (
            "BIM 교육 컨설팅 담당자가 오늘 알아야 할 교육 시장 동향이나 "
            "커리큘럼 설계 팁을 200~300자로 작성하라. "
            "BIM 자격증 동향, 연차별 교육 수요, 교육 효과 측정 방법을 포함하라."
        ),
    },
    "전략기획": {
        "title": "전략기획 시장 인텔리전스 업데이트",
        "tags": "strategy,market,BIM,update",
        "queries": ["한국 BIM 시장 동향 2025 공공 민간 규모", "BIM market size Korea 2025 growth"],
        "prompt": (
            "BIM 회사 전략기획 담당자가 오늘 알아야 할 시장 인텔리전스를 "
            "200~300자로 작성하라. 국내 BIM 시장 규모, "
            "정부 정책 변화, 신규 사업 기회를 포함하라."
        ),
    },
    "법무조항검토": {
        "title": "BIM 법무·계약 최신 동향 업데이트",
        "tags": "legal,contract,BIM,update",
        "queries": ["BIM 용역 계약 법무 이슈 2025 Korea 지식재산권", "BIM contract legal IP Korea"],
        "prompt": (
            "BIM 용역 계약·법무 담당자가 오늘 알아야 할 최신 이슈나 팁을 "
            "200~300자로 작성하라. BIM 데이터 지식재산권, "
            "소프트웨어 EULA 이슈, 하자 책임 범위를 포함하라."
        ),
    },
    "프로젝트분석": {
        "title": "BIM 프로젝트 분석 최신 방법론 업데이트",
        "tags": "project-analysis,BIM,cost,update",
        "queries": ["BIM 프로젝트 사전분석 공수산정 2025 Korea", "BIM project analysis feasibility Korea"],
        "prompt": (
            "BIM 프로젝트 사전 분석 담당자가 오늘 알아야 할 분석 방법론이나 팁을 "
            "200~300자로 작성하라. 공수 산정 방법, 리스크 분류, "
            "발주처 요구사항 분석 프레임워크를 포함하라."
        ),
    },
    "견적서담당": {
        "title": "BIM 견적 작성 최신 기준 업데이트",
        "tags": "cost,estimation,proposal,update",
        "queries": ["BIM 용역 견적서 작성 기준 단가표 2025 Korea", "BIM service quotation Korea"],
        "prompt": (
            "BIM 용역 견적 작성 담당자가 오늘 알아야 할 최신 단가 기준이나 팁을 "
            "200~300자로 작성하라. 공종별 BIM 단가, "
            "간접비 산정, 경쟁입찰 전략을 포함하라."
        ),
    },
    "견적심사원": {
        "title": "BIM 견적 심사 기준 업데이트",
        "tags": "cost-review,audit,BIM,update",
        "queries": ["BIM 용역 견적 심사 기준 2025 공공 발주", "BIM cost audit public procurement Korea"],
        "prompt": (
            "BIM 용역 견적 심사 담당자가 오늘 알아야 할 심사 기준이나 팁을 "
            "200~300자로 작성하라. 공공 발주 심사 기준, "
            "원가 적정성 검토 방법, 부당 저가 판단 기준을 포함하라."
        ),
    },
    "경영지원": {
        "title": "경영지원 운영 최신 기준 업데이트",
        "tags": "administration,support,operations,update",
        "queries": ["스타트업 경영지원 운영 효율화 2025", "startup admin operations Korea 2025"],
        "prompt": (
            "BIM 스타트업 경영지원 담당자가 오늘 알아야 할 운영 효율화 팁이나 "
            "행정 기준을 200~300자로 작성하라. "
            "회계 처리, 계약 관리, 인사 행정 체계를 포함하라."
        ),
    },
    "고객지원CS": {
        "title": "고객지원 CS 운영 최신 기준 업데이트",
        "tags": "cs,customer-support,SLA,update",
        "queries": ["SaaS 고객지원 CS 운영 기준 2025 Korea", "software customer support SLA best practices"],
        "prompt": (
            "BIM 소프트웨어 고객지원 CS 담당자가 오늘 알아야 할 운영 팁이나 "
            "기준을 200~300자로 작성하라. SLA 관리, "
            "티켓 에스컬레이션 프로세스, 고객 만족도 향상 방법을 포함하라."
        ),
    },
    "고객지원운영": {
        "title": "고객지원 운영 시스템 최신 동향",
        "tags": "cs,operations,helpdesk,update",
        "queries": ["고객지원 헬프데스크 운영 자동화 2025", "helpdesk automation customer support 2025"],
        "prompt": (
            "BIM 소프트웨어 고객지원 운영 담당자가 오늘 알아야 할 "
            "운영 자동화 팁이나 도구 동향을 200~300자로 작성하라. "
            "AI 기반 1차 응대, 지식베이스 연동, 운영 KPI 관리를 포함하라."
        ),
    },
    "글로벌_매출관리원": {
        "title": "글로벌 매출 관리 최신 동향",
        "tags": "global,revenue,sales,update",
        "queries": ["Autodesk App Store 글로벌 매출 관리 2025", "AEC software global sales management"],
        "prompt": (
            "글로벌 BIM 소프트웨어 매출 관리 담당자가 오늘 알아야 할 "
            "시장 동향이나 팁을 200~300자로 작성하라. "
            "Autodesk App Store 매출 최적화, 지역별 가격 전략, 환율 관리를 포함하라."
        ),
    },
    "글로벌_유통기획관": {
        "title": "글로벌 유통 전략 최신 동향",
        "tags": "global,distribution,channel,update",
        "queries": ["AEC software global distribution partner 2025", "BIM software reseller channel strategy"],
        "prompt": (
            "글로벌 BIM 소프트웨어 유통 기획 담당자가 오늘 알아야 할 "
            "채널 전략이나 파트너십 동향을 200~300자로 작성하라. "
            "Autodesk 파트너 프로그램, 해외 리셀러 관리, 현지화 전략을 포함하라."
        ),
    },
    "라이선스_보안관": {
        "title": "소프트웨어 라이선스·보안 최신 동향",
        "tags": "license,security,compliance,update",
        "queries": ["소프트웨어 라이선스 보안 컴플라이언스 2025", "software license security compliance Autodesk"],
        "prompt": (
            "BIM 소프트웨어 라이선스·보안 담당자가 오늘 알아야 할 "
            "컴플라이언스 이슈나 보안 팁을 200~300자로 작성하라. "
            "Autodesk 라이선스 정책 변화, 불법 복제 방지, 데이터 보안 기준을 포함하라."
        ),
    },
    "라이선스결제": {
        "title": "라이선스 결제 시스템 최신 동향",
        "tags": "license,payment,subscription,update",
        "queries": ["SaaS 구독 결제 시스템 2025 Korea Paddle Stripe", "software subscription payment gateway 2025"],
        "prompt": (
            "BIM 소프트웨어 라이선스 결제 담당자가 오늘 알아야 할 "
            "결제 시스템 동향이나 팁을 200~300자로 작성하라. "
            "Paddle/Stripe 수수료 구조, 구독 갱신 자동화, 환불 정책을 포함하라."
        ),
    },
    "러닝콘텐츠디자이너": {
        "title": "BIM 러닝 콘텐츠 설계 최신 동향",
        "tags": "learning,content,design,update",
        "queries": ["BIM 온라인 교육 콘텐츠 설계 2025 eLearning", "BIM eLearning instructional design 2025"],
        "prompt": (
            "BIM 학습 콘텐츠 디자이너가 오늘 알아야 할 콘텐츠 설계 트렌드나 "
            "도구를 200~300자로 작성하라. "
            "마이크로러닝 설계, AI 기반 콘텐츠 제작, NotebookLM 활용법을 포함하라."
        ),
    },
    "배포문서": {
        "title": "소프트웨어 배포 문서화 최신 기준",
        "tags": "deployment,documentation,release,update",
        "queries": ["소프트웨어 배포 문서화 기준 2025 릴리스 노트", "software release documentation best practices"],
        "prompt": (
            "BIM 소프트웨어 배포 문서 담당자가 오늘 알아야 할 "
            "문서화 기준이나 팁을 200~300자로 작성하라. "
            "릴리스 노트 작성 기준, 설치 가이드 표준화, Autodesk Store 제출 문서를 포함하라."
        ),
    },
    "법규변경모니터링": {
        "title": "건설·BIM 관련 법규 변경 모니터링",
        "tags": "regulation,monitoring,BIM,update",
        "queries": ["건설 건축 소방 법규 최신 개정 2025 고시", "Korea construction building code regulation update 2025"],
        "prompt": (
            "건설·건축·소방 법규 모니터링 담당자가 오늘 알아야 할 "
            "최신 법규 변경 사항을 200~300자로 작성하라. "
            "건축법, 소방법, KDS/KCS 최신 개정 고시 번호와 주요 변경 내용을 포함하라."
        ),
    },
    "브랜드마케팅": {
        "title": "BIM 브랜드·마케팅 최신 동향",
        "tags": "marketing,brand,AEC,update",
        "queries": ["AEC BIM 소프트웨어 마케팅 전략 2025", "BIM software marketing content strategy 2025"],
        "prompt": (
            "BIM 소프트웨어 브랜드·마케팅 담당자가 오늘 알아야 할 "
            "마케팅 트렌드나 팁을 200~300자로 작성하라. "
            "AEC 콘텐츠 마케팅, LinkedIn 전략, 기술 블로그 운영 방법을 포함하라."
        ),
    },
    "빌드검증": {
        "title": "Revit Add-in 빌드 검증 최신 기준",
        "tags": "build,validation,revit,qa,update",
        "queries": ["Revit Add-in 빌드 검증 테스트 2025 Autodesk Store", "Revit addin build validation CI/CD"],
        "prompt": (
            "Revit Add-in 빌드 검증 담당자가 오늘 알아야 할 "
            "검증 기준이나 자동화 팁을 200~300자로 작성하라. "
            "Revit 버전별 smoke test, Autodesk Store 심사 대응, CI/CD 파이프라인을 포함하라."
        ),
    },
    "스토어심사": {
        "title": "Autodesk Store 심사 최신 기준",
        "tags": "autodesk-store,review,submission,update",
        "queries": ["Autodesk App Store 심사 기준 2025 거절 사유", "Autodesk store submission review 2025"],
        "prompt": (
            "Autodesk App Store 심사 담당자가 오늘 알아야 할 "
            "심사 기준 변화나 통과 팁을 200~300자로 작성하라. "
            "최근 거절 사유 패턴, 문서 요건, 개인정보 정책 기준을 포함하라."
        ),
    },
    "아이디어발굴": {
        "title": "BIM 신규 아이디어 발굴 최신 동향",
        "tags": "innovation,idea,BIM,update",
        "queries": ["BIM AI 자동화 신규 아이디어 2025 AEC", "BIM innovation AI automation ideas 2025"],
        "prompt": (
            "BIM 신규 아이디어 발굴 담당자가 오늘 알아야 할 "
            "혁신 기회나 트렌드를 200~300자로 작성하라. "
            "AI+BIM 융합 아이디어, 해결 안 된 현장 문제, 상품화 가능 기술을 포함하라."
        ),
    },
    "엑셀자동화": {
        "title": "엑셀·업무 자동화 최신 기법 업데이트",
        "tags": "excel,automation,python,update",
        "queries": ["엑셀 파이썬 자동화 openpyxl 최신 기법 2025", "Excel automation Python openpyxl 2025"],
        "prompt": (
            "엑셀 업무 자동화 담당자가 오늘 알아야 할 "
            "최신 자동화 기법이나 라이브러리 팁을 200~300자로 작성하라. "
            "openpyxl, pandas, xlwings 최신 기능, BIM 연동 자동화를 포함하라."
        ),
    },
    "외주관리": {
        "title": "외주 협력사 관리 최신 기준",
        "tags": "outsourcing,vendor,management,update",
        "queries": ["BIM 외주 협력사 관리 계약 기준 2025", "BIM outsourcing vendor management Korea"],
        "prompt": (
            "BIM 외주·협력사 관리 담당자가 오늘 알아야 할 "
            "관리 기준이나 팁을 200~300자로 작성하라. "
            "외주 계약 핵심 조항, 품질 평가 기준, 리스크 관리 방법을 포함하라."
        ),
    },
    "요구사항분석": {
        "title": "BIM 요구사항 분석 최신 방법론",
        "tags": "requirements,analysis,BIM,update",
        "queries": ["BIM 요구사항 분석 방법론 2025 EIR", "BIM requirements analysis stakeholder Korea"],
        "prompt": (
            "BIM 요구사항 분석 담당자가 오늘 알아야 할 "
            "분석 방법론이나 팁을 200~300자로 작성하라. "
            "이해관계자 인터뷰 기법, EIR 작성 방법, 요구사항 우선순위화를 포함하라."
        ),
    },
    "인프라_DevOpsObsidian": {
        "title": "DevOps·Obsidian 인프라 최신 동향",
        "tags": "devops,obsidian,infrastructure,update",
        "queries": ["Obsidian 지식관리 DevOps 자동화 2025", "knowledge management DevOps automation 2025"],
        "prompt": (
            "DevOps·Obsidian 지식 인프라 담당자가 오늘 알아야 할 "
            "최신 자동화 팁이나 도구 동향을 200~300자로 작성하라. "
            "Obsidian 플러그인 활용, CI/CD 자동화, 지식베이스 품질 관리를 포함하라."
        ),
    },
    "제품패키징": {
        "title": "BIM 제품 패키징 최신 기준",
        "tags": "product,packaging,release,update",
        "queries": ["Autodesk Add-in 제품 패키징 번들 2025", "BIM software product packaging distribution"],
        "prompt": (
            "BIM 소프트웨어 제품 패키징 담당자가 오늘 알아야 할 "
            "패키징 기준이나 팁을 200~300자로 작성하라. "
            "설치 패키지 구성, 버전 관리, Autodesk Store 번들 제출 방법을 포함하라."
        ),
    },
    "지식업데이트": {
        "title": "지식 관리 및 업데이트 운영 최신 기준",
        "tags": "knowledge,governance,update",
        "queries": ["지식 관리 KM 시스템 자동화 2025", "knowledge management automation AI 2025"],
        "prompt": (
            "지식 관리 담당자가 오늘 알아야 할 "
            "지식 관리 자동화 트렌드나 운영 팁을 200~300자로 작성하라. "
            "AI 기반 지식 큐레이션, RAG 시스템 적용, 품질 관리 기준을 포함하라."
        ),
    },
    "지식큐레이터": {
        "title": "지식 큐레이션 최신 방법론",
        "tags": "knowledge,curation,intelligence,update",
        "queries": ["AI 지식 큐레이션 방법론 2025 RAG", "knowledge curation AI intelligence 2025"],
        "prompt": (
            "지식 큐레이터가 오늘 알아야 할 "
            "큐레이션 방법론이나 도구 트렌드를 200~300자로 작성하라. "
            "AI 보조 큐레이션, 출처 검증 방법, 지식 승격 기준을 포함하라."
        ),
    },
    "최고전략CSO": {
        "title": "최고전략책임자 전략 인텔리전스 업데이트",
        "tags": "cso,strategy,BIM,update",
        "queries": ["AEC BIM 전략 방향 2025 디지털 전환", "AEC digital transformation strategy 2025"],
        "prompt": (
            "BIM 회사 최고전략책임자(CSO)가 오늘 알아야 할 "
            "전략적 인사이트를 200~300자로 작성하라. "
            "AEC 디지털 전환 방향, 신사업 기회, 경쟁사 동향을 포함하라."
        ),
    },
    "테크니컬_라이터": {
        "title": "테크니컬 라이팅 최신 기준 업데이트",
        "tags": "technical-writing,documentation,update",
        "queries": ["테크니컬 라이팅 BIM 문서화 기준 2025", "technical writing AEC documentation best practices"],
        "prompt": (
            "BIM 테크니컬 라이터가 오늘 알아야 할 "
            "문서화 기준이나 트렌드를 200~300자로 작성하라. "
            "사용자 가이드 구조, API 문서화, Docs-as-Code 방법론을 포함하라."
        ),
    },
    "파이프라인_오케스트레이터": {
        "title": "데이터 파이프라인 오케스트레이션 최신 동향",
        "tags": "pipeline,orchestration,automation,update",
        "queries": ["데이터 파이프라인 오케스트레이션 2025 Airflow", "BIM data pipeline orchestration automation"],
        "prompt": (
            "BIM 데이터 파이프라인 오케스트레이터가 오늘 알아야 할 "
            "최신 자동화 기법이나 도구를 200~300자로 작성하라. "
            "Python 스케줄러, LaunchAgent, cron 관리, 에러 처리 패턴을 포함하라."
        ),
    },
    "프로그램개발": {
        "title": "BIM 소프트웨어 개발 최신 동향",
        "tags": "development,revit-api,csharp,update",
        "queries": ["Revit API C# 개발 최신 트렌드 2025", "BIM software development .NET Revit 2025"],
        "prompt": (
            "BIM 소프트웨어 개발자가 오늘 알아야 할 "
            "개발 트렌드나 기술 팁을 200~300자로 작성하라. "
            "Revit API 2025 변경 사항, .NET 최신 기법, "
            "Autodesk Store 심사 기술 요건을 포함하라."
        ),
    },
    "프롬프트엔지니어": {
        "title": "프롬프트 엔지니어링 최신 기법",
        "tags": "prompt-engineering,AI,LLM,update",
        "queries": ["프롬프트 엔지니어링 최신 기법 2025 Claude", "prompt engineering best practices LLM 2025"],
        "prompt": (
            "BIM 도메인 프롬프트 엔지니어가 오늘 알아야 할 "
            "최신 프롬프트 기법이나 LLM 활용법을 200~300자로 작성하라. "
            "Chain-of-Thought, RAG 연동, 구조화 출력, 캐싱 전략을 포함하라."
        ),
    },
    "협력사안부": {
        "title": "협력사 안부 및 관계 관리 업데이트",
        "tags": "partner,relationship,communication,update",
        "queries": ["BIM 파트너사 협력사 관계 관리 2025", "BIM partner relationship management Korea"],
        "prompt": (
            "BIM 협력사 관계 관리 담당자가 오늘 알아야 할 "
            "파트너십 관리 팁이나 동향을 200~300자로 작성하라. "
            "정기 안부 체계, 협력사 평가 기준, 신규 파트너 발굴 방법을 포함하라."
        ),
    },
    "경비정산_AI": {
        "title": "AI 기반 경비 정산 최신 동향",
        "tags": "expense,ai,automation,update",
        "queries": ["AI 경비 정산 자동화 2025 OCR", "AI expense management automation OCR Korea"],
        "prompt": (
            "AI 기반 경비 정산 담당자가 오늘 알아야 할 "
            "자동화 기법이나 도구 동향을 200~300자로 작성하라. "
            "OCR 영수증 인식, 회계 연동, 이상 지출 탐지 방법을 포함하라."
        ),
    },
    "QA_테스터": {
        "title": "BIM Add-in QA 테스트 최신 기준",
        "tags": "qa,testing,revit,update",
        "queries": ["Revit Add-in QA 테스트 자동화 2025", "BIM software QA testing automation 2025"],
        "prompt": (
            "BIM Add-in QA 테스터가 오늘 알아야 할 "
            "테스트 기준이나 자동화 팁을 200~300자로 작성하라. "
            "Revit 버전별 회귀 테스트, UI 자동화, P1/P2 버그 기준을 포함하라."
        ),
    },
    "Caveman_토큰다이어터": {
        "title": "AI 토큰 최적화 최신 기법",
        "tags": "token-optimization,AI,cost,update",
        "queries": ["Claude API 토큰 최적화 캐싱 비용 2025", "LLM token optimization prompt caching 2025"],
        "prompt": (
            "AI 토큰 비용 최적화 담당자가 오늘 알아야 할 "
            "토큰 절감 기법이나 캐싱 전략을 200~300자로 작성하라. "
            "프롬프트 캐싱, 응답 압축, 모델 선택 기준을 포함하라."
        ),
    },
    "EIRBEP_심사원": {
        "title": "EIR·BEP 심사 최신 기준 업데이트",
        "tags": "EIR,BEP,review,update",
        "queries": ["BIM EIR BEP 심사 기준 2025 국토부", "EIR BEP review standard Korea 2025"],
        "prompt": (
            "EIR·BEP 심사원이 오늘 알아야 할 "
            "심사 기준 변화나 체크포인트를 200~300자로 작성하라. "
            "국토부 BIM 지침 기반 심사 항목, 자주 발생하는 미비 사항을 포함하라."
        ),
    },
    "산업동향_데일리브리핑": {
        "title": "BIM·건설 산업 동향 데일리 업데이트",
        "tags": "industry,daily-briefing,BIM,construction,update",
        "queries": ["BIM 건설 산업 동향 최신 뉴스 2025", "AEC BIM construction news today 2025"],
        "prompt": (
            "BIM·건설 산업 데일리 브리핑 담당자가 오늘 정리해야 할 "
            "주요 산업 동향 인사이트를 200~300자로 작성하라. "
            "Autodesk 동향, 국내 BIM 정책, 스마트 건설 기술 트렌드를 포함하라."
        ),
    },
}


# ---------------------------------------------------------------------------
# 태그 유사도 기반 관련 토픽 사전 계산
# ---------------------------------------------------------------------------
_STOP_TAGS = {"update"}


def _build_related_map() -> dict[str, list[str]]:
    """KB_TOPICS 태그 overlap으로 각 파일의 관련 파일 top-5를 사전 계산."""
    tag_sets: dict[str, set[str]] = {}
    for stem, topic in KB_TOPICS.items():
        raw = topic.get("tags", "")
        tag_sets[stem] = {
            t.strip() for t in raw.split(",")
            if t.strip() and t.strip() not in _STOP_TAGS
        }
    stems = list(tag_sets.keys())
    related: dict[str, list[str]] = {}
    for stem in stems:
        my_tags = tag_sets[stem]
        if not my_tags:
            related[stem] = []
            continue
        scores = [
            (len(my_tags & tag_sets[other]), other)
            for other in stems if other != stem
        ]
        scores.sort(key=lambda x: -x[0])
        related[stem] = [s for score, s in scores if score > 0][:5]
    return related


RELATED_MAP = _build_related_map()


# ---------------------------------------------------------------------------
# 멀티 엔진 병렬 검색 (Naver + Tavily + Google CSE + DuckDuckGo)
# ---------------------------------------------------------------------------

async def _search_tavily_async(query: str, client: "_httpx.AsyncClient") -> list[dict]:
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if not api_key:
        return []
    try:
        resp = await client.post(
            "https://api.tavily.com/search",
            json={"api_key": api_key, "query": query, "search_depth": "basic",
                  "include_answer": True, "max_results": 4},
            timeout=12,
        )
        data = resp.json()
        results = data.get("results", [])
        answer = (data.get("answer") or "").strip()
        if answer:
            results.insert(0, {"title": "Tavily AI 요약", "content": answer,
                                "url": "", "_is_answer": True})
        return results
    except Exception as e:
        log(f"  [Tavily 오류] {e}")
        return []


async def _search_duckduckgo_async(query: str, client: "_httpx.AsyncClient") -> list[dict]:
    try:
        resp = await client.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers={"User-Agent": "Mozilla/5.0 (compatible; LUABIMBot/1.0)"},
            timeout=12,
            follow_redirects=True,
        )
        titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', resp.text, re.DOTALL)
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', resp.text, re.DOTALL)
        results = []
        for t, s in zip(titles[:5], snippets[:5]):
            title = re.sub(r"<[^>]+>", "", t).strip()
            content = re.sub(r"<[^>]+>", "", s).strip()
            if content:
                results.append({"title": title, "content": content})
        return results
    except Exception as e:
        log(f"  [DDG 오류] {e}")
        return []


async def _search_google_cse_async(query: str, client: "_httpx.AsyncClient") -> list[dict]:
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    cse_id = os.environ.get("GOOGLE_CSE_ID", "")
    if not api_key or not cse_id:
        return []
    try:
        resp = await client.get(
            "https://www.googleapis.com/customsearch/v1",
            params={"key": api_key, "cx": cse_id, "q": query, "num": 4, "hl": "ko"},
            timeout=12,
        )
        return [
            {"title": item.get("title", ""), "content": item.get("snippet", ""),
             "url": item.get("link", "")}
            for item in resp.json().get("items", [])
        ]
    except Exception as e:
        log(f"  [Google CSE 오류] {e}")
        return []


async def _search_naver_async(query: str, client: "_httpx.AsyncClient") -> list[dict]:
    client_id = os.environ.get("NAVER_CLIENT_ID", "")
    client_secret = os.environ.get("NAVER_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        return []
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
    results: list[dict] = []
    try:
        for search_type in ("webkr", "news"):
            resp = await client.get(
                f"https://openapi.naver.com/v1/search/{search_type}.json",
                params={"query": query, "display": 4, "sort": "sim"},
                headers=headers,
                timeout=12,
            )
            if resp.status_code != 200:
                continue
            for item in resp.json().get("items", []):
                title = re.sub(r"<[^>]+>", "", item.get("title", "")).strip()
                desc = re.sub(r"<[^>]+>", "", item.get("description", "")).strip()
                url = item.get("link", "") or item.get("originallink", "")
                if desc:
                    results.append({"title": title, "content": desc, "url": url})
    except Exception as e:
        log(f"  [Naver 오류] {e}")
    return results


async def _run_multi_search(query: str) -> str:
    """4개 엔진 병렬 검색 후 병합 결과 반환."""
    async with _httpx.AsyncClient() as client:
        naver_r, tavily_r, google_r, ddg_r = await asyncio.gather(
            _search_naver_async(query, client),
            _search_tavily_async(query, client),
            _search_google_cse_async(query, client),
            _search_duckduckgo_async(query, client),
        )

    seen: set[str] = set()
    blocks: list[str] = []

    for label, items in [("Naver", naver_r), ("Google", google_r),
                         ("Tavily", tavily_r), ("DDG", ddg_r)]:
        for item in items:
            if item.get("_is_answer"):
                content = (item.get("content") or "").strip()[:500]
                if content and content[:60] not in seen:
                    seen.add(content[:60])
                    blocks.insert(0, f"• [Tavily AI요약] {content}")
                continue
            content = (item.get("content") or "").strip()[:300]
            if content and content[:60] not in seen:
                seen.add(content[:60])
                url = item.get("url", "")
                blocks.append(f"• [{label}] {item.get('title','')}\n  {content}"
                               + (f"\n  출처: {url}" if url else ""))

    return "\n\n".join(blocks[:8])


def multi_engine_search(query: str) -> str:
    """동기 래퍼 — asyncio.run()으로 병렬 검색 실행."""
    if not _HTTPX_AVAILABLE:
        log("  httpx 미설치 — 검색 스킵")
        return ""
    try:
        return asyncio.run(_run_multi_search(query))
    except Exception as e:
        log(f"  멀티 엔진 검색 오류 ({query[:40]}): {e}")
        return ""


# ---------------------------------------------------------------------------
# AI 콘텐츠 생성 (Ollama 우선 → Anthropic 폴백)
# ---------------------------------------------------------------------------

def _ollama_generate(prompt: str) -> str:
    """로컬 Ollama(qwen2.5:7b)로 텍스트 생성."""
    base_url = os.environ.get("LOCAL_CODER_BASE_URL", "http://127.0.0.1:11434")
    model = os.environ.get("KNOWLEDGE_QA_MODEL", "qwen2.5:7b")
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 600, "temperature": 0.4},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("response", "").strip()


def _anthropic_generate(prompt: str) -> str:
    """Anthropic Claude Haiku로 텍스트 생성 (폴백용)."""
    if not _ANTHROPIC_AVAILABLE:
        return ""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return ""
    client = _anthropic_module.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def generate_kb_section(file_stem: str, topic: dict, search_context: str) -> str:
    """KB 섹션 텍스트 생성: Ollama 우선, 실패 시 Anthropic 폴백."""
    prompt_parts = [topic["prompt"]]
    if search_context:
        prompt_parts.append(
            f"\n\n참고 검색 결과 (최신 정보, 필요 시 활용):\n{search_context[:1500]}"
        )
    prompt_parts.append(
        "\n\n출력 형식: 순수 텍스트만. 마크다운 제목(#) 없이, "
        "항목은 '- ' 불릿으로, 수치·기준·규격번호를 반드시 포함. "
        "한국어로 작성."
    )
    full_prompt = "".join(prompt_parts)

    # 1차: 로컬 Ollama
    try:
        result = _ollama_generate(full_prompt)
        if result:
            return result
    except Exception as e:
        log(f"  Ollama 오류 ({file_stem}): {e}")

    # 2차: Anthropic (크레딧 있을 때)
    try:
        result = _anthropic_generate(full_prompt)
        if result:
            return result
    except Exception as e:
        log(f"  Anthropic 오류 ({file_stem}): {e}")

    return ""


# ---------------------------------------------------------------------------
# 파일 업데이트 여부 판단
# ---------------------------------------------------------------------------
def needs_update(kb_file: Path) -> bool:
    """파일에 오늘 날짜 섹션이 없으면 업데이트 필요."""
    if not kb_file.exists():
        return True
    content = kb_file.read_text(encoding="utf-8")
    return TODAY not in content


# ---------------------------------------------------------------------------
# KB 파일에 섹션 append
# ---------------------------------------------------------------------------
def append_section(kb_file: Path, title: str, tags: str, body: str, stem: str) -> None:
    related_stems = RELATED_MAP.get(stem, [])[:4]
    related_line = ""
    if related_stems:
        links = " · ".join(f"[[{s}]]" for s in related_stems)
        related_line = f"\n- 관련: {links}"
    section = (
        f"\n\n## {title} ({TODAY})\n"
        f"- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama {TODAY}\n"
        f"- Tags: {tags}\n\n"
        f"{body}{related_line}\n"
    )
    with kb_file.open("a", encoding="utf-8") as f:
        f.write(section)


# ---------------------------------------------------------------------------
# 메인 실행
# ---------------------------------------------------------------------------
def main() -> None:
    log(f"==== {NOW} auto_enrich_knowledge_base start ====")

    ollama_url = os.environ.get("LOCAL_CODER_BASE_URL", "http://127.0.0.1:11434")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not anthropic_key:
        log("INFO: ANTHROPIC_API_KEY 미설정 — Ollama 단독 모드")
    log(f"AI 백엔드: Ollama({ollama_url}) 우선, Anthropic 폴백")

    files_to_update = []
    for stem, topic in KB_TOPICS.items():
        kb_file = KB_DIR / f"{stem}.md"
        if needs_update(kb_file):
            files_to_update.append((stem, kb_file, topic))

    log(f"업데이트 대상: {len(files_to_update)}/{len(KB_TOPICS)}개 파일")

    updated = 0
    skipped = 0
    errors = 0

    for i, (stem, kb_file, topic) in enumerate(files_to_update, 1):
        log(f"  [{i}/{len(files_to_update)}] {stem} 처리 중...")

        # 검색 — 쿼리 2개를 이어 붙여 4개 엔진 병렬 검색
        search_ctx = ""
        if topic.get("queries"):
            combined_query = " ".join(topic["queries"][:2])
            search_ctx = multi_engine_search(combined_query)

        body = generate_kb_section(stem, topic, search_ctx)
        if not body:
            log(f"    → 콘텐츠 생성 실패, 스킵")
            errors += 1
            continue

        # 파일이 없으면 헤더 생성
        if not kb_file.exists():
            kb_file.write_text(f"# {stem} 지식 베이스\n", encoding="utf-8")

        append_section(kb_file, topic["title"], topic["tags"], body, stem)
        log(f"    → 완료 ({len(body)}자)")
        updated += 1

        # API 레이트 리밋 방지
        if i < len(files_to_update):
            time.sleep(1.5)

    log(
        f"==== 완료: 업데이트 {updated}개 | 스킵 {skipped}개 | 오류 {errors}개 ===="
    )


if __name__ == "__main__":
    main()
