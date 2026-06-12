import os
import json
import asyncio
from fastapi import FastAPI, WebSocket
from openai import OpenAI

app = FastAPI()

# OpenAI 호환 DeepSeek 클라이언트 설정
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

# 10대 공종 마스터 리스트 및 초기 상태
AGENTS = ["건축", "구조", "토목", "위생", "공조배관", "공조덕트", "소방기계", "소방전기", "전기", "통신"]
agent_states = {name: {"status": "Idle", "message": "대기 중"} for name in AGENTS}

@app.websocket("/ws/office")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # 차장님이 던져주실 실무 간섭 시나리오 가상 지정
        issue_description = "지하 1층 전이보 구간 대형 덕트 및 케이블 트레이 복합 간섭 발생"
        
        system_prompt = f"""
        당신은 설계·시공 BIM 협의를 진행하는 AI 가상 사무실입니다.
        제시된 이슈에 대해 {', '.join(AGENTS)} 담당자 순서대로 의견을 개진하되,
        반드시 답변 시작할 때 '[[공종명]]' 태그를 정확히 붙여주세요. (예: [[건축]] 건축 의견입니다...)
        모든 공종이 끝나면 마지막에 [[조율차장]] 태그를 붙이고 최종 마스터 조율안을 도출하세요.
        """

        # DeepSeek API 스트리밍 호출 (stream=True)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"검토 이슈: {issue_description}"}
            ],
            temperature=0.4,
            stream=True # ◀ 실시간 스트리밍 활성화
        )

        current_agent = None
        buffer = ""

        # 딥시크가 뱉는 글자 조각(Chunk)을 실시간으로 추적
        for chunk in response:
            token = chunk.choices[0].delta.content
            if not token:
                continue
            
            buffer += token
            
            # 텍스트 스트림 중에서 [[공종명]] 태그를 감지하여 현재 Active 에이전트 변경
            for agent in AGENTS + ["조율차장"]:
                tag = f"[[{agent}]]"
                if tag in buffer:
                    # 기존 에이전트가 있었다면 Idle로 복귀
                    if current_agent and current_agent in agent_states:
                        agent_states[current_agent]["status"] = "Idle"
                    
                    # 새로운 에이전트를 Active로 전환
                    current_agent = agent
                    if current_agent in agent_states:
                        agent_states[current_agent]["status"] = "Active"
                        agent_states[current_agent]["message"] = "" # 대사 초기화
                    
                    # 버퍼에서 태그 제거
                    buffer = buffer.replace(tag, "")
            
            # 현재 활성화된 에이전트의 말풍선 메시지에 실시간 토큰 누적
            if current_agent and current_agent in agent_states:
                agent_states[current_agent]["message"] += token
                
                # 대시보드 화면(웹소켓)으로 현재 10개 공종 상태 통째로 전송
                await websocket.send_text(json.dumps({
                    "type": "STATE_UPDATE",
                    "data": agent_states,
                    "current": current_agent
                }))
                
                # 브라우저 과부하 방지를 위한 미세한 딜레이 (DeepSeek 속도가 워낙 빨라서 조율)
                await asyncio.sleep(0.01)

    except Exception as e:
        print(f"웹소켓 통신 에러: {e}")
