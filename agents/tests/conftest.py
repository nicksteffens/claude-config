"""Pytest configuration and fixtures for agent tests."""

import pytest
from pathlib import Path
from datetime import date


@pytest.fixture
def skills_dir():
    """Get the skills directory path."""
    return Path.home() / ".claude" / "skills"


@pytest.fixture
def daily_log_dir():
    """Get the daily log directory path."""
    return Path.home() / ".claude" / "logs"


@pytest.fixture
def today_str():
    """Get today's date as YYYY-MM-DD string."""
    return date.today().strftime("%Y-%m-%d")


@pytest.fixture
def current_year():
    """Get current year as string."""
    return str(date.today().year)


@pytest.fixture
def current_month():
    """Get current month as MM string."""
    return f"{date.today().month:02d}"


@pytest.fixture
def expected_log_filename(current_year, current_month):
    """Get expected daily log filename."""
    return f"{current_year}-{current_month}-daily.md"


@pytest.fixture
def expected_log_path(daily_log_dir, current_year, expected_log_filename):
    """Get expected full path to current daily log file."""
    return daily_log_dir / current_year / expected_log_filename


@pytest.fixture
def sample_session_entry(today_str):
    """Get a sample session log entry."""
    return f"""
## {today_str}

**Session Duration:** 2 hours
**Success Rating:** 8/10

**Main Objectives:**
- Completed testing framework implementation
- Added pytest configuration

**What Went Well:**
- Tests are running successfully
- Good code organization

**Challenges:**
- Needed to figure out async testing with pytest
- SDK integration took some iteration

**Key Decisions:**
- Use pytest-asyncio for async tests
- Mock LLM client for fast tests
- Keep validators separate from test logic

**Follow-up Items:**
- Add more test cases
- Test with real Claude SDK
- Add CI integration
"""


@pytest.fixture
def mock_skill_content():
    """Get mock skill file content for testing."""
    return """---
name: test-skill
description: A test skill for testing
---

# Test Skill Instructions

This is a test skill that helps with testing.

Follow these steps:
1. Read the user's request
2. Generate appropriate output
3. Return the result
"""
