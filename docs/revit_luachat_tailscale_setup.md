# Revit LUAChat Tailscale Setup

This is now an internal testing path only.

For commercial users, use `docs/revit_luachat_commercial_api_setup.md` and the public HTTPS endpoint:

```text
https://api.luabimlabs.com
```

## Current backend endpoint

Use this URL on Windows PCs that are logged in to the same Tailscale tailnet:

```text
http://choejeong-yeon-ui-macmini.tailf5784f.ts.net:8000
```

Short tailnet-only form:

```text
http://choejeong-yeon-ui-macmini:8000
```

## Windows add-in setting

Commercial installers no longer configure the Tailscale URL. Use this only for internal testing or older test builds.

Run this in Windows Command Prompt, then fully restart Revit:

```bat
setx LUA_BIM_LABS_BACKEND_URL "http://choejeong-yeon-ui-macmini.tailf5784f.ts.net:8000"
```

Use the command above only when fixing an older install manually.

Check in a browser on the Windows PC:

```text
http://choejeong-yeon-ui-macmini.tailf5784f.ts.net:8000/
```

Expected result: JSON containing `status: running`.

## Mac restart checklist

1. Start the LUA BIM LABS backend:

```zsh
scripts/start_server.sh
```

2. Start Tailscale userspace serve:

```zsh
scripts/start_tailscale_revit_backend.sh
```

3. Confirm serve status shows:

```text
http://choejeong-yeon-ui-macmini.tailf5784f.ts.net:8000 (tailnet only)
|-- / proxy http://127.0.0.1:8000
```

## Notes

- The Homebrew CLI Tailscale is installed because the GUI app requires an administrator password.
- Tailscale userspace mode is kept alive by this user LaunchAgent:
  `~/Library/LaunchAgents/com.luabimlabs.tailscale-userspace.plist`
- This setup keeps the backend private to Tailscale instead of exposing it publicly.
- If Tailscale asks for login again, run the command printed by `scripts/start_tailscale_revit_backend.sh` and approve the browser login URL.

## Installer behavior

Commercial installers must not install Tailscale or point to a tailnet hostname.
Keep this path for internal diagnostics only.
