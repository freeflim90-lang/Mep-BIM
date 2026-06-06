# 2026-06-06 AI 지식 고도화 Iteration 19 업데이트

## 업데이트 개요
- 날짜: 2026-06-06
- 이터레이션: 19
- 보강 파일: Revit_Addin.md
- 소스: Autodesk Developer Blog "Revit 2027 SDK .NET 10 Migration and Key API Changes", Microsoft .NET 10 Breaking Changes, Autodesk Platform Services docs

---

## 1. Revit_Addin.md — Revit 2027 SDK .NET 10 마이그레이션 보강

### 핵심 내용 (지식 공백 해소)
기존 KB Revit_Addin.md에는 Revit 2027 AI Assistant / Forma / Carbon 기능은 있으나 **SDK .NET 10 마이그레이션** 정보가 전무 → LUA BIM LABS Add-in 개발에 즉시 영향 미치는 핵심 정보 보강

**⚠️ 핵심 변경 사항:**
- Revit 2027(2026-04-07 출시) = **.NET 10 런타임** (Revit 2025/2026 = .NET 8)
- 모든 신규 Add-in은 .NET 10 SDK로 빌드 필수

**호환성 원칙 (가장 중요):**
| 상황 | 결과 |
|------|------|
| .NET 8 빌드 Add-in → Revit 2027 | 대부분 작동 (하위 호환, 보장 없음) |
| .NET 10 빌드 Add-in → Revit 2025/2026 | **완전 실패** (상위 호환 없음) |

**배포 경로 변경:**
- 기존: `%ProgramData%\Autodesk\Revit\Addins\2026\`
- Revit 2027: `%ProgramFiles%\Autodesk\Revit 2027\AddIns\` (보안 강화)
- 인스톨러 배포 시 경로 분기 필수

**.NET 10 마이그레이션 실패 원인:**
1. 어셈블리 로딩 동작 변경
2. 리플렉션(Reflection) 동작 변경
3. 직렬화(`System.Text.Json` / `Newtonsoft.Json`) 버전 불일치
4. Native Interop(P/Invoke, COM) 처리 방식 차이
5. 전이적(transitive) NuGet 패키지 .NET 10 미지원

**BIM CC 마이그레이션 체크리스트:**
```xml
<!-- .csproj 변경 -->
<TargetFramework>net10-windows</TargetFramework>  <!-- 기존: net8-windows -->
```
- 전체 NuGet 패키지 .NET 10 호환 여부 확인: `dotnet list package --framework net10-windows`
- 멀티 타깃 빌드: Revit 2024~2026 = net8-windows, Revit 2027 = net10-windows
- CI(GitHub Actions) 멀티 타깃 빌드 자동화 설정

**강화된 Add-in 격리:**
- Add-in 간 명시적 의존성 정의 가능 → DLL Hell 방지
- 복수 Add-in 병존 환경에서 어셈블리 버전 충돌 해소

**Dynamo 4.0.2:**
- 동일하게 .NET 10 전환 → 기하 연산 속도 향상

---

## 지식 공백 식별 방법
- Revit_Addin.md 기존 섹션 확인: Revit 2027 섹션(AI/Forma/Carbon)은 있으나 SDK .NET 마이그레이션 누락
- 검증: grep "net10\|\.NET 10\|dotnet 10" → 결과 없음 → 공백 확인
- 소스: Autodesk Developer Blog + Microsoft .NET 10 breaking changes 문서

## 연관 지식
- [[Revit_Addin]] · [[ACC_BIM360]] · [[BIM_납품검수]]
- [[해외건설기업_동향분석]] · [[Scan-to-BIM]] · [[IFC_OpenBIM]]
