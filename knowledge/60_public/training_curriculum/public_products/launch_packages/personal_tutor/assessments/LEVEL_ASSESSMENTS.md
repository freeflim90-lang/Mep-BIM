# Personal Tutor — Level Assessments (L1–L5)

**Service:** LUA BIM LABS Personal Tutor  
**Purpose:** (1) Intake level diagnosis, (2) Monthly level check  
**Format:** 10 questions per level — mix of multiple choice and short answer  
**Scoring:** 1 point per correct answer (10 points total per test)  
**Document Owner:** COO  
**Confidentiality:** FOR LUA BIM LABS USE ONLY — Do not share answer keys with clients

---

## How to Administer

1. Send questions only (not the answer key) to the client via Telegram
2. Number each question 1–10; ask the client to reply with their answers (e.g., "1-A, 2-C, 3-..." or short text for SA items)
3. Score using the answer key in this document
4. Record score and identified weak areas in client's `WEAKNESS_LOG.md`

---

# LEVEL 1 ASSESSMENT — Beginner

**Topics:** BIM concepts, MEP systems overview, Revit interface basics

---

**[Send to client — questions only, no answer labels]**

**Level 1 수준 진단 테스트**
아래 10문항에 답해 주세요. 객관식은 정답을 하나 선택하고, 주관식은 짧게 서술해 주세요.

---

**Q1 (Multiple Choice)**
BIM(Building Information Modeling)이란 무엇인가요?

A) 건물의 2D 도면을 디지털로 보관하는 방법  
B) 건물의 3D 형상과 데이터 정보를 통합한 디지털 모델  
C) 건물 공사 일정을 관리하는 소프트웨어  
D) 건물 구조 계산을 자동화하는 시스템

**ANSWER:** B  
**EXPLANATION:** BIM은 형상(3D)과 데이터(파라미터, 속성)를 통합한 디지털 모델로, 단순 3D 시각화를 넘어 설계·시공·운영 전 단계에서 정보를 공유하는 방법론이다.

---

**Q2 (Multiple Choice)**
Revit에서 MEP(기계·전기·배관) 모델링에 사용되는 기본 카테고리가 아닌 것은?

A) 덕트 (Duct)  
B) 배관 (Pipe)  
C) 케이블 트레이 (Cable Tray)  
D) 구조 기둥 (Structural Column)

**ANSWER:** D  
**EXPLANATION:** 구조 기둥은 구조(Structural) 분야 카테고리이다. 덕트, 배관, 케이블 트레이는 모두 MEP 카테고리에 속한다.

---

**Q3 (Multiple Choice)**
MEP에서 "HVAC"의 올바른 풀이는?

A) High Voltage AC Circuit  
B) Heating, Ventilation, and Air Conditioning  
C) Heavy Vent and Cooling  
D) Horizontal Vertical Axis Control

**ANSWER:** B  
**EXPLANATION:** HVAC는 Heating(난방), Ventilation(환기), Air Conditioning(냉방)의 약자로, 건물 공조 시스템 전반을 의미한다.

---

**Q4 (Multiple Choice)**
Revit에서 새 프로젝트를 시작할 때 가장 먼저 확인해야 할 설정은?

A) 재질 색상  
B) 프로젝트 단위 (Units)  
C) 그래픽 카드 성능  
D) 인쇄 설정

**ANSWER:** B  
**EXPLANATION:** 프로젝트 단위를 먼저 설정해야 모든 요소의 치수가 올바르게 기록된다. 단위 오류는 나중에 수정이 매우 어렵다.

---

**Q5 (Multiple Choice)**
Revit에서 "패밀리(Family)"란 무엇인가요?

A) 같은 회사 직원들이 공유하는 파일  
B) 재사용 가능한 BIM 요소의 템플릿 (예: 팬코일 유닛, 밸브)  
C) 프로젝트 단계를 나누는 분류 기준  
D) Revit 업데이트 버전명

**ANSWER:** B  
**EXPLANATION:** 패밀리는 Revit에서 반복 사용되는 요소를 정의하는 템플릿이다. MEP 분야에서는 기계 장비, 배관 피팅, 전기 패널 등이 패밀리로 제공된다.

---

**Q6 (Short Answer)**
소방 시스템(Fire Protection)에서 스프링클러 헤드를 연결하는 배관 시스템의 역할을 2문장 이내로 설명하세요.

**ANSWER (Model answer):** 스프링클러 배관 시스템은 화재 발생 시 가압수를 스프링클러 헤드로 공급하는 역할을 한다. 건물 내 화재 감지 신호에 반응하여 자동으로 작동해 화재를 초기에 억제한다.  
**SCORING:** Award 1 point if the client mentions (a) water supply and (b) fire suppression/automatic response. Partial credit not applicable — this is scored full/zero.

---

**Q7 (Multiple Choice)**
Revit에서 평면도(Floor Plan)와 천장 평면도(Reflected Ceiling Plan, RCP)의 주요 차이점은?

A) RCP는 3D 뷰이고 Floor Plan은 2D 뷰이다  
B) RCP는 위에서 내려다보는 반면 Floor Plan은 바닥에서 올려다본 투영이다  
C) RCP는 천장에 설치된 요소를 표현하는 뷰이고, Floor Plan은 바닥 레벨 요소를 중심으로 표현한다  
D) 차이가 없다 — 같은 뷰이다

**ANSWER:** C  
**EXPLANATION:** RCP는 천장 면에 설치되는 요소(조명, 디퓨저, 스프링클러 헤드 등)를 표현하는 데 사용되며, 전기 및 기계 분야에서 특히 중요하다.

---

**Q8 (Multiple Choice)**
MEP 코디네이션에서 "클래시(Clash)"란 무엇을 의미하나요?

A) 설계팀 간의 의사소통 문제  
B) 서로 다른 MEP 요소 또는 구조와 MEP 요소가 공간적으로 충돌하는 것  
C) 파일이 손상된 상태  
D) 렌더링 오류

**ANSWER:** B  
**EXPLANATION:** 클래시는 두 요소가 같은 공간을 점유할 때 발생하는 공간적 충돌이다. 예: 덕트가 보(Beam)를 관통하거나, 배관과 덕트가 교차하는 경우.

---

**Q9 (Short Answer)**
Revit의 "레벨(Level)"이란 무엇이며, MEP 모델링에서 왜 중요한지 설명하세요.

**ANSWER (Model answer):** 레벨은 건물의 각 층 높이를 정의하는 수평 기준 평면이다. MEP 모델링에서 각 요소는 레벨을 기준으로 높이가 결정되므로, 레벨 설정이 정확해야 모든 MEP 요소가 올바른 위치에 배치되고 층별 조정이 가능해진다.  
**SCORING:** Award 1 point for mentioning (a) horizontal reference plane for floors and (b) height reference for MEP elements.

---

**Q10 (Multiple Choice)**
전기 분야 BIM 모델에서 "케이블 트레이(Cable Tray)"의 주된 역할은?

A) 전기 케이블을 보호하고 정리된 경로로 배선하기 위한 지지 구조물  
B) 전기를 생산하는 장치  
C) 냉방 장비에 전원을 끊는 차단기  
D) 조명 패널의 다른 이름

**ANSWER:** A  
**EXPLANATION:** 케이블 트레이는 전력 케이블과 통신 케이블을 구조적으로 지지하고 정해진 경로로 배선하는 지지 구조물이다. BIM 모델에서는 케이블 트레이의 경로, 크기, 레이어 구분이 중요하다.

---

# LEVEL 2 ASSESSMENT — Modeler

**Topics:** Modeling accuracy, system connections, naming conventions, parameters

---

**Level 2 수준 진단 테스트**

---

**Q1 (Multiple Choice)**
Revit에서 덕트를 모델링할 때 "오프셋(Offset)" 값은 무엇을 기준으로 측정되나요?

A) 천장 레벨로부터의 거리  
B) 현재 뷰의 레벨(Level)로부터의 수직 거리  
C) 가장 가까운 기둥 중심으로부터의 수평 거리  
D) 이전에 배치한 요소로부터의 상대 거리

**ANSWER:** B  
**EXPLANATION:** Revit에서 오프셋 값은 현재 배치 기준 레벨로부터 요소 중심선(또는 하단, 상단)까지의 수직 거리다. 정확한 레벨 설정과 오프셋 입력이 조정 협업의 기본이 된다.

---

**Q2 (Multiple Choice)**
MEP 시스템 연결(System Connection)이 완료된 상태란?

A) 패밀리가 뷰에 표시되어 있는 상태  
B) 모든 커넥터(Connector)가 시스템에 할당되어 개방된 커넥터가 없는 상태  
C) 모델이 저장된 상태  
D) Navisworks에 내보내진 상태

**ANSWER:** B  
**EXPLANATION:** Revit에서 MEP 요소의 커넥터가 시스템에 연결되지 않으면 흐름 계산, 간섭 분석, 도면 태그가 정상 작동하지 않는다. 개방된 커넥터(Open Connector)는 항상 확인 및 처리해야 한다.

---

