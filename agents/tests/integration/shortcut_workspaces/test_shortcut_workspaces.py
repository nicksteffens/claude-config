"""Tests for shortcut-workspaces skill.

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


class Testshortcutworkspaces:
    """Test shortcut-workspaces skill behavior."""

    @pytest.mark.asyncio
    async def test_basic_functionality(self):
        """[EDIT ME] Test basic skill behavior."""
        mock_response = """[EDIT ME] Expected response from skill"""

        runner = AgentRunner(
            skill_name="shortcut-workspaces",
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
            skill_name="shortcut-workspaces",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("[EDIT ME] Request")

        assert result.success
        # [EDIT ME] Use validators as appropriate
        # Example: assert TemplateValidator.has_required_sections(result.output, ["Section1"])


class TestshortcutworkspacesSecurity:
    """Security tests for shortcut-workspaces skill."""

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


class TestshortcutworkspacesEdgeCases:
    """Edge case tests for shortcut-workspaces skill."""

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
