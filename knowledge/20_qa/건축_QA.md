# 건축 Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(건축.md)과 분리 운영.

## 2026-06-05 건축 실전 Q&A 추가 (BIM LOD·BF 기준 반영)
- Source: 건설산업 BIM 기본지침, 건축법 시행령, BF 인증 기준
- Tags: architecture,qa,lod,bf,bim,2026

**Q: 건축 BIM LOD 300과 LOD 350 차이가 뭔가요?**
A: LOD 300은 치수·재료·개구부가 확정된 수준으로 설계도면 수준입니다. LOD 350은 공종 간 인터페이스(MEP 관통·개구부 위치·연결부) 조율이 완료된 수준입니다. 실무에서 실시설계 납품은 LOD 350이 기준이며, LOD 300 → 350은 간섭검토 후 수정된 결과가 반영되어야 합니다. *(KST01 공식확인)*

**Q: 건축 BIM에서 방화구획을 어떻게 표현하나요?**
A: Revit에서 방화구획 경계벽은 Fire Rating 파라미터(1시간·2시간)를 입력합니다. 방화구획 관통부에는 방화댐퍼·내화충전재 파라미터를 추가합니다. BIM에서 방화구획 경계를 색상으로 구분하면 간섭검토 시 소방 경로와 함께 확인이 쉽습니다. *(KST01 공식확인)*

**Q: BF(Barrier-Free) 인증을 위해 BIM에서 무엇을 확인해야 하나요?**
A: BF 인증 대상 시설 여부를 먼저 확인합니다. 장애인등편의법 시행령 별표 기준으로 주출입구 경사(1/18 이하), 문폭(900mm 이상), 복도폭(1,200mm 이상), 화장실 회전반경(1,500mm 이상)을 BIM에서 파라미터로 입력·확인합니다. 자동검수는 후보를 찾는 1차 수단이며, BF 인증 통과는 인증기관·설계자 확인으로 확정합니다. *(KST01 공식확인 + KST03 적용주의: 인증기관 확인 필요)*

**Q: 건축 BIM과 구조 BIM을 별도 파일로 관리하는 이유가 뭔가요?**
A: 성능 관리와 작업 분업 때문입니다. 대형 프로젝트에서 건축+구조를 한 파일에 담으면 파일 크기가 너무 커집니다. Revit Link로 각 파일을 연결하면 공종별 팀이 독립적으로 작업하면서 통합 뷰를 볼 수 있습니다. Workset 방식도 있지만 링크 파일 방식이 분업에 유리합니다. *(KST03 적용주의: 프로젝트 규모와 발주처 요건에 따라 달라짐)*


## 건축 FAQ (2026-05-23)
- Source: LUA BIM LABS internal MEP knowledge baseline
- Tags: architecture,faq,bim,coordination,ceiling,fire-compartment

방화구획을 MEP가 관통할 때 어떻게 처리하는지 물을 때:
- 배관은 방화 슬리브(Steel Sleeve) + 내화채움재(Firestop)로 처리한다.
- 덕트는 방화댐퍼(Fire Damper)를 방화구획 경계에 설치한다.
- 소방 배관은 방화댐퍼 없이 관통 가능하지만 방화 슬리브와 내화채움재는 필요하다.
- 케이블·전선관은 내화채움재로 처리한다.

천장 안에 MEP가 너무 많아서 천장고가 낮아질 때 어떻게 하는지 물을 때:
- 먼저 우선순위가 낮은 설비(말단 배관, 전선관)를 조정한다.
- 덕트 단면을 넓이보다 높이를 줄이는 방향으로 재검토한다.
- 구조 보를 관통하는 방안을 구조팀과 협의한다.
- 해결이 어려우면 건축 레벨(슬래브 높이) 조정을 설계팀에 제안한다.

건축 모델과 MEP 모델이 다를 때 무엇을 기준으로 하는지 물을 때:
- 최신 승인된 건축 도면과 모델이 기준이다.
- 건축 링크 모델 개정 이력을 확인하고 최신 버전으로 업데이트한다.
- 차이가 있으면 건축 담당자에게 확인하고 MEP 모델을 수정한다.


## Q: 인천공항 제2터미널 면적이 얼마야? (2026-05-24 07:18:30)
- Source: telegram-qa
- Tags: qa,auto-collect

인천공항이 제시한 T1 종합시설개선 계획에 따르면 리뉴얼 공사는 2028년 1월부터 2032년 8월까지 약 4년 7개월간 구간별로 진행된다. 공사 기간 중 터미널 전체 면적의 25~50%가량이 단계적으로 폐쇄될 수 있고, 해당 구역...


## Q: 인천공항 제1터미널 면적이 얼마야? (2026-05-24 07:18:53)
- Source: telegram-qa
- Tags: qa,auto-collect

인천공항 1터미널은 50만 7천㎡의 넓은 면적을 자랑합니다. 이는 축구장 70개가 넘는 크기로, 연간 1억 600만 명의 여객을 처리할 수 있는 막대한 수용력을 갖추고 있습니다. 넓은 공간과 높은 처리능력으로 편리하고 효율적인 여행을 지원합니다.


## Q: 인천공항 제2터미널 면적이 얼마야? (2026-05-24 07:19:20)
- Source: telegram-qa
- Tags: qa,auto-collect

인천공항이 제시한 T1 종합시설개선 계획에 따르면 리뉴얼 공사는 2028년 1월부터 2032년 8월까지 약 4년 7개월간 구간별로 진행된다. 공사 기간 중 터미널 전체 면적의 25~50%가량이 단계적으로 폐쇄될 수 있고, 해당 구역...


## Q: 인천공항 건축 물량이 얼마나 들어갔어? (2026-05-24)
- Source: telegram-qa
- Tags: architecture,qa,incheon-airport,quantity

인천국제공항 건축 연면적 참고 수치 (공개 자료 기준):

| 시설 | 연면적 |
|---|---|
| 여객터미널 1 (1단계, 2001) | 약 496,000 m² |
| 탑승동 Concourse (2단계, 2008) | 약 105,600 m² |
| 여객터미널 2 (3단계, 2018) | 약 384,000 m² |
| 탑승동 2 (3단계, 2018) | 약 99,000 m² |
| 전체 터미널 합계 | 약 1,084,000 m² |
| 화물터미널·지원시설 포함 총 건축면적 | 약 1,700,000 m² 이상 추정 |

주의: 위 수치는 공개 발표 및 준공 보고서 기반 참고값이며, 정밀 BQ는 인천국제공항공사 발주 설계도서 기준이다.


## Q: 국내 주요 대형 건축 프로젝트 현황 (2026-05-24)
- Source: telegram-qa
- Tags: architecture,qa,domestic-project,large-scale,2025-2030

### SOC·공공 대형 건축

| 프로젝트 | 규모 | 일정 |
|---|---|---|
| GTX-A 수서~동탄 역사 (수서·성남·용인·동탄) | 지하 역사 4개소, 역사당 연면적 약 10,000~30,000 m² | 2024 부분 개통, 2030 완전 개통 목표 |
| GTX-B 인천대입구~마석 역사 | 지하 역사 12개소 | 2030년 개통 목표 |
| GTX-C 양주~수원 역사 | 지하 역사 10개소 | 2028년 개통 목표 |
| 제2경인선 (인천~서울) 역사 | 복선 전철 역사 다수 | 2029년 목표 |
| 새만금 국제공항 청사 | 연면적 약 48,000 m² (1단계) | 2028년 개항 목표 |
| 가덕도 신공항 여객터미널 | 연면적 약 400,000 m² (계획) | 2035년 목표 |

### 민간 대형 복합시설 (건축)

| 프로젝트 | 규모 | 일정 |
|---|---|---|
| 현대GBC (글로벌비즈니스센터), 삼성동 | 연면적 약 930,000 m², 105층 | 2030년 완공 목표 |
| 롯데월드타워 2차 (잠실) | 계획 중 | 미정 |
| 수원 광교 앨리웨이 확장 | 복합 상업 시설 | 진행 중 |
| 용산 국제업무지구 개발 | 약 49만 평 부지 복합개발 | 2030년대 |
| 부산 에코델타시티 스마트빌리지 | 스마트홈·공공시설 복합 | 진행 중 |

