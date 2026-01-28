---
description: Create a task branch and plan doc by manual input or change analysis
argument-hint: "[task description (optional)]"
allowed-tools: Bash(git *), Write, Bash(mkdir *), Bash(date *)
---

# Task Initiation & Planning

## Step 1: Determine Task Context

If `$ARGUMENTS` is provided, proceed directly to **Step 2** using those arguments.
If `$ARGUMENTS` is empty, present the following two options to the user:

1.  **Manual Entry**: Ask "What task are you planning to work on?"
2.  **Analyze Current Changes**:
    - Ask the user: "Which **base branch** should I compare against? (e.g., main, develop)"
    - Once the base branch is provided, analyze:
      - `git diff [base-branch]`: To see uncommitted changes.
      - `git log [base-branch]..HEAD --oneline`: To see commits not yet in the base branch.
    - Summarize these changes into a task description.

## Step 2: Categorize and Slugify

Based on the manual input or analyzed summary, determine:

- **Category**: `feature`, `fix`, `docs`, or `chore`.
- **Slug**: A clean, URL-friendly string (e.g., `update-schema-logic`).

## Step 3: Git Branch & Document Creation

1.  **Branch Name**: `[category]/[slug]`
2.  **Bash Action**: `git checkout -b [branch-name]`
3.  **File Setup**:
    - **Path**: `docs/plans/[branch-name-with-underscore]_!date +%Y-%m-%d!.md`
    - **Content**:

      ```markdown
      # Plan: [Summary of Task]

      - **Base Branch**: [The base branch used for comparison, if applicable]
      - **Created At**: !`date +%Y-%m-%d`
      - **Branch**: [branch-name]
      - **Status**: 🏗️ In Progress

      ## Context / Analysis

      [Briefly explain the current changes analyzed or the manual input provided]

      ## Objectives

      - [Objective 1]
      - [Objective 2]
      ```

## Step 4: Finalize

- Report the created branch and the path to the plan document.
- Ask if the user wants to start the next implementation step.
