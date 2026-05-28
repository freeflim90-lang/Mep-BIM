import os
from weasyprint import HTML

# Create updated HTML content including the "Shadow Strike" rule
html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>LUA BIM LAND 최종 완성형 개발지시서</title>
    <style>
        @page {
            size: A4;
            margin: 20mm 15mm;
            @bottom-right {
                content: counter(page) " / " counter(pages);
                font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
                font-size: 9pt;
                color: #888888;
            }
            @bottom-left {
                content: "LUA BIM LAND | 마스터 개발 규격서";
                font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
                font-size: 9pt;
                color: #888888;
                font-weight: bold;
            }
        }

        body {
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
            font-size: 10pt;
            line-height: 1.6;
            color: #2c3e50;
            margin: 0;
            padding: 0;
        }

        *, *::before, *::after {
            box-sizing: border-box;
        }

        h1, h2, h3, h4 {
            color: #1a365d;
            margin-top: 0;
            page-break-after: avoid;
        }

        h1 {
            font-size: 22pt;
            text-align: center;
            margin-bottom: 5px;
            padding-bottom: 15px;
            border-bottom: 3px double #1a365d;
        }

        .subtitle {
            text-align: center;
            font-size: 12pt;
            color: #4a5568;
            margin-bottom: 40px;
        }

        h2 {
            font-size: 14pt;
            border-left: 5px solid #2b6cb0;
            padding-left: 10px;
            margin-top: 30px;
            margin-bottom: 15px;
            page-break-after: avoid;
        }

        h3 {
            font-size: 11pt;
            color: #2b6cb0;
            margin-top: 20px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }

        p {
            margin-bottom: 12px;
            text-align: justify;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            page-break-inside: avoid;
        }

        th, td {
            border: 1px solid #cbd5e0;
            padding: 8px 10px;
            font-size: 9.5pt;
            text-align: left;
        }

        th {
            background-color: #f7fafc;
            color: #1a365d;
            font-weight: bold;
        }

        .center-align {
            text-align: center;
        }

        code {
            font-family: 'Consolas', monospace;
            background-color: #edf2f7;
            padding: 2px 5px;
            border-radius: 3px;
            font-size: 9pt;
            color: #c53030;
        }

        pre {
            font-family: 'Consolas', monospace;
            background-color: #f7fafc;
            border: 1px solid #e2e8f0;
            padding: 12px;
            border-radius: 5px;
            font-size: 8.5pt;
            overflow: hidden;
            margin: 10px 0;
            page-break-inside: avoid;
        }

        .math {
            font-family: 'Times New Roman', serif;
            font-style: italic;
            font-weight: bold;
            color: #2b6cb0;
        }

        .formula-box {
            text-align: center;
            margin: 15px 0;
            font-size: 11pt;
            background-color: #f7fafc;
            padding: 10px;
            border: 1px dashed #2b6cb0;
            border-radius: 4px;
        }

        .info-box {
            background-color: #fffaf0;
            border-left: 4px solid #dd6b20;
            padding: 12px;
            margin: 15px 0;
            border-radius: 0 4px 4px 0;
            page-break-inside: avoid;
        }

        .info-box p {
            margin: 0;
            font-size: 9.5pt;
            color: #dd6b20;
            font-weight: bold;
        }

        ul {
            margin-top: 5px;
            margin-bottom: 12px;
            padding-left: 20px;
        }

        li {
            margin-bottom: 6px;
        }

        .highlight {
            background-color: #fff5f5;
            font-weight: bold;
            color: #e53e3e;
        }
    </style>
