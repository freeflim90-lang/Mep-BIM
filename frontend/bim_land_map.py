"""
LUA BIM LAND — 영토 지도 대시보드 (Streamlit + folium)

실행:
    streamlit run frontend/bim_land_map.py

의존성:
    pip install streamlit folium streamlit-folium
"""

import json
import datetime
from pathlib import Path

import streamlit as st
import folium
from streamlit_folium import st_folium

# ── 경로 ────────────────────────────────────────────────────────────────────────
_ROOT = Path(__file__).resolve().parents[1]
_TERRITORIES_FILE = _ROOT / "data" / "bim_land" / "territories.json"
_LOGS_FILE        = _ROOT / "data" / "bim_land" / "territory_logs.json"

# ── 등급별 스타일 ────────────────────────────────────────────────────────────────
GRADE_COLOR = {
    "Normal":    "#6b7280",   # 회색
    "Rare":      "#3b82f6",   # 파랑
    "Epic":      "#8b5cf6",   # 보라
    "Legendary": "#f97316",   # 주황
}
GRADE_EMOJI = {"Normal": "🟢", "Rare": "🔵", "Epic": "🟣", "Legendary": "🟠"}
GRADE_ORDER = ["Legendary", "Epic", "Rare", "Normal"]

# ── 팀 색상 팔레트 ───────────────────────────────────────────────────────────────
_TEAM_PALETTE = [
    "#ef4444", "#3b82f6", "#22c55e", "#f59e0b",
    "#8b5cf6", "#ec4899", "#06b6d4", "#84cc16",
]


def _team_color(team: str, teams: list[str]) -> str:
    idx = teams.index(team) if team in teams else 0
    return _TEAM_PALETTE[idx % len(_TEAM_PALETTE)]


# ── 데이터 로드 ──────────────────────────────────────────────────────────────────

