# Revit LUAChat No Fixed Address Pilot

This mode avoids domain purchase and fixed DNS.

It is suitable for demos, pilots and internal tests. It is not suitable for long-lived commercial installs because the backend URL can change whenever the quick tunnel restarts.

## Flow

```text
Revit Add-in
-> temporary trycloudflare.com URL
-> Cloudflare Quick Tunnel
-> Mac backend http://127.0.0.1:8000
```

## Start Backend

```zsh
scripts/start_server.sh
```

## Start Temporary Tunnel

```zsh
scripts/start_cloudflare_quick_revit_tunnel.sh
```

The script writes the current backend URL to:

```text
runtime/revit_luachat_backend_url.txt
```

It also creates a Windows helper snippet:

```text
runtime/install_revit_luachat_with_current_tunnel.bat
```

## Installer Parameter

The Inno installer now accepts a runtime backend URL:

```bat
RevitLUAChat_Setup_v1.2.1.exe /BackendUrl="https://example.trycloudflare.com"
```

The installer writes that value to the machine environment variable:

```text
LUA_BIM_LABS_BACKEND_URL
```

Restart Revit after installation.

## Manual Fix For Existing Install

If the tunnel URL changes, update Windows and restart Revit:

```bat
setx LUA_BIM_LABS_BACKEND_URL "https://new-url.trycloudflare.com" /M
```

## Limitation

This removes domain cost, but it does not provide a stable product endpoint. If the tunnel URL changes, installed clients must be updated.
