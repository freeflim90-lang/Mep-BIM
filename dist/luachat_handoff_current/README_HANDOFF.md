# LUAChat Add-in Dashboard Handoff

## Purpose

This package contains the current LUAChat/Revit Assistant code for integration into Addin Dashboard on another computer.

Current product direction:

```text
Search-assisted LUAChat
-> answer user
-> capture Q/A, sources and gaps
-> save as Obsidian knowledge candidates
```

Search-assisted answers are saved as review candidates, not approved knowledge.

## Main Folders

- `source/RevitLUAChat/`
  - Revit add-in source code and Inno Setup installer script.
  - `ApiClient.cs` sends chat and feedback requests.
  - `RevitLUAChat.iss` accepts `/BackendUrl="..."` at install time.

- `backend/`
  - FastAPI backend routes and search/Obsidian logic.
  - `server_total.py`: `/api/revit-assistant/chat` and `/api/revit-assistant/feedback`.
  - `web_search.py`: Tavily, Google CSE, Naver and DuckDuckGo search pipeline.
  - `obsidian_notes.py`: Revit Assistant Q/A note writer.
  - `knowledge_store.py`: knowledge/QA candidate append logic.

- `docs/`
  - MVP direction and setup notes.
  - Start with `revit_luachat_search_to_obsidian_mvp.md`.

- `scripts/`
  - Tunnel helper scripts for pilot/commercial connection tests.

- `config/cloudflared/`
  - Cloudflare Tunnel config example.

## Search APIs

The backend can use:

- `TAVILY_API_KEY`
- `GOOGLE_API_KEY`
- `GOOGLE_CSE_ID`
- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_SECRET`

If a key is missing, that provider is skipped.
DuckDuckGo HTML fallback does not require an API key.

## Backend URL For No Fixed Address Pilot

Start a temporary Cloudflare Quick Tunnel:

```zsh
scripts/start_cloudflare_quick_revit_tunnel.sh
```

It writes the current URL to:

```text
runtime/revit_luachat_backend_url.txt
```

Install on Windows with:

```bat
RevitLUAChat_Setup_v1.2.1.exe /BackendUrl="https://example.trycloudflare.com"
```

## Backend API Key Guard

Backend supports optional API key validation:

```zsh
REVIT_ASSISTANT_API_KEYS="key_1,key_2"
```

Client sends:

```text
X-LUA-BIM-API-Key
```

The add-in reads the key from:

```text
LUA_BIM_LABS_API_KEY
```

Leave `REVIT_ASSISTANT_API_KEYS` empty for local/pilot testing.

## Build Note

The add-in must be built on a Windows/Revit development machine with `RevitAPI.dll` and `RevitAPIUI.dll` available.
The Mac environment cannot complete the Revit add-in build because those Autodesk DLLs are not installed.
