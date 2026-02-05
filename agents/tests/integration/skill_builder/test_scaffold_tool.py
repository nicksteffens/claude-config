"""Tests for the skill-builder scaffold tool.

This demonstrates "dogfooding" - using our own testing framework
to test the skill-builder agent that creates skills and tests.
"""

import pytest
import subprocess
import tempfile
import shutil
from pathlib import Path


class TestScaffoldTool:
    """Test the scaffold.sh CLI tool."""

    @pytest.fixture
    def scaffold_script(self):
        """Path to scaffold.sh script."""
        return Path.home() / ".claude" / "agents" / "skill-builder" / "scaffold.sh"

    @pytest.fixture
    def temp_skills_dir(self, tmp_path):
        """Temporary skills directory for testing."""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()
        return skills_dir

    @pytest.fixture
    def temp_tests_dir(self, tmp_path):
        """Temporary tests directory for testing."""
        tests_dir = tmp_path / "tests" / "integration"
        tests_dir.mkdir(parents=True)
        return tests_dir

    def test_creates_skill_file(self, scaffold_script, tmp_path):
        """Test that scaffold creates a skill markdown file."""
        result = subprocess.run(
            [
                str(scaffold_script),
                "test-scaffold-skill",
                "--no-tests"
            ],
            env={
                "HOME": str(tmp_path),
                "PATH": subprocess.os.environ["PATH"]
            },
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        # Should succeed
        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Should create skill file
        skill_file = tmp_path / ".claude" / "skills" / "test-scaffold-skill.md"
        assert skill_file.exists(), f"Skill file not created at {skill_file}"

        # Should have valid content
        content = skill_file.read_text()
        assert "---" in content, "Missing YAML frontmatter"
        assert "name: test-scaffold-skill" in content
        assert "user_invocable: false" in content

    def test_creates_test_file(self, scaffold_script, tmp_path):
        """Test that scaffold creates test files."""
        result = subprocess.run(
            [
                str(scaffold_script),
                "test-scaffold-skill"
            ],
            env={
                "HOME": str(tmp_path),
                "PATH": subprocess.os.environ["PATH"]
            },
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Should create test directory
        test_dir = tmp_path / ".claude" / "agents" / "tests" / "integration" / "test_scaffold_skill"
        assert test_dir.exists(), f"Test dir not created at {test_dir}"

        # Should create test file
        test_file = test_dir / "test_test_scaffold_skill.py"
        assert test_file.exists(), f"Test file not created at {test_file}"

        # Should have valid test structure
        content = test_file.read_text()
        assert "import pytest" in content
        assert "from agents.tests.lib import AgentRunner" in content
        assert "class Test" in content

    def test_user_invocable_flag(self, scaffold_script, tmp_path):
        """Test --user-invocable flag sets correct frontmatter."""
        subprocess.run(
            [
                str(scaffold_script),
                "invocable-skill",
                "--user-invocable",
                "--no-tests"
            ],
            env={
                "HOME": str(tmp_path),
                "PATH": subprocess.os.environ["PATH"]
            },
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        skill_file = tmp_path / ".claude" / "skills" / "invocable-skill.md"
        content = skill_file.read_text()
        assert "user_invocable: true" in content

    def test_no_tests_flag(self, scaffold_script, tmp_path):
        """Test --no-tests flag skips test file creation."""
        subprocess.run(
            [
                str(scaffold_script),
                "no-test-skill",
                "--no-tests"
            ],
            env={
                "HOME": str(tmp_path),
                "PATH": subprocess.os.environ["PATH"]
            },
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        # Skill should exist
        skill_file = tmp_path / ".claude" / "skills" / "no-test-skill.md"
        assert skill_file.exists()

        # Tests should NOT exist
        test_dir = tmp_path / ".claude" / "agents" / "tests" / "integration" / "no_test_skill"
        assert not test_dir.exists()

    def test_rejects_invalid_skill_name(self, scaffold_script, tmp_path):
        """Test that invalid skill names are rejected."""
        # Test with uppercase (should fail - must be kebab-case)
        result = subprocess.run(
            [
                str(scaffold_script),
                "InvalidName",
                "--no-tests"
            ],
            env={
                "HOME": str(tmp_path),
                "PATH": subprocess.os.environ["PATH"]
            },
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        assert result.returncode != 0, "Should reject uppercase names"
        assert "kebab-case" in result.stderr.lower()

    def test_skill_already_exists(self, scaffold_script, tmp_path):
        """Test that creating duplicate skill fails."""
        # Create first skill
        subprocess.run(
            [
                str(scaffold_script),
                "duplicate-skill",
                "--no-tests"
            ],
            env={
                "HOME": str(tmp_path),
                "PATH": subprocess.os.environ["PATH"]
            },
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        # Try to create again - should fail
        result = subprocess.run(
            [
                str(scaffold_script),
                "duplicate-skill",
                "--no-tests"
            ],
            env={
                "HOME": str(tmp_path),
                "PATH": subprocess.os.environ["PATH"]
            },
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        assert result.returncode != 0, "Should reject duplicate skill"
        assert "already exists" in result.stderr.lower()


class TestScaffoldLocalMode:
    """Test scaffold tool with --local flag for repo-specific skills."""

    @pytest.fixture
    def temp_repo(self, tmp_path):
        """Create a temporary git repository."""
        repo = tmp_path / "test-repo"
        repo.mkdir()

        # Initialize git repo
        subprocess.run(["git", "init"], cwd=str(repo), capture_output=True)
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=str(repo),
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.email", "test@test.com"],
            cwd=str(repo),
            capture_output=True
        )

        return repo

    @pytest.fixture
    def scaffold_script(self):
        """Path to scaffold.sh script."""
        return Path.home() / ".claude" / "agents" / "skill-builder" / "scaffold.sh"

    def test_local_creates_in_repo_claude_dir(self, scaffold_script, temp_repo):
        """Test --local creates skills in repo's .claude/ directory."""
        result = subprocess.run(
            [
                str(scaffold_script),
                "repo-specific-skill",
                "--local",
                "--no-tests"
            ],
            cwd=str(temp_repo),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"

        # Should create in repo's .claude/skills/
        skill_file = temp_repo / ".claude" / "skills" / "repo-specific-skill.md"
        assert skill_file.exists(), f"Skill not created in repo at {skill_file}"

        # Should NOT create in global ~/.claude/skills/
        global_skill = Path.home() / ".claude" / "skills" / "repo-specific-skill.md"
        assert not global_skill.exists(), "Should not create in global skills dir"

    def test_local_creates_gitignore(self, scaffold_script, temp_repo):
        """Test --local creates .claude/.gitignore."""
        subprocess.run(
            [
                str(scaffold_script),
                "repo-skill",
                "--local",
                "--no-tests"
            ],
            cwd=str(temp_repo),
            capture_output=True,
            text=True
        )

        gitignore = temp_repo / ".claude" / ".gitignore"
        assert gitignore.exists(), "Should create .claude/.gitignore"

        content = gitignore.read_text()
        assert "projects/" in content, "Should ignore runtime files"
        assert "history.jsonl" in content
        assert "!skills/" in content or "skills" not in content, "Should allow skills/"

    def test_local_requires_git_repo(self, scaffold_script, tmp_path):
        """Test --local fails outside git repo."""
        non_repo = tmp_path / "not-a-repo"
        non_repo.mkdir()

        result = subprocess.run(
            [
                str(scaffold_script),
                "fail-skill",
                "--local",
                "--no-tests"
            ],
            cwd=str(non_repo),
            capture_output=True,
            text=True
        )

        assert result.returncode != 0, "Should fail outside git repo"
        assert "not in a git repository" in result.stderr.lower()


class TestScaffoldOutput:
    """Test scaffold tool output and naming conventions."""

    @pytest.fixture
    def scaffold_script(self):
        """Path to scaffold.sh script."""
        return Path.home() / ".claude" / "agents" / "skill-builder" / "scaffold.sh"

    def test_converts_kebab_to_snake_for_tests(self, scaffold_script, tmp_path):
        """Test that kebab-case skill names convert to snake_case for tests."""
        subprocess.run(
            [
                str(scaffold_script),
                "my-kebab-skill"
            ],
            env={
                "HOME": str(tmp_path),
                "PATH": subprocess.os.environ["PATH"]
            },
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        # Test directory should use snake_case
        test_dir = tmp_path / ".claude" / "agents" / "tests" / "integration" / "my_kebab_skill"
        assert test_dir.exists(), "Test dir should use snake_case"

        # Test file should also use snake_case
        test_file = test_dir / "test_my_kebab_skill.py"
        assert test_file.exists(), "Test file should use snake_case"

    def test_generates_proper_class_names(self, scaffold_script, tmp_path):
        """Test that test class names are properly formatted."""
        subprocess.run(
            [
                str(scaffold_script),
                "my-test-skill"
            ],
            env={
                "HOME": str(tmp_path),
                "PATH": subprocess.os.environ["PATH"]
            },
            capture_output=True,
            text=True,
            cwd=str(tmp_path)
        )

        test_file = tmp_path / ".claude" / "agents" / "tests" / "integration" / "my_test_skill" / "test_my_test_skill.py"
        content = test_file.read_text()

        # Should have valid Python class names (start with Test, no hyphens/spaces)
        assert "class Test" in content, "Should have test classes starting with Test"
        assert "class TestmytestskillSecurity:" in content or "class TestMyTestSkillSecurity:" in content
        # Verify no hyphens in class names
        assert "class Test-" not in content, "Class names should not contain hyphens"
