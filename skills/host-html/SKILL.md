---
name: host-html
description: "Use when the user wants to preview, host, boot up, or serve a chunk of raw HTML locally — e.g. pasted email markup, a snippet, or a Movable Ink block. Spins up a throwaway local HTTP server and returns both a browser link and a scannable QR code for testing on a phone on the same Wi-Fi."
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

Every run hands back **both** a browser link and a phone QR — no mode to pick.

1. **Write to a temp dir, never the repo.** Use `mktemp -d`, write the HTML to `index.html` inside it.
2. **Wrap fragments.** If the content has no `<html>` tag, wrap it in a full document: `<!DOCTYPE html>`, `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, and a `<body style="margin:0;padding:0;">`. Fix obvious structural gaps (e.g. a `<td>` with no `<tr>`).
3. **Start the server in the background**, bound to `0.0.0.0` so the local browser *and* phones on the same Wi-Fi can both reach it. Uncommon port (default `8347`, bump if taken), `run_in_background: true`:
   ```
   python3 -m http.server 8347 --bind 0.0.0.0 --directory <tempdir>
   ```
4. **Verify** with `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8347/` — expect `200`.
5. **Get the LAN IP** with `ipconfig getifaddr en0` (fall back to `en1`).
6. **Hand back both:**
   - **Browser:** http://127.0.0.1:8347/
   - **Phone:** a scannable QR of the **LAN** URL — never the loopback one, since a phone scanning `127.0.0.1` would hit itself, not this machine:
     ```
     qrencode -t ANSIUTF8 "http://<lan-ip>:8347/"
     ```
     If `qrencode` is missing, install it once with `brew install qrencode` (local, no external calls). Never use an online QR service — it leaks the URL.

If the phone can't connect: macOS may prompt to allow incoming connections for Python (accept it), or the firewall (System Settings → Network → Firewall) may be blocking it.

## Tearing down

When the user says to kill/stop it, `TaskStop` the background task, then confirm it's down with the same curl (expect `000`/failure).

## Notes

- Binding `0.0.0.0` exposes the server to the local network for as long as it runs, so tear it down when done.
- Merge/personalization tokens (`%%...%%`, `{camp.id}`, `{{UserAttribute[...]}}`, `{{Campaign Id}}`, etc.) pass through as literal text; the remote server may serve a fallback rather than personalized content. Mention this if the HTML contains them.
- SDK globals (e.g. `window.moengage`) won't exist outside their host app, so click/tracking handlers fall through to plain navigation. Fine for visual/layout testing, not for testing tracking or deeplinks.
- The temp dir self-clears on reboot; offer to `trash` it if the user wants it gone sooner (never `rm`).
