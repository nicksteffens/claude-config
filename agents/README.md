# Claude Code Agents

Specialized agents for building and testing Claude Code skills.

## Available Agents

### Skill Builder (`skill-builder/`)

An interactive agent that helps create new Claude Code skills with tests.

**Purpose**: Guide users through creating production-quality skills with proper structure, comprehensive tests, and security validation.

**Features**:
- Interactive discovery questions
- Generates skill files with proper YAML frontmatter
- Creates comprehensive test files using the testing framework
- Includes security tests automatically
- Follows best practices and conventions

**Usage**:
```bash
# Interactive mode (recommended)
claude-agent ~/.claude/agents/skill-builder/agent.md

# Quick scaffolding (manual editing required)
~/.claude/agents/skill-builder/scaffold.sh my-skill-name
```

**See**: [`skill-builder/README.md`](skill-builder/README.md) for complete documentation

## Testing Framework

Located in `tests/`, provides infrastructure for testing Claude Code agents and skills.

**Features**:
- MockLLMClient for fast testing without API calls
- AgentRunner for programmatic skill execution
- Validators for output checking
- Pytest integration with async support
- Comprehensive test markers and fixtures

**Usage**:
```bash
# Run all tests
./tests/run_tests.sh

# Run specific skill tests
./tests/run_tests.sh daily-log

# Run critical tests (known bugs)
./tests/run_tests.sh critical
```

**See**: [`tests/README.md`](tests/README.md) for complete documentation

## Workflow: Creating a New Skill

### Option 1: Interactive with Skill Builder Agent (Recommended)

```bash
# 1. Invoke the agent
claude-agent ~/.claude/agents/skill-builder/agent.md

# 2. Answer the agent's questions about your skill

# 3. Agent creates:
#    - ~/.claude/skills/your-skill.md
#    - ~/.claude/agents/tests/integration/your_skill/test_your_skill.py

# 4. Test your skill
cd ~/.claude/agents/tests
./run_tests.sh your-skill
```

### Option 2: Quick Scaffolding

```bash
# 1. Scaffold the skill
~/.claude/agents/skill-builder/scaffold.sh my-skill

# 2. Edit the generated files
#    - Fill in [EDIT ME] placeholders
#    - Update skill instructions
#    - Update test assertions

# 3. Test your skill
cd ~/.claude/agents/tests
./run_tests.sh my-skill
```

### Option 3: Manual Creation

1. Create skill file in `~/.claude/skills/my-skill.md`
2. Add YAML frontmatter and instructions
3. Create test file in `~/.claude/agents/tests/integration/my_skill/`
4. Use existing skills and tests as reference

## Directory Structure

```
agents/
├── README.md                    # This file
├── skill-builder/               # Agent for creating skills
│   ├── agent.md                # Agent instructions
│   ├── README.md               # Documentation
│   ├── scaffold.sh             # Quick scaffolding tool
│   └── templates/              # Skill and test templates
│       ├── skill-template.md
│       └── test-template.py
└── tests/                      # Testing framework
    ├── lib/                    # Core testing utilities
    ├── integration/            # Integration tests
    ├── conftest.py            # Pytest fixtures
    ├── pytest.ini             # Pytest config
    ├── run_tests.sh           # Test runner
    └── README.md              # Testing docs
```

## Best Practices

### Skill Design
- **Single responsibility**: Each skill does one thing well
- **Clear instructions**: Be explicit about what Claude should do
- **Examples**: Show concrete usage patterns
- **Security first**: Always validate user input
- **Error handling**: Guide behavior for edge cases

### Test Design
- **Fast mocks first**: Test logic without API calls
- **Critical paths real**: Use real SDK for important flows
- **Security always**: Every skill needs security tests
- **Clear assertions**: Make test failures obvious
- **Good descriptions**: Explain what each test validates

### File Organization
- Skills: `~/.claude/skills/kebab-case-name.md`
- Tests: `~/.claude/agents/tests/integration/snake_case_name/`
- Agents: `~/.claude/agents/agent-name/`

## Examples

### Creating a JSON Validator Skill

```bash
# Interactive
claude-agent ~/.claude/agents/skill-builder/agent.md
# Tell agent: "Create a skill that validates JSON files"

# Quick scaffold
~/.claude/agents/skill-builder/scaffold.sh validate-json --user-invocable
```

### Creating a Git Analysis Skill

```bash
# Interactive
claude-agent ~/.claude/agents/skill-builder/agent.md
# Tell agent: "Create a skill that analyzes git commit history"

# Quick scaffold
~/.claude/agents/skill-builder/scaffold.sh git-analyzer
```

## Testing Your Skills

All skills should have comprehensive tests:

```bash
# Navigate to tests directory
cd ~/.claude/agents/tests

# Install dependencies (first time)
pip install -r requirements-test.txt

# Run tests for your skill
./run_tests.sh your-skill-name

# Run with pytest directly
pytest integration/your_skill_name/ -v

# Run security tests
pytest -m security integration/your_skill_name/ -v
```

## Adding New Agents

To add a new agent to this directory:

1. Create a new directory: `agents/your-agent-name/`
2. Add agent instructions: `your-agent-name/agent.md`
3. Add README: `your-agent-name/README.md`
4. Add any helper scripts or templates
5. Update this README to document the new agent

## See Also

- [Testing Framework](tests/README.md) - Complete testing documentation
- [Testing Quick Start](tests/QUICK_START.md) - Get started quickly
- [Skill Builder](skill-builder/README.md) - Skill creation guide
- [Skills Directory](../skills/) - Existing skills for reference

## Contributing

To improve the agents:

1. Update agent instructions in `agent.md` files
2. Improve templates in `templates/` directories
3. Add more test coverage
4. Document patterns that work well
5. Share with the community