**Q3 (Short Answer)**
Revit에서 HVAC 덕트를 "공급(Supply)"과 "환기(Return)" 시스템으로 구분하는 방법을 설명하세요.

**ANSWER (Model answer):** 덕트를 배치하거나 선택한 후 Properties 패널 또는 Type Properties에서 System Type을 Supply Air 또는 Return Air로 지정한다. 시스템 분류는 덕트 색상, 흐름 방향, 계산에 영향을 미친다.  
**SCORING:** Award 1 point for mentioning System Type assignment and its consequence (color coding, flow direction, or calculation).

---

**Q4 (Multiple Choice)**
LOD(Level of Development) 200과 LOD 350의 주요 차이점은?

A) LOD 200은 3D이고 LOD 350은 2D이다  
B) LOD 200은 요소의 크기와 형태가 대략적이며, LOD 350은 연결부 상세와 시공 가능한 치수를 포함한다  
C) LOD 200은 구조 분야 전용이고 LOD 350은 MEP 전용이다  
D) LOD 숫자가 클수록 파일 크기가 작다

**ANSWER:** B  
**EXPLANATION:** LOD 200은 개략적 크기와 위치로 계획 단계에 적합하다. LOD 350은 실제 시공에 필요한 치수, 연결 위치, 지지 요소를 포함하여 조정 및 시공 단계에 사용된다.

---

**Q5 (Multiple Choice)**
Revit에서 배관 경사(Slope)를 설정하는 위치는?

A) View Properties  
B) Project Information  
C) Pipe의 Properties 패널 — Slope 파라미터  
D) Manage 탭 → Project Units

**ANSWER:** C  
**EXPLANATION:** 배관 선택 후 Properties 패널의 Slope 값에 경사도를 입력하거나, 배관 도구 실행 중 옵션 바에서 설정한다. 위생 배관의 드레인 경사는 반드시 설정해야 한다.

---

**Q6 (Multiple Choice)**
LUA BIM LABS 명명 규칙에서 Revit 뷰 이름의 기본 형식으로 적절한 것은?

A) 층번호_분야코드_뷰유형_스케일  
B) 작성자이니셜_날짜_층번호  
C) 임의 이름 — 일관성보다 가독성이 중요  
D) 분야코드만으로도 충분

**ANSWER:** A  
**EXPLANATION:** 일관된 명명 규칙은 다분야 팀에서 특정 뷰를 빠르게 찾고, 필터링하고, 공유하는 데 필수적이다. 층번호_분야코드_뷰유형_스케일 형식이 가장 일반적인 표준이다.

---

**Q7 (Short Answer)**
Revit에서 "공유 파라미터(Shared Parameter)"가 일반 프로젝트 파라미터와 다른 이유를 설명하세요.

**ANSWER (Model answer):** 공유 파라미터는 외부 .txt 파일에 정의되어 여러 프로젝트 및 패밀리에서 동일하게 사용할 수 있다. 일반 프로젝트 파라미터는 해당 프로젝트에만 존재하므로 스케줄에 표시되지 않는 경우가 있고 패밀리와 공유되지 않는다.  
**SCORING:** Award 1 point for mentioning (a) external definition file and (b) cross-project or cross-family reusability, or schedule availability.

---

**Q8 (Multiple Choice)**
Revit 워크셋(Workset)의 주된 목적은?

A) 파일을 여러 버전으로 저장하는 기능  
B) 팀원 여러 명이 동일한 중앙 파일을 동시에 편집할 수 있도록 모델을 분할하는 협업 기능  
C) 뷰를 카테고리별로 정리하는 기능  
D) 3D 렌더링 품질을 높이는 기능

**ANSWER:** B  
**EXPLANATION:** 워크셋은 Revit의 중앙 모델 협업 기능으로, 여러 사용자가 서로 다른 워크셋을 소유하여 동시 편집이 가능하다. 대형 프로젝트에서 팀 분업의 핵심이다.

---

**Q9 (Multiple Choice)**
덕트 또는 배관 경로에서 "유연한 연결(Flexible Connection)"을 사용해야 하는 경우는?

A) 두 층 사이를 연결할 때  
B) 기계 장비의 진동이 배관 또는 덕트로 전달되지 않도록 할 때  
C) 직선 덕트의 끝을 마감할 때  
D) 배관 크기를 변경할 때

**ANSWER:** B  
**EXPLANATION:** 유연한 연결재(Flexible Duct/Connector)는 진동 절연을 위해 AHU, 팬코일 유닛, 펌프 등 기계 장비 연결부에 설치한다. 누락 시 진동 소음 및 장비 손상이 발생할 수 있다.

