# Claude Code Agent Testing Framework

A comprehensive testing framework for Claude Code agents and skills using the Claude Agent SDK.

## Overview

This framework enables **real agent testing** - not just validating files after manual execution, but actually invoking agents programmatically and validating their behavior. Tests can run with:

- **Mock LLM Client**: Fast, deterministic tests without API calls
- **Real Claude SDK**: End-to-end validation with actual Claude API

## Architecture

```
agents/tests/
├── lib/                          # Shared testing utilities
│   ├── mock_client.py           # Mock LLM client for testing
│   ├── skill_loader.py          # Load and parse skill files
│   ├── agent_runner.py          # Execute skills via SDK
│   ├── base_test.py             # Abstract base test class
│   └── validators.py            # Output validation utilities
├── integration/                  # Integration tests
│   └── daily_log/               # Daily-log skill tests
│       └── test_daily_log.py
├── conftest.py                  # Pytest fixtures
├── pytest.ini                   # Pytest configuration
├── requirements-test.txt        # Test dependencies
└── run_tests.sh                 # Test execution script
```

## Quick Start

### Run Tests

```bash
# Run all tests
./agents/tests/run_tests.sh

# Run only daily-log tests
./agents/tests/run_tests.sh daily-log

# Run critical tests (known bugs)
./agents/tests/run_tests.sh critical

# Run security tests
./agents/tests/run_tests.sh security

# Run with coverage report
./agents/tests/run_tests.sh coverage
```

### Manual Pytest Execution

```bash
cd agents/tests

# Install dependencies
pip install -r requirements-test.txt

# Run all tests
pytest integration/ -v

# Run specific test
pytest integration/daily_log/test_daily_log.py::TestDailyLogBehavior::test_self_rating_bug -v

# Run by marker
pytest -m critical -v
pytest -m security -v
```

## Test Markers

Tests can be marked with the following markers:

- `@pytest.mark.critical` - Critical tests for known bugs
- `@pytest.mark.security` - Security vulnerability tests
- `@pytest.mark.integration` - Integration tests using SDK
- `@pytest.mark.unit` - Unit tests with mocks only

## Writing Tests for a New Skill

### 1. Create Test File

```python
# agents/tests/integration/my_skill/test_my_skill.py

import pytest
from agents.tests.lib import AgentRunner, create_mock
from agents.tests.lib.validators import TemplateValidator

class TestMySkill:
    """Tests for my-skill."""

    @pytest.mark.asyncio
    async def test_basic_behavior(self):
        """Test basic skill behavior."""
        mock_response = "Expected output from skill"

        runner = AgentRunner(
            skill_name="my-skill",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("User request")

        assert result.success
        assert "expected text" in result.output
```

### 2. Use Validators

```python
from agents.tests.lib.validators import (
    TemplateValidator,
    MarkdownValidator,
    SecurityValidator,
    FileStructureValidator
)

# Check template sections
assert TemplateValidator.has_required_sections(
    result.output,
    ["Section 1", "Section 2"]
)

# Check markdown formatting
assert MarkdownValidator.has_valid_headings(result.output)

# Check security
assert SecurityValidator.no_path_traversal(user_input)
assert SecurityValidator.no_command_injection(result.output)
```

### 3. Test with Real SDK

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_with_real_sdk(self):
    """Test with actual Claude API (requires ANTHROPIC_API_KEY)."""
    # Don't pass mock_client to use real SDK
    runner = AgentRunner(skill_name="my-skill")

    result = await runner.execute("User request")

    assert result.success
    # Validate real output
```

## Testing the Self-Rating Bug

The daily-log skill has a known bug where it auto-fills the success rating instead of asking the user. Test `test_self_rating_bug` documents and detects this:

```bash
# This test will FAIL while bug exists
pytest integration/daily_log/test_daily_log.py::TestDailyLogBehavior::test_self_rating_bug -v
```

Expected failure output:
```
FAILED - BUG DETECTED: Skill filled in rating without asking user!
Expected: Skill should ask 'How would you rate...'
Got: Skill auto-filled rating in output
```

When the skill is fixed to ask for rating, this test will pass.

## Mock Strategies

### Fixed Response

```python
from agents.tests.lib import create_mock

