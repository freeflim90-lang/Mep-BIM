---
type: qwen-product-draft
project: Model Quality Auditor
task_id: BIMLIZE-QWEN-007
status: generated
created: 2026-05-24
tags:
  - qwen
  - mqa
  - backend-draft
  - product-development
---

# BIMLIZE-QWEN-007 Schedule Excel Export 계약 초안

선정 아이템: BIMlize 기능 범위 내재화 - Phase 1 Simple Features

## 작업 정보

| 항목 | 내용 |
|---|---|
| 산출물 | schedule field order, read-only/import restriction note, CSV/XLSX export report 구조 |
| 범위 | Export only. Import/Sync는 Phase 2로 분리. |
| 예상 출력 위치 | `backend/bim_command_center/schedule_export_contract.py` |
| Qwen 실행 | 성공 |
| 모델 | qwen2.5-coder:7b |
| 사유 | - |

## Qwen 초안

### Plan:
**Purpose:** Define the contract for exporting schedules to Excel in a CSV/XLSX format. This includes defining the field order and restrictions on read-only/import operations.

**Input:** Revit schedule data.

**Output:** CSV/XLSX file containing schedule data with specified field order.

**Excluded Scope:** Import/Sync functionality, which will be addressed in Phase 2.

### Draft:
```python
# backend/bim_command_center/schedule_export_contract.py

from abc import ABC, abstractmethod
import csv
import json

class ScheduleExportContract(ABC):
    @abstractmethod
    def export_schedule(self, schedule_data: dict) -> str:
        """Export schedule data to a CSV/XLSX file."""
        pass

    @abstractmethod
    def get_field_order(self) -> list:
        """Return the order of fields to be exported."""
        pass

    @abstractmethod
    def is_read_only(self) -> bool:
        """Check if export operation is read-only."""
        pass

class CSVExport(ScheduleExportContract):
    def __init__(self, field_order: list):
        self.field_order = field_order

    def export_schedule(self, schedule_data: dict) -> str:
        with open('schedule_export.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.field_order)
            writer.writeheader()
            for row in schedule_data['rows']:
                writer.writerow({key: row.get(key, '') for key in self.field_order})
        return 'schedule_export.csv'

    def get_field_order(self) -> list:
        return self.field_order

    def is_read_only(self) -> bool:
        return False

class ReadOnlyExport(ScheduleExportContract):
    def export_schedule(self, schedule_data: dict) -> str:
        raise Exception("Read-only operation not allowed.")

    def get_field_order(self) -> list:
        raise Exception("Read-only operation not allowed.")

    def is_read_only(self) -> bool:
        return True

# Example usage
if __name__ == "__main__":
    field_order = ['Task Name', 'Start Date', 'Finish Date']
    export_contract = CSVExport(field_order)
    schedule_data = {
        'rows': [
            {'Task Name': 'Task 1', 'Start Date': '2023-04-01', 'Finish Date': '2023-04-10'},
            {'Task Name': 'Task 2', 'Start Date': '2023-04-11', 'Finish Date': '2023-04-20'}
        ]
    }
    export_contract.export_schedule(schedule_data)
```

### Verification:
1. **Unit Tests:**
   - Test `CSVExport` class to ensure it correctly exports schedule data in CSV format.
   - Test `ReadOnlyExport` class to ensure it raises exceptions for read-only operations.

2. **Manual Testing:**
   - Manually verify that the exported CSV file contains the correct field order and data.

### API Need Assessment:
- No external API/Revit API/Navisworks API is required for this functionality.

### Next Draft Task:
Develop a unit test suite to validate the `ScheduleExportContract` implementation.

## 연결

- [[Qwen Draft Index]]
- [[Qwen Development Boundary]]
- [[Revit API Test Gate Index]]
- [[Build Test Index]]
