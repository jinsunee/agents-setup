전체 플로우 (최종)

[사용자 아이디어]
↓
/feature-planning
↓
features/[name]_[YYYY-MM-DD]/
├── prd.md ← 요구사항 (피드백 받음)
├── plan.md ← 아키텍처, 기능 목록 (피드백 받음)
└── tests/ ← 통합 테스트 코드 (실패 상태)
↓
/writing-tasks
↓
features/[name]_[YYYY-MM-DD]/
└── tasks/
├── g1-01_xxx.md ← 그룹 1
├── g1-02_xxx.md
├── g2-01_xxx.md ← 그룹 2
├── 01_xxx.md ← independent
└── ...
↓
/setup-task-worktrees
↓
.worktrees/
├── feature-[name]\_g1/
├── feature-[name]\_g2/
└── feature-[name]\_independent/
↓
각 worktree에서 터미널 열고 claude 실행
↓
/executing-tasks (각 worktree에서)
↓
TDD 방식으로 Task 순차 실행 → 테스트 점점 통과 → 완료

---

Skill 목록 (최종)
┌───────────────────────┬───────────────────────────────────────────┐
│ Skill │ 역할 │
├───────────────────────┼───────────────────────────────────────────┤
│ /feature-planning │ 아이디어 → PRD, Plan, Tests 생성 │
├───────────────────────┼───────────────────────────────────────────┤
│ /writing-tasks │ Plan → 2-5분 단위 Task 분해 (그룹핑 포함) │
├───────────────────────┼───────────────────────────────────────────┤
│ /setup-task-worktrees │ Tasks 기반으로 Worktree 일괄 생성 │
├───────────────────────┼───────────────────────────────────────────┤
│ /executing-tasks │ TDD 방식으로 Task 순차 실행 │
└───────────────────────┴───────────────────────────────────────────┘
