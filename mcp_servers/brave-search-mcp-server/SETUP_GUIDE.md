# Brave Search MCP Server Setup Guide

## Overview
The Brave Search MCP Server has been successfully installed and configured in your project.

## Installation Summary
- **Repository**: https://github.com/brave/brave-search-mcp-server
- **Version**: 2.0.75
- **Location**: `mcp_servers/brave-search-mcp-server/`
- **Config File**: `.vscode/cline_mcp_settings.json`

## Getting Your Brave API Key

### Steps:
1. Visit [Brave Search API](https://brave.com/search/api/)
2. Sign up for an account (free plan available with 2,000 queries/month)
3. Navigate to [Developer Dashboard](https://api-dashboard.search.brave.com/app/keys)
4. Generate your API key

### Plans:
- **Free Plan**: 2,000 queries/month, basic web search
- **Pro Plan**: Enhanced features including local search, AI summaries, extra snippets

## Configuration

### Update Your API Key
Edit `.vscode/cline_mcp_settings.json` and replace `YOUR_BRAVE_API_KEY_HERE` with your actual API key:

```json
{
  "mcpServers": {
    "github.com/brave/brave-search-mcp-server": {
      "command": "node",
      "args": [
        "mcp_servers/brave-search-mcp-server/dist/index.js"
      ],
      "env": {
        "BRAVE_API_KEY": "YOUR_ACTUAL_BRAVE_API_KEY_HERE"
      }
    }
  }
}
```

### Environment Variable (Alternative)
You can also set the BRAVE_API_KEY as a system environment variable instead of putting it in the configuration file.

## Available Tools

Once configured, you'll have access to the following MCP tools:

### 1. `brave_web_search`
Perform comprehensive web searches with rich result types and advanced filtering.

**Parameters:**
- `query` (required): Search terms
- `count`: Results per page (1-20, default: 10)
- `country`: Country code (default: "US")
- `search_lang`: Search language (default: "en")
- `safesearch`: Content filtering ("off", "moderate", "strict")
- `freshness`: Time filter ("pd", "pw", "pm", "py")
- `summary`: Enable summary key for AI summarization

### 2. `brave_local_search`
Search for local businesses and places with ratings, hours, and AI descriptions.

### 3. `brave_image_search`
Search for images with thumbnail information.

### 4. `brave_video_search`
Search for videos with comprehensive metadata.

### 5. `brave_news_search`
Search for current news articles with freshness controls.

### 6. `brave_summarizer`
Generate AI-powered summaries from web search results.

## Usage Examples

### Basic Web Search
```
Use the brave_web_search tool with query "latest AI developments"
```

### Image Search
```
Use the brave_image_search tool with query "machine learning diagrams"
```

### News Search
```
Use the brave_news_search tool with query "technology news today"
```

### AI Summary
1. First perform a web search with `summary: true`
2. Then use the returned summary key with `brave_summarizer`

## Testing the Server

To verify the server is working correctly:

1. Update your API key in `.vscode/cline_mcp_settings.json`
2. Reload VS Code or restart Cline
3. Try a simple web search command

## Troubleshooting

### Server not responding
- Ensure Node.js is installed and accessible
- Check that the path `mcp_servers/brave-search-mcp-server/dist/index.js` exists
- Verify your BRAVE_API_KEY is correct

### API errors
- Check your Brave API key hasn't expired
- Verify you haven't exceeded your query limit
- Check the [Brave API Dashboard](https://api-dashboard.search.brave.com/app/keys)

## Additional Resources

- [Brave Search API Documentation](https://api.search.brave.com/app/documentation)
- [MCP Server GitHub Repository](https://github.com/brave/brave-search-mcp-server)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Notes
- The server uses STDIO transport by default (recommended)
- No Docker required - running directly with Node.js
- All dependencies are installed and the project is built
- Configuration uses relative paths for portability