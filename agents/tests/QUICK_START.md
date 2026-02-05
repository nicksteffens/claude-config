# Quick Start Guide

## Install and Run Tests

```bash
# Navigate to test directory
cd ~/.claude/agents/tests

# Install dependencies
pip install -r requirements-test.txt

# Run all tests (with mocks - no API key needed)
./run_tests.sh

# Run specific test suite
./run_tests.sh daily-log

# Run critical tests (known bugs)
./run_tests.sh critical
```

## Test the Self-Rating Bug

The daily-log skill has a known bug where it auto-fills the success rating instead of asking the user.

```bash
# This test will FAIL while the bug exists
pytest integration/daily_log/test_daily_log.py::TestDailyLogBehavior::test_self_rating_bug -v
```

Expected output:
```
FAILED - BUG DETECTED: Skill filled in rating without asking user!
Expected: Skill should ask 'How would you rate...'
Got: Skill auto-filled rating in output
```

## Write a Simple Test

Create `integration/my_skill/test_my_skill.py`:

```python
import pytest
from agents.tests.lib import AgentRunner, create_mock

class TestMySkill:
    @pytest.mark.asyncio
    async def test_basic_behavior(self):
        """Test my skill responds correctly."""
        mock_response = "Task completed successfully!"

        runner = AgentRunner(
            skill_name="my-skill",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("Do the thing")

        assert result.success
        assert "completed" in result.output
```

Run it:
```bash
pytest integration/my_skill/ -v
```

## Test with Real Claude SDK

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_with_real_sdk(self):
    """Test with actual Claude API."""
    # Don't pass mock_client to use real SDK
    runner = AgentRunner(skill_name="my-skill")

    result = await runner.execute("User request")

    assert result.success
```

Run with API key:
```bash
export ANTHROPIC_API_KEY=your_key
pytest integration/my_skill/ -v
```

## Validate Output

```python
from agents.tests.lib.validators import (
    TemplateValidator,
    SecurityValidator
)

# Check required sections
assert TemplateValidator.has_required_sections(
    result.output,
    ["Section 1", "Section 2"]
)

# Check security
assert SecurityValidator.no_path_traversal(user_input)
```

## Mock Strategies

### Fixed Response
```python
from agents.tests.lib import create_mock

mock = create_mock("Always this response")
```

### Sequential Responses
```python
from agents.tests.lib import create_sequence_mock

mock = create_sequence_mock([
    "First response",
    "Second response"
])
```

### Dynamic Responses
```python
from agents.tests.lib import create_callable_mock

def custom_response(prompt: str) -> str:
    if "help" in prompt:
        return "Here's help"
    return "Default response"

mock = create_callable_mock(custom_response)
```

## Next Steps

1. Read [`README.md`](./README.md) for complete documentation
2. See [`integration/daily_log/test_daily_log.py`](./integration/daily_log/test_daily_log.py) for examples
3. Add tests for your own skills
4. Run tests in CI/CD pipeline

## Troubleshooting

**Import errors:** Ensure you're in the tests directory and have dependencies installed.

**Async warnings:** Make sure `pytest-asyncio` is installed and `pytest.ini` has `asyncio_mode = auto`.

**SDK not found:** Mock tests work without SDK. For real tests, install `claude-agent-sdk`.
