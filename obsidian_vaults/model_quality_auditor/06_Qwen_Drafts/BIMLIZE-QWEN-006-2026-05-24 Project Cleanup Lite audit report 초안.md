---
type: qwen-product-draft
project: Model Quality Auditor
task_id: BIMLIZE-QWEN-006
status: generated
created: 2026-05-24
tags:
  - qwen
  - mqa
  - backend-draft
  - product-development
---

# BIMLIZE-QWEN-006 Project Cleanup Lite audit report 초안

선정 아이템: BIMlize 기능 범위 내재화 - Phase 1 Simple Features

## 작업 정보

| 항목 | 내용 |
|---|---|
| 산출물 | unused views, imported CAD, warnings count, unplaced rooms/spaces, unused templates audit result 구조 |
| 범위 | Audit/report only. 삭제 또는 정리 액션은 Phase 2 이후 명시 확인 기반. |
| 예상 출력 위치 | `backend/bim_command_center/project_cleanup_audit.py` |
| Qwen 실행 | 성공 |
| 모델 | qwen2.5-coder:7b |
| 사유 | - |

## Qwen 초안

### Plan:
**Purpose:** Create an audit report for project cleanup that includes unused views, imported CAD files, warning counts, unplaced rooms/spaces, and unused templates.

**Input:** Revit project file (.rvt)

**Output:** Audit report in JSON format with the following structure:
```json
{
  "unused_views": [...],
  "imported_cad_files": [...],
  "warnings_count": int,
  "unplaced_rooms_spaces": [...],
  "unused_templates": [...]
}
```

**Excluded Scope:** Deletion or cleanup actions, which will be addressed in Phase 2 based on explicit confirmation.

### Draft:
```csharp
using System;
using System.Collections.Generic;

namespace BIMCommandCenter.ProjectCleanupAudit
{
    public class ProjectCleanupAuditResult
    {
        public List<string> UnusedViews { get; set; }
        public List<string> ImportedCADFiles { get; set; }
        public int WarningsCount { get; set; }
        public List<string> UnplacedRoomsSpaces { get; set; }
        public List<string> UnusedTemplates { get; set; }

        public ProjectCleanupAuditResult()
        {
            UnusedViews = new List<string>();
            ImportedCADFiles = new List<string>();
            UnplacedRoomsSpaces = new List<string>();
            UnusedTemplates = new List<string>();
        }
    }

    public class ProjectCleanupAudit
    {
        public static ProjectCleanupAuditResult AuditProject(string projectFilePath)
        {
            // Placeholder for actual audit logic
            var result = new ProjectCleanupAuditResult();
            
            // Example data (to be replaced with actual logic)
            result.UnusedViews.Add("View1");
            result.ImportedCADFiles.Add("File1.dwg");
            result.WarningsCount = 5;
            result.UnplacedRoomsSpaces.Add("Room1");
            result.UnusedTemplates.Add("Template1");

            return result;
        }
    }
}
```

### Verification:
1. **Unit Tests:** Write unit tests for the `ProjectCleanupAuditResult` class and the `ProjectCleanupAudit.AuditProject` method to ensure it returns the correct structure.
2. **Manual Testing:** Manually run the audit on a sample project file and verify that the output JSON matches the expected structure.

### API Neediness Judgment:
- No external API/Revit API/Navisworks API is required for this task. The logic can be implemented using pure C# without any dependencies on Revit APIs.

### Next Draft Task:
- Implement the actual audit logic to populate the result object with accurate data from the project file.
- Ensure that the code adheres to the specified architecture and design principles, focusing on testability and maintainability.

## 연결

- [[Qwen Draft Index]]
- [[Qwen Development Boundary]]
- [[Revit API Test Gate Index]]
- [[Build Test Index]]