주의: 일정·규모는 공개 발표 기준이며 사업 변경 가능성 있음.


## Q: 성수 k project 면적이 얼마야? (2026-05-24 13:09:12)
- Source: telegram-qa
- Tags: qa,auto-collect

성수 K 프로젝트의 연면적은 21만 8093㎡입니다.


## Q: 제2철도 관제센터 연면적은 얼마야? (2026-05-24 13:09:37)
- Source: telegram-qa
- Tags: qa,auto-collect

제2철도교통관제센터의 연면적 정보는 제공된 참고 지식에서 언급되지 않았습니다. 연면적과 관련된 자세한 정보가 필요하다면 건축 설계 문서나 공사 계획서 등을 확인해보세요.


## Q: 성수 k project 면적이 얼마야? (2026-05-24 13:09:55)
- Source: telegram-qa
- Tags: qa,auto-collect

성수 K 프로젝트의 연면적은 21만 8093㎡입니다.


## Q: 청라스타필드 면적이 얼마야? (2026-05-24 13:18:10)
- Source: telegram-qa
- Tags: qa,auto-collect

[📚 지식 베이스 (score 31) + 🔍 웹 검색 보강]

스타필드 청라의 연면적은 51만㎡입니다.


## Q: 청라 스타필드 면적이 얼마야? (2026-05-24 13:18:27)
- Source: telegram-qa
- Tags: qa,auto-collect

[📚 지식 베이스 (score 31) + 🔍 웹 검색 보강]

청라 스타필드의 연면적은 50만㎡입니다. 이 면적은 약 65개의 축구장 크기로, 대규모 프로젝트임을 알 수 있습니다.


## Q: 청라 스타필드 기계실 면적이 얼마야? (2026-05-24 13:18:43)
- Source: telegram-qa
- Tags: qa,auto-collect

[📚 지식 베이스 (score 32) + 🔍 웹 검색 보강]

스타필드 청라의 기계실 면적 정보는 직접적으로 제공된 자료에서 확인할 수 없습니다. 연면적 50만㎡라는 전체 규모만 언급되어 있어, 기계실의 정확한 면적은 추가 정보가 필요합니다. 현장 조사나 설계 문서를 참고해보시는 것이 좋을 것 같습니다.


## Q: gtx a 철근누락으로 현재 내가 진행중인 무역센터 리모델링 프로젝트에 영향이 있지 않을까? (2026-05-24 16:05:40)
- Source: telegram-qa
- Tags: qa,auto-collect

[📚 지식 베이스 (score 16) + 🔍 웹 검색 보강]

GTX-A 노선과 관련된 무역센터 리모델링 프로젝트에서는 철근 누락이 발생했지만, 현재까지 알려진 정보로는 지하철 환승 센터와 직접적인 영향은 없어 보입니다. 하지만 프로젝트 관리에서 철근 누락은 시공 기간 연장이나 비용 증가 등의 부수적 영향을 줄 수 있으므로, 이에 대한 대응 계획을 마련하는 것이 중요합니다.


## Q: phase 구분이 되어있는 파일내에서 간섭해소를 진행하려고 하는데 이때 간섭해소를 빠르게 하는 방법을 알려줘 (2026-05-25 22:28:35)
- Source: telegram-qa
- Tags: qa,auto-collect

[📚 지식 베이스 (score 26) + 🔍 웹 검색 보강]

간섭해소를 빠르게 진행하려면 다음과 같은 방법을 활용할 수 있습니다:

1. **필수적인 간섭만 선택**: 전체 MEP 설계 중에서 간섭이 가장 심한 부분부터 처리합니다.
2. **자동화 도구 사용**: 간섭 검출 및 해소를 위한 자동화된 도구를 활용하여 시간을 절약합니다.
3. **팀워크 강화**: 여러 전문가들이 협력하여 작업을 분배하고 효율적으로 진행합니다.
4. **규칙 설정**: 반복적인 작업을 자동으로 처리할 수 있는 규칙을 정립합니다.
5. **정기적인 검토**: 작업 진행 상황을 주기적으로 점검하여 문제를 빠르게 해결합니다.

이러한 방법들을 통해 MEP BIM 파일의 간섭해소 과정을 효율화할 수 있습니다.


## Q: gtx a 철근누락으로 현재 내가 진행중인 무역센터 리모델링 프로젝트에 영향이 있지 않을까? (2026-05-25 22:46:28)
- Source: telegram-qa
- Tags: qa,auto-collect

[📚 지식 베이스 (score 29) + 🔍 웹 검색 보강]

철근 누락은 시공 기간 연장이나 비용 증가 등의 부수적 영향을 줄 수 있으므로, 이를 대응하기 위한 계획을 마련하는 것이 중요합니다. 하지만 현재까지 알려진 정보로는 무역센터 리모델링 프로젝트와 GTX-A 노선 사이에 직접적인 영향은 없어 보입니다.


## Q: 인천공항 제2터미널 연면적이 얼마야 (2026-05-28 08:23:40)
- Source: search-assisted-qa
- Tags: qa,auto-collect,revit-addin,search-assisted,knowledge-candidate,needs-review

Status: needs-review

Question:
인천공항 제2터미널 연면적이 얼마야

Draft answer:
인천공항 제2터미널(T2)의 연면적은 약 38만 7000㎡입니다. 이는 서울 여의도공원 면적(21만㎡)의 약 20배 규모입니다.

Search evidence:
• [Tavily] Tavily AI 요약
  The Incheon Airport Terminal 2 has a total floor area of 347,000 square meters. It was completed in 2018 and expanded to double the size of the original terminal. The expansion added a large, modern design with eco-friendly features.
  출처: 

• [Naver] 제2 여객터미널-인천국제공항
  주차대행서비스 이용 시, 차량보관을 위한 별도의 주차장 예약은 불필요합니다. 성수기 차량 일시 집중 시, 불가피하게 임시주차장 및 화물청사주차장에 보관할 수 있습니다. 3층 도로는 주차대행 전면금지구간 입니다.
  출처: https://www.airport.kr/ap_ko/961/subview.do

• [Naver] 인천국제공항 제2여객터미널
  개요 인천국제공항 제2여객터미널 은 연면적 380,000m 2 에 지하 2층, 지상 5층의 건물 로 지어졌다.... 영종도 북쪽 해안선을 따라 새로 건설된 도로로 가면 인천공항 제2터미널 이 모습이 드러난다. 두 동의...
  출처: https://ko.wikipedia.org/wiki/%EC%9D%B8%EC%B2%9C%EA%B5%AD%EC%A0%9C%EA%B3%B5%ED%95%AD_%EC%A0%9C2%EC%97%AC%EA%B0%9D%ED%84%B0%EB%AF%B8%EB%84%90

• [Naver] 편의 · 공공시설
  제2여객터미널 3층 면세지역 291번 게이트 인근 ; 제2여객터미널 3층 면세지역 279번 게이트 인근 ; 제2여객터미널 3층 면세지역 220번 게이트 인근
  출처: https://www.airport.kr/ap_ko/1008/subview.do?enc=Zm5jdDF8QEB8JTJGZmFjaWxpdHlJbmZvJTJGYXBfa28lMkYyNSUyRmxpc3QuZG8lM0ZzcmNoVGVybWluYWxJZCUzRFAwMyUyNnNyY2hDb2x1bW4lM0R1c2VyJTI2c3JjaExjbGFzJTNEMSUyNnNyY2hNbHNmYyUzRDE5JTI2c3JjaFNjbGFzJTNEMTkzJTI2c3JjaFdyZCUzRCUyNg%3D%3D

• [Naver] 제2 여객터미널 - 인천국제공항
  주차 가능 대수 ; 지상 4층 · 888대 가능 ; 지상 3층 · 319대 가능 ; 지상 2층 · 176대 가능 ; 지상 1층 · 만차 ; M 층 · 123대 가능
  출처: https://www.airport.kr/ap_ko/966/subview.do

