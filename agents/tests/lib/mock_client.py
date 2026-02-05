"""Mock LLM client for testing Claude agents without API calls."""

from typing import Callable, List, Optional, Union
from dataclasses import dataclass


@dataclass
class MockResponse:
    """Response from mock LLM client."""
    content: str
    model: str = "mock-model"
    stop_reason: str = "end_turn"


class MockLLMClient:
    """Mock LLM client that returns predefined responses.

    Matches the async interface expected by Claude Agent SDK.
    """

    def __init__(
        self,
        responses: Optional[Union[str, List[str], Callable[[str], str]]] = None
    ):
        """Initialize mock client with response strategy.

        Args:
            responses: Single response, list of responses, or callable that
                      generates responses based on input prompt
        """
        if responses is None:
            self.responses = []
        elif isinstance(responses, str):
            self.responses = [responses]
        elif callable(responses):
            self.response_fn = responses
            self.responses = None
        else:
            self.responses = list(responses)

        self.call_count = 0
        self.prompts_received = []

    async def submit(self, prompt: str) -> MockResponse:
        """Submit a prompt and get mock response.

        Args:
            prompt: The input prompt

        Returns:
            MockResponse with predefined content
        """
        self.prompts_received.append(prompt)
        self.call_count += 1

        # Use callable response function if provided
        if hasattr(self, 'response_fn'):
            content = self.response_fn(prompt)
        # Use sequential responses
        elif self.responses:
            idx = min(self.call_count - 1, len(self.responses) - 1)
            content = self.responses[idx]
        else:
            content = "Mock response"

        return MockResponse(content=content)

    def reset(self):
        """Reset call tracking."""
        self.call_count = 0
        self.prompts_received = []


def create_mock(response: str) -> MockLLMClient:
    """Create a mock client that always returns the same response.

    Args:
        response: The fixed response to return

    Returns:
        Configured MockLLMClient
    """
    return MockLLMClient(responses=response)


def create_sequence_mock(responses: List[str]) -> MockLLMClient:
    """Create a mock client that returns responses in sequence.

    Args:
        responses: List of responses to return in order

    Returns:
        Configured MockLLMClient
    """
    return MockLLMClient(responses=responses)


def create_callable_mock(fn: Callable[[str], str]) -> MockLLMClient:
    """Create a mock client that generates responses dynamically.

    Args:
        fn: Function that takes prompt and returns response

    Returns:
        Configured MockLLMClient
    """
    return MockLLMClient(responses=fn)
