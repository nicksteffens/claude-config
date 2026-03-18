---
name: personality
description: Swap between Star Wars droid personalities for tone and statusline
user_invocable: true
---

# Personality Swap

Switch the active droid personality. This changes the tone/personality section in CLAUDE.md, the statusline quips, and the spinner verbs.

## Instructions

1. **Read available personalities** by globbing `~/.claude/personalities/*.md` and reading each file's frontmatter to get the name and description.

2. **Present choices** using `AskUserQuestion` with the available personalities. Each option should show the droid name and description. Use header "Personality".

3. **Read the selected personality file** in full.

4. **Update CLAUDE.md tone section**: Read `~/.claude/CLAUDE.md`, then use the Edit tool to replace the `## Tone & Personality` section (from `## Tone & Personality` up to but not including the next `#` heading that is NOT under `## Tone & Personality`) with the content from the personality file's `## Tone` section, renamed as `## Tone & Personality`.

5. **Regenerate statusline script**: Parse the `## Quips` section from the personality file. Each `### category` contains quip lines (starting with `- "`). Extract the tag from frontmatter. Write `~/.claude/statusline-command.sh` using this template:

```bash
#!/bin/bash
# {name} status line for Claude Code
# {description}

INPUT=$(cat)

MODEL=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('model',{}).get('display_name','unknown'))" 2>/dev/null || echo "unknown")
CONTEXT=$(echo "$INPUT" | python3 -c "import sys,json; print(int(json.load(sys.stdin).get('context_window',{}).get('used_percentage',0)))" 2>/dev/null || echo "0")
DIR=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('workspace',{}).get('current_dir','').split('/')[-1])" 2>/dev/null || echo "")

# {name}'s mood depends on context usage
if [ "$CONTEXT" -gt 80 ]; then
  QUIPS=(
    {angry_quips}
  )
elif [ "$CONTEXT" -gt 50 ]; then
  QUIPS=(
    {grumpy_quips}
  )
elif [ "$CONTEXT" -gt 20 ]; then
  QUIPS=(
    {annoyed_quips}
  )
else
  QUIPS=(
    {fresh_quips}
  )
fi

# Pick a quip based on seconds so it rotates but doesn't flicker
INDEX=$(( $(date +%s) / 15 % ${{#QUIPS[@]}} ))
QUIP="${{QUIPS[$INDEX]}}"

echo "[{tag}] ${{MODEL}} | ${{DIR}} | ${{QUIP}}"
```

Replace `{angry_quips}`, `{grumpy_quips}`, `{annoyed_quips}`, `{fresh_quips}` with the quoted quip lines from each `###` section, one per line with 4-space indent. Replace `{tag}`, `{name}`, `{description}` from frontmatter.

6. **Update spinner verbs**: Parse the `## Spinner Verbs` section from the personality file. Each line starting with `- ` is a verb. Read `~/.claude/settings.json`, update (or add) the `spinnerVerbs` key:

```json
{
  "spinnerVerbs": {
    "mode": "replace",
    "verbs": ["Verb1", "Verb2", "..."]
  }
}
```

Write the updated settings back, preserving all other keys.

7. **Confirm the swap** with a short message in the new personality's voice.