• [Naver] [르포] 인천공항 2터미널, 양날개 달고 완전체로…&quot;아름답고 편한 공항...
  제2터미널의 새 '날개'에는 60ｍ 길이의 일반 무빙워크 6개와 130ｍ 길이의 장거리 무빙워크 3개가 놓였다. 교통약자나 탑승 시간이 얼마 남지 않은 승객의 빠른 이동을 위해서는 현재 인천공항공사가 2대, 대한항공이 6대...
  출처: https://n.news.naver.com/mnews/article/001/[LONG_ID_MASKED]?sid=102

• [Naver] &quot;출국하러? 난 놀러 간다&quot;...인천공항 제2여객터미널
  그런 점에서 지난 18일 새롭게 문을 연 '인천국제공항 제2여객터미널(T2)'은 해외로 떠나는 비행기에 몸을... T2가 서울 여의도공원(21만㎡) 20배에 이르는 연면적 38만7000㎡로 들어섰다지만, 출국장만 봐도 T1보다 크게 작다....
  출처: https://n.news.naver.com/mnews/article/003/[LONG_ID_MASKED]?sid=103

• [Naver] 여행의 시작과 끝, 인천국제공항 사람들
  바로 인천국제공항이다. 연면적 5,606만㎡(약 1,700만 평) 규모의 인천국제공항은 하루 평균 20만 명의 여객이... 4조 3교대로 근무하는 계류장관리팀은 1조당 6~7명의 인원이 T1(제1여객터미널), T2(제2여객터미널), 탑승동...
  출처: http://www.laborplus.co.kr/news/articleView.html?idxno=22361


## Q: 인천공항 제2터미널 연면적이 얼마야`n`n답변 지침: 개장 당시 수치와 최신 확장 후 수치가 다를 수 있으면 (2026-05-28 08:26:18)
- Source: search-assisted-qa
- Tags: qa,auto-collect,revit-addin,search-assisted,knowledge-candidate,needs-review

Status: needs-review

Question:
인천공항 제2터미널 연면적이 얼마야`n`n답변 지침: 개장 당시 수치와 최신 확장 후 수치가 다를 수 있으면 기준 시점을 구분해서 답하세요.

Draft answer:
인천공항 제2터미널의 연면적은 개장 당시 약 53,157.68㎡였습니다. 최신 확장 후의 수치는 제공된 정보로는 확인할 수 없습니다. 최근 자료를 참조하시면 정확한 값을 얻을 수 있습니다.

Search evidence:
• [Tavily] Tavily AI 요약
  The Incheon International Airport Terminal 2 has a total floor area of 380,000 square meters. It opened on January 18, 2018. The terminal is designed to handle up to 52 million passengers annually.
  출처: 

• [Naver] 인천항 세관 통합검사장 신축사업
  68 제2절 예비타당성조사... 91 2. 인천항 시설현...
  출처: https://www.kdi.re.kr/file/download?atch_no=%2F3Ay2dvDRgPz2seBgvyyLg%3D%3D

• [Naver] 인천항 아암물류2단지 조성사업
  2016년도 예비타당성조사 보고서 인천항 아암물류2단지 조성사업 인천항 아암물류2단지 조성사업... 의뢰한 인천항 아암물류 단지 조성𰡔 사업𰡕 예비타당성조사의 최종보고서로 제출합니다 2016. 12....
  출처: https://www.kdi.re.kr/file/download?atch_no=J1HzkA7KWGVTrU4UA8rZwg%3D%3D

• [Naver] IFEZ - 인천경제자유구역청
  가발계획 2. 단지벌 주요 프로젝트 3 기빈시설 즈성 추진현황 제2설 영중공항도시 개발계획 빛 추신현황 1. 개발계획 1. 금 항 3. 기빈시설 조성 추진현황 3. 광역교농당 R E E E C N Z 0 N E 262 제5장...
  출처: https://www.ifez.go.kr/other/attach/process.file.do;JSESS=44622AD8EBF8D5CE6053EA246CB17E94?TP=dn&sn=61216&key=25067AEB45803AA

• [Naver] 國土海洋委員會會議錄 第 2 號(附錄) 國 會 事 務 處
  제303회-국토해양제2차(부록)(2011년10월26일) 1 第303回國會 (定期會) 國土海洋委員會會議錄 第 2 號(附錄) 國 會 事 務 處 日 時 2011年10月26日(水) 場 所 國土海洋委員會會議室 【서면질의․답변서】 (질의서)...
  출처: https://record.assembly.go.kr/assembly/mnts/apdix/apdixDownload.do?fileId=570575

• [Tavily] 인천국제공항 제2여객터미널(4단계) - 정림건축
  53,157,681.00m2
 ###### 연면적

  735,305.05m2
 ###### 건축면적

  265,478.19m2
 ###### 규모

  지하 2층, 지상 5층
 ###### 설계

  스마트 R&D BU
 ###### 컨소시엄

  삼우종합건축사사무소, 간삼건축사사무소, 나우건축사사무소
 ###### 참여

  최승환, 이효성, 정목조, 김명진, 강창희, 기현철, 김용재, 손혜경, 신승수, 신학섭, 이상현, 이영한, 이종효, 정재선, 조성원

인천국제공항 제2여객터미널 확장사업은 2001년 개항 이후 20여 년간
  출처: https://junglim.com/incheon-international-airport-t2-phase4

• [Tavily] 인천공항 제2의 개항 맞이
  3단계 사업의 핵심은 단일 건물로 2조3000억원이 투입된 제2여객터미널이다. 제2여객터미널은 체크인과 보안검색, 세관검사, 검역, 탑승 등 출입국을 위한 모든 절차가 제1여객터미널과 별도로 이뤄진다.  
　연면적 38만㎡로 롯데월드타워 32만㎡보다 큰 제2여객터미널은 철골재량만 7만4000여t으로 파리의 에펠탑 10개를 세울 수 있는 양이다. 지붕 면적은 16만2957㎡로 상암 월드컵경기장 전체 면적의 3배, 외장유리 면적도 9만7000㎡로 잠실야구장의 7배이다. 전선과 전력케이블은 2808㎞로 서울∼부산(456㎞)을 3회 왕복할
  출처: https://airport.khan.kr/entry/%EC%A0%9C2%EC%97%AC%EA%B0%9D%ED%84%B0%EB%AF%B8%EB%84%90-%EA%B0%9C%EC%9E%A5%E2%80%A6%EC%9D%B8%EC%B2%9C%EA%B3%B5%ED%95%AD-%EC%A0%9C2%EC%9D%98-%EA%B0%9C%ED%95%AD

• [Tavily] [르포 영상] 인천공항 2터미널, 양날개 달고 완전체로… “아름답고 편한 공항” | 한인포스트
  제2터미널 확장은 지난 2017년 말부터 총 4조8천억원을 투입해 7년간 진행한 ‘인천공항 4단계 건설사업’의 핵심이다. 4번째 활주로를 신설하고, 계류장 75곳을 추가해 늘어나는 항공 수요에 대응하고, 인천공항의 글로벌 허브 기능을 강화하기 위한 목적이다. 제4활주로는 2021년 6월 먼저 건설을 마쳤다.

제2터미널에는 터미널 북서쪽으로 각 750ｍ 길이의 ‘양 날개’가 달리면서 축구장 48개 크기, 연면적 34만㎡ 규모의 공간이 추가된다. 2018년 초 개항한 현재의 38만㎡ 규모에서 약 2배로 넓어지는 것이다.

확장 지역을
  출처: https://haninpost.com/archives/100637


## Q: 4단계 확장 포함하면 연면적은 얼마야? (2026-05-28 08:28:04)
- Source: search-assisted-qa
- Tags: qa,auto-collect,revit-addin,search-assisted,knowledge-candidate,needs-review

Status: needs-review

Question:
4단계 확장 포함하면 연면적은 얼마야?

Draft answer:
4단계 확장 포함하면 연면적 계산 시 계단 면적이 층마다 중복으로 반영됩니다. 예를 들어, 5㎡의 계단이 3층이라면 15㎡가 연면적으로 추가되겠죠. 베란다 확장을 고려해 계산해야 정확한 결과를 얻을 수 있습니다.

Search evidence:
• [Tavily] Tavily AI 요약
  The total floor area of the 4th phase expansion of Incheon International Airport is 735,305.05 square meters. The expansion includes the construction of a new runway and the extension of Terminal 2. The project was completed in October 2024.
  출처: 

• [Naver] 연면적 계산 어디서부터 포함이 될까
  설계 단계부터 정확한 연면적 계산이 정말 중요해요! 5. 실전 꿀팁 3가지 1. 계단·승강기 면적은 층마다 중복 포함돼요 : 계단 5㎡라도 3층이면 5×3=15㎡로 들어갑니다. 2. 베란다 확장 여부 꼭 체크하세요 : 확장된...
  출처: https://blog.naver.com/vkool5645/[LONG_ID_MASKED]

• [Naver] 건축법 내 도로법 '접도요건'
  「건축법」에서 대지란 토지 중에서 건축물을 건축할 수 있는 토지를 의미합니다. 즉, 모든 토지에 건축물을 건축할 수 있는 것이 아닙니다. 「건축법」은 그 목적에도 밝히고 있듯이 건축물을 건축할 수 있는 땅(대지)의 요건을 규정하고 있으며(※대지 참고) 그 요건에 부합하지 않으면 건축행위를 할 수 없습니다. 이를 대지의 접도요건이라고 부르며 「건축법」 제44조 ‘대지...
  출처: https://www.midascad.com/cad_archive/arhcitectrule-10

• [Naver] 「공유재산 및 물품 관리법 시행령」 개정 설명회(1.31. 대전시청).pdf
  사용되는 면적을 포함한다. &lt; 비 고 &gt; 1. 기준 면적은 해당 건축물의 연면적을 기준으로 계산하되, 다음... 4. 지방자치단체의 장은 제1호부터 제3호까지의 규정에도 불구하고 해당 지식재산의 사용료등을 산정할...
  출처: https://mois.go.kr/cmm/fms/FileDown.do?atchFileId=FILE_00074981JbuTp70&fileSn=0

• [Naver] 새만금 간척 사업
  2 )등을 포함하여 총 409km 2 면적(서울 면적의 2/3 규모)의 간척지를... 18선석, 4.8km 2 ) 및 남북․동서도로(총 43.57km) 등 기반시설... 산업연구용지 내에 새만금 산업단지가 일부 조성(1단계 총 18.5km 2 )되어 일본...
  출처: https://ko.wikipedia.org/wiki/%EC%83%88%EB%A7%8C%EA%B8%88_%EA%B0%84%EC%B2%99_%EC%82%AC%EC%97%85

• [Naver] [Who Is ?] 정민교 채비 대표이사
  보호예수와 단계적 매각 원칙을 약속했다. △공모자금 1093억, 충전 인프라·해외 거점·운영 안정화에 배분 채비는 상장으로 확보한 순유입 자금 1093억 원 가량을 충전 인프라 확장, 채비스테이 거점 구축, 해외...
  출처: https://www.businesspost.co.kr/BP?command=article_view&num=437550

• [Naver] 250억에 시작한 예배당 건축, 500억 됐는데…교인들 &quot;완공 뒤 알았다&quot;
  도림비전센터는 연면적 2만 4643㎡ 규모에 지하 5층, 지상 5층 크기 건물로, 본당에는 3000명을 수용할 수 있다.... 교인들은 건축 시작 당시 200억 원대가 들 거라는 얘기만 들었을 뿐 총 공사 비용이 얼마나 들었는지 알지...
  출처: https://www.newsnjoy.or.kr/news/articleView.html?idxno=400400

• [Naver] &quot;CDMO 글로벌 표준 도전장&quot;...BMI, 매출 1조 승부수 전략은
  겨냥한 연면적 7,476㎡의 CDMO 전초기지다. 한국비엠아이 제주공장이 기존 생산과 매출을 책임지는 안정적... 오송공장은 필요 시 추가 증축을 통해 배양 규모를 확장할 수 있는 구조적 여유를 갖추고 있어 임상 단계에...
  출처: https://www.pharmnews.com/news/articleView.html?idxno=301685


## Q: 인천공한 제2터미널 최신 연면적이 궁금해 (2026-05-28 08:28:32)
- Source: search-assisted-qa
- Tags: qa,auto-collect,revit-addin,search-assisted,knowledge-candidate,needs-review

Status: needs-review

Question:
인천공한 제2터미널 최신 연면적이 궁금해

Draft answer:
인천공항 제2여객터미널의 최신 연면적은 약 73.5만㎡입니다.

Search evidence:
• [Tavily] Tavily AI 요약
  The latest area of Incheon Airport's Terminal 2 is 73.5 square meters. It opened in January 2018 and expanded in December 2024. The expansion increased its capacity and facilities.
  출처: 

• [Naver] 인천공항 창업, 제2여객터미널 확장공사 준공 세계 3위 규모
  인천국제공항 제2여객터미널은 이번 4단계 공사를 통해 연면적 약 73.5만㎡, 연간수용능력 5,200만명... 공간과 최신 ICT 기술이 함께 조화를 이룬 터미널로 완성되었는데요. 이로써 인천공항은 225곳에서 동시에...
  출처: https://blog.naver.com/kdy_3879/[LONG_ID_MASKED]

• [Naver] (주)한화 건설부문, 인천공항 제2여객터미널 확장공사 준공… 앞선 기술력 선보여
  인천국제공항 제2여객터미널은 이번 4단계 공사를 통해 연면적 약... 인천국제공항의 건물 내부는 친환경 공간과 최신 ICT 기술이 함께... 시공한 동편은 한국의 전통 정원을 테마로 창덕궁 승재정을 재현했다....
  출처: http://www.ikld.kr/news/articleView.html?idxno=304579

• [Naver] ㈜한화 건설부문, 인천국제공항 제2여객터미널 확장 공사 준공
  인천국제공항 제2여객터미널은 이번 4단계 공사를 통해 연면적 약... 인천국제공항 건물 내부는 친환경 공간과 최신 정보통신기술(ICT)이... 시공한 동편은 한국의 전통 정원을 테마로 창덕궁 승재정을 재현했다....
  출처: http://www.newscape.co.kr/news/articleView.html?idxno=107826

• [Naver] 다락휴 | 인천공항 제2여객터미널
  인천공항 캡슐 호텔은 긴 여행에 지친 몸을 어우르며 편안한 휴식을 취할 수 있도록, 전통적인 인테리어 디자인에 독립된 공간에서 느낄 수 있는 안락함까지 모두 담았습니다.
  출처: https://www.walkerhill.com/darakhyu/t2/kr/about/Introduction.jsp

• [Tavily] 공항건설 - 인천국제공항공사
  단계별 주요 시설물 (1·2·3단계 계류장 및 기타시설물 표기 생략)

## 인천공항의 현재

인천공항의 현재 - 구분, 현재

     | 구분 | 현재 |
| 터미널 면적 | 제1 여객터미널 | 50.7만㎡ |
| 제2 여객터미널 | 73.5만㎡ |
| 탑승동 | 16.6만㎡ |
| 연간처리능력 | 여객 | 1억 600만명 |
| 화물 | 630만톤 |
| 운항 | 60만회 |
| 활주로 제원 | 제1·2활주로(1단계) | 3,750x60m |
| 제3활주로(2단계) | 4,000x60m |
| 제4활주로(4단계) | 3,750
  출처: https://www.airport.kr/co_ko/767/subview.do

• [Tavily] 인천국제공항 제2여객터미널 (r44 판) - 나무위키
  |  |  |
 --- |
| 층 | 제2여객터미널 |
| 일반구역 | 면세구역 |
| 5F | 인천공항 홍보전망대 
| 4F | 전문식당가, 항공사 사무실 | 라운지, 푸드코트 |
| 3F | 출국장 | 출국장 면세점, 탑승구 208~291, 직행셔틀 |
| 2F | 정부종합행정센터, 상주기관 사무실 | 도착게이트 |
| 1F | 입국장 | 입국장 면세점 |
| B1F | 전문식당가, 교통센터 통로 | 셔틀트레인 |

