"""Agent runner that executes skills using Claude Agent SDK."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any
import asyncio

from .skill_loader import build_skill_prompt


@dataclass
class ToolCall:
    """Represents a tool invocation by the agent."""
    tool_name: str
    parameters: Dict[str, Any]
    result: Optional[str] = None


@dataclass
class AgentResult:
    """Result from executing an agent/skill."""
    output: str
    tool_calls: List[ToolCall]
    duration_ms: Optional[int] = None
    success: bool = True
    error: Optional[str] = None


class AgentRunner:
    """Executes Claude Code skills using the Claude Agent SDK.

    Can run with real Claude API or with mock LLM client for testing.
    """

    def __init__(
        self,
        skill_name: str,
        skills_dir: Optional[Path] = None,
        mock_client=None,
    ):
        """Initialize the agent runner.

        Args:
            skill_name: Name of the skill to run
            skills_dir: Directory containing skills (defaults to ~/.claude/skills)
            mock_client: Optional mock LLM client for testing
        """
        self.skill_name = skill_name
        self.skills_dir = skills_dir or Path.home() / ".claude" / "skills"
        self.mock_client = mock_client

    async def execute(self, user_request: str) -> AgentResult:
        """Execute the skill with a user request.

        Args:
            user_request: The user's input/request to the skill

        Returns:
            AgentResult containing output and metadata
        """
        try:
            # Build prompt from skill + user request
            prompt = build_skill_prompt(
                self.skill_name,
                user_request,
                self.skills_dir
            )

            # If using mock client, return mock response
            if self.mock_client:
                response = await self.mock_client.submit(prompt)
                return AgentResult(
                    output=response.content,
                    tool_calls=[],
                    success=True
                )

            # Otherwise use real Claude Agent SDK
            return await self._execute_with_sdk(prompt)

        except Exception as e:
            return AgentResult(
                output="",
                tool_calls=[],
                success=False,
                error=str(e)
            )

    async def _execute_with_sdk(self, prompt: str) -> AgentResult:
        """Execute using real Claude Agent SDK.

        Args:
            prompt: Complete prompt to send

        Returns:
            AgentResult with SDK execution results
        """
        try:
            # Import SDK here to avoid requiring it for mock tests
            from claude_agent_sdk import ClaudeAgentOptions, query

            options = ClaudeAgentOptions(
                allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
                cwd=str(Path.home() / ".claude"),
                model="haiku",  # Fast model for testing
                max_turns=10,
            )

            messages = []
            tool_calls = []

            async for message in query(prompt=prompt, options=options):
                messages.append(message)

                # Extract tool calls from message
                if hasattr(message, 'tool_uses'):
                    for tool_use in message.tool_uses:
                        tool_calls.append(ToolCall(
                            tool_name=tool_use.name,
                            parameters=tool_use.input,
                            result=getattr(tool_use, 'result', None)
                        ))

            # Extract final text output
            output = ""
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    for block in last_message.content:
                        if hasattr(block, 'text'):
                            output += block.text

            return AgentResult(
                output=output,
                tool_calls=tool_calls,
                duration_ms=getattr(messages[-1], 'duration_ms', None) if messages else None,
                success=True
            )

        except ImportError:
            return AgentResult(
                output="",
                tool_calls=[],
                success=False,
                error="claude-agent-sdk not installed. Run: pip install claude-agent-sdk"
            )
        except Exception as e:
            return AgentResult(
                output="",
                tool_calls=[],
                success=False,
                error=str(e)
            )
