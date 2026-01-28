---
name: browser-use-installer
description: Install and configure browser-use for browser automation. Use when the user needs to install browser-use globally, set up Playwright and Chromium for web automation, or verify their browser-use installation. Handles installation via uv tool, Playwright setup, and provides usage guidance for browser automation tasks.
---

# Browser-Use Installer

## Overview

Install browser-use as a global CLI tool for browser automation. This skill provides scripts and guidance for installing browser-use using uv, setting up Playwright and Chromium, and verifying the installation works correctly.

## Installation Workflow

### Step 1: Install browser-use

Use the installation script to install browser-use globally:

```bash
bash scripts/install_browser_use.sh
```

Or manually:

```bash
uv tool install browser-use
```

**Prerequisites:**
- `uv` must be installed (install via: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

**What gets installed:**
- `browser-use` - Main CLI command
- `bu` - Short alias
- `browseruse` - Alternative command
- `browser` - Another alias

### Step 2: Install Playwright and Chromium

Browser-use requires Playwright and Chromium for actual browser automation:

```bash
bash scripts/install_playwright.sh
```

Or manually:

```bash
# Install Playwright
pip3 install --user playwright

# Install Chromium browser
~/Library/Python/3.x/bin/playwright install chromium
```

**Note:** Replace `3.x` with your Python version (e.g., `3.9`, `3.12`)

### Step 3: Verify Installation

Run the verification script to confirm everything is working:

```bash
bash scripts/verify_installation.sh
```

Or manually test:

```bash
# Check command exists
which browser-use

# Test help command
browser-use --help

# Test browser automation
browser-use --headed open https://www.google.com
```

## Quick Start

After installation, test with a simple command:

```bash
# Open a website (headless)
browser-use open https://www.naver.com

# Open with visible browser window
browser-use --headed open https://www.google.com

# Get current page state
browser-use state

# Take a screenshot
browser-use screenshot
```

## Common Commands

### Navigation
- `browser-use open <url>` - Navigate to URL
- `browser-use back` - Go back in history

### Interaction
- `browser-use click <index>` - Click element by index
- `browser-use type "<text>"` - Type text
- `browser-use input <index> "<text>"` - Type into specific element
- `browser-use scroll <direction>` - Scroll page (up/down)

### Information
- `browser-use state` - Get page state (URL, title, elements)
- `browser-use screenshot` - Take screenshot
- `browser-use eval "<javascript>"` - Execute JavaScript

### AI Features (requires API key)
- `browser-use extract "<prompt>"` - Extract data using LLM
- `browser-use run "<task>"` - Run AI agent task

For detailed usage examples, see [references/usage_examples.md](references/usage_examples.md).

## Troubleshooting

### Command not found

If `browser-use` is not found after installation, add uv's bin directory to PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add to `~/.zshrc` or `~/.bashrc` to make permanent.

### Playwright not found

If browser automation fails, verify Playwright installation:

```bash
pip3 show playwright
```

Reinstall if needed:

```bash
pip3 install --user --upgrade playwright
~/Library/Python/3.x/bin/playwright install chromium
```

### Browser automation not working

If the browser doesn't open or automation fails:

1. Verify Chromium is installed: `~/Library/Python/3.x/bin/playwright install chromium`
2. Test with headed mode: `browser-use --headed open https://google.com`
3. Check for error messages in output

## Resources

### scripts/
- `install_browser_use.sh` - Install browser-use via uv
- `install_playwright.sh` - Install Playwright and Chromium
- `verify_installation.sh` - Verify installation is working

### references/
- `usage_examples.md` - Comprehensive usage examples and workflows