---

**Q10 (Multiple Choice)**
Revit에서 스케줄(Schedule)을 만들 때 "공간 유형별 장비 수량"을 집계하려면 어떤 설정이 필요한가요?

A) 장비 패밀리에 "Room" 파라미터를 연결하고 스케줄에서 Grouping 적용  
B) 모든 장비를 하나의 그룹으로 묶은 후 내보내기  
C) 구조 분야 템플릿으로 전환 후 집계  
D) 스케줄로는 공간별 집계가 불가능하다

**ANSWER:** A  
**EXPLANATION:** 장비 패밀리에 Room 파라미터(또는 Space 파라미터)를 연결하면 스케줄에서 공간별 Grouping 및 Subtotal 기능으로 공간 유형별 수량 집계가 가능하다.

---

# LEVEL 3 ASSESSMENT — Coordinator

**Topics:** Clash types, coordination workflows, Navisworks basics, issue tracking

---

**Level 3 수준 진단 테스트**

---

**Q1 (Multiple Choice)**
Navisworks에서 "하드 클래시(Hard Clash)"와 "소프트 클래시(Soft Clash, Clearance Clash)"의 차이는?

A) 하드 클래시는 덕트 전용, 소프트 클래시는 배관 전용이다  
B) 하드 클래시는 두 요소가 실제로 겹치는 충돌이고, 소프트 클래시는 요소 간 최소 간격 기준이 확보되지 않은 충돌이다  
C) 하드 클래시는 구조 충돌만을 의미한다  
D) 소프트 클래시는 자동 해결이 가능하다

**ANSWER:** B  
**EXPLANATION:** 하드 클래시는 두 요소가 실제로 같은 공간을 점유한다. 소프트 클래시(Clearance Clash)는 설정한 최소 간격(예: 덕트와 배관 사이 100mm)이 확보되지 않아 발생하는 잠재적 문제다.

---

**Q2 (Multiple Choice)**
MEP 코디네이션 워크플로에서 "CSD(Coordinated Service Drawing)"의 역할은?

A) 설계 초안을 보관하는 문서  
B) 다분야(구조, 기계, 전기) 코디네이션이 완료된 MEP 시스템 경로를 보여주는 최종 조정 도면  
C) 발주처 검토 전에 사용하는 내부 참고 도면  
D) Revit 내보내기 형식의 이름

**ANSWER:** B  
**EXPLANATION:** CSD는 다분야 조정이 완료된 후 작성되는 통합 서비스 도면으로, 시공팀이 현장에서 MEP 배관 경로를 따라 시공하기 위한 기준 도면이다.

---

**Q3 (Short Answer)**
Navisworks에서 클래시 감지를 실행한 후 클래시를 해결하는 일반적인 3단계 프로세스를 설명하세요.

**ANSWER (Model answer):** (1) 클래시 보고서를 확인하여 충돌 요소와 위치를 파악한다. (2) Revit(또는 해당 분야 소프트웨어)에서 해당 요소의 경로나 위치를 수정한다. (3) 수정된 모델을 Navisworks에 다시 가져와 재검토(Re-run)하여 클래시가 해결되었는지 확인한다.  
**SCORING:** Award 1 point for mentioning all three steps: identify → fix in authoring tool → re-check.

---

**Q4 (Multiple Choice)**
MEP 코디네이션에서 "수직 우선순위(Vertical Priority)"란?

A) 파이프가 덕트보다 항상 위에 위치해야 한다는 규정  
B) 충돌 시 경로 변경을 덕트, 배관, 전선관 순으로 유연하게 조정하는 우선순위 기준  
C) 수직 방향 요소(기둥, 벽)가 수평 요소보다 우선한다는 기준  
D) 엘리베이터 기계실 배치 기준

**ANSWER:** B  
**EXPLANATION:** 코디네이션 시 공간이 부족할 경우 어떤 시스템의 경로를 먼저 변경할지 결정하는 기준이다. 일반적으로 중력 흐름 배관(위생, 드레인)이 가장 높은 우선순위를 가진다.

---

**Q5 (Multiple Choice)**
Navisworks에서 클래시 상태를 "Approved(승인)"로 변경하는 것이 적절한 경우는?

A) 클래시를 발견했지만 수정 시간이 없을 때  
B) 엔지니어링 검토 후 해당 충돌이 허용 가능하거나 의도적인 것으로 확인되었을 때  
C) 클래시가 자동으로 해결될 것으로 예상될 때  
D) 클래시 개수를 줄여 보고서를 짧게 만들 때

