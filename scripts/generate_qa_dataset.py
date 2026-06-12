"""
BIM/MEP Q&A 데이터셋 자동 생성기
지식 베이스 파일에서 구조화된 Q&A 쌍을 대규모로 생성한다.
목표: Telegram 답변 품질 향상을 위한 풍부한 Q&A 코퍼스 구축
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import AGENT_KB_DIR, QA_DATASET_DIR  # noqa: E402

KNOWLEDGE_BASE = AGENT_KB_DIR
QA_OUTPUT = QA_DATASET_DIR
QA_OUTPUT.mkdir(parents=True, exist_ok=True)


# ─── 도메인별 Q&A 템플릿 ───────────────────────────────────────────────
DOMAIN_QA_TEMPLATES: dict[str, list[dict]] = {
    "공조배관": [
        {
            "q": "공조배관에서 CHWS와 CHWR의 차이가 뭐야?",
            "a": "CHWS(Chilled Water Supply)는 냉동기에서 냉각된 물을 AHU·FCU 냉방 코일로 보내는 냉수 공급 배관이고, CHWR(Chilled Water Return)은 코일을 통과한 뒤 따뜻해진 물이 다시 냉동기로 돌아오는 냉수 환수 배관입니다. 설계 기준 공급온도 7℃, 환수온도 13℃로 온도차 6℃입니다.",
            "tags": ["hvac-piping", "chilled-water", "fluid-type"]
        },
        {
            "q": "냉각수(CW)와 냉수(CHW)가 어떻게 다른지 설명해줘",
            "a": "냉수(CHW)는 냉동기에서 만든 차가운 물을 실내 AHU/FCU 코일로 보내 냉방하는 계통입니다. 냉각수(CW)는 냉동기에서 발생한 응축열을 냉각탑으로 운반해 대기로 버리는 계통입니다. 냉수는 실내 냉방 목적(7℃/13℃), 냉각수는 냉동기 방열 목적(32℃/37℃)으로 완전히 다른 역할입니다.",
            "tags": ["hvac-piping", "chilled-water", "condenser-water"]
        },
        {
            "q": "HW(난방온수)와 HWS(급탕)을 도면에서 어떻게 구별해?",
            "a": "HW/HWS 약어는 문맥에 따라 난방온수와 급탕 둘 다 쓰이므로 반드시 도면 범례와 계통도를 확인해야 합니다. 난방온수는 공조 AHU·FCU·방열기로 연결되고, 급탕은 세면기·샤워기·싱크대 등 위생기구로 연결됩니다. Revit에서는 Hydronic Supply vs Domestic Hot Water Supply 계통명으로 구분합니다.",
            "tags": ["hvac-piping", "hot-water", "domestic-hot-water", "drawing"]
        },
        {
            "q": "냉매배관 BIM에서 어떤 이격 기준을 적용해야 해?",
            "a": "R-410A 냉매배관은 전기 케이블 트레이에서 최소 300mm 이격(단열 포함 외경 기준)이 필요합니다. 가스 배관과는 60mm 이상, 전력선과는 150mm 이상 이격합니다. BIM 간섭 검토 시 냉매관은 단열 포함 외경으로 BoundingBox를 설정해야 실제 간섭이 정확히 감지됩니다.",
            "tags": ["hvac-piping", "refrigerant", "clearance", "bim"]
        },
        {
            "q": "공조배관 간섭 검토에서 중심선 충돌만 봐도 되는가?",
            "a": "아니요, 중심선 충돌만 보면 부족합니다. 단열재 두께, 플랜지 돌출, 밸브 핸들 조작 공간, 행거, 점검 공간까지 포함해서 확인해야 합니다. 밸브류는 조작 방향과 해체 공간(플랜지 직경 + 양측 200mm)을 추가로 검토하고, AHU 전면 유지보수 통로 1,000mm 이상도 확인합니다.",
            "tags": ["hvac-piping", "clash", "maintenance", "bim"]
        },
        {
            "q": "팽창탱크를 왜 펌프 흡입 측에 설치해야 해?",
            "a": "팽창탱크를 펌프 흡입 측 환수 배관에 설치하면 시스템 전체의 기준 압력점이 안정됩니다. 펌프 토출 측에 설치하면 펌프 운전 시 압력이 팽창탱크 설정값을 초과해 안전밸브가 빈번하게 열릴 수 있고, 공기 분리가 제대로 이루어지지 않을 수 있습니다.",
            "tags": ["hvac-piping", "expansion-tank", "pump"]
        },
        {
            "q": "공조배관에서 공기빼기 밸브가 필요한 위치는 어디야?",
            "a": "배관 최고점(공기가 자연스럽게 모이는 지점)과 루프 끝단에 설치합니다. 구체적으로는 배관이 위로 올라갔다가 내려가는 꼭짓점, AHU·FCU 코일 상부, 수직 라이저 최상부입니다. 공기 고임이 생기면 유체 소음, 진동, 유량 감소가 발생합니다.",
            "tags": ["hvac-piping", "air-vent", "maintenance"]
        },
        {
            "q": "증기 배관(Steam)과 응축수 배관(Condensate)은 어떤 관계야?",
            "a": "증기가 AHU·가습기·열교환기 등 말단 장비에서 열을 방출하면 응축수(물)로 변합니다. 증기트랩(Steam Trap)이 이 응축수를 자동으로 배출하고 증기는 통과시키지 않습니다. 응축수는 응축수 회수 배관으로 보일러에 돌려보내 재사용합니다. 병원·산업시설에 주로 사용됩니다.",
            "tags": ["hvac-piping", "steam", "condensate", "trap"]
        },
        {
            "q": "배관 단열 두께 기준은 어디서 찾아야 해?",
            "a": "국내 기준은 '건축물 에너지절약 설계기준 [별표 3] 배관 단열 기준'을 따릅니다. 냉수 배관의 결로 방지 단열과 냉난방 배관의 열손실 방지 단열 두께가 구분되어 있습니다. ASHRAE Handbook Fundamentals도 참고 설계 자료로 사용됩니다. 최종 사양은 설계자 지정 사양과 인허가 기준이 우선입니다.",
            "tags": ["hvac-piping", "insulation", "regulation"]
        },
        {
            "q": "Revit에서 냉수 공급·환수 계통이 뒤바뀌어 있으면 어떤 문제가 생겨?",
            "a": "냉수 공급(CHWS)과 환수(CHWR)가 뒤바뀌면 코일에 역방향으로 물이 흐르게 됩니다. 성능상으로는 온도차가 반대가 되고, BIM 간섭 검토 및 시공 도면에서 밸브·스트레이너·유량계 방향이 틀려집니다. 장비 일람표의 공급/환수 접속구 위치와 Revit 계통명 방향을 반드시 대조해야 합니다.",
            "tags": ["hvac-piping", "revit", "system-direction", "bim"]
        },
    ],

    "공조덕트": [
        {
            "q": "SA와 RA 덕트의 차이가 뭐야?",
            "a": "SA(Supply Air, 급기)는 AHU에서 온습도 조정된 공기를 실내 디퓨저로 공급하는 덕트입니다. RA(Return Air, 환기)는 사용된 실내 공기를 AHU로 회수하는 덕트입니다. 냉방 시 SA는 12~16℃, 난방 시 30~40℃입니다. SA와 RA가 Revit에서 계통이 반대로 지정되면 간섭 검토 공종 분류 오류가 발생합니다.",
            "tags": ["hvac-duct", "supply-air", "return-air"]
        },
        {
            "q": "제연덕트가 일반 공조덕트보다 우선순위가 높은 이유가 뭐야?",
            "a": "제연덕트는 화재 시 피난자의 생명을 보호하는 소방 기능을 담당합니다. 소방법(NFTC 501, 501A)에 따라 불연 재료 또는 1시간 내화 피복이 의무이며, 방화구획 관통 시 300mm 이격 기준이 적용됩니다. 간섭 발생 시 제연덕트를 먼저 보호하고 다른 설비를 조정합니다.",
            "tags": ["hvac-duct", "smoke-control", "priority", "code"]
        },
        {
            "q": "덕트 풍속 기준이 어떻게 돼?",
            "a": "주 덕트(Main Duct): 6~10 m/s, 분기 덕트(Branch): 4~6 m/s, 취출구 전(Near Diffuser): 1.5~2.5 m/s가 일반 기준입니다. 풍속이 너무 빠르면 소음과 정압 손실이 증가하고, 너무 느리면 덕트 단면이 커져 천장고에 영향을 줍니다. 병원(NC-25)과 사무실(NC-35) 등 소음 기준에 따라 풍속 상한이 달라집니다.",
            "tags": ["hvac-duct", "velocity", "noise", "sizing"]
        },
        {
            "q": "VAV 박스 주변에 왜 점검구가 필요해?",
            "a": "VAV 박스는 댐퍼 개도 조절 액추에이터, 유량 측정 센서, 재열 코일(해당 시) 등 유지관리가 필요한 부품이 있습니다. 필터 교체, 액추에이터 교체, 교정 작업 시 점검구를 통해 접근해야 합니다. 점검구 크기는 최소 300×300mm(손 진입) 또는 600×600mm(전신 작업) 이상이 권장됩니다.",
            "tags": ["hvac-duct", "vav", "access-panel", "maintenance"]
        },
        {
            "q": "방화댐퍼가 필요한 위치는 어디야?",
            "a": "방화댐퍼(Fire Damper)는 덕트가 방화구획을 관통하는 모든 지점에 설치합니다. 화재 시 열에 의해 용융 링크가 녹으면 댐퍼가 자동으로 닫혀 방화구획을 복원합니다. 제연댐퍼(Smoke Damper)는 연기 감지기 신호 또는 방재 연동으로 전동 폐쇄합니다. 방화구획 경계 교차 덕트를 BIM에서 자동 감지해야 합니다.",
            "tags": ["hvac-duct", "fire-damper", "fire-compartment", "code"]
        },
        {
            "q": "외기(OA)와 배기(EA) 루버 위치를 어떻게 결정해?",
            "a": "외기 루버와 배기 루버는 최소 3m 이상 이격하거나 수직으로 분리해야 합니다(단락 방지). 주방 배기 루버는 외기 루버, 창문, 환기구에서 3m 이상 이격이 필요합니다. 루버 위치는 건축 파사드 디자인과 기능 요건을 조율해야 합니다. 바람 방향에 따라 오염 공기가 외기로 역류하는 단락(Short Circuit)이 발생하지 않도록 합니다.",
            "tags": ["hvac-duct", "outdoor-air", "exhaust", "louver"]
        },
        {
            "q": "전열교환기(ERV)가 뭐고 어떤 덕트와 연결돼?",
            "a": "전열교환기(Energy Recovery Ventilator)는 배기(EA)와 외기(OA) 사이에서 열과 습기를 교환해 에너지를 회수하는 장비입니다. OA와 EA 두 계통이 동시에 필요하며, 교환 후 OA는 더 따뜻하게(겨울) 또는 차갑게(여름) 조건이 개선됩니다. 겨울 동파 방지와 여름 외기 냉방 부하 절감 모두에 유리합니다.",
            "tags": ["hvac-duct", "erv", "heat-recovery", "outdoor-air"]
        },
        {
            "q": "덕트 종횡비(Aspect Ratio) 기준이 뭐야?",
            "a": "장방형 덕트의 종횡비는 4:1 이하를 권장하고 최대 8:1이 한계입니다. 종횡비가 높아질수록 덕트 둘레가 길어져 마찰 손실이 증가하고 소음이 커집니다. 천장 공간이 제한될 때는 덕트 높이를 줄이고 폭을 늘리는 방향으로 조정하되, 풍속과 정압 손실 재계산이 필요합니다.",
            "tags": ["hvac-duct", "aspect-ratio", "sizing", "friction"]
        },
        {
            "q": "주방 배기 덕트에 왜 스테인리스를 써야 해?",
            "a": "주방 배기는 고온(60~80℃) + 유증기(기름 증기)가 포함된 공기를 배출합니다. 일반 아연도 강판은 고온 유증기에 의해 부식되고, 기름이 덕트 내부에 쌓여 화재 위험이 됩니다. 스테인리스 덕트는 내식성과 내열성이 뛰어나고 청소가 용이합니다. 주방 배기는 재순환(RA로 돌리는 것) 금지가 원칙입니다.",
            "tags": ["hvac-duct", "kitchen-exhaust", "stainless", "fire-risk"]
        },
        {
            "q": "CAV 시스템과 VAV 시스템에서 덕트 설계가 어떻게 달라?",
            "a": "CAV(Constant Air Volume)는 풍량이 항상 일정하므로 설계 풍량 기준으로 덕트 크기를 고정해 설계합니다. VAV(Variable Air Volume)는 존별 부하에 따라 풍량이 변하므로 VAV 박스 위치, 최소·최대 풍량, 덕트 정압 설계가 추가로 필요합니다. VAV는 전체 AHU 풍량이 줄어들므로 팬 인버터 제어와 덕트 정압 제어가 핵심입니다.",
            "tags": ["hvac-duct", "vav", "cav", "design"]
        },
    ],

    "위생": [
        {
            "q": "급수(CWS)와 급탕(HWS)의 차이가 뭐야?",
            "a": "급수(CWS, Cold Water Supply)는 음용·위생용 냉수를 공급하는 배관이고, 급탕(HWS, Hot Water Supply)은 세면기·샤워기·주방 등에서 쓰는 온수를 공급하는 배관입니다. 급탕은 레지오넬라균 사멸을 위해 급탕기 출구 60℃ 이상 유지가 필수입니다. 공조 난방온수(HW)와 급탕(HWS)은 완전히 다른 계통입니다.",
            "tags": ["plumbing", "cold-water", "hot-water", "domestic"]
        },
        {
            "q": "오배수 배관에 구배가 필요한 이유가 뭐야?",
            "a": "오배수 배관은 펌프 없이 중력으로 물이 흐르는 자연유하 방식입니다. 구배(경사)가 없으면 물이 고여 막히고 악취가 발생합니다. 구배 기준: DN50=1/50, DN75=1/75, DN100=1/100, DN125=1/125, DN150=1/150. 유속이 0.6 m/s 이상이 되어야 고형물이 씻겨 내려갑니다.",
            "tags": ["plumbing", "sanitary", "slope", "drainage"]
        },
        {
            "q": "통기관이 없으면 어떤 문제가 생겨?",
            "a": "오배수가 흐를 때 배관 내 부압(음압)이 발생해 위생기구 트랩의 봉수(물 막음)가 빨려 나갑니다. 봉수가 없어지면 하수 가스(황화수소, 메탄)가 실내로 역류해 악취와 건강 문제가 생깁니다. 통기관은 이 압력 변화를 외기로 해소해 봉수를 보호합니다.",
            "tags": ["plumbing", "vent", "trap", "odor"]
        },
        {
            "q": "화장실 바닥에 트렌치(선홈통)를 쓰는 이유가 뭐야?",
            "a": "트렌치(Trench Drain)는 넓은 구역의 물을 선형으로 집수해 배수하는 설비입니다. 대형 화장실, 샤워실, 주차장, 기계실 바닥처럼 넓은 면적에서 물이 발생하는 곳에 사용합니다. 점형 바닥 배수구보다 집수 면적이 넓어 배수 효율이 좋고, 구배를 최소화할 수 있습니다.",
            "tags": ["plumbing", "drainage", "trench-drain", "floor"]
        },
        {
            "q": "급수 역류 방지 장치가 왜 필요해?",
            "a": "역류 방지 장치(Check Valve, Backflow Preventer)는 수도 본관의 압력이 일시적으로 낮아질 때 건물 내 오염수가 역류해 공중 상수도를 오염시키는 것을 방지합니다. 수도법 제17조에 역류 방지 장치 설치 의무가 규정되어 있습니다. 수처리 약품 주입 설비, 스프링클러 연결 구간, 냉각탑 보급수에 특히 중요합니다.",
            "tags": ["plumbing", "backflow-preventer", "regulation", "code"]
        },
        {
            "q": "집수정(Sump Pit) 크기는 어떻게 정해?",
            "a": "집수정 용량은 유입량 기준 10~15분 분량을 기본으로 합니다. 오수 펌프가 2대 교대 운전하는 경우 펌프 1회 운전 시 방출량과 유입량의 균형을 고려합니다. 집수정이 너무 작으면 펌프가 빈번하게 기동해 수명이 짧아집니다. 오수 집수정과 우수 집수정은 반드시 분리합니다.",
            "tags": ["plumbing", "sump-pit", "pump", "sizing"]
        },
    ],

    "소방기계": [
        {
            "q": "스프링클러 헤드 살수가 막히는 경우 BIM에서 어떻게 확인해?",
            "a": "헤드 디플렉터 아래 450mm 이내에 덕트, 배관, 구조 보가 있으면 살수 장애로 봅니다. Navisworks 간섭 검토에서 헤드 주변 '살수 예비 공간'을 별도 체크 존으로 지정합니다. 장애물 폭과 이격 거리에 따라 NFPA 13 기준으로 추가 헤드 설치 여부를 판단합니다.",
            "tags": ["fire-mechanical", "sprinkler", "head", "clash", "bim"]
        },
        {
            "q": "습식과 건식 스프링클러의 차이가 뭐야?",
            "a": "습식(Wet Pipe)은 배관 내 항상 물이 차 있어 헤드 개방 즉시 방수됩니다. 동결 우려 없는 일반 구역에 사용합니다. 건식(Dry Pipe)은 배관 내 가압 공기가 있다가 화재 시 공기가 빠지고 물이 충전된 후 방수됩니다. 동결 우려 구역(주차장, 옥외)에 사용하며 방수까지 시간이 지연됩니다.",
            "tags": ["fire-mechanical", "sprinkler", "wet-pipe", "dry-pipe"]
        },
        {
            "q": "소방 배관이 방화구획을 관통할 때 어떻게 처리해야 해?",
            "a": "소방 배관도 방화구획 관통 시 방화 슬리브와 내화채움재가 필요합니다. 단, 소방배관은 방화댐퍼 없이 관통 가능합니다(덕트와 다름). 방화 슬리브는 관 외경보다 최소 25mm 큰 내경, 내화채움재는 1시간 이상 내화 성능 제품을 사용합니다. BIM에서 방화구획 경계를 교차하는 소방 배관을 자동 감지해 처리 여부를 확인합니다.",
            "tags": ["fire-mechanical", "fire-compartment", "penetration", "firestop"]
        },
        {
            "q": "소방펌프실에 다른 설비 배관이 들어와도 되는가?",
            "a": "소방 전용 공간(소화펌프실, 수조실)에는 다른 설비 배관이 원칙적으로 불가합니다. 소방시설법 시행령과 NFTC 402에 따라 소방 전용으로 관리되어야 합니다. 부득이 관통해야 하는 경우 소방 담당자 및 인허가 기관 협의가 필요합니다.",
            "tags": ["fire-mechanical", "pump-room", "code", "coordination"]
        },
        {
            "q": "가스계 소화 설비가 있는 방에서 문틈을 막아야 하는 이유가 뭐야?",
            "a": "가스계 소화 방호구역은 소화약제가 방출됐을 때 농도를 유지해야 소화 효과가 있습니다. 기밀이 부족하면 약제가 빠져나가 목표 농도에 못 미칩니다. 방호구역 내 개구부에는 자동 폐쇄 댐퍼, 방화문, 씰링이 필요합니다. 환기 댐퍼는 소화약제 방출 신호와 연동해 자동 폐쇄됩니다.",
            "tags": ["fire-mechanical", "gas-suppression", "sealed-room", "damper"]
        },
    ],

    "전기": [
        {
            "q": "강전과 약전 트레이를 분리해야 하는 이유가 뭐야?",
            "a": "강전(전력 케이블 220V~380V) 근처에 약전 케이블(LAN, CCTV, 통신)이 있으면 전자기 간섭(EMI)이 발생합니다. 데이터 오류, 통신 장애, 영상 노이즈가 생길 수 있습니다. TIA-569 기준 최소 150mm 이격 또는 금속 격벽으로 분리합니다. BIM에서 강전/약전 트레이 이격 부족 구간을 EMI 위험 항목으로 분류합니다.",
            "tags": ["electrical", "cable-tray", "emi", "separation"]
        },
        {
            "q": "케이블 트레이 충전율 50% 기준은 왜 있는 거야?",
            "a": "충전율(Cable Fill Ratio) 50% 이하 기준은 케이블의 발열 방산, 장래 증설 여유, 케이블 교체 및 포설 작업성을 확보하기 위한 것입니다. 케이블이 빽빽하면 열이 쌓여 절연 열화가 빠르게 진행됩니다. 설계 시에는 현재 필요량의 50%를 넘지 않게 계획해 장래 확장을 대비합니다.",
            "tags": ["electrical", "cable-tray", "fill-ratio", "design"]
        },
        {
            "q": "분전반 전면에 최소 1,000mm 작업 공간이 필요한 이유가 뭐야?",
            "a": "분전반은 차단기 조작, 케이블 연결·교체, 전기 점검 작업 시 작업자가 전면에서 작업합니다. KEC(한국전기설비규정) 기준 저압 분전반 전면 최소 1,000mm, 고압 수배전반 1,200mm를 확보해야 합니다. 이 공간이 배관, 덕트, 구조물에 침해되면 안전 작업 불가 상태가 됩니다.",
            "tags": ["electrical", "panel", "clearance", "kec", "maintenance"]
        },
        {
            "q": "전기실 위에 급수 배관이 지나가면 왜 안 돼?",
            "a": "급수·위생 배관 누수 시 전기실로 물이 유입되면 단락·화재·감전 위험이 발생합니다. 전기실과 통신실은 누수 위험이 있는 배관 직상부 배치를 원칙적으로 금지합니다. 부득이하게 통과해야 할 경우 방수 커버, 누수 감지 센서, IP44 이상 방수 등급 장비 적용을 검토합니다.",
            "tags": ["electrical", "electrical-room", "water-protection", "safety"]
        },
        {
            "q": "접지(Grounding)가 MEP 배관에도 필요해?",
            "a": "금속 배관(강관, 동관)과 금속 덕트는 전기 설비에서 누전이 발생할 경우 전류 통로가 될 수 있습니다. 접지 본딩(Bonding)으로 금속 배관들을 서로 연결하고 대지에 접지하면 누전 전류를 안전하게 흘려보내 감전을 방지합니다. 특히 의료시설, 폭발 위험 장소, 외부 인입 배관에서 중요합니다.",
            "tags": ["electrical", "grounding", "bonding", "piping", "safety"]
        },
    ],

    "설비자동제어": [
        {
            "q": "VAV 박스에서 최소풍량을 왜 설정해야 해?",
            "a": "최소풍량(Minimum Airflow) 설정은 법정 환기량(1인당 25m³/h 이상) 확보를 위해 필요합니다. 냉방 부하가 없어도 환기를 위한 최소 풍량이 필요하고, 너무 낮아지면 CO₂ 농도 상승으로 공기질이 나빠집니다. 또한 최소풍량 이하에서 재열 코일이 작동하면 냉난방 동시 운전으로 에너지가 낭비됩니다.",
            "tags": ["bas", "vav", "minimum-airflow", "iaq", "energy"]
        },
        {
            "q": "덕트 정압 제어가 뭔지 설명해줘",
            "a": "VAV 시스템에서 각 존의 VAV 박스 댐퍼 개도가 바뀌면 덕트 내 압력이 변합니다. 덕트 정압(Static Pressure) 제어는 중간 덕트에 설치된 압력 센서로 정압을 측정하고, 팬 인버터 주파수를 조절해 정압을 설정값으로 유지하는 제어입니다. 정압이 너무 높으면 소음과 에너지 낭비, 너무 낮으면 각 존 풍량 부족이 생깁니다.",
            "tags": ["bas", "vav", "static-pressure", "fan-control", "inverter"]
        },
        {
            "q": "BAS에서 포인트(Point)가 뭐야?",
            "a": "포인트는 자동제어 시스템에서 감시·제어하는 하나의 신호 단위입니다. 신호 유형: AI(Analog Input: 온도·압력·습도 등 연속값 입력), AO(Analog Output: 밸브 개도·인버터 주파수 등 연속값 출력), DI(Digital Input: 운전상태·고장·스위치 등 ON/OFF 입력), DO(Digital Output: 기동·정지·개폐 등 ON/OFF 출력). Point List 문서에 모든 포인트가 목록화되어야 합니다.",
            "tags": ["bas", "point-list", "ai-ao-di-do", "ddc"]
        },
        {
            "q": "AHU 자동제어에서 급기온도와 환기온도를 모두 봐야 하는 이유가 뭐야?",
            "a": "급기온도(Supply Air Temp)는 코일 밸브 제어의 직접 기준으로 목표값에 맞춰 냉수/온수 밸브를 조절합니다. 환기온도(Return Air Temp)는 실내 평균 온도를 추정하며, 급기온도 설정값 리셋(Reset)에 사용됩니다. 예를 들어 실내가 충분히 시원하면 급기온도를 올려 에너지를 절감하는 제어에 환기온도가 기준이 됩니다.",
            "tags": ["bas", "ahu", "supply-temperature", "return-temperature", "reset"]
        },
        {
            "q": "소방 방재 연동이 일반 자동제어와 다른 점이 뭐야?",
            "a": "소방 방재 연동은 소방시설법과 화재안전기술기준(NFTC)에 따른 법적 의무 제어입니다. 임의 변경이 불가하고, 제연팬·방화댐퍼·방화셔터·비상방송·엘리베이터 귀환 등의 동작 시퀀스가 소방 시나리오로 확정되어야 합니다. 일반 자동제어(BAS/BMS)는 에너지 효율과 쾌적성이 목적이지만, 소방 연동은 인명 안전이 목적으로 우선순위가 다릅니다.",
            "tags": ["bas", "fire-interlock", "smoke-control", "code", "priority"]
        },
    ],

    "Dynamo": [
        {
            "q": "Dynamo에서 All Elements of Category 노드는 무엇을 하는 거야?",
            "a": "All Elements of Category 노드는 현재 Revit 문서에서 지정한 카테고리(예: Ducts, Pipes, Mechanical Equipment)의 모든 인스턴스 요소를 리스트로 반환합니다. Categories 노드에서 카테고리를 선택하고 연결하면 됩니다. 단, 이 노드만으로는 Revit UI의 선택 상태가 바뀌지 않습니다. UI 선택까지 변경하려면 Python 노드에서 uidoc.Selection.SetElementIds()를 사용해야 합니다.",
            "tags": ["dynamo", "revit", "category", "all-elements", "selection"]
        },
        {
            "q": "Dynamo에서 FilteredElementCollector와 All Elements of Category의 차이가 뭐야?",
            "a": "All Elements of Category는 Dynamo의 비주얼 노드이고, FilteredElementCollector는 Revit API의 C#/Python 클래스입니다. FilteredElementCollector는 훨씬 세밀한 필터(뷰 기준, 패밀리 타입 기준, 파라미터 기준 등)를 체이닝할 수 있어 대형 모델에서 성능이 좋습니다. Dynamo Python 노드에서 FilteredElementCollector를 사용하면 All Elements of Category보다 빠르고 정밀한 수집이 가능합니다.",
            "tags": ["dynamo", "revit-api", "FilteredElementCollector", "performance"]
        },
        {
            "q": "Dynamo에서 파라미터 값을 읽는 방법이 뭐야?",
            "a": "노드 방식: Element.GetParameterValueByName 노드에 요소 리스트와 파라미터 이름 문자열을 연결합니다. Python 방식: element.LookupParameter('파라미터명').AsString() 또는 AsDouble(), AsInteger()를 사용합니다. 공유 파라미터는 GUID로 찾는 것이 안정적입니다. AsDouble()은 Revit 내부 단위(피트)를 반환하므로 mm 변환이 필요합니다.",
            "tags": ["dynamo", "revit", "parameter", "element", "python"]
        },
        {
            "q": "Dynamo로 파라미터 값을 변경할 때 Transaction이 필요한 이유가 뭐야?",
            "a": "Revit 모델을 변경하는 모든 작업(파라미터 수정, 요소 생성, 삭제)은 Transaction 내에서 실행해야 합니다. Transaction 없이 모델을 변경하면 Revit API에서 InvalidOperationException이 발생합니다. Dynamo에서는 TransactionManager.Instance.EnsureInTransaction(doc)과 TransactionTaskDone()으로 트랜잭션을 관리합니다.",
            "tags": ["dynamo", "revit-api", "transaction", "python"]
        },
        {
            "q": "Dynamo에서 링크 모델의 요소에 접근하는 방법이 뭐야?",
            "a": "현재 문서의 FilteredElementCollector(doc)로는 링크 모델 요소를 수집할 수 없습니다. 링크 모델에 접근하려면: 1) FilteredElementCollector(doc).OfClass(typeof(RevitLinkInstance))로 링크 인스턴스를 찾고, 2) linkInstance.GetLinkDocument()로 링크 문서를 가져온 후, 3) 링크 문서에 FilteredElementCollector(linkDoc)로 수집합니다. 링크 요소는 현재 문서 기준으로 직접 수정이 불가합니다.",
            "tags": ["dynamo", "revit-api", "linked-model", "RevitLinkInstance"]
        },
        {
            "q": "Dynamo에서 엑셀 데이터를 읽어서 Revit 파라미터를 업데이트하는 구조가 어떻게 돼?",
            "a": "1) Data.ImportExcel 또는 Python의 openpyxl/csv.reader로 엑셀 데이터를 읽습니다. 2) 첫 번째 열을 요소 식별자(예: 장비번호, ElementId)로 사용합니다. 3) FilteredElementCollector로 Revit 요소를 수집하고 식별자로 매칭합니다. 4) Transaction 내에서 element.LookupParameter('파라미터명').Set(값)으로 업데이트합니다. 5) 실패 항목은 로그에 기록합니다.",
            "tags": ["dynamo", "excel", "parameter-update", "batch", "python"]
        },
    ],

    "설비도면해석": [
        {
            "q": "설비 도면을 처음 받았을 때 어떤 순서로 읽는 게 좋아?",
            "a": "① 일반사항·범례에서 약어, 선종, 기호, 재료, 특기사항을 먼저 확인합니다. ② 계통도에서 장비 연결과 흐름 방향을 이해합니다. ③ 평면도에서 실제 위치와 경로를 확인합니다. ④ 단면도에서 높이와 간섭 가능성을 봅니다. ⑤ 장비일람표에서 성능값과 규격을 확인합니다. 순서를 건너뛰면 약어 오해나 계통 혼동이 생깁니다.",
            "tags": ["mep", "drawing", "reading-order", "legend"]
        },
        {
            "q": "도면의 범례를 봐야 하는 이유가 뭐야?",
            "a": "같은 약어도 설계 회사, 발주처, 국가에 따라 의미가 다를 수 있습니다. 예를 들어 CWS는 공조 문맥에서는 냉각수(Condenser Water Supply), 위생 문맥에서는 급수(Cold Water Supply)를 뜻할 수 있습니다. 범례와 일반사항에서 해당 도면의 약어 정의를 반드시 확인해야 오해 없이 해석할 수 있습니다.",
            "tags": ["mep", "drawing", "legend", "abbreviation"]
        },
        {
            "q": "계통도와 평면도를 같이 봐야 하는 이유가 뭐야?",
            "a": "계통도는 장비 연결 관계와 흐름을 보여주지만 실제 위치와 경로가 표현되지 않습니다. 평면도는 위치와 경로는 보여주지만 장비 연결 순서와 계통 방향을 파악하기 어렵습니다. 두 도면을 함께 보면 장비 위치 + 연결 관계 + 계통 흐름을 입체적으로 이해할 수 있습니다.",
            "tags": ["mep", "drawing", "system-diagram", "plan"]
        },
        {
            "q": "도면에서 배관이 점선으로 그려진 건 뭘 의미해?",
            "a": "도면에서 점선은 보통 천장 위(숨겨진) 배관, 매립 배관, 또는 가상 경계를 나타냅니다. 정확한 의미는 도면 범례의 선종 정의를 확인해야 합니다. 설계 회사마다 실선/점선/1점 쇄선의 용도 정의가 다를 수 있으므로, 항상 해당 도면의 일반사항을 먼저 확인합니다.",
            "tags": ["mep", "drawing", "line-type", "hidden", "legend"]
        },
        {
            "q": "장비일람표에서 필수로 확인해야 하는 항목이 뭐야?",
            "a": "공통 필수: 장비번호, 명칭, 설치층·위치, 용량, 전원(전압·상·주파수·전류·소비전력), 중량, 특기사항. 공조 장비 추가: 풍량, 정압, 냉방/난방 용량. 배관 장비 추가: 유량, 양정(펌프), 운전압력. 소방 장비 추가: 방수압, 방수량. 일람표 값과 Revit 장비 파라미터, 계통도 사양이 일치하는지 대조합니다.",
            "tags": ["mep", "drawing", "equipment-schedule", "verification"]
        },
    ],
}


def load_knowledge_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def extract_existing_faq(content: str) -> list[dict]:
    """기존 지식 파일에서 FAQ 패턴을 추출한다."""
    qa_pairs = []
    lines = content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.endswith("을 때:") or line.endswith("때:") or line.endswith("때"):
            question_hint = line.rstrip(":")
            answer_lines = []
            j = i + 1
            while j < len(lines) and (lines[j].startswith("-") or lines[j].strip() == ""):
                if lines[j].strip():
                    answer_lines.append(lines[j].strip().lstrip("- "))
                j += 1
            if answer_lines:
                question = question_hint.replace("을 ", "은 ").replace("을때", "할 때")
                answer = " ".join(answer_lines)
                qa_pairs.append({
                    "q": question + "?",
                    "a": answer,
                    "source": "extracted_faq",
                    "tags": []
                })
            i = j
        else:
            i += 1
    return qa_pairs


def generate_variations(qa: dict) -> list[dict]:
    """Q&A에 질문 표현 변형을 추가한다."""
    variations = [qa]
    q = qa["q"]
    a = qa["a"]
    base_tags = qa.get("tags", [])

    # 경어체 ↔ 반말 변형
    casual_q = q.replace("주세요", "줘").replace("어떻게 해야 하나요?", "어떻게 해?").replace("인가요?", "야?").replace("입니까?", "야?")
    if casual_q != q:
        variations.append({"q": casual_q, "a": a, "source": "variation", "tags": base_tags})

    formal_q = q.replace("줘?", "주세요?").replace("야?", "인가요?")
    if formal_q != q and formal_q not in [v["q"] for v in variations]:
        variations.append({"q": formal_q, "a": a, "source": "variation", "tags": base_tags})

    return variations


def save_qa_batch(domain: str, qa_list: list[dict], batch_num: int) -> Path:
    """Q&A 배치를 JSONL 파일로 저장한다."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = QA_OUTPUT / f"qa_{domain}_{batch_num:04d}_{timestamp}.jsonl"
    with open(filename, "w", encoding="utf-8") as f:
        for qa in qa_list:
            record = {
                "domain": domain,
                "question": qa["q"],
                "answer": qa["a"],
                "source": qa.get("source", "manual"),
                "tags": qa.get("tags", []),
                "created_at": datetime.now().isoformat(),
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return filename


def generate_from_knowledge_files() -> int:
    """모든 지식 파일에서 Q&A를 추출·생성한다."""
    total = 0
    for kb_file in sorted(KNOWLEDGE_BASE.glob("*.md")):
        domain = kb_file.stem
        content = load_knowledge_file(kb_file)
        if not content:
            continue

        batch: list[dict] = []

        # 1. 사전 정의된 템플릿 Q&A
        if domain in DOMAIN_QA_TEMPLATES:
            for qa in DOMAIN_QA_TEMPLATES[domain]:
                for variation in generate_variations(qa):
                    variation["source"] = "template"
                    batch.append(variation)

        # 2. 기존 파일에서 FAQ 추출
        extracted = extract_existing_faq(content)
        for qa in extracted:
            qa["tags"] = [domain.lower()]
            batch.append(qa)

        if batch:
            out_file = save_qa_batch(domain, batch, 1)
            print(f"[{domain}] {len(batch)}개 Q&A → {out_file.name}")
            total += len(batch)

    return total


def get_current_disk_usage_percent() -> float:
    """현재 SSD 사용률(%)을 반환한다."""
    import shutil
    usage = shutil.disk_usage("/")
    return (usage.used / usage.total) * 100


def main():
    print("=" * 60)
    print("BIM/MEP Q&A 데이터셋 생성기")
    print(f"시작: {datetime.now().isoformat()}")
    print(f"출력 디렉토리: {QA_OUTPUT}")
    print(f"현재 SSD 사용률: {get_current_disk_usage_percent():.1f}%")
    print("=" * 60)

    total = generate_from_knowledge_files()

    # 통계
    qa_files = list(QA_OUTPUT.glob("*.jsonl"))
    total_size = sum(f.stat().st_size for f in qa_files) / 1024
    print("\n완료!")
    print(f"총 Q&A 쌍: {total}개")
    print(f"생성된 파일: {len(qa_files)}개")
    print(f"총 데이터 크기: {total_size:.1f} KB")
    print(f"현재 SSD 사용률: {get_current_disk_usage_percent():.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
