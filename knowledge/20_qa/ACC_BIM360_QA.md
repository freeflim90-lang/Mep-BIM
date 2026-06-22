# ACC_BIM360 Q&A 지식

## 2026-06-20 ACC/BIM360 CDE 실무 케이스 Q&A
- Source: `knowledge/40_curation/quality/2026-06-20_EXTENSION_AGENTS_PRACTICAL_CASE_LIBRARY.md`
- Tags: acc,bim360,cde,field-case,version,approval,qa,2026

**Q: 최신 파일과 승인 파일이 다르면 무엇을 기준으로 답하나요?**
A: 최신 업로드 파일보다 승인 상태와 워크플로우 로그를 먼저 확인한다. 검토용, 공유용, 승인용 상태를 분리하고, 고객 제출에는 승인된 Revision과 Transmittal 기록을 근거로 삼는다.


실무 보강 (2026-06-20 답변 품질 보강):
1. 기준 확인: `ACC_BIM360` 담당자는 이 질문을 단순 설명이 아니라 KST02 이상 운영 기준, 프로젝트 범위, 고객 영향도, 납품/계약 책임을 함께 확인하는 실무 판단 문제로 본다.
2. 조건 분기: 확정 기준, 현장 예외, 고객 요청, 내부 승인 여부를 먼저 나눈다. 수치나 법규가 필요한 경우에는 시행일, 적용 대상, 원문 출처, LOD 300/350 같은 모델 상세 수준을 확인하기 전까지 단정하지 않는다.
3. 다음 액션: 24시간 안에 현재 자료와 누락 자료를 정리하고, 7일 안에 담당자·기한·검증 방법이 있는 조치 항목으로 바꾼다. 반복 문의는 QA로 남기고 2회 이상 반복되면 KB 본문 승격 후보로 올린다.
4. 리스크 경계: 비용, 일정, 안전, 개인정보, 법무, 고객 약속으로 번질 수 있는 내용은 즉답보다 확인 로그와 승인 경로를 우선한다. 불확실한 답은 '가능/불가'보다 확인 조건과 대안 2개를 함께 제시한다.
5. 답변 형식: 결론 1문장, 근거 2개, 확인할 자료 3개, 다음 행동 1개 순서로 응답한다. Source: LUA BIM LABS agent QA quality baseline. Tags: qa,quality,field-case,kst02,risk,2026.

## 2026-06-21 ACC/BIM360 승인흐름 추가 Q&A
- Source: LUA BIM LABS coverage hardening
- Tags: acc,bim360,cde,revision,transmittal,approval,2026

**Q: ACC에서 같은 파일명이 여러 번 올라오면 어떤 버전을 고객에게 보내야 하나요?**
A: 결론: 파일명보다 Revision, Status, Review Workflow, Transmittal 로그가 일치하는 승인 버전을 고객에게 보낸다. 1. 최신 업로드 시간, 승인 상태, 검토 코멘트, 배포 패키지 번호를 같은 화면에서 확인한다. 2. 조건상 최신 파일이 WIP 또는 Shared 상태이면 참고용으로만 쓰고, 반면 Published/Approved 상태와 Transmittal 번호가 있으면 고객 제출 후보로 본다. 다만 승인권자와 배포 목적이 불명확한 경우에는 제출 불가로 구분하고, 예외 요청은 PM 승인 전까지 보류한다. ISO 19650 CDE 흐름과 BEP 문서관리 기준을 근거로 남긴다. 승인되지 않은 파일을 보내면 계약, 비용, 일정, 책임 리스크가 생기므로 24시간 내 문서관리 담당자가 상태를 기록하고 7일 내 PM 승인, 기한, 로그 링크를 공유한다.

**Q: BIM360 이슈가 닫혔는데 모델에는 수정이 안 보이면 어떻게 확인하나요?**
A: 결론: Issue status만 믿지 않고 모델 Revision, Viewpoint, Markup, RFI 답변, 담당자 코멘트를 함께 확인한다. 1. Closed 상태의 이슈 ID와 수정 모델의 업로드 버전이 같은지 대조한다. 2. 조건상 코멘트만 닫힌 경우에는 재오픈하고, 반면 수정 모델이 별도 패키지에 있으면 Transmittal 링크를 연결한다. Revit/ACC/BIM360 로그, BCF, RFI를 근거로 남기며 누락되면 재작업, 납품 반려, 책임 분쟁 리스크가 있다. 24시간 내 담당자에게 증빙을 요청하고 7일 내 승인자, 기한, 상태 로그를 기록해 공유한다.

## 2026-06-21 ACC/BIM360 CDE 통제 추가 Q&A
- Source: LUA BIM LABS coverage hardening
- Tags: acc,bim360,cde,permissions,issue,rfi,2026

**Q: ACC 권한 설정이 바뀐 뒤 고객이 파일을 못 본다고 하면 무엇부터 확인하나요?**
A: 결론: 파일 문제로 단정하지 않고 폴더 권한, 역할, 링크 만료, 배포 패키지 상태를 먼저 확인한다. 1. 담당자는 사용자 계정, 회사 역할, Folder Permission, Transmittal, Source, Tags를 24시간 안에 기록한다. 2. 조건상 Published/Approved 파일인데 고객이 접근하지 못하면 권한 상속과 링크 만료를 검토하고 관리자에게 요청한다. 반면 WIP 파일이면 고객 공개 대상이 아니라고 구분한다. 다만 보안, 개인정보, 계약 책임 리스크가 있으면 예외 없이 승인 로그와 7일 처리 결과를 공유하고 보고한다.

**Q: ACC 이슈와 RFI가 서로 다른 결론을 가리키면 어느 흐름을 따르나요?**
A: 결론: 이슈 코멘트보다 공식 RFI 답변과 승인 워크플로우를 우선하되 모델 수정 증거를 함께 확인한다. 1. 담당자는 RFI 번호, Issue ID, Revision, Viewpoint, BEP 문서관리 기준, Source, Tags를 24시간 안에 대조한다. 2. 조건상 RFI 승인 답변이 있고 모델이 미수정이면 담당자에게 수정 요청을 공유한다. 반면 이슈 코멘트가 최신 근거라면 RFI 보완을 요청한다. 다만 납품 반려, 모델 오류, 법무 책임, 비용, 고객 약속 리스크가 있으면 승인자와 7일 검토 로그를 남기고 보고한다.

## 2026-06-21 ACC/BIM360 감사추적 추가 Q&A
- Source: LUA BIM LABS coverage expansion
- Tags: acc,bim360,cde,audit,permission,transmittal,2026

**Q: ACC에서 파일을 삭제하거나 이동한 기록이 보이면 바로 복구해야 하나요?**
A: 결론: 바로 복구하지 말고 삭제·이동 사유, 권한자, 배포 영향, 최신 승인 상태를 먼저 확인한다. 1. 담당자는 Activity Log, 파일 경로, Revision, Transmittal, 권한자, Source/Tags, 24시간 변경 시각을 기록한다. 2. 조건상 Approved/Published 파일이 고객 제출물에 연결되어 있으면 복구 요청과 PM 승인을 공유하고, 반면 WIP 중복 파일이면 정리 로그로 처리한다. 무검토 복구는 버전 혼선, 보안, 법무, 고객 약속 책임 리스크를 만든다. 7일 내 승인자, 기한, 복구/보류 결과를 보고한다.
