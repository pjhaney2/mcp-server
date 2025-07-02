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
    },
    "msa_fips_search": {
        "name": "MSA FIPS Search",
        "description": "Search for US MSA/Micropolitan area FIPS codes by area name keyword",
        "tools": [
            {
                "name": "search_msa_fips",
                "description": "Search for MSA/Micropolitan areas by keyword and return their FIPS codes",
                "parameters": {
                    "keyword": {"type": "string", "description": "Search term to match against MSA/Micropolitan area names (case-insensitive)"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return (default: 20)", "optional": True}
                }
            }
        ]
    },
    "state_fips_search": {
        "name": "State FIPS Search",
        "description": "Search for US state FIPS codes by state name keyword",
        "tools": [
            {
                "name": "search_state_fips",
                "description": "Search for states by keyword and return their FIPS codes",
                "parameters": {
                    "keyword": {"type": "string", "description": "Search term to match against state names (case-insensitive)"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return (default: 20)", "optional": True}
                }
            }
        ]
    },
    "acs_social_place": {
        "name": "ACS Social Place Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for place-level social characteristics",
        "tools": [
            {
                "name": "acs_social_place_pull",
                "description": "Pulls place-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "place_fips": {"type": "string", "description": "Place FIPS code (5 digits)"},
                    "state_fips": {"type": "string", "description": "State FIPS code (2 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_economic_place": {
        "name": "ACS Economic Place Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for place-level economic characteristics",
        "tools": [
            {
                "name": "acs_economic_place_pull",
                "description": "Pulls place-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "place_fips": {"type": "string", "description": "Place FIPS code (5 digits)"},
                    "state_fips": {"type": "string", "description": "State FIPS code (2 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_housing_place": {
        "name": "ACS Housing Place Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for place-level housing characteristics",
        "tools": [
            {
                "name": "acs_housing_place_pull",
                "description": "Pulls place-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "place_fips": {"type": "string", "description": "Place FIPS code (5 digits)"},
                    "state_fips": {"type": "string", "description": "State FIPS code (2 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_social_msa": {
        "name": "ACS Social MSA Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for MSA/Micropolitan area-level social characteristics",
        "tools": [
            {
                "name": "acs_social_msa_pull",
                "description": "Pulls MSA/Micropolitan area-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "msa_fips": {"type": "string", "description": "MSA/Micropolitan area FIPS code (5 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_economic_msa": {
        "name": "ACS Economic MSA Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for MSA/Micropolitan area-level economic characteristics",
        "tools": [
            {
                "name": "acs_economic_msa_pull",
                "description": "Pulls MSA/Micropolitan area-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "msa_fips": {"type": "string", "description": "MSA/Micropolitan area FIPS code (5 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_housing_msa": {
        "name": "ACS Housing MSA Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for MSA/Micropolitan area-level housing characteristics",
        "tools": [
            {
                "name": "acs_housing_msa_pull",
                "description": "Pulls MSA/Micropolitan area-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "msa_fips": {"type": "string", "description": "MSA/Micropolitan area FIPS code (5 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_social_state": {
        "name": "ACS Social State Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for state-level social characteristics",
        "tools": [
            {
                "name": "acs_social_state_pull",
                "description": "Pulls state-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "state_fips": {"type": "string", "description": "State FIPS code (2 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_economic_state": {
        "name": "ACS Economic State Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for state-level economic characteristics",
        "tools": [
            {
                "name": "acs_economic_state_pull",
                "description": "Pulls state-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "state_fips": {"type": "string", "description": "State FIPS code (2 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_housing_state": {
        "name": "ACS Housing State Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for state-level housing characteristics",
        "tools": [
            {
                "name": "acs_housing_state_pull",
                "description": "Pulls state-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "state_fips": {"type": "string", "description": "State FIPS code (2 digits)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_social_national": {
        "name": "ACS Social National Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for national-level social characteristics",
        "tools": [
            {
                "name": "acs_social_national_pull",
                "description": "Pulls national-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_economic_national": {
        "name": "ACS Economic National Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for national-level economic characteristics",
        "tools": [
            {
                "name": "acs_economic_national_pull",
                "description": "Pulls national-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_housing_national": {
        "name": "ACS Housing National Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for national-level housing characteristics",
        "tools": [
            {
                "name": "acs_housing_national_pull",
                "description": "Pulls national-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates",
                "parameters": {
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
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