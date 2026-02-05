# Skill Builder Agent

An interactive agent for creating new Claude Code skills and their tests.

## Purpose

This agent guides you through creating production-quality skills with:
- Proper skill structure and frontmatter
- Clear, actionable instructions for Claude
- Comprehensive test coverage
- Security validation
- Best practices baked in

## Usage

### Invoke the Agent

```bash
# From anywhere in your project
claude-agent agents/skill-builder/agent.md
```

Or use it within Claude Code:
```
I want to create a new skill that [describe what it should do]
```

### The agent will:
1. Ask discovery questions about your skill requirements
2. Generate a properly formatted skill file
3. Create comprehensive test files
4. Explain how to use and test your new skill

## Example Session

```
You: I want to create a skill that validates JSON files

Agent: Great! Let me ask a few questions to understand your requirements:

1. Should it just validate JSON syntax, or also validate against a schema?
2. What should happen when validation fails?
3. Should it suggest fixes for common issues?
4. Where should the JSON files be located?

[After your answers...]

Agent: I'll create the skill with these features:
- JSON syntax validation
- Schema validation (optional)
- Clear error messages
- Security checks for file paths

[Creates files and shows them to you...]

Agent: Your skill is ready! Here's how to use it:
```bash
/validate-json path/to/file.json
```

Test it with:
```bash
./agents/tests/run_tests.sh validate-json
```
```

## What Gets Created

### Skill File
Location: `~/.claude/skills/your-skill-name.md`

Contains:
- YAML frontmatter (name, description, user_invocable flag)
- Clear instructions for Claude
- Step-by-step workflow
- Security guidelines
- Tool usage notes
- Examples

### Test Files
Location: `~/.claude/agents/tests/integration/your_skill_name/`

Contains:
- `test_your_skill_name.py` - Main test file with:
  - Basic functionality tests
  - Security tests
  - Edge case tests
  - Validator usage
  - Mock and real SDK examples

## Templates

The agent uses these templates as starting points:

- `templates/skill-template.md` - Skill file structure
- `templates/test-template.py` - Test file structure

These ensure consistency across all generated skills.

## Best Practices

The agent enforces these best practices:

### Skill Design
- **Single responsibility** - Each skill does one thing well
- **Clear instructions** - Explicit steps for Claude to follow
- **Examples** - Concrete usage patterns
- **Security first** - Always validate user input
- **Error handling** - Guide behavior for edge cases

### Test Design
- **Fast mocks first** - Test logic without API calls
- **Critical paths real** - Use real SDK for important flows
- **Security always** - Every skill needs security tests
- **Clear assertions** - Make failures obvious
- **Good descriptions** - Explain what validates

### File Organization
- Skills: `~/.claude/skills/kebab-case-name.md`
- Tests: `~/.claude/agents/tests/integration/snake_case_name/`
- Follow Python naming conventions for test files

## Testing Your New Skill

After the agent creates your skill:

```bash
# Navigate to tests directory
cd ~/.claude/agents/tests

# Install dependencies (first time only)
pip install -r requirements-test.txt

# Run your skill's tests
./run_tests.sh your-skill-name

# Or with pytest directly
pytest integration/your_skill_name/ -v
```

## Customization

You can customize the templates in `templates/` to match your preferences:

1. Edit `templates/skill-template.md` for skill structure
2. Edit `templates/test-template.py` for test patterns
3. The agent will use your customized templates

## Tips

### For Simple Skills
Tell the agent: "Keep it simple, just [basic requirement]"

### For Complex Skills
Provide details: "I need multi-step workflow with [details]"

### For Security-Critical Skills
Mention: "This handles sensitive data, needs strong security"

### For User-Facing Skills
Specify: "This should be invocable as /command-name"

## Agent Capabilities

The skill builder agent can:
- ✅ Ask clarifying questions about requirements
- ✅ Generate skill files with proper structure
- ✅ Create comprehensive test files
- ✅ Include security tests automatically
- ✅ Follow naming conventions
- ✅ Update documentation
- ✅ Explain usage and testing
- ✅ Refine based on your feedback

## Integration with Testing Framework

This agent generates tests that use the testing framework from `agents/tests/`:

- Uses `AgentRunner` for skill execution
- Uses `MockLLMClient` for fast testing
- Uses validators for output checking
- Follows pytest conventions
- Includes markers (security, critical, etc.)

See `agents/tests/README.md` for testing framework details.

## Examples

### Creating a File Validation Skill
```
You: Create a skill that validates markdown files for broken links

Agent: [Asks about link types, external vs internal, etc.]
Agent: [Creates skill with validation logic]
Agent: [Creates tests for various link scenarios]
Agent: [Shows usage examples]
```

### Creating a Code Generator Skill
```
You: Create a skill that generates boilerplate test files

Agent: [Asks about test framework, language, etc.]
Agent: [Creates skill with generation logic]
Agent: [Creates tests verifying generated output]
Agent: [Shows how to use it]
```

### Creating an Analysis Skill
```
You: Create a skill that analyzes git commit history

Agent: [Asks about analysis type, output format, etc.]
Agent: [Creates skill with git commands]
Agent: [Creates tests with mocked git output]
Agent: [Shows usage examples]
```

## Troubleshooting

**Agent creates files in wrong location:**
- Tell agent: "Put skill in ~/.claude/skills/ and tests in ~/.claude/agents/tests/integration/"

**Tests don't work:**
- Check dependencies: `pip install -r agents/tests/requirements-test.txt`
- Verify pytest config: `cat agents/tests/pytest.ini`

**Skill doesn't match requirements:**
- Give agent feedback: "Actually, I need it to [different requirement]"
- Agent will refine the skill

## Contributing

To improve the skill builder agent:

1. Update `agent.md` with better instructions
2. Improve templates in `templates/`
3. Add more examples to this README
4. Share patterns that work well

## See Also

- [Testing Framework README](../tests/README.md) - Test infrastructure docs
- [Testing Quick Start](../tests/QUICK_START.md) - Get started with testing
- [Skills Directory](../../skills/) - Existing skills for reference
