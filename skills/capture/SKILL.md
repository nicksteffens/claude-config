---
name: capture
description: "Quick capture a thought, link, or snippet into the second-brain inbox. Zero friction — just type /capture followed by your note."
argument-hint: "<your note>"
---

# Capture

Drop a timestamped note into the second-brain inbox.

## Behavior

1. Take the user's argument text as the note body
2. Generate a filename from the current timestamp: `YYYY-MM-DD-HHmm-<slugified-first-5-words>.md`
3. Write the file to `~/github/nicksteffens/second-brain/00-inbox/` with this format:

```markdown
---
captured: YYYY-MM-DD HH:mm
---

<user's note text>
```

4. Confirm with the filename and a one-line summary

## Rules

- No questions asked — just capture it
- If no argument is provided, ask "What do you want to capture?"
- Keep the filename short and readable
- Do not organize, categorize, or edit the note — that happens during review
