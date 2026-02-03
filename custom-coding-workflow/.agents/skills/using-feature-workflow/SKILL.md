---
name: using-feature-workflow
description: Use when building new features - guides through the complete workflow from idea to implementation
---

# Using Feature Workflow

## Overview

This skill guides you through the complete feature development workflow. Follow the phases in order.

**Announce at start:** "I'm using the feature-workflow skill to guide this development."

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  Phase 1: Planning                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  /feature-planning                                                   │   │
│  │      │                                                               │   │
│  │      ├── /prd ──────────────────► prd.md                            │   │
│  │      │                                                               │   │
│  │      └── /technical-spec ───────► technical-spec.md                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│                                      ▼                                      │
│  Phase 2: Plan Writing                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  /writing-plans                                                      │   │
│  │      │                                                               │   │
│  │      ├── plan.md (overview + dependency graph)                      │   │
│  │      │                                                               │   │
│  │      └── tasks/                                                      │   │
│  │          ├── group-a.md                                             │   │
│  │          ├── group-b.md                                             │   │
│  │          └── group-c.md                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│                                      ▼                                      │
│  Phase 3: Execution                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  /executing-plans                                                    │   │
│  │      │                                                               │   │
│  │      └── Create worktrees ──► Guide user to terminals               │   │
│  │                            ──► Execute tasks (TDD)                  │   │
│  │                            ──► Merge when all complete              │   │
│  │                                                                      │   │
│  │  During execution:                                                   │   │
│  │      • /test-driven-development (always)                            │   │
│  │      • /systematic-debugging (when stuck)                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│                                      ▼                                      │
│  Phase 4: Review                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  /requesting-code-review ──► Request review                         │   │
│  │  /receiving-code-review  ──► Handle feedback                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                      │                                      │
│                                      ▼                                      │
│  Phase 5: Completion                                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  /verification-before-completion ──► Verify all tests pass          │   │
│  │  /finishing-a-development-branch ──► Merge / PR / Keep / Discard    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Output Structure

```
docs/features/[feature-name]_[YYYY-MM-DD]/
├── prd.md                  # Phase 1: Product requirements
├── technical-spec.md       # Phase 1: Technical specification
├── plan.md                 # Phase 2: Implementation overview
└── tasks/                  # Phase 2: Executable task files
    ├── group-a.md
    ├── group-b.md
    └── group-c.md
```

## Skill Reference

| Phase | Skill | Purpose |
|-------|-------|---------|
| 1. Planning | `/feature-planning` | Entry point - orchestrates PRD + spec |
| | `/prd` | Create Product Requirements Document |
| | `/technical-spec` | Create technical specification |
| 2. Plan Writing | `/writing-plans` | Create plan.md + task files |
| 3. Execution | `/executing-plans` | Create worktrees + execute tasks |
| | `/test-driven-development` | TDD methodology (always) |
| | `/systematic-debugging` | Debug when stuck |
| 4. Review | `/requesting-code-review` | Request code review |
| | `/receiving-code-review` | Handle review feedback |
| 5. Completion | `/verification-before-completion` | Verify before claiming done |
| | `/finishing-a-development-branch` | Merge/PR/Keep/Discard |

---

## Phase 1: Planning

**Purpose:** Transform idea into PRD and technical specification.

**Invoke:** `/feature-planning`

```
User: "Add user authentication"
You: Invoke Skill tool with "feature-planning"
     Follow the skill to create PRD and technical-spec
```

**Output:**
```
docs/features/[feature-name]_[YYYY-MM-DD]/
├── prd.md
└── technical-spec.md
```

**When complete:** Proceed to Phase 2.

---

## Phase 2: Plan Writing

**Purpose:** Create detailed implementation plan with grouped tasks.

**Invoke:** `/writing-plans`

```
You: Invoke Skill tool with "writing-plans"
     Argument: "docs/features/[feature-name]_[YYYY-MM-DD]"
```

**Output:**
```
docs/features/[feature-name]_[YYYY-MM-DD]/
├── plan.md                 # Overview + dependency graph
└── tasks/
    ├── group-a.md          # Sequential tasks
    ├── group-b.md          # Sequential tasks
    └── group-c.md          # Independent tasks
```

**When complete:** Commit task files, proceed to Phase 3.

---

## Phase 3: Execution

**Purpose:** Execute tasks in isolated worktrees.

**Invoke:** `/executing-plans`

```
You: Invoke Skill tool with "executing-plans"
     Argument: "docs/features/[feature-name]_[YYYY-MM-DD]"
```

### Execution Flow Detail

```
/executing-plans
       │
       ▼
┌──────────────────┐
│ Read plan.md     │
│ Read tasks/*.md  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ Create worktree for EACH group:                              │
│   .worktrees/[feature]_group-a                              │
│   .worktrees/[feature]_group-b                              │
│   .worktrees/[feature]_group-c                              │
│                                                              │
│ (Every group gets isolated worktree - keeps main clean)     │
└──────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ Guide user to open terminals:                                │
│                                                              │
│   Terminal 1: cd .worktrees/[feature]_group-a && claude     │
│               "Execute tasks/group-a.md"                     │
│                                                              │
│   Terminal 2: cd .worktrees/[feature]_group-b && claude     │
│               "Execute tasks/group-b.md"                     │
│                                                              │
│   Terminal 3: cd .worktrees/[feature]_group-c && claude     │
│               "Execute tasks/group-c.md"                     │
│                                                              │
│ (Run in parallel or sequentially - user's choice)           │
└──────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ In each worktree session:                                    │
│   • Read assigned task file                                  │
│   • Execute tasks sequentially (Red → Green → Commit)        │
│   • Report "Group X done" when complete                      │
└──────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────┐
│ Wait for         │
│ "All groups done"│
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ Merge branches:                                              │
│   git checkout -b feature/[feature-name]                    │
│   git merge feature/[feature]_group-a                       │
│   git merge feature/[feature]_group-b                       │
│   git merge feature/[feature]_group-c                       │
└──────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────┐
│ Cleanup          │
│ worktrees        │
└──────────────────┘
```

**During execution, also use:**
- `/test-driven-development` - Always (Red → Green → Commit)
- `/systematic-debugging` - When tests fail unexpectedly

**When complete:** All branches merged, proceed to Phase 4.

---

## Phase 4: Review

**Purpose:** Get code review and handle feedback.

**Invoke:** `/requesting-code-review` then `/receiving-code-review`

```
You: Invoke Skill tool with "requesting-code-review"
     After receiving feedback:
     Invoke Skill tool with "receiving-code-review"
```

**When complete:** All review feedback addressed, proceed to Phase 5.

---

## Phase 5: Completion

**Purpose:** Verify and finalize the work.

**Invoke:** `/verification-before-completion` then `/finishing-a-development-branch`

```
You: Invoke Skill tool with "verification-before-completion"
     Verify all tests pass

     Invoke Skill tool with "finishing-a-development-branch"
     Choose: Merge / PR / Keep / Discard
```

**When complete:** Feature is merged or PR created.

---

## Quick Start

```bash
# Start a new feature
claude
> /feature-planning "Add user authentication"

# After planning complete
> /writing-plans docs/features/user-auth_2025-02-03

# Execute the plan
> /executing-plans docs/features/user-auth_2025-02-03

# After implementation complete
> /finishing-a-development-branch
```

## Red Flags

**Never:**
- Skip phases
- Start coding without PRD + technical-spec
- Execute tasks without plan.md
- Merge without verification
- Skip TDD during execution

**Always:**
- Follow phases in order
- Invoke each skill before acting
- Use worktrees for isolation
- Verify tests before completion
