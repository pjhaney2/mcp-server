#!/bin/bash

echo "=== GitHub MCP Configuration Fix ==="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if GitHub token is provided as argument
if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage: ./fix_github_mcp.sh YOUR_GITHUB_TOKEN${NC}"
    echo ""
    echo "To create a GitHub personal access token:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. Give it a descriptive name (e.g., 'Claude MCP')"
    echo "4. Select scopes: repo, read:org, read:user"
    echo "5. Generate token and copy it"
    echo ""
    exit 1
fi

GITHUB_TOKEN="$1"
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Create backup of existing config if it exists and has content
if [ -f "$CLAUDE_CONFIG" ] && [ -s "$CLAUDE_CONFIG" ]; then
    cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "${GREEN}✅ Backed up existing config${NC}"
fi

# Create the configuration
cat > "$CLAUDE_CONFIG" << EOF
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    },
    "mcp-demo-server": {
      "command": "python",
      "args": ["server.py", "--stdio"],
      "cwd": "/Users/peterhaney/code/mcp-server"
    }
  }
}
EOF

echo -e "${GREEN}✅ Updated Claude configuration${NC}"

# Verify the configuration
echo ""
echo "Configuration saved to: $CLAUDE_CONFIG"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Quit Claude Desktop completely (Cmd+Q)"
echo "2. Restart Claude Desktop"
echo "3. Look for the GitHub icon in the MCP section"
echo ""
echo -e "${GREEN}The GitHub MCP server should now be available!${NC}"
echo ""
echo "Available MCP servers in your configuration:"
echo "- GitHub (with your personal access token)"
echo "- Playwright (browser automation)"
echo "- MCP Demo Server (calculator, pirate talk)"