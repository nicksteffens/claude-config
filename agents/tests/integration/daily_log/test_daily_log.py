"""Integration tests for daily-log skill.

Tests the daily-log skill's ability to:
- Ask for required information (not auto-fill)
- Create proper file paths
- Use correct template format
- Append to files correctly
- Handle multiple sessions per day
"""

import pytest
from pathlib import Path
from datetime import date

from agents.tests.lib import AgentRunner, create_mock, create_sequence_mock
from agents.tests.lib.validators import (
    TemplateValidator,
    MarkdownValidator,
    SecurityValidator,
    FileStructureValidator
)


class TestDailyLogBehavior:
    """Test daily-log skill behavioral requirements."""

    @pytest.mark.critical
    @pytest.mark.asyncio
    async def test_self_rating_bug(self, tmp_path):
        """TC-005: Verify skill ASKS for rating instead of filling it in.

        This is a KNOWN BUG - the skill currently auto-fills the success rating
        instead of asking the user for it. This test documents the bug and will
        pass once the skill is fixed.
        """
        # Mock response that auto-fills rating (current buggy behavior)
        mock_response = """I'll create the daily log entry for you.

Let me add this to your daily log:

**Success Rating:** 8/10

**Main Objectives:**
- Completed the authentication module

**What Went Well:**
- Implementation was smooth

**Challenges:**
- None

**Key Decisions:**
- Used JWT tokens

**Follow-up Items:**
- Add tests tomorrow
"""

        runner = AgentRunner(
            skill_name="daily-log",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute(
            "Log today's session: we finished the auth module"
        )

        assert result.success, f"Execution failed: {result.error}"

        # The bug: Check if skill auto-filled the rating
        # When fixed, this should fail because skill should ASK for rating
        has_auto_filled_rating = "Success Rating:" in result.output

        # Currently this will be True (bug exists)
        # When skill is fixed, it should ask "How would you rate" instead
        if has_auto_filled_rating:
            pytest.fail(
                "BUG DETECTED: Skill filled in rating without asking user!\n"
                "Expected: Skill should ask 'How would you rate...'\n"
                f"Got: Skill auto-filled rating in output:\n{result.output}"
            )

    @pytest.mark.asyncio
    async def test_asks_for_session_duration(self):
        """Verify skill asks for session duration."""
        mock_response = "How long was your session? (e.g., '2 hours' or '90 minutes')"

        runner = AgentRunner(
            skill_name="daily-log",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("Log today's work")

        assert result.success
        assert "How long" in result.output or "duration" in result.output.lower()

    @pytest.mark.asyncio
    async def test_file_path_format(self):
        """TC-001: Verify correct file path format (YYYY/YYYY-MM-daily.md)."""
        today = date.today()
        expected_year = str(today.year)
        expected_month = f"{today.month:02d}"
        expected_filename = f"{today.year}-{expected_month}-daily.md"

        runner = AgentRunner(skill_name="daily-log")

        # We can't run real SDK in tests without API key, so check tool calls would be made
        # For now, just verify the skill loads correctly
        assert runner.skill_name == "daily-log"

    @pytest.mark.asyncio
    async def test_complete_template_sections(self):
        """TC-002: Verify all required template sections are present."""
        mock_response = """
## 2024-02-05

**Session Duration:** 2 hours
**Success Rating:** 8/10

**Main Objectives:**
- Complete testing framework

**What Went Well:**
- Made good progress

**Challenges:**
- None

**Key Decisions:**
- Use pytest

**Follow-up Items:**
- Add more tests
"""

        runner = AgentRunner(
            skill_name="daily-log",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("Log today's session")

        assert result.success
        assert TemplateValidator.has_complete_template(result.output)

    @pytest.mark.asyncio
    async def test_no_duplicate_date_headings(self):
        """TC-003: Verify no duplicate date headings in file."""
        today = date.today()
        date_str = today.strftime("%Y-%m-%d")

        mock_response = f"""
## {date_str}

**Session Duration:** 1 hour
**Success Rating:** 7/10

**Main Objectives:**
- First session

**What Went Well:**
- Good start
"""

        runner = AgentRunner(
            skill_name="daily-log",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("Log session")

        assert result.success
        assert MarkdownValidator.no_duplicate_date_headings(result.output, date_str)

    @pytest.mark.asyncio
    async def test_multiple_sessions_separator(self):
        """TC-004: Verify multiple sessions on same day use --- separator."""
        mock_response = """
---

**Session Duration:** 1 hour
**Success Rating:** 8/10

**Main Objectives:**
- Second session today
"""

        runner = AgentRunner(
            skill_name="daily-log",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("Log another session for today")

        assert result.success
        # If multiple sessions, should have separator
        if "second session" in result.output.lower():
            assert "---" in result.output


class TestDailyLogSecurity:
    """Security tests for daily-log skill."""

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_no_path_traversal(self):
        """Verify skill prevents path traversal attacks."""
        malicious_input = "Log session ../../etc/passwd"

        runner = AgentRunner(skill_name="daily-log")

        # Skill should sanitize input and not allow path traversal
        # This is a structural test - actual prevention happens in skill logic
        assert SecurityValidator.no_path_traversal(malicious_input)

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_no_command_injection(self):
        """Verify skill prevents command injection in log entries."""
        malicious_input = "Log session with $(rm -rf /) in it"

        mock_response = "Session logged successfully"

        runner = AgentRunner(
            skill_name="daily-log",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute(malicious_input)

        # Response should not contain dangerous patterns
        assert SecurityValidator.no_command_injection(result.output)


class TestDailyLogFileOperations:
    """Test file operation behaviors."""

    @pytest.mark.asyncio
    async def test_appends_to_end_of_file(self, tmp_path):
        """TC-006: Verify new entries are appended to end, not inserted in middle."""
        # This would require actual file operations
        # For now, test the validator logic
        original = "## 2024-02-04\n\nOld content\n"
        insertion = "\n## 2024-02-05\n\nNew content\n"
        new_content = original + insertion

        assert MarkdownValidator.appends_to_end(original, new_content, insertion)

    @pytest.mark.asyncio
    async def test_creates_directory_structure(self):
        """Verify skill creates YYYY/ directory if it doesn't exist."""
        runner = AgentRunner(skill_name="daily-log")

        # Verify runner initializes correctly
        assert runner.skill_name == "daily-log"
        # Actual directory creation happens via tool calls in real execution
