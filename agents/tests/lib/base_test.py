"""Base test class for skill testing."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict
from pathlib import Path

from .agent_runner import AgentRunner, AgentResult


@dataclass
class TestCase:
    """Represents a single test case."""
    name: str
    user_input: str
    expected_behavior: str
    mock_response: str = ""
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseSkillTest(ABC):
    """Abstract base class for skill tests."""

    @property
    @abstractmethod
    def skill_name(self) -> str:
        """Name of skill to test (e.g., 'daily-log')."""
        pass

    @abstractmethod
    def verify_output(self, output: str, test_case: TestCase) -> bool:
        """Skill-specific output validation.

        Args:
            output: The agent's output
            test_case: The test case being run

        Returns:
            True if output is valid, False otherwise
        """
        pass

    async def run_skill(
        self,
        user_input: str,
        mock_response: str = None,
        skills_dir: Path = None
    ) -> AgentResult:
        """Load skill, invoke with mock or real client, return output.

        Args:
            user_input: User request to the skill
            mock_response: Optional mock response (for testing)
            skills_dir: Optional skills directory

        Returns:
            AgentResult with execution results
        """
        from .mock_client import create_mock

        mock_client = create_mock(mock_response) if mock_response else None

        runner = AgentRunner(
            skill_name=self.skill_name,
            skills_dir=skills_dir,
            mock_client=mock_client
        )

        return await runner.execute(user_input)

    async def run_test_case(
        self,
        test_case: TestCase,
        skills_dir: Path = None
    ) -> tuple[bool, str]:
        """Run a single test case.

        Args:
            test_case: The test case to run
            skills_dir: Optional skills directory

        Returns:
            Tuple of (passed, message)
        """
        result = await self.run_skill(
            test_case.user_input,
            test_case.mock_response,
            skills_dir
        )

        if not result.success:
            return False, f"Execution failed: {result.error}"

        try:
            passed = self.verify_output(result.output, test_case)
            if passed:
                return True, f"Test '{test_case.name}' passed"
            else:
                return False, f"Test '{test_case.name}' failed validation"
        except AssertionError as e:
            return False, f"Test '{test_case.name}' failed: {str(e)}"
