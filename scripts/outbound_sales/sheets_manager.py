# ================================================================
# sheets_manager.py — Google Sheets 연동 관리
#
# 설정 방법:
# 1. Google Cloud Console → IAM → 서비스 계정 생성
# 2. 키 생성 → JSON 다운로드 → 아래 경로에 저장:
#    /Users/choejeong-yeon/LUA BIM LABS/scripts/outbound_sales/data/service_account.json
# 3. Google Sheets API 활성화 (Cloud Console → 라이브러리)
# 4. 생성된 시트를 서비스 계정 이메일과 공유 (편집자 권한)
# ================================================================
import os
import sqlite3
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from config import DB_PATH, BASE_DIR

# 서비스 계정 JSON 경로
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "data", "service_account.json")

# 구글 시트 이름 및 ID (최초 생성 후 config에서 관리)
SHEET_TITLE = "LUA BIM LABS — 영업 업체 리스트"

# 시트 ID 저장 파일
SHEET_ID_FILE = os.path.join(BASE_DIR, "data", "sheet_id.txt")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SHEETS_API_CREATE_URL = "https://sheets.googleapis.com/v4/spreadsheets"

# 헤더 정의 (사용자 시트 구조 기준)
HEADERS = ["Code", "회사명", "주소", "연락처", "이메일", "담당자 이메일", "회사분류", "리스트 현황", "업데이트 일자"]

# 상태별 색상 (구글 시트 배경색)
STATUS_COLORS = {
    "new":        {"red": 1.0,  "green": 1.0,  "blue": 1.0},    # 흰색
    "email_sent": {"red": 0.83, "green": 0.94, "blue": 0.78},   # 연초록
    "replied":    {"red": 0.68, "green": 0.85, "blue": 0.90},   # 연파랑
    "excluded":   {"red": 0.95, "green": 0.95, "blue": 0.95},   # 연회색
}


def _get_client() -> gspread.Client:
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


def _get_or_create_sheet(client: gspread.Client) -> gspread.Spreadsheet:
    """시트 ID 파일이 있으면 열고, 없으면 Sheets API로 신규 생성"""
    if os.path.exists(SHEET_ID_FILE):
        with open(SHEET_ID_FILE) as f:
            sheet_id = f.read().strip()
        if sheet_id:
            try:
                return client.open_by_key(sheet_id)
            except Exception:
                pass  # ID 무효 → 재생성 시도

    # Drive API 대신 Sheets API로 직접 생성 (서비스 계정 Drive 쿼터 우회)
    try:
        resp = client.http_client.request(
            "post",
            SHEETS_API_CREATE_URL,
            json={"properties": {"title": SHEET_TITLE, "locale": "ko_KR"}},
        )
        spreadsheet_id = resp.json()["spreadsheetId"]
        spreadsheet = client.open_by_key(spreadsheet_id)
        with open(SHEET_ID_FILE, "w") as f:
            f.write(spreadsheet_id)
        print(f"[SHEETS] 새 시트 생성: {spreadsheet.url}")
        return spreadsheet
    except Exception as e:
        _print_manual_sheet_guide()
        raise RuntimeError(f"시트 자동 생성 실패 ({e}) — 위 안내를 따라 수동 생성 후 재시도하세요.") from e


def _print_manual_sheet_guide():
    sa_email = "lua-bim-labs@plexiform-being-454307-q5.iam.gserviceaccount.com"
    print(f"""
┌─────────────────────────────────────────────────────────────────┐
│  구글 시트 수동 생성 안내 (1회만 필요)                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. https://sheets.google.com 에서 빈 스프레드시트 생성          │
│ 2. 우상단 [공유] → 아래 이메일을 '편집자'로 추가:              │
│    {sa_email}  │
│ 3. 스프레드시트 URL에서 ID 복사:                                │
│    https://docs.google.com/spreadsheets/d/[이 부분]/edit       │
│ 4. 아래 파일에 ID 붙여넣기:                                     │
│    data/sheet_id.txt                                            │
│ 5. 다시 실행: python main.py sheets-sync                        │
└─────────────────────────────────────────────────────────────────┘
""")


def _load_from_db() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies ORDER BY status, created_at DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def _row_values(c: dict) -> list:
    return [
        c.get("id", ""),
        c.get("name", ""),
        c.get("address", ""),
        c.get("phone", ""),
        c.get("email", ""),          # 자동 추출 이메일
        "",                           # 담당자 이메일 (수동 입력 — 동기화 시 덮어쓰지 않음)
        c.get("category", ""),
        c.get("status", "new"),
        c.get("created_at", ""),
    ]


def _format_sheet(ws: gspread.Worksheet, num_rows: int):
    """헤더 서식 + 열 너비 + 상태 색상 자동 적용"""
    requests = []
    sheet_id = ws.id

    # 헤더 굵게 + 배경색 (네이비)
    requests.append({
        "repeatCell": {
            "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1},
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.07, "green": 0.10, "blue": 0.16},
                    "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 10},
                    "horizontalAlignment": "CENTER",
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
        }
    })

    # 열 고정 (헤더 freeze)
    requests.append({
        "updateSheetProperties": {
            "properties": {"sheetId": sheet_id, "gridProperties": {"frozenRowCount": 1}},
            "fields": "gridProperties.frozenRowCount",
        }
    })

    # 자동 열 너비
    requests.append({
        "autoResizeDimensions": {
            "dimensions": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 9}
        }
    })

    ws.spreadsheet.batch_update({"requests": requests})


def sync_to_sheets(full_refresh: bool = False) -> str:
    """
    DB 데이터를 구글 시트에 동기화.
    full_refresh=True : 데이터 전체 재작성 (F열 담당자 이메일은 보존)
    full_refresh=False: 신규 업체 추가 + 기존 행 이메일 컬럼 업데이트
    """
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print("[SHEETS] service_account.json 없음 — 설정 필요")
        print("  → 가이드: python main.py sheets-setup")
        return ""

    client = _get_client()
    spreadsheet = _get_or_create_sheet(client)
    ws = spreadsheet.sheet1
    ws.update_title("업체 리스트")

    companies = _load_from_db()
    company_map = {str(c["id"]): c for c in companies}

    if full_refresh:
        # F열(담당자 이메일) 수동 입력값 보존 후 전체 재작성
        manual_emails: dict[str, str] = {}
        try:
            all_vals = ws.get_all_values()
            for row in all_vals[1:]:
                if len(row) >= 6 and row[0] and row[5]:
                    manual_emails[row[0]] = row[5]  # id → 담당자 이메일
        except Exception:
            pass

        ws.clear()
        all_rows = [HEADERS]
        for c in companies:
            row = _row_values(c)
            row[5] = manual_emails.get(str(c["id"]), "")  # 담당자 이메일 복원
            all_rows.append(row)
        ws.update(all_rows, "A1")
        print(f"[SHEETS] 전체 동기화 완료: {len(companies)}개 (담당자 이메일 {len(manual_emails)}개 보존)")

    else:
        # 기존 시트 데이터 읽기
        try:
            all_vals = ws.get_all_values()
        except Exception:
            all_vals = []

        existing: dict[str, int] = {}  # id → 행 번호(1-based)
        existing_emails: dict[str, str] = {}  # id → 현재 시트 이메일

        for i, row in enumerate(all_vals[1:], start=2):
            if row and row[0]:
                existing[row[0]] = i
                existing_emails[row[0]] = row[4] if len(row) > 4 else ""

        # 신규 업체 추가
        new_rows = [_row_values(c) for c in companies if str(c["id"]) not in existing]
        if new_rows:
            ws.append_rows(new_rows, value_input_option="USER_ENTERED")
            print(f"[SHEETS] 신규 {len(new_rows)}개 업체 추가")
        else:
            print("[SHEETS] 추가할 신규 업체 없음")

        # 이메일이 새로 추출된 기존 행 업데이트 (E열만)
        email_cell_updates = []
        for cid, row_num in existing.items():
            c = company_map.get(cid)
            if c and c.get("email") and not existing_emails.get(cid):
                email_cell_updates.append({
                    "range": f"E{row_num}",
                    "values": [[c["email"]]],
                })
        if email_cell_updates:
            ws.batch_update(email_cell_updates)
            print(f"[SHEETS] 이메일 업데이트: {len(email_cell_updates)}개")

    _format_sheet(ws, len(companies))

    url = spreadsheet.url
    print(f"[SHEETS] 시트 URL: {url}")
    return url


def print_setup_guide():
    """서비스 계정 설정 가이드 출력"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║        Google Sheets 서비스 계정 설정 가이드                 ║
╚══════════════════════════════════════════════════════════════╝

1. Google Cloud Console 접속
   → https://console.cloud.google.com

2. IAM 및 관리자 → 서비스 계정 → [+ 서비스 계정 만들기]
   - 이름: lua-bim-labs-sheets
   - 역할: 편집자

3. 서비스 계정 클릭 → 키 탭 → 키 추가 → JSON
   → 다운로드된 파일을 아래 경로에 저장:
   /Users/choejeong-yeon/LUA BIM LABS/scripts/outbound_sales/data/service_account.json

4. Google Sheets API 활성화
   → Cloud Console → API 라이브러리 → "Google Sheets API" 검색 → 사용 설정

5. 설정 완료 후 실행:
   python main.py sheets-sync

   (최초 실행 시 새 시트가 자동 생성됩니다)

※ 서비스 계정 이메일 주소(JSON 파일 내 client_email)를
  생성된 시트에 편집자로 공유하면 jycompany90@naver.com으로도 접근 가능합니다.
""")
