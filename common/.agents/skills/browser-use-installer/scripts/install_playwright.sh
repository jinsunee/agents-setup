#!/bin/bash
# Install Playwright and Chromium for browser automation

set -e

echo "🌐 Installing Playwright and Chromium..."

# Check if pip3 or python3 is available
if ! command -v pip3 &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 is not installed"
    exit 1
fi

# Install playwright
echo "📦 Installing playwright package..."
pip3 install --user playwright

# Get the playwright executable path
PLAYWRIGHT_PATH=$(python3 -c "import site; print(site.USER_BASE + '/bin/playwright')")

if [ ! -f "$PLAYWRIGHT_PATH" ]; then
    echo "⚠️  Warning: playwright not found in expected location"
    echo "Trying alternative path..."
    PLAYWRIGHT_PATH="$HOME/Library/Python/$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')/bin/playwright"
fi

# Install Chromium browser
echo "📦 Installing Chromium browser..."
"$PLAYWRIGHT_PATH" install chromium

echo "✅ Playwright and Chromium installed successfully!"
echo ""
echo "Installation complete! You can now use browser-use with browser automation."
