"""Utilities for loading and parsing Claude Code skill files."""

import re
from pathlib import Path
from typing import Dict, Tuple
import yaml


def parse_skill_frontmatter(content: str) -> Tuple[Dict, str]:
    """Parse YAML frontmatter and content from skill markdown.

    Args:
        content: Raw skill file content

    Returns:
        Tuple of (frontmatter_dict, remaining_content)
    """
    # Match YAML frontmatter between --- delimiters
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return {}, content

    frontmatter_text = match.group(1)
    remaining_content = match.group(2)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        frontmatter = {}

    return frontmatter, remaining_content


def load_skill(skill_name: str, skills_dir: Path = None) -> Tuple[Dict, str]:
    """Load a skill file and parse its frontmatter and content.

    Args:
        skill_name: Name of the skill (without .md extension)
        skills_dir: Directory containing skills (defaults to ~/.claude/skills)

    Returns:
        Tuple of (frontmatter_dict, skill_content)

    Raises:
        FileNotFoundError: If skill file doesn't exist
    """
    if skills_dir is None:
        skills_dir = Path.home() / ".claude" / "skills"

    skill_path = skills_dir / f"{skill_name}.md"

    if not skill_path.exists():
        raise FileNotFoundError(f"Skill not found: {skill_path}")

    content = skill_path.read_text()
    return parse_skill_frontmatter(content)


def build_skill_prompt(skill_name: str, user_request: str, skills_dir: Path = None) -> str:
    """Build a complete prompt from skill content and user request.

    Args:
        skill_name: Name of the skill
        user_request: User's request to the skill
        skills_dir: Directory containing skills

    Returns:
        Complete prompt string combining skill instructions and user request
    """
    frontmatter, skill_content = load_skill(skill_name, skills_dir)

    prompt = f"{skill_content.strip()}\n\n"
    prompt += f"User request: {user_request}"

    return prompt
