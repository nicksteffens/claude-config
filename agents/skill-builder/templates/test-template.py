"""Tests for {{SKILL_NAME}} skill.

{{TEST_FILE_DESCRIPTION}}
"""

import pytest
from pathlib import Path

from agents.tests.lib import AgentRunner, create_mock, create_sequence_mock
from agents.tests.lib.validators import (
    TemplateValidator,
    SecurityValidator,
    MarkdownValidator,
    FileStructureValidator
)


class Test{{SKILL_CLASS_NAME}}:
    """Test {{SKILL_NAME}} skill behavior."""

    @pytest.mark.asyncio
    async def test_basic_functionality(self):
        """{{TEST_BASIC_DESCRIPTION}}"""
        mock_response = """{{MOCK_RESPONSE_BASIC}}"""

        runner = AgentRunner(
            skill_name="{{SKILL_NAME}}",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("{{USER_REQUEST_BASIC}}")

        assert result.success
        # Add specific assertions based on expected behavior
        {{BASIC_ASSERTIONS}}

    @pytest.mark.asyncio
    async def test_{{TEST_CASE_2_NAME}}(self):
        """{{TEST_CASE_2_DESCRIPTION}}"""
        mock_response = """{{MOCK_RESPONSE_2}}"""

        runner = AgentRunner(
            skill_name="{{SKILL_NAME}}",
            mock_client=create_mock(mock_response)
        )

        result = await runner.execute("{{USER_REQUEST_2}}")

        assert result.success
        {{TEST_2_ASSERTIONS}}

    @pytest.mark.asyncio
    async def test_{{TEST_CASE_3_NAME}}(self):
        """{{TEST_CASE_3_DESCRIPTION}}"""
        {{TEST_CASE_3_BODY}}


class Test{{SKILL_CLASS_NAME}}Security:
    """Security tests for {{SKILL_NAME}} skill."""

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_no_path_traversal(self):
        """Verify skill prevents path traversal attacks."""
        malicious_input = "{{MALICIOUS_INPUT_EXAMPLE}}"

        runner = AgentRunner(skill_name="{{SKILL_NAME}}")

        # Verify security checks
        assert SecurityValidator.no_path_traversal(malicious_input)

    @pytest.mark.security
    @pytest.mark.asyncio
    async def test_input_validation(self):
        """Verify skill validates user input properly."""
        {{SECURITY_TEST_BODY}}


class Test{{SKILL_CLASS_NAME}}EdgeCases:
    """Edge case tests for {{SKILL_NAME}} skill."""

    @pytest.mark.asyncio
    async def test_{{EDGE_CASE_1_NAME}}(self):
        """{{EDGE_CASE_1_DESCRIPTION}}"""
        {{EDGE_CASE_1_BODY}}

    @pytest.mark.asyncio
    async def test_{{EDGE_CASE_2_NAME}}(self):
        """{{EDGE_CASE_2_DESCRIPTION}}"""
        {{EDGE_CASE_2_BODY}}
