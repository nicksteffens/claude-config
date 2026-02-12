"""Tests for shortcut-workspaces skill.

Tests verify the static reference data for Shortcut workspaces is loaded correctly.
"""

import pytest
from pathlib import Path

from agents.tests.lib.skill_loader import load_skill


class TestShortcutWorkspacesContent:
    """Test shortcut-workspaces skill content."""

    def test_skill_loads(self):
        """Verify skill file loads without errors."""
        frontmatter, content = load_skill("shortcut-workspaces")

        assert frontmatter["name"] == "shortcut-workspaces"
        assert "user_invocable" in frontmatter
        assert len(content) > 0

    def test_contains_workspace_references(self):
        """Verify skill contains both workspace references."""
        _, content = load_skill("shortcut-workspaces")

        # Should reference both workspaces in examples/docs
        assert "CoherentPath" in content or "coherentpath" in content
        assert "Movable Ink" in content or "movableink" in content

    def test_contains_mcp_tool_prefixes(self):
        """Verify MCP tool prefixes are documented."""
        _, content = load_skill("shortcut-workspaces")

        assert "mcp__shortcut__" in content
        assert "mcp__shortcut-mi__" in content

    def test_contains_team_data(self):
        """Verify skill documents how to access team data."""
        _, content = load_skill("shortcut-workspaces")

        # Should reference the data file and show structure
        assert "shortcut-workspaces-data.json" in content
        assert "teams" in content
        assert "uuid" in content or "UUID" in content
        assert "mention" in content

    def test_contains_user_info(self):
        """Verify skill documents how to access user information."""
        _, content = load_skill("shortcut-workspaces")

        # Should show how to get user data from JSON file
        assert "user" in content
        assert "jq" in content  # Shows how to query the data


class TestShortcutWorkspacesMetadata:
    """Test skill metadata and configuration."""

    def test_skill_metadata(self):
        """Verify skill has correct metadata."""
        frontmatter, _ = load_skill("shortcut-workspaces")

        assert frontmatter["user_invocable"] is True
        assert "description" in frontmatter
        assert len(frontmatter["description"]) > 0
