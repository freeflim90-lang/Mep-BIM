#!/usr/bin/env python3
# ================================================================
# main.py — OUTBOUND SALES BOT CLI
#
# 사용법:
#   python main.py crawl              # 구글맵 업체 수집 + DB 저장
#   python main.py extract            # 웹사이트에서 이메일 추출
#   python main.py send               # 제안 이메일 발송 (실제 발송)
#   python main.py send --dry-run     # 발송 내용 미리보기 (실제 발송 안함)
#   python main.py update             # 크롤링 + 이메일 추출 한번에
#   python main.py status             # 현재 DB 통계 출력
#   python main.py export             # CSV 파일로 전체 리스트 내보내기
# ================================================================
import argparse
import os
import sys
from datetime import datetime

from sheets_manager import sync_to_sheets, print_setup_guide
from db_manager import (
    init_db, upsert_company,
    get_companies_without_email,
    update_email,
    get_companies_to_contact,
    mark_contacted,
    get_stats,
    export_to_csv,
)
from crawler       import crawl, crawl_naver
from email_extractor import extract_emails_from_website, pick_best_email, search_email_via_ddg
from naver_search   import search_email_via_naver
from mailer        import send_bulk
from config        import BASE_DIR


# ── 커맨드 핸들러 ───────────────────────────────────────────────

def cmd_crawl(args):
    """구글맵에서 업체 수집 → DB 저장"""
    print("=" * 60)
    print("🔍 [CRAWL] 업체 수집 시작 (구글맵 + 네이버)")
    print("=" * 60)

    # 구글맵 Places API
    companies = crawl()

    # 네이버 지역 검색 병합 (API 키 설정 시 자동 실행)
    naver_companies = crawl_naver()
    companies.extend(naver_companies)
    print(f"\n[MERGE] 총 수집: {len(companies)}개 (구글맵 {len(companies)-len(naver_companies)} + 네이버 {len(naver_companies)})")

    inserted = updated = skipped = 0
    for c in companies:
        _, action = upsert_company(c)
        if action == "inserted":
            inserted += 1
        elif action == "updated":
            updated += 1
        else:
            skipped += 1

    print(f"\n[CRAWL 완료] 신규: {inserted} | 업데이트: {updated} | 중복: {skipped}")
    _print_stats()


def cmd_extract(args):
    """웹사이트 스캔으로 이메일 추출 → DB 업데이트"""
    print("=" * 60)
    print("📧 [EXTRACT] 이메일 추출 시작")
    print("=" * 60)

    targets = get_companies_without_email()
    if not targets:
        print("이메일 미수집 업체가 없습니다.")
        return

    print(f"대상: {len(targets)}개 업체\n")
    found_count = 0

    for company in targets:
        website = company.get("website", "")
        print(f"  🌐 {company['name']} — {website}")

        emails = extract_emails_from_website(website)

        # 폴백 1: 네이버 웹 검색
        if not emails:
            print(f"     🔎 네이버 검색 폴백...")
            emails = search_email_via_naver(company["name"])

        # 폴백 2: DuckDuckGo
        if not emails:
            print(f"     🔎 DDG 검색 폴백...")
            emails = search_email_via_ddg(company["name"])

        if emails:
            best = pick_best_email(emails)
            update_email(company["id"], best)
            print(f"     ✅ {best}")
            found_count += 1
        else:
            print(f"     ⚠️  이메일 미발견")

    print(f"\n[EXTRACT 완료] 이메일 수집: {found_count}/{len(targets)}개")
    _print_stats()


