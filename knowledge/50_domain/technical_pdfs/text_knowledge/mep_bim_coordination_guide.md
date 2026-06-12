# MEP BIM 조율 실무 기준 문서
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