**ANSWER:** B  
**EXPLANATION:** Approved 상태는 엔지니어링 판단으로 허용 가능하다고 결정된 클래시에 사용한다. 임의로 Approved 처리하면 실제 문제를 은폐할 수 있으므로 반드시 검토 근거를 남겨야 한다.

---

**Q6 (Multiple Choice)**
MEP 코디네이션 회의에서 "Issue Tracker"를 사용하는 주요 목적은?

A) 회의 참석자 명단 관리  
B) 클래시 및 조정 이슈를 추적하고, 담당자 배정, 기한 설정, 해결 상태를 기록하는 것  
C) Revit 파일 버전 관리  
D) 비용 변경 사항 기록

**ANSWER:** B  
**EXPLANATION:** Issue Tracker(BIM 360/ACC의 Issues, Navisworks의 Comments 등)는 발견된 문제를 체계적으로 추적하고 책임을 명확히 하기 위한 도구다. 해결되지 않은 이슈가 현장 오류로 이어지는 것을 방지한다.

---

**Q7 (Short Answer)**
주간 MEP 코디네이션 회의에서 BIM 코디네이터가 회의 전에 준비해야 할 사항을 3가지 이상 나열하세요.

**ANSWER (Model answer):** (1) 업데이트된 클래시 보고서 준비, (2) 지난 회의 이슈 목록의 해결 상태 업데이트, (3) 각 분야별 최신 모델 병합 확인, (4) 해결이 필요한 미결 이슈 우선순위 정리, (5) 회의 의제 배포.  
**SCORING:** Award 1 point for listing any 3 of the above or equivalent valid items.

---

**Q8 (Multiple Choice)**
Revit에서 링크된 모델(Linked Model)의 클래시를 Navisworks에서 확인하려면 어떤 형식으로 내보내야 하나요?

A) PDF  
B) IFC  
C) NWC (Navisworks Cache) 또는 NWD  
D) DWG

**ANSWER:** C  
**EXPLANATION:** Revit은 Navisworks Exporter 플러그인을 통해 .nwc 파일로 내보낼 수 있다. 여러 분야의 .nwc 파일을 Navisworks에서 조합(Append)하여 전체 모델 클래시 감지를 수행한다.

---

**Q9 (Multiple Choice)**
클래시 해결 우선순위 결정 시 가장 먼저 경로를 조정해야 하는 시스템은?

A) 냉난방 공조 덕트  
B) 중력 배수 배관 (Gravity Drainage)  
C) 케이블 트레이  
D) 전기 배관 (Conduit)

**ANSWER:** B  
**EXPLANATION:** 중력 배수 배관은 경사도를 유지해야 하므로 경로 변경이 가장 어렵다. 따라서 다른 시스템이 배수관을 피하도록 조정하는 것이 원칙이다.

---

**Q10 (Short Answer)**
BIM 코디네이션 과정에서 "RFI(Request for Information)"가 발생하는 상황과 그 목적을 설명하세요.

**ANSWER (Model answer):** RFI는 설계 도서에 불명확하거나 상충된 정보가 있을 때 시공사 또는 BIM 팀이 설계자에게 공식적으로 확인을 요청하는 문서다. 목적은 시공 전 불확실성을 제거하고 변경 사항을 공식 기록으로 남기는 것이다.  
**SCORING:** Award 1 point for mentioning (a) request for design clarification and (b) formal documentation purpose.

---

# LEVEL 4 ASSESSMENT — Lead

**Topics:** BEP sections, QA/QC criteria, delivery management, team operations

---

**Level 4 수준 진단 테스트**

---

**Q1 (Multiple Choice)**
BEP(BIM Execution Plan)에서 "BIM 목표(BIM Goals)"와 "BIM 활용(BIM Uses)"의 차이는?

A) BIM 목표는 클라이언트 요구사항이고, BIM 활용은 소프트웨어 목록이다  
B) BIM 목표는 프로젝트에서 BIM을 통해 달성하려는 결과이고, BIM 활용은 그 목표를 달성하기 위해 사용할 구체적인 BIM 프로세스다  
C) 두 용어는 같은 의미이다  
D) BIM 목표는 비용 절감만을 의미한다

**ANSWER:** B  
**EXPLANATION:** BIM 목표(예: 시공 오류 30% 감소)는 What을 정의하고, BIM 활용(예: 클래시 감지, 4D 시뮬레이션, QTO)은 How를 정의한다. 두 요소는 BEP의 핵심 구조를 이룬다.

---

**Q2 (Multiple Choice)**
BEP에서 "정보 전달 이정표(Information Delivery Milestone)"란?

