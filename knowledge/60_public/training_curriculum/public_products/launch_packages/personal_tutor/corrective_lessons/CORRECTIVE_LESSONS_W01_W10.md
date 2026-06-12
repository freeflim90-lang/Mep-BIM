# Personal Tutor — Corrective Lesson Library (W01–W10)

**Service:** LUA BIM LABS Personal Tutor  
**Purpose:** Immediate corrective micro-lessons sent when a weakness pattern is detected  
**Trigger:** 2+ instances of the same error pattern within one week (see DELIVERY_SOP.md Section 4.4)  
**Delivery:** Sent as a separate Telegram message labeled "📌 보충 레슨 (Corrective Lesson)"  
**Format:** Focused, practical, under 5 minutes to read  
**Version:** 1.0

---

## How to Send a Corrective Lesson

Header to use when sending:
```
📌 보충 레슨 — [W-Code]: [Lesson Title]

학습 중 반복적으로 확인된 부분을 집중적으로 정리해드립니다.
아래를 읽고 오늘 바로 연습 과제를 시도해 보세요!
```

---

### W01 — Level Offset Numeric Entry Errors: 오프셋 수치 입력 정확하게 하기

DETECTED PATTERN:
배관, 덕트, 케이블 트레이 등 MEP 요소를 배치할 때 오프셋(높이 값)을 잘못 입력하거나, 밀리미터와 미터 단위를 혼동하거나, 소수점 위치를 틀리는 오류가 반복됩니다. 예: 2400mm를 입력해야 하는데 2.4 또는 24000으로 입력.

WHY IT HAPPENS:
Revit의 오프셋 입력 단위가 프로젝트 단위 설정에 따라 달라지는데, 단위를 확인하지 않고 습관적으로 숫자를 입력하기 때문입니다. 또한 Revit이 일부 경우 자동 단위 변환을 적용하여 의도와 다른 값이 입력되는 것을 사용자가 알아차리지 못하기 때문입니다.

THE FIX:
**Step 1. 프로젝트 단위 확인**
- 상단 메뉴: Manage 탭 → Settings 패널 → Project Units 클릭
- Length 항목의 단위 확인 (mm 또는 m 중 어느 쪽인지)
- 이 설정에 따라 오프셋 입력값의 단위가 결정됨

**Step 2. 오프셋 입력 시 단위 직접 명시**
- Revit에서 값을 입력할 때 숫자 뒤에 단위를 명시하면 자동 변환됨
- 예: 프로젝트가 m 단위여도 "2400mm" 또는 "2.4m"로 입력하면 자동 변환
- 숫자만 입력하면 현재 프로젝트 단위로 처리됨

**Step 3. 입력 후 Properties 패널에서 반드시 확인**
- 요소 배치 후 선택하여 Properties 패널의 Elevation / Offset 값을 다시 읽음
- 의도한 값과 일치하는지 두 번 확인
- 특히 소수점이 있는 경우 (1.2m = 1200mm인지 12m = 12000mm인지) 반드시 확인

**Step 4. 단면 뷰에서 시각적 검증**
- 오프셋 입력 후 해당 요소가 포함된 단면 뷰(Section View)를 열어 실제 높이를 시각적으로 확인
- 인접 요소 (보, 슬래브, 다른 MEP 요소)와의 상대적 위치를 눈으로 검증

PRACTICE:
현재 작업 중인 Revit 모델에서 배관 또는 덕트 요소 하나를 선택하고, Properties 패널에서 Offset 값을 확인하세요. 그 후 단면 뷰를 만들어 해당 요소의 실제 높이가 Properties 값과 일치하는지 확인하세요. 일치하면 Pass, 다르면 프로젝트 단위 설정을 확인하고 다시 입력하세요.

CHECK:
- Manage → Project Units에서 프로젝트 길이 단위가 설계팀 표준과 동일한지 확인
- 주요 MEP 요소 3개를 선택하여 오프셋 값이 설계 도면의 의도한 높이와 일치하는지 단면 뷰로 검증

---

