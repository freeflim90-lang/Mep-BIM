# ================================================================
# db_manager.py — SQLite 데이터베이스 관리
# ================================================================
import sqlite3
import os
from datetime import datetime
from config import DB_PATH


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """테이블 초기화 (최초 1회)"""
    conn = get_conn()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS companies (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            place_id            TEXT    UNIQUE NOT NULL,
            name                TEXT    NOT NULL,
            address             TEXT,
            phone               TEXT,
            website             TEXT,
            email               TEXT,
            category            TEXT,
            status              TEXT    DEFAULT 'new',
            created_at          TEXT    DEFAULT (datetime('now','localtime')),
            updated_at          TEXT    DEFAULT (datetime('now','localtime')),
            last_contacted_at   TEXT,
            notes               TEXT
        );

        CREATE TABLE IF NOT EXISTS email_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id  INTEGER NOT NULL,
            subject     TEXT,
            status      TEXT,
            sent_at     TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (company_id) REFERENCES companies(id)
        );
    """)
    conn.commit()
    conn.close()
    print("[DB] 초기화 완료")


def upsert_company(data: dict) -> tuple[int, str]:
    """
    업체 저장 또는 업데이트.
    반환: (company_id, action)  action = 'inserted' | 'updated' | 'skipped'
    """
    conn = get_conn()
    cur  = conn.cursor()

    cur.execute("SELECT id, website, email FROM companies WHERE place_id = ?", (data["place_id"],))
    existing = cur.fetchone()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if existing is None:
        cur.execute("""
            INSERT INTO companies (place_id, name, address, phone, website, email, category)
            VALUES (:place_id, :name, :address, :phone, :website, :email, :category)
        """, data)
        company_id = cur.lastrowid
        action = "inserted"
    else:
        # 웹사이트나 이메일이 새로 발견된 경우만 업데이트
        updates = {}
        if data.get("website") and not existing["website"]:
            updates["website"] = data["website"]
        if data.get("email") and not existing["email"]:
            updates["email"] = data["email"]

        if updates:
            updates["updated_at"] = now
            updates["id"] = existing["id"]
            set_clause = ", ".join(f"{k} = :{k}" for k in updates if k != "id")
            cur.execute(f"UPDATE companies SET {set_clause} WHERE id = :id", updates)
            action = "updated"
        else:
            action = "skipped"
        company_id = existing["id"]

    conn.commit()
    conn.close()
    return company_id, action


def get_companies_without_email() -> list[dict]:
    """이메일 미수집 업체 조회 (웹사이트가 있는 경우 우선)"""
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        SELECT id, name, website FROM companies
        WHERE (email IS NULL OR email = '')
          AND website IS NOT NULL AND website != ''
        ORDER BY created_at DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def update_email(company_id: int, email: str):
    conn = get_conn()
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "UPDATE companies SET email = ?, updated_at = ? WHERE id = ?",
        (email, now, company_id)
    )
    conn.commit()
    conn.close()


def get_companies_to_contact() -> list[dict]:
    """발송 대상 업체 조회 (이메일 있고, 아직 미발송)"""
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("""
        SELECT id, name, email, address, category FROM companies
        WHERE email IS NOT NULL AND email != ''
          AND status = 'new'
        ORDER BY created_at DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def mark_contacted(company_id: int, subject: str, status: str = "sent"):
    conn = get_conn()
    now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "UPDATE companies SET status = 'email_sent', last_contacted_at = ?, updated_at = ? WHERE id = ?",
        (now, now, company_id)
    )
    conn.execute(
        "INSERT INTO email_logs (company_id, subject, status) VALUES (?, ?, ?)",
        (company_id, subject, status)
    )
    conn.commit()
    conn.close()


def get_stats() -> dict:
    """현황 통계"""
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM companies")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM companies WHERE email IS NOT NULL AND email != ''")
    has_email = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM companies WHERE status = 'email_sent'")
    sent = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM companies WHERE status = 'new'")
    pending = cur.fetchone()[0]
    conn.close()
    return {
        "total": total,
        "has_email": has_email,
        "email_sent": sent,
        "pending": pending,
        "no_email": total - has_email,
    }


def export_to_csv(output_path: str):
    """전체 업체 리스트 CSV 내보내기"""
    import csv
    conn = get_conn()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM companies ORDER BY status, created_at DESC")
    rows = cur.fetchall()
    conn.close()

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "상호명", "주소", "전화", "웹사이트", "이메일", "업종", "상태", "등록일", "최종발송일"])
        for r in rows:
            writer.writerow([r["id"], r["name"], r["address"], r["phone"],
                             r["website"], r["email"], r["category"],
                             r["status"], r["created_at"], r["last_contacted_at"]])
    print(f"[EXPORT] CSV 저장: {output_path}")
