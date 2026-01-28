#!/bin/bash
# Verify browser-use installation

set -e

echo "🔍 Verifying browser-use installation..."
echo ""

# Check browser-use command
if command -v browser-use &> /dev/null; then
    echo "✅ browser-use command found"
    BROWSER_USE_PATH=$(which browser-use)
    echo "   Location: $BROWSER_USE_PATH"
else
    echo "❌ browser-use command not found"
    exit 1
fi

# Check aliases
echo ""
echo "Available aliases:"
if command -v bu &> /dev/null; then
    echo "  ✅ bu"
fi
if command -v browseruse &> /dev/null; then
    echo "  ✅ browseruse"
fi

# Check Playwright
echo ""
if pip3 show playwright &> /dev/null 2>&1; then
    echo "✅ Playwright installed"
    PLAYWRIGHT_VERSION=$(pip3 show playwright | grep Version | cut -d' ' -f2)
    echo "   Version: $PLAYWRIGHT_VERSION"
else
    echo "⚠️  Playwright not installed (required for browser automation)"
fi

# Test browser-use help command
echo ""
echo "Testing browser-use help..."
if browser-use --help &> /dev/null; then
    echo "✅ browser-use is working correctly"
else
    echo "⚠️  browser-use help command failed"
fi

echo ""
echo "✅ Installation verification complete!"