mock_client = create_mock("Fixed response")
```

### Sequential Responses

```python
from agents.tests.lib import create_sequence_mock

mock_client = create_sequence_mock([
    "First response",
    "Second response",
    "Third response"
])
```

### Dynamic Responses

```python
from agents.tests.lib import create_callable_mock

def response_fn(prompt: str) -> str:
    if "question" in prompt:
        return "Answer"
    return "Default response"

mock_client = create_callable_mock(response_fn)
```

## Project Structure

### Core Components

**MockLLMClient** (`lib/mock_client.py`)
- Simulates LLM responses without API calls
- Tracks prompts received for verification
- Supports fixed, sequential, and dynamic responses

**SkillLoader** (`lib/skill_loader.py`)
- Loads skill markdown files from `~/.claude/skills/`
- Parses YAML frontmatter
- Builds complete prompts

**AgentRunner** (`lib/agent_runner.py`)
- Executes skills via Claude Agent SDK
- Supports both mock and real LLM clients
- Captures tool calls and output

**Validators** (`lib/validators.py`)
- `FileStructureValidator` - Path validation, permissions
- `TemplateValidator` - Required sections, completeness
- `MarkdownValidator` - Heading format, duplicates, append behavior
- `SecurityValidator` - Path traversal, command injection

### Test Organization

**Integration Tests** (`integration/`)
- Test actual skill behavior
- Can use mocks or real SDK
- Validate complete workflows

**Fixtures** (`conftest.py`)
- Common test data
- Path helpers
- Date/time utilities
- Sample content

## CI Integration

### GitHub Actions Example

```yaml
name: Agent Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd agents/tests
          pip install -r requirements-test.txt
      - name: Run tests
        run: |
          cd agents/tests
          pytest integration/ -v
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Best Practices

### 1. Test with Mocks First
- Fast, deterministic
- No API costs
- Easy to reproduce

### 2. Critical Paths with Real SDK
- Validates actual behavior
- Catches API changes
- End-to-end confidence

### 3. Use Markers
- Organize tests by type
- Run subsets efficiently
- Clear test intent

### 4. Document Known Bugs
- Tests as bug reports
- Track expected failures
- Verify fixes

### 5. Validate Security
- Path traversal
- Command injection
- File permissions
- Input sanitization

## Troubleshooting

### Import Errors

If you see import errors like `ModuleNotFoundError: No module named 'agents'`:

```bash
# Ensure you're in the tests directory
cd agents/tests

# Check pytest.ini has pythonpath set
cat pytest.ini | grep pythonpath
```

### Async Test Warnings

If async tests don't run, ensure `pytest-asyncio` is installed:

```bash
pip install pytest-asyncio>=0.23.0
```

And `pytest.ini` has:
```ini
[pytest]
asyncio_mode = auto
```

### SDK Not Found

Mock tests work without SDK. For real SDK tests:

```bash
pip install claude-agent-sdk
export ANTHROPIC_API_KEY=your_key
```

## Examples

See `integration/daily_log/test_daily_log.py` for comprehensive examples of:
- Testing known bugs (self-rating bug)
- Template validation
- File path verification
- Security testing
- Multiple session handling

## Contributing

When adding tests for a new skill:

1. Create `integration/skill_name/` directory
2. Add `test_skill_name.py` with test classes
3. Use appropriate markers (`@pytest.mark.critical`, etc.)
4. Document known bugs with clear failure messages
5. Add validators for skill-specific requirements

## Future Enhancements

- [ ] Add support for multi-turn agent interactions
- [ ] Add performance benchmarks
- [ ] Add visual diff for file changes
- [ ] Add test generation from skill documentation
- [ ] Add integration with LLM evaluation frameworks