### W02 — MEP System Connection Not Completed (Open Connectors): 열린 커넥터 완전 해결하기

DETECTED PATTERN:
Revit 모델에서 MEP 요소(덕트, 배관, 전선관, 케이블 트레이)의 커넥터가 시스템에 연결되지 않아 열린 상태(Open Connector)로 남아 있습니다. Revit 경고창에 "Connector is not connected" 메시지가 다수 누적되어 있습니다.

WHY IT HAPPENS:
요소를 배치했지만 커넥터를 실제로 연결하는 마지막 단계를 빠뜨리기 때문입니다. Revit에서는 요소를 시각적으로 가깝게 배치해도 자동으로 연결되지 않으며, 반드시 커넥터를 명시적으로 연결해야 합니다. 또한 모델링 중 경로를 수정하면서 기존 연결이 끊어지는 경우도 있습니다.

THE FIX:
**Step 1. 열린 커넥터 전체 확인**
- 상단 메뉴: Manage 탭 → Review Warnings 또는 Check 탭에서 MEP Checks → Open Connectors 실행
- 또는: View 탭 → Window → Warnings 패널에서 Open Connector 관련 경고 필터링
- 열린 커넥터가 있는 요소 목록이 표시됨

**Step 2. 시스템 브라우저로 확인**
- View 탭 → User Interface → System Browser 활성화
- 시스템 브라우저에서 각 MEP 시스템(예: Supply Air, Chilled Water Return)을 클릭
- 해당 시스템에 속하지 않은 요소(Unassigned) 항목 확인

**Step 3. 커넥터 연결 방법**
- 방법 A (직접 연결): 덕트 또는 배관의 열린 끝단(파란색 화살표 표시)에 커서를 올리고 요소를 클릭하면 연결 가능
- 방법 B (Create System): 연결할 요소들을 모두 선택 후 Modify 탭 → Create Systems → 적절한 System Type 선택
- 방법 C (Draw Connection): 배관/덕트 도구를 사용하여 두 요소 간 연결 세그먼트 추가

**Step 4. 연결 완료 후 검증**
- System Browser에서 연결된 요소가 올바른 시스템 아래에 표시되는지 확인
- 경고창에서 Open Connector 경고가 사라졌는지 확인
- 연결된 배관/덕트를 선택하여 System Name 파라미터가 올바르게 채워져 있는지 확인

PRACTICE:
현재 모델에서 Manage → Review Warnings를 실행하여 Open Connector 경고 수를 기록하세요. 경고를 하나씩 클릭하여 해당 요소를 모델에서 찾아 연결하세요. 모든 Open Connector 경고가 사라질 때까지 반복하고, 최종 경고 수를 0으로 만든 스크린샷을 캡처하세요.

CHECK:
- Review Warnings에서 Open Connector 관련 경고 수 = 0 확인
- System Browser에서 Unassigned 카테고리에 요소가 없는지 확인

---

### W03 — Supply/Return System Confusion in HVAC: 공급-환기 시스템 혼동 바로잡기

DETECTED PATTERN:
HVAC 모델에서 공급(Supply) 덕트와 환기(Return) 덕트가 잘못된 시스템 타입에 할당되어 있습니다. 예: 공급 디퓨저가 Return Air 시스템에 연결되거나, Supply Air 덕트와 Return Air 덕트가 동일한 시스템에 묶여 있습니다.

WHY IT HAPPENS:
공급과 환기 덕트는 외관이 유사하여 모델링 중 시스템 타입 설정을 혼동하기 쉽습니다. 또한 AHU 주변 덕트를 배치할 때 공급 측과 환기 측을 잘못 연결하는 경우가 있으며, 시스템 타입 선택 창에서 빠르게 클릭하다 잘못 선택하기도 합니다.

THE FIX:
**Step 1. 공급/환기 시스템 구분 기준 이해**
- 공급(Supply Air): AHU → 덕트 → 디퓨저 → 실내 공간 (차가운 공기 공급)
- 환기(Return Air): 실내 공간 → 그릴(Return Grille) → 덕트 → AHU (실내 공기 회수)
- 외기(Outside Air): 외기 댐퍼 → AHU (신선 외기 도입)

