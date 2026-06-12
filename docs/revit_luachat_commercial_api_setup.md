# Revit LUAChat Commercial API Setup

## Product Direction

Commercial users should not install or sign in to Tailscale.

The add-in should call one stable HTTPS endpoint:

```text
https://api.luabimlabs.com
```

Cloudflare Tunnel maps that public HTTPS hostname to the private Mac backend:

```text
https://api.luabimlabs.com -> Cloudflare Tunnel -> http://127.0.0.1:8000
```

## Add-in Behavior

`RevitLUAChat` now defaults to:

```text
https://api.luabimlabs.com
```

The installer also writes:

```text
LUA_BIM_LABS_BACKEND_URL=https://api.luabimlabs.com
```

Manual override is still possible for internal testing.

## Backend Protection

The backend supports an optional API key allowlist.

Set this on the backend host:

```zsh
REVIT_ASSISTANT_API_KEYS="key_1,key_2"
```

If `REVIT_ASSISTANT_API_KEYS` is empty, local development remains open.
If it is set, Revit clients must send:

```text
X-LUA-BIM-API-Key: key_1
```

The add-in reads the key from:

```text
LUA_BIM_LABS_API_KEY
```

For commercial release, this should be replaced or complemented by license-account based authentication. Do not hardcode a shared secret in the public installer.

## One-Time Cloudflare Setup

Install Cloudflare Tunnel CLI on the Mac:

```zsh
brew install cloudflared
```

Log in:

```zsh
cloudflared tunnel login
```

Create a named tunnel:

```zsh
cloudflared tunnel create lua-bim-labs-revit-api
```

Copy `config/cloudflared/revit-api-config.example.yml` to the Cloudflare config location and update the `credentials-file` path to the generated JSON file:

```zsh
mkdir -p ~/.cloudflared
cp config/cloudflared/revit-api-config.example.yml ~/.cloudflared/config.yml
```

Create the DNS route:

```zsh
cloudflared tunnel route dns lua-bim-labs-revit-api api.luabimlabs.com
```

## Run

Start the backend:

```zsh
scripts/start_server.sh
```

Start the tunnel:

```zsh
scripts/start_cloudflare_revit_tunnel.sh
```

Check:

```zsh
curl https://api.luabimlabs.com/
```

Expected result: JSON containing `status: running`.

## Release Rule

For product builds:

- Do not require Tailscale.
- Do not expose `127.0.0.1`, LAN IP, or tailnet hostnames in the installer.
- Keep the backend URL stable at `https://api.luabimlabs.com`.
- Use HTTPS only.