1. 개요2. 체크인 카운터3. 교통센터4. 은행, ATM, 환전소, 우체국5. 음식점, 카페, 편의점, 약국6.
  출처: https://namu.wiki/w/%EC%9D%B8%EC%B2%9C%EA%B5%AD%EC%A0%9C%EA%B3%B5%ED%95%AD%20%EC%A0%9C2%EC%97%AC%EA%B0%9D%ED%84%B0%EB%AF%B8%EB%84%90?uuid=8d480718-54ad-43e7-9ce3-8cd43ef5e9a0

• [Tavily] 어서 와, 인천국제공항 제2여객터미널(T2)은 처음이지?> 여행기사
  여행 마니아에게 최고의 음식은 기내식이다. 하늘에서 먹는 소박한 한 끼만큼이나 여행자를 들뜨게 하는 건 공항의 이국적인 공기다. 여행의 시작과 끝을 알리는 공항은 그 나라, 그 도시의 첫인상이기도 하다. 2001년 개항 이래 세계 공항서비스 평가에서 12년 연속 1위를 하며 세계인들에게 인정받은 인천국제공항이 2018년 제2여객터미널을 공식 개장했다. 2009년 공사에 착수한 지 9년 만에 문을 연 제2여객터미널은 아트포트(Artport·Art+Airport) 개념 의 엔터테인먼트 공간으로 꾸며져 볼거리, 즐길 거리가 가득하다. 더
  출처: https://korean.visitkorea.or.kr/detail/rem_detail.do?cotid=9cc5925e-575a-4350-a524-ab65322bd9cf


## Q: 인천공항 제2터미널 연면적은 얼마야? (2026-05-28 09:23:39)
- Source: telegram-qa
- Tags: qa,auto-collect

[📚 지식 베이스 (score 36) + 🔍 웹 검색 보강]

인천공항 제2터미널의 연면적은 약 38만 7000㎡입니다. 이는 서울 여의도공원 면적의 약 20배 규모입니다.


## Q: 인천공항 제2터미널 최신 여면적이 궁금했어 (2026-05-28 09:25:50)
- Source: telegram-qa
- Tags: qa,auto-collect

[📚 지식 베이스 (score 36) + 🔍 웹 검색 보강]

인천공항 제2터미널의 연면적은 약 40만㎡입니다. 이数值是基于提供的参考知识进行的翻译，但为了更准确地回答问题，我们可以进一步明确：

制2终端楼的建筑面积约为40万平方米。由于没有最新的扩展数据，这个面积应该是最近的数据。

如需最新数据，请查阅相关官方资料或更新的信息来源。


## Q: 한국어로 답변해줘 (2026-05-28 09:26:07)
- Source: telegram-qa
- Tags: qa,auto-collect

[🔍 웹 검색]

해당 참고 자료는 TikTok에서 'Whatismycursedontexplain'과 관련된 영상들을 탐색하는 내용으로 보입니다. 만약 이와 관련이 없다면, 좀 더 구체적인 질문이나 필요로 하는 정보를 알려주시면 도움을 드리겠습니다.


## Q: lua bim labs 첫번째 런칭한 상품 소개해줘 (2026-05-29 19:24:08)
- Source: telegram-qa
- Tags: qa,auto-collect

[📚 지식 베이스 (score 35) + 🔍 웹 검색 보강]

lua bim labs의 첫 번째 런칭 상품은 MEP BIM 전문 어시스턴트 기능입니다. 이 제품은 건설 및 인프라 프로젝트에서 MEP ( Mechanical, Electrical, Plumbing ) 설계를 위한 자동화된 도구들을 제공합니다. 이를 통해 엔지니어들은 시간과 노력을 줄이고, 정확도를 높일 수 있습니다.


## Q: 간섭검토를 진행할때 고려해야하는 사항에 대해서 공정별로 회피해야하는 기본적인 가이드라인 알려줘 (2026-06-06 15:06:43)
- Source: telegram-qa
- Tags: qa,auto-collect

[📚 지식 베이스 (score 16) + 🔍 웹 검색 보강]

간섭검토를 진행할 때 고려해야 하는 사항은 공정별로 다음과 같이 회피해야 합니다.

1. **건축공사**:
   - 건물의 지하 구조와 지상 구조 간 간섭을 확인합니다.
   - 주변 건축물과의 거리를 검토하여 법규를 준수합니다.

2. **도로공사**:
   - 도로와 건설 현장 사이의 안전거리를 확인합니다.
   - 교량이나 지하도와의 간섭을 점검합니다.

3. **철도공사**:
   - 철도와 건설 현장 간의 안전 거리를 검토합니다.
   - 지반 조건과 철로의 안정성을 확인합니다.

4. **수도공사**:
   - 수돗물 파이프와 건설 현장 간의 거리를 확인합니다.
   - 하천이나 저수지와의 관계를 점검하여 환경적 영향을 최소화합니다.

5. **가스공사**:
   - 가스 파이프와 건설 현장 간의 안전 거리를 검토합니다.
   - 주변 건물과의 거리 및 설치 방식을 확인하여 위험성을 평가합니다.

6. **전기공사**:
   - 전력선과 건설 현장 간의 거리를 확인합니다.
   - 지하 전선과의 간섭을 점검하여 안전성을 확보합니다.

이러한 사항들을 종합적으로 검토하고, 필요한 조치를 취함으로써 프로젝트의 성공적인 진행을 보장할 수 있습니다.


## 웹 보강: Autodesk Forma 초기 설계 환경분석 기능 활용법 (2026-06-14 08:45:07)
- Source: system-auto-quality-search
- Tags: auto-collect,needs-review

질문: Autodesk Forma 초기 설계 환경분석 기능 활용법

• [Naver] 🌇 Autodesk Forma 사용법 – AI 기반 도시 설계 시뮬레이션의 시작 - AI 건축연구소
  Autodesk Forma는 도시 설계와 초기 건축 분석을 위한 AI 기반 시뮬레이션 도구입니다. 채광, 음영, 바람 등 다양한 요소를 분석하고 Revit과 연동되는 Autodesk Forma 사용법과 주요 기능을 정리했습니다.
  출처: https://ai-archi.shinssblog.com/%F0%9F%8C%87-autodesk-forma-%EC%82%AC%EC%9A%A9%EB%B2%95-ai-%EA%B8%B0%EB%B0%98-%EB%8F%84%EC%8B%9C-%EC%84%A4%EA%B3%84-%EC%8B%9C%EB%AE%AC%EB%A0%88%EC%9D%B4%EC%85%98%EC%9D%98-%EC%8B%9C/

• [Naver] 건축에서 AI가 설계와 건설의 미래를 구현해 가는 방식
  건축에서 AI가 어떻게 설계와 건설의 변화를 주도하고, 효율, 혁신, 지속가능성을 촉진하는지 알아본다. 건축 및 건설에 AI를 도입할 때 발생하는 이점과 과제, 그리고 AI가 업계의 미래를 구현해가는 방식을 살펴본다.
  출처: https://www.autodesk.com/kr/design-make/articles/ai-in-architecture

• [Naver] [AUTODESK] 건축에서 AI가 설계와 건설의 미래를 구현해 가는 방식
  소비량 분석에 이르기까지 AI는 작업 흐름을 간소화하여 건축가가... AI의 기능을 활용한다. AI는 또한 더욱 몰입할 수 있고 상호작용할 수 있는 설계 경험을 제공하여 VR과 AR을 포함한 XR 기술을 혁신하고...
  출처: https://blog.naver.com/geosol77/223696131532

• [Naver] Autodesk AI | Design &amp; Make를 위한 인공 지능
  창의성 확대, 혁신 가속화 ; Design &amp; Make 산업의 고유한 과제를 해결하기 위해 개발된 Autodesk AI를 통해 고객은 업계의 요구와 기술 변화에 발빠르게 대응하며 포부와 창의성, 지속가능성을 실현할 수 있습니다.
  출처: https://www.autodesk.com/kr/solutions/autodesk-ai

