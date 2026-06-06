# AI 지식 고도화 Iteration 23 업데이트 (2026-06-06)

## 보강 배경
- 목표: 토목·BIM시방서 AI 에이전트의 전문 도메인 지식 공백 해소
- 방법: auto-enrich 저품질 섹션 교체 → 법령·지침 기반 전문 지식으로 보강
- QA 결과: 35/35 → 39/39 (100%) — 새 테스트 케이스 4건 추가, 전원 통과

---

## 보강 파일 1: 토목.md

### 추가 섹션: `## 2026-06-06 IFC4.3 인프라 엔티티·Civil 3D BIM 연동·토공 물량 산출 전문 지식`

**핵심 지식:**

#### IFC4.3 인프라 도메인 핵심 엔티티
| IFC 엔티티 | 용도 |
|-----------|------|
| IfcAlignment | 선형 (평면·종단·편경사 통합) |
| IfcRoad | 도로 시설물 |
| IfcBridge | 교량 (ARCHED/CABLE_STAYED/GIRDER) |
| IfcRailway | 철도 시설물 |
| IfcEarthworksCut | 절토 |
| IfcEarthworksFill | 성토 |
| IfcPavement | 포장층 (FLEXIBLE/RIGID) |

#### Civil 3D → IFC4.3 워크플로우
1. Alignment 설계 (평면→종단→노면경사)
2. IFC 4.3 Extension (Autodesk App Store) 설치
3. IfcProject → IfcSite → IfcAlignment 계층 내보내기
4. 한국 좌표계: GRS80, TM, EPSG:5186 설정 필수

#### 토공 물량 산출
- **양단면 평균법**: V = (A1+A2)/2 × L
- **각주공식**: V = L/6 × (A1 + 4Am + A2)
- Civil 3D 토적표: 절토·성토 누적 곡선으로 운반거리 최적화

#### 발주처별 토목 BIM 납품기준
| 발주처 | 지침 | LOD |
|-------|-----|-----|
| 한국도로공사 | EX-BIM (2022) | BIL30 |
| 국가철도공단 | 철도BIM (2023) | BIL30~40 |
| LH공사 | 공동주택BIM (2024) | BIL20~30 |

---

## 보강 파일 2: BIM_시방서.md

### 추가 섹션: `## 2026-06-06 EIR 작성방법·발주처별 BIM 납품기준·BIM 과업지시서 전문 지식`

**핵심 지식:**

#### EIR 필수 포함 사항 (국토부 BIM 시행지침 발주자편)
1. 프로젝트 목적 및 BIM 활용 목표
2. BIM 정보 요구 수준 (BIL: BIM Information Level)
3. 제출 일정 (BIM 수행 마일스톤)
4. 성과품 형식 요건 (원본+IFC+PDF)
5. CDE 플랫폼 지정
6. 좌표계 및 측지계 (GRS80, 인천만 수준기면)
7. BIM 품질관리 계획

#### 문서 관계
- EIR → BIM 과업지시서 (계약 반영) → BEP (수급자 실행 계획)
- AIR: 유지관리 단계 BIM 데이터 요건

#### 발주처별 납품기준
| 발주처 | 단계 | LOD | 형식 |
|-------|-----|-----|-----|
| LH공사 | 실시설계 | BIL30 | IFC+RVT+PDF |
| 한국도로공사 | 실시설계 | BIL30 | IFC (Civil 3D) |
| 국가철도공단 | 실시설계 | BIL30~40 | IFC4.3+PDF |

#### COBie 납품 핵심
- 주요 시트: Facility/Floor/Space/Zone/Type/Component/System
- 장비 자산 데이터: 유지보수 주기, 제조사, 모델번호 필수

---

## QA 검증 결과

| 항목 | Before | After |
|------|--------|-------|
| 전체 테스트 수 | 35 | 39 |
| 통과 수 | 35 | 39 |
| 통과율 | 100% | 100% |

새 추가 테스트 케이스:
- ✅ 토목: "IFC4.3 IfcAlignment 도로 BIM Civil 3D 내보내기"
- ✅ 토목: "토공 양단면 평균법 절토 성토 물량 산출"
- ✅ BIM_시방서: "EIR 발주자정보요구사항 BIM 과업지시서 작성 방법"
- ✅ BIM_시방서: "COBie BIM 유지관리 납품 데이터 표준"

---

## 누적 현황 (Iteration 23 기준)
- QA 커버리지: 39개 도메인 질문 100% 통과
- 전문 지식 보강 완료 도메인: 구조·공조덕트·전기·건축·BIM납품검수·Revit_Addin·BIM견적·인력파견·통신·소방전기·토목·BIM시방서

## 다음 보강 후보
- `위생.md`: 절수 의무 기준, 급수·배수 수리계산 심화
- `BIM_제안서.md`: 기술제안서 BIM 항목 구성, 프레젠테이션 전략
- `패시브하우스_PHIKO.md`: ZEB 제로에너지빌딩 IFC 에너지 속성 심화

---
tags: [지식고도화, BIM, 토목, BIM시방서, IFC4.3, EIR, COBie, QA검증, Iteration23]
date: 2026-06-06