**Step 2. Revit에서 시스템 타입 확인 방법**
- 덕트 또는 덕트 피팅을 선택
- Properties 패널에서 System Type 파라미터 확인
- System Name 파라미터에 올바른 이름(예: Supply Air 1, Return Air 1)이 있는지 확인

**Step 3. 잘못 할당된 시스템 수정**
- 잘못된 시스템에 속한 덕트/피팅 선택
- Properties → System Type 드롭다운에서 올바른 시스템 타입 선택
- 또는 선택 후 Modify → MEP Settings에서 시스템 편집

**Step 4. 색상 코딩으로 시각적 검증**
- 공급 덕트는 파란색, 환기 덕트는 빨간색(또는 다른 색)으로 뷰 필터 설정
- Visibility/Graphics (VG) → Filters 탭 → 시스템 타입별 색상 필터 추가
- 평면도에서 덕트 색상을 보고 공급/환기 구분이 시각적으로 명확한지 확인

**Step 5. AHU 연결부에서 출발하여 경로 추적**
- AHU의 공급 커넥터에서 시작하는 덕트 경로를 따라가며 모든 요소가 Supply Air로 연결되는지 확인
- AHU의 환기 커넥터에서 시작하는 경로도 동일하게 Return Air로 연결되는지 확인

PRACTICE:
현재 HVAC 모델에서 AHU 하나를 선택하고 System Browser를 열어 해당 AHU에 연결된 공급 및 환기 시스템의 요소 목록을 확인하세요. 각 시스템에 속한 디퓨저와 그릴이 올바른 유형(Supply Diffuser → Supply Air, Return Grille → Return Air)인지 검증하세요.

CHECK:
- System Browser에서 Supply Air 시스템에 Return Grille이 포함되지 않았는지 확인
- System Browser에서 Return Air 시스템에 Supply Diffuser가 포함되지 않았는지 확인
- 뷰 필터 색상 설정 후 공급/환기 경로가 시각적으로 명확하게 구분되는지 확인

---

### W04 — Drainage Pipes Modeled Flat (Zero Slope): 배수관 경사 올바르게 설정하기

DETECTED PATTERN:
위생 배수 배관이 경사 없이 수평(Slope = 0%)으로 모델링되어 있습니다. Revit Properties 패널의 Slope 파라미터가 0 또는 빈 칸으로 남아 있으며, 배관 양 끝단의 오프셋 값이 동일합니다.

WHY IT HAPPENS:
배수 배관을 배치할 때 Revit 기본 설정이 수평(Slope = 0)이므로, 경사를 별도로 설정하지 않으면 자동으로 평탄하게 배치됩니다. 배관 도구를 실행할 때 옵션 바의 Slope 옵션을 보지 않고 바로 클릭하는 습관 때문에 발생합니다.

THE FIX:
**Step 1. 설계 기준 경사값 확인**
- 국내 기준: 배수 배관 최소 경사 — 100A 이하: 1/50(2%), 125A–200A: 1/100(1%), 250A 이상: 1/200(0.5%)
- 설계 도면 또는 프로젝트 시방서에서 적용 기준 확인

**Step 2. 배관 배치 시 경사 사전 설정 (새 배관 작성 시)**
- Systems 탭 → Plumbing & Piping 패널 → Pipe 도구 실행
- 상단 옵션 바에서 "Slope" 드롭다운 클릭
- "Slope Down" 또는 "Slope Up" 선택 후 경사값 입력 (예: 1/100 또는 1.0%)
- 이후 배치되는 배관에 경사가 자동 적용됨

**Step 3. 기존 평탄 배관 수정**
- 수정할 배관 세그먼트 선택
- Properties 패널에서 Slope 파라미터 클릭
- 설계 기준 경사값 입력 (예: 1.0000% 또는 0.01m/m)
- Enter 후 Revit이 한쪽 끝의 오프셋을 자동 조정함
- 조정된 끝단 오프셋 값이 물리적으로 허용 가능한 범위인지 확인

