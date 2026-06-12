@echo off
set BACKEND_URL=https://included-newman-airlines-necessity.trycloudflare.com
echo Installing RevitLUAChat with backend %BACKEND_URL%
RevitLUAChat_Setup_v1.2.1.exe /BackendUrl="%BACKEND_URL%"
