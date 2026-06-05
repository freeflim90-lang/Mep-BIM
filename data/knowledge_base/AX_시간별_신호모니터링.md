# AX 시간별 신호모니터링 지식 베이스

AX 기업 성장을 위해 건설, 설계, 시공, BIM, AI 관련 시간별 신호를 가볍게 기록한다.
깊은 판단은 일일 큐레이션과 주간 AX 전략 리뷰에서 수행한다.

## 2026-06-05 AX 신호모니터링 운영 기준 업데이트
- Source: LUA BIM LABS AX 전략 리뷰(W23), 내부 성장 펄스
- Tags: ax,signal-monitoring,construction-ai,trend,2026

**AX 시간별 신호 분류 기준 (2026 업데이트):**
| 신호 유형 | 설명 | 다음 액션 |
|---------|------|---------|
| 고신호 (즉시) | BIM 의무화 확대·AX 바우처 공고 | 당일 전략 반영 |
| 중신호 (주간) | 해외 BIM 트렌드·기술 발표 | 주간 AX 리뷰에서 판단 |
| 저신호 (관찰) | 일반 건설 뉴스·참고 자료 | Watch 유지 |

**2026-06-05 기준 주요 AX 신호 현황:**
- 국내 건설 AI 전환 시장 급성장 (경기도 AI 도입 추진)
- buildingSMART openBIM Hackathon Porto 2026 (글로벌 협업 기회)
- Autodesk MaintainX 인수($3.6B): BIM+FM 통합 가속
- AX 원스톱 바우처 지원사업 공고 (13억원 지원)
- DL이앤씨 MEP BIM 완전 자동화 목표 (2026) → MEP BIM 수요 증가