검토 기준: 공식 문서 여부·최신성·프로젝트 적용성 확인 후 FAQ 승격.


## 웹 보강: 건축물 피난계단 직통계단 유효폭과 설치 기준 건축법 (2026-06-14 09:07:29)
- Source: system-auto-quality-search
- Tags: auto-collect,needs-review

질문: 건축물 피난계단 직통계단 유효폭과 설치 기준 건축법

• [Naver] 계단의 설치기준 (단높이, 단너비, 손잡이, 대체 경사로)
  건축계획에 있어 일반적으로 계단은 기능적 측면에서 다루어지며, 이것을 어떻게 설치할 것인가에 관한 문제는 전적으로 건축주와 설계자의 자유로운 판단에 의해 이루어집니다. 다만 연면적 200㎡를 초과하는 건축물에 설치하는 계단은 위험방지를 목적으로 「건축법」의 통제 대상이 됩니다.
  출처: https://www.midascad.com/cad_archive/buildingact-4

• [Naver] 직통계단과 피난계단 설치 기준, 예외 사항, 건축물 용도군!!
  직통계단은 건축물의 피난층을 제외한 모든 층에서 피난층 또는 지상으로 직접 연결되는 계단을 의미하며 이 계단은 건축물의 아래위층을 수직으로 관통하여 연결되고, 복도나 거실 등을 거치지 않게 대피할 수 있는 것을 말해요. 피난계단은 재난 발생 시 안전하게 대피할 수 있도록 설계된 계단으로, 출입구에 방화문이 설치되어 있으며 주로 5층 이상 또는 지하 2...
  출처: https://goldmoneyblog.co.kr/%EC%A7%81%ED%86%B5%EA%B3%84%EB%8B%A8%EA%B3%BC-%ED%94%BC%EB%82%9C%EA%B3%84%EB%8B%A8-%EC%84%A4%EC%B9%98-%EA%B8%B0%EC%A4%80-%EC%98%88%EC%99%B8-%EC%82%AC%ED%95%AD-%EA%B1%B4%EC%B6%95%EB%AC%BC/

• [Naver] 건축물 계단 관련 법규 총정리 (공동주택·근린생활시설·업무시설 등) --상세
  제한됨) 건축법 시행령 제34조(직통계단의 설치): 피난층(지상 출입구가 있는 층 또는 초고층건축물의 피난안전구역을 제외한 모든 층은... 넘는 계단은 높이 3m 이내마다 유효폭 1.2m 이상의 계단참(수평 descanso)을...
  출처: https://blog.naver.com/jenna2034/223879172324

• [Naver] 주택성능등급인정 시 직통계단일때도 피난계단 유효폭 규정을 적용_2011.09.28
  ■ 질의 ⇒ 주택성능등급 인정 및 관리기준에서 5.화재소방등급 중 (2)피난안전등급의 2)복도 및 계단 유효폭의 등급기준에서 건축법 규정에 따른 계단실 출입구 및 복도의 유효폭 확보라 함은 출입구 규정에서 계단이 피난계단이나 특별피난계단이 아닌 직통계단일 경우도 계단실 출입문의 유효폭이 0.9m 이상이어야 하는지요? [1개에 3950원이 부담이 되시나...
  출처: https://qnaqc.co.kr/product/2011-09-28_%EC%A3%BC%ED%83%9D%EC%84%B1%EB%8A%A5%EB%93%B1%EA%B8%89%EC%9D%B8%EC%A0%95-%EC%8B%9C-%EC%A7%81%ED%86%B5%EA%B3%84%EB%8B%A8%EC%9D%BC%EB%95%8C%EB%8F%84-%ED%94%BC%EB%82%9C%EA%B3%84%EB%8B%A8/

• [Naver] &quot;은평 폐기물 처리시설 지으려는 서울시 부당성 알리겠다&quot;
  의원 = 건축법 시행령 제46조에 따라 아파트로 4층 이상인 층의 각 세대가 2개 이상의 직통계단을 사용할 수 없는 경우, 발코니에 대피공간을 설치해야 한다. 다만, 경계벽을 경량구조로 설치하거나, 경계벽에 피난구를...
  출처: http://www.mygoyang.com/news/articleView.html?idxno=40773

검토 기준: 공식 문서·최신성·적용성 확인 후 FAQ 승격.


## 웹 보강: BIM 소프트웨어 해외진출 현지화 우선순위 결정 (2026-06-14 16:18:38)
- Source: system-auto-quality-search
- Tags: auto-collect,needs-review

질문: BIM 소프트웨어 해외진출 현지화 우선순위 결정

• [DDG] oma-fse-group/Evac4Bim - GitHub
  A Revit add-in that improves the integration of Fire Evacuation into te BIM worklfow. This add-in was developed as part of a master thesis and in partial fulfilment of the requirements for the degree of The International Master of Science in Fire Safety Engineering (IMFSE).
  출처: https://github.com/oma-fse-group/Evac4BIM

• [DDG] Naviate Bimfire
  Fire Safety information directly in the BIM model Bimfire is made for Fire Safety Engineers to work directly in Revit. It enables you to transmit data from your Fire Safety models to the other collaborators in a building project. Instead of writing documentation and redlining Fire Safety drawings on
  출처: https://www.naviate.com/naviate-for-revit/naviate-bimfire/

• [DDG] Naviate Bimfire - Make BIM Easy
  A Revit plugin for fire safety design, Bimfire lets fire safety information integrate directly into the BIM process for a digital workflow. Intuitive and easy to get going, with immediate results in ongoing projects.
  출처: https://www.bimfiretools.com/

• [DDG] Clearance Zones in Revit - Kinship Blog
  Improve your design, coordination and clash detection with our recommended workflow for incorporating clearance zones into your Revit families.
  출처: https://kinship.io/blog/clearance-zones-in-revit

• [DDG] Revit add ins, add ons, and plugins for many purposes
  Revit is powerful out of the box - but the right addins can transform your workflow. This guide covers the best Revit plugins and add-ons for architecture, MEP, and structural teams, including options for automation, rendering, coordination, and clash detection.
  출처: https://revizto.com/resources/blog/revit-addins-addons-plugins

검토 기준: 공식 문서·최신성·적용성 확인 후 FAQ 승격.


## 웹 보강: 건축물 내진설계 횡력저항시스템 (2026-06-14 21:36:54)
- Source: system-auto-quality-search
- Tags: auto-collect,needs-review

질문: 건축물 내진설계 횡력저항시스템

• [Naver] 건축물 내진설계 기준
  1.2 용어의 정의 ·가새골조：횡력에 저항하기 위하여 건물골조방식 또는 이중골조방식에서 중심형 또는 편심형의 수직트러스 또는 이와 동등한 구성체. ·감쇠 : 점성, 소성 또는 마찰에 의해 구조물에 입력된 동적 에너지가 소산되어 구조물의 진동이 감소하는 현상 ·감쇠시스템：개별 감쇠장치 및 그로부터 구조물의 기초와 지진력저항시스템에 하중을 전달하는 구조요소 또...
  출처: https://www.kcsc.re.kr/standardCode/viewer/KDS%2041%2017%2000:2022-10-11

• [DDG] PDF 건축물 내진설계기준
  1.1 (1) 이 기준은 건축법과 주택법에 따라 건축하거나 대수선 및 유지·관리하는 건축물 및 건물외구 조물의 구조체와 부구조체 및 비구조요소의 내진설계에 적용�. 1.2 가새골조 횡력에 저항하기 위하여 건물골조방식 또는 이중골조방식에서 중심형 또는 ∙:편심형의 수직트러스 또는 이와 동등한 구�. 체 . 감쇠 점성 소성 또는 마찰에 의해 구조물에 입력된 동적 에너지가 소산되어 구조물 ∙ : , 의 진동이 감소하는 현상 감쇠시스템 개별 감쇠장치 및 그로부터 구조물의 기초와 지진력저항시스템에 하중을 ∙:전달하는 구조요소 또는 가새 등을
  출처: https://www.kim2kie.com/res/html/0_formula/00%20Dynamics/KDS%2041/KDS%2041%2017%2000.pdf

• [Naver] [내진] 건축물의 지진력저항시스템
  25%를 저항할 수 있어야 한다. 6.2.7 강구조기준의 일반규정만을 만족하는 철골구조시스템 (1) KDS 41 31 00 건축물 강구조 설계기준에서 4.10 강구조의 내진설계와 4.11 합성구조의 내진설계을 제외한 나머지 규정을...
  출처: https://blog.naver.com/ssssenc/223815191732

• [DDG] 국가건설기준센터 (Kcsc)
  선택코드번호코드명대분류중분류개정이력 별 내용보기최종 제‧개정일관련단체다운로드 KDS 41 17 00 건축물 내진설계기준 건축 구조기준 건축물 내진설계기준 2019 2022
  출처: https://www.kcsc.re.kr/standardCode/list/10204117

• [Naver] 건축물 내진설계기준 KDS 41 17 00 : 2022
  따라 건축하거나 대수선 및 유지·관리하는 건축물 및 건물외구조물의 구조체와 부구조체 및 비구조요소의 내진설계에 적용한다. 1.2 용어의 정의 가새골조：횡력에 저항하기 위하여 건물골조방식 또는...
  출처: https://blog.naver.com/ksjin0212/223147167217

• [DDG] 건축물 내진설계기준 Kds 41 17 00 : 2022 - 네이버 블로그
  (1) 이 기준은 건축법과 주택법에 따라 건축하거나 대수선 및 유지·관리하는 건축물 및 건물외구조물의 구조체와 부구조체 및 비구조요소의 내진설계에 적용한다. 가새골조：횡력에 저항하기 위하여 건물골조방식 또는 이중골조방식에서 중심형 또는 편심형의 수직트러스 또는 이와 동등한 구성체. 감쇠시스템：개별 감쇠장치 및 그로부터 구조물의 기초와 지진력저항시스템에 하중을 전달하는 구조요소 또는 가새 등을 모두 포함하는 구조체. 감쇠장치：감쇠시스템의 일부로서 장치 양 단부의 상대적 움직임에 따라 에너지를 소산시키는 유연한 구조요소.
  출처: https://m.blog.naver.com/ksjin0212/223147167217

• [Naver] 🏢 빌딩의 횡력 저항 구조 시스템 완전정복
  안녕! 오늘은 우리가 매일 드나드는 고층 빌딩들이 어떻게 바람과 지진 같은 횡력(옆으로 미는 힘)에 버티는지 알아볼 거야. 🌪️ 솔직히 건물 설계할 때 가장 머리 아픈 부분 중 하나가 바로 이 횡력 저항 시스템이거든. 특히 상업용 빌딩이나 업무용 건물처럼 높이 올라가는 구조물일수록 더더욱 중요해지지. 생각해봐. 100층짜리 빌딩이 강풍에 흔들린다면? 😱 상상만 해도 아찔...
  출처: https://www.jaenung.net/tree/38840

검토 기준: 공식문서·최신성·적용성 확인 후 FAQ 승격.


## 웹 보강: 건축물 피뢰설비 보호각 기준 (2026-06-14 21:36:58)
- Source: system-auto-quality-search
- Tags: auto-collect,needs-review

질문: 건축물 피뢰설비 보호각 기준

• [Naver] 건축물 등의 피뢰설비 설치에 관한 기술지침
  KOSHA GUIDE E - 107 - 2011 건축물 등의 피뢰설비 설치에 관한 기술지침 2011. 12. 한국산업안전보건공단... 2 수뢰부의 배치 (1) 수뢰부의 배치는 구조물의 형상에 따라 &lt;표 1&gt;에 나타낸 보호각, 회전구체...
  출처: https://oshri.kosha.or.kr/extappKosha/kosha/guidance/fileDownload.do?sfhlhTchnlgyManualNo=E-107-2011&fileOrdrNo=3

• [DDG] 건축물의 설비기준 등에 관한 규칙 - 국가법령정보센터
  측면 낙뢰를 방지하기 위하여 높이가 60미터를 초과하는 건축물 등에는 지면에서 건축물 높이의 5분의 4가 되는 지점부터 최상단부분까지의 측면에 수뢰부를 설치하여야 하며, 지표레벨에서 최상단부의 높이가 150미터를 초과하는 건축물은 120미터 지점 ...
  출처: https://law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B1%B4%EC%B6%95%EB%AC%BC%EC%9D%98%EC%84%A4%EB%B9%84%EA%B8%B0%EC%A4%80%EB%93%B1%EC%97%90%EA%B4%80%ED%95%9C%EA%B7%9C%EC%B9%99/%EC%A0%9C20%EC%A1%B0

• [Naver] 한국전기설비규정(KEC) 정리 - 피뢰시스템
  01. 피뢰시스템의 적용범위 및 구성 01-1. 피뢰시스템 01-2. 외부피뢰시스템 01-3. 인하도선 시스템 01-4. 접지극 시스템 01-5. 부품 및 접속 01-6. 옥외에 시설된 전기설비의 피뢰시스템 02.내부피뢰시스템 02-1.전기전자설비 보호 02-2. 피뢰등전위본딩 [적용범위] 본 규정은 아래에 제시된 곳에 설치하는 피뢰시스템에 적용합니다. 가) 낙뢰로부터 보호가 필요한 전기전자설비가 설치된 건축...
  출처: https://www.midascad.com/cad_archive/electricity-cad-kec-5

