# LUA BIM LABS 교육 상품별 커리큘럼 인덱스

문서번호: LBL-TRN-PUB-000
문서상태: 상품 커리큘럼 마스터 플랜
작성일: 2026-05-29
배포등급: Internal Planning

---

## 상품-커리큘럼 매핑 (v2 업데이트)

| 상품명 | 가격 | 상태 | 대상 레벨 | 핵심 가치 | 커리큘럼 파일 |
|---|---:|---|---|---|---|
| Starter | USD 39/월 | **런칭 완료** | Level 1 | 90일 커리큘럼 + 수료 인증서 + 퀵 레퍼런스 카드 + BIM Check Friday | `01_STARTER_60DAY_CURRICULUM.md` |
| Personal Tutor | USD 119/월 | Coming Soon | Level 1~5 | 월간 진도 보고서 + 레벨 체크 + 공종 시나리오 + 약점 보정 라이브러리 | `02_PERSONAL_TUTOR_CURRICULUM.md` |
| Coordinator Mentor | USD 229/월 | Coming Soon | Level 3 | 월 30분 Zoom 세션 + 조율 템플릿 팩 + 케이스 스터디 + 수료 인증서 | `03_COORDINATOR_MENTOR_CURRICULUM.md` |
| Project Mentor | USD 490/월 | Coming Soon | Level 4~5 | 월 1시간 Zoom 세션 + 프로젝트 템플릿 팩 + 분기 커리어 Assessment + 24h 응답 | `04_PROJECT_MENTOR_CURRICULUM.md` |

### 티어별 핵심 가치 차별화 요약

| 티어 | 소비자 심리 | 핵심 가치 제공 방식 |
|---|---|---|
| Starter $39 | "매일 1달러로 BIM 습관" | 일일 레슨 + 진행감(퀴즈/마일스톤) + 남는 자료(카드/인증서) |
| Personal Tutor $119 | "나만의 선생님" | 개인화의 증거(보고서) + 성장 측정(레벨 체크) + 공종 특화 |
| Coordinator Mentor $229 | "전문가와 함께 문제 해결" | 동기적 접촉(Zoom 30분) + 즉시 쓸 도구(템플릿) + 실사례 학습 |
| Project Mentor $490 | "내 커리어의 파트너" | 전략 파트너십(Zoom 1시간) + 문서 도구 + 분기 성장 측정 |

---

## 학습 레벨 정의

| Level | 학습자 유형 | 실무 역량 기준 | 진입 상품 |
|---|---|---|---|
| Level 1 | MEP BIM 입문자 | BIM 개념 이해, Revit MEP 미경험~3개월 | Starter |
| Level 2 | Revit MEP 모델러 | 단독 공종 모델링 가능, 1~2년 경력 | Starter → Personal Tutor |
| Level 3 | BIM 코디네이터 | 다공종 간섭 조율, 3~5년 경력 | Coordinator Mentor |
| Level 4 | MEP BIM 리드 | BEP 작성, QA/QC 운영, 5~8년 경력 | Project Mentor |
| Level 5 | BIM 자동화 학습자 | Dynamo·Python·Revit API 역량 개발 중 | Personal Tutor / Project Mentor |

---

## 커리큘럼 설계 원칙

1. 각 레슨은 실무 결과(coordination consequence)를 중심으로 설명한다.
2. 이론보다 체크 항목과 Action Item 중심으로 구성한다.
3. 기밀 프로젝트 데이터 없이 일반화된 시나리오로 설명한다.
4. 레벨이 올라갈수록 자기 주도 학습 비중이 증가한다.
5. 각 상품의 서비스 범위 내에서만 콘텐츠를 제공한다 (설계 검토·법규 확인·인증 결과 보장 금지).

---

## 공종별 트랙 선택 가이드

| 공종 | 영문명 | 추천 집중 트랙 |
|---|---|---|
| 공조/냉난방 | HVAC | 덕트 모델링, 계통 연결, 공조 간섭 |
| 배관 | Piping | 파이프 라우팅, 기계 연결, 플랜지 |
| 위생 | Plumbing/Sanitary | 수직 배관, 트랩, 연결 |
| 소방 | Fire Protection | 스프링클러, 헤드, 헤더 |
| 전기 | Electrical | 케이블 트레이, 패널, 배관 |
| 통합 조율 | General MEP Coordination | 다공종 통합, 간섭 조율 |

---

## 상품 간 업셀 경로

```
Starter (입문)
  → Personal Tutor Level 2 (Revit MEP 심화)
    → Personal Tutor Level 3 (조율 입문)
      → Coordinator Mentor (조율 전문)
        → Project Mentor (리드·자동화)
```

---

## 관련 문서

- 내부 MEP BIM 커리큘럼: `../mep_bim_ai/00_CURRICULUM_INDEX.md`
- 레슨 품질 기준: `../../starter_plan_lesson_quality_standard.md`
- 상품 포지셔닝: `../../personal_mep_bim_tutor_positioning.md`
- 가격 정책: `../../personal_mep_bim_tutor_pricing_payment.md`
