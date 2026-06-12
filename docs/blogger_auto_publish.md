# Blogger Auto Publish

This publishes LUA BIM LABS English MEP BIM posts to:

https://engineer250212.blogspot.com/

## Setup

1. In Google Cloud Console, enable Blogger API v3.
2. Create an OAuth Client ID for a Desktop app.
3. If a Client Secret was pasted into chat or shared anywhere, rotate it before publishing.
4. Use either the downloaded JSON file or local environment variables.

If you created a Web application OAuth client instead of a Desktop app, add this Authorized redirect URI:

```text
http://localhost:8080/
```

The trailing slash is important. If Google shows `400 error: redirect_uri_mismatch`, add the exact URI above to the OAuth client or create a new OAuth Client ID with Application type `Desktop app`.

### Option A: JSON File

Download the OAuth JSON file and save it as:

```bash
config/blogger/client_secret.json
```

### Option B: Environment Variables

```bash
export BLOGGER_CLIENT_ID="your-new-client-id"
export BLOGGER_CLIENT_SECRET="your-new-client-secret"
```

Do not commit these values.

## Install

Install dependencies:

```bash
python3 -m pip install -r scripts/requirements-blogger.txt
```

## Dry Run

```bash
python3 scripts/blogger_publish.py \
  --meta-json content/blogger/2026-05-29-why-mep-bim-skills-matter.meta.json \
  --content-file content/blogger/2026-05-29-why-mep-bim-skills-matter.html \
  --dry-run
```

## Publish

```bash
python3 scripts/blogger_publish.py \
  --meta-json content/blogger/2026-05-29-why-mep-bim-skills-matter.meta.json \
  --content-file content/blogger/2026-05-29-why-mep-bim-skills-matter.html
```

The first publish opens a Google OAuth page. After approval, the token is stored in:

```bash
config/blogger/token.json
```

Keep both `client_secret.json` and `token.json` private.
