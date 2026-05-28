from __future__ import annotations

import datetime
import os
from pathlib import Path

from backend.core.paths import DATA_DIR, PROJECT_ROOT
from backend.models import KnowledgeUpdateRequest

ORGANIZATION = {
    "MANAGEMENT": ["CEO", "조율차장"],
    "ESTIMATION_TEAM": ["건축", "구조", "토목"],
    "ENGINEERING_TEAM": ["공조배관", "공조덕트", "소방기계", "소방전기", "전기"],
    "REPORTING_TEAM": ["위생", "통신"],
    "ADDIN_DEVELOPMENT_TEAM": ["요구사항분석", "Revit_Addin", "Navisworks_Addin", "빌드검증", "배포문서"],
    "STORE_COMMERCIALIZATION_TEAM": ["제품패키징", "스토어심사", "라이선스결제", "고객지원 CS"],
    "ADMIN_FINANCE_TEAM": ["경영지원", "경비정산_AI"],
    "PEOPLE_ENABLEMENT_TEAM": ["HR_인재분석관", "교육컨설팅", "러닝콘텐츠디자이너"],
    "KNOWLEDGE_TEAM": ["지식업데이트", "지식큐레이터"],
}

ALL_AGENTS = [agent for team_agents in ORGANIZATION.values() for agent in team_agents]

DISCIPLINE_GROUPS = {
    "공통": [],
    "건축": ["건축"],
    "구조": ["구조"],
    "토목": ["토목"],
    "위생": ["위생"],
    "공조배관": ["공조배관"],
    "공조덕트": ["공조덕트"],
    "소방기계": ["소방기계"],
    "소방전기": ["소방전기"],
    "전기": ["전기"],
    "통신": ["통신"],
    "MEP통합": ["위생", "공조배관", "공조덕트", "소방기계", "소방전기", "전기", "통신"],
    "전체공정": ["건축", "구조", "토목", "위생", "공조배관", "공조덕트", "소방기계", "소방전기", "전기", "통신"],
}

DISCIPLINE_KEYWORDS = {
    "건축": ["건축", "천장고", "방화구획", "마감", "실면적", "문짝", "문틀", "벽체",
             "면적", "연면적", "바닥면적", "건축면적", "층수", "층고", "공항", "터미널",
             "여객터미널", "청사", "공공건물", "건물규모", "시설규모"],
    "구조": ["구조", "구조보", "기둥", "슬래브", "전이보", "타공", "관통", "보강"],
    "토목": ["토목", "대지", "외부 인입", "gl", "관로", "우수", "오수"],
    "위생": ["위생", "급수", "배수", "오배수", "구배", "펌프", "위생배관"],
    "공조배관": ["공조배관", "냉온수", "냉수", "온수", "냉각수", "냉매", "증기", "응축수", "브라인", "글리콜", "chw", "chws", "chwr", "hw", "hws", "hwr", "cw", "cws", "cwr", "ref", "stm", "cond", "배관", "밸브", "단열"],
    "공조덕트": ["공조덕트", "덕트", "풍량", "정압", "제연덕트"],
    "소방기계": ["소방기계", "스프링클러", "소화", "소방배관", "헤드"],
    "소방전기": ["소방전기", "감지기", "발신기", "수신기", "방재"],
    "전기": ["전기", "케이블", "트레이", "분전반", "전력", "강전"],
    "통신": ["통신", "약전", "네트워크", "cctv", "방송", "통신트레이",
             "mdf", "idf", "lan", "광케이블", "utp", "cat6", "광선로", "배선반"],
}

KNOWLEDGE_DIR = os.environ.get("KNOWLEDGE_BASE_DIR", str(DATA_DIR / "knowledge_base"))
QA_KNOWLEDGE_DIR = str(DATA_DIR / "knowledge_base" / "qa")

EXTRA_KNOWLEDGE_AGENTS = {
    "최고전략 (CSO)", "파이프라인_오케스트레이터", "Caveman_토큰다이어터",
    "프로그램개발", "QA_테스터", "테크니컬_라이터", "라이선스_보안관",
    "COO", "CFO", "아이디어발굴", "전략기획", "프로젝트분석", "브랜드마케팅",
    "고객지원 CS", "CS_기술지원관", "협력사안부", "법무조항검토", "견적심사원",
    "EIR/BEP_심사원", "BIM_템플릿기획관", "프롬프트엔지니어", "글로벌_유통기획관",
    "엔지니어링계산서", "외주관리", "견적서담당", "글로벌_매출관리원",
    "경영지원", "교육컨설팅", "러닝콘텐츠디자이너", "엑셀자동화", "지식큐레이터",
    "인프라_DevOps (Obsidian)", "Qwen_Coder_8B", "Dynamo",
}

KNOWLEDGE_AGENTS = sorted(set(ALL_AGENTS) | EXTRA_KNOWLEDGE_AGENTS | set(DISCIPLINE_KEYWORDS) | {
    "Revit_Addin", "Navisworks_Addin", "요구사항분석", "빌드검증", "배포문서",
    "제품패키징", "스토어심사", "라이선스결제", "고객지원 CS",
})

