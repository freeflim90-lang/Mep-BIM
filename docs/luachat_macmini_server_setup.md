# LUAChat Mac mini Server Setup

이 Mac mini는 LUAChat 중앙 서버 역할을 한다.

- Revit Addin 설치 PC는 질문과 Revit 컨텍스트만 보낸다.
- Mac mini가 내부 지식/Obsidian을 먼저 검색한다.
- 지식이 부족하면 Mac mini가 웹 검색 API를 호출한다.
- 답변, 출처, 피드백은 Obsidian vault에 Markdown으로 축적된다.

## 1. Mac mini 환경변수

프로젝트 루트의 `.env`에 아래 값을 설정한다.

```bash
LUA_CHAT_TOKEN=공유_비밀키

# 최소 하나 이상 권장. 없으면 DuckDuckGo fallback만 동작한다.
TAVILY_API_KEY=
GOOGLE_API_KEY=
GOOGLE_CSE_ID=
NAVER_CLIENT_ID=
NAVER_CLIENT_SECRET=

# 유료 LLM 합성이 필요할 때만 사용한다.
PAID_AI_ENABLED=false
DEEPSEEK_API_KEY=
```

## 2. Mac mini 서버 실행

```bash
cd "/Users/choejeong-yeon/LUA BIM LABS"
./scripts/start_server.sh
```

헬스 체크:

```bash
curl http://127.0.0.1:8000/api/luachat/health
```

같은 네트워크의 Windows/Revit PC에서는 아래 주소로 접속한다.

```text
http://MAC_MINI_IP:8000/api/luachat
```

외부 현장/다른 네트워크에서 쓸 경우에는 ngrok 또는 Cloudflare Tunnel을 붙이고, 터널 주소를 사용한다.

```text
https://your-tunnel-url/api/luachat
```

## 3. Addin 요청 형식

```http
POST /api/luachat
Authorization: Bearer 공유_비밀키
Content-Type: application/json
```

```json
{
  "user_id": "revit_user",
  "message": "사용자 질문",
  "revit_context": "Project, Active View, 선택 요소 정보",
  "client_version": "LUAChat",
  "source": "revit-addin"
}
```

응답:

```json
{
  "status": "ok",
  "brand": "LUA BIM LABS",
  "agent": "Revit_Addin",
  "answer": "답변 내용",
  "sources": [
    {
      "path": "data/knowledge_base/Revit_Addin.md",
      "score": 80
    }
  ],
  "note_path": "obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/Revit_Assistant_QA/QA - ....md",
  "needs_more": false
}
```

## 4. Addin 피드백 요청 형식

```http
POST /api/luachat/feedback
Authorization: Bearer 공유_비밀키
Content-Type: application/json
```

```json
{
  "user_id": "revit_user",
  "message": "원 질문",
  "answer": "원 답변",
  "is_good": true,
  "note_path": "서버가 반환한 note_path",
  "feedback": "Revit Add-in answer accepted"
}
```

## 5. Windows/Revit PC 설정

검색 API 키는 Windows PC에 두지 않는다. Addin PC에는 Mac mini 주소와 토큰만 설정한다.

```bat
setx LUA_CHAT_URL "http://MAC_MINI_IP:8000/api/luachat"
setx LUA_CHAT_TOKEN "공유_비밀키"
```

설정 후 Revit을 완전히 종료했다가 다시 실행한다.

확인:

```bat
echo %LUA_CHAT_URL%
echo %LUA_CHAT_TOKEN%
```

## 6. 운영 흐름

```text
Revit Addin PC
  -> /api/luachat 질문 전송
Mac mini
  -> Obsidian/지식 베이스 검색
  -> 부족 시 웹 검색
  -> 답변 생성
  -> Obsidian에 Q&A 저장
  -> Addin으로 답변 반환
Addin PC
  -> 답변 표시
  -> 좋아요/아쉬워요를 /api/luachat/feedback 전송
```
