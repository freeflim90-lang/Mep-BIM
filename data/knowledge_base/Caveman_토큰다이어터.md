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
