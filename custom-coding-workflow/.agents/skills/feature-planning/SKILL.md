---
name: feature-planning
description: Use when starting a new feature - transforms ideas into PRD, Plan, and test code through collaborative dialogue
argument-hint: "[feature description (optional)]"
---

# Feature Planning

## Overview

Transform user ideas into structured feature documentation through brainstorming-style dialogue. Creates PRD, implementation plan, and test code (TDD approach - tests first, failing state).

**Announce at start:** "I'm using the feature-planning skill to create PRD, Plan, and Tests."

**Output location:** `docs/features/[feature-name]_[YYYY-MM-DD]/`

## Workflow

### Step 1: Start

- If `$ARGUMENTS` provided → proceed to Step 2 with that context
- If `$ARGUMENTS` empty → ask "What feature would you like to build?"

### Step 2: Requirements Gathering (Brainstorming Style)

Explore the idea through dialogue:

- Ask **one question at a time**
- Prefer **multiple choice** when possible
- Cover: purpose, target users, core features, constraints, success criteria
- Propose **2-3 approaches** with trade-offs when relevant
- Lead with your recommendation and explain why

### Step 3: Create Folder & PRD

1. Create folder: `docs/features/[feature-name]_[YYYY-MM-DD]/`
2. Write `prd.md`:

```markdown
# [Feature Name] PRD

**Created:** YYYY-MM-DD
**Status:** Draft | Ready | In Progress | Done

## Purpose

[Why this feature is needed]

## Target Users

[Who will use this]

## Core Features

- [ ] Feature 1
- [ ] Feature 2

## Constraints

- [Technical/business constraints]

## Success Criteria

- [How to know it's complete]
```

3. **Request feedback:** "PRD looks good? Any changes needed?"
4. Apply feedback if any → repeat until approved

### Step 4: Write Plan

1. Write `plan.md`:

```markdown
# [Feature Name] Implementation Plan

**PRD:** ./prd.md
**Created:** YYYY-MM-DD
**Status:** Planning | Ready | In Progress | Done

## Architecture Overview

[2-3 sentences on overall approach]

## Tech Stack

- [Technologies/libraries to use]

## Feature List

- [ ] Feature 1: [brief description]
- [ ] Feature 2: [brief description]

## Reference

- [Related docs/code links]
```

2. **Request feedback:** "Plan looks good? Any changes needed?"
3. Apply feedback if any → repeat until approved

### Step 5: Write Test Code

1. Create `tests/` folder
2. Write integration tests based on PRD success criteria
3. Tests should be in **failing state** (implementation doesn't exist yet)
4. Cover end-to-end scenarios that verify the complete feature

```
tests/
  test_[feature]_integration.py   # or .ts, .js depending on project
  test_[feature]_e2e.py
```

### Step 6: Complete

Report created files:

```
Feature planning complete!

Created:
  features/[name]_[date]/
    ├── prd.md
    ├── plan.md
    └── tests/
          ├── test_xxx.py
          └── ...

Next step: /writing-tasks features/[name]_[date]
```

## Key Principles

- **One question at a time** - Don't overwhelm
- **Multiple choice preferred** - Easier to answer
- **Feedback after each document** - PRD and Plan must be approved
- **Tests first (TDD)** - Write failing tests before implementation
- **YAGNI** - Remove unnecessary features from designs

## Integration

**Next skill:** `/writing-tasks` - breaks Plan into 2-5 minute task units

**Pairs with:**

- `/writing-tasks` → `/setup-task-worktrees` → `/executing-tasks`
