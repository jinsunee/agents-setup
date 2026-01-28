# Agents Setup

This repository is a centralized hub for managing **Agent Skills** and environment configurations across various domains (Backend, Marketing, Design, etc.).

## 📂 Project Structure

- `common/.agents/skills`: The central repository for all reusable agent skills.
- `scripts/`: Utility scripts for setting up agent environments.
- `setups/`: Configuration files for various agents (Antigravity, Claude, etc.).
- `backend/`, `react-native/`, `ui-ux-design/`, `marketing/`: Domain-specific workspaces.

## 🛠 Key Features

### Link Skill

Creates symbolic links for specific skills into directories where agents can recognize them (`.agent/skills` and `.claude/skills`).

```bash
# Usage
npm run link-skill <path-to-skill>

# Example
npm run link-skill common/.agents/skills/browser-use
```

## 🚀 Getting Started

1. Install the required dependencies:

   ```bash
   pnpm install
   ```

2. Link necessary skills from the common repository to your desired project stage or area.

## 📝 Available Skills

The `common/.agents/skills` directory currently contains a wide variety of skills, including:

- `browser-use`: Browser automation and interaction.
- `continuous-learning`: Methodology for ongoing knowledge accumulation.
- `systematic-debugging`: Structured approaches to debugging.
- `test-driven-development`: Guides for TDD-based development.
- ...and many more (over 20+ specialized skills).