**Step 4. 경사 설정 후 연결부 확인**
- 경사 적용 후 연결된 위생기구(세면대, 변기 등)의 배수 커넥터 높이와 배관 끝단 높이가 일치하는지 확인
- 불일치 시 피팅(Elbow, Junction)으로 높이 차이 처리

**Step 5. Revit 스케줄로 경사 일괄 검증**
- View 탭 → Schedules → Schedule/Quantities → Pipes 카테고리 선택
- Slope 파라미터를 스케줄 열에 추가
- 경사값이 0인 배관 행을 필터링하여 수정 대상 목록 생성

PRACTICE:
배수 배관 스케줄을 만들고 Slope 열을 추가하세요. 경사값이 0%인 배관을 모두 찾아 올바른 경사값으로 수정하고, 수정 후 스케줄에서 0% 항목이 없어졌는지 확인하세요.

CHECK:
- Pipe Schedule의 Slope 열에서 경사 0% 배관이 없는지 확인
- 경사 수정 후 배관 끝단(스택 연결부)의 오프셋이 설계 의도와 맞는지 단면 뷰로 확인

---

### W05 — Naming Convention Inconsistency: 명명 규칙 일관성 확보하기

DETECTED PATTERN:
뷰 이름, 패밀리 이름, 시스템 이름, 파라미터 값 등에서 명명 규칙이 일관되지 않습니다. 예: "Supply Air 1", "supply_air_1", "공급공기1", "SA-01"이 같은 프로젝트 내에 혼재. 또는 뷰 이름에 날짜 및 작성자 이니셜이 임의로 포함.

WHY IT HAPPENS:
프로젝트 표준 명명 규칙을 명확히 이해하지 못한 상태에서 작업을 시작했거나, 여러 사람이 작업한 파일에서 각자 다른 방식을 사용했기 때문입니다. 또한 Revit이 일부 항목에서 기본 이름을 자동 생성하는데, 이를 수정하지 않고 그대로 사용하는 경우도 있습니다.

THE FIX:
**Step 1. 프로젝트 명명 규칙 문서 확인**
- 프로젝트 BEP 또는 BIM 표준의 명명 규칙 섹션 확인
- 없다면 LUA BIM LABS 기본 명명 규칙 적용:
  - **뷰 이름:** `[층번호]_[분야코드]_[뷰유형]_[스케일]` 예: `FL04_ME_PLAN_1:100`
  - **시스템 이름:** `[분야코드]-[시스템타입]-[번호]` 예: `ME-SA-01` (기계-공급공기-01)
  - **패밀리 이름:** 제조사 이름 제외, 기능+크기+유형 예: `Pipe_Elbow_90deg_50A`

**Step 2. 기존 불일치 항목 일괄 수정**
- **뷰 이름:** View 탭 → Views (All) 뷰 목록에서 이름 확인 및 수정 (뷰 이름 더블클릭)
- **시스템 이름:** MEP Checks 또는 System Browser에서 시스템 이름 확인 및 수정
- **파라미터 값:** Revit 스케줄에서 해당 파라미터 열을 정렬하여 불일치 값 찾아 일괄 수정

**Step 3. 명명 규칙 참조 문서를 Revit 내에 보관**
- Drafting View를 만들어 프로젝트 명명 규칙 테이블을 텍스트로 입력
- 팀원 모두가 같은 파일 내에서 언제든지 확인 가능하게 함

**Step 4. 신규 요소 작성 시 즉시 명명 규칙 적용**
- 요소 배치 직후 이름 입력 단계에서 규칙에 따른 이름을 즉시 입력하는 습관 형성
- "나중에 바꾸겠다"는 접근은 항상 누락으로 이어짐

PRACTICE:
현재 모델에서 뷰 목록(Views All)을 열고 명명 규칙에 맞지 않는 뷰를 3개 이상 찾아 올바른 이름으로 수정하세요. 수정 전후 이름을 기록하고 다음 레슨 때 공유해 주세요.

CHECK:
- Views All 목록에서 임의 번호나 "Copy of" 접두어가 포함된 뷰 이름이 없는지 확인
- System Browser에서 "Undefined" 또는 "System 1" 같은 기본 시스템 이름이 없는지 확인

---

### W06 — Linked Model Shared Coordinate Mismatch: 링크 모델 공유 좌표 불일치 해결하기

DETECTED PATTERN:
다른 분야 Revit 링크 모델(건축, 구조 등)을 현재 MEP 모델에 링크했을 때 요소들이 잘못된 위치에 표시됩니다. 건축 모델의 벽이 MEP 모델의 기존 요소들과 수십 미터 떨어진 위치에 나타나거나, 완전히 다른 높이로 표시됩니다.

WHY IT HAPPENS:
각 Revit 파일은 자체 원점(Internal Origin)을 가지고 있습니다. 프로젝트 공유 좌표(Shared Coordinates)가 설정되지 않았거나 서로 다른 기준점을 사용하면 링크 시 요소가 의도하지 않은 위치에 나타납니다. 이는 대형 현장 좌표를 사용하는 프로젝트에서 특히 자주 발생합니다.

THE FIX:
**Step 1. 링크 방식 확인**
- Revit에서 링크를 삽입할 때 Import/Link RVT 대화상자에서 "Positioning" 옵션 확인
- 옵션들: Auto - Origin to Origin / Auto - Center to Center / Manual - Origin / Shared Coordinates
- 올바른 옵션: **Shared Coordinates** (프로젝트 공유 좌표가 설정된 경우) 또는 **Auto - Origin to Origin** (공유 좌표 미설정 시)

**Step 2. 공유 좌표 상태 확인**
- Manage 탭 → Coordinates 패널 → Coordinates 또는 Publish Coordinates 기능 확인
- 링크된 모델을 선택하고 Properties에서 "Shared Location" 파라미터 확인

**Step 3. 위치 오류 수정 방법**
- 방법 A: 링크를 제거(Unlink)하고 "Shared Coordinates" 옵션으로 다시 링크
- 방법 B: 링크 파일을 선택 후 Manage Links → Reload 또는 위치 재설정
- 방법 C: Manage → Coordinates → Acquire Coordinates (호스트 파일에서 좌표 취득)로 두 파일의 공유 좌표 동기화

**Step 4. 시각적 검증**
- 링크 후 건축 모델의 벽이 MEP 모델의 공간과 정확히 일치하는지 평면도와 단면도에서 확인
- 슬래브 레벨이 MEP 모델의 레벨과 동일한지 Elevation 뷰에서 비교

**Step 5. 팀 전체 공유 좌표 프로세스 확립**
- 프로젝트 시작 시 건축 팀이 공유 좌표를 설정하고 모든 분야에 배포
- 각 분야는 동일한 공유 좌표 기반으로 파일 작성
- 이 과정이 BEP에 명시되어야 함

PRACTICE:
현재 프로젝트에서 링크 모델을 선택하고 Manage Links 창을 열어 링크 상태를 확인하세요. Positioning 방식을 확인하고, 건축 모델의 특정 벽이 MEP 모델과 올바른 위치에 있는지 단면 뷰로 검증하세요.

CHECK:
- 링크 모델 삽입 시 Positioning 옵션이 프로젝트 표준에 맞게 설정되어 있는지 확인
- 건축 링크 모델의 슬래브 레벨이 MEP 모델의 레벨 높이와 일치하는지 Elevation 뷰로 확인

---

### W07 — LOD Under-Specification (LOD 200 Submitted for LOD 350 Requirement): LOD 기준 정확히 적용하기

DETECTED PATTERN:
납품 요건은 LOD 350이지만 제출된 BIM 모델이 LOD 200 수준입니다. 요소의 크기가 개략적이거나, 연결 피팅이 생략되어 있거나, 지지대(Hanger)가 없거나, 파라미터 정보가 부족합니다.

