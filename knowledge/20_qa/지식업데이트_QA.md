

## Telegram 팀원 보강 요청 (2026-06-06 15:07:03)
- Source: telegram:@FreeFilmer (7899169126)
- Tags: telegram,team-request,knowledge-gap,kst02-review

팀원이 기존 Obsidian 답변이 부족하다고 회신했다.

원 질문: 간섭검토를 진행할때 고려해야하는 사항에 대해서 공정별로 회피해야하는 기본적인 가이드라인 알려줘
추가 요청: 추가 설명 없음

처리 기준:
1. 내부 지식에서 누락된 기준을 우선 보강한다.
2. 외부 검색 또는 공식 문서 확인이 필요한 항목은 자동 수집 후 지식 업데이트 후보로 표시한다.
3. 고객명, 프로젝트명, 개인정보는 수집하지 않는다.

## 2026-06-20 지식업데이트 검색 노이즈/경험 승격 실무 케이스 Q&A
- Source: `knowledge/40_curation/quality/2026-06-20_ALL_AGENTS_PRACTICAL_CASE_LIBRARY.md`
- Tags: knowledge-update,field-case,search-noise,promotion,kst,qa,2026

**Q: 자동 검색 결과가 많지만 질문과 맞지 않는 자료가 섞이면 어떻게 하나요?**
A: 검색 결과를 바로 지식으로 승격하지 않는다. 공식성, 최신성, 질문 적합성, 프로젝트 적용 가능성으로 등급화하고, 엉뚱한 결과는 노이즈로 기록한다. 특히 제품 매뉴얼, 블로그, 특허, 포럼이 섞이면 확정 지식과 참고 지식을 분리한다.


실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `지식업데이트` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.
**Q: 팀원이 "답변이 부족하다"고 했을 때 바로 웹 검색부터 하나요?**
A: 먼저 내부 KB에서 누락된 기준과 질문 의도를 확인한다. 외부 검색은 공식 기준이나 최신 정보가 필요한 경우에 사용하고, 수집 후보 결과는 KST04로 저장한다. 반복되는 부족 질문은 담당 QA로 승격한다.


## Telegram 더 찾아줘 수집 후보 결과 (2026-06-06 15:07:04)
- Source: telegram-search-candidate:@FreeFilmer (7899169126)
- Tags: telegram,team-request,kst04-collected-review,kst02-review

원 질문: 간섭검토를 진행할때 고려해야하는 사항에 대해서 공정별로 회피해야하는 기본적인 가이드라인 알려줘
추가 요청: 추가 설명 없음

수집 후보 결과:

• Tavily evidence Tavily AI 요약
  To avoid interference, construction phases should consider coordination between different trades, review design changes, and manage construction sequences. Key steps include regular meetings, design reviews, and conflict checks between different construction phases.
  출처: 

• [Naver] 시·도 조례에 따른 환경영향평가 안내서
  위한 기본적인 사항과 환경영향평가 단계에서의 검토 방법· 및 내용 등을 수록하였습니다.... 지침 등을 고려하여 탄력적으로 적용 하는 것이 바람직합니다. 차 / 례 / 제 편 환경영향평가 제도 개요1...
  source-url: https://www.eia-career.or.kr/cmm/fms/FileDown.do?atchFileId=FILE_000000000222221&fileSn=0

• [Naver] CNS TODAY 제1호 정책정보 상세보기
  종합발전 기본계획 분석 정부는 1980년대부터 항행안전시설 중장기 확충방안 을 수립하는 등의 지속적인 시설확충, 신설계획을 마련... 또한, 일본은 기본적으로 미국의 NextGen 프로젝트, ICAO의 ATM...
  source-url: https://www.molit.go.kr/USR/policyData/m_34681/dtl.jsp?id=3800

• [Naver] 우리나라 수용법제에 대한 법경제학적 검토
  법경제학적 검토 2013년도 정책연구 보고서 2013년도 정책연구 보고서 우리나라 수용법제에 대한 법경제학적 검토 2013. 12. 공 공 투 자... 법경제학적 검토 KDI 연구진 : 이호준 연구위원 - 연구총괄 홍성필...
  source-url: https://www.kdi.re.kr/file/download?atch_no=DFTQuuN9hKweatdV6kYO1Q%3D%3D

