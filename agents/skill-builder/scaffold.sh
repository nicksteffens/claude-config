#!/bin/bash
# Quick scaffolding tool for creating skill files and tests
# This complements the skill-builder agent for rapid prototyping

set -e

SCRIPT_DIR="$(dirname "$0")"
GLOBAL_SKILLS_DIR="${HOME}/.claude/skills"
GLOBAL_TESTS_DIR="${HOME}/.claude/agents/tests/integration"
TEMPLATE_DIR="$SCRIPT_DIR/templates"

# Default to global skills
SKILLS_DIR="$GLOBAL_SKILLS_DIR"
TESTS_DIR="$GLOBAL_TESTS_DIR"
IS_LOCAL=false

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    cat << EOF
Usage: $0 <skill-name> [options]

Create a new Claude Code skill with tests.

Arguments:
    skill-name          Name of the skill (kebab-case, e.g., validate-json)

Options:
    --user-invocable    Make skill invocable as slash command (default: false)
    --local             Create in current repo's .claude/skills/ (repo-specific)
    --global            Create in ~/.claude/skills/ (all projects, default)
    --no-tests          Skip test file creation
    --help              Show this help message

Examples:
    # Create global skill (available everywhere)
    $0 my-new-skill

    # Create repo-specific skill (only for this codebase)
    $0 my-new-skill --local

    # Create user-invocable repo skill
    $0 my-new-skill --local --user-invocable

    # Create skill without tests
    $0 my-new-skill --no-tests

Notes:
    - Global skills: ~/.claude/skills/ (available in all projects)
    - Local skills: .claude/skills/ in current repo (repo-specific, team-shared)
    - For interactive creation with guidance, use the skill-builder agent instead

EOF
    exit 0
}

error() {
    echo -e "${YELLOW}Error: $1${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

info() {
    echo -e "${BLUE}→ $1${NC}"
}

# Parse arguments
SKILL_NAME=""
USER_INVOCABLE="false"
CREATE_TESTS="true"

while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            usage
            ;;
        --user-invocable)
            USER_INVOCABLE="true"
            shift
            ;;
        --local)
            IS_LOCAL=true
            shift
            ;;
        --global)
            IS_LOCAL=false
            shift
            ;;
        --no-tests)
            CREATE_TESTS="false"
            shift
            ;;
        -*)
            error "Unknown option: $1"
            ;;
        *)
            if [ -z "$SKILL_NAME" ]; then
                SKILL_NAME="$1"
            else
                error "Too many arguments. Skill name already set to: $SKILL_NAME"
            fi
            shift
            ;;
    esac
done

# Set up directories based on local vs global
if [ "$IS_LOCAL" = true ]; then
    # Check if we're in a git repo
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        error "Not in a git repository. Use --global to create a global skill."
    fi

    REPO_ROOT=$(git rev-parse --show-toplevel)
    REPO_NAME=$(basename "$REPO_ROOT")
    SKILLS_DIR="${REPO_ROOT}/.claude/skills"
    TESTS_DIR="${REPO_ROOT}/.claude/tests/integration"

    # Create .claude directory structure
    mkdir -p "$SKILLS_DIR"
    mkdir -p "$TESTS_DIR"

    # Create .gitignore for .claude if it doesn't exist
    if [ ! -f "${REPO_ROOT}/.claude/.gitignore" ]; then
        cat > "${REPO_ROOT}/.claude/.gitignore" << 'GITIGNORE'
# Claude runtime files (ignored)
projects/
todos/
history.jsonl
cache/
session-env/
telemetry/

# Skills and tests are team-shared (tracked by default)
# To ignore a specific skill, add it here:
#   skills/my-private-skill/
GITIGNORE
    fi

    # Source repo context if available
    if [ -f "$SCRIPT_DIR/repo-context.sh" ]; then
        source "$SCRIPT_DIR/repo-context.sh"
        REPO_INFO=$(get_repo_info "$REPO_ROOT")
    fi
fi

# Validate skill name
if [ -z "$SKILL_NAME" ]; then
    error "Skill name is required. Use --help for usage."
fi

# Validate skill name format (kebab-case)
if ! [[ "$SKILL_NAME" =~ ^[a-z][a-z0-9-]*$ ]]; then
    error "Skill name must be in kebab-case (lowercase, hyphens allowed): $SKILL_NAME"
fi

# Convert skill name to different formats
SKILL_NAME_SNAKE="${SKILL_NAME//-/_}"  # my-skill -> my_skill
SKILL_NAME_TITLE="$(echo "$SKILL_NAME" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')"  # my-skill -> My Skill
SKILL_CLASS_NAME="$(echo "$SKILL_NAME_TITLE" | sed 's/ //g')"  # My Skill -> MySkill

SKILL_DIR="${SKILLS_DIR}/${SKILL_NAME}"
SKILL_FILE="${SKILL_DIR}/SKILL.md"
TEST_DIR="${TESTS_DIR}/${SKILL_NAME_SNAKE}"
TEST_FILE="${TEST_DIR}/test_${SKILL_NAME_SNAKE}.py"