A) 프로젝트 킥오프 날짜  
B) 특정 LOD의 모델 또는 데이터가 발주처나 타 분야에 전달되어야 하는 시점  
C) 소프트웨어 업데이트 일정  
D) 팀 회의 빈도

**ANSWER:** B  
**EXPLANATION:** 정보 전달 이정표는 누가, 무엇을, 언제, 어떤 형식으로 전달해야 하는지를 명시한다. 이를 통해 각 분야의 납품 책임과 기한이 명확해진다.

---

**Q3 (Short Answer)**
BIM 리드로서 납품 전 QA/QC 체크를 수행할 때 최소한 확인해야 할 5가지 항목을 나열하세요.

**ANSWER (Model answer):** (1) 열린 커넥터(Open Connectors) 없음 확인, (2) 명명 규칙 준수 여부, (3) 필수 파라미터 입력 완료 여부, (4) 요소 LOD가 계약 요건 충족 여부, (5) Revit 경고(Warning) 누적 수 확인 및 주요 경고 해결, (6) 링크된 모델 공유 좌표 일치 여부.  
**SCORING:** Award 1 point for listing any 5 valid QA/QC items.

---

**Q4 (Multiple Choice)**
팀 내 BIM 담당자가 납품 기한 3일 전에 모델에 심각한 오류를 발견했다고 보고했을 때 BIM 리드의 첫 번째 조치는?

A) 오류를 무시하고 납품 진행  
B) 오류의 심각도를 평가하고, 발주처 또는 PM에게 상황을 즉시 보고한 뒤 수정 일정을 협의  
C) 담당자를 교체  
D) 납품 기한을 일방적으로 연장

**ANSWER:** B  
**EXPLANATION:** 납품 전 오류 발견 시 은폐하지 않고 투명하게 보고하고, 우선순위에 따라 수정 계획을 수립하는 것이 BIM 리드의 책임이다. 발주처와 PM이 조기에 상황을 파악해야 대응이 가능하다.

---

**Q5 (Multiple Choice)**
Common Data Environment(CDE)에서 "Published" 상태의 문서 또는 모델이 의미하는 것은?

A) 아직 검토가 필요한 초안 상태  
B) 검토와 승인이 완료되어 다른 분야가 참조할 수 있는 공식 상태  
C) 폐기된 문서  
D) 암호화가 필요한 기밀 파일

**ANSWER:** B  
**EXPLANATION:** CDE(공통 데이터 환경)에서 Published/Approved 상태는 공식 검토를 통과한 참조 가능한 정보를 의미한다. 다른 분야는 Published 모델만을 기준으로 작업해야 조정 혼란을 방지할 수 있다.

---

**Q6 (Multiple Choice)**
BIM 납품물 검토 시 IFC 파일 품질을 확인하는 도구로 가장 적합한 것은?

A) Microsoft Excel  
B) Solibri Model Checker 또는 BIMcollab Zoom  
C) AutoCAD  
D) Adobe Acrobat

**ANSWER:** B  
**EXPLANATION:** Solibri Model Checker 또는 BIMcollab Zoom은 IFC 파일의 속성, 구조, 기하학적 정확도를 자동으로 검증하는 BIM QA 도구다. 발주처 IFC 납품 전 필수 검토 단계이다.

---

**Q7 (Short Answer)**
BIM 코디네이션 팀의 신입 모델러가 Revit에서 반복적으로 시스템 연결을 빠뜨리는 경우, BIM 리드가 취할 수 있는 두 가지 접근 방법을 설명하세요.

**ANSWER (Model answer):** (1) 교육 접근: 시스템 연결의 중요성을 설명하는 짧은 가이드 또는 체크리스트를 작성하여 팀에 배포하고, 오픈 커넥터 확인 방법을 직접 시연한다. (2) 프로세스 접근: 납품 전 QA 체크리스트에 "오픈 커넥터 확인" 항목을 필수로 포함시키고, QA 담당자가 검토 후 서명하도록 절차를 구조화한다.  
**SCORING:** Award 1 point for proposing both a training/mentoring approach and a process/QA approach.

---

**Q8 (Multiple Choice)**
ISO 19650 기반 BIM 프로세스에서 "EIR(Employer's Information Requirements)"의 역할은?

A) 시공사가 발주처에 제출하는 기술 제안서  
B) 발주처가 프로젝트에서 필요로 하는 BIM 정보와 납품 기준을 정의하는 문서  
C) 소프트웨어 라이선스 계약서  
D) 프로젝트 예산 분류 코드