• [Naver] 공정거래법 위반 행위로 받게 되는 제재의 종류 및 내용 1 _ 독과점행위, 불공정거래행위, 부당공동행위, 재판매....
  보호하는 동시에 국민 경제의 균형 있는 발전을 도모하는 데 목적을 두고 있으며, 독과점화 규제, 불공정 거래 규제, 경쟁 제한 행위의 규제 등 경쟁정책 외 다양한 정책을 두고 있습니다. 관련 법의 위반에 대해서는...
  source-url: https://blog.naver.com/lawfluencer/222663928988

• Tavily evidence [PDF] 건설산업 BIM 시행지침 _시공자 편
  그림 4 BIM 수행계획서 작성 절차 [출처: BEP Guide & Templates – Version 2.2, 2019] 32 건설산업 BIM 시행지침_시공자 편 표 2 BIM 수행계획서 세부구성 항목 예시 구분 내용 BIM 과업 개요 과업의 기본 정보, BIM 목표 및 활용 등에 대한 개요 명시 BIM 업무 범위 계획수립 BIM 업무수행 범위, BIM 업무 일정계획, 작성대상 및 수준 등에 대한 계획 명시 실제 시공 일정과 BIM 검토완료 시기에 대한 구체적 계획 명시 BIM 수행 조직 계획수립 BIM 업무수행 조직 편성, 조직
  source-url: https://damassets.autodesk.net/content/dam/autodesk/www/pdf/construction-bim-implementation-guide-for-operator-final.pdf

• Tavily evidence [PDF] 철도 BIM 적용지침 - 빌딩스마트협회
  [그림 1-1] BIM의 구성 및 활용 철도 BIM 적용지침 - 2 -1.1.2 철도분야 BIM 적용 기대효과 ・철도사업의 특성상 여러 분야의 시설물(노반, 건축, 설비, 궤도, 전차선, 신호통신 등)을 분리하여 단계별 설계 및 시공함에 따라 각 분야 간의 인터페이스 및 간섭사항, 선후 공정관리 등의 세부 검토가 필요하다. [...] ・[표 1-1]와 같이 철도에 BIM(3차원 도면에 설계정보가 포함된 통합모델 기반의 업무방식) 을 도입하게 되면, 전 분야의 시설물 도면을 3차원 모델로 작성하여 직관적인 설계오류 검토 및 타 분야와
  source-url: https://buildingsmart.or.kr/NewsFile/%EC%A7%80%EC%B9%A8/KR/%EB%B6%99%EC%9E%841.%20%EC%B2%A0%EB%8F%84%20BIM%20%EC%A0%81%EC%9A%A9%EC%A7%80%EC%B9%A8.pdf

• Tavily evidence 행정규칙 > 건설공사 사업관리방식 검토기준 및 업무수행지침
  2. 설계조직 간의 조직적 및 기술적 연계성을 확립하고, 필요한 설계정보가 문서화되고 정기적으로 검토되기 위해서 필요한 경우 정기적인 검토회의를 개최해야 하며, 설계조직 간의 체계도를 작성하여 관리

3. 실시설계업무 협조 및 조정

4. 실시설계 업무의 연계성 검토, 발주청 지원

5. 공종 간 간섭사항 검토

② 건설사업관리기술인은 실시설계단계에서 공사비가 타당한 사유로 예산을 초과해야 할 경우, 발주청으로 하여금 설계용역을 중지하거나 진행하면서 총사업비 증액조정업무를 처리하도록 하여야 한다.

③ 건설사업관리기술인은 견적방법 
  source-url: https://www.law.go.kr/LSW//admRulInfoP.do?admRulSeq=2100000256028&chrClsCd=010201

검토 기준: 공식 문서 여부, 최신성, 프로젝트 적용 가능성, 보안/개인정보 포함 여부를 확인한 뒤 표준/교육/FAQ 후보로 승격한다.


## Telegram 팀원 보강 요청 (2026-06-18 07:04:24)
- Source: telegram:@FreeFilmer (7899169126)
- Tags: telegram,team-request,knowledge-gap,kst02-review

팀원이 기존 Obsidian 답변이 부족하다고 회신했다.

원 질문: 냉동기 장비에 연결되는 어샘블리 밸브 순서가 어떻게 될까?
추가 요청: 추가 설명 없음

처리 기준:
1. 내부 지식에서 누락된 기준을 우선 보강한다.
2. 외부 검색 또는 공식 문서 확인이 필요한 항목은 자동 수집 후 지식 업데이트 후보로 표시한다.
3. 고객명, 프로젝트명, 개인정보는 수집하지 않는다.


