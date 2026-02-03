---
name: feature-planning
description: Use when starting a new feature - creates PRD and technical-spec through collaborative dialogue
argument-hint: "[feature description or PRD folder path (optional)]"
---

# Feature Planning

## Overview

Transform user ideas into PRD and technical specification. Checks for existing PRD first, then creates technical-spec.

**Announce at start:** "I'm using the feature-planning skill to create PRD and Technical Spec."

**Output location:** `docs/features/[feature-name]_[YYYY-MM-DD]/`

## Workflow

### Step 1: Start

- If `$ARGUMENTS` is a folder path (e.g., `docs/features/xxx`) → check for existing PRD
- If `$ARGUMENTS` is a description → proceed to Step 2
- If `$ARGUMENTS` empty → ask "What feature would you like to build?"

### Step 2: PRD Check

Check if PRD exists:

**PRD exists:**
- Read and summarize the PRD
- Confirm with user: "Found existing PRD. Should I proceed to technical-spec?"
- If yes → Step 3

**PRD does not exist:**
- Invoke `/prd` skill to create PRD
- After PRD complete → Step 3

### Step 3: Technical Spec

Invoke `/technical-spec` skill with the feature folder path.

The technical-spec skill will:
- Read the PRD
- Create technical-spec.md through brainstorming dialogue
- Cover: 목적, 해결(아키텍처/API), 행동 정의, 테스트 전략, 리스크, 오픈 이슈

### Step 4: Complete

Report created files:

```
Feature planning complete!

Created:
  docs/features/[name]_[date]/
    ├── prd.md
    └── technical-spec.md

Next step: /writing-plans docs/features/[feature-name]_[YYYY-MM-DD]
```

## Key Principles

- **PRD first** - Always ensure PRD exists before technical-spec
- **Delegate to skills** - Use /prd and /technical-spec skills
- **Brainstorming style** - One question at a time, multiple choice preferred

## Integration

**Uses:**
- `/prd` - creates PRD if not exists
- `/technical-spec` - creates technical specification

**Next skill:** `/writing-plans` - creates detailed implementation plan (plan.md)
