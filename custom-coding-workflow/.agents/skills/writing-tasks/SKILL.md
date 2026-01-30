---
name: writing-tasks
description: Use after feature-planning to break Plan into 2-5 minute executable task units with dependency grouping
argument-hint: "features/[feature-name]_[date]"
---

# Writing Tasks

## Overview

Break down a feature Plan into 2-5 minute executable tasks. Groups dependent tasks together for sequential execution, leaves independent tasks ungrouped for parallel execution across worktrees.

**Announce at start:** "I'm using the writing-tasks skill to break down the Plan into executable tasks."

**Input:** Feature folder path with `prd.md`, `plan.md`, and `tests/`

**Output:** `tasks/` folder with task markdown files

## Workflow

### Step 1: Start

- If `$ARGUMENTS` provided → use as feature folder path
- If `$ARGUMENTS` empty → ask "Which feature folder should I create tasks for?"

### Step 2: Load Context

Read and understand:
- `prd.md` → requirements
- `plan.md` → architecture, feature list
- `tests/` → what tests need to pass

### Step 3: Task Decomposition & Grouping

Break Plan features into 2-5 minute tasks:

**Dependency analysis:**
- Tasks with sequential dependency → same group (`g1-`, `g2-`, ...)
- Independent tasks → no prefix

**Example:**
```
tasks/
  # Group 1: User model → API (must be sequential)
  g1-01_create-user-model.md
  g1-02_create-user-api.md
  g1-03_add-user-validation.md

  # Group 2: Auth flow (must be sequential)
  g2-01_create-auth-middleware.md
  g2-02_create-login-endpoint.md

  # Independent: can run in any worktree
  01_setup-logging.md
  02_add-config.md
  03_update-docker.md
```

### Step 4: Write Task Files

Each task file follows this template:

```markdown
# Task [prefix][number]: [Task Name]

**Feature:** [feature-name]
**Status:** ⬜ Todo | 🔄 In Progress | ✅ Done

## Goal
[One line: what changes when this task is complete]

## Files
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test_file.py`

## Step 1: Write failing test

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Run:** `pytest tests/path/test.py::test_name -v`
**Expected:** FAIL - "function not defined"

## Step 2: Minimal implementation

```python
def function(input):
    return expected
```

## Step 3: Verify test passes

**Run:** `pytest tests/path/test.py::test_name -v`
**Expected:** PASS

## Step 4: Commit

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

**Task file requirements:**
- Exact file paths always
- Complete code snippets (not "add validation")
- Exact commands with expected output
- TDD flow: test first → implement → verify → commit

### Step 5: Complete

Report created tasks grouped:

```
Tasks created!

features/[name]_[date]/tasks/

  Group 1 (sequential):
    g1-01_create-user-model.md
    g1-02_create-user-api.md

  Group 2 (sequential):
    g2-01_create-auth-middleware.md
    g2-02_create-login-endpoint.md

  Independent (parallel OK):
    01_setup-logging.md
    02_add-config.md

Parallel execution guide:
  - Group 1, Group 2: separate worktrees, run sequentially within group
  - Independent: any worktree

Next step: /setup-task-worktrees features/[name]_[date]
```

## Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Grouped task | `g[N]-[NN]_[slug].md` | `g1-01_create-user-model.md` |
| Independent task | `[NN]_[slug].md` | `01_setup-logging.md` |

## Key Principles

- **2-5 minutes per task** - If longer, split it
- **TDD in every task** - Test first, then implement
- **Independent by default** - Only group if truly dependent
- **Complete code** - No placeholders or "add X here"
- **Exact paths** - Never use relative or vague paths

## Integration

**Previous skill:** `/feature-planning` - creates PRD, Plan, Tests

**Next skill:** `/setup-task-worktrees` - creates worktrees for parallel execution

**Pairs with:**
- `/setup-task-worktrees` → `/executing-tasks`