**ANSWER:** B  
**EXPLANATION:** EIR은 발주처의 BIM 요구사항(정보 요건, LOD, 파일 형식, 납품 시점, 명명 규칙 등)을 정의하는 문서다. BEP는 EIR에 응답하는 형식으로 작성된다.

---

**Q9 (Multiple Choice)**
프로젝트 BIM 코디네이션에서 "모델 분리(Model Separation)" 전략이 필요한 주요 이유는?

A) 파일 크기를 크게 만들기 위해  
B) 대형 프로젝트에서 Revit 성능 유지, 분야별 독립 작업, 권한 관리를 위해  
C) 클래시 감지를 방지하기 위해  
D) 발주처가 분리된 파일을 선호하기 때문

**ANSWER:** B  
**EXPLANATION:** 대형 프로젝트에서 모든 분야를 하나의 Revit 파일에 통합하면 성능이 급격히 저하된다. 분야별, 구역별로 모델을 분리하고 링크로 조합하는 전략이 필요하다.

---

**Q10 (Short Answer)**
BIM 리드로서 발주처(Client)와의 월간 BIM 검토 회의를 준비할 때 반드시 포함해야 할 자료 3가지를 설명하세요.

**ANSWER (Model answer):** (1) 현재 모델 진행 상황 요약 (LOD 달성 현황, 미완료 구역 목록), (2) 클래시 현황 보고서 (총 클래시 수, 해결된 수, 미결 수, 우선순위 미결 항목), (3) 다음 이정표까지의 납품 계획 및 리스크 사항.  
**SCORING:** Award 1 point for including any 3 of: progress status, clash report, delivery plan, risk register, or open issues list.

---

# LEVEL 5 ASSESSMENT — Automation

**Topics:** Dynamo concepts, Python basics, Revit API understanding, automation ROI

---

**Level 5 수준 진단 테스트**

---

**Q1 (Multiple Choice)**
Dynamo에서 "노드(Node)"란 무엇인가요?

A) Revit의 구조 절점  
B) 특정 기능(연산, 데이터 조작, Revit 조작)을 수행하는 시각적 프로그래밍 블록  
C) Python 코드 파일  
D) Dynamo 설치 폴더

**ANSWER:** B  
**EXPLANATION:** Dynamo는 노드 기반 시각적 프로그래밍 환경이다. 각 노드는 입력을 받아 처리 후 출력을 내보내며, 노드들을 와이어(Wire)로 연결하여 로직 흐름을 구성한다.

---

**Q2 (Multiple Choice)**
Dynamo에서 List.Map 노드의 기능은?

A) 리스트를 알파벳 순으로 정렬한다  
B) 리스트의 각 항목에 동일한 함수를 적용하여 결과 리스트를 반환한다  
C) 두 리스트를 하나로 합친다  
D) 리스트에서 중복 항목을 제거한다

**ANSWER:** B  
**EXPLANATION:** List.Map은 함수형 프로그래밍의 map 연산과 동일하다. MEP BIM에서는 예를 들어 "모든 덕트 요소에 대해 레벨 파라미터를 읽어 리스트로 반환"하는 데 사용된다.

---

**Q3 (Short Answer)**
Revit API에서 "Transaction"이 반드시 필요한 이유를 설명하세요.

**ANSWER (Model answer):** Revit의 데이터베이스는 ACID 트랜잭션 모델로 보호되어 있다. API를 통해 Revit 문서를 수정하는 모든 작업(요소 생성, 파라미터 변경 등)은 반드시 Transaction 블록 안에서 실행해야 한다. 트랜잭션이 없으면 Revit이 변경을 거부하고, 트랜잭션 실패 시 Rollback으로 모델 무결성이 보호된다.  
**SCORING:** Award 1 point for mentioning (a) required for any modification to Revit document and (b) rollback/integrity protection on failure.

---

**Q4 (Multiple Choice)**
Python에서 다음 코드의 출력은?
```python
elements = [1, 2, 3, 4, 5]
result = [x * 2 for x in elements if x > 2]
print(result)
```

A) [1, 2, 3, 4, 5]  
B) [2, 4, 6, 8, 10]  
C) [6, 8, 10]  
D) [3, 4, 5]

**ANSWER:** C  
**EXPLANATION:** 리스트 컴프리헨션에서 `if x > 2` 조건으로 3, 4, 5만 선택되고, `x * 2`로 각각 6, 8, 10이 된다. MEP Dynamo 스크립트에서 조건부 필터링에 자주 사용되는 패턴이다.

---

**Q5 (Multiple Choice)**
Revit API에서 "FilteredElementCollector"의 역할은?