WHY IT HAPPENS:
LOD의 각 단계가 무엇을 요구하는지 명확히 이해하지 못한 상태에서 "3D로 보이면 충분하다"고 판단하기 때문입니다. LOD는 형상 정확도뿐만 아니라 정보(파라미터) 완성도와 연결 상세도를 포함하는 개념인데, 이를 형상만으로 이해하는 오해가 있습니다.

THE FIX:
**Step 1. LOD 기준 명확히 이해**
- **LOD 100:** 아이콘 또는 기호 수준 — 형태 없음
- **LOD 200:** 개략적 크기와 위치 — 계획 단계 (덕트 크기 근사값)
- **LOD 300:** 정확한 크기, 위치, 형상 — 설계 완료 단계
- **LOD 350:** 연결 상세, 지지 구조, 시공 가능한 치수 포함 — 시공 도면 단계
- **LOD 400:** 제조사 실제 형상과 동일한 수준 — 제작 단계

**Step 2. LOD 350 요건 체크리스트 (MEP 기준)**
- [ ] 모든 덕트/배관 크기가 설계 치수와 정확히 일치
- [ ] 모든 피팅(엘보, 티, 리듀서) 실제 형상으로 배치됨
- [ ] 플렉시블 연결재 배치됨
- [ ] 행거/지지대 위치 및 형상 표현됨
- [ ] 단열재 두께 파라미터 입력됨
- [ ] 필수 파라미터(시스템 이름, LOD, 크기) 모두 입력됨
- [ ] 커넥터 연결 완료 (Open Connector = 0)

**Step 3. 현재 모델과 체크리스트 대조**
- 위 체크리스트의 각 항목을 현재 모델에서 확인
- 미달 항목 목록 작성

**Step 4. 미달 항목 보완**
- 피팅 형상: Revit에서 Fitting Preference 또는 실제 크기 피팅 패밀리 로드
- 행거 표현: 행거 패밀리를 지정 간격으로 배치 (일반적으로 1.5–2.0m 간격)
- 단열재: 파이프 단열재(Pipe Insulation) 또는 덕트 단열재 레이어 추가
- 파라미터: Revit 스케줄을 통해 미입력 파라미터 일괄 확인 및 입력

PRACTICE:
현재 모델에서 배관 또는 덕트 구간 하나를 선택하고 위의 LOD 350 체크리스트와 대조하세요. 부족한 항목을 기록하고 그 중 하나를 직접 보완한 후 스크린샷을 남기세요.

CHECK:
- BEP의 LOD 요건 섹션을 다시 읽고 납품 요건이 LOD 350인지 다른 수준인지 재확인
- 위 LOD 350 체크리스트의 7개 항목 중 미달 항목 수를 기록하여 개선 목표 설정

---

### W08 — Required Parameters Not Populated: 필수 파라미터 누락 없이 입력하기

DETECTED PATTERN:
BIM 모델에서 발주처 또는 프로젝트 BEP가 요구하는 필수 파라미터(예: System Classification, Insulation Thickness, Installation Phase, Specification Reference 등)가 입력되지 않거나 기본값(0, None, 빈 칸)으로 남아 있습니다.

WHY IT HAPPENS:
어떤 파라미터가 필수인지 정확히 파악하지 못한 채 모델링을 진행하거나, 나중에 입력하려고 미루다 누락하는 경우가 많습니다. 또한 팀 내에서 파라미터 입력이 특정 담당자의 역할로 명확히 정해지지 않아 "누군가 하겠지"로 넘어가기도 합니다.

