---
name: executing-tasks
description: Use in a worktree to execute tasks sequentially with TDD approach - tests first, then implementation
argument-hint: "features/[feature-name]_[date]"
---

# Executing Tasks

## Overview

Execute tasks in TDD style within a worktree. Automatically detects which task group to run based on current worktree name, then executes tasks sequentially with test-driven development flow.

**Announce at start:** "I'm using the executing-tasks skill to implement tasks with TDD approach."

**Input:** Feature folder path (or auto-detect from worktree name)

**Output:** Implemented code with passing tests

## Workflow

### Step 1: Detect Context

**Auto-detect from worktree:**
```bash
# Get current worktree name
basename $(pwd)  # e.g., "user-auth_g1"
```

Parse worktree name:
- `*_g1` → execute `g1-*` tasks
- `*_g2` → execute `g2-*` tasks
- `*_independent` → execute tasks without prefix

**Or use argument:** If `$ARGUMENTS` provided, use that feature folder path.

### Step 2: Load Tasks

```bash
# Example: in worktree user-auth_g1
ls features/user-auth_2025-01-30/tasks/g1-*.md
```

Sort by number and load in order:
- `g1-01_create-user-model.md`
- `g1-02_create-user-api.md`
- `g1-03_add-user-validation.md`

### Step 3: Check Test Status

Run integration tests to see current state:

```bash
pytest features/[name]_[date]/tests/ -v
```

Report: "Currently X/Y tests passing. Starting task execution."

### Step 4: Execute Tasks (TDD Style)

For each task in order:

**4.1 Mark as in progress**
- Update task file: `⬜ Todo` → `🔄 In Progress`

**4.2 Red: Write/run failing test**
- Follow task's Step 1
- Run test command from task file
- Verify it fails as expected

**4.3 Green: Implement**
- Follow task's Step 2
- Write minimal code to pass test

**4.4 Verify: Test passes**
- Follow task's Step 3
- Run test command
- Confirm it passes

**4.5 Commit**
- Follow task's Step 4
- Commit with message from task file

**4.6 Mark as complete**
- Update task file: `🔄 In Progress` → `✅ Done`

### Step 5: Batch Report

After every 3 tasks:

```
Progress Report:

Completed:
  ✅ g1-01_create-user-model
  ✅ g1-02_create-user-api
  ✅ g1-03_add-user-validation

Test status: 8/15 passing

Remaining: 2 tasks

Continue? (y/n)
```

Wait for user confirmation before proceeding.

### Step 6: Group Complete

When all tasks in group are done:

```
Group 1 Complete!

Completed tasks:
  ✅ g1-01_create-user-model
  ✅ g1-02_create-user-api
  ✅ g1-03_add-user-validation
  ✅ g1-04_add-user-tests
  ✅ g1-05_add-user-docs

Test status: 12/15 passing

Commits: 5 new commits on branch feature/user-auth_g1

Next steps:
  - Check other worktrees for remaining work
  - When all groups done, merge branches
```

## TDD Flow (Enforced)

Every task MUST follow this cycle:

```
┌─────────────────────────────────────┐
│  1. RED: Run test → must FAIL       │
├─────────────────────────────────────┤
│  2. GREEN: Implement → minimal code │
├─────────────────────────────────────┤
│  3. VERIFY: Run test → must PASS    │
├─────────────────────────────────────┤
│  4. COMMIT: Save progress           │
└─────────────────────────────────────┘
```

**Never skip the RED phase.** If test already passes, something is wrong.

## When to Stop

**Stop immediately when:**
- Test doesn't fail in RED phase (unexpected)
- Test doesn't pass after implementation
- Task instructions are unclear
- Missing dependency or file

**Ask for help rather than guessing.**

## Key Principles

- **TDD is mandatory** - Red → Green → Commit
- **One task at a time** - Complete fully before next
- **Verify at each step** - Don't assume, run tests
- **Batch reports** - Pause every 3 tasks for review
- **Stop when blocked** - Ask, don't guess

## Integration

**Previous skill:** `/setup-task-worktrees` - creates this worktree

**Pairs with:**
- Run in parallel across multiple worktrees
- Each worktree handles its own task group