A) Revit 경고(Warning)를 필터링하는 기능  
B) 프로젝트 또는 뷰 내의 Revit 요소를 조건에 따라 선택하고 수집하는 쿼리 도구  
C) IFC 파일을 내보내는 기능  
D) Revit 패밀리를 삭제하는 기능

**ANSWER:** B  
**EXPLANATION:** FilteredElementCollector는 Revit API의 핵심 쿼리 메커니즘이다. 특정 카테고리, 클래스, 파라미터 조건으로 요소를 선택한다. 예: 모든 덕트 요소 수집 → 파라미터 일괄 수정.

---

**Q6 (Short Answer)**
MEP BIM 팀에서 Dynamo 스크립트로 자동화할 때 ROI(투자 대비 수익)를 계산하는 방법을 간단히 설명하세요.

**ANSWER (Model answer):** ROI = (자동화 전 수동 작업 시간 × 시간당 인건비) − 스크립트 개발 시간 × 시간당 인건비. 예: 수동 작업 5시간/월을 5분으로 줄이면 연간 절감 = 59.9시간 × 시간당 단가. 개발에 8시간이 걸렸다면 약 2개월 내 ROI 달성. 반복 빈도가 높을수록 ROI가 높다.  
**SCORING:** Award 1 point for mentioning (a) comparison of manual time vs. automated time and (b) amortizing development cost over repeated runs.

---

**Q7 (Multiple Choice)**
Dynamo에서 "Lacing(레이싱)" 설정의 목적은?

A) Dynamo 스크립트를 Revit에 저장하는 방법  
B) 길이가 다른 두 리스트를 노드에 입력할 때 리스트 항목을 매핑하는 방식을 제어하는 것  
C) 노드의 색상을 변경하는 기능  
D) Revit API 버전 선택

**ANSWER:** B  
**EXPLANATION:** Lacing은 Shortest, Longest, Cross Product 세 가지 옵션이 있다. 예: 10개 요소 리스트와 3개 값 리스트를 연결할 때 Longest는 마지막 값을 반복 사용한다. 잘못된 Lacing 선택은 예상치 못한 결과를 낳는다.

---

**Q8 (Multiple Choice)**
다음 중 Dynamo 스크립트로 자동화하기 가장 적합한 MEP 작업은?

A) 새로운 MEP 시스템 엔지니어링 설계 결정  
B) 수백 개의 MEP 요소에 표준 파라미터 값을 일괄 입력  
C) 클래시 해결을 위한 엔지니어링 판단  
D) 발주처와의 계약 협상

**ANSWER:** B  
**EXPLANATION:** 반복적이고 규칙 기반인 작업(파라미터 일괄 입력, 명명 규칙 적용, 뷰 생성)이 자동화 최적 대상이다. 엔지니어링 판단이 필요한 작업은 자동화 범위 밖이다.

---

**Q9 (Short Answer)**
Revit API를 사용하여 프로젝트 내 모든 배관(Pipe) 요소의 "System Type" 파라미터 값을 읽어 콘솔에 출력하는 코드의 핵심 단계를 순서대로 설명하세요 (코드 작성 불필요 — 단계만 기술).

**ANSWER (Model answer):** (1) FilteredElementCollector를 사용하여 현재 문서에서 Pipe 카테고리 요소를 모두 수집한다. (2) 각 Pipe 요소를 반복(iterate)한다. (3) 각 요소에서 LookupParameter("System Type") 또는 get_Parameter(BuiltInParameter)로 파라미터를 가져온다. (4) Parameter.AsValueString() 또는 AsString()으로 값을 읽는다. (5) TaskDialog 또는 Python print로 출력한다.  
**SCORING:** Award 1 point for correctly describing all 5 stages in order.

---

**Q10 (Multiple Choice)**
MEP BIM 자동화 스크립트를 팀 전체에 배포할 때 가장 중요한 고려사항은?

A) 스크립트의 시각적 디자인  
B) 스크립트의 Revit 버전 호환성 테스트, 오류 처리 코드 포함, 사용법 문서화  
C) 스크립트를 가능한 한 짧게 만드는 것  
D) 스크립트를 암호화하여 수정 불가하게 하는 것

**ANSWER:** B  
**EXPLANATION:** 팀 배포용 스크립트는 (1) 사용하는 Revit 버전에서 테스트, (2) 예외 처리로 오류 시 Revit 크래시 방지, (3) 비개발자도 사용할 수 있는 명확한 문서가 필수다. 이 세 가지가 없으면 팀 혼란과 오용으로 이어진다.

---

*End of Level Assessments v1.0 — FOR LUA BIM LABS USE ONLY*
