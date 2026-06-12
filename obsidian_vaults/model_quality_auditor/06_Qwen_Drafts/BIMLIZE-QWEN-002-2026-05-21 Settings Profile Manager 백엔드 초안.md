---
type: qwen-product-draft
project: Model Quality Auditor
task_id: BIMLIZE-QWEN-002
status: generated
created: 2026-05-21
tags:
  - qwen
  - mqa
  - backend-draft
  - product-development
---

# BIMLIZE-QWEN-002 Settings Profile Manager 백엔드 초안

선정 아이템: BIMlize 기능 범위 내재화 - Phase 1 Simple Features

## 작업 정보

| 항목 | 내용 |
|---|---|
| 산출물 | JSON 설정 프로필 저장/불러오기, 버전 검증, office/project profile 분리, 깨진 프로필 거부 로직 |
| 범위 | Non-Revit core only. 모델 변경 없음. 모든 명령의 설정 백본으로 사용. |
| 예상 출력 위치 | `backend/bim_command_center/settings_profiles.py` |
| Qwen 실행 | 성공 |
| 모델 | qwen2.5-coder:7b |
| 사유 | - |

## Qwen 초안

### Plan:
**목적**: Settings Profile Manager 백엔드 초안을 작성하여 설정 프로필 저장/불러오기, 버전 검증, office/project profile 분리, 깨진 프로필 거부 로직을 구현합니다.

**입력**: JSON 형식의 설정 프로필

**출력**: JSON 파일에 설정 프로필 저장 및 불러오기 기능, 버전 검증 로직, office/project profile 분리 로직, 깨진 프로필 거부 로직

**제외 범위**: Revit API 의존 코드

### Draft:
```python
import json
from typing import Dict, Any

class SettingsProfileManager:
    def __init__(self):
        self.office_profile = {}
        self.project_profile = {}

    def save_profile(self, profile: Dict[str, Any], is_project: bool) -> None:
        if is_project:
            self.project_profile = profile
        else:
            self.office_profile = profile
        with open('settings_profiles.json', 'w') as f:
            json.dump(profile, f)

    def load_profile(self, is_project: bool) -> Dict[str, Any]:
        try:
            with open('settings_profiles.json', 'r') as f:
                profiles = json.load(f)
                if is_project:
                    return profiles.get('project_profile', {})
                else:
                    return profiles.get('office_profile', {})
        except FileNotFoundError:
            return {}

    def validate_version(self, profile: Dict[str, Any]) -> bool:
        current_version = '1.0'
        return profile.get('version', '') == current_version

    def reject_broken_profile(self, profile: Dict[str, Any]) -> None:
        if not self.validate_version(profile):
            raise ValueError("Broken profile detected")

# Example usage
manager = SettingsProfileManager()
profile = {'version': '1.0', 'settings': {}}
manager.save_profile(profile, is_project=False)
loaded_profile = manager.load_profile(is_project=False)
print(loaded_profile)
```

### Verification:
1. **단위 테스트**: `SettingsProfileManager` 클래스의 각 메서드를 단위 테스트로 검증합니다.
   - `save_profile`: 저장된 JSON 파일이 올바른 내용을 가진지 확인
   - `load_profile`: 불러온 JSON 파일이 올바른 내용을 가진지 확인
   - `validate_version`: 버전 검증 로직이 올바르게 작동하는지 확인
   - `reject_broken_profile`: 깨진 프로필 거부 로직이 올바르게 작동하는지 확인

2. **통합 테스트**: 설정 프로필을 저장하고 불러오는 과정에서 데이터의 일관성을 검증합니다.

### API 필요성 판단:
- 외부 API/Revit API/Navisworks API 필요 여부: No
  - 모든 기능은 순수 C# 로직으로 구현 가능

### Next Draft Task:
1. **로컬 검증**: 작성한 초안을 로컬 환경에서 테스트하여 버그를 확인합니다.
2. **문서화**: 초안에 대한 문서를 작성하고, QA 체크리스트를 준비합니다.
3. **다음 작업 연결**: Telegram 중간보고 및 다음 큐 작업으로 자연스럽게 이어갑니다.

## 연결

- [[Qwen Draft Index]]
- [[Qwen Development Boundary]]
- [[Revit API Test Gate Index]]
- [[Build Test Index]]