## 2026-05-28 09:54 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-28/0954_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- Key Outcomes from the Domain Leadership Conference in Zurich (BIM Automation)
- buildingSMART International Appoints Aidan Mercer as Managing Director (BIM Automation)
- 대우건설, AI·스마트건설 오픈이노베이션 추진 - 인더뉴스 (Smart Construction, BIM Automation)
- 대우건설, 안전·AI·스마트건설 분야 예비창업자 모집 나선다 - 한국경제 (Smart Construction, BIM Automation)
- What's New with ArcGIS GeoBIM in ArcGIS Enterprise 12.1 (May 2026) - Esri (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-28 15:56 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-28/1556_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- 대우건설, 오픈 이노베이션 통해 안전‧AI‧스마트건설 핵심 기술 확보 나선다 - 내외뉴스통신 (Smart Construction, BIM Automation)
- AI로 중대재해 예방…대우건설, 오픈 이노베이션 열고 핵심 기술 확보 - 네이트 (BIM Automation)
- Top AI Field Reporting Apps for Contractors in 2026 - Robotics & Automation News (BIM Automation)
- SLA Designs Public Spaces and Streetscapes for Toronto's New Island Community in the Port Lands (BIM Automation)
- Anatomy of a Maya City: The Urban Structure of Copán in Honduras (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.

## AX 시간별 신호모니터링 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: ax,signal-monitoring,industry-intelligence,automation,bim-automation

**신호 수집 자동화 체계:**
- RSS/Atom 피드 수집: buildingSMART News, Autodesk AEC Blog, Revit Forum, 국토교통부 보도자료 RSS
- 수집 주기: 매시 정각 APScheduler 5.x cron trigger → Python 3.12 비동기 aiohttp 병렬 요청
- 신호 분류 기준: BIM Automation / Smart Construction / AI Regulation / Market Signal / Product Opportunity
- 중복 제거: 제목 SHA-256 해시 기반 deduplication (동일 신호 24시간 내 재수집 차단)
- 고신호 임계값: 3개 이상 채널 동시 등장 OR 국내 법규 변경 관련 키워드 포함

**2026년 주요 모니터링 채널:**
- buildingSMART International: IFC 4.4 Draft, IDS 1.0 배포 상황
- Autodesk App Store: 심사 정책 변경 (2025년 8월 코드 서명 강화), 리뷰 API 정책
- 국토부 고시: BIM 의무화 연면적 기준 3만㎡ → 1만㎡ 단계적 확대 모니터링
- 소방청 NFTC 개정: 2025년 NFTC 103 헤드 간격·유량 기준 개정 추적
- GitHub Trending: Revit API, Dynamo, IFC 관련 오픈소스 신호

**승격 로직:**
- 시간별 신호 → 일일 큐레이션: 같은 키워드 3시간 내 2회 이상 등장 시 자동 플래그
- 일일 → 주간 전략 리뷰: 일일 4.0점 이상 평균 신호
- 주간 → 제품 백로그: CSO 승인 후 GitHub Issues 자동 생성
- 관련: [[AX_전략승격리뷰]] · [[산업동향_데일리브리핑]] · [[내부성장루프]] · [[법규변경모니터링]]


## AX 시간별 신호모니터링 마스터급 경험 지식 (2026-05-29)
- Source: claude-code-enhanced 2026-05-29
- Tags: AX모니터링, 신호감지, 비정형건물신호, 오탐감소, 임계값조정

### 신호 모니터링 오탐(False Positive) 감소 전략

**비정형 건물 관련 신호 특수성:**
- "비정형", "자유형", "파라메트릭", "랜드마크" 키워드는 고부가가치 프로젝트 신호
- 일반 건설 키워드(아파트, 오피스) 대비 3~5배 높은 단가 → 신호 가중치 1.5배 적용 권장

**오탐 감소 패턴:**

| 오탐 유형 | 원인 | 해결 |
|---------|------|------|
| 경쟁사 자사 광고 | 경쟁사 제품명으로 검색 히트 | 네거티브 키워드 목록 관리 |
| 해외 뉴스 국내 무관 | 번역 기사 → 실제 수요 없음 | 한국 도메인 소스 필터링 |
| 연구/학술 언급 | 논문 인용 → 실제 도입 아님 | ".ac.kr" 소스 가중치 낮춤 |
| 오래된 기사 재확산 | 3개월+ 이전 기사 SNS 공유 | 발행일 기준 30일 이내만 집계 |

### 신호 점수 계산 예시 (BIM 도메인 특화)

```python
SIGNAL_WEIGHTS = {
    "BIM_의무화": 5.0,
    "비정형_건물": 4.5,  # 고부가가치 가중치
    "Revit_AddIn": 4.0,
    "클래시_검토": 3.5,
    "IFC_납품": 3.0,
    "BIM_모델러": 2.5,
    "아파트_BIM": 2.0,  # 경쟁 포화 감점
}
NEGATIVE_KEYWORDS = ["연구", "논문", "해외", "학술"]

def score_signal(text: str) -> float:
    score = sum(w for kw, w in SIGNAL_WEIGHTS.items() if kw.replace("_", " ") in text)
    penalty = 1.0 if any(neg in text for neg in NEGATIVE_KEYWORDS) else 0.0
    return max(0, score - penalty)
```


## 2026-05-28 22:05 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-28/2205_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- "건설산업, AI 기반 프로세스 혁신"...'AECO AX 서밋’ 성료 - 지디넷코리아 (AX/AI Transformation, BIM Automation)
- 대우건설, 안전·AI 분야 스타트업 발굴해 기술 협업 - 핸드메이커 (BIM Automation)
- Top 5 Cloud Migration and Backup Companies in 2026 An Honest Comparison - openPR.com (Watch)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-29 06:57 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-29/0657_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- Zemlja Earth Apartment / Projekt V Arhitektura (BIM Automation, Quality/Product)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-29 08:23 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-29/0823_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- 대우건설, 스타트업 혁신기술 공개 모집…안전·AI·로보틱스 5개 분야 - 글로벌이코노믹 (BIM Automation)
- Best CPM Scheduling Tools for Construction Teams in 2026 - GigWise (Watch)
- Prefab & Modular Construction Trends 2026 | Sustainabllity Awards - Architecture & Design (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-29 09:23 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-29/0923_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- 대우건설, 건기연과 '하이퍼 안전 및 AI 오픈 이노베이션' 개최 - 투어코리아 (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-29 17:05 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-29/1705_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- “AI 맞춰 건설산업 프로세스 혁신”…‘AECO AX Summit’ 성료 - 헤럴드경제 (AX/AI Transformation, BIM Automation)
- 대우건설, '2026 대우건설 Hyper Safety & AI 오픈 이노베이션' 개최 - 벤처타임즈 (BIM Automation)
- Shang'Ao Canal Social Service Center / Atelier Liu Yuyang Architects (BIM Automation, Quality/Product)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-30 09:37 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-30/0937_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- [중대재해사고예방] 대우건설, AI·IoT로 '건설 현장' 안전시스템 구축 - 주간한국 (BIM Automation)
- 보스턴다이내믹스 스팟, 美 대형 건설사 맥카시 ‘디지털 시공’ 시연 무대 등장 - 더구루 (BIM Automation)
- Global BIM Market Size Expected to Hit USD 20.7 Billion by 2035 - openPR.com (BIM Automation)
- More Architecture for Less: SSdH and the Latent Potential of Existing Buildings (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-30 12:51 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-30/1251_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- [중대재해사고예방] BS한양, ‘충돌·질식·추락막는 AI’...스마트 안전관리 본격 가동 - 주간한국 (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-30 14:16 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-30/1416_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- 한명식 "경영 효율화로 엔지니어링 대가 20~30% 높일 수 있어" - 뉴시스 (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-30 16:45 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-30/1645_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- 한명식 "경영 효율화로 엔지니어링 대가 20~30% 높일 수 있어" - yjb0802.com (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-30 17:46 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-30/1746_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- The buildingSMART Implementers Assembly, February 2026 Event Report (BIM Automation)
- Python in AEC. The simplest 6-step learning path to automation (BIM Automation)
- IFC Use Cases – 5 Practical Applications (Part 2) (BIM Automation, Quality/Product)
- Haulotte tests robotic arms attached to MEWPs (BIM Automation)
- Your Digital Construction Week to-do list (Smart Construction, BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-31 14:40 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-31/1440_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- Autodesk Q1 Earnings Call Highlights - The Globe and Mail (BIM Automation)
- “AI 맞춰 건설산업 프로세스 혁신”…‘AECO AX Summit’ 성료 - 헤럴드경제 (AX/AI Transformation, BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-05-31 19:55 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-05-31/1955_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- Global BIM Market Size Expected to Hit USD 20.7 Billion by 2035 - openPR.com (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-01 07:52 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-01/0752_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- [파워인터뷰]이윤상 가덕도신공항건설공단 이사장 “우선시공분 연내 착공…2035년 반드시 개항” - 대한경제 (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-01 09:57 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-01/0957_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- 한미글로벌·M3시스템즈·밸류맵, ‘AI 기반 모듈러 건축 혁신 비즈니스’ 모델 구축… 건설산업 비효율성 개선 앞장선다 - 국토일보 (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-01 17:30 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-01/1730_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- Build safe, smart and sustainable: CIOB Midlands event discusses competence and delivering sustainability safely (BIM Automation)
- Policy, funding and capability take stage at CIOB retrofit discussion (BIM Automation, Quality/Product)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-02 07:00 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-02/0700_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- IMAGINiT launches Clarity 2027 for AEC automation - Engineering.com (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-02 17:27 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-02/1727_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- '센서·AI·로봇'…스마트 안전기술로 사고 막는다 - 주간한국 (BIM Automation)
- What if your BIM model could say ‘no’? (Smart Construction, BIM Automation, Quality/Product)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-03 10:42 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-03/1042_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- '센서·AI·로봇'…스마트 안전기술로 사고 막는다 - 주간한국 (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-03 17:13 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-03/1713_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- BIM Services India's Revit Models Maximize Site Safety and Productivity - openPR.com (AX/AI Transformation, BIM Automation, Quality/Product)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-04 11:35 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-04/1135_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- 경기도, 건설 안전·품질 관리분야 AI 도입 추진 - 네이트 (BIM Automation, Quality/Product)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-04 13:27 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-04/1327_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- 경기도, 건설현장에도 AI 도입. 중소건설기업 활성화 방안 모색 - 시사일보 (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-04 15:25 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-04/1525_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- 경기도, 건설현장에도 AI 도입. 중소건설기업 활성화 방안 모색 - 경인통신 (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-04 22:42 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-04/2242_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- 경기도, 건설현장 스마트화 추진…경기도, AI 활용 정책 연구 착수 - 디스커버리뉴스(DISCOVERYNEWS) (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-05 05:44 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-05/0544_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- BIM and CAD Integrations at the 2026 Esri User Conference - Esri (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-05 20:12 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-05/2012_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- 경기도, 건설분야 AI 활용 전략 수립 착수 - 글로벌에픽 (BIM Automation)
- 경기도, 건설현장에도 AI 도입. 중소건설기업 활성화 방안 모색 - 엔디엔뉴스 (BIM Automation)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.


## 2026-06-05 21:13 AX 시간별 고신호
- Source: `docs/industry_intelligence/hourly/2026-06-05/2113_AX_SIGNAL_MONITOR.md`
- Tags: ax,hourly-signal,construction,bim,ai

- Modelling the unmortared: how Aecom helped build the 2026 Serpentine Pavilion (BIM Automation, Quality/Product)

운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.
