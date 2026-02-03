---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
argument-hint: "docs/features/[feature-name]_[YYYY-MM-DD]"
---

# Writing Plans

## Overview

Write comprehensive implementation plans with task files grouped by dependency. Each task is bite-sized (2-5 min) with complete TDD steps.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** Run after `/feature-planning` completes (PRD + technical-spec exist).

## Output Structure

```
docs/features/[feature-name]_[YYYY-MM-DD]/
├── prd.md              # (already exists)
├── technical-spec.md   # (already exists)
├── plan.md             # Overview + dependency graph
└── tasks/
    ├── group-a.md      # Sequential tasks (e.g., Task 1 → 2 → 3)
    ├── group-b.md      # Sequential tasks (e.g., Task 4 → 5)
    └── group-c.md      # Independent task (e.g., Task 6)
```

## The Process

### Step 1: Read Technical Spec

1. Read `technical-spec.md` from feature folder
2. Identify all required components/changes
3. Break down into 2-5 minute tasks

### Step 2: Identify Dependencies

For each task, determine:
- What must be done before this task?
- What files does this task create/modify?
- Does another task depend on this task's output?

### Step 3: Group Tasks

**Grouping rules:**
- Tasks with sequential dependencies → same group
- Independent tasks → separate groups
- Each group can run in parallel with other groups

**Example:**
```
Task 1: Create User model
Task 2: Add User validation (depends on Task 1)
Task 3: Create User API (depends on Task 1, 2)
Task 4: Create Auth middleware (independent)
Task 5: Add Auth tests (depends on Task 4)
Task 6: Update README (independent)

Groups:
- Group A: Task 1 → Task 2 → Task 3
- Group B: Task 4 → Task 5
- Group C: Task 6
```

### Step 4: Write plan.md

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** Use `/executing-plans` to implement this plan.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---

## Task Groups

| Group | Tasks | Parallel? |
|-------|-------|-----------|
| A | Task 1 → 2 → 3 | Yes (with B, C) |
| B | Task 4 → 5 | Yes (with A, C) |
| C | Task 6 | Yes (with A, B) |

## Dependency Graph

```
Group A: Task 1 → Task 2 → Task 3
Group B: Task 4 → Task 5
Group C: Task 6

A, B, C can run in parallel.
```

## Task Files

- `tasks/group-a.md` - User model, validation, API
- `tasks/group-b.md` - Auth middleware and tests
- `tasks/group-c.md` - Documentation update
```

### Step 5: Write Task Files

Each task file in `tasks/` folder:

```markdown
# [Feature] - Group [X]

**Execution:** Sequential (Task 1 must complete before Task 2)

---

## Task 1: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

```bash
pytest tests/path/test.py::test_name -v
```

Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

```bash
pytest tests/path/test.py::test_name -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```

---

## Task 2: [Next Component]
...
```

### Step 6: Commit and Handoff

```bash
git add docs/features/[feature-name]_[YYYY-MM-DD]/plan.md
git add docs/features/[feature-name]_[YYYY-MM-DD]/tasks/
git commit -m "docs: add implementation plan and task files"
```

Then report:

```
Plan complete!

Created:
  docs/features/[feature-name]_[YYYY-MM-DD]/
    ├── plan.md (overview + dependency graph)
    └── tasks/
        ├── group-a.md (3 tasks, sequential)
        ├── group-b.md (2 tasks, sequential)
        └── group-c.md (1 task)

Next step: /executing-plans docs/features/[feature-name]_[YYYY-MM-DD]
```

## Task Writing Rules

- **Exact file paths** - No "somewhere in src/"
- **Complete code** - Not "add validation logic"
- **Exact commands** - Include expected output
- **2-5 minutes per task** - If longer, split it
- **TDD always** - Red → Green → Commit
- **One thing per task** - If "and" appears, split it

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Integration

**Previous skill:** `/feature-planning` or `/technical-spec`

**Next skill:** `/executing-plans` - creates worktrees and executes
