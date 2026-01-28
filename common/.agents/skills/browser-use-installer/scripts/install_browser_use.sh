#!/bin/bash
# Install browser-use globally using uv tool install

set -e

echo "🚀 Installing browser-use..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv is not installed"
    echo "Please install uv first: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install browser-use as a global tool
echo "📦 Installing browser-use via uv..."
uv tool install browser-use

echo "✅ browser-use installed successfully!"
echo ""
echo "Available commands:"
echo "  - browser-use"
echo "  - bu (short alias)"
echo "  - browseruse"
echo ""
echo "Next: Install Playwright and Chromium for browser automation"
