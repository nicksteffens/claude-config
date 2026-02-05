# Repository-Specific Skills

Create skills that are specific to a particular codebase and can be shared with your team.

## Overview

Skills can be **global** (available everywhere) or **repository-specific** (only for a particular codebase).

### Global Skills
- Location: `~/.claude/skills/`
- Available in all projects
- Personal or general-purpose
- Examples: `format-json`, `explain-code`, `commit-message`

### Repository-Specific Skills
- Location: `.claude/skills/` in the repo
- Only active when working in that repo
- Shared with team (committed to git)
- Understand repo conventions and patterns
- Examples: `mi-component-setup`, `validate-design-system`, `create-api-endpoint`

## Why Repo-Specific Skills?

**Team Collaboration:**
- Skills are committed to the repo
- Everyone on the team can use them
- Ensures consistency across the team

**Codebase Context:**
- Skills understand your APIs and patterns
- Know your testing frameworks
- Follow your conventions
- Reference actual code examples

**Examples for Movable Ink:**
- `mi-create-component` - Creates React components following MI design system
- `mi-api-endpoint` - Scaffolds API endpoints with proper structure
- `mi-migration-helper` - Helps with framework migrations
- `validate-pr-checklist` - Validates PR against MI checklist

## Creating Repo-Specific Skills

### Quick Scaffolding

```bash
# Navigate to your repo
cd ~/github/movable-ink/front-end

# Create a repo-specific skill
~/.claude/agents/skill-builder/scaffold.sh create-component --local --user-invocable

# Files created in:
# - .claude/skills/create-component.md
# - .claude/tests/integration/create_component/test_create_component.py
```

### Interactive with Skill Builder Agent

```bash
# From within your repo
cd ~/github/movable-ink/front-end

# Invoke the agent
claude-agent ~/.claude/agents/skill-builder/agent.md

# Tell the agent you want a repo-specific skill
# It will detect repo context automatically
```

The agent will:
1. Detect you're in a repo (vs global .claude directory)
2. Ask if this should be repo-specific
3. Gather repo context (package manager, framework, conventions)
4. Create skill with repo-specific knowledge
5. Add examples using actual repo patterns

## Directory Structure

### Movable Ink Front-End Example

```
front-end/
├── .claude/
│   ├── .gitignore          # Don't ignore skills/
│   ├── skills/             # Team-shared skills
│   │   ├── README.md
│   │   ├── create-component.md
│   │   ├── api-endpoint.md
│   │   └── validate-design-system.md
│   └── tests/
│       └── integration/    # Skill tests
│           ├── create_component/
│           └── api_endpoint/
├── src/
├── package.json
└── ...
```

### What Gets Committed

**DO commit:**
- `.claude/skills/` - Team-shared skills
- `.claude/tests/` - Skill tests
- `.claude/.gitignore` - To not ignore skills

**DON'T commit:**
- `.claude/projects/` - Personal session data
- `.claude/history.jsonl` - Personal conversation history
- `.claude/cache/` - Runtime cache

## Skill Examples

### Example 1: Create MI Component

```markdown
---
name: mi-create-component
description: Create a new React component following MI design system patterns
user_invocable: true
repository: front-end
---

# MI Create Component

Creates a new React component following Movable Ink's design system patterns
and folder structure.

## Instructions

1. **Get component details from user**
   - Component name (PascalCase)
   - Component type (functional/class)
   - Should it use design system components?

2. **Create component file structure**
   ```
   src/components/ComponentName/
   ├── index.tsx
   ├── ComponentName.tsx
   ├── ComponentName.test.tsx
   ├── ComponentName.styles.ts
   └── types.ts
   ```

3. **Generate component code**
   - Import from @movable-ink/design-system if needed
   - Follow MI TypeScript conventions
   - Add PropTypes documentation
   - Include basic tests

4. **Add to component index**
   - Export from src/components/index.ts

## Important Guidelines

- **Design System**: Use @movable-ink/design-system components
- **TypeScript**: All components must be typed
- **Testing**: Include at least basic render test
- **Styling**: Use styled-components via .styles.ts file

## Examples

<example>
User: "Create a UserCard component"
Assistant:
1. Creating src/components/UserCard/
2. Generating UserCard.tsx with proper imports
3. Adding UserCard.test.tsx with render test
4. Creating UserCard.styles.ts for styling
5. Exporting from src/components/index.ts
</example>
```

### Example 2: Validate API Endpoint

