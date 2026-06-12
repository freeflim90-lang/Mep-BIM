---
type: qwen-product-draft
project: Model Quality Auditor
task_id: BIMLIZE-QWEN-005
status: generated
created: 2026-05-24
tags:
  - qwen
  - mqa
  - backend-draft
  - product-development
---

# BIMLIZE-QWEN-005 Tag/Text Aligner geometry preview 초안

선정 아이템: BIMlize 기능 범위 내재화 - Phase 1 Simple Features

## 작업 정보

| 항목 | 내용 |
|---|---|
| 산출물 | 선택된 태그/문자 정렬·분배 preview DTO, pinned skip, leader 보존 정책 |
| 범위 | 현재 선택 요소만 대상으로 하고 실제 이동은 Revit API 게이트에서 검증. |
| 예상 출력 위치 | `backend/bim_command_center/tag_text_align_contract.py` |
| Qwen 실행 | 성공 |
| 모델 | qwen2.5-coder:7b |
| 사유 | - |

## Qwen 초안

### Plan:
**Purpose:** Develop a preview DTO for selected tag/text alignment and distribution, including pinned skip and leader preservation policies. The initial implementation will focus on the current selection only.

**Input:** Selected elements in Revit

**Output:** Preview DTO containing tag/text alignment and distribution information, with options for pinned skip and leader preservation.

**Exclusion Range:** Actual movement of elements is to be validated through the Revit API gate.

### Draft:
```python
# backend/bim_command_center/tag_text_align_contract.py

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TagTextAlignPreviewDTO:
    element_ids: List[str]
    alignment_type: str  # e.g., 'Horizontal', 'Vertical'
    distribution_type: str  # e.g., 'Evenly Spaced', 'Custom Spacing'
    pinned_elements: Optional[List[str]] = None
    leader_preservation_policy: bool = False

def generate_preview_dto(selected_elements: List[str], alignment_type: str, distribution_type: str,
                          pinned_elements: Optional[List[str]] = None, leader_preservation_policy: bool = False) -> TagTextAlignPreviewDTO:
    return TagTextAlignPreviewDTO(
        element_ids=selected_elements,
        alignment_type=alignment_type,
        distribution_type=distribution_type,
        pinned_elements=pinned_elements,
        leader_preservation_policy=leader_preservation_policy
    )
```

### Verification:
1. **Unit Test:** Write unit tests for the `generate_preview_dto` function to ensure it correctly constructs the DTO with various inputs.
2. **Manual Testing:** Manually select elements in Revit, run the preview feature, and verify that the generated DTO matches the expected output.

### API Neediness Judgment:
- No external API/Revit API/Navisworks API is required for this initial implementation.

### Next Draft Task:
Develop a frontend interface to display the preview DTO and allow users to interact with the tag/text alignment settings.

## 연결

- [[Qwen Draft Index]]
- [[Qwen Development Boundary]]
- [[Revit API Test Gate Index]]
- [[Build Test Index]]
