#!/usr/bin/env python3
"""1~2년차 MEP BIM Foundation 과정 일별 교육 메시지 Telegram 발송.

사용법:
  python daily_training_message.py --day 2
  python daily_training_message.py --day 2 --dry-run   # 실제 전송 없이 메시지 출력
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
USERS_FILE = PROJECT_ROOT / "data" / "team_requests" / "team_telegram_users.json"

# ────────────────────────────────────────────────
# 1년차 Foundation 과정 일별 커리큘럼
# 12주 과정을 일 단위로 매핑 (주 5일 기준)
# ────────────────────────────────────────────────
CURRICULUM: dict[int, dict] = {
    1: {
        "week": 1, "topic": "오리엔테이션 · 조직/보안 이해",
        "modules": ["M01 회사 문서 체계", "M06 보안/NDA"],
        "content": (
            "✅ 오늘 학습\n"
            "• 회사 문서번호·Revision·배포 등급 체계\n"
            "• 보안/NDA — 고객 자료 등급과 외부 공유 금지 기준\n"
        ),
        "practice": "회사 STD-011·STD-014 문서 읽고 핵심 3가지 메모",
        "tip": "모든 파일에는 Revision이 있어요. 'Rev.00' 이 초안, 'Rev.01'부터 검토·배포본입니다.",
    },
    2: {
        "week": 1, "topic": "CDE 기초 — WIP / Shared / Published",
        "modules": ["M02 CDE 기초"],
        "content": (
            "✅ 오늘 학습\n"
            "• WIP(작업중) → Shared(검토용) → Published(공식 배포) 3단계 구분\n"
            "• CDE 접속 방법과 폴더 구조\n"
            "• 제출대장: 파일명·버전·제출일 기록 방법\n"
        ),
        "practice": "CDE에 접속해 폴더 구조를 탐색하고, WIP 폴더에 연습 파일 1개 업로드해보세요.",
        "tip": "WIP 파일을 바로 Published로 올리면 안 돼요. 반드시 Shared 검토 단계를 거쳐야 합니다.",
    },
    3: {
        "week": 1, "topic": "CDE 실습 · 파일명 규칙",
        "modules": ["M01 회사 문서 체계", "M02 CDE 기초"],
        "content": (
            "✅ 오늘 학습\n"
            "• 파일명 규칙: 프로젝트-공종-구역-Revision\n"
            "• 제출대장 XLSX 샘플 작성\n"
            "• 잘못된 파일명 사례 식별 훈련\n"
        ),
        "practice": "샘플 파일 5개의 파일명을 규칙에 맞게 수정해서 제출대장에 기록하세요.",
        "tip": "파일명에 한글·공백·특수문자는 가급적 쓰지 마세요. 협업 시 오류 원인이 됩니다.",
    },
    4: {
        "week": 2, "topic": "Revit MEP 인터페이스·뷰",
        "modules": ["M03 Revit MEP 기본"],
        "content": (
            "✅ 오늘 학습\n"
            "• Revit 인터페이스: 리본, 프로젝트 브라우저, 특성 창\n"
            "• 뷰 유형: 평면도·단면도·3D 뷰\n"
            "• 링크 모델 불러오기와 가시성 설정\n"
        ),
        "practice": "연습 Revit 파일을 열고 평면도·3D 뷰 전환, 건축 링크 모델 가시성 켜고 끄기를 실습하세요.",
        "tip": "View Template을 미리 적용하면 뷰마다 설정을 반복하지 않아도 됩니다.",
    },
    5: {
        "week": 2, "topic": "Revit MEP 카테고리·패밀리·시스템",
        "modules": ["M03 Revit MEP 기본"],
        "content": (
            "✅ 오늘 학습\n"
            "• MEP 카테고리: 덕트·배관·전선관·케이블트레이·기계장비\n"
            "• 패밀리와 타입의 차이\n"
            "• 시스템(System) 이름과 색상 구분\n"
        ),
        "practice": "연습 모델에서 덕트 1개를 선택해 카테고리·패밀리·시스템명·주요 파라미터를 확인해보세요.",
        "tip": "시스템명이 잘못 지정되면 물량 산출과 간섭 보고에서 오류가 납니다. 처음부터 정확히 설정하세요.",
    },
    6: {
        "week": 2, "topic": "MEP 도면 읽기",
        "modules": ["M04 MEP 도면 읽기"],
        "content": (
            "✅ 오늘 학습\n"
            "• 공조덕트 기호: SA·RA·EA·OA 구분\n"
            "• 배관 선종: 냉수·온수·냉각수·냉매\n"
            "• 소방 기호: 스프링클러 헤드, 알람밸브, 송수구\n"
            "• 전기 기호: 트레이, 분전반, 조명·콘센트 범례\n"
        ),
        "practice": "샘플 도면 1장에서 공종별 기호를 10개 이상 찾아 이름과 의미를 기록하세요.",
        "tip": "도면 범례(Legend)를 먼저 보면 낯선 기호를 빠르게 파악할 수 있습니다.",
    },
    7: {
        "week": 3, "topic": "좌표·레벨·그리드 기준 이해",
        "modules": ["M05 모델 품질 기초"],
        "content": (
            "✅ 오늘 학습\n"
            "• 프로젝트 기준점(Project Base Point)과 측량 기준점(Survey Point)\n"
            "• 레벨(Level)과 그리드(Grid) 확인 방법\n"
            "• 좌표가 틀렸을 때 발생하는 문제 사례\n"
        ),
        "practice": "연습 모델에서 Project Base Point를 확인하고, 링크 모델 좌표와 일치하는지 체크리스트로 기록하세요.",
        "tip": "좌표 불일치는 간섭 보고 오류의 가장 흔한 원인입니다. 모델링 전에 반드시 확인하세요.",
    },
    8: {
        "week": 3, "topic": "공조덕트·배관 기초 모델링",
        "modules": ["M03 Revit MEP 기본", "M04 MEP 도면 읽기"],
        "content": (
            "✅ 오늘 학습\n"
            "• 공조덕트 배치: 사각·원형 덕트, 엘보·티·전이관\n"
            "• 배관 배치: 관경 선택, 단열재 포함 외경 확인\n"
            "• 천장고 여유 공간 확인 방법\n"
        ),
        "practice": "소형 기계실 도면을 보고 공조덕트 주요 경로와 배관 1개 계통을 모델링하세요.",
        "tip": "덕트 배치 후 단면도(Section)를 잘라서 천장고 여유를 반드시 확인하세요.",
    },
    9: {
        "week": 4, "topic": "위생·소방·전기 기초 모델링",
        "modules": ["M03 Revit MEP 기본"],
        "content": (
            "✅ 오늘 학습\n"
            "• 위생: 급수·배수·통기 배치, 배수 구배 설정\n"
            "• 소방: 스프링클러 헤드 배치, 방호 반경 확인\n"
            "• 전기: 케이블트레이 배치, 강전·약전 구분\n"
        ),
        "practice": "샘플 천장 평면도에서 위생·소방·전기 요소를 각 1개 계통씩 모델링해보세요.",
        "tip": "배수 배관은 반드시 구배를 설정해야 합니다. Revit에서 기울기(Slope) 값을 입력하세요.",
    },
    10: {
        "week": 4, "topic": "Navisworks 기본 — 통합 모델·Clash",
        "modules": ["M05 모델 품질 기초"],
        "content": (
            "✅ 오늘 학습\n"
            "• NWD/NWC 파일 형식 차이\n"
            "• 모델 Append(붙이기)와 공종별 색상 설정\n"
            "• Clash Detective: 테스트 설정, 결과 열람\n"
        ),
        "practice": "연습 NWD 파일을 열고 덕트-구조 Clash 결과를 확인해 이슈 3건을 기록하세요.",
        "tip": "Clash 결과는 Critical/High/Medium/Low로 분류합니다. 처음엔 Hard Clash(실제 겹침)만 집중하세요.",
    },
    11: {
        "week": 5, "topic": "모델 품질 체크 — 명명·파라미터",
        "modules": ["M05 모델 품질 기초"],
        "content": (
            "✅ 오늘 학습\n"
            "• 필수 파라미터 목록: 시스템명·ItemCode·단열두께\n"
            "• 명명 규칙 위반 사례 식별\n"
            "• 체크리스트 기반 자체 품질 점검 방법\n"
        ),
        "practice": "연습 모델에서 필수 파라미터 누락 요소를 10개 이상 찾아 체크리스트에 기록하세요.",
        "tip": "처음부터 파라미터를 입력하는 습관을 만드세요. 나중에 일괄 수정은 시간이 몇 배 걸립니다.",
    },
    12: {
        "week": 5, "topic": "AI 활용 기초",
        "modules": ["M07 AI 기본 사용"],
        "content": (
            "✅ 오늘 학습\n"
            "• AI 질문법: 도면 용어 정리, 체크리스트 초안 생성\n"
            "• AI 결과는 반드시 검토·수정 후 사용\n"
            "• AI로 만들면 안 되는 것: 설계 기준·법규 판단\n"
        ),
        "practice": "AI를 사용해 공조덕트 용어집 10개를 생성하고, 내용을 직접 검토·수정해서 제출하세요.",
        "tip": "AI는 초안 생성 도구입니다. AI 답변을 그대로 납품하면 안 됩니다. 항상 검토 흔적을 남기세요.",
    },
    13: {
        "week": 6, "topic": "Excel/CSV 기본 — 제출대장·파일 목록",
        "modules": ["M08 Excel/CSV 기본"],
        "content": (
            "✅ 오늘 학습\n"
            "• Excel 필터·중복 제거·조건부 서식\n"
            "• 제출대장 자동 번호 채우기\n"
            "• CSV 인코딩(UTF-8) 확인 방법\n"
        ),
        "practice": "파일 목록 CSV를 Excel로 열어 공종별로 필터링하고, 제출대장 형식으로 변환하세요.",
        "tip": "Excel 파일은 저장 전에 항상 다른 이름으로 백업 사본을 만드세요.",
    },
    14: {
        "week": 6, "topic": "중간 점검 · Q&A",
        "modules": ["전 모듈 복습"],
        "content": (
            "✅ 오늘 학습\n"
            "• 1~6주차 핵심 개념 복습\n"
            "• 어렵거나 헷갈렸던 내용 질문\n"
            "• 지금까지 만든 산출물 셀프 점검\n"
        ),
        "practice": "지금까지 만든 모든 산출물을 CDE WIP 폴더에 정리하고, 파일명·Revision을 점검하세요.",
        "tip": "모르는 게 있으면 지금이 질문할 타이밍입니다. 혼자 고민하지 마세요!",
    },
}


def load_users() -> list[dict]:
    with open(USERS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("users", [])


def send_telegram(token: str, chat_id: str, text: str) -> bool:
    payload = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }).encode("utf-8")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"  telegram=sent chat_id={chat_id} status={resp.status}")
            return True
    except Exception as exc:
        print(f"  telegram=failed chat_id={chat_id} {type(exc).__name__}: {exc}")
        return False


def build_message(name: str, day: int) -> str:
    info = CURRICULUM.get(day)
    if not info:
        return (
            f"안녕하세요, {name}님!\n\n"
            f"📚 MEP BIM Foundation 과정 {day}일차입니다.\n"
            "오늘도 화이팅입니다! 궁금한 점은 언제든지 질문해주세요."
        )

    lines = [
        f"안녕하세요, {name}님! 👋",
        f"",
        f"📚 <b>MEP BIM Foundation 과정 — {day}일차</b>",
        f"📅 {info['week']}주차 | {info['topic']}",
        f"",
        info["content"].rstrip(),
        f"",
        f"🛠 <b>오늘 실습</b>",
        f"{info['practice']}",
        f"",
        f"💡 <b>Tip</b>",
        f"{info['tip']}",
        f"",
        f"궁금한 점은 여기서 바로 질문해주세요! 🙌",
    ]
    return "\n".join(lines)


def run(day: int, dry_run: bool = False) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        print("ERROR: TELEGRAM_BOT_TOKEN 환경 변수가 없습니다.")
        return

    users = load_users()
    # 교육 대상자 4명만 필터 (role 미지정 = 교육 대상)
    targets = [
        u for u in users
        if u.get("telegram_chat_id") and u.get("name") in {"최정연", "오수빈", "김선정", "허진석"}
    ]

    print(f"[daily_training_message] day={day} dry_run={dry_run} targets={len(targets)}")

    for user in targets:
        name = user["name"]
        chat_id = user["telegram_chat_id"]
        message = build_message(name, day)

        print(f"\n── {name} (chat_id={chat_id}) ──")
        print(message)

        if not dry_run:
            send_telegram(token, chat_id, message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Daily MEP BIM training message sender")
    parser.add_argument("--day", type=int, required=True, help="교육 일차 (예: 2)")
    parser.add_argument("--dry-run", action="store_true", help="실제 전송 없이 메시지만 출력")
    args = parser.parse_args()
    run(day=args.day, dry_run=args.dry_run)
