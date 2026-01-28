# Browser-Use Usage Examples

## Basic Navigation

```bash
# Open a URL (headless mode)
browser-use open https://www.naver.com

# Open a URL with visible browser window
browser-use --headed open https://www.google.com
```

## Interacting with Pages

```bash
# Click an element by index
browser-use click 5

# Type text
browser-use type "Hello World"

# Type text into specific element
browser-use input 3 "search query"

# Scroll page
browser-use scroll down
browser-use scroll up

# Navigate back
browser-use back
```

## Getting Page Information

```bash
# Get current browser state (URL, title, elements)
browser-use state

# Get state as JSON
browser-use --json state

# Take a screenshot
browser-use screenshot

# Execute JavaScript
browser-use eval "document.title"

# Extract data using LLM
browser-use extract "Get all product prices"
```

## Advanced Features

```bash
# Run Python code with browser context
browser-use python "print(browser.url)"

# Run AI agent task (requires API key)
browser-use run "Fill the contact form with my details"

# List active browser sessions
browser-use sessions

# Close a session
browser-use close --session mysession
```

## Session Management

```bash
# Use named session
browser-use --session work open https://example.com

# Switch between tabs
browser-use switch 2

# Close current tab
browser-use close-tab
```

## Browser Modes

```bash
# Use Chromium (default)
browser-use --browser chromium open https://example.com

# Use real Chrome browser
browser-use --browser real open https://example.com

# Use remote browser
browser-use --browser remote open https://example.com
```

## Common Workflows

### Web Scraping Example

```bash
# Open page
browser-use --headed open https://news.ycombinator.com

# Get page state to see element indices
browser-use state

# Click on a story (replace 5 with actual element index)
browser-use click 5

# Extract content
browser-use extract "Get the article title and top 3 comments"
```

### Form Filling Example

```bash
# Open form page
browser-use open https://example.com/contact

# Fill form fields (get indices from state command)
browser-use input 3 "John Doe"
browser-use input 4 "john@example.com"
browser-use input 5 "Hello, this is my message"

# Submit form
browser-use click 10
```

### Automated Testing Example

```bash
# Start session
browser-use --session test --headed open https://myapp.com/login

# Fill login form
browser-use --session test input 2 "testuser"
browser-use --session test input 3 "password123"
browser-use --session test click 4

# Verify login
browser-use --session test state

# Take screenshot for evidence
browser-use --session test screenshot

# Close session
browser-use --session test close
```