DEFAULT_KNOWLEDGE = {
    "건축": "천장고, 피난/방화구획, 실 사용성, 마감 두께, 유지관리 접근성을 Add-in 요구사항 검토 기준으로 둔다.",
    "구조": "보/기둥/슬래브 관통, 전이보, 개구부 보강 가능 여부와 구조 검토 승인 필요 여부를 우선 판단한다.",
    "토목": "외부 인입 레벨, 대지 경계, 우수/오수 관로, GL/FL 관계와 건축/MEP 접속 조건을 함께 검토한다.",
    "위생": "배수 구배, 통기관, 유지관리 공간, 펌프/집수정 연계와 관경별 간섭 우선순위를 반영한다.",
    "공조배관": "단열 포함 외경, 밸브 조작 공간, 플랜지/유니온 유지관리, 냉온수/냉매 배관의 레이어를 확인한다.",
    "공조덕트": "덕트 사이즈, 풍량/정압, 점검구, 소음/진동, 제연덕트 우선순위를 보고서 항목에 포함한다.",
    "소방기계": "스프링클러 헤드 살수반경, 배관 레이어, 소방법 민감 구간, 알람밸브/펌프 연계 조건을 확인한다.",
    "소방전기": "감지기 배치, 방재 신호, 방화셔터/제연 연동, 배선 경로와 유지관리 접근성을 검토한다.",
    "전기": "케이블 트레이 폭/높이, 곡률 반경, 누수 회피, 강전/약전 이격과 분전반 접근 공간을 우선한다.",
    "통신": "약전 트레이, 네트워크/CCTV/방송 배선, 전력선 이격, MDF/IDF 접근성을 요구사항에 반영한다.",
}


def knowledge_file_path(agent: str) -> str:
    safe_name = "".join(ch for ch in agent if ch.isalnum() or ch in ("_", "-"))
    return os.path.join(KNOWLEDGE_DIR, f"{safe_name}.md")


def qa_knowledge_file_path(agent: str) -> str:
    safe_name = "".join(ch for ch in agent if ch.isalnum() or ch in ("_", "-"))
    return os.path.join(QA_KNOWLEDGE_DIR, f"{safe_name}_QA.md")


def ensure_knowledge_base() -> None:
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
    os.makedirs(QA_KNOWLEDGE_DIR, exist_ok=True)
    for agent, seed in DEFAULT_KNOWLEDGE.items():
        path = knowledge_file_path(agent)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as kb_file:
                kb_file.write(f"# {agent} 지식 베이스\n\n## 초기 기준\n{seed}\n")


def _is_qa_update(source: str, tags: str) -> bool:
    src = source.lower()
    tag_set = {tag.strip() for tag in tags.lower().split(",")}
    if "manual-knowledge" in tag_set:
        return False
    return (
        src.startswith("telegram-auto")
        or src.startswith("system-auto")
        or src == "telegram-qa"
        or "auto-collect" in tag_set
        or "needs-review" in tag_set
    )


def _extract_content_fingerprints(content: str) -> set[str]:
    fingerprints: set[str] = set()
    for line in content.splitlines():
        line = line.strip()
        if len(line) < 20:
            continue
        if any(marker in line for marker in ("http", "https", "[link]", "| ")):
            fingerprints.add(line[:120].lower())
        elif line.startswith("- ") and len(line) > 30:
            fingerprints.add(line[:120].lower())
    return fingerprints


def _is_duplicate_content(new_content: str, existing_text: str, threshold: float = 0.5) -> bool:
    new_fps = _extract_content_fingerprints(new_content)
    if not new_fps:
        return False
    existing_lower = existing_text.lower()
    matched = sum(1 for fp in new_fps if fp in existing_lower)
    return (matched / len(new_fps)) >= threshold


def append_knowledge_update(update: KnowledgeUpdateRequest) -> dict:
    if update.agent not in KNOWLEDGE_AGENTS:
        raise ValueError(f"지원하지 않는 지식 에이전트입니다: {update.agent}")
    if not update.content.strip():
        raise ValueError("지식 업데이트 내용이 비어 있습니다.")

    ensure_knowledge_base()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = qa_knowledge_file_path(update.agent) if _is_qa_update(update.source, update.tags) else knowledge_file_path(update.agent)

    try:
        existing_text = Path(path).read_text(encoding="utf-8") if Path(path).exists() else ""
        if existing_text and _is_duplicate_content(update.content, existing_text):
            return {"agent": update.agent, "path": path, "updated_at": now, "skipped": True, "reason": "duplicate"}
    except Exception:
        pass

    entry = (
        f"\n\n## {update.title.strip()} ({now})\n"
        f"- Source: {update.source.strip() or 'manual'}\n"
        f"- Tags: {update.tags.strip() or '-'}\n\n"
        f"{update.content.strip()}\n"
    )
    with open(path, "a", encoding="utf-8") as kb_file:
        kb_file.write(entry)
    return {"agent": update.agent, "path": path, "updated_at": now, "skipped": False}
