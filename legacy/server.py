import os
import json
import asyncio
from fastapi import FastAPI, WebSocket
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

AGENTS = ["건축", "구조", "토목", "위생", "공조배관", "공조덕트", "소방기계", "소방전기", "전기", "통신"]

@app.websocket("/ws/office")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # 상태 및 토큰 사용량 초기화
        agent_states = {
            name: {"status": "Idle", "message": "대기 중...", "tokens": 0} 
            for name in AGENTS + ["조율차장"]
        }
        
        issue_description = "지하 1층 전이보 구간 대형 덕트 및 케이블 트레이 복합 간섭 발생"
        
        system_prompt = f"""
        당신은 설계·시공 BIM 협의를 진행하는 AI 가상 사무실입니다.
        제시된 이슈에 대해 {', '.join(AGENTS)} 담당자 순서대로 의견을 개진하되,
        반드시 답변 시작할 때 '[[공종명]]' 태그를 정확히 붙여주세요. (예: [[건축]] 건축 의견입니다...)
        모든 공종이 끝나면 마지막에 [[조율차장]] 태그를 붙이고 최종 마스터 조율안을 도출하세요.
        """

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"검토 이슈: {issue_description}"}
            ],
            temperature=0.4,
            stream=True
        )

        current_agent = None
        buffer = ""

        for chunk in response:
            token = chunk.choices[0].delta.content
            if not token:
                continue
            
            buffer += token
            
            for agent in AGENTS + ["조율차장"]:
                tag = f"[[{agent}]]"
                if tag in buffer:
                    if current_agent and current_agent in agent_states:
                        agent_states[current_agent]["status"] = "Idle"
                    
                    current_agent = agent
                    if current_agent in agent_states:
                        agent_states[current_agent]["status"] = "Active"
                        agent_states[current_agent]["message"] = ""
                    
                    buffer = buffer.replace(tag, "")
            
            if current_agent and current_agent in agent_states:
                agent_states[current_agent]["message"] += token
                # 💡 실시간 토큰 카운트 업 (대략적인 추정치로 1글자/조각당 1토큰 가산)
                agent_states[current_agent]["tokens"] += 1
                
                await websocket.send_text(json.dumps({
                    "type": "STATE_UPDATE",
                    "data": agent_states,
                    "current": current_agent
                }))
                await asyncio.sleep(0.01)

    except Exception as e:
        print(f"웹소켓 통신 에러: {e}")
