#!/usr/bin/env python3
"""Validate per-agent Q&A quality in knowledge/20_qa.

This script checks the stored Q&A pairs for each AI agent, then reports
agent-level quality scores and concrete improvement targets.

Usage:
  .dev-venv/bin/python scripts/validate_agent_qa_quality.py
  .dev-venv/bin/python scripts/validate_agent_qa_quality.py --agent 고객지원CS
  .dev-venv/bin/python scripts/validate_agent_qa_quality.py --verbose --no-save
  .dev-venv/bin/python scripts/validate_agent_qa_quality.py --no-save --min-score 96 --min-pass-rate 100
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.core.paths import LOGS_DIR, QA_KB_DIR  # noqa: E402

TODAY = dt.date.today().isoformat()
LOG_DIR = LOGS_DIR / "agent_qa_quality"
LOG_DIR.mkdir(parents=True, exist_ok=True)

QUESTION_RE = re.compile(r"^\s*(?:#+\s*)?(?:\*\*)?Q\s*:\s*(.+?)(?:\*\*)?\s*$", re.IGNORECASE)
ANSWER_RE = re.compile(r"^\s*(?:\*\*)?A\s*:\s*(.+)$", re.IGNORECASE)

NUMERIC_RE = re.compile(
    r"(\d+\.?\d*\s*(mm|cm|m|m/s|m³|%|일|시간|회|점|℃|dn\d+|lod|p[1-3]|kst\d+)|1/\d+)",
    re.IGNORECASE,
)
EVIDENCE_RE = re.compile(
    r"(kst\d+|nftc|nfpc|kec|kds|ks\b|bep|eir|lod|ifc|autodesk|revit|navisworks|"
    r"국토부|건축법|소방법|운영 기준|source|tags)",
    re.IGNORECASE,
)
CONDITION_WORDS = (
    "경우", "조건", "단,", "다만", "우선", "먼저", "반면", "예외", "불가", "가능",
    "확인", "구분", "분리", "필요", "최우선",
)
# 한국어 최빈 조건형(용언 어간 + '~면'). 명사형 '면'(반면·표면·화면·측면)과 구분하려
# 흔한 용언 결합형만 명시 매칭한다(부분문자열 오검출 방지).
CONDITION_SUFFIX_RE = re.compile(
    r"(하면|되면|있으면|없으면|다르면|같으면|아니면|맞으면|틀리면|낮으면|높으면|"
    r"초과하면|미만이면|이상이면|이하이면|명확하면|불명확하면|어긋나면|넘으면)"
)
ACTION_WORDS = (
    "확인", "요청", "기록", "공유", "전달", "검토", "분류", "추가", "재시도",
    "보고", "문의", "안내", "정리",
    # 실무 답변에 흔한 액션 동사(누락분 보강) — 산문형 절차 답변 과소평가 교정.
    "질의", "대조", "비교", "산정", "남기", "남긴", "제시", "표시", "반영",
    "협의", "결정", "지정", "설정", "점검",
)
# 산문형 구조 마커: 번호·불릿이 없어도 논리 구획이 뚜렷한 답변을 인정한다.
PROSE_STRUCTURE_MARKERS = (
    "결론", "적용 범위", "적용범위", "반면", "다만", "먼저", "우선",
    "후보로", "후보,", "→", "그다음", "이때", "단계", "기준은",
)
RISK_WORDS = (
    "위험", "리스크", "주의", "민감", "보안", "개인정보", "법적", "확정하지", "승인",
    "책임", "누수", "충돌", "오류", "차단",
)
TRACEABILITY_RE = re.compile(
    r"(담당|기한|로그|승인|bcf|rfi|검토자|owner|due|status|상태|기록)",
    re.IGNORECASE,
)
NOISE_WORDS = (
    "telegram-auto-search", "자동 수집 결과", "[tavily]", "[ddg]", "출처: http",
    "needs-review", "auto-collect",
)


def parse_pairs(path: Path) -> list[dict]:
    """Extract Q/A pairs from an agent *_QA.md file."""
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    pairs: list[dict] = []
    current_question: str | None = None
    current_answer: list[str] = []
    current_line = 0

    def flush() -> None:
        nonlocal current_question, current_answer, current_line
        if current_question is None:
            return
        answer = "\n".join(current_answer).strip()
        pairs.append({
            "question": current_question.strip(),
            "answer": answer,
            "line": current_line,
        })
        current_question = None
        current_answer = []
        current_line = 0

    for lineno, line in enumerate(lines, 1):
        q_match = QUESTION_RE.match(line)
        if q_match:
            flush()
            current_question = q_match.group(1).strip()
            current_answer = []
            current_line = lineno
            continue

        if current_question is None:
            continue

        a_match = ANSWER_RE.match(line)
        if a_match and not current_answer:
            current_answer.append(a_match.group(1).strip())
            continue

        if line.startswith("**Q:") or line.startswith("## Q:"):
            flush()
            continue

        current_answer.append(line)

    flush()
    return [p for p in pairs if p["question"] or p["answer"]]


def score_pair(question: str, answer: str) -> dict:
    """Score one Q&A pair on a 100-point practical quality rubric."""
    q = question.strip()
    a = answer.strip()
    combined_lower = f"{q}\n{a}".lower()
    answer_lower = a.lower()

    question_score = 0
    if len(q) >= 10:
        question_score += 8
    if any(token in q for token in ("?", "나요", "인가", "뭐", "어떻게", "기준", "차이")):
        question_score += 7

    answer_score = 0
    if len(a) >= 80:
        answer_score += 10
    if len(a) >= 180:
        answer_score += 5

    structure_score = 0
    # 명시적 번호·불릿 리스트 또는 산문형 논리 구획(마커 2개 이상) 중 하나면 인정.
    has_list = bool(re.search(r"①|②|③|1\.|2\.|3\.|- ", a))
    prose_marker_hits = sum(1 for m in PROSE_STRUCTURE_MARKERS if m in a)
    if has_list or prose_marker_hits >= 2:
        structure_score += 8
    if ":" in a or "—" in a or "->" in a:
        structure_score += 4

    evidence_score = 0
    if EVIDENCE_RE.search(a):
        evidence_score += 12
    if NUMERIC_RE.search(a):
        evidence_score += 8

    condition_hits = sum(1 for word in CONDITION_WORDS if word in answer_lower)
    condition_hits += len(CONDITION_SUFFIX_RE.findall(a))
    condition_score = min(condition_hits * 4, 15)

    action_hits = sum(1 for word in ACTION_WORDS if word in answer_lower)
    action_score = min(action_hits * 3, 10)

    risk_hits = sum(1 for word in RISK_WORDS if word in combined_lower)
    risk_score = min(risk_hits * 4, 10)

    traceability_score = 3 if TRACEABILITY_RE.search(a) else 0

    noise_penalty = min(sum(8 for word in NOISE_WORDS if word.lower() in combined_lower), 20)
    missing = []
    if question_score < 10:
        missing.append("질문 의도 구체화")
    if answer_score < 12:
        missing.append("답변 길이/설명량")
    if structure_score < 8:
        missing.append("구조화")
    if evidence_score < 12:
        missing.append("근거/수치/기준")
    if condition_score < 8:
        missing.append("조건 분기")
    if action_score < 6:
        missing.append("다음 액션")
    if risk_score < 4:
        missing.append("리스크/책임 경계")
    if traceability_score < 3:
        missing.append("담당자/기한/승인 로그 추적성")
    if noise_penalty:
        missing.append("자동수집 노이즈 제거")

    total = (
        question_score
        + answer_score
        + structure_score
        + evidence_score
        + condition_score
        + action_score
        + risk_score
        + traceability_score
        - noise_penalty
    )
    total = max(0, min(100, total))

    return {
        "total": total,
        "question": question_score,
        "answer": answer_score,
        "structure": structure_score,
        "evidence": evidence_score,
        "condition": condition_score,
        "action": action_score,
        "risk": risk_score,
        "traceability": traceability_score,
        "noise_penalty": -noise_penalty,
        "missing": missing,
    }


def evaluate_agent(path: Path, min_score: int) -> dict:
    agent = path.stem.removesuffix("_QA")
    pairs = parse_pairs(path)
    scored_pairs = []

    for pair in pairs:
        quality = score_pair(pair["question"], pair["answer"])
        scored_pairs.append({**pair, "quality": quality, "passed": quality["total"] >= min_score})

    if scored_pairs:
        scores = [p["quality"]["total"] for p in scored_pairs]
        avg = int(sum(scores) / len(scores))
        min_pair_score = min(scores)
        pass_count = sum(1 for p in scored_pairs if p["passed"])
    else:
        avg = 0
        min_pair_score = 0
        pass_count = 0

    low_pairs = sorted((p for p in scored_pairs if not p["passed"]), key=lambda p: p["quality"]["total"])
    return {
        "agent": agent,
        "path": str(path.relative_to(PROJECT_ROOT)),
        "pair_count": len(scored_pairs),
        "avg": avg,
        "min": min_pair_score,
        "pass_count": pass_count,
        "passed": bool(scored_pairs) and avg >= min_score and pass_count == len(scored_pairs),
        "low_pairs": low_pairs[:5],
        "pairs": scored_pairs,
    }


def run(agent_filter: str | None, min_score: int) -> dict:
    qa_files = sorted(QA_KB_DIR.glob("*_QA.md"))
    if agent_filter:
        qa_files = [p for p in qa_files if agent_filter.lower() in p.stem.lower()]

    agents = [evaluate_agent(path, min_score) for path in qa_files]
    agents.sort(key=lambda item: (item["avg"], item["agent"]))

    total_pairs = sum(a["pair_count"] for a in agents)
    passed_pairs = sum(a["pass_count"] for a in agents)
    avg_score = int(sum(a["avg"] for a in agents) / len(agents)) if agents else 0
    pass_rate = int(passed_pairs / total_pairs * 100) if total_pairs else 0

    return {
        "date": TODAY,
        "min_score": min_score,
        "agent_count": len(agents),
        "total_pairs": total_pairs,
        "passed_pairs": passed_pairs,
        "pass_rate": pass_rate,
        "avg_score": avg_score,
        "agents": agents,
    }


def verdict(avg: int, pair_count: int, pass_count: int) -> str:
    if pair_count == 0:
        return "NO_QA"
    if avg >= 80 and pass_count == pair_count:
        return "PASS"
    if avg >= 65:
        return "WARN"
    return "FAIL"


def build_report(result: dict) -> str:
    lines = [
        "# Agent Q&A Quality Report",
        "",
        f"실행일: {result['date']} | 기준점수: {result['min_score']}점 | "
        f"에이전트: {result['agent_count']}개 | Q&A: {result['passed_pairs']}/{result['total_pairs']} 통과 "
        f"({result['pass_rate']}%) | 평균: {result['avg_score']}점",
        "",
        "## Agent Summary",
        "",
        "| Agent | Q&A | Avg | Min | Pass | Verdict |",
        "|---|---:|---:|---:|---:|---|",
    ]

    for agent in result["agents"]:
        lines.append(
            f"| {agent['agent']} | {agent['pair_count']} | {agent['avg']} | {agent['min']} | "
            f"{agent['pass_count']}/{agent['pair_count']} | "
            f"{verdict(agent['avg'], agent['pair_count'], agent['pass_count'])} |"
        )

    weak_agents = [a for a in result["agents"] if a["low_pairs"] or a["pair_count"] == 0]
    if weak_agents:
        lines += ["", "## Improvement Targets", ""]
        for agent in weak_agents[:20]:
            lines.append(f"### {agent['agent']} ({agent['avg']}점)")
            if agent["pair_count"] == 0:
                lines.append("- Q&A 쌍이 없습니다. 최소 3개 이상의 실제 질문/답변을 추가하세요.")
                lines.append("")
                continue
            for pair in agent["low_pairs"][:3]:
                missing = ", ".join(pair["quality"]["missing"]) or "심화 보강"
                q_preview = pair["question"].replace("|", "/")[:90]
                lines.append(
                    f"- line {pair['line']} | {pair['quality']['total']}점 | {q_preview}"
                )
                lines.append(f"  개선: {missing}")
            lines.append("")

    lines += [
        "## Rubric",
        "",
        "- 질문 명확성 15점",
        "- 답변 설명량 15점",
        "- 구조화 12점",
        "- 근거/수치/기준 20점",
        "- 조건 분기 15점",
        "- 다음 액션 10점",
        "- 리스크/책임 경계 10점",
        "- 담당자/기한/승인 로그 추적성 3점",
        "- 자동수집 노이즈 최대 -20점",
    ]
    return "\n".join(lines)


def exit_code_for_rate(pass_rate: int, min_pass_rate: int) -> int:
    return 0 if pass_rate >= min_pass_rate else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate per-agent Q&A quality.")
    parser.add_argument("--agent", help="특정 agent만 검사합니다. 예: 고객지원CS")
    parser.add_argument("--min-score", type=int, default=70, help="Q&A 쌍 통과 기준 점수")
    parser.add_argument("--min-pass-rate", type=int, default=70, help="전체 Q&A 통과율 하한 %")
    parser.add_argument("--no-save", action="store_true", help="리포트를 파일로 저장하지 않습니다.")
    parser.add_argument("--verbose", "-v", action="store_true", help="저품질 Q&A 세부 정보를 출력합니다.")
    args = parser.parse_args()

    result = run(args.agent, args.min_score)
    report = build_report(result)
    print(report)

    if args.verbose:
        for agent in result["agents"]:
            for pair in agent["low_pairs"]:
                print()
                print(f"[{agent['agent']}] line {pair['line']} score={pair['quality']['total']}")
                print(f"Q: {pair['question']}")
                print(f"missing: {', '.join(pair['quality']['missing'])}")

    if not args.no_save:
        md_path = LOG_DIR / f"agent_qa_quality_{TODAY}.md"
        json_path = LOG_DIR / f"agent_qa_quality_{TODAY}.json"
        md_path.write_text(report, encoding="utf-8")
        json_path.write_text(
            json.dumps(
                {k: v for k, v in result.items() if k != "agents"} | {
                    "agents": [
                        {k: v for k, v in agent.items() if k != "pairs"}
                        for agent in result["agents"]
                    ]
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print()
        print(f"report: {md_path}")
        print(f"json:   {json_path}")

    if result["pass_rate"] < args.min_pass_rate:
        print(f"FAIL: Q&A 통과율 {result['pass_rate']}% < 기준 {args.min_pass_rate}%")

    sys.exit(exit_code_for_rate(result["pass_rate"], args.min_pass_rate))


if __name__ == "__main__":
    main()
