from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio

app = FastAPI()  # 💡 uvicorn main:app 호출을 위한 인스턴스 정의 (NameError 해결)

# 웹 브라우저 접속을 위한 CORS 허용 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 실시간 웹소켓 세션을 관리하는 매니저 클래스
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"📡 [웹소켓] 새로운 클라이언트 연결 성공 (총 연결 수: {len(self.active_connections)})")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"🔌 [웹소켓] 클라이언트 연결 해제 (남은 연결 수: {len(self.active_connections)})")

    async def broadcast(self, message: str):
        # 연결된 모든 대시보드 브라우저로 실시간 수치 패킷 송신
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"⚠️ [송신오류] 패킷 전달 실패: {e}")

manager = ConnectionManager()

# 🎯 대시보드가 접속하는 웹소켓 라우터 주소
@app.websocket("/ws/office")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)  # 💡 비동기 함수 안에서 올바르게 await 실행 (SyntaxError 해결)
    try:
        while True:
            # 대시보드나 외부 테스트 스크립트로부터 데이터를 수신하는 대기 루프
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                print(f"📥 [수신 데이터]: type={payload.get('type')}, current={payload.get('current')}")
                
                # 수신받은 패킷을 연결된 모든 브라우저 화면으로 즉시 브로드캐스팅(재전송)
                await manager.broadcast(data)
            except json.JSONDecodeError:
                print("⚠️ [수신오류] 올바르지 않은 JSON 데이터 포맷입니다.")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"⚠️ [세션오류] 예외 발생: {e}")
        manager.disconnect(websocket)

@app.get("/")
def read_root():
    return {"status": "MIMIC BIM Backend is Running"}