@st.cache_data(ttl=5)
def load_territories() -> dict:
    if not _TERRITORIES_FILE.exists():
        return {}
    try:
        return json.loads(_TERRITORIES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


@st.cache_data(ttl=5)
def load_logs() -> list[dict]:
    if not _LOGS_FILE.exists():
        return []
    try:
        return json.loads(_LOGS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


# ── 리더보드 연산 ────────────────────────────────────────────────────────────────

def compute_leaderboard(territories: dict) -> list[dict]:
    team_xp: dict[str, float] = {}
    team_count: dict[str, int] = {}
    for t in territories.values():
        team = t.get("owner_team", "unknown")
        team_xp[team]    = team_xp.get(team, 0)    + t.get("total_xp", 0)
        team_count[team] = team_count.get(team, 0) + 1
    ranked = sorted(team_xp.items(), key=lambda x: x[1], reverse=True)
    return [
        {"rank": i + 1, "team": tm, "total_xp": round(xp, 1), "territories": team_count[tm]}
        for i, (tm, xp) in enumerate(ranked)
    ]


# ── 페이지 설정 ──────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="LUA BIM LAND — 영토 지도",
    page_icon="⚔️",
    layout="wide",
)

st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    h1 { color: #e2b96f; }
    .stMetric label { font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

st.title("⚔️ LUA BIM LAND — 영토 지도 대시보드")
st.caption(f"마지막 갱신: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  5초마다 자동 캐시 갱신")

territories = load_territories()
logs        = load_logs()
leaderboard = compute_leaderboard(territories)
all_teams   = [item["team"] for item in leaderboard]

# ── 상단 지표 ────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("총 영토 수",         len(territories))
col2.metric("참여 팀 수",         len(all_teams))
col3.metric("총 동기화 횟수",     len(logs))
total_xp = sum(t.get("total_xp", 0) for t in territories.values())
col4.metric("누적 XP",            f"{total_xp:,.0f}")

st.divider()

# ── 메인 레이아웃: 지도 + 사이드바 ───────────────────────────────────────────────
map_col, side_col = st.columns([3, 1])

with map_col:
    st.subheader("🗺️ 한국 영토 현황")

    if not territories:
        st.info("아직 동기화 데이터가 없습니다.\n\n"
                "`python scripts/test_bim_land_api.py` 로 샘플 데이터를 먼저 생성하세요.")
    else:
        m = folium.Map(
            location=[36.5, 127.8],
            zoom_start=7,
            tiles="CartoDB positron",
        )

        for code, t in territories.items():
            lat = t.get("latitude",  0.0)
            lng = t.get("longitude", 0.0)
            if lat == 0.0 and lng == 0.0:
                continue

            grade  = t.get("grade", "Normal")
            team   = t.get("owner_team", "?")
            xp     = t.get("total_xp", 0)
            color  = _team_color(team, all_teams)
            radius = max(8, min(30, xp / 500))

            popup_html = f"""
            <div style='font-family:sans-serif;min-width:180px'>
              <b style='font-size:13px'>{t.get('project_name', code)}</b><br/>
              <span style='color:{GRADE_COLOR[grade]}'>{GRADE_EMOJI[grade]} {grade}</span><br/>
              팀: <b>{team}</b><br/>
              XP: <b>{xp:,.1f}</b><br/>
              코드: {code}
            </div>"""

            folium.CircleMarker(
                location=[lat, lng],
                radius=radius,
                color=color,
                fill=True,
                fill_color=GRADE_COLOR[grade],
                fill_opacity=0.75,
                popup=folium.Popup(popup_html, max_width=220),
                tooltip=f"{t.get('project_name', code)} | {grade}",
            ).add_to(m)

            # 랜드마크 등급은 깃발 아이콘 추가
            if grade == "Legendary":
                folium.Marker(
                    location=[lat, lng],
                    icon=folium.DivIcon(
                        html=f'<div style="font-size:18px">🚩</div>',
                        icon_size=(20, 20),
                        icon_anchor=(0, 20),
                    ),
                    tooltip=f"🏆 Legendary: {t.get('project_name', code)}",
                ).add_to(m)

        st_folium(m, width=None, height=520, returned_objects=[])

with side_col:
    st.subheader("🏆 팀 랭킹")
    if leaderboard:
        medals = ["🥇", "🥈", "🥉"]
        for item in leaderboard:
            medal = medals[item["rank"] - 1] if item["rank"] <= 3 else f"{item['rank']}."
            color = _team_color(item["team"], all_teams)
            st.markdown(
                f"{medal} **{item['team']}**  \n"
                f"<span style='color:{color}'>XP {item['total_xp']:,.0f}</span>  |  "
                f"영토 {item['territories']}개",
                unsafe_allow_html=True,
            )
            st.markdown("---")
    else:
        st.info("데이터 없음")

# ── 영토 목록 테이블 ─────────────────────────────────────────────────────────────
st.subheader("📋 전체 영토 목록")
if territories:
    rows = []
    for code, t in sorted(territories.items(),
                           key=lambda x: x[1].get("total_xp", 0), reverse=True):
        rows.append({
            "코드":       code,
            "프로젝트명": t.get("project_name", ""),
            "등급":       f"{GRADE_EMOJI.get(t.get('grade',''), '')} {t.get('grade', '')}",
            "점령팀":     t.get("owner_team", ""),
            "XP":         f"{t.get('total_xp', 0):,.1f}",
            "상태":       t.get("status", ""),
            "마지막 동기화": t.get("last_sync_at", "")[:16],
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.info("영토 데이터가 없습니다.")

# ── 최근 동기화 로그 ─────────────────────────────────────────────────────────────
with st.expander("📜 최근 동기화 로그 (최신 20건)"):
    recent = sorted(logs, key=lambda x: x.get("sync_at", ""), reverse=True)[:20]
    if recent:
        st.dataframe(
            [{
                "시각":      entry.get("sync_at", "")[:16],
                "프로젝트":  entry.get("project_code", ""),
                "유저":      entry.get("user_email", ""),
                "팀":        entry.get("user_team", ""),
                "등급":      entry.get("territory_grade", ""),
                "XP":        entry.get("xp_earned", 0),
                "Shadow":    "⚡" if entry.get("shadow_strike") else "—",
            } for entry in recent],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("로그 없음")

# ── 자동 새로고침 ────────────────────────────────────────────────────────────────
st.markdown("""
<script>
setTimeout(function(){ window.location.reload(); }, 30000);
</script>
""", unsafe_allow_html=True)
