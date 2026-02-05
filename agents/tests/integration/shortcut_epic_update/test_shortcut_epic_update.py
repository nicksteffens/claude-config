"""Tests for shortcut-epic-update skill.

Tests verify the skill documentation for updating epics via Shortcut API.
"""

import pytest
from pathlib import Path

from agents.tests.lib.skill_loader import load_skill


class TestShortcutEpicUpdateContent:
    """Test shortcut-epic-update skill content."""

    def test_skill_loads(self):
        """Verify skill file loads without errors."""
        frontmatter, content = load_skill("shortcut-epic-update")

        assert frontmatter["name"] == "shortcut-epic-update"
        assert "user_invocable" in frontmatter
        assert len(content) > 0

    def test_contains_api_token_instructions(self):
        """Verify skill documents token configuration."""
        _, content = load_skill("shortcut-epic-update")

        # Should reference the token config file
        assert "shortcut-tokens.json" in content
        assert "shortcut-tokens.sample.json" in content

    def test_contains_curl_examples(self):
        """Verify skill contains curl command examples."""
        _, content = load_skill("shortcut-epic-update")

        assert "curl -X PUT" in content
        assert "api.app.shortcut.com" in content
        assert "Shortcut-Token" in content

    def test_documents_common_operations(self):
        """Verify skill documents common update operations."""
        _, content = load_skill("shortcut-epic-update")

        # Should document common operations
        assert "Link to Objective" in content
        assert "Change State" in content
        assert "Update Owner" in content
        assert "objective_ids" in content

    def test_no_hardcoded_tokens(self):
        """Verify skill doesn't contain hardcoded API tokens."""
        _, content = load_skill("shortcut-epic-update")

        # Should NOT contain actual token values (starting with sct_ or UUID format)
        assert "sct_rw_coherentpath_" not in content
        # Sample/placeholder tokens in examples are OK
        assert "$TOKEN" in content or "your_" in content


class TestShortcutEpicUpdateMetadata:
    """Test skill metadata and configuration."""

    def test_skill_metadata(self):
        """Verify skill has correct metadata."""
        frontmatter, _ = load_skill("shortcut-epic-update")

        assert frontmatter["user_invocable"] is False
        assert "description" in frontmatter
        assert len(frontmatter["description"]) > 0

    def test_token_sample_file_exists(self):
        """Verify sample token file exists."""
        sample_file = Path.home() / ".claude" / "skills" / "shortcut-tokens.sample.json"
        assert sample_file.exists(), "shortcut-tokens.sample.json should exist as reference"
