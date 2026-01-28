---
name: verification-loop
description: Use when completing features, before creating PRs, after refactoring, or when ensuring quality gates pass. Triggers on build failures, type errors, test failures, or before code integration.
---

# Verification Loop

## Overview

A systematic verification system that runs multiple quality gates in sequence. Each phase must pass before proceeding to the next, ensuring comprehensive quality checks before code integration.

## When to Use

**Invoke this skill:**
- After completing a feature or significant code change
- Before creating a PR or merging code
- When you want to ensure quality gates pass
- After refactoring
- When build, type, or test errors are suspected

**Don't use when:**
- Making trivial changes (typo fixes, comment updates)
- In early exploration/prototyping phase
- Running continuous integration (CI handles this)

## Verification Phases

Run phases in order. If any phase fails, STOP and fix before continuing.

### Phase 1: Build Verification

```bash
# Check if project builds
npm run build 2>&1 | tail -20
# OR
pnpm build 2>&1 | tail -20
```

**If build fails:** STOP and fix compilation errors before continuing.

### Phase 2: Type Check

```bash
# TypeScript projects
npx tsc --noEmit 2>&1 | head -30

# Python projects
pyright . 2>&1 | head -30
```

Report all type errors. Fix critical ones before continuing.

### Phase 3: Lint Check

```bash
# JavaScript/TypeScript
npm run lint 2>&1 | head -30

# Python
ruff check . 2>&1 | head -30
```

Address linting errors, warnings are optional.

### Phase 4: Test Suite

```bash
# Run tests with coverage
npm run test -- --coverage 2>&1 | tail -50

# Check coverage threshold (Target: 80% minimum)
```

**Report:**
- Total tests: X
- Passed: X
- Failed: X
- Coverage: X%

### Phase 5: Security Scan

```bash
# Check for secrets
grep -rn "sk-" --include="*.ts" --include="*.js" . 2>/dev/null | head -10
grep -rn "api_key" --include="*.ts" --include="*.js" . 2>/dev/null | head -10

# Check for console.log in production code
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
```

### Phase 6: Diff Review

```bash
# Show what changed
git diff --stat
git diff HEAD~1 --name-only
```

**Review each changed file for:**
- Unintended changes
- Missing error handling
- Potential edge cases

## Output Format

After running all phases, produce a verification report:

```
VERIFICATION REPORT
==================

Build:     [PASS/FAIL]
Types:     [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...
```

## Quick Reference

| Phase | Command | Pass Criteria |
|-------|---------|---------------|
| Build | `npm run build` | Exit code 0 |
| Types | `npx tsc --noEmit` | No type errors |
| Lint | `npm run lint` | No errors (warnings OK) |
| Tests | `npm test -- --coverage` | All pass, >80% coverage |
| Security | `grep` for secrets/logs | No sensitive data |
| Diff | `git diff --stat` | Only intended changes |

## Continuous Mode

For long sessions, run verification checkpoints:

**Set mental checkpoints:**
- After completing each major function
- After finishing a component
- Before moving to next task
- Every 15 minutes during active coding

**Run:** Quick verification loop at each checkpoint.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping phases when "confident" | Always run all phases. Confidence ≠ correctness. |
| Continuing after phase failure | STOP at first failure. Fix before proceeding. |
| Not checking git diff | Unintended changes slip through. Always review diff. |
| Ignoring coverage drops | Coverage drops indicate untested code paths. |
| Running phases in wrong order | Build → Types → Lint → Tests. Order matters. |

## Integration with Other Tools

**Complements PostToolUse hooks:**
- Hooks catch issues immediately after tool use
- This skill provides comprehensive review before integration
- Use both for maximum quality

**Complements CI/CD:**
- Run this locally before pushing
- Catches issues faster than waiting for CI
- Reduces CI failures and iteration time

## Real-World Impact

**Without verification loop:**
- Type errors discovered after PR creation
- Build failures block team
- Security issues in production
- Time wasted on CI failures

**With verification loop:**
- Issues caught locally before push
- Clean PRs that pass CI first time
- Confidence in code quality
- Faster review cycles
