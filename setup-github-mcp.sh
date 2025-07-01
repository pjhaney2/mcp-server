#!/bin/bash

# Setup GitHub MCP server for Claude Code

# First, set your GitHub token if not already set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Please set your GITHUB_TOKEN environment variable first:"
    echo "export GITHUB_TOKEN='your-github-personal-access-token'"
    exit 1
fi

# Create the MCP servers configuration
MCP_CONFIG='{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "'$GITHUB_TOKEN'"
    }
  }
}'

# Add to shell profile
SHELL_PROFILE="$HOME/.zshrc"
if [ -f "$HOME/.bash_profile" ]; then
    SHELL_PROFILE="$HOME/.bash_profile"
fi

echo "" >> "$SHELL_PROFILE"
echo "# GitHub MCP Server for Claude Code" >> "$SHELL_PROFILE"
echo "export GITHUB_TOKEN='$GITHUB_TOKEN'" >> "$SHELL_PROFILE"
echo "export CLAUDE_MCP_SERVERS='$MCP_CONFIG'" >> "$SHELL_PROFILE"

echo "GitHub MCP server configuration added to $SHELL_PROFILE"
echo "Please run: source $SHELL_PROFILE"
echo "Then restart Claude Code for the changes to take effect"