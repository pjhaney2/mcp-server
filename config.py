import os
from typing import Dict, Any

TOOL_CONFIGS = {
    "calculator": {
        "name": "Calculator Tools",
        "description": "Basic mathematical operations",
        "tools": [
            {
                "name": "add",
                "description": "Add two numbers",
                "parameters": {
                    "a": {"type": "float", "description": "First number"},
                    "b": {"type": "float", "description": "Second number"}
                }
            },
            {
                "name": "subtract", 
                "description": "Subtract two numbers",
                "parameters": {
                    "a": {"type": "float", "description": "First number"},
                    "b": {"type": "float", "description": "Second number"}
                }
            },
            {
                "name": "multiply",
                "description": "Multiply two numbers", 
                "parameters": {
                    "a": {"type": "float", "description": "First number"},
                    "b": {"type": "float", "description": "Second number"}
                }
            },
            {
                "name": "divide",
                "description": "Divide two numbers",
                "parameters": {
                    "a": {"type": "float", "description": "Dividend"},
                    "b": {"type": "float", "description": "Divisor"}
                }
            }
        ]
    }
}

PROMPT_CONFIGS = {
    "pirate_talk": {
        "name": "Pirate Talk",
        "description": "Transform text to sound like a pirate",
        "template": """Transform the following text to sound like a pirate would speak. Use pirate vocabulary like 'ahoy', 'matey', 'arr', 'ye', 'me hearties', etc. Make it sound authentic but fun.

Text to transform: {text}

Pirate version:"""
    }
}

RESOURCE_CONFIGS = {
    "waupaca_report": {
        "name": "Waupaca Draft Report",
        "description": "City of Waupaca Draft Report PDF",
        "path": "/resources/waupaca_report.pdf",
        "type": "pdf"
    }
}

SERVER_CONFIG = {
    "name": "MCP Demo Server",
    "version": "1.0.0",
    "description": "A demonstration MCP server with tools, prompts, and resources",
    "port": int(os.getenv("PORT", 8000)),
    "host": os.getenv("HOST", "0.0.0.0")
}