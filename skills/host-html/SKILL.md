---
name: host-html
description: "Use when the user wants to preview, host, boot up, or serve a chunk of raw HTML locally in a browser — e.g. pasted email markup, a snippet, or a Movable Ink block. Spins up a throwaway local HTTP server."
argument-hint: "[paste HTML here, or leave blank to use clipboard]"
---

# Host HTML Locally

Take a chunk of HTML and serve it on a throwaway local HTTP server so the user can open it in a browser.

## Get the HTML

In priority order:
1. HTML passed as the argument, or pasted into the current/recent message.
2. If none provided (or the user says "clipboard" / "what I copied"), run `pbpaste`.

If you still have nothing, ask what to host.

## Serve it

1. **Write to a temp dir, never the repo.** Use `mktemp -d`, write the HTML to `index.html` inside it.
2. **Wrap fragments.** If the content has no `<html>` tag, wrap it in a full document: `<!DOCTYPE html>`, `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, and a `<body style="margin:0;padding:0;">`. Fix obvious structural gaps (e.g. a `<td>` with no `<tr>`).
3. **Start the server in the background** on an uncommon port (default `8347`, bump if taken):
   ```
   python3 -m http.server 8347 --bind 127.0.0.1 --directory <tempdir>
   ```
   Use `run_in_background: true`.
4. **Verify** with `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8347/` — expect `200`.
5. Give the user the URL: **http://127.0.0.1:8347/**

## Tearing down

When the user says to kill/stop it, `TaskStop` the background task, then confirm it's down with the same curl (expect `000`/failure).

## Notes

- Bind to `127.0.0.1` only — local preview, not exposed to the network.
- Merge/personalization tokens (`%%...%%`, `{camp.id}`, etc.) pass through as literal text; the remote server may serve a fallback image. Mention this if the HTML contains them.
- The temp dir self-clears on reboot; offer to `trash` it if the user wants it gone sooner (never `rm`).
