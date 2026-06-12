"""
BIM 기술 문서 PDF 수집기
국내외 공개 기술 기준서·가이드라인을 수집한다.
주로 무료·공개 자료만 대상으로 한다.
"""

from __future__ import annotations

import json
import os
import sys
import time
import shutil
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys as _sys  # noqa: E402
if str(PROJECT_ROOT) not in _sys.path:
    _sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import TECHNICAL_PDFS_DIR  # noqa: E402

PDF_OUTPUT = TECHNICAL_PDFS_DIR
PDF_OUTPUT.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/pdf,text/html,*/*",
}

# 공개 자료 직접 링크 목록 (무료·공개 자료만)
DIRECT_PDF_SOURCES: list[dict] = [
    # buildingSMART IFC 사양 (공개)
    {
        "name": "IFC4_Add2_TC1_Release_Notes",
        "url": "https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/annex/annex-e.htm",
        "category": "ifc_standard",
        "language": "en",
    },
    # ASHRAE 62.1 환기 기준 (공개 요약)
    {
        "name": "ASHRAE_62_1_Ventilation_Overview",
        "url": "https://www.ashrae.org/file%20library/technical%20resources/standards%20and%20guidelines/standards%20addenda/62_1_2016_b_20180313.pdf",
        "category": "hvac_standard",
        "language": "en",
    },
    # EU BIM Handbook (공개)
    {
        "name": "EU_BIM_Handbook",
        "url": "https://www.eubim.eu/wp-content/uploads/2017/07/EUBIM_Handbook_Web_Chapter1.pdf",
        "category": "bim_general",
        "language": "en",
    },
    # Singapore BIM Guide (공개)
    {
        "name": "Singapore_BIM_Guide_v2",
        "url": "https://www.corenet.gov.sg/media/586996/Singapore-BIM-Guide_V2.pdf",
        "category": "bim_guide",
        "language": "en",
    },
    # buildingSMART IFC for MEP (공개)
    {
        "name": "buildingSMART_MEP_Summary",
        "url": "https://standards.buildingsmart.org/IFC/DEV/IFC4_2/FINAL/HTML/link/ifcdistributionelement.htm",
        "category": "ifc_mep",
        "language": "en",
    },
]

# 웹 페이지 스크래핑 대상 (링크 추출 방식)
WEB_SCRAPE_SOURCES: list[dict] = [
    # UK NBS BIM Resources
    {
        "name": "NBS_BIM_Resources",
        "url": "https://www.thenbs.com/knowledge/bim",
        "category": "bim_standards",
        "pdf_pattern": ".pdf",
    },
]

TARGET_SIZE_MB = 2048  # 목표 2GB


def get_disk_usage_percent() -> float:
    usage = shutil.disk_usage("/")
    return (usage.used / usage.total) * 100


def get_collected_pdf_size_mb() -> float:
    total = sum(f.stat().st_size for f in PDF_OUTPUT.rglob("*.pdf") if f.is_file())
    return total / (1024 * 1024)


def download_pdf(url: str, dest_path: Path, timeout: int = 60) -> bool:
    """PDF를 다운로드한다."""
    if dest_path.exists():
        print(f"    이미 존재: {dest_path.name}")
        return True
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout, stream=True)
        if response.status_code == 200:
            content_type = response.headers.get("content-type", "")
            if "pdf" in content_type.lower() or url.lower().endswith(".pdf"):
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                with open(dest_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                size_kb = dest_path.stat().st_size / 1024
                print(f"    ↓ {dest_path.name} ({size_kb:.1f} KB)")
                return True
            else:
                print(f"    PDF 아님 (content-type: {content_type})")
                return False
        else:
            print(f"    HTTP {response.status_code}: {url}")
            return False
    except Exception as e:
        print(f"    다운로드 실패: {e}")
        return False


def save_metadata(source: dict, dest_path: Path, success: bool) -> None:
    """다운로드 메타데이터를 저장한다."""
    meta_path = dest_path.with_suffix(".json")
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "name": source.get("name"),
        "url": source.get("url"),
        "category": source.get("category"),
        "language": source.get("language", "ko"),
        "downloaded_at": datetime.now().isoformat(),
        "success": success,
        "file_size_kb": dest_path.stat().st_size / 1024 if dest_path.exists() else 0,
    }
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")


def collect_direct_pdfs() -> int:
    """직접 링크 PDF를 수집한다."""
    collected = 0
    print("\n=== 직접 링크 PDF 수집 ===")

    for source in DIRECT_PDF_SOURCES:
        name = source["name"]
        url = source["url"]
        category = source.get("category", "general")
        print(f"\n  [{category}] {name}")
        print(f"  URL: {url}")

        dest_path = PDF_OUTPUT / category / f"{name}.pdf"
        success = download_pdf(url, dest_path)
        save_metadata(source, dest_path, success)

        if success:
            collected += 1

        current_size = get_collected_pdf_size_mb()
        print(f"  현재 PDF 수집 크기: {current_size:.1f} MB")

        if current_size >= TARGET_SIZE_MB:
            print("목표 크기 도달!")
            break

        time.sleep(2)

    return collected


def generate_text_knowledge_docs() -> int:
    """PDF 대신 구조화된 텍스트 지식 문서를 생성한다."""
    print("\n=== 텍스트 기반 기술 지식 문서 생성 ===")
    text_output = TECHNICAL_PDFS_DIR / "text_knowledge"
    text_output.mkdir(parents=True, exist_ok=True)

    # 국내 소방법 기준 요약 문서
    nftc_knowledge = """# 화재안전기술기준(NFTC) 핵심 요약
## 출처: 소방청 화재안전기술기준 공개 정보 기반 요약
## 작성: LUA BIM LABS Knowledge Team
## 날짜: 2026-05-23

---

## NFTC 103 스프링클러설비 핵심 기준

### 헤드 배치 기준 (NFTC 103 제7조)
- 표준형 헤드 최대 방호면적: 20 m² (표준위험) 또는 10 m² (고위험)
- 헤드 간 최대 거리: 4.6m (NFPA 13 기준 차용, 국내 NFTC 103 확인 필요)
- 헤드와 벽 이격: 헤드 방호반경 × 0.5 이상, 최소 100mm
- 헤드 디플렉터와 천장 마감 거리: 25~305mm

### 수계 소화설비 배관 기준
- 가지관 최소 관경: DN25
- 교차배관: DN32 이상
- 주배관(급수관): DN50 이상
- 최저 방수압: 0.1 MPa
- 최고 방수압: 1.2 MPa
- 최저 방수량: 80 L/min (헤드당)

### 소화수조 및 소방펌프 기준 (NFTC 402, NFTC 103)
- 소화수조 용량: 동시 방수 헤드 수 × 1.6 m³ 이상 (표준위험)
- 소방펌프: 주펌프 + 예비펌프 + 충압펌프 3대 구성
- 충압펌프 자동 기동: 배관 내 압력이 설정압력 이하로 낮아질 때
- 주펌프 자동 기동: 충압펌프만으로 압력 유지 불가 시

---

## NFTC 203 자동화재탐지설비 핵심 기준

### 감지기 설치 기준
- 차동식 스포트형 1종:
  - 4m 미만: 50 m² / 개
  - 4m 이상 8m 미만: 50 m² / 개 (2종은 30 m²)
- 정온식 스포트형:
  - 4m 미만: 바닥 면적 30~70 m² (등급별 상이)
- 광전식(연기감지기):
  - 복도·통로: 보행 15m마다 1개
  - 계단·경사로: 수직거리 15m마다 1개

### 수신기 기준
- P형 수신기: 감지기 신호를 공통선으로 수신
- R형 수신기: 주소형 감지기, 개별 주소 감지 가능 → 대형 건물에 적합

---

## NFTC 501 제연설비 핵심 기준

### 가압 제연 기준 (NFTC 501A 부속실 가압)
- 부속실 최소 차압: 40 Pa (방화문 폐쇄 상태)
- 최대 차압: 60 Pa (방화문 개방 시 상한)
- 피난 계단실: 40 Pa 이상 가압
- 급기량 산정: 문 틈새, 누기 면적, 차압 기준

### 배연 설비 기준 (NFTC 501)
- 배연 풍량: 해당 방호구역 면적 × 1 m³/min/m² 이상 (최소)
- 배연구 위치: 천장 또는 천장에서 80cm 이내 벽면
- 흡입 속도: 배연구에서 최대 10 m/s 이하

---

## 건축물 에너지절약 설계기준 핵심 요약

### 공조 설비 기준
- 외기 도입: 최소 환기량 확보 의무
- 전열교환기 설치 의무: 연면적 3,000 m² 이상 업무시설
- 공조 배관 단열 기준: [별표 3] 배관 용도별 단열재 두께 기준

### 배관 단열 두께 기준 (냉수 배관 예시, [별표 3])
- DN50 이하 냉수 배관: 25mm 이상 (냉동고무발포체 기준)
- DN50 초과 ~ DN100 이하: 32mm 이상
- DN100 초과: 38mm 이상

---

## 기계설비법 핵심 기준

### 적용 대상 (기계설비법 제2조)
- 건축법 제2조에 따른 건축물의 기계 설비
- 냉난방·환기·위생·자동제어·방음·방진 설비 포함

### 주요 의무
- 대형 건물 기계설비 성능 점검: 연 1회 이상
- 기계설비 유지관리 기준 준수
- 기계설비 설계·시공·감리 분리 의무 (일정 규모 이상)

---
"""

    ashrae_knowledge = """# ASHRAE 핵심 기준 요약 (설계 참고)
## 출처: ASHRAE 공개 정보 기반 요약
## 작성: LUA BIM LABS Knowledge Team
## 날짜: 2026-05-23

---

## ASHRAE Standard 62.1 환기 기준

### 최소 환기량 (사람 기준)
- 사무실: 10 cfm/person (= 약 17 m³/h/person)
- 회의실: 10 cfm/person
- 교실: 10 cfm/person + 0.12 cfm/ft²
- 병원 일반 병실: 25 cfm/person
- 한국 기준: 1인당 25 m³/h 이상 (건축물 설비기준 등에 관한 규칙)

### CO₂ 농도 관리
- 실내 CO₂ 목표: 1,000 ppm 이하 (한국: 실내공기질 관리법)
- 외기 CO₂: 약 400 ppm
- 차이 600 ppm 이하 유지가 목표

---

## ASHRAE Standard 55 온열쾌적 기준

### 실내 온열 쾌적 범위
- 여름: 23~26℃, 상대습도 30~60%
- 겨울: 20~23.5℃, 상대습도 30~60%
- 활동량, 착의량에 따라 범위 변동

### 유효 드래프트(Draft) 기준
- 취출구 주변 기류 속도: 0.25 m/s 이하 권장
- 고령자, 민감군: 0.15 m/s 이하

---

## ASHRAE Handbook - HVAC 시스템

### 전공기 방식 (All-Air System)
- CAV: 일정 풍량, 온도 제어 → 정압 손실 등마찰법 0.8~1.2 Pa/m
- VAV: 가변 풍량, 정압 제어 → 팬 인버터 필수, 최소풍량 설정 중요
- 이중덕트: SA와 냉온기를 말단에서 혼합 → 에너지 비효율로 신규 적용 감소

### 전수 방식 (All-Water System)
- FCU: 실내기 + 냉온수 코일 → 소규모 개별 제어에 유리
- 4관식: 냉방·난방 동시 공급 → 혼합 부하가 발생하는 병원·호텔에 적합
- 2관식: 냉방·난방 계절별 전환 → 단순하지만 전환 기간 부분 부하 대응 어려움

### 냉방 사이클 성능 지표
- COP(Coefficient of Performance): 냉동기 냉방 효율. COP=냉방 능력(kW)/소비전력(kW)
- EER(Energy Efficiency Ratio): 냉방 효율. EER = 냉방 능력(Btu/h)/소비전력(W)
- IPLV(Integrated Part Load Value): 부분부하 통합 효율. 연간 에너지 소비 대표값

### 배관 유속 설계 기준 (ASHRAE)
- 냉수 배관: 1.5~3.0 m/s (메인), 0.5~1.5 m/s (분기)
- 냉각수 배관: 0.9~2.4 m/s
- 증기 배관: 25~35 m/s (저압), 35~50 m/s (중압)

---

## ASHRAE Standard 15 냉매 안전 기준

### 냉매 허용 농도 (밀폐 공간)
- R-410A: ASHRAE 그룹 A1 (낮은 독성, 낮은 연소성)
- 기계실 환기: 냉매 누출 시 최대 1,000 ppm 미만 유지
- 직접 팽창식 시스템이 사람이 있는 공간에 설치될 때 최대 허용 농도 적용

### 기계실 환기
- 냉동기 기계실: 최소 0.5 ACH(시간당 환기횟수) 또는 냉매 누설 감지 시 자동 강제 환기

---
"""

    mep_coordination_knowledge = """# MEP BIM 조율 실무 기준 문서
## 출처: LUA BIM LABS 실무 기준 정리
## 작성: LUA BIM LABS Knowledge Team
## 날짜: 2026-05-23

---

## BIM 조율(Coordination) 절차

### 1단계: BIM 모델 준비
- 각 공종(건축·구조·공조·위생·전기·통신·소방) 모델 완성도 확인
- Revit 링크 또는 NWC 내보내기로 Navisworks에 통합
- 공종별 색상 코드 설정으로 시각 구분

### 2단계: 간섭 검토 (Clash Detection)
- Navisworks Manage에서 Clash Detective 실행
- 규칙 설정: 공종별 허용 이격 기준 입력
- 결과 분류: Hard Clash(물리 충돌) / Soft Clash(이격 부족) / Duplicate(중복 요소)

### 3단계: 이슈 관리
- 이슈별 담당 공종, 조치 방향, 우선순위 분류
- BIM 협의 보고서 작성: 이슈 번호, 위치, 사진, 조치 방법, 상태
- 정기 조율 회의에서 이슈 해결 현황 공유

### 4단계: 수정 반영 및 재검토
- 각 공종 담당자가 모델 수정 후 재검토
- 해결된 이슈는 Resolved로 처리
- 미해결 이슈는 설계 질의(RFI)로 전환

---

## 이격 기준표 (BIM 조율 기본값)

| 계통 A | 계통 B | 최소 이격 | 비고 |
|--------|--------|-----------|------|
| 강전 트레이 | 약전 트레이 | 300mm | 또는 금속 격벽 |
| 냉매 배관 | 전기 트레이 | 300mm | 단열 포함 외경 기준 |
| 가스 배관 | 전력선 | 150mm | |
| 소방 배관 | 전기 기기 | 300mm | 누수 위험 관점 |
| 제연 덕트 | 일반 설비 | 100mm | 방화구획 관통부 300mm |
| 오배수 배관 | 급수 배관 | 직접 접촉 금지 | 급수가 오배수 위로 |

---

## Revit 공종별 카테고리 기준표

### 공조 덕트
- Ducts: 주 덕트, 분기 덕트
- Duct Fittings: 엘보, T분기, 레듀서
- Duct Accessories: 댐퍼, 방화댐퍼, VAV 박스
- Mechanical Equipment: AHU, FCU, 팬

### 공조 배관
- Pipes: 냉수, 온수, 냉각수, 냉매 배관
- Pipe Fittings: 엘보, T, 리듀서
- Pipe Accessories: 밸브, 스트레이너, 팽창탱크

### 위생 배관
- Pipes: 급수, 급탕, 오배수, 통기, 우수
- Plumbing Fixtures: 세면기, 양변기, 욕조

### 전기
- Conduit: 전선관
- Cable Tray: 케이블 트레이
- Electrical Equipment: 분전반, 배전반

### 통신
- Conduit (약전 전용 레이어)
- Electrical Equipment: MDF, IDF 랙

### 소방
- Pipes (Fire Protection 계통): 스프링클러, 옥내소화전
- Sprinklers: 헤드
- Fire Protection Equipment: 알람밸브, 소방펌프

---

## 방화구획 관통 처리 기준

### 공종별 관통 처리 방법
| 공종 | 처리 방법 |
|------|-----------|
| 배관 (일반) | 방화 슬리브 + 내화채움재 (Firestop) |
| 소방 배관 | 방화 슬리브 + 내화채움재 (방화댐퍼 불필요) |
| 덕트 | 방화댐퍼 (Fire Damper) 설치 |
| 제연 덕트 | 제연댐퍼 (Smoke Damper) 또는 내화 처리 |
| 케이블·전선관 | 내화채움재 (Firestop Sealant/Mortar) |

### 내화채움재 성능 기준
- 1시간 내화: 일반 방화구획 관통부
- 2시간 내화: 주요 구조부 관통부 (건물 규모·용도에 따라 결정)
- 제품 선정: 인증된 UL 또는 국토부 인정 시험 성적서 확인

---
"""

    # 파일 저장
    docs = [
        ("nftc_fire_safety_standards_summary.md", nftc_knowledge),
        ("ashrae_hvac_standards_summary.md", ashrae_knowledge),
        ("mep_bim_coordination_guide.md", mep_coordination_knowledge),
    ]

    saved = 0
    for filename, content in docs:
        dest = text_output / filename
        dest.write_text(content, encoding="utf-8")
        size_kb = dest.stat().st_size / 1024
        print(f"  ✓ {filename} ({size_kb:.1f} KB)")
        saved += 1

    return saved


def main():
    print("=" * 60)
    print("BIM 기술 문서 수집기")
    print(f"시작: {datetime.now().isoformat()}")
    print(f"출력 디렉토리: {PDF_OUTPUT}")
    print(f"현재 SSD 사용률: {get_disk_usage_percent():.1f}%")
    print("=" * 60)

    # 1. 구조화된 텍스트 지식 문서 생성 (즉시 실행 가능)
    text_saved = generate_text_knowledge_docs()
    print(f"\n텍스트 지식 문서 {text_saved}개 생성 완료")

    # 2. 공개 PDF 다운로드 시도
    print("\n공개 PDF 다운로드 시도...")
    pdf_collected = collect_direct_pdfs()
    print(f"\nPDF {pdf_collected}개 수집 완료")

    # 최종 보고
    final_pdf_size = get_collected_pdf_size_mb()
    print("\n" + "=" * 60)
    print("수집 완료!")
    print(f"PDF 수집 크기: {final_pdf_size:.1f} MB")
    print(f"현재 SSD 사용률: {get_disk_usage_percent():.1f}%")


if __name__ == "__main__":
    main()
