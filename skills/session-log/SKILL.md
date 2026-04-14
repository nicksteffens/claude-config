---
name: session-log
description: "Create a new session log entry in the second-brain. Extracts context from the current session and asks for your assessment."
---

# Session Log

Create a session log entry in `~/github/nicksteffens/second-brain/01-sessions/`.

## Behavior

1. **Determine session number**: Look at existing files in `01-sessions/YYYY/MM/` for today's date. Count existing sessions and increment.

2. **Extract from conversation context**:
   - Objective (what were we working on)
   - Duration (estimate from session start to now)
   - Repos touched (from file paths and git operations in the session)
   - Tags (infer from work done — use tag keywords: bug-fix, feature, refactor, testing, infrastructure, eslint, design-system, api, documentation, debugging, performance, upgrade, automation, multi-repo, research, review)
   - What was accomplished (summarize key actions)
   - Challenges encountered
   - Key insight

3. **Ask the user** (batch these questions):
   - Rating (1-10)
   - Role (directing, collaborating, reviewing, learning)
   - Wins (what went well — for future distillation)
   - Improvements (what should be better next time)
   - Any key decisions made
   - Follow-up items

4. **Write the file**: `01-sessions/YYYY/MM/YYYY-MM-DD-session-N.md` using the session log format with frontmatter matching this schema:

```yaml
---
title: "<truncated objective, max 80 chars>"
date: YYYY-MM-DD
session: N
duration: "<duration>"
rating: N
objective: "<full objective>"
repos: ["repo1", "repo2"]
tags: ["tag1", "tag2"]
role: "<role>"
shortcut: "<sc-NNNNN if applicable>"
wins:
  - "<win 1>"
improvements:
  - "<improvement 1>"
decisions:
  - "<decision 1>"
---

### What We Accomplished
<bulleted list>

### Challenges Encountered
<bulleted list>

### Most Valuable Collaboration
<paragraph>

### Key Insight
<paragraph>

### Follow-Up Items
- [ ] <item>

### Role Distribution
**Human:** <description>
**Claude:** <description>

### Success Factors
<paragraph>
```

5. **Commit**: Stage and commit the new session log file.

## Rules

- Always check for existing sessions today before assigning a session number
- Frontmatter must be valid YAML — quote strings with special characters
- Tags should use the established vocabulary: bug-fix, feature, refactor, testing, infrastructure, eslint, design-system, api, documentation, debugging, performance, upgrade, automation, multi-repo, research, review
- The session log file path must match the pattern `01-sessions/YYYY/MM/YYYY-MM-DD-session-N.md`