## Telegram 더 찾아줘 수집 후보 결과 (2026-06-18 07:04:25)
- Source: telegram-search-candidate:@FreeFilmer (7899169126)
- Tags: telegram,team-request,kst04-collected-review,kst02-review

원 질문: 냉동기 장비에 연결되는 어샘블리 밸브 순서가 어떻게 될까?
추가 요청: 추가 설명 없음

수집 후보 결과:

• [Naver] 1286772055_1.pdf_x
  냉장고에 수도관이 연결되어 있지 않거나 연결되어 있는 수도관 얼음 디스펜서가 제대로 작동하지 않을 경우 이 잠겨 있을 경우?냉장고에 수도관이 연결되고 밸브가 열려 있는지를 냉동실 문이 제대로 닫히지 않은...
  source-url: http://www.whirlpoolkorea.net/shop/board_data/bbs_pdata/1286772055_1.pdf_x

• DDG evidence 냉동기 배관의 이해(부속장치 명칭 및 용어 설명) - 네이버 블로그
  다량의 기포가 보일 경우 : 냉매 부족, 여과기가 필터가 막힘. 응축 온도가 낮음. 고장 수리 등에 대비하여 바이패스 관음 설치할 수도 있다.
  source-url: https://m.blog.naver.com/raykdk/222432730719

• [Naver] 공조 필답 이론 해설
  전자밸브 ; 전자기력 이용해 입력신호 따라 전기회로 온오프 ; 기계적 트랩으로 포화수와 증기의 비중차를 이용해 응축수 배출 ; 도통시험
  source-url: https://www.moducbt.com/exam/solution/8225

• DDG evidence 냉동기 관련 밸브 개요 : 네이버 블로그
  응축온도가 내려가 사이클 내 충분한 압력을 형성할 수 없을 때, 핫가스를 수액기로 보내 액냉매를 증발시켜 압력을 형성하는 밸브 SV (Solenoid Valve) 1. SV1와 SV2가 닫힐 경우 : 펌프다운 2. SV1만 열릴경우 : 냉동사이클 3. SV2만 열릴경우 : 핫가스 제상 TXV ...
  source-url: https://blog.naver.com/PostView.naver?blogId=hvackkw&amp;logNo=220524231904

• [Naver] [특허]냉동시스템의 냉매팽창 장치와 냉매체적 제어 방법
  피스톤(43)은 냉매가 반대방향으로 유동할때, 솔레노이드 밸브장치(48)주위의 최소 바이패스 유량을 제공하도록 유량을 계측 유동시키고, 유동방향이 역전되면, 유동로(44)를 통한 유량에 아무런 제약도 가하지 않게 된다. 또한, 솔레노이드 밸브(48)는 냉매에 열을 전달하기 위한 열전달 코일을 구비하는 형식의 냉동시스템에 쓰이는 냉매팽창장치에 있어서, 상기 냉매를 증발기 코...
  source-url: https://scienceon.kisti.re.kr/srch/selectPORSrchPatent.do?cn=KOR1019870012199

• DDG evidence 냉동용 밸브의 종류와 특징
  냉동 시스템에서 적절한 밸브 선택은 시스템의 효율성과 신뢰성을 크게 향상시킬 수 있습니다. 각 밸브의 특성을 이해하고 시스템 요구사항에 맞는 최적의 밸브를 선택하는 것이 중요합니다. 이를 통해 에너지 효율을 높이고 유지보수 비용을 줄일 수 ...
  source-url: https://myjobbox.tistory.com/41

• [Naver] [특허]냉동 시스템에서의 팽창밸브 제어 장치 및 방법
  냉동 시스템에서의 팽창밸브 제어 장치 및 방법 Apparatus and Method for controling expansion valve in refrigerating system 원문보기
  source-url: https://scienceon.kisti.re.kr/srch/selectPORSrchPatent.do?cn=KOR1020070099187

검토 기준: 공식 문서 여부, 최신성, 프로젝트 적용 가능성, 보안/개인정보 포함 여부를 확인한 뒤 표준/교육/FAQ 후보로 승격한다.


## Telegram 팀원 보강 요청 (2026-06-18 07:05:58)
- Source: telegram:@FreeFilmer (7899169126)
- Tags: telegram,team-request,knowledge-gap,kst02-review

