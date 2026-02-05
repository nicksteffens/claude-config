"""Output validation utilities for agent tests."""

from pathlib import Path
from typing import List, Optional
import re


class FileStructureValidator:
    """Validates file paths and structure."""

    @staticmethod
    def is_valid_path(path: str, base_dir: Path = None) -> bool:
        """Check if path is valid and doesn't escape base directory.

        Args:
            path: Path to validate
            base_dir: Base directory path must be within

        Returns:
            True if path is valid and safe
        """
        try:
            p = Path(path).resolve()

            # Check for path traversal
            if ".." in path:
                return False

            # If base_dir provided, ensure path is within it
            if base_dir:
                base_resolved = base_dir.resolve()
                if not str(p).startswith(str(base_resolved)):
                    return False

            return True
        except Exception:
            return False

    @staticmethod
    def check_file_permissions(path: Path) -> bool:
        """Check if file has appropriate permissions.

        Args:
            path: File path to check

        Returns:
            True if permissions are appropriate
        """
        if not path.exists():
            return True  # New files are OK

        # Check file is readable and writable
        return path.is_file() and path.stat().st_mode & 0o600


class TemplateValidator:
    """Validates that output contains required template sections."""

    @staticmethod
    def has_required_sections(content: str, required_sections: List[str]) -> bool:
        """Check if content has all required sections.

        Args:
            content: Content to validate
            required_sections: List of required section headers

        Returns:
            True if all sections present
        """
        for section in required_sections:
            if section not in content:
                return False
        return True

    @staticmethod
    def has_complete_template(content: str) -> bool:
        """Check if content has a complete session log template.

        Args:
            content: Content to validate

        Returns:
            True if template is complete
        """
        required = [
            "Main Objectives",
            "What Went Well",
            "Challenges",
            "Key Decisions",
            "Follow-up Items"
        ]
        return TemplateValidator.has_required_sections(content, required)


class MarkdownValidator:
    """Validates markdown formatting."""

    @staticmethod
    def has_valid_headings(content: str) -> bool:
        """Check if markdown headings are properly formatted.

        Args:
            content: Markdown content

        Returns:
            True if headings are valid
        """
        # Check for malformed headings (missing space after #)
        malformed = re.findall(r'^#{1,6}[^\s#]', content, re.MULTILINE)
        return len(malformed) == 0

    @staticmethod
    def no_duplicate_date_headings(content: str, date_str: str) -> bool:
        """Check that date heading doesn't appear multiple times.

        Args:
            content: File content
            date_str: Date string to check (e.g., "2024-02-05")

        Returns:
            True if date appears only once or not at all
        """
        pattern = f"^## {re.escape(date_str)}"
        matches = re.findall(pattern, content, re.MULTILINE)
        return len(matches) <= 1

    @staticmethod
    def appends_to_end(original_content: str, new_content: str, insertion: str) -> bool:
        """Check that content was appended to end, not inserted in middle.

        Args:
            original_content: Original file content
            new_content: File content after modification
            insertion: The text that should have been appended

        Returns:
            True if insertion was at the end
        """
        if not new_content.endswith(insertion):
            return False

        # Check that everything before the insertion matches original
        expected_prefix = new_content[:-len(insertion)]
        return original_content.strip() == expected_prefix.strip()


class SecurityValidator:
    """Validates security aspects of agent output."""

    @staticmethod
    def no_path_traversal(path: str) -> bool:
        """Check for path traversal attempts.

        Args:
            path: Path to check

        Returns:
            True if no traversal detected
        """
        dangerous_patterns = [
            "..",
            "~",
            "/etc/",
            "/root/",
            "/var/",
        ]

        path_lower = path.lower()
        return not any(pattern in path_lower for pattern in dangerous_patterns)

    @staticmethod
    def no_command_injection(content: str) -> bool:
        """Check for potential command injection patterns.

        Args:
            content: Content to check

        Returns:
            True if no injection patterns found
        """
        dangerous_patterns = [
            r'\$\(',  # Command substitution
            r'`',     # Backtick execution
            r';\s*rm',  # Chained dangerous commands
            r'\|\s*sh',
            r'>\s*/dev/',
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, content):
                return False

        return True
