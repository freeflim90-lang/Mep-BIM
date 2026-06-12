---
type: qwen-product-draft
project: Model Quality Auditor
task_id: BIMLIZE-QWEN-003
status: generated
created: 2026-05-24
tags:
  - qwen
  - mqa
  - backend-draft
  - product-development
---

# BIMLIZE-QWEN-003 View Template Copier dry-run 계약 초안

선정 아이템: BIMlize 기능 범위 내재화 - Phase 1 Simple Features

## 작업 정보

| 항목 | 내용 |
|---|---|
| 산출물 | 템플릿 목록, 복사 대상 preview, skip/rename/replace 정책, copy report DTO |
| 범위 | Revit API 호출은 인터페이스로만 표현. 기본 정책은 skip이며 replace는 명시 확인 필요. |
| 예상 출력 위치 | `backend/bim_command_center/view_template_copy_contract.py` |
| Qwen 실행 | 성공 |
| 모델 | qwen2.5-coder:7b |
| 사유 | - |

## Qwen 초안

### Plan:
**Purpose:** To create a dry-run contract for the View Template Copier feature in BIM Command Center for Revit. This will include defining the template list, preview of copy targets, skip/rename/replace policies, and a copy report DTO.

**Input:** None

**Output:** 
- `view_template_list.py`
- `copy_preview.py`
- `policy_manager.py`
- `copy_report_dto.py`

**Exclusion:** Revit API calls will be expressed through interfaces. The default policy is skip, and replace requires explicit confirmation.

### Draft:
#### view_template_list.py
```python
class ViewTemplateList:
    def get_templates(self) -> list:
        pass
```

#### copy_preview.py
```python
class CopyPreview:
    def preview_copy_targets(self, templates: list) -> dict:
        pass
```

#### policy_manager.py
```python
class PolicyManager:
    def skip_policy(self, template: str) -> bool:
        pass

    def replace_policy(self, template: str) -> bool:
        pass
```

#### copy_report_dto.py
```python
class CopyReportDTO:
    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message
```

### Verification:
1. **Unit Tests:** Write unit tests for each class to ensure they function as expected without Revit API calls.
2. **Integration Tests:** Simulate the copy process using mock data and verify that the skip/rename/replace policies work correctly.

### API Need Assessment:
No external APIs or Revit API calls are required for this feature. All logic is purely domain-driven.

### Next Draft Task:
Develop the actual implementation of the View Template Copier feature, ensuring it adheres to the defined contracts and does not rely on Revit API calls directly.

## 연결

- [[Qwen Draft Index]]
- [[Qwen Development Boundary]]
- [[Revit API Test Gate Index]]
- [[Build Test Index]]
