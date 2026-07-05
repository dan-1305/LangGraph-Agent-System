# MCP Playwright Server Setup Guide

## Overview

The ExecuteAutomation Playwright MCP Server provides browser automation capabilities using Playwright. This server enables LLMs to interact with web pages, take screenshots, generate test code, scrape web pages, and execute JavaScript in a real browser environment.

## Installation Details

- **Package**: `@executeautomation/playwright-mcp-server`
- **Installation Method**: Global npm install
- **Configuration**: Added to `.vscode/cline_mcp_settings.json`

## Configuration

The server is configured in `.vscode/cline_mcp_settings.json`:

```json
"github.com/executeautomation/mcp-playwright": {
  "command": "npx",
  "args": [
    "-y",
    "@executeautomation/playwright-mcp-server"
  ]
}
```

## Browser Installation

The Playwright MCP Server **automatically installs browser binaries** when you first use it. No manual setup required!

### Optional: Manual Browser Installation

If you prefer to install browsers manually:

```bash
# Install all browsers
npx playwright install

# Or install specific browsers
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit
```

### Browser Storage Location (Windows)

Browsers are installed to: `%USERPROFILE%\AppData\Local\ms-playwright`

## Available Tools

The Playwright MCP server provides the following main capabilities:

### 1. **playwright_navigate**
Navigate to a URL in the browser.

### 2. **playwright_click**
Click on an element on the page.

### 3. **playwright_fill**
Fill in text input fields.

### 4. **playwright_screenshot**
Take screenshots of the page or specific elements.

### 5. **playwright_evaluate**
Execute JavaScript code in the browser context.

### 6. **playwright_select**
Select options from dropdown menus.

### 7. **playwright_resize**
Resize the browser window or use device emulation (143 real device presets supported).

### 8. **playwright_wait**
Wait for elements, conditions, or timeouts.

### 9. **playwright_close**
Close the current browser context.

### 10. **playwright_get_page_info**
Get information about the current page (URL, title, content).

## Device Emulation

Test on real device profiles with 143 device presets:

```javascript
// Test on iPhone 13
await playwright_resize({ device: "iPhone 13" });

// Switch to iPad with landscape orientation
await playwright_resize({ device: "iPad Pro 11", orientation: "landscape" });

// Test desktop view
await playwright_resize({ device: "Desktop Chrome" });
```

**Supported devices include:** iPhone, iPad, Pixel, Galaxy, and Desktop browsers with proper emulation of viewport, user-agent, touch events, and device pixel ratios.

## Usage Example

A typical workflow might look like:

1. Navigate to a webpage
2. Wait for elements to load
3. Take a screenshot
4. Interact with elements (click, fill forms)
5. Execute JavaScript to extract data
6. Take final screenshot
7. Close the browser

## Restart Required

After adding this MCP server, **restart VS Code** for the changes to take effect and the server to become available.

## Logging

In stdio mode, logging is automatically directed to files only (not console) to maintain clean JSON-RPC communication. Logs are written to `~/playwright-mcp-server.log`.

## Documentation

- [Official Documentation](https://executeautomation.github.io/mcp-playwright/)
- [API Reference](https://executeautomation.github.io/mcp-playwright/docs/playwright-web/Supported-Tools)
- [Device Quick Reference](https://executeautomation.github.io/mcp-playwright/docs/playwright-web/Device-Quick-Reference)

## Troubleshooting

### Browser Not Found
The server will automatically install browsers on first use. If you encounter issues, try manually installing browsers using `npx playwright install`.

### Connection Issues
- Ensure VS Code has been restarted after configuration
- Check that npm and npx are available in your PATH
- Verify the server configuration in `.vscode/cline_mcp_settings.json`

## Version Information

- **Installed Version**: Latest via npm global install
- **Server Name**: `github.com/executeautomation/mcp-playwright`
- **Current Features**: Device emulation, automatic browser installation, full Playwright API support