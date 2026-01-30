---
name: setup-task-worktrees
description: Use after writing-tasks to create worktrees for parallel task execution based on task groups
argument-hint: "features/[feature-name]_[date]"
---

# Setup Task Worktrees

## Overview

Analyze tasks folder and create git worktrees for parallel execution. One worktree per task group, plus one for independent tasks.

**Announce at start:** "I'm using the setup-task-worktrees skill to create worktrees for parallel execution."

**Input:** Feature folder path with `tasks/` folder

**Output:** Multiple worktrees ready for parallel work

## Workflow

### Step 1: Start

- If `$ARGUMENTS` provided → use as feature folder path
- If `$ARGUMENTS` empty → ask "Which feature folder should I create worktrees for?"

### Step 2: Analyze Tasks Folder

Scan `tasks/` and identify groups:

```bash
ls features/[name]_[date]/tasks/
```

Parse filenames:
- `g1-*` → Group 1
- `g2-*` → Group 2
- No prefix → Independent

**Example analysis:**
```
Found:
  - Group 1: g1-01, g1-02, g1-03 (3 tasks)
  - Group 2: g2-01, g2-02 (2 tasks)
  - Independent: 01, 02, 03 (3 tasks)

Will create 3 worktrees.
```

### Step 3: Directory Selection

Follow priority order (same as using-git-worktrees):

1. Check existing: `.worktrees/` or `worktrees/`
2. Check CLAUDE.md for preference
3. Ask user if not found

### Step 4: Safety Verification

For project-local directories:

```bash
git check-ignore -q .worktrees 2>/dev/null
```

**If NOT ignored:**
1. Add to `.gitignore`
2. Commit the change
3. Proceed

### Step 5: Create Worktrees

For each group + independent:

```bash
# Get feature name from folder
feature_name="user-auth"  # extracted from features/user-auth_2025-01-30

# Create worktrees
git worktree add ".worktrees/${feature_name}_g1" -b "feature/${feature_name}_g1"
git worktree add ".worktrees/${feature_name}_g2" -b "feature/${feature_name}_g2"
git worktree add ".worktrees/${feature_name}_independent" -b "feature/${feature_name}_independent"
```

### Step 6: Project Setup (Each Worktree)

Auto-detect and run:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### Step 7: Verify Baseline

Run tests in each worktree to ensure clean state:

```bash
# Use project-appropriate command
npm test / pytest / cargo test / go test ./...
```

**If tests fail:** Report and ask whether to proceed.

### Step 8: Complete

Report all worktrees:

```
Worktrees created!

| Worktree | Path | Branch | Tasks |
|----------|------|--------|-------|
| g1 | .worktrees/user-auth_g1 | feature/user-auth_g1 | g1-01, g1-02, g1-03 |
| g2 | .worktrees/user-auth_g2 | feature/user-auth_g2 | g2-01, g2-02 |
| independent | .worktrees/user-auth_independent | feature/user-auth_independent | 01, 02, 03 |

Start working in each worktree:

  # Terminal 1 (Group 1)
  cd .worktrees/user-auth_g1 && claude

  # Terminal 2 (Group 2)
  cd .worktrees/user-auth_g2 && claude

  # Terminal 3 (Independent)
  cd .worktrees/user-auth_independent && claude

In each session, run: /executing-tasks features/user-auth_2025-01-30
```

## Worktree Naming Convention

| Type | Worktree Name | Branch Name |
|------|---------------|-------------|
| Group N | `[feature]_g[N]` | `feature/[feature]_g[N]` |
| Independent | `[feature]_independent` | `feature/[feature]_independent` |

## Key Principles

- **One worktree per group** - Parallel execution across groups
- **Sequential within group** - Tasks in same group run in order
- **Always verify .gitignore** - Never commit worktree contents
- **Clean baseline required** - Tests must pass before starting

## Integration

**Previous skill:** `/writing-tasks` - creates tasks with group prefixes

**Next skill:** `/executing-tasks` - runs in each worktree

**References:** `/using-git-worktrees` - core worktree logic
