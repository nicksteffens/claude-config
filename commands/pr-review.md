# PR Review Command

## Description
Comprehensive pull request review workflow with Shortcut integration and cross-repository support.

## Usage
```
/pr-review <PR_NUMBER> [--repo <REPO_PATH>] [--agent]
```

### Agent Mode (Recommended)
```
/pr-review <PR_NUMBER> --agent
```
Uses the `pr-reviewer` agent for autonomous execution of the entire review workflow with consistent quality standards and design system enforcement.

### Manual Mode
```
/pr-review <PR_NUMBER>
```
Step-by-step manual workflow for learning or debugging purposes.

## Steps

### 1. Initial PR Investigation
```bash
# View PR details and diff
gh pr view {{PR_NUMBER}} --json number,title,body,author,state,isDraft,files,additions,deletions
gh pr diff {{PR_NUMBER}}

# Check PR status and CI
gh pr checks {{PR_NUMBER}}
```

### 2. Shortcut Story Integration
- Extract Shortcut story ID from PR title/body (format: sc-XXXXX)
- Use Shortcut MCP to get story details:
  ```
  mcp__shortcut__get-story with storyPublicId: <STORY_ID>
  ```
- Review acceptance criteria and requirements
- Check for design team approvals or discussions

### 3. Code Review Analysis

#### Design System Compliance (Frontend)
- **CRITICAL**: Verify usage of @movable/ui components over MUI equivalents
- Common replacements to check:
  - `Dialog` → `InkDialog`
  - `Button` → `InkButton`
  - `TextField` → `InkTextField`
  - `Select` → `InkSelect`
  - `DataGrid` → `InkDataGrid`
  - `Alert` → Keep for inline alerts (InkSnackbarAlert is for notifications only)

#### Code Quality Checks
- Component patterns match existing codebase
- Proper TypeScript typing
- Test coverage for new functionality
- Error handling and edge cases
- Performance considerations (memoization, lazy loading)

#### Cross-Repository Dependencies
- If frontend PR, check for corresponding backend PR
- If backend PR, check for frontend consumer
- Verify API contracts match between repos

### 4. Testing Verification
```bash
# Check for test files in the changeset
gh pr view {{PR_NUMBER}} --json files --jq '.files[].path' | grep -E '\.(spec|test)\.(ts|tsx|js|jsx)$'

# Look for testing commands in PR description
gh pr view {{PR_NUMBER}} --json body --jq '.body' | grep -i -E 'test|cypress|jest'
```

### 5. Review Feedback

#### Using Conventional Comments
When providing feedback, use conventional comment syntax:
- `issue:` for blocking problems
- `suggestion:` for improvements
- `praise:` for good practices
- `question:` for clarifications

Example:
```
issue: This component should use InkDialog from @movable/ui instead of MUI Dialog

suggestion: Consider memoizing this expensive calculation with useMemo

praise: Excellent error handling with fallback UI!
```

### 6. Review Actions

#### For Approval
```bash
gh pr review {{PR_NUMBER}} --approve --body "LGTM! {{REVIEW_SUMMARY}}

Co-reviewed-by: Claude <noreply@anthropic.com>"
```

#### For Changes Requested
```bash
gh pr review {{PR_NUMBER}} --request-changes --body "{{REVIEW_SUMMARY}}

Please address the comments above before merging.

Co-reviewed-by: Claude <noreply@anthropic.com>"
```

#### For Comments Only
```bash
gh pr review {{PR_NUMBER}} --comment --body "{{REVIEW_SUMMARY}}

Co-reviewed-by: Claude <noreply@anthropic.com>"
```

### 7. Post-Review Actions
- If changes requested, add comment about specific components needing updates
- Link any relevant documentation or examples
- Offer to help with implementation if needed

## Example Usage

### Basic Review
```
/pr-review 9789
```

### Cross-Repository Review
```
/pr-review 9789 --repo ~/github/movable-ink/front-end
/pr-review 7606 --repo ~/github/movable-ink/railsapp
```

## Key Principles
1. **Always check Shortcut stories** for context and requirements
2. **Prioritize design system compliance** (@movable/ui over MUI)
3. **Consider cross-repository impacts** for API changes
4. **Provide actionable feedback** with specific examples
5. **Credit yourself** in review comments
6. **Be constructive** - praise good patterns while addressing issues

## Common Issues to Check
- [ ] Design system component usage
- [ ] Test coverage for new features
- [ ] Error handling and loading states
- [ ] Accessibility considerations
- [ ] Performance implications
- [ ] API contract compatibility
- [ ] Documentation updates
- [ ] TypeScript typing completeness