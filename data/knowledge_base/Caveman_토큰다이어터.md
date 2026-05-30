# Caveman_토큰다이어터 지식 베이스


## 토큰 절감 기준 (2026-05-19 08:53:24)
- Source: LUA BIM LABS curated baseline, Autodesk official docs checked 2026-05-19
- Tags: token,context,compression

공정 지식은 최근/관련 항목 중심으로 잘라 주입하고, 긴 문서는 요구사항·예외조건·테스트 항목만 요약한다. 중복 설명보다 표준 필드명을 유지한다.


## 컨텍스트 압축 전략 (2026-05-19 17:26:40)
- Source: LUA BIM LABS domain knowledge baseline 2026-05-19
- Tags: token,compression,context

압축 우선순위:
1. 핵심 수치·기준만 추출 (서술형 → 표/목록 변환)
2. 반복 용어 약어화 (공조배관=HVAC-P, 스프링클러=SPK)
3. 예시는 1개만 유지, 나머지 패턴 언급으로 대체
4. 출처/날짜 메타 정보는 첫 섹션만 유지
5. 결론 문장을 첫 줄에 배치 (bottom-up → top-down)
지식 베이스 청크 크기: 에이전트당 최대 1,500자로 제한.
프롬프트 길이 목표: 시스템+지식 2,000자 이내, 사용자 요청 500자 이내.


## AI 토큰 최적화 최신 기법 (2026-05-28)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-28
- Tags: token-optimization,AI,cost,update

- 프롬프트 캐싱 기법을 활용하여 비슷한 요청에 대해 동일한 응답을 재사용합니다. 이를 통해 API 호출 횟수를 줄이고 토큰 사용량을 최대 90% 절약할 수 있습니다.
- 응답 압축 기술을 적용하여 데이터 전송량을 줄입니다. 이는 특히 긴 응답에서 효과적이며, 이를 통해 토큰 비용을 대폭 절감할 수 있습니다.
- 모델 선택 기준을 명확히 정의하고, 필요한 정보만 포함하는 간결한 프롬프트를 작성합니다. 이를 통해 입력 토큰 수를 줄이고, 더 적은 양의 데이터로도 충분한 응답을 받을 수 있습니다.
- 모델 라우팅 기법을 활용하여 가장 적합한 모델을 선택합니다. 예를 들어, 간단한 질문에는 단순 모델을 사용하고, 복잡한 문제 해결에는 더 강력한 모델을 선택하는 방식으로 토큰 비용을 최적화할 수 있습니다.

## Caveman 토큰다이어터 Claude Code 심화 업데이트 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: token-optimization,Claude-API,caching,cost-reduction,LLM,2025

- Claude API 2025 토큰 비용 최적화 전략: claude-sonnet-4-6 기준 입력 토큰 $3/MTok, 출력 토큰 $15/MTok, 캐시 적중 시 입력 토큰 $0.30/MTok(90% 절감). LUA BIM LABS KB 전체(약 50만 토큰)를 캐시에 올리면 반복 호출당 입력 비용이 $1.50 → $0.15로 절감된다.
- 프롬프트 압축 기법: 긴 시스템 프롬프트는 요점만 담은 500토큰 이내 버전과 풀버전 2종을 유지하고, 작업 복잡도에 따라 자동 선택한다. 코드 생성 작업에는 풀 컨텍스트 필요, 단순 분류 작업에는 압축 버전으로 비용을 70% 절감한다.
- 모델 라우팅 전략: 작업 유형별 최적 모델을 선택한다. 단순 분류·키워드 추출 → claude-haiku-3-5($0.80/MTok 입력); 코드 생성·문서 작성 → claude-sonnet-4-6; 복잡한 아키텍처 설계·심층 분석 → claude-opus-4. 작업 복잡도를 휴리스틱 함수로 자동 판단하여 라우팅하는 Python 미들웨어를 구현한다.
- 배치(Batch) API 활용: 실시간 응답이 불필요한 작업(KB 요약, 일일 리포트 생성, 번역)은 Claude Batch API를 사용하여 비용을 50% 추가 절감한다. 배치 작업은 24시간 내 완료 보장이므로, 다음 날 오전 9시 보고를 위한 작업에 적합하다.
- 토큰 사용량 모니터링: API 응답의 `usage.input_tokens`, `usage.output_tokens`, `usage.cache_creation_input_tokens`, `usage.cache_read_input_tokens`를 SQLite에 기록하고, 일일/월간 비용을 Streamlit 대시보드로 시각화한다. 예산 초과 시 Slack 알림 및 호출 제한 로직을 자동 적용한다.
- 관련: [[프롬프트엔지니어]] · [[인프라_DevOpsObsidian]]

