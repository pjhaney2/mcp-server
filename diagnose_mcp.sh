#!/bin/bash

echo "=== MCP Configuration Diagnostic ==="
echo ""

# Check for GitHub token
echo "1. GitHub Token Status:"
if [ -z "$GITHUB_TOKEN" ]; then
    echo "   ❌ GITHUB_TOKEN not set in environment"
    echo "   ℹ️  GitHub MCP requires a personal access token"
else
    echo "   ✅ GITHUB_TOKEN is set"
fi
echo ""

# Check for GITHUB_PERSONAL_ACCESS_TOKEN (alternative name)
echo "2. Alternative Token Check:"
if [ -z "$GITHUB_PERSONAL_ACCESS_TOKEN" ]; then
    echo "   ❌ GITHUB_PERSONAL_ACCESS_TOKEN not set"
else
    echo "   ✅ GITHUB_PERSONAL_ACCESS_TOKEN is set"
fi
echo ""

# Check Claude MCP environment variable
echo "3. Claude MCP Servers Environment Variable:"
if [ -z "$CLAUDE_MCP_SERVERS" ]; then
    echo "   ❌ CLAUDE_MCP_SERVERS not set"
else
    echo "   ✅ CLAUDE_MCP_SERVERS is set"
    echo "   Content: $CLAUDE_MCP_SERVERS" | head -c 200
    echo "..."
fi
echo ""

# Check npm installation
echo "4. NPM Package Installation:"
if npm list -g @modelcontextprotocol/server-github 2>/dev/null | grep -q "@modelcontextprotocol/server-github"; then
    echo "   ✅ GitHub MCP server is installed globally"
    npm list -g @modelcontextprotocol/server-github 2>/dev/null | grep "@modelcontextprotocol/server-github"
else
    echo "   ❌ GitHub MCP server not installed globally"
fi
echo ""

# Check if npx can find the package
echo "5. NPX Availability Test:"
if npx --no-install @modelcontextprotocol/server-github --help 2>/dev/null | grep -q "GitHub"; then
    echo "   ✅ GitHub MCP server is accessible via npx"
else
    echo "   ❌ GitHub MCP server not accessible via npx"
    echo "   Try: npx -y @modelcontextprotocol/server-github"
fi
echo ""

# Check Claude desktop config
echo "6. Claude Desktop Configuration:"
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
if [ -f "$CLAUDE_CONFIG" ]; then
    echo "   ✅ Claude config file exists"
    if [ -s "$CLAUDE_CONFIG" ]; then
        echo "   ✅ Config file has content"
        echo "   Preview:"
        cat "$CLAUDE_CONFIG" | python3 -m json.tool 2>/dev/null | head -20 || echo "   ⚠️  Invalid JSON format"
    else
        echo "   ❌ Config file is empty"
    fi
else
    echo "   ❌ Claude config file not found"
fi
echo ""

# Test GitHub MCP server directly
echo "7. Direct GitHub MCP Server Test:"
echo "   Testing server startup..."
timeout 5s npx -y @modelcontextprotocol/server-github 2>&1 | head -10
echo ""

# Suggest configuration
echo "=== Suggested Configuration ==="
echo ""
echo "Add this to your Claude Desktop config file:"
echo "Location: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
cat << 'EOF'
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-github-token-here"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
EOF
echo ""
echo "Replace 'your-github-token-here' with your actual GitHub personal access token"
echo ""
echo "=== Next Steps ==="
echo "1. Create a GitHub personal access token at: https://github.com/settings/tokens"
echo "2. Update the Claude config file with the configuration above"
echo "3. Restart Claude Desktop application"
echo "4. The GitHub MCP server should appear in Claude's MCP section"