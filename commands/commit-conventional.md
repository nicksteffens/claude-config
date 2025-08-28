# Conventional Commit Slash Command

Guide for creating proper conventional commits following repository standards.

## Conventional Commit Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
[optional co-authored-by]
```

## Common Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

## Examples
```bash
feat(auth): add user invitation validation
fix(ui): resolve accordion font size regression
docs: update README with new setup instructions
refactor(api): simplify user context logic
chore(deps): update @movable/ui to 3.1.2
```

## Co-Authors Process
1. **Ask user**: "Did anyone else help with this work besides you and me?"
2. **If yes**: Check recent commit history with `git log --pretty=format:"%s%n%b" -10` to find existing co-author patterns
3. **Match format** from previous commits for consistency
4. **Add co-authored-by trailer**:
   ```
   Co-authored-by: Name <email@example.com>
   Co-authored-by: Claude <noreply@anthropic.com>
   ```

## Process
1. **Identify the type** of change being made
2. **Add scope** if relevant (component, module, area)
3. **Write concise description** (imperative mood, no period)
4. **Ask about co-authors** and check existing patterns
5. **Reference tickets** in footer if applicable:
   - `Fixes #123` for GitHub issues
   - `Refs SC-12345` for Shortcut stories

## Template
```bash
git commit -m "<type>(<scope>): <description>

Refs <ticket-reference>

Co-authored-by: Name <email@example.com>
Co-authored-by: Claude <noreply@anthropic.com>"
```

**Always use imperative mood**: "add feature" not "added feature" or "adds feature"
