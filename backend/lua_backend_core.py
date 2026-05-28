# -*- coding: utf-8 -*-
"""
🌟 LUA BIM LABS v19.6 - SYSTEM BACKEND CORE
- Engine: Crawl4AI Engine & CFO Routing & DevOps Obsidian Core
- Path: /Users/YOUR_MAC_NAME/Obsidian/Vaults/LuaBimLabs
"""

import asyncio
import os
import datetime
import requests
from pathlib import Path
from crawl4ai import AsyncWebCrawler

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def load_local_env(path=None):
    """Load simple KEY=VALUE pairs for local development without adding a dependency."""
    path = Path(path) if path else PROJECT_ROOT / ".env"
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

load_local_env()

# =====================================================================
# [지배자 설정 영역] 마운트할 로컬 환경에 맞게 고치십시오.
# =====================================================================
OBSIDIAN_VAULT_PATH = os.environ.get("OBSIDIAN_VAULT_PATH", "/Users/Shared/LuaBimLabs_Vault")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
# =====================================================================

class LuaBimLabsCore:
    def __init__(self):
        self.tax_ratio = 0.25         # 🏦 25% 글로벌 세금 유보
        self.reinvest_ratio = 0.70    # 🚀 70% 조직 성장 올인 풀
        self.family_ratio = 0.05      # 👑 5% 가문 지분 배당 (MRR $10k 돌파시)

    async def collect_tech_intelligence(self, target_url):
        """
        [3계층 R&D] Crawl4AI를 구동하여 웹 노이즈를 100% 제거한 순수 마크다운 수집
        """
        print(f"🕸️ [Crawl4AI] 대상 데이터 소스 타겟팅 스크래핑 개시: {target_url}")
        
        async with AsyncWebCrawler(verbose=False) as crawler:
            result = await crawler.arun(
                url=target_url,
                bypass_cache=True,
                screenshot=False
            )
            
            if result.success and result.markdown:
                print("🟢 [Crawl4AI] 퓨어 마크다운 정제 성공.")
                return result.markdown
            else:
                error_msg = f"❌ [Crawl4AI] 스크래핑 실패 또는 빈 데이터 리턴. URL: {target_url}"
                self.send_telegram_alert(error_msg)
                raise Exception(error_msg)

    def calculate_cfo_routing(self, gross_revenue):
        """
        [1계층 CFO] v19.5 정관에 따른 자본 분배 및 배당 런타임 연산
        """
        tax = gross_revenue * self.tax_ratio
        reinvest = gross_revenue * self.reinvest_ratio
        family_payout = gross_revenue * self.family_ratio if gross_revenue >= 10000 else 0.0
        
        # 배당 임계점 미달 시 재투자 풀로 일시 전환 락킹
        if gross_revenue < 10000:
            reinvest += gross_revenue * self.family_ratio

        return {
            "gross": gross_revenue,
            "tax": tax,
            "reinvest": reinvest,
            "family": family_payout,
            "dividend_active": "ACTIVE (🟢)" if gross_revenue >= 10000 else "HOLD (🟡)"
        }

    def write_to_obsidian_vault(self, financial_data, tech_markdown):
        """
        [3계층 우측: 인프라_DevOps] 로컬 옵시디언 금고에 무인 실시간 상태창 마운트
        """
        if not os.path.exists(OBSIDIAN_VAULT_PATH):
            os.makedirs(OBSIDIAN_VAULT_PATH)

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. 재무 관제 상태창 마크다운 템플릿 생성
        dashboard_content = f"""---
🎯 타이틀: LUA BIM LABS 글로벌 자본 흐름 관제창
📅 관측일시: {now_str}
🤖 관제엔진: 🪙 CFO 에이전트 & 🧪 인프라_DevOps 연동 모듈
⚖️ 거버넌스 모드: 소유-경영 절대 분리 (지배자 참여도 0%)
---

## 🪙 1. 글로벌 총 매출 현황 (Total Revenue)
* **당월 누적 매출 (Gross Revenue):** ${financial_data['gross']:,} USD
* **배당 임계점 돌파 여부:** {financial_data['dividend_active']}

---

## 📊 2. v19.5 정관 기준 자본 라우팅 상태 (Capital Routing System)

| 자본 배분 항목 | 배분 비율 | 실시간 집행 금액 (USD) | 자본 락킹 및 송출 목적지 |
| :--- | :---: | :---: | :--- |
| **🏦 전사 세금 유보금** | **25%** | ${financial_data['tax']:,} USD | 글로벌 종합소득세 및 VAT 선제적 격리 완료 |
| **🚀 조직 성장 올인 풀** | **70%** | ${financial_data['reinvest']:,} USD | 3계층 R&D 부서 DeepSeek API 쿼터 자동 충전 |
| **👑 가문 지분 배당 풀** | **5%** | **${financial_data['family']:,} USD** | 🔒 지배자 가문 신탁 계좌 (`Choi Lua's Trust`) 즉시 송출 |

---
[🔒 LUA BIM LABS SYSTEM LOCK - 가문의 허가 없이 정관 비율 수정 불가]
"""
        
        # 파일 쓰기 강제 집행 (부서 보고 없는 실시간 동기화)
        status_path = os.path.join(OBSIDIAN_VAULT_PATH, "01_재무_상태창_최신.md")
        with open(status_path, "w", encoding="utf-8") as f:
            f.write(dashboard_content)
        print("💾 [DevOps] 옵시디언 재무 관제 상태창 업데이트 완료.")

        # 2. 수집된 기술 마크다운 적재
        tech_path = os.path.join(OBSIDIAN_VAULT_PATH, "02_오토데스크_API_신기술_지식.md")
        with open(tech_path, "w", encoding="utf-8") as f:
            f.write(f"# 📚 자문 자율 수집 기술 지식\n> 수집일시: {now_str}\n\n" + tech_markdown)
        print("💾 [DevOps] 옵시디언 기술 지식 문서 무인 적재 완료.")

    def send_telegram_alert(self, message):
        """
        [🛜 Telegram API 인프라] 시스템 예외 및 런타임 긴급 리포트 라우팅
        """
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("🟡 [Telegram] 토큰 또는 채팅 ID 미설정: 알림 송출을 건너뜁니다.")
            return

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": f"🚨 [LUA BIM LABS ALERT]\n{message}"}
        try:
            requests.post(url, json=payload, timeout=5)
            print("🛜 [Telegram] 시스템 실시간 알림 경보 송출 완 완료.")
        except Exception as e:
            print(f"텔레그램 통신 실패: {e}")

# =====================================================================
# 시스템 통합 테스트 런타임 격발
# =====================================================================
async def main():
    system = LuaBimLabsCore()
    
    # 가상 시나리오 데이터: 당월 가상 매출 $14,500 발생
    simulated_gross_revenue = 14500.00
    target_tech_docs = "https://html.spec.whatwg.org/" # 오토데스크 대체 테스트용 경량 기술 표준 문서
    
    try:
        # Step 1: Crawl4AI를 통한 마크다운 정제 데이터 수집
        tech_md = await system.collect_tech_intelligence(target_tech_docs)
        
        # Step 2: CFO 자본 배분 룰셋 가동
        fin_report = system.calculate_cfo_routing(simulated_gross_revenue)
        
        # Step 3: 인프라_DevOps 옵시디언 무인 적재단 실행
        system.write_to_obsidian_vault(fin_report, tech_md)
        
        print("🏆 [LUA BIM LABS v19.6] 무인 파이프라인 자율 구동 완결.")
        
    except Exception as e:
        system.send_telegram_alert(f"메인 런타임 코어 크래시 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