# Check if skill already exists
if [ -d "$SKILL_DIR" ]; then
    error "Skill already exists: $SKILL_DIR"
fi

info "Creating skill: $SKILL_NAME"
echo "  Skill dir: $SKILL_DIR"
echo "  Skill file: $SKILL_FILE"
if [ "$CREATE_TESTS" = "true" ]; then
    echo "  Test dir: $TEST_DIR"
    echo "  Test file: $TEST_FILE"
fi
echo

# Create skill directory and file
mkdir -p "$SKILL_DIR"

cat > "$SKILL_FILE" << EOF
---
name: ${SKILL_NAME}
description: [EDIT ME] Brief description of what this skill does
user_invocable: ${USER_INVOCABLE}
---

# ${SKILL_NAME_TITLE}

[EDIT ME] Overview of what this skill does and when to use it.

## Instructions

Follow these steps:

1. **[STEP 1 NAME]**
   - [Detail about what to do]
   - [Use appropriate tools]

2. **[STEP 2 NAME]**
   - [More details]
   - [Tool usage]

3. **[STEP 3 NAME]**
   - [Final actions]
   - [What to return]

## Important Guidelines

- **Security**: [Any security considerations - path validation, input sanitization, etc.]
- **File handling**: [How to handle files safely]
- **Error cases**: [How to handle errors gracefully]

## Tool Usage

[Document which tools this skill uses and why]
- Read: [When to use]
- Write: [When to use]
- Edit: [When to use]
- Bash: [When to use]

## Examples

<example>
User: "[Example user request]"
Assistant: [Shows expected behavior step by step]
</example>

## Notes

[Any additional notes, limitations, or future improvements]
EOF

success "Created skill file: $SKILL_FILE"

# Create test files if requested
if [ "$CREATE_TESTS" = "true" ]; then
    mkdir -p "$TEST_DIR"

    # Create __init__.py
    cat > "${TEST_DIR}/__init__.py" << EOF
"""Tests for ${SKILL_NAME} skill."""
EOF

    # Create test file
    cat > "$TEST_FILE" << EOF
"""Tests for ${SKILL_NAME} skill.

[EDIT ME] Describe what aspects of the skill these tests cover.
"""

import pytest
from pathlib import Path

from agents.tests.lib import AgentRunner, create_mock
from agents.tests.lib.validators import (
    TemplateValidator,
    SecurityValidator,
    MarkdownValidator,
)


class Test${SKILL_CLASS_NAME}:
    """Test ${SKILL_NAME} skill behavior."""

    @pytest.mark.asyncio
    async def test_basic_functionality(self):
        """[EDIT ME] Test basic skill behavior."""
        mock_response = """[EDIT ME] Expected response from skill"""

        runner = AgentRunner(
            skill_name="${SKILL_NAME}",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("[EDIT ME] User request")

        assert result.success
        # [EDIT ME] Add specific assertions
        assert "[expected text]" in result.output

    @pytest.mark.asyncio
    async def test_validates_output(self):
        """[EDIT ME] Test output validation."""
        mock_response = """[EDIT ME] Response to validate"""

        runner = AgentRunner(
            skill_name="${SKILL_NAME}",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("[EDIT ME] Request")

        assert result.success
        # [EDIT ME] Use validators as appropriate
        # Example: assert TemplateValidator.has_required_sections(result.output, ["Section1"])


class Test${SKILL_CLASS_NAME}Security:
    """Security tests for ${SKILL_NAME} skill."""

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_no_path_traversal(self):
        """Verify skill prevents path traversal attacks."""
        malicious_input = "../../../etc/passwd"

        # [EDIT ME] Adjust test based on how skill handles paths
        assert SecurityValidator.no_path_traversal(malicious_input)

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_input_validation(self):
        """Verify skill validates user input properly."""
        # [EDIT ME] Add tests for your skill's input validation
        pass


class Test${SKILL_CLASS_NAME}EdgeCases:
    """Edge case tests for ${SKILL_NAME} skill."""

    @pytest.mark.asyncio
    async def test_empty_input(self):
        """Test behavior with empty input."""
        # [EDIT ME] Test edge cases specific to your skill
        pass

    @pytest.mark.asyncio
    async def test_large_input(self):
        """Test behavior with large input."""
        # [EDIT ME] Test edge cases specific to your skill
        pass
EOF

    success "Created test directory: $TEST_DIR"
    success "Created test file: $TEST_FILE"
fi

echo
info "Next steps:"
echo "  1. Edit the skill file: ${SKILL_FILE}"
echo "  2. Fill in [EDIT ME] placeholders"
if [ "$CREATE_TESTS" = "true" ]; then
    echo "  3. Update test file: ${TEST_FILE}"
    echo "  4. Run tests: cd ~/.claude/agents/tests && ./run_tests.sh ${SKILL_NAME}"
fi
if [ "$USER_INVOCABLE" = "true" ]; then
    echo "  5. Use skill as: /${SKILL_NAME}"
else
    echo "  5. Skill is agent-only (not invocable as slash command)"
fi
echo
echo "For interactive creation with guidance, use the skill-builder agent:"
echo "  claude-agent ~/.claude/agents/skill-builder/agent.md"
echo
