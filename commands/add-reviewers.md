# Add Standard Reviewers Command

Adds JessWallin and Sh1pley as reviewers to the current PR.

## Steps

1. Get the current branch name
2. Find the PR number for the current branch
3. Add JessWallin and Sh1pley as reviewers

## Command Execution

```bash
# Get current branch
BRANCH=$(git branch --show-current)

# Find PR number for current branch
PR_NUMBER=$(gh pr list --head "$BRANCH" --json number --jq '.[0].number')

if [ -z "$PR_NUMBER" ]; then
  echo "❌ No PR found for current branch: $BRANCH"
  echo "Create a PR first with: gh pr create"
  exit 1
fi

echo "📝 Adding reviewers to PR #$PR_NUMBER..."

# Add reviewers
gh pr edit "$PR_NUMBER" --add-reviewer JessWallin,Sh1pley

if [ $? -eq 0 ]; then
  echo "✅ Successfully added JessWallin and Sh1pley as reviewers to PR #$PR_NUMBER"
  echo "🔗 PR URL: https://github.com/movableink/front-end/pull/$PR_NUMBER"
else
  echo "❌ Failed to add reviewers"
fi
```

## Usage

Simply run `/add-reviewers` after creating a PR to automatically add the standard reviewers.

## Notes

- This command assumes you have an open PR for the current branch
- If Copilot needs to be added, it must be done manually through the GitHub UI
- The reviewers will receive a notification to review the PR