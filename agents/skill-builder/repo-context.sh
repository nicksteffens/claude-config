#!/bin/bash
# Detect repository context for skill creation

set -e

get_repo_name() {
    local repo_dir="$1"
    cd "$repo_dir" 2>/dev/null || return 1

    if [ -d .git ]; then
        basename "$(git rev-parse --show-toplevel 2>/dev/null)" || echo "unknown"
    else
        echo "not-a-repo"
    fi
}

get_repo_info() {
    local repo_dir="${1:-$(pwd)}"

    if [ ! -d "$repo_dir/.git" ]; then
        echo "error: Not a git repository"
        return 1
    fi

    cd "$repo_dir"

    local repo_name=$(basename "$(git rev-parse --show-toplevel)")
    local repo_remote=$(git remote get-url origin 2>/dev/null || echo "no-remote")
    local package_manager="none"
    local has_tests="false"
    local framework="unknown"

    # Detect package manager
    if [ -f "package.json" ]; then
        if grep -q '"volta"' package.json; then
            if grep -q '"yarn"' package.json; then
                package_manager="yarn (via volta)"
            else
                package_manager="npm (via volta)"
            fi
        elif [ -f "yarn.lock" ]; then
            package_manager="yarn"
        else
            package_manager="npm"
        fi
    elif [ -f "Gemfile" ]; then
        package_manager="bundler"
    elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
        package_manager="pip/poetry"
    fi

    # Detect framework
    if [ -f "package.json" ]; then
        if grep -q '"react"' package.json; then
            framework="React"
        elif grep -q '"vue"' package.json; then
            framework="Vue"
        elif grep -q '"angular"' package.json; then
            framework="Angular"
        fi
    fi

    # Detect test setup
    if [ -d "tests" ] || [ -d "test" ] || [ -d "__tests__" ]; then
        has_tests="true"
    fi

    cat << EOF
{
  "repo_name": "$repo_name",
  "repo_remote": "$repo_remote",
  "package_manager": "$package_manager",
  "framework": "$framework",
  "has_tests": "$has_tests",
  "repo_path": "$(pwd)"
}
EOF
}

get_local_skills_dir() {
    local repo_dir="${1:-$(pwd)}"
    echo "${repo_dir}/.claude/skills"
}

create_local_skills_dir() {
    local repo_dir="${1:-$(pwd)}"
    local skills_dir=$(get_local_skills_dir "$repo_dir")

    mkdir -p "$skills_dir"

    # Create .gitignore if needed
    if [ ! -f "${repo_dir}/.claude/.gitignore" ]; then
        cat > "${repo_dir}/.claude/.gitignore" << 'GITIGNORE'
# Claude runtime files
projects/
todos/
history.jsonl
cache/
session-env/

# Skills are team-shared - don't ignore
!skills/
GITIGNORE
    fi

    # Create README
    if [ ! -f "$skills_dir/README.md" ]; then
        cat > "$skills_dir/README.md" << 'README'
# Repository-Specific Skills

Skills in this directory are specific to this repository and are shared across the team.

## Usage

These skills are automatically loaded when Claude Code is used in this repository.

## Creating Skills

```bash
# Create a new repo-specific skill
~/.claude/agents/skill-builder/scaffold.sh my-skill --local

# Or use the interactive agent
claude-agent ~/.claude/agents/skill-builder/agent.md
```

## Best Practices

- Make skills specific to this codebase's conventions
- Include examples using actual code from this repo
- Document any repo-specific APIs or patterns
- Test skills work with the repo's testing framework
README
    fi

    echo "$skills_dir"
}

# If run directly, show repo info
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    get_repo_info "$@"
fi
