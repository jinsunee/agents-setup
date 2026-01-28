# Common Agent Skills and Configuration

Shared agent skills, rules, and configurations for Claude Code and other AI coding assistants.

## Overview

This directory contains common skills, references, and configurations that can be used across multiple projects. Skills defined here are domain-agnostic and applicable to general software development workflows.

## Directory Structure

```
common/
├── .agents/          # Master skills directory (source of truth)
│   └── skills/       # Agent skill definitions
├── .agent/           # Symbolic links for Codex agent
│   └── skills/       # → points to .agents/skills/
└── .claude/          # Symbolic links for Claude Code
    └── skills/       # → points to .agents/skills/
```

## Available Skills

### Development Workflow
- **test-driven-development** - TDD methodology with RED-GREEN-REFACTOR cycle
- **tdd** - Compact TDD reference
- **verification-before-completion** - Quality gates before claiming work complete
- **verification-loop** - Comprehensive verification system for features and PRs

### Code Review & Quality
- **requesting-code-review** - How to request effective code reviews
- **receiving-code-review** - How to respond to code review feedback
- **systematic-debugging** - Structured approach to debugging issues

### Planning & Execution
- **brainstorming** - Exploring user intent and requirements before implementation
- **writing-plans** - Creating implementation plans for multi-step tasks
- **executing-plans** - Executing written implementation plans with checkpoints
- **finishing-a-development-branch** - Structured options for merge, PR, or cleanup

### Agent Management
- **dispatching-parallel-agents** - Running multiple independent tasks concurrently
- **subagent-driven-development** - Executing plans with subagents in current session
- **agent-browser** - Browser automation for testing and data extraction

### Testing & Evaluation
- **qa-test-planner** - Generate test plans and manual test cases
- **eval-harness** - Evaluation framework for testing agent behavior

### Documentation & Skills
- **writing-skills** - TDD approach to creating agent skills
- **find-skills** - Discovering and installing agent skills

### Performance & Best Practices
- **vercel-react-best-practices** - React/Next.js optimization from Vercel
- **strategic-compact** - Context management through manual compaction
- **continuous-learning** - Learning from past sessions and improving over time

## Usage

### For Claude Code

Skills in `.claude/skills/` are automatically discovered by Claude Code CLI. No additional configuration needed.

```bash
# Skills are invoked automatically based on context
# Or explicitly via slash commands if configured
```

### For Other Agents

1. Create symbolic links in your agent's skills directory:
```bash
ln -s /path/to/common/.agents/skills/skill-name ~/.your-agent/skills/
```

2. Or reference skills directly in your agent configuration.

## Skill Structure

Each skill follows this structure:

```
skill-name/
├── SKILL.md              # Main skill documentation (required)
└── supporting-files.*    # Optional supporting files
```

### SKILL.md Format

```markdown
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview
Core principle in 1-2 sentences.

## When to Use
Bullet list with symptoms and use cases

## Quick Reference
Tables or bullets for scanning

## Implementation
Code examples or links to supporting files

## Common Mistakes
What goes wrong + fixes
```

## Adding New Skills

Skills should be added to `.agents/skills/` (source of truth), then symlinked to `.agent/skills/` and `.claude/skills/`.

```bash
# 1. Create skill directory
mkdir -p .agents/skills/new-skill

# 2. Write SKILL.md with proper frontmatter
vim .agents/skills/new-skill/SKILL.md

# 3. Create symbolic links
ln -s ../../.agents/skills/new-skill .agent/skills/new-skill
ln -s ../../.agents/skills/new-skill .claude/skills/new-skill
```

**Important:** Follow TDD principles for skill creation. See `writing-skills` for methodology.

## Skill Categories

### Discipline Skills (Rules/Requirements)
Enforce specific workflows and quality standards.
- test-driven-development
- verification-before-completion
- verification-loop

### Technique Skills (How-To Guides)
Step-by-step methods for specific tasks.
- systematic-debugging
- agent-browser
- qa-test-planner

### Pattern Skills (Mental Models)
Ways of thinking about problems.
- brainstorming
- strategic-compact

### Reference Skills (Documentation)
API docs, syntax guides, tool documentation.
- vercel-react-best-practices

## Best Practices

1. **Single Source of Truth**: Always edit skills in `.agents/skills/`, never in symlinked directories
2. **Test Before Deploy**: Use writing-skills methodology (RED-GREEN-REFACTOR)
3. **Clear Descriptions**: Start with "Use when..." and include specific triggers
4. **Token Efficiency**: Keep frequently-loaded skills under 200 words
5. **Searchable Keywords**: Include error messages, symptoms, tool names

## Contributing

When adding skills that could benefit others:

1. Follow writing-skills methodology
2. Test with pressure scenarios
3. Ensure proper frontmatter formatting
4. Include Quick Reference section
5. Document Common Mistakes
6. Consider contributing back via PR

## Related Directories

- `../backend/` - Backend-specific skills and configurations
- `../frontend/` - Frontend-specific skills and configurations
- `../ui-ux-design/` - Design-specific skills and tools

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Agent Skills Best Practices](https://docs.anthropic.com/agent-skills)
- Writing Skills guide: `.agents/skills/writing-skills/SKILL.md`

## License

[Specify your license here]
