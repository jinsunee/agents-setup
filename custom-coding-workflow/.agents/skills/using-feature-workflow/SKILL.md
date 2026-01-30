---
name: using-feature-workflow
description: Use when building new features - guides through the complete workflow from idea to implementation with TDD and parallel execution
---

# Using Feature Workflow

## Overview

Complete workflow for turning ideas into implemented features using TDD approach and parallel execution across worktrees.

## The Workflow

```
┌──────────────────────────────────────────────────────────────┐
│  1. /feature-planning                                        │
│     Idea → PRD → Plan → Tests (failing)                      │
│     Output: features/[name]_[date]/                          │
│              ├── prd.md                                      │
│              ├── plan.md                                     │
│              └── tests/                                      │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│  2. /writing-tasks                                           │
│     Plan → 2-5 min tasks with grouping                       │
│     Output: features/[name]_[date]/                          │
│              └── tasks/                                      │
│                    ├── g1-01_xxx.md  (group 1)               │
│                    ├── g1-02_xxx.md                          │
│                    ├── g2-01_xxx.md  (group 2)               │
│                    └── 01_xxx.md     (independent)           │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│  3. /setup-task-worktrees                                    │
│     Tasks → Worktrees for parallel execution                 │
│     Output: .worktrees/                                      │
│              ├── [feature]_g1/                               │
│              ├── [feature]_g2/                               │
│              └── [feature]_independent/                      │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│  4. /executing-tasks (in each worktree)                      │
│     TDD: Red → Green → Commit                                │
│                                                              │
│     Terminal 1:                  Terminal 2:                 │
│     cd .worktrees/xxx_g1         cd .worktrees/xxx_g2        │
│     claude                       claude                      │
│     /executing-tasks             /executing-tasks            │
└──────────────────────────────────────────────────────────────┘
```

## When to Use Each Skill

| Situation | Skill |
|-----------|-------|
| "새 기능 만들고 싶어" | `/feature-planning` |
| "PRD, Plan이 있는데 task로 쪼개줘" | `/writing-tasks` |
| "task 작성 완료, worktree 만들어줘" | `/setup-task-worktrees` |
| "worktree에서 task 실행해줘" | `/executing-tasks` |

## Quick Start

**새 기능 시작:**
```
/feature-planning 사용자 인증 기능 추가
```

**이미 Plan이 있을 때:**
```
/writing-tasks features/user-auth_2025-01-30
```

**Tasks 완료 후 worktree 생성:**
```
/setup-task-worktrees features/user-auth_2025-01-30
```

**각 worktree에서 실행:**
```bash
cd .worktrees/user-auth_g1 && claude
# Claude 세션에서:
/executing-tasks features/user-auth_2025-01-30
```

## Key Principles

### TDD is Mandatory

Every task follows:
1. **RED**: Write test → must fail
2. **GREEN**: Implement → minimal code
3. **VERIFY**: Run test → must pass
4. **COMMIT**: Save progress

### Parallel Execution

- **Same group** (`g1-01`, `g1-02`) → Sequential in one worktree
- **Different groups** (`g1-*`, `g2-*`) → Parallel in separate worktrees
- **Independent** (no prefix) → Any worktree, any order

### Feedback at Every Step

- PRD 작성 후 → 피드백 요청
- Plan 작성 후 → 피드백 요청
- 3개 Task 완료마다 → 진행 리포트

## File Structure

```
features/
  [feature-name]_[YYYY-MM-DD]/
    ├── prd.md              # Requirements
    ├── plan.md             # Architecture, feature list
    ├── tests/              # Integration tests (TDD - written first)
    │     └── test_xxx.py
    └── tasks/              # Executable task units
          ├── g1-01_xxx.md  # Group 1 (sequential)
          ├── g1-02_xxx.md
          ├── g2-01_xxx.md  # Group 2 (sequential)
          └── 01_xxx.md     # Independent

.worktrees/
  ├── [feature]_g1/         # Worktree for group 1
  ├── [feature]_g2/         # Worktree for group 2
  └── [feature]_independent/ # Worktree for independent tasks
```

## Red Flags

| Thought | Reality |
|---------|---------|
| "Plan 없이 바로 코딩하자" | `/feature-planning` 먼저 |
| "테스트는 나중에" | TDD 필수, 테스트 먼저 |
| "한 터미널에서 다 하자" | 그룹별로 worktree 분리 |
| "task 파일 없이 진행" | `/writing-tasks`로 task 생성 |
| "의존성 있는 task를 병렬로" | 같은 그룹은 순차 실행 |

## Integration with Other Skills

**Before feature-planning:**
- `/brainstorming` - 아이디어가 불명확할 때

**After all tasks complete:**
- `/finishing-a-development-branch` - 브랜치 머지/PR 생성