THE FIX:
**Step 1. 필수 파라미터 목록 확보**
- 프로젝트 BEP → 정보 요건(Information Requirements) 섹션 확인
- 발주처 EIR(Employer's Information Requirements) 문서 확인
- 없으면 LUA BIM LABS 기본 필수 파라미터 목록 적용:
  - 공통: Mark, Comments, Phase Created
  - MEP 공통: System Name, System Type, Specification Reference
  - 배관 추가: Pipe Size(mm), Pipe Material, Insulation Type, Insulation Thickness
  - 덕트 추가: Duct Width, Duct Height, Insulation Type, Insulation Thickness
  - 장비 추가: Equipment Mark, Model Number, Manufacturer, Capacity

**Step 2. 스케줄로 미입력 파라미터 파악**
- View → Schedules → Schedule/Quantities → 해당 카테고리(예: Pipes) 선택
- 필수 파라미터를 스케줄 열로 추가
- 빈 칸이나 기본값으로 남은 행 확인
- 스케줄에서 직접 값을 입력하거나 수정 가능 (해당 셀 클릭 → 값 입력)

**Step 3. 일괄 입력 방법**
- 동일 파라미터 값을 여러 요소에 적용해야 할 때: 여러 요소 선택(Ctrl+클릭 또는 필터 선택) → Properties 패널에서 파라미터 값 입력 → 선택된 모든 요소에 동시 적용

**Step 4. 파라미터 입력 프로세스에 통합**
- 각 요소 배치 직후 Properties 패널을 확인하여 필수 파라미터 즉시 입력
- 일일 작업 마감 전 5분 동안 당일 배치한 요소들의 스케줄을 확인하여 누락된 파라미터 보완

PRACTICE:
배관(Pipe) 스케줄을 만들고 System Name, Pipe Size, Insulation Type, Insulation Thickness 열을 추가하세요. 빈 칸이 있는 행을 모두 찾아 값을 입력하고, 스케줄에 빈 칸이 없어질 때까지 완성하세요.

CHECK:
- 필수 파라미터 스케줄에서 빈 칸(Null) 또는 기본값(0, None)이 없는지 확인
- 스케줄 데이터를 CSV로 내보내 발주처 요건과 항목별 대조

---

### W09 — View Discipline Filter Set Incorrectly: 뷰 분야 필터 올바르게 설정하기

DETECTED PATTERN:
기계 분야(Mechanical) 뷰에서 전기 또는 구조 요소가 불필요하게 표시되거나, 반대로 표시되어야 할 MEP 요소가 뷰에서 사라져 있습니다. 뷰 Discipline 설정이 잘못되어 있거나, Visibility/Graphics 필터가 의도와 다르게 설정된 경우입니다.

WHY IT HAPPENS:
Revit의 뷰 Discipline 설정(Mechanical, Electrical, Plumbing, Coordination)이 무엇을 표시/숨기는지 정확히 이해하지 못하고 있거나, View Template이 잘못 적용되어 있거나, 동료가 수정한 뷰 필터가 덮어씌워진 경우입니다.

THE FIX:
**Step 1. 뷰 Discipline 설정 확인**
- 문제 뷰 선택 (선택하지 말고 해당 뷰로 이동)
- Properties 패널 → View Properties 섹션 → Discipline 파라미터 확인
- 옵션: Architectural / Structural / Mechanical / Electrical / Plumbing / Coordination
- MEP 분야별 적용 원칙:
  - **Mechanical:** 기계(HVAC, 배관) 요소 우선 표시, 전기 요소 기본 숨김
  - **Electrical:** 전기 요소 우선 표시, 기계 요소 기본 숨김
  - **Plumbing:** 위생 배관 우선 표시
  - **Coordination:** 모든 분야 동시 표시 (클래시 검토용)

**Step 2. Visibility/Graphics (VG) 설정 확인**
- 단축키 VG 또는 Manage → Visibility/Graphics 실행
- Model Categories 탭에서 각 카테고리의 표시 여부 확인
- Filters 탭에서 현재 뷰에 적용된 필터 목록 확인
- 불필요한 필터 제거, 필요한 필터 추가

**Step 3. View Template 확인**
- Properties 패널 → View Template 파라미터 확인
- View Template이 적용되어 있으면 VG 설정이 자동으로 제어됨
- 잘못된 View Template이 적용된 경우: View Template → None으로 변경 후 수동 설정 또는 올바른 Template 선택

**Step 4. 올바른 뷰 설정 저장**
- 뷰 설정 완료 후 View Template으로 저장하여 재사용
- View 탭 → View Templates → Create Template from Current View
- 팀 전체가 동일한 View Template 사용하도록 공유

**Step 5. 링크 모델 가시성 확인**
- VG → Revit Links 탭에서 링크된 모델의 카테고리별 표시 설정 확인
- 건축 링크 모델을 기계 뷰에서 반투명 또는 특정 카테고리만 표시하도록 설정

PRACTICE:
현재 작업 중인 기계 분야 평면도 뷰를 열고 Properties에서 Discipline 파라미터를 확인하세요. Mechanical로 설정된 경우 전기 카테고리가 숨겨져 있는지 VG에서 확인하고, 뷰 목적에 맞게 카테고리 표시 설정을 조정한 후 View Template으로 저장하세요.

CHECK:
- 기계 뷰에서 불필요한 전기/구조 요소가 표시되지 않는지 확인
- 현재 뷰에 적용된 View Template 이름이 올바른지 Properties 패널에서 확인

---

### W10 — Revit Warnings Accumulated and Ignored: Revit 경고 관리하고 해결하기

DETECTED PATTERN:
Revit 모델에 경고(Warning)가 수십 개에서 수백 개 누적되어 있으며, 이를 확인하거나 해결하지 않고 작업을 계속하고 있습니다. "경고는 에러가 아니니까 괜찮다"는 인식이 있습니다.

WHY IT HAPPENS:
Revit 경고가 작업을 중단시키지 않기 때문에 무시하기 쉽습니다. 또한 경고 메시지가 기술적 언어로 되어 있어 의미를 파악하기 어려워 그냥 닫는 습관이 생기기 때문입니다. 경고 누적이 모델 성능 저하와 데이터 오류의 원인임을 인식하지 못하는 경우가 많습니다.

THE FIX:
**Step 1. 현재 경고 수 확인**
- Manage 탭 → Inquiry 패널 → Review Warnings 클릭
- 경고 목록이 표시됨 — 총 경고 수와 유형 확인
- 경고를 클릭하면 해당 요소가 모델에서 선택됨

**Step 2. 경고 유형별 우선순위 분류**

높은 우선순위 (즉시 해결):
- "Elements have duplicate identical instances" — 요소 중복 배치
- "There are identical instances in the same place" — 동일 위치 중복
- "Connector is not connected" — 열린 커넥터 (W02 참조)
- "One or more elements are not in a loop" — 시스템 루프 미완성

중간 우선순위 (이번 주 내 해결):
- "Room is not in a properly enclosed region" — 공간 경계 미완성
- "The highlighted pipes/ducts are joined but not at matching elevations" — 비매칭 높이 연결
- "Level is below the base of the building" — 레벨 설정 문제

낮은 우선순위 (월말 정리):
- "Highlighted walls are attached to, but miss..." — 일부 건축 관련 경고
- 뷰 관련 경고 (표시 문제, 실제 모델 오류 아님)

**Step 3. 중복 요소 경고 해결**
- "Elements have duplicate identical instances" 경고 클릭
- 중복된 요소가 선택됨 → 하나를 삭제

**Step 4. 비매칭 높이 연결 경고 해결**
- 연결부의 오프셋 값 확인
- 두 요소의 높이를 일치시키거나 적절한 피팅(Elbow 등)으로 연결

**Step 5. 경고 정기 관리 루틴**
- 매주 금요일 Review Warnings 실행
- 새로 발생한 경고와 기존 경고 구분
- 목표: 납품 전 Critical 경고 = 0, 전체 경고 최소화

PRACTICE:
지금 바로 Manage → Review Warnings를 실행하고 현재 경고 수를 기록하세요. 경고를 우선순위별로 분류하고, 높은 우선순위 경고를 최소 3개 해결하세요. 해결 전후 경고 수를 기록하고 결과를 공유해 주세요.

CHECK:
- Review Warnings에서 "Identical instances"(중복 요소) 경고가 없는지 확인
- "Connector not connected"(열린 커넥터) 경고가 없는지 확인
- 총 경고 수가 이전 주 대비 감소했는지 확인

---

*End of Corrective Lessons W01–W10 v1.0*
*W11–W30 to be developed in subsequent releases.*
