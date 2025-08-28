# Repository Assessment Slash Command

**Gist ID:** `e94be4a40a691ec79471e2a0bb243c37`  
**Gist URL:** https://gist.github.com/nicksteffens/e94be4a40a691ec79471e2a0bb243c37  
**Update Command:** `gh gist edit e94be4a40a691ec79471e2a0bb243c37`

You are starting work in a new repository. **ALWAYS** perform these checks in order before making any changes:

## 1. Package Manager Detection
- **Check `package.json` for volta configuration** - look for `volta.node`, `volta.yarn`, `volta.npm` fields
- **Rule**: If volta specifies yarn, use `yarn` commands. If no yarn specified, use `npm`
- Check for `packageManager` field as backup indicator
- **NEVER assume** - always verify before running package commands

## 2. Git Branch Safety Check
- **CRITICAL**: Check current branch with `git branch --show-current`
- **NEVER COMMIT TO MAIN/DEFAULT BRANCH** - This is an automatic session failure
- If on main/master/default branch or any shared branch, **ALWAYS ASK** user if they want to create a new feature branch
- **Branch naming convention**: `nicksteffens+claude/{sc-number || issues/number}/short-description`
  - Use `sc-{number}` for Shortcut stories (e.g. `nicksteffens+claude/sc-165234/fix-user-invitations`)
  - Use `issues/{number}` for GitHub issues (e.g. `nicksteffens+claude/issues/369/remove-empty-state-margins`)
- **Always offer to create branch** before making any code changes

## 3. Pre-commit and Git Hooks
- Check for `.husky/` directory and examine hook files
- Read `pre-commit` and `commit-msg` hook scripts to understand requirements
- **ALWAYS use conventional commit format** without being reminded
- Follow the exact format expected by the repository's commitlint configuration

## 4. Pull Request Templates
- Check for `.github/pull_request_template.md` or `PULL_REQUEST_TEMPLATE.md` in repo root
- Read template structure and follow all required sections
- Include summary, test plan, and any other sections specified

## 5. Testing Commands
- Look for test scripts in `package.json`
- Check for `README.md` testing instructions
- Identify lint, typecheck, build commands for later use

## 6. Existing Issues/PRs
- Search for existing issues or PRs related to your task
- Avoid duplicate work

**Output**: Provide a summary of findings from each check before proceeding with any work.