팀원이 기존 Obsidian 답변이 부족하다고 회신했다.

원 질문: 냉동기 장비에 연결되는 어샘블리 밸브 순서가 어떻게 될까?
추가 요청: 추가 설명 없음

처리 기준:
1. 내부 지식에서 누락된 기준을 우선 보강한다.
2. 외부 검색 또는 공식 문서 확인이 필요한 항목은 자동 수집 후 지식 업데이트 후보로 표시한다.
3. 고객명, 프로젝트명, 개인정보는 수집하지 않는다.

## 2026-06-20 장기 지식 업데이트 루프 시뮬레이션 보강 Q&A
- Source: LUA BIM LABS qa-simulation hardening
- Tags: knowledge-update,simulation,kst,loop,quality,field-case,2026

**Q: 20년차 전문가라면 이 답변 체계가 3년 뒤에도 유효하려면 어떤 지식 업데이트 루프가 필요하다고 보나요?**
A: 3년 뒤에도 유효하려면 지식 업데이트 루프를 "수집 -> 검증 -> 승격 -> 회귀 테스트 -> 폐기" 5단계로 고정한다. 1. 수집: 고객 질문, 현장 오류, 법규 변경, 제품 릴리즈를 매일 기록한다. 2. 검증: KST04 수집 후보, KST03 적용주의, KST02 검토 지식, KST01 공식확인으로 등급화한다. 3. 승격: 같은 질문 2회는 QA, 3회 또는 고객/안전/매출 영향이 크면 KB 본문으로 올린다. 4. 회귀 테스트: 월 1회 69개 이상 시뮬레이션, 95% 로컬 즉답률, 454개 담당자 Q&A 통과를 확인한다. 5. 폐기: 시행일이 지난 법규, 오래된 가격, 실패한 임시 답변은 보관만 하고 기본 답변에서 제외한다. 조건상 법규·가격·안전·계약 지식은 24시간 내 원문 출처와 담당자를 확인하고, 예외나 충돌이 있으면 지식큐레이터에게 공유·요청한다. 7일 내 승인/보류/폐기 상태를 기록하지 못하면 기본 답변에서 제외한다. 이 루프가 없으면 자동수집 노이즈, 오래된 기준, 고객 오답 리스크가 누적된다.
다만 예외 조건이 있거나 승인권자 판단이 필요한 경우에는 확정 답변으로 닫지 말고, 근거·담당자·기한을 기록해 공유한다.

## 2026-06-21 지식 업데이트 승격/폐기 추가 Q&A
- Source: LUA BIM LABS coverage expansion
- Tags: knowledge-update,kst,curation,qa,regression,2026

**Q: 자동 수집 후보가 공식 문서와 블로그를 동시에 포함하면 무엇을 먼저 승격하나요?**
A: 결론: 공식 문서와 프로젝트 적용성이 확인된 자료를 먼저 KST02 이상 후보로 승격한다. 1. 담당자는 원문 출처, 시행일, 작성자, Source/Tags, 고객 질문, 적용 공종, LOD 300/350 관련성을 24시간 안에 비교한다. 2. 조건상 법규, BEP, Revit 모델 기준처럼 책임 영향이 있으면 공식 문서 원문을 우선 확인하고 큐레이터 검토를 요청한다. 반면 블로그나 포럼은 참고 후보로 분리한다. 잘못 승격하면 고객 오답, 법무, 비용, 책임 리스크가 생긴다. 7일 내 승인자, 기한, KST 상태, 폐기/승격 로그를 공유한다.

**Q: 오래된 KB가 여전히 검색 상위에 나오면 지식업데이트 담당자는 어떻게 처리하나요?**
A: 결론: 삭제보다 상태 변경, 대체 문서 연결, 회귀 테스트 반영을 먼저 한다. 1. 담당자는 문서 날짜, 적용 기준, 최신 대체 자료, 검색 로그, Source/Tags, KST02/KST04 상태를 확인한다. 2. 조건상 법규·가격·보안·납품 기준이 바뀐 경우 24시간 내 경고 문구와 대체 링크를 추가하고 답변 기본값에서 제외한다. 반면 역사적 참고이면 보관 상태로 둔다. 방치하면 오래된 기준, 법무, 고객 약속, 비용 리스크가 누적된다. 7일 내 담당자, 승인자, 기한, 회귀 테스트 결과를 공유·보고한다.