def cmd_send(args):
    """제안 이메일 발송"""
    dry_run = args.dry_run
    print("=" * 60)
    print(f"✉️  [SEND] 이메일 발송 시작{'  (DRY RUN — 실제 발송 안함)' if dry_run else ''}")
    print("=" * 60)

    targets = get_companies_to_contact()
    if not targets:
        print("발송 대상 업체가 없습니다. (이메일 있고 미발송인 업체 조회 결과 0건)")
        return

    print(f"발송 대상: {len(targets)}개 업체\n")

    result = send_bulk(targets, dry_run=dry_run)

    if not dry_run:
        # 발송 성공 업체 DB 상태 업데이트
        for company in targets:
            if company.get("email"):
                subject = f"[LUA BIM LABS] MEP BIM 협업 제안 — {company['name']} 귀중"
                mark_contacted(company["id"], subject, status="sent")

    print(f"\n[SEND 완료] 성공: {result['success']} | 실패: {result['fail']} | 건너뜀: {result['skip']}")
    if not dry_run:
        _print_stats()


def cmd_update(args):
    """크롤링 + 이메일 추출 한번에 실행 (신규 업체 추가 + 기존 업체 이메일 보완)"""
    print("=" * 60)
    print("🔄 [UPDATE] 업체 리스트 업데이트 시작")
    print("=" * 60)
    cmd_crawl(args)
    print()
    cmd_extract(args)


def cmd_status(args):
    """현재 DB 현황 출력"""
    print("=" * 60)
    print("📊 [STATUS] 현재 영업 DB 현황")
    print("=" * 60)
    _print_stats(verbose=True)


def cmd_export(args):
    """CSV 내보내기"""
    timestamp  = datetime.now().strftime("%Y%m%d_%H%M")
    output     = os.path.join(BASE_DIR, "data", f"companies_{timestamp}.csv")
    export_to_csv(output)


def cmd_sheets_sync(args):
    """구글 시트 동기화 (신규 업체 추가 or 전체 갱신)"""
    print("=" * 60)
    print("📊 [SHEETS] 구글 시트 동기화 시작")
    print("=" * 60)
    url = sync_to_sheets(full_refresh=args.full_refresh)
    if url:
        print(f"\n✅ 완료: {url}")


def cmd_sheets_setup(args):
    """구글 시트 서비스 계정 설정 가이드 출력"""
    print_setup_guide()


# ── 내부 유틸 ───────────────────────────────────────────────────

def _print_stats(verbose: bool = False):
    s = get_stats()
    print(f"\n  총 수집 업체   : {s['total']:,}개")
    print(f"  이메일 보유    : {s['has_email']:,}개")
    print(f"  발송 대기      : {s['pending']:,}개")
    print(f"  발송 완료      : {s['email_sent']:,}개")
    if verbose:
        print(f"  이메일 미수집  : {s['no_email']:,}개")


# ── CLI 진입점 ──────────────────────────────────────────────────

def main():
    init_db()

    parser = argparse.ArgumentParser(
        prog="outbound_sales",
        description="LUA BIM LABS — 아웃바운드 영업 자동화 봇",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("crawl",   help="구글맵 업체 수집 → DB 저장")
    sub.add_parser("extract", help="웹사이트에서 이메일 추출 → DB 업데이트")

    p_send = sub.add_parser("send", help="제안 이메일 발송")
    p_send.add_argument("--dry-run", action="store_true", help="실제 발송 없이 미리보기만")

    sub.add_parser("update",  help="crawl + extract 한번에 실행 (신규 업체 추가·업데이트)")
    sub.add_parser("status",  help="현재 DB 통계 출력")
    sub.add_parser("export",  help="전체 리스트 CSV 내보내기 (로컬 백업용)")

    p_sheets = sub.add_parser("sheets-sync",  help="구글 시트 동기화")
    p_sheets.add_argument("--full-refresh", action="store_true", help="전체 재작성 (기본: 신규만 추가)")
    sub.add_parser("sheets-setup", help="구글 시트 서비스 계정 설정 가이드")

    args = parser.parse_args()

    commands = {
        "crawl":        cmd_crawl,
        "extract":      cmd_extract,
        "send":         cmd_send,
        "update":       cmd_update,
        "status":       cmd_status,
        "export":       cmd_export,
        "sheets-sync":  cmd_sheets_sync,
        "sheets-setup": cmd_sheets_setup,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