```markdown
---
name: mi-validate-api
description: Validate API endpoint follows MI backend conventions
user_invocable: true
repository: railsapp
---

# MI Validate API Endpoint

Validates that an API endpoint follows Movable Ink backend conventions.

## Instructions

1. **Check file location**
   - Controllers in app/controllers/api/v*/
   - Proper versioning (v1, v2, etc.)

2. **Validate structure**
   - Uses JSON API format
   - Includes proper error handling
   - Has rate limiting
   - Uses authorized! for auth checks

3. **Check tests**
   - Has request specs in spec/requests/
   - Tests success and error cases
   - Includes auth tests

4. **Report findings**
   - List any violations
   - Suggest fixes
   - Show examples of correct patterns

## Repository Context

- Framework: Ruby on Rails
- API Format: JSON API
- Auth: Doorkeeper OAuth2
- Testing: RSpec
```

## Using Repo-Specific Skills

### As Team Member

```bash
# Clone the repo
git clone git@github.com:movable-ink/front-end.git
cd front-end

# Skills are automatically available!
/mi-create-component UserProfile

# Or just reference them
"Create a component using our design system patterns"
```

### Creating for Your Team

```bash
# In your repo
cd ~/github/movable-ink/front-end

# Create skill
~/.claude/agents/skill-builder/scaffold.sh mi-create-component --local --user-invocable

# Edit the skill
# Add repo-specific patterns and examples

# Test it
cd .claude/tests
./run_tests.sh mi-create-component

# Commit and push
git add .claude/skills/mi-create-component.md
git add .claude/tests/integration/mi_create_component/
git commit -m "feat: add component creation skill"
git push
```

## Best Practices

### Skill Naming

**Global skills:**
- Generic names: `format-json`, `explain-code`

**Repo-specific skills:**
- Prefix with company/project: `mi-create-component`, `mi-validate-api`
- Clearly indicates it's repo-specific

### Skill Content

**Include:**
- Actual code examples from the repo
- Links to internal docs
- Team conventions and patterns
- Repo-specific APIs and tools

**Avoid:**
- Generic examples that could apply anywhere
- Outdated patterns no longer used
- Personal preferences not shared by team

### Testing

```bash
# Test repo-specific skills in repo context
cd ~/github/movable-ink/front-end/.claude/tests
./run_tests.sh mi-create-component

# Tests should verify:
# - Correct file structure for THIS repo
# - Uses THIS repo's conventions
# - Follows THIS repo's patterns
```

### Documentation

Add a `.claude/skills/README.md` in your repo:

```markdown
# Team Skills for Front-End

## Available Skills

- `/mi-create-component` - Create React component with design system
- `/mi-api-endpoint` - Scaffold API endpoint
- `/validate-design-system` - Check component compliance

## Creating New Skills

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines on creating
team skills.

## Testing

```bash
cd .claude/tests
./run_tests.sh
```
```

## Migration Path

### Convert Global Skill to Repo-Specific

If you have a global skill that should be repo-specific:

```bash
# Copy to repo
cp ~/.claude/skills/my-skill.md ~/github/movable-ink/front-end/.claude/skills/

# Add repo context
# Edit frontmatter to add: repository: front-end

# Add repo-specific examples
# Update with actual patterns from the repo

# Remove global version
trash ~/.claude/skills/my-skill.md

# Commit to repo
cd ~/github/movable-ink/front-end
git add .claude/skills/my-skill.md
git commit -m "feat: add my-skill as team skill"
```

## Repo Detection

The skill builder agent automatically detects:
- Repository name
- Package manager (npm, yarn, bundler)
- Framework (React, Rails, etc.)
- Testing framework
- Existing conventions

This context is used to:
- Suggest skill names
- Generate appropriate examples
- Include correct tool usage
- Follow repo patterns

## FAQ

**Q: Can a skill be both global and repo-specific?**
A: No, but you can create both versions. Global for general use, repo-specific with codebase details.

**Q: What if I don't want to share a skill with my team?**
A: Use global skills (`~/.claude/skills/`) - these are never committed.

**Q: Can I test repo skills without committing?**
A: Yes! Create in `.claude/skills/` but don't commit until tested and ready.

**Q: What about secrets in repo skills?**
A: Never include secrets. Use environment variables and document setup in README.

**Q: Can I use repo skills from another repo?**
A: Only if you copy them. Skills are repo-scoped by location.

## Examples by Repository Type

### React/TypeScript Repo (front-end)
- Component creation
- Hook scaffolding
- Storybook story generation
- Design system validation

### Rails API Repo (railsapp)
- Controller generation
- Migration creation
- RSpec test scaffolding
- API documentation

### Monorepo
- Cross-package refactoring
- Dependency management
- Package creation
- Workspace navigation

## See Also

- [Skill Builder Agent](README.md) - Create skills interactively
- [Testing Framework](../tests/README.md) - Test your skills
- [Global Skills](../../skills/README.md) - Personal skills
