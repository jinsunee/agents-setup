---
name: tdd
description: Enforces strict TDD discipline for Vite/React and Python (Django/FastAPI) environments. Combines the Red-Green-Refactor iron law with modern E2E QA using agent-browser.
---

# Unified TDD Mastery (Full-Stack)

This skill mandates a **Test-First** approach for all features, bug fixes, and refactoring. It integrates rigorous TDD cycles with high-level User Journey verification.

## ⚖️ The Iron Law

> **"NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST."**
> If you wrote code before the test: **Delete it. Start over.** No exceptions.

1. **Watch it Fail:** You must see the test fail with the expected error. If it passes immediately, your test is invalid.
2. **Minimalism:** Write only the simplest code to pass the current test.
3. **80% Coverage:** Maintain ≥80% coverage across Unit, Integration, and E2E layers.

---

## 🛠 Tech Stack & Tools

### Frontend: Vite + React

- **Unit/Integration:** `Vitest` + `React Testing Library`
- **E2E/QA:** `Playwright` + `agent-browser` (for AI-driven exploratory QA)

### Backend: Python (Django / FastAPI)

- **Frameworks:** `pytest-django` or `pytest` + `httpx` (for FastAPI)
- **Principles:** Isolated database for tests, mocking external APIs only.

---

## 🔄 The Unified TDD Workflow

### Step 1: Define User Journeys (E2E)

Before coding, define the "Happy Path" using Playwright or `agent-browser`.

- **E2E Test:** Create a `.spec.ts` for the critical flow.
- **AI QA:** Use `agent-browser` to verify the UI requirements or complex workflows.
  > Example: `agent-browser "Verify that the search results update dynamically as I type 'BTC' in the market search bar."`

### Step 2: RED - Write Failing Tests

Start from the smallest unit of behavior.

#### [React Example]

```typescript
// Search.test.tsx
it('renders results based on search input', () => {
  render(<SearchComponent />);
  const input = screen.getByPlaceholderText(/search/i);
  fireEvent.change(input, { target: { value: 'Election' } });
  // This fails because implementation doesn't exist yet
  expect(screen.getByText('US Election 2024')).toBeInTheDocument();
});
```
