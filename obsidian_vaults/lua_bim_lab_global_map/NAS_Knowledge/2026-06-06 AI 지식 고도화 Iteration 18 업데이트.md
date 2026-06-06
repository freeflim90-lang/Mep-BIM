# 2026-06-06 AI 지식 고도화 Iteration 18 업데이트

## 업데이트 개요
- 날짜: 2026-06-06
- 이터레이션: 18
- 보강 파일: OpenBIM_프로그램연동.md, 해외건설기업_동향분석.md
- 소스: thefuture3d.com Scan-to-BIM 2026, Leica CloudWorx, Nemetschek/Vectorworks 2026 Update 4

---

## 1. OpenBIM_프로그램연동.md — Scan-to-BIM·포인트클라우드 Reality Capture 지식 신규 추가

### 핵심 내용 (지식 공백 해소)
기존 KB에서 Scan-to-BIM / 포인트클라우드 / 현실 캡처 관련 지식이 전무(全無)했음 → 신규 보강

**Scan-to-BIM 워크플로우 (2026):**
1. 현장 LiDAR 스캔 (1~3일)
2. 포인트클라우드 처리·등록 (2~5일) → .e57 / .rcp / .las 출력
3. Revit BIM 모델링 (4~16주, LOD에 따라 상이)
4. 품질 검증: LOD 300 ±5mm, LOD 400 ±2mm 허용 오차

**주요 스캐너 비교 (2026):**
| 스캐너 | 최대 범위 | 정확도 | 적합 용도 |
|--------|---------|--------|---------|
| Leica RTC360 | 130m | ±1.9mm | 실내·중소 건물 |
| FARO Focus Premium | 350m | ±1mm | 대형 시설·외벽 |
| Matterport Pro3 | 20m | ±20mm | VR 투어 (AEC 납품 부적합) |

**Revit 포인트클라우드 연동:**
- .rcp → Revit Insert > Link Point Cloud (Autodesk ReCap 경유)
- .e57 → Revit 2022+ 직접 링크
- Leica CloudWorx for Revit 플러그인: 단면 슬라이싱, 스캔-BIM 편차 체크

**국내 적용 현황:**
- 노후 공공건물 리모델링 (도면 부재 건물)
- 준공 검측 자동화 (설계 BIM vs 스캔 비교)
- 플랜트·반도체 시설 정밀 설비 배치

**LUA BIM LABS 기회:**
- Add-in: 포인트클라우드 자동 정합 기능
- 서비스: 리모델링 전문 Scan-to-BIM LOD 300 패키지
- MQA 연동: 준공 스캔 vs BIM 자동 편차 검사

---

## 2. 해외건설기업_동향분석.md — Nemetschek 2026 전략·Vectorworks 2026 Update 4

### 핵심 내용
**Nemetschek 그룹 통합 생태계 전략:**
- 브랜드: Graphisoft (Archicad) · Vectorworks · Bluebeam · Maxon · dRofus
- 전략: 브랜드 독립 유지 + 브랜드 간 네이티브 통합 (Autodesk 대항 OpenBIM 연합)

**Vectorworks 2026 Update 4 (2026-03 출시) 주요 기능:**
- **Data-Driven Phasing**: BIM 모델에 시간 축 내장 (existing/new/demolished/relocated/temporary)
- **Embodied Carbon Analysis**: 내재탄소 분석 내장 → LCA 자동 계산 (ESG 설계 대응)
- **Maxon Redshift 통합**: 실시간 렌더링 직접 통합 (Nemetschek 그룹 브랜드 시너지)

**LUA BIM LABS 연계:**
- 내재탄소 기능 내장 트렌드 → Add-in에 BIM 자재 탄소계수 파라미터 체크 기능 필요
- Phasing BIM + Scan-to-BIM 조합 → 리모델링 BIM 전문 서비스 가능

---

## 지식 공백 식별 방법
- grep 검색: "scan", "point.cloud", "포인트클라우드" → 기존 KB에서 핵심 기술 파일 전무 확인
- 해외 BIM SW 경쟁 지형 파일 → Nemetschek 최신 동향 갱신 필요

## 연관 지식
- [[OpenBIM_프로그램연동]] · [[해외건설기업_동향분석]]
- [[FM_자산관리]] · [[BIM_납품검수]] · [[Revit_Addin]] · [[시설유형]]