</head>
<body>

    <h1>LUA BIM LAND 마스터 개발지시서 (PRD)</h1>
    <div class="subtitle">Revit Add-in 기반 실시간 영토 쟁탈 및 인력 매커니즘 연동 플랫폼</div>

    <h2>1. 프로젝트 개요</h2>
    <p><strong>플랫폼명:</strong> LUA BIM LAND (루아 비엠 랜드)</p>
    <p><strong>핵심 콘셉트:</strong> Revit 환경에서 근무하는 BIM 엔지니어들의 일일 작업량(Central 동기화 데이터)을 크롤링·연산하여, 실제 건축물의 바닥 면적을 점령, 방어, 찬탈하는 위치 기반 엔지니어링 게이밍 플랫폼.</p>
    <p><strong>개발 목적:</strong> 고강도 일과인 BIM 데이터 구조화 및 간섭 체크 업무에 강력한 게임 역학을 결합하여, 부서·회사 간 선의의 경쟁을 유도하고 프로젝트 수행 품질(에러 감소 및 밀도 향상)을 극대화함.</p>

    <h2>2. 핵심 시스템 게임 규칙 (Rule Engine)</h2>

    <h3>2.1 BIM 밀도(D<sub>BIM</sub>) 기반 영토 난이도 산정</h3>
    <p>영토의 가치와 점수 배점은 단순 바닥 면적이 아닌, 단위 면적당 포함된 가상 객체의 조밀함을 뜻하는 <strong>'BIM 밀도'</strong>를 기준으로 자동 등급화한다.</p>
    <div class="formula-box">
        <span class="math">D<sub>BIM</sub> = 총 객체 수 (Total Elements) / 연면적 (Gross Floor Area, m²)</span>
    </div>

    <table>
        <thead>
            <tr>
                <th style="width: 15%;" class="center-align">영토 등급</th>
                <th style="width: 25%;" class="center-align">BIM 밀도 규격</th>
                <th style="width: 45%;">대표 공종 및 대상 건축물 예시</th>
                <th style="width: 15%;" class="center-align">배점 가산 승수</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="center-align">일반 (Normal)</td>
                <td class="center-align"><span class="math">D<sub>BIM</sub> &lt; 0.5</span></td>
                <td>물류창고, 실내 주차장, 단순 오픈형 오피스</td>
                <td class="center-align">× 1.0</td>
            </tr>
            <tr>
                <td class="center-align">레어 (Rare)</td>
                <td class="center-align"><span class="math">0.5 &le; D<sub>BIM</sub> &lt; 1.5</span></td>
                <td>일반 공동주택(아파트) 단지, 표준 상업 빌딩 기본 공종</td>
                <td class="center-align">× 1.5</td>
            </tr>
            <tr>
                <td class="center-align">에픽 (Epic)</td>
                <td class="center-align"><span class="math">1.5 &le; D<sub>BIM</sub> &lt; 3.0</span></td>
                <td>초고층 빌딩 코어부, 복잡한 데이터 센터 인프라 구조/MEP</td>
                <td class="center-align">× 2.0</td>
            </tr>
            <tr>
                <td class="center-align" style="background-color: #fffaf0;"><strong>레전더리</strong></td>
                <td class="center-align" style="background-color: #fffaf0;"><span class="math">D<sub>BIM</sub> &ge; 3.0</span></td>
                <td style="background-color: #fffaf0;"><strong>종합병원 內 복잡 공종, 반도체 생산 플랜트, MEP 기계·전기실</strong></td>
                <td class="center-align" style="background-color: #fffaf0; color: #dd6b20; font-weight: bold;">× 3.0</td>
            </tr>
        </tbody>
    </table>

    <h3>2.2 팀 협업 및 리모델링 찬탈 시스템</h3>
    <ul>
        <li><strong>기간제 스쿼드(Squad):</strong> 동일 프로젝트 코드 하에서 작업 기간이 오버랩되는 엔지니어 군은 자동으로 연합 스쿼드로 지정된다. 준공 완료 시 기여도 비율에 따라 연면적 배점을 공동 소유한다.</li>
        <li><strong>리모델링 영토 찬탈:</strong> 이미 소유권이 부여된 영토에 타 사/타 팀 엔지니어의 동기화 신호가 유입될 시 즉시 해당 영토는 <code>UNDER_ATTACK</code> 모드로 전환되며, 신규 리모델링 프로젝트가 준공 완료 처리되면 영토 소유권이 통째로 이양된다.</li>
    </ul>

    <h3 class="highlight">2.3 특수 매커니즘: 섀도우 스트라이크 (Shadow Strike) - 인력 이직 어드벤티지</h3>
    <p>과거 특정 프로젝트를 수행하여 영토를 완공했던 스쿼드 멤버가 <strong>타 회사로 이직 후, 동일 프로젝트의 리모델링 공격(동기화)에 참여할 경우</strong> 발동하는 역전 매커니즘이다.</p>
    <ul>
        <li><strong>발동 조건:</strong> <code>공격자 계정 소속 != 기존 영토 점령 팀</code> 이면서, 과거 해당 <code>project_code</code>의 완료 로그에 해당 유저 이메일이 매칭될 때 서버 단에서 자동 연산.</li>
        <li><strong>어드벤티지 획득 효과:</strong> 도면 및 설계 히스토리를 꿰뚫고 있는 이직자 참여 보너스로, 공격팀의 실시간 동기화 점수 획득 속도가 비약적으로 상승한다.</li>
    </ul>
    <div class="formula-box">
        <span class="math">최종 배점(XP) = (연면적 &times; 동기화 기여도) &times; 등급 가산 승수 &times; <b>섀도우 스트라이크 승수</b></span>
    </div>
    <ul>
        <li><strong>이직 인원 1명 참여 시:</strong> 섀도우 스트라이크 승수 <span class="math">× 1.3</span> (공격력 30% 증가)</li>
        <li><strong>이직 인원 2명 이상 참여 시:</strong> 섀도우 스트라이크 승수 <span class="math">× 1.5</span> (공격력 50% 증가)</li>
    </ul>

    <h2>3. 기술 스펙 및 개발 구현 요건</h2>

    <h3>3.1 클라이언트 모듈 (Revit Add-in - C#)</h3>
    <p>동기화 처리 가로채기는 UI 메인 프로세스를 블로킹하지 않는 완전 비동기 태스크 인프라를 채택한다.</p>
    <pre>
using System;
using Autodesk.Revit.DB.Events;
using Autodesk.Revit.UI;

namespace LuaBimLand.AddIn
{
    public class SyncTrackerApp
    {
        public void RegisterEvents(UIControlledApplication app)
        {
            app.ControlledApplication.DocumentSynchronizedWithCentral +=
                new EventHandler&lt;DocumentSynchronizedWithCentralEventArgs&gt;(OnSynchronizedWithCentral);
        }

        private async void OnSynchronizedWithCentral(object sender, DocumentSynchronizedWithCentralEventArgs e)
        {
            try
            {
                var doc = e.Document;
                string projectCode = doc.ProjectInformation.Number;
                string projectName = doc.ProjectInformation.Name;
                string userEmail = doc.Application.Username; // 또는 사내 AD 연동 이메일

                // 백그라운드 스레드에서 REST API 비동기 포스팅 실행 (레빗 프리징 방지)
                // await CoreHttpClient.SendSyncPayload(projectCode, projectName, userEmail);
            }
            catch (Exception ex)
            {
                // 내부 오류 핸들링 인프라 연동
            }
        }
    }
}</pre>

    <h3>3.2 데이터베이스 스키마 및 공간 쿼리 설계 (PostgreSQL + PostGIS)</h3>
    <pre>
-- 1. LUA BIM LAND 영토 마스터 테이블
CREATE TABLE lua_territories (
    territory_id VARCHAR(50) PRIMARY KEY,
    building_name VARCHAR(100) NOT NULL,
    gross_floor_area NUMERIC NOT NULL,
    total_elements INT DEFAULT 0,
    bim_density NUMERIC GENERATED ALWAYS AS (total_elements / NULLIF(gross_floor_area, 0)) STORED,
    geom GEOMETRY(Polygon, 4326),          -- PostGIS 위경도 좌표 데이터
    current_owner_team VARCHAR(50),
    status VARCHAR(20) DEFAULT 'STABLE',    -- STABLE, UNDER_ATTACK
    last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 섀도우 스트라이크 연산을 위한 과거 이력 조회 고속 인덱스 및 연산 함수
CREATE INDEX idx_territory_logs_lookup ON territory_logs (project_id, user_email);

CREATE OR REPLACE FUNCTION check_shadow_strike(p_id VARCHAR, u_email VARCHAR, c_team VARCHAR)
RETURNS NUMERIC AS $$
DECLARE
    has_history INT;
BEGIN
    -- 과거에 다른 팀 소속으로 동일 프로젝트를 수행한 이력이 있는지 검증
    SELECT COUNT(*) INTO has_history
    FROM territory_logs
    WHERE project_id = p_id AND user_email = u_email AND user_team != c_team;

    IF has_history > 0 THEN
        RETURN 1.3; -- 섀도우 스트라이크 1단계 버프 적용
    ELSE
        RETURN 1.0; -- 일반 상태
    END IF;
END;
$$ LANGUAGE plpgsql;</pre>

    <h3>3.3 인게임 프론트엔드 연출 가이드 (WebView2 독커블 패널)</h3>
    <div class="info-box">
        <p>[🚨 인력 유출 및 영토 침공 경보 연출 요건]</p>
        <p style="color: #2c3e50; font-weight: normal; margin-top: 5px;">
            타사로 이직한 과거 스쿼드 멤버에 의해 우리 영토가 침공당하는 즉시, 기존 점령 팀의 레빗 우측 독커블 패널 전체 배경이 싸이렌 효과(Dark Red Glazing)와 함께 점멸해야 한다. 화면 중앙에는 <strong>"비상 상황: 과거 본 현장의 핵심 엔지니어가 포함된 적 스쿼드가 리모델링 영토 찬탈을 개시했습니다!"</strong> 텍스트가 강제 팝업된다.
        </p>
    </div>

</body>
</html>
"""

# Output PDF path
output_pdf = "LUA_BIM_LAND_PRD_Master_Final.pdf"

# Write to PDF using WeasyPrint
HTML(string=html_content).write_pdf(output_pdf)
print(f"Successfully generated {output_pdf}")