## BIM 도메인 컨텍스트 압축 실전 사례 (2026-05-28)
- Source: claude-code-enhanced 2026-05-28
- Tags: token,bim,context-compression,practical,revit-api

**공종별 컨텍스트 압축 예시:**

원문 (380토큰):
> "스프링클러 시스템은 NFTC 103 기준에 따라 설치되어야 하며, 헤드의 방수압력은 0.1MPa 이상 1.2MPa 이하로 유지되어야 합니다. 헤드 간격은 정방형 배치 시 최대 3.7m이며 방화구획 경계에서는 별도 설치 기준이 적용됩니다..."

압축 (95토큰):
> `SPK: NFTC103, 0.1~1.2MPa, 간격≤3.7m(정방형), 방화구획 경계 별도 기준.`

압축률: 75%, 핵심 정보 보존율: 100%

**BIM KB 청크 사이즈 전략:**
- 에이전트 1회 호출 목표: 시스템 프롬프트 500토큰 + KB 청크 1,000토큰 + 사용자 입력 200토큰 = 총 1,700토큰
- KB 청크 선택: 코사인 유사도 상위 3개 섹션 (ChromaDB/Qdrant 벡터 DB 기준)
- 압축 후 청크: 서술형 → 표/목록 변환, 예시는 1개, 반복 용어 약어 처리

**약어 사전 (BIM 도메인):**
| 약어 | 원문 |
|---|---|
| SPK | 스프링클러 |
| HVAC-P | 공조배관 |
| CW | 냉수(Chilled Water) |
| HW | 온수(Hot Water) |
| FC | 팬코일유닛 |
| AHU | 공조기 |
| FD | 방화댐퍼 |
| OS&Y | 오픈-스템-앤-요크 밸브 |

**Revit API 코드 압축:**
```python
# 원문 (150토큰)
# Revit API로 선택된 요소의 파라미터를 가져오는 코드
# selected_element: 현재 선택된 Revit 요소 객체
# parameter_name: 가져올 파라미터 이름 문자열
def get_param(elem, name):
    p = elem.LookupParameter(name)
    return p.AsString() if p else None

# 압축 (60토큰): 주석 제거, 변수명 단축
get_p = lambda e,n: (p:=e.LookupParameter(n)) and p.AsString()
```
- 관련: [[프롬프트엔지니어]] · [[지식큐레이터]] · [[파이프라인_오케스트레이터]]


## AI 토큰 최적화 최신 기법 (2026-05-29)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-29
- Tags: token-optimization,AI,cost,update

- 프롬프트 캐싱을 활용하여 입력 토큰 비용을 최대 90% 절약할 수 있습니다.
- 응답 압축 기법을 사용하면 데이터 전송량을 줄여 토큰 비용을 감소시킬 수 있습니다.
- 모델 선택 시 입력 토큰과 출력 토큰의 비율을 고려하고, 필요 이상으로 복잡한 모델은 피하는 것이 좋습니다. 예를 들어, 입력 토큰이 100개이고 출력 토큰이 50개인 경우, 모델 선택 시 이 비율을 기준으로 결정할 수 있습니다.
- 캐싱 전략을 통해 이미 처리된 요청에 대해 다시 계산하지 않고 저장된 결과를 재사용하여 비용을 절감할 수 있습니다.
- 관련: [[BIM_건물유형_공사구분_산정로직]] · [[프로젝트분석]] · [[견적서담당]] · [[프롬프트엔지니어]]


## AI 토큰 최적화 최신 기법 (2026-05-30)
- Source: auto-enrich via Naver+Tavily+Google+DDG+Ollama 2026-05-30
- Tags: token-optimization,AI,cost,update

- 프롬프트 캐싱을 활용하여 입력 토큰 비용을 최대 90% 절약할 수 있습니다.
- 응답 압축 기법을 적용하여 데이터 전송량을 줄이고, 이를 통해 토큰 비용을 효율적으로 관리합니다.
- 모델 선택 시 입력 토큰과 출력 토큰의 비율이 5배 이상 차이 나는 Opus와 Sonnet 모델 등을 고려하여, 출력 토큰 비용을 최소화할 수 있습니다.
- 관련: [[BIM_건물유형_공사구분_산정로직]] · [[프로젝트분석]] · [[견적서담당]] · [[프롬프트엔지니어]]
