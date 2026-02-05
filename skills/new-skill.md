---
name: new-skill
description: Create a new Claude Code skill with tests
user_invocable: true
---

# New Skill Creator

Creates a new Claude Code skill with comprehensive tests using the skill-builder framework.

## Instructions

1. **Ask the user for skill details**
   - Skill name (kebab-case, e.g., validate-json, create-component)
   - Should it be user-invocable? (can they use /skill-name)
   - Is this for the current repo or global? (--local vs --global)
   - Should we skip test creation? (usually no)

2. **Run the scaffold tool**
   ```bash
   ~/.claude/agents/skill-builder/scaffold.sh SKILL_NAME [flags]
   ```

   Flags:
   - `--user-invocable` - Make it a slash command
   - `--local` - Create in current repo's .claude/skills/ (team-shared)
   - `--global` - Create in ~/.claude/skills/ (default, personal)
   - `--no-tests` - Skip test file creation

3. **Show what was created**
   - List the files created
   - Show the skill file path
   - Show the test file path (if created)
   - Explain next steps

4. **Guide next steps**
   - Tell user to edit the [EDIT ME] placeholders
   - Show how to run tests: `cd ~/.claude/agents/tests && ./run_tests.sh SKILL_NAME`
   - If --local, remind to commit and share with team

## Examples

<example>
User: "/new-skill"
Assistant: "I'll help you create a new skill. What would you like to call it? (use kebab-case like 'validate-json' or 'create-component')"
User: "create-component"
Assistant: "A few questions:
1. Should this be user-invocable as /create-component? (yes/no)
2. Is this for the current repo only, or global? (local/global)
3. Should I create tests? (yes/no - recommend yes)"
User: "yes, local, yes"
Assistant: [Runs scaffold.sh create-component --user-invocable --local]
"✓ Created skill files:
- .claude/skills/create-component.md
- .claude/tests/integration/create_component/test_create_component.py

Next steps:
1. Edit .claude/skills/create-component.md and fill in [EDIT ME] placeholders
2. Update the test file with specific test cases
3. Run tests: cd .claude/tests && pytest integration/create_component/ -v
4. Commit and share with team: git add .claude/skills/ .claude/tests/"
</example>

<example>
User: "/new-skill validate-json --global"
Assistant: [Detects inline arguments, runs scaffold]
"✓ Created global skill:
- ~/.claude/skills/validate-json.md
- ~/.claude/agents/tests/integration/validate_json/test_validate_json.py

This is a global skill (available in all projects).
Edit the skill file and fill in the [EDIT ME] placeholders."
</example>

## Important Notes

- **Naming**: Always use kebab-case (my-skill, not MySkill or my_skill)
- **Local vs Global**:
  - Local: Repo-specific, shared with team via git
  - Global: Personal, available everywhere
- **User-invocable**: Let users call it as /skill-name
- **Tests**: Always recommend creating tests

## Tool Usage

Use **Bash** tool to run the scaffold script:
```bash
~/.claude/agents/skill-builder/scaffold.sh SKILL_NAME --user-invocable --local
```

Check current directory to determine if --local makes sense (are we in a git repo?).
