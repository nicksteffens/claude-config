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

        # Should contain both workspace sections
        assert "CoherentPath Workspace (Primary)" in content
        assert "Movable Ink Workspace (Legacy)" in content

    def test_contains_mcp_tool_prefixes(self):
        """Verify MCP tool prefixes are documented."""
        _, content = load_skill("shortcut-workspaces")

        assert "mcp__shortcut__" in content
        assert "mcp__shortcut-mi__" in content

    def test_contains_team_data(self):
        """Verify skill contains team reference tables."""
        _, content = load_skill("shortcut-workspaces")

        # Should have team tables with UUIDs
        assert "Team Name" in content
        assert "UUID" in content
        assert "Mention Name" in content
        assert "Default Workflow ID" in content

    def test_contains_user_info(self):
        """Verify skill contains user information sections."""
        _, content = load_skill("shortcut-workspaces")

        # Should have Nick's info for both workspaces
        assert "Nick's Information" in content
        assert "@nicksteffens" in content


class TestShortcutWorkspacesMetadata:
    """Test skill metadata and configuration."""

    def test_skill_metadata(self):
        """Verify skill has correct metadata."""
        frontmatter, _ = load_skill("shortcut-workspaces")

        assert frontmatter["user_invocable"] is True
        assert "description" in frontmatter
        assert len(frontmatter["description"]) > 0
