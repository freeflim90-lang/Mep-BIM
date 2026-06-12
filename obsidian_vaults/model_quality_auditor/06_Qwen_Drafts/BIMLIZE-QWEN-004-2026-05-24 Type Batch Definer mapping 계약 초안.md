---
type: qwen-product-draft
project: Model Quality Auditor
task_id: BIMLIZE-QWEN-004
status: generated
created: 2026-05-24
tags:
  - qwen
  - mqa
  - backend-draft
  - product-development
---

# BIMLIZE-QWEN-004 Type Batch Definer mapping 계약 초안

선정 아이템: BIMlize 기능 범위 내재화 - Phase 1 Simple Features

## 작업 정보

| 항목 | 내용 |
|---|---|
| 산출물 | JSON/CSV 타입 정의 매핑, missing/existing preview, readonly parameter skip 정책 |
| 범위 | Dry-run mandatory. 실제 type 생성/수정은 Revit API 게이트 이후 확정. |
| 예상 출력 위치 | `backend/bim_command_center/type_batch_contract.py` |
| Qwen 실행 | 성공 |
| 모델 | qwen2.5-coder:7b |
| 사유 | - |

## Qwen 초안

### Plan:
**목적:** Type Batch Definer mapping 계약 초안을 작성하여 BIM Command Center for Revit의 초기 기능 중 하나를 구현합니다.

**입력:** 
- JSON/CSV 타입 정의 매핑 파일
- missing/existing preview 정보
- readonly parameter skip 정책

**출력:**
- backend/bim_command_center/type_batch_contract.py 파일 작성

**제외 범위:**
- Revit API 의존 코드 구현은 제외합니다. 순수 로직과 데이터 계약만 작성합니다.

### Draft:
```python
# backend/bim_command_center/type_batch_contract.py

from dataclasses import dataclass, field
import json
import csv

@dataclass
class TypeBatchDefinerMapping:
    mapping: dict = field(default_factory=dict)
    missing_preview: list = field(default_factory=list)
    existing_preview: list = field(default_factory=list)
    readonly_skip: list = field(default_factory=list)

def load_mapping_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_mapping_to_json(mapping, file_path):
    with open(file_path, 'w') as file:
        json.dump(mapping, file, indent=4)

def load_mapping_from_csv(file_path):
    mapping = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapping[row['type']] = row['definition']
    return mapping

def save_mapping_to_csv(mapping, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['type', 'definition']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for type, definition in mapping.items():
            writer.writerow({'type': type, 'definition': definition})

def preview_mapping(mapping):
    missing = [t for t in mapping if not mapping[t]]
    existing = [t for t in mapping if mapping[t]]
    return missing, existing

def skip_readonly_params(params):
    readonly_skip = [param for param in params if param.readonly]
    return readonly_skip
```

### Verification:
1. **JSON 파일 로드/저장 테스트:**
   - `load_mapping_from_json`과 `save_mapping_to_json` 함수를 사용하여 JSON 파일을 로드하고 저장하는 테스트를 수행합니다.
   
2. **CSV 파일 로드/저장 테스트:**
   - `load_mapping_from_csv`와 `save_mapping_to_csv` 함수를 사용하여 CSV 파일을 로드하고 저장하는 테스트를 수행합니다.

3. **미리보기 테스트:**
   - `preview_mapping` 함수를 사용하여 mapping의 missing/existing 항목을 확인합니다.
   
4. **읽기 전용 파라미터 스킵 테스트:**
   - `skip_readonly_params` 함수를 사용하여 readonly parameter를 스킵하는 테스트를 수행합니다.

### API 필요성 판단:
- 이 초안은 순수 로직과 데이터 계약을 작성하므로, Revit API 의존 코드는 필요하지 않습니다.

### Next Draft Task:
- Revit API 게이트 이후 실제 type 생성/수정 구현으로 이어갑니다.

## 연결

- [[Qwen Draft Index]]
- [[Qwen Development Boundary]]
- [[Revit API Test Gate Index]]
- [[Build Test Index]]
