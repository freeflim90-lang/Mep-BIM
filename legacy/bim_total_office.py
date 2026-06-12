import os
from openai import OpenAI

# 1. 딥시크 API 클라이언트 초기화
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

def run_total_bim_office(issue_description):
    print("🏗️ [10대 공종 통합 가상 사무실] 전 공종 교차 검토 및 토론을 시작합니다...\n")
    
    system_prompt = """
    당신은 종합 건설 프로젝트의 설계·시공 BIM 협의를 진행하는 AI 가상 사무실의 총괄 디렉터입니다.
    입력된 복합 공종 간섭 및 설계 이슈에 대해, 다음 10개 전문 공종 담당자의 페르소나(Persona)에 완전히 빙의하여 각자의 관점에서 핵심 의견을 개진하세요.
    
    [토론 참여자 라인업]
    1. 건축 담당자 (Architect): 공간 프로그램, 방화구획, 법적 천장고(CH), 마감 제약 검토
    2. 구조 담당자 (Structural): 보(Beam)/기둥/슬래브 구조 안전성, 타공(Sleeve) 가능 여부 및 보강 의견
    3. 토목 담당자 (Civil): 대지 경계, 구조물 인입 및 기초 레벨(GL), 외부 관로 연동 검토
    4. 위생배관 담당자 (Plumbing): 오배수 횡주관 자연유하 구배, 최상단 레벨 제약 검토
    5. 공조배관 담당자 (HVAC Piping): 냉온수/냉매 관로 경로, 단열재 마감 외경 및 밸브 공간 검토
    6. 공조덕트 담당자 (HVAC Duct): 대형 사각/원형 덕트 횡단 경로, 종횡비(Aspect Ratio), 정압 손실 검토
    7. 소방기계 담당자 (Fire Mech): 스프링클러 살수반경, 헤드 배치, 소방 주배관/교차관로 레이어 검토
    8. 소방전기 담당자 (Fire Elec): 감지기 선로 사각지대 및 방화셔터/제연 연동 배선 검토
    9. 전기 인프라 담당자 (Electrical): 강전 케이블 트레이 곡률 반경, 누수 회피를 위한 상부 레이어 배치 검토
    10. 통신 인프라 담당자 (Telecom): 약전 트레이 경로, 전력선과의 이격 거리를 통한 전자파 간섭(EMI) 차단 검토

    [출력 포맷 및 순서]
    1. [공종별 난상 토론]: 1번부터 10번까지 순서대로 각 공종의 기술적 입장과 타 공종에 대한 요구사항을 생생하게 기술하세요.
    2. [종합 조율 결론]: 최종적으로 '13년 차 Senior MEP BIM Engineer(차장)'의 종합 시각에서, 건축/구조/토목의 제약을 100% 준수하면서도 7개 MEP 공종의 시공성을 극대화하는 정밀한 [마스터 조율안]을 도출하세요.
    """

    user_prompt = f"현재 검토 이슈:\n{issue_description}"

    # DeepSeek-V3 엔진 가동 (10개 공종이 아무리 길게 써도 비용은 수십 원 미만)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4, # 현실적이고 일관성 있는 엔지니어링 팩트 기반 출력을 위해 조절
        stream=False
    )
    
    return response.choices[0].message.content

# 🚀 실제 종합 간섭 시나리오 구동 테스트
if __name__ == "__main__":
    # 토목 인입 레벨과 구조 전이보, 건축 천장고, MEP 7대 공종이 모두 얽힌 복합 이슈
    total_project_issue = (
        "지하 1층 주차장 진입 램프 구간입니다. "
        "토목 외부 인입 관로 레벨(GL) 고정으로 인해 위생 배수 메인 관이 구조 전이보(Transfer Beam) 구간을 "
        "반드시 관통해야 구배가 나오는 상황입니다. 하지만 구조에서는 타공 불가 의견을 냈습니다. "
        "동일 선상 하부로 1400x600 대형 공조덕트와 강전 케이블 트레이가 교차하고 있어, "
        "이를 우회 시 건축 법적 천장고(CH 2.3m) 및 주차장 차량 통행 높이 확보가 불가능한 복합 간섭 상황입니다."
    )
    
    coordination_report = run_total_bim_office(total_project_issue)
    print(coordination_report)
