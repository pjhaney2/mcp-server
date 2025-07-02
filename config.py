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
    },
    "acs_social_county": {
        "name": "ACS Social County Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for county-level social characteristics",
        "tools": [
            {
                "name": "acs_social_county_pull",
                "description": "Pulls county-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "geo_fips": {"type": "string", "description": "County FIPS code (3 digits)"},
                    "state_fips": {"type": "string", "description": "State FIPS code (2 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_economic_county": {
        "name": "ACS Economic County Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for county-level economic characteristics",
        "tools": [
            {
                "name": "acs_economic_county_pull",
                "description": "Pulls county-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "geo_fips": {"type": "string", "description": "County FIPS code (3 digits)"},
                    "state_fips": {"type": "string", "description": "State FIPS code (2 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_housing_county": {
        "name": "ACS Housing County Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for county-level housing characteristics",
        "tools": [
            {
                "name": "acs_housing_county_pull",
                "description": "Pulls county-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "geo_fips": {"type": "string", "description": "County FIPS code (3 digits)"},
                    "state_fips": {"type": "string", "description": "State FIPS code (2 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "county_fips_search": {
        "name": "County FIPS Search",
        "description": "Search for US county FIPS codes by county name keyword",
        "tools": [
            {
                "name": "search_county_fips",
                "description": "Search for counties by keyword and return their FIPS codes",
                "parameters": {
                    "keyword": {"type": "string", "description": "Search term to match against county names (case-insensitive)"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return (default: 20)", "optional": True}
                }
            }
        ]
    },
    "place_fips_search": {
        "name": "Place FIPS Search",
        "description": "Search for US place FIPS codes by place name keyword",
        "tools": [
            {
                "name": "search_place_fips",
                "description": "Search for places (cities, towns, CDPs) by keyword and return their FIPS codes",
                "parameters": {
                    "keyword": {"type": "string", "description": "Search term to match against place names (case-insensitive)"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return (default: 20)", "optional": True}
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