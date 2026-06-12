# 스토어심사 Q&A 지식

텔레그램 질문·자동 수집 응답 저장소 — 기준 가이드라인(스토어심사.md)과 분리 운영.

## 2026-06-05 Autodesk App Store 심사 실전 Q&A 추가
- Source: Autodesk App Store Publisher 가이드, LUA BIM LABS Add-in 개발 경험
- Tags: autodesk-store,app-review,publish,add-in,qa,2026

**Q: Autodesk App Store 심사에 얼마나 걸리나요?**
A: 제출 후 보통 2~4주가 소요됩니다. 심사 항목에는 기능 테스트(Revit 2023~2026 버전별), 악성코드 스캔, 아이콘·스크린샷·설명 검토가 포함됩니다. 심사 중 수정 요청이 오면 대응하면서 기간이 늘어날 수 있습니다. *(KST01 공식확인)*

**Q: Add-in이 심사에서 자주 반려되는 이유는 뭔가요?**
A: 주요 반려 사유: ① 아이콘 해상도 부적합(32×32px 미충족), ② 스크린샷 최소 3장 미충족, ③ 여러 Revit 버전 중 일부 버전에서 오류 발생, ④ .addin 매니페스트 경로 오류, ⑤ 설명에 타사 제품 비교·폄하 내용 포함. 제출 전 체크리스트로 확인하는 것이 중요합니다. *(KST01 공식확인)*

**Q: 무료 Add-in을 나중에 유료로 전환할 수 있나요?**
A: 가능합니다. 무료로 출시 후 사용자 피드백·인지도를 쌓은 다음 유료 구독 또는 프리미엄 버전으로 전환하는 전략이 일반적입니다. 가격 모델 변경은 언제든 Autodesk Publisher 포털에서 수정할 수 있습니다. 단, 기존 무료 사용자 경험을 갑자기 차단하면 부정 리뷰가 쌓일 수 있습니다. *(KST03 적용주의)*

**Q: LUA BIM LABS BIM Command Center는 언제 출시 예정인가요?**
A: 현재 개발 중이며 Autodesk App Store 제출을 목표로 하고 있습니다. 출시 시 LUA BIM LABS 텔레그램 채널을 통해 안내드리겠습니다. 베타 테스터 신청은 텔레그램 봇에서 가능합니다. *(내부 운영 기준)*


## 스토어심사 FAQ (2026-05-24)
- Source: LUA BIM LABS internal store submission knowledge baseline
- Tags: store,faq,autodesk,submission,review

Autodesk App Store 심사 소요 기간을 물을 때:
- 신규 등록: 평균 2~4주 (기능 복잡도·심사 대기 수에 따라 변동)
- 업데이트: 1~2주 (주요 기능 변경 시 더 길어질 수 있음)
- 기술 검수 후 마케팅 검수 순으로 진행
- 심사 상태는 Autodesk Developer Portal에서 확인

심사 거절 주요 사유를 물을 때:
- 설명과 실제 기능 불일치 (스크린샷·설명 vs 실제 동작)
- 비허가 Revit API 또는 내부 Autodesk 리소스 직접 접근
- 개인정보 무단 수집 또는 외부 서버 무단 전송
- MSI 설치 파일 서명 누락 (코드 서명 인증서 필수)
- 설치/제거 후 잔여 파일 미정리
- Autodesk 제품 성능 저하 또는 충돌 유발
- 스크린샷 미제공 또는 저화질

심사 통과를 위한 체크리스트를 물을 때:
→ `12_STORE_SUBMISSION_CHECKLIST.md` 참조
- 기능 설명과 실제 동작 일치 확인
- 지원 Revit 버전 명시
- EV 코드 서명 인증서 적용
- 설치/제거 완전성 테스트
- 개인정보처리방침 URL 제공
- 지원 이메일 기재


## Q: Autodesk Store 심사에서 거절당했을 때 대응법은? (2026-05-24)
- Source: LUA BIM LABS internal store submission knowledge baseline
- Tags: store,qa,rejection,resubmit

거절 후 재제출 프로세스:
1. 거절 사유 이메일 상세 확인 (Autodesk Publisher Portal)
2. 사유별 수정:
   - 기능 설명 불일치 → 스크린샷·설명 문구 수정
   - API 위반 → 해당 API 사용 제거 또는 대체 방법 구현
   - 개인정보 → 처리방침 URL 추가 및 데이터 흐름 재검토
   - 코드 서명 → EV 인증서 적용 후 재빌드
3. 수정 완료 후 재제출 + 수정 내역 메모 첨부
4. 재심사 소요: 1~2주 추가
5. 동일 사유 2회 이상 거절 시 Autodesk 파트너 채널로 직접 문의

거절 예방:
- 제출 전 `12_STORE_SUBMISSION_CHECKLIST.md` 전체 체크
- 내부 dry-run 테스트 (빌드검증 에이전트 활용)
- 스토어심사 에이전트의 심사 시뮬레이션 진행


## Q: 스토어 제품 설명 최적화 방법은? (2026-05-24)
- Source: LUA BIM LABS internal product/marketing knowledge baseline
- Tags: store,qa,listing,marketing

Autodesk App Store 리스팅 최적화:
- 제목: 핵심 기능 키워드 포함 (예: "BIM Command Center for Revit")
- 설명 첫 2줄: 가장 강력한 가치 제안 (검색 결과에서 표시되는 부분)
- 키워드: Revit, BIM, MEP, automation, productivity 등 실무자 검색어
- 스크린샷: 실제 Revit 환경에서 기능 동작 화면 (최소 3장)
- 비디오: 30~60초 기능 데모 (있으면 전환율 크게 향상)
- 버전 호환성: 지원 Revit 버전을 명확하게 나열
- 업데이트 노트: 각 버전에서 개선된 내용 구체적으로 기재