• [DDG] 피뢰설비 설치관련 기준과 규정 (보호각, 회전구체, 자연부재 ...
  한편 「한국공업규격 KS C 9609 (피뢰침) - 1985.12.4」와 「건축물의 설비기준에 관한 규칙-2001.1.17」에 따르면 피뢰침의 보호각은 60°이하를 권장하고 있으며, 화약·가연성 액체·가연성 가스를 보호하기 위한 피뢰침의 각도는 45°로 규정하고 있다. 2. 회전구체법
  출처: https://m.blog.naver.com/kimih2917/221398870557

• [Naver] 건축물 등의 피뢰설비 설치에 관한 기술지침(KOSHA GUIDE) - 2011.12
  E - 107 - 2011 건축물 등의 피뢰설비 설치에 관한 기술지침 1. 목 적 이 지침은 산업안전보건기준에... 2 수뢰부의 배치 (1) 수뢰부의 배치는 구조물의 형상에 따라 &lt;표 1&gt;에 나타낸 보호각, 회전구체...
  출처: https://blog.naver.com/summitsec/222593557796

• [DDG] 피뢰설비 (Lightning Protection System)의 등급 / 피뢰설비의 시공방법
  일반건축물의 경우 60°이하, 위험물저장,제조,취급하는 건축물의 보호각은 45°이하로 규정되어 있다. 2) 국제규격 (IEC : Internatinal Electrotechnical Commission/ TC 81, NFMA 78, BS 6651.) 건축물의 높이에 따라 보호각의 범위가 달라지며, 회전구체법이나 메시법에만 적용한다. 뇌격거리 R은 대지로부터 하강리더를 향해서 발생하는 상승리더의 거리를 말하며, 이 거리는 뇌전류의 크기에 의해서 결정되고 개략 100m정도이다. (미국에서는 45m 회전구체법을 적용하도록 규정하고 있다.
  출처: https://electriceng.tistory.com/800

• [Naver] 건축물 등의 피뢰설비 설치에 관한 기술지침
  [건축물 등의 피뢰설비 설치에 관한 기술지침] 2011.12 - 한국산업안전보공단 ㅇ개정자... 2 수뢰부의 배치 (1) 수뢰부의 배치는 구조물의 형상에 따라 &lt;표 1&gt;에 나타낸 보호각, 회전구체, 메시 치수등을...
  출처: https://blog.naver.com/elec0610/221060064729

검토 기준: 공식문서·최신성·적용성 확인 후 FAQ 승격.


## 웹 보강: 출입통제 시스템 BIM 연동 (2026-06-14 21:36:59)
- Source: system-auto-quality-search
- Tags: auto-collect,needs-review

질문: 출입통제 시스템 BIM 연동

• [Naver] 논문집 - 사단법인 한국건축시공학회
  스마트노드 시스템의 적용 사례 6 나상호·이장현·박영미·김성진 FCP(Free-form Concrete Panel)... structure in the coating-sheet composite waterproofing method 최 성 민 * 1) 오 상 근 ** 박 진 상 *** 김 동 범...
  출처: https://kic.or.kr/wp/2021a/data/2021%20%EB%B4%84%ED%95%99%EC%88%A0%EB%B0%9C%ED%91%9C%EC%A7%91.pdf

• [DDG] Naviate Bimfire
  Fire Safety information directly in the BIM model Bimfire is made for Fire Safety Engineers to work directly in Revit. It enables you to transmit data from your Fire Safety models to the other collaborators in a building project. Instead of writing documentation and redlining Fire Safety drawings on
  출처: https://www.naviate.com/naviate-for-revit/naviate-bimfire/

• [Naver] 한국방재학회 학술발표대회
  Test Plan on Complex Seismic Damage of a Ceiling System Caused by Interactions... Components in Full-Scale Shake Table Testing of a 10-Story Steel Building 73... 근현기 BIM 기반 칠도터널 유지관리 시스템 구축을 위한 설계요소 및...
  출처: https://www.kosham.or.kr/html/?pmode=BBBS0010400001&smode=ajax&fn=fileDownload&seq=4810&bseq=1107&fnm=2025102115065868f72302ed49c

• [DDG] oma-fse-group/Evac4Bim - GitHub
  A Revit add-in that improves the integration of Fire Evacuation into te BIM worklfow. This add-in was developed as part of a master thesis and in partial fulfilment of the requirements for the degree of The International Master of Science in Fire Safety Engineering (IMFSE).
  출처: https://github.com/oma-fse-group/Evac4BIM

• [DDG] Naviate Bimfire - Make BIM Easy
  A Revit plugin for fire safety design, Bimfire lets fire safety information integrate directly into the BIM process for a digital workflow. Intuitive and easy to get going, with immediate results in ongoing projects.
  출처: https://www.bimfiretools.com/

• [DDG] Features in Naviate Bimfire
  Naviate Bimfire Features Integrate fire safty information directly in your Revit model. Easier, faster, safer.
  출처: https://www.naviate.com/naviate-for-revit/naviate-bimfire/features/

• [DDG] BIM objects - Free download! Revit Fire Products | BIMobject
  Download and search for Revit fire products. Browse through BIMobject&#x27;s curated library of manufacturer-specific products to research and select which Revit fire products to use in your project. Whether you&#x27;re looking for something for a particular market, BIM software, or brand you can fi
  출처: https://www.bimobject.com/en/categories/fire-products?software=revit

검토 기준: 공식문서·최신성·적용성 확인 후 FAQ 승격.


## 웹 보강: 건축물 피뢰설비 보호각 회전구체법 (2026-06-15 20:47:11)
- Source: system-auto-quality-search
- Tags: auto-collect,needs-review

질문: 건축물 피뢰설비 보호각 회전구체법

• [Naver] 건축물 등의 피뢰설비 설치에 관한 기술지침
  KOSHA GUIDE E - 107 - 2011 건축물 등의 피뢰설비 설치에 관한 기술지침... 하며, 보호대상 건축물의 표면이 평평한 경우에 적합하다. &lt;그림 1&gt; 보호각법의 보호범위 &lt;그림 2&gt; 회전구체법의 보호범위 KOSHA
  출처: https://oshri.kosha.or.kr/extappKosha/kosha/guidance/fileDownload.do?sfhlhTchnlgyManualNo=E-107-2011&fileOrdrNo=3

• [DDG] 한국전기설비규정 Kec 152 외부피뢰시스템 회전구체 보호각
  안녕하세요. 사이비교수입니다. 이번시간에는 외부피뢰시스템의 회전구체법과 보호각법에 대해서 공부하겠습니다. 외부피뢰시스템은 건축물이 번개를 직격뢰를 맞아서 대지로 흘려보내기 위해서 적용합니다.
  출처: https://cyberprofessor.tistory.com/entry/%ED%95%9C%EA%B5%AD%EC%A0%84%EA%B8%B0%EC%84%A4%EB%B9%84%EA%B7%9C%EC%A0%95-KEC-152-%EC%99%B8%EB%B6%80%ED%94%BC%EB%A2%B0%EC%8B%9C%EC%8A%A4%ED%85%9C-%ED%9A%8C%EC%A0%84%EA%B5%AC%EC%B2%B4-%EB%B3%B4%ED%98%B8%EA%B0%81

• [Naver] 한국전기설비규정(KEC) 정리 - 피뢰시스템
  ● 수평도체 : 건축물 보호 및 회전구체에 의하여 구획되어지는 하부 시설물 보호를 말한다, ● 돌침형 피뢰침 : 건축물의 상부에 설치되는 시설물을 보호하는 역할을 한다.(예시 : 안테나, 에어컨 냉각탑, 에어컨 실외기, 태양광전지판 등) 나) 수뢰부시스템을 구성하는 재료는 아래의 자료를 내용에 따라 선정하여야 합니다. ● KS C IEC 62305-3(피뢰시스템-제3부:구조물의 물리적 손...
  출처: https://www.midascad.com/cad_archive/electricity-cad-kec-5

• [DDG] 피뢰설비 설치관련 기준과 규정 (보호각, 회전구체, 자연부재 ...
  그림 5-2에 나타낸 바와 같이 뇌격거리와 동등한 반경의 가상구를 건축물에 회전시킬 때 접촉하는 모든 점에 피뢰침을 설치하도록 요구하는 방법이다. 즉, 보호영역은 뇌격거리 R을 반경으로 하는 구를 돌출물 (피뢰도체)에 접하게 했을 때 구내부로 노출되지 않는 공간이다. 이와 같이 RSM을 적용할 때는 구가 놓일 수 있는 가능한 모든 위치가 고려되어야 한다. 일률적으로 보호각을 적용하는 보호각법과는 달리 회전구체법은 1970년대부터 적용되기 시작한 방법으로 최근 선진 각국에서는 과학적인 타당성이 입증된 회전구체법이 널리 사용되고 있다.
  출처: https://m.blog.naver.com/kimih2917/221398870557

• [Naver] 피뢰설비의 등급 / 피뢰설비의 시공방법
  이하의 건축물에 자주적인 피뢰설비를 실시할 때 이용하는... 의한 피뢰침의 보호각(회전구체법과 메시법에 적용한다) 3) 회전구체법... 1-2) 돌침지지관,지지철물 및 설치대 돌침부는 건축법에서 규정한...
  출처: https://blog.naver.com/zeratuss/222944176167

• [DDG] 한국전기설비규정 (Kec) 정리 - 피뢰시스템 - 마이다스캐드
  돌침, 수평도체, 메시도체의 요소 중 한 가지를 선택하거나 이들을 조합하여 설치하여야 합니다. 수평도체 : 건축물 보호 및 회전구체에 의하여 구획되어지는 하부 시설물 보호를 말한다, 돌침형 피뢰침 : 건축물의 상부에 설치되는 시설물을 보호하는 역할을 한다.
  출처: https://www.midascad.com/cad_archive/electricity-cad-kec-5

• [Naver] 피뢰설비 설치대상과 설치기준 알아보기 | 하다
  낙뢰는 인명 피해뿐만 아니라 건축물 파손, 화재, 정전 등 2차 피해를 유발할 수 있는 위험 요소입니다. 이에 각종 법률과 안전보건규칙에서는 낙뢰로 인한 재해를 예방하기 위해 건축물에 피뢰설비를 설치하도록 규정하고 있습니다. 이번 글에서는 피뢰설비의 개념과 종류, 설치대상 및 설치기준에 대해 자세히 알아보겠습니다. 피뢰설비란 낙뢰로부터 특정 공간을 보호하고, 2차...
  출처: https://www.hadaworks.com/blog-insight/lightning-protection-system-installation-requirements-standards

검토: 공식문서·최신성·적용성 확인 후 FAQ 승격.
