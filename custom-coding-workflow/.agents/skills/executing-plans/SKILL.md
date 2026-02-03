---
name: executing-plans
description: Use when you have a written implementation plan to execute - reads task groups, creates worktrees for parallel execution
argument-hint: "docs/features/[feature-name]_[YYYY-MM-DD]"
---

# Executing Plans

## Overview

Read plan and task files, create worktrees for parallel execution, guide user to run tasks.

**Core principle:** Parallel where possible, sequential within groups.

**Announce at start:** "I'm using the executing-plans skill to execute this plan."

**Input:** Feature folder path containing `plan.md` and `tasks/` folder

## Expected Input Structure

```
docs/features/[feature-name]_[YYYY-MM-DD]/
├── plan.md             # Overview + dependency graph
└── tasks/
    ├── group-a.md      # Sequential tasks
    ├── group-b.md      # Sequential tasks
    └── group-c.md      # Independent task
```

## The Process

### Step 1: Load Plan

1. Read `plan.md` from feature folder
2. Read all files in `tasks/` folder
3. Count groups and tasks per group

Report:
```
Loaded plan: [Feature Name]

Groups:
- group-a.md: 3 tasks (sequential)
- group-b.md: 2 tasks (sequential)
- group-c.md: 1 task

Total: 6 tasks in 3 groups
```

### Step 2: Create Worktrees

**Every group gets its own worktree** - keeps main branch clean and enables parallel work.

### Step 3: Setup Worktrees

**3-1. Ensure .worktrees is gitignored:**

```bash
if ! git check-ignore -q .worktrees 2>/dev/null; then
  echo ".worktrees/" >> .gitignore
  git add .gitignore
  git commit -m "chore: add .worktrees to gitignore"
fi
```

**3-2. Create worktree for each group:**

```bash
git worktree add ".worktrees/[feature]_group-a" -b "feature/[feature]_group-a"
git worktree add ".worktrees/[feature]_group-b" -b "feature/[feature]_group-b"
git worktree add ".worktrees/[feature]_group-c" -b "feature/[feature]_group-c"
```

**3-3. Guide user:**

```
Worktrees created!

┌─────────────────────────────────────────────────────────────────┐
│  Open terminals for each group:                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Terminal 1 (Group A - 3 tasks):                               │
│  $ cd .worktrees/[feature]_group-a && claude                   │
│  Then say: "Execute tasks/group-a.md"                          │
│                                                                 │
│  Terminal 2 (Group B - 2 tasks):                               │
│  $ cd .worktrees/[feature]_group-b && claude                   │
│  Then say: "Execute tasks/group-b.md"                          │
│                                                                 │
│  Terminal 3 (Group C - 1 task):                                │
│  $ cd .worktrees/[feature]_group-c && claude                   │
│  Then say: "Execute tasks/group-c.md"                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Run in parallel or one at a time - your choice.

When all groups complete, return here and say "All groups done"
to merge branches and cleanup.
```

→ Wait for user to report completion

### Step 4: Execute Tasks (In Each Worktree Session)

When executing inside a worktree:

**4-1. Read task file**

**4-2. For each task in order:**

1. Announce: "Starting Task N: [Name]"
2. **Red**: Write failing test, run to verify it fails
3. **Green**: Implement minimal code, run to verify it passes
4. **Commit**: Save progress
5. Announce: "Task N complete."

**4-3. Report every 3 tasks:**

```
Progress: Tasks 1-3 complete.

Commits:
- feat: add user model
- feat: add user validation
- feat: add user API

Continuing to Task 4...
```

**4-4. When all tasks done:**

```
Group complete! All tasks executed.

Summary:
- 5 tasks completed
- 5 commits made
- All tests passing

Return to main session and report "Group X done"
```

### Step 5: Merge Branches (After All Groups Complete)

When user reports all groups are done:

**5-1. Verify each branch:**

```bash
cd .worktrees/[feature]_group-a && npm test  # or project's test command
cd .worktrees/[feature]_group-b && npm test
cd .worktrees/[feature]_group-c && npm test
```

**5-2. Create merge branch and merge:**

```bash
git checkout main
git checkout -b feature/[feature-name]
git merge feature/[feature]_group-a
git merge feature/[feature]_group-b
git merge feature/[feature]_group-c
```

**5-3. Resolve conflicts if any**

**5-4. Run full test suite:**

```bash
npm test  # or project's test command
```

**5-5. Report:**

```
All branches merged successfully!

Merged:
- feature/[feature]_group-a (3 tasks)
- feature/[feature]_group-b (2 tasks)
- feature/[feature]_group-c (1 task)

All tests passing.

Next: /finishing-a-development-branch
```

### Step 6: Cleanup

After merge verified:

```bash
# Remove worktrees
git worktree remove .worktrees/[feature]_group-a
git worktree remove .worktrees/[feature]_group-b
git worktree remove .worktrees/[feature]_group-c

# Delete branches
git branch -d feature/[feature]_group-a
git branch -d feature/[feature]_group-b
git branch -d feature/[feature]_group-c
```

## Skills Used During Execution

- `/test-driven-development` - Always follow TDD (Red → Green → Commit)
- `/systematic-debugging` - When tests fail unexpectedly
- `/verification-before-completion` - Before claiming any task done

## When to Stop and Ask

**STOP immediately when:**
- Task instructions are unclear
- Test doesn't fail in Red phase
- Test doesn't pass after implementation
- Merge conflict you can't resolve

**Ask for help rather than guessing.**

## Red Flags

**Never:**
- Skip the Red phase
- Execute tasks out of order within a group
- Merge without all tests passing
- Delete worktrees before merge is verified
- Claim completion without running tests

## Integration

**Previous skill:** `/writing-plans` - creates plan.md and tasks/

**Used during:** `/test-driven-development`, `/systematic-debugging`

**Next skill:** `/finishing-a-development-branch` - merge/PR options
