import sqlite3
from datetime import datetime

DB_PATH = "lua_governance.db"

def log_agent_token(agent_name: str, model_name: str, prompt_cnt: int, completion_cnt: int):
    """
    개발 에이전트별 토큰 사용량을 현재 월 기준으로 누적 관리합니다.
    """
    current_month = datetime.now().strftime("%Y-%m")
    total_cnt = prompt_cnt + completion_cnt
    
    # 💡 모델별 토큰 단가 정의 (백만 토큰당 가격 기준 - 임의 설정 가능)
    # 예시: V4 Pro 입/출력 평균 단가 상정
    cost_per_token = 0.000002 if "reasoner" in model_name else 0.000001
    calculated_cost = total_cnt * cost_per_token

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # PEP 668 환경 위에서 안전하게 작동하는 UPSERT 쿼리
    query = """
    INSERT INTO agent_token_usage 
        (year_month, agent_name, model_name, prompt_tokens, completion_tokens, total_tokens, accumulated_cost, last_updated)
    VALUES 
        (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(year_month, agent_name, model_name) DO UPDATE SET
        prompt_tokens = prompt_tokens + excluded.prompt_tokens,
        completion_tokens = completion_tokens + excluded.completion_tokens,
        total_tokens = total_tokens + excluded.total_tokens,
        accumulated_cost = accumulated_cost + excluded.accumulated_cost,
        last_updated = CURRENT_TIMESTAMP;
    """

    try:
        cursor.execute(query, (current_month, agent_name, model_name, prompt_cnt, completion_cnt, total_cnt, calculated_cost))
        conn.commit()
        print(f"🟢 [{agent_name}] 토큰 누적 성공: +{total_cnt} tx")
    except Exception as e:
        conn.rollback()
        print(f"🔴 토큰 누적 실패: {e}")
    finally:
        conn.close()

# 사용 예시: 우측 3계층 '프로그램개발' 에이전트가 5,000 토큰 소모 시
# log_agent_token("프로그램개발", "ds-reasoner", 3000, 2000)
