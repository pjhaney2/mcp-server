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
                    "geo_fips": {"type": "array", "items": {"type": "string"}, "description": "County FIPS code(s). Array of strings (e.g., ['031'] for single county or ['031', '045'] for multiple counties)"}, 
                    "state_fips": {"type": "string", "description": "State FIPS code(s) as a STRING. Use '17' for single state or '17,06' for multiple states (comma-separated, no spaces, NO ARRAYS)"},
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
                    "geo_fips": {"type": "array", "items": {"type": "string"}, "description": "County FIPS code(s). Array of strings (e.g., ['031'] for single county or ['031', '045'] for multiple counties)"}, 
                    "state_fips": {"type": "string", "description": "State FIPS code(s) as a STRING. Use '17' for single state or '17,06' for multiple states (comma-separated, no spaces, NO ARRAYS)"},
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
                    "geo_fips": {"type": "array", "items": {"type": "string"}, "description": "County FIPS code(s). Array of strings (e.g., ['031'] for single county or ['031', '045'] for multiple counties)"}, 
                    "state_fips": {"type": "string", "description": "State FIPS code(s) as a STRING. Use '17' for single state or '17,06' for multiple states (comma-separated, no spaces, NO ARRAYS)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "county_fips_search": {
        "name": "County FIPS Search",
        "description": "Search for US county FIPS codes by county name keyword(s)",
        "tools": [
            {
                "name": "search_county_fips",
                "description": "Search for counties by keyword(s) and return their FIPS codes",
                "parameters": {
                    "keyword": {"type": "array", "items": {"type": "string"}, "description": "Search term(s) to match against county names (case-insensitive). Array of strings (e.g., ['cook', 'dupage']) for multiple searches, or single string ['cook'] for one search"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return (default: 20)", "optional": True}
                }
            }
        ]
    },
    "place_fips_search": {
        "name": "Place FIPS Search",
        "description": "Search for US place FIPS codes by place name keyword(s)",
        "tools": [
            {
                "name": "search_place_fips",
                "description": "Search for places (cities, towns, CDPs) by keyword(s) and return their FIPS codes",
                "parameters": {
                    "keyword": {"type": "array", "items": {"type": "string"}, "description": "Search term(s) to match against place names (case-insensitive). Array of strings (e.g., ['chicago', 'milwaukee']) for multiple searches, or single string ['chicago'] for one search"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return (default: 20)", "optional": True}
                }
            }
        ]
    },
    "msa_fips_search": {
        "name": "MSA FIPS Search",
        "description": "Search for US MSA/Micropolitan area FIPS codes by area name keyword(s)",
        "tools": [
            {
                "name": "search_msa_fips",
                "description": "Search for MSA/Micropolitan areas by keyword(s) and return their FIPS codes",
                "parameters": {
                    "keyword": {"type": "array", "items": {"type": "string"}, "description": "Search term(s) to match against MSA/Micropolitan area names (case-insensitive). Array of strings (e.g., ['chicago', 'milwaukee']) for multiple searches, or single string ['chicago'] for one search"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return (default: 20)", "optional": True}
                }
            }
        ]
    },
    "state_fips_search": {
        "name": "State FIPS Search",
        "description": "Search for US state FIPS codes by state name keyword(s)",
        "tools": [
            {
                "name": "search_state_fips",
                "description": "Search for states by keyword(s) and return their FIPS codes",
                "parameters": {
                    "keyword": {"type": "array", "items": {"type": "string"}, "description": "Search term(s) to match against state names (case-insensitive). Array of strings (e.g., ['california', 'texas']) for multiple searches, or single string ['california'] for one search"},
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
                    "place_fips": {"type": "array", "items": {"type": "string"}, "description": "Place FIPS code(s). Array of strings (e.g., ['14000'] for single place or ['14000', '51000'] for multiple places)"}, 
                    "state_fips": {"type": "string", "description": "State FIPS code(s) as a STRING. Use '17' for single state or '17,06' for multiple states (comma-separated, no spaces, NO ARRAYS)"},
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
                    "place_fips": {"type": "array", "items": {"type": "string"}, "description": "Place FIPS code(s). Array of strings (e.g., ['14000'] for single place or ['14000', '51000'] for multiple places)"}, 
                    "state_fips": {"type": "string", "description": "State FIPS code(s) as a STRING. Use '17' for single state or '17,06' for multiple states (comma-separated, no spaces, NO ARRAYS)"},
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
                    "place_fips": {"type": "array", "items": {"type": "string"}, "description": "Place FIPS code(s). Array of strings (e.g., ['14000'] for single place or ['14000', '51000'] for multiple places)"}, 
                    "state_fips": {"type": "string", "description": "State FIPS code(s) as a STRING. Use '17' for single state or '17,06' for multiple states (comma-separated, no spaces, NO ARRAYS)"},
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
                    "msa_fips": {"type": "array", "items": {"type": "string"}, "description": "MSA/Micropolitan area FIPS code(s). Array of strings (e.g., ['16980'] for single area or ['16980', '35620'] for multiple areas)"}, 
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
                    "msa_fips": {"type": "array", "items": {"type": "string"}, "description": "MSA/Micropolitan area FIPS code(s). Array of strings (e.g., ['16980'] for single area or ['16980', '35620'] for multiple areas)"}, 
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
                    "msa_fips": {"type": "array", "items": {"type": "string"}, "description": "MSA/Micropolitan area FIPS code(s). Array of strings (e.g., ['16980'] for single area or ['16980', '35620'] for multiple areas)"}, 
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
                    "state_fips": {"type": "array", "items": {"type": "string"}, "description": "State FIPS code(s). Array of strings (e.g., ['17'] for single state or ['17', '06'] for multiple states)"}, 
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
                    "state_fips": {"type": "array", "items": {"type": "string"}, "description": "State FIPS code(s). Array of strings (e.g., ['17'] for single state or ['17', '06'] for multiple states)"}, 
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
                    "state_fips": {"type": "array", "items": {"type": "string"}, "description": "State FIPS code(s). Array of strings (e.g., ['17'] for single state or ['17', '06'] for multiple states)"}, 
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
    },
    "acs_demographics_county": {
        "name": "ACS Demographics County Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for county-level demographic characteristics",
        "tools": [
            {
                "name": "acs_demographics_county_pull",
                "description": "Pulls county-level demographic data including total population, sex (male/female distribution), age distribution, race, and voting age population",
                "parameters": {
                    "geo_fips": {"type": "array", "items": {"type": "string"}, "description": "County FIPS code(s). Array of strings (e.g., ['031'] for single county or ['031', '045'] for multiple counties)"}, 
                    "state_fips": {"type": "string", "description": "State FIPS code(s) as a STRING. Use '17' for single state or '17,06' for multiple states (comma-separated, no spaces, NO ARRAYS)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_demographics_place": {
        "name": "ACS Demographics Place Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for place-level demographic characteristics",
        "tools": [
            {
                "name": "acs_demographics_place_pull",
                "description": "Pulls place-level demographic data including total population, sex (male/female distribution), age distribution, race, and voting age population",
                "parameters": {
                    "place_fips": {"type": "array", "items": {"type": "string"}, "description": "Place FIPS code(s). Array of strings (e.g., ['14000'] for single place or ['14000', '51000'] for multiple places)"}, 
                    "state_fips": {"type": "string", "description": "State FIPS code(s) as a STRING. Use '17' for single state or '17,06' for multiple states (comma-separated, no spaces, NO ARRAYS)"},
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_demographics_msa": {
        "name": "ACS Demographics MSA Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for MSA/Micropolitan area-level demographic characteristics",
        "tools": [
            {
                "name": "acs_demographics_msa_pull",
                "description": "Pulls MSA/Micropolitan area-level demographic data including total population, sex (male/female distribution), age distribution, race, and voting age population",
                "parameters": {
                    "msa_fips": {"type": "array", "items": {"type": "string"}, "description": "MSA/Micropolitan area FIPS code(s). Array of strings (e.g., ['16980'] for single area or ['16980', '35620'] for multiple areas)"}, 
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_demographics_state": {
        "name": "ACS Demographics State Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for state-level demographic characteristics",
        "tools": [
            {
                "name": "acs_demographics_state_pull",
                "description": "Pulls state-level demographic data including total population, sex (male/female distribution), age distribution, race, and voting age population",
                "parameters": {
                    "state_fips": {"type": "array", "items": {"type": "string"}, "description": "State FIPS code(s). Array of strings (e.g., ['17'] for single state or ['17', '06'] for multiple states)"}, 
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "acs_demographics_national": {
        "name": "ACS Demographics National Data",
        "description": "Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates for national-level demographic characteristics",
        "tools": [
            {
                "name": "acs_demographics_national_pull",
                "description": "Pulls national-level demographic data including total population, sex (male/female distribution), age distribution, race, and voting age population",
                "parameters": {
                    "year": {"type": "string", "description": "Year for data (optional, defaults to most recent available)", "optional": True}
                }
            }
        ]
    },
    "oews_data": {
        "name": "OEWS Employment and Wage Data",
        "description": "Get occupation employment and wage statistics from the Bureau of Labor Statistics OEWS program with location quotients",
        "tools": [
            {
                "name": "get_oews_data",
                "description": "Get simplified OEWS occupation and wage data for multiple locations and occupations with location quotients",
                "parameters": {
                    "geo_codes": {"type": "array", "items": {"type": "string"}, "description": "Geographic area codes (e.g., ['0600000'] for California, ['0000000'] for national, ['0016980'] for Chicago metro). Array of strings for multiple locations"},
                    "occ_codes": {"type": "array", "items": {"type": "string"}, "description": "SOC occupation codes (e.g., ['111011'] for Chief Executives, ['151252'] for Software Developers). Array of strings for multiple occupations"}
                }
            }
        ]
    },
    "oews_fips_search": {
        "name": "OEWS Geographic Area Search",
        "description": "Search for OEWS geographic area FIPS codes by area name keyword(s)",
        "tools": [
            {
                "name": "search_oews_fips",
                "description": "Search for OEWS geographic areas by keyword(s) and return their FIPS codes",
                "parameters": {
                    "keyword": {"type": "array", "items": {"type": "string"}, "description": "Search term(s) to match against area names (case-insensitive). Array of strings (e.g., ['california', 'texas']) for multiple searches, or single string ['california'] for one search"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return (default: 20)", "optional": True}
                }
            }
        ]
    },
    "oews_soc_search": {
        "name": "OEWS Occupation Search",
        "description": "Search for SOC occupation codes by occupation title keyword(s)",
        "tools": [
            {
                "name": "search_oews_soc",
                "description": "Search for occupations by keyword(s) and return their SOC codes",
                "parameters": {
                    "keyword": {"type": "array", "items": {"type": "string"}, "description": "Search term(s) to match against occupation titles (case-insensitive). Array of strings (e.g., ['software', 'manager']) for multiple searches, or single string ['software'] for one search"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return (default: 20)", "optional": True}
                }
            }
        ]
    },
    "qcew_data": {
        "name": "QCEW Employment and Establishment Data",
        "description": "Get industry employment and establishment statistics from the Bureau of Labor Statistics QCEW program with location quotients",
        "tools": [
            {
                "name": "get_qcew_data",
                "description": "Get simplified QCEW industry establishment and employee data for multiple locations and industries with location quotients",
                "parameters": {
                    "geo_codes": {"type": "array", "items": {"type": "string"}, "description": "Geographic area codes (e.g., ['17043'] for DuPage County IL, ['US000'] for national, ['06'] for California state). Array of strings for multiple locations"},
                    "industry_codes": {"type": "array", "items": {"type": "string"}, "description": "NAICS industry codes (e.g., ['1013'] for Manufacturing, ['10'] for Total All Industries). Array of strings for multiple industries"},
                    "year": {"type": "string", "description": "Specific year for historical data (optional, defaults to latest available)", "optional": True}
                }
            }
        ]
    },
    "qcew_fips_search": {
        "name": "QCEW Geographic Area Search",
        "description": "Search for QCEW geographic area FIPS codes by area name keyword(s)",
        "tools": [
            {
                "name": "search_qcew_fips",
                "description": "Search for QCEW geographic areas by keyword(s) and return their FIPS codes",
                "parameters": {
                    "keyword": {"type": "array", "items": {"type": "string"}, "description": "Search term(s) to match against area names (case-insensitive). Array of strings (e.g., ['chicago', 'illinois']) for multiple searches, or single string ['chicago'] for one search"},
                    "max_results": {"type": "integer", "description": "Maximum number of results to return (default: 20)", "optional": True}
                }
            }
        ]
    },
    "qcew_naics_search": {
        "name": "QCEW Industry Search",
        "description": "Search for NAICS industry codes by industry name keyword(s)",
        "tools": [
            {
                "name": "search_qcew_naics",
                "description": "Search for industries by keyword(s) and return their NAICS codes",
                "parameters": {
                    "keyword": {"type": "array", "items": {"type": "string"}, "description": "Search term(s) to match against industry names (case-insensitive). Array of strings (e.g., ['manufacturing', 'retail']) for multiple searches, or single string ['manufacturing'] for one search"}
                }
            }
        ]
    },
    "rank_acs_data_high": {
        "name": "Rank ACS Data High",
        "description": "Find geographic areas with the highest values for a specific ACS data point",
        "tools": [
            {
                "name": "rank_acs_data_high",
                "description": "Find geographic areas (places, counties, states, MSAs) with the highest values for a specified ACS data point",
                "parameters": {
                    "data_point": {"type": "string", "description": "The ACS data point/variable to sort by (e.g., 'DP02_0001E', 'DP03_0062E')"},
                    "geo_type": {"type": "string", "description": "The geographic type to query ('place', 'county', 'state', 'metropolitan statistical area/micropolitan statistical area')"},
                    "state_fips": {"type": "string", "description": "The FIPS code for the state to limit results to. If not provided, queries all areas. Note: Not applicable for MSA queries.", "optional": True},
                    "year": {"type": "string", "description": "Year of ACS data (optional, defaults to most recent available)", "optional": True},
                    "limit": {"type": "integer", "description": "Number of top results to return (default: 20, max: 100)", "optional": True}
                }
            }
        ]
    },
    "rank_acs_data_low": {
        "name": "Rank ACS Data Low",
        "description": "Find geographic areas with the lowest values for a specific ACS data point",
        "tools": [
            {
                "name": "rank_acs_data_low", 
                "description": "Find geographic areas (places, counties, states, MSAs) with the lowest values for a specified ACS data point",
                "parameters": {
                    "data_point": {"type": "string", "description": "The ACS data point/variable to sort by (e.g., 'DP02_0001E', 'DP03_0062E')"},
                    "geo_type": {"type": "string", "description": "The geographic type to query ('place', 'county', 'state', 'metropolitan statistical area/micropolitan statistical area')"},
                    "state_fips": {"type": "string", "description": "The FIPS code for the state to limit results to. If not provided, queries all areas. Note: Not applicable for MSA queries.", "optional": True},
                    "year": {"type": "string", "description": "Year of ACS data (optional, defaults to most recent available)", "optional": True},
                    "limit": {"type": "integer", "description": "Number of lowest results to return (default: 20, max: 100)", "optional": True}
                }
            }
        ]
    },
    "eia_elec_rates": {
        "name": "EIA Electricity Rates",
        "description": "Get electricity rates by zipcode from investor-owned and non-investor-owned utilities",
        "tools": [
            {
                "name": "get_electricity_rates",
                "description": "Fetch electricity rates for specified zipcodes from IOU and non-IOU utilities",
                "parameters": {
                    "zipcodes": {"type": "array", "items": {"type": "string"}, "description": "List of zipcode strings to filter for (e.g., ['60067', '60622'] for multiple zipcodes)"}
                }
            }
        ]
    },
    "ipeds_institution_directory": {
        "name": "IPEDS Institution Directory",
        "description": "Get postsecondary institution directory data from IPEDS with filtering by location, category, and keywords",
        "tools": [
            {
                "name": "get_postsecondary_institutions",
                "description": "Get institution directory from Integrated Postsecondary Education Data System (IPEDS) data",
                "parameters": {
                    "state_fips": {"type": "array", "items": {"type": "string"}, "description": "State FIPS code(s). Array of strings (e.g., ['17'] for Illinois or ['17', '06'] for Illinois and California)"},
                    "county_fips": {"type": "array", "items": {"type": "string"}, "description": "County FIPS code(s) - can be 3-digit (e.g., ['031']) or full 5-digit codes (e.g., ['17031']). Array of strings (optional)"},
                    "cbsa": {"type": "array", "items": {"type": "string"}, "description": "Core Based Statistical Area code(s). Array of strings (e.g., ['16980'] for Chicago metro) (optional)"},
                    "year": {"type": "integer", "description": "Year of data (defaults to current year - 2)", "optional": True},
                    "inst_category": {"type": "array", "items": {"type": "integer"}, "description": "Institution category code(s). Array of integers: 1=Graduate only, 2=Primarily bachelor's+, 3=Not primarily bachelor's+, 4=Associate's & certificates, 5=Nondegree above bachelor's, 6=Nondegree sub-bachelor's (optional)"},
                    "inst_keywords": {"type": "array", "items": {"type": "string"}, "description": "Optional keyword(s) to filter institution names (case-insensitive). Array of strings (e.g., ['university'] or ['college', 'community']) (optional)"}
                }
            }
        ]
    },
    "ipeds_program_data": {
        "name": "IPEDS Program Completion Data",
        "description": "Get program completion data from IPEDS with filtering by location, award levels, and CIP code keywords",
        "tools": [
            {
                "name": "get_programs",
                "description": "Get program completion data from Integrated Postsecondary Education Data System (IPEDS) data",
                "parameters": {
                    "state_fips": {"type": "array", "items": {"type": "string"}, "description": "State FIPS code(s). Array of strings (e.g., ['17'] for Illinois or ['17', '06'] for Illinois and California)"},
                    "year": {"type": "integer", "description": "Year of data (defaults to current year - 3)", "optional": True},
                    "award_levels": {"type": "array", "items": {"type": "integer"}, "description": "Award level code(s). Array of integers (defaults to [4, 7, 9, 22, 23, 24] for Associate's, Bachelor's, Master's, and Doctoral degrees). 4=Associate's, 7=Bachelor's, 9=Master's, 22=Doctor's research, 23=Doctor's professional, 24=Doctor's other (optional)"},
                    "cip_keywords": {"type": "array", "items": {"type": "string"}, "description": "Optional keyword(s) to filter CIP code descriptions (case-insensitive). Array of strings (e.g., ['engineering'] or ['computer', 'technology']) (optional)"}
                }
            }
        ]
    },
    "ipeds_cip_codes": {
        "name": "IPEDS CIP Code Lookup",
        "description": "Look up Classification of Instructional Programs (CIP) codes and descriptions",
        "tools": [
            {
                "name": "get_cip_codes",
                "description": "Get CIP code information from IPEDS data",
                "parameters": {
                    "search_term": {"type": "string", "description": "Optional search term to filter CIP code names (case-insensitive)", "optional": True},
                    "cip_codes": {"type": "array", "items": {"type": "string"}, "description": "Optional CIP code(s) to look up specific codes. Array of strings (optional)"}
                }
            }
        ]
    },
    "ipeds_award_levels": {
        "name": "IPEDS Award Level Lookup",
        "description": "Look up IPEDS award level codes and descriptions",
        "tools": [
            {
                "name": "get_award_levels",
                "description": "Get award level information from IPEDS data",
                "parameters": {
                    "search_term": {"type": "string", "description": "Optional search term to filter award level names (case-insensitive)", "optional": True},
                    "award_level_codes": {"type": "array", "items": {"type": "string"}, "description": "Optional award level code(s) to look up specific levels. Array of strings (optional)"}
                }
            }
        ]
    },
    "cre_county": {
        "name": "CRE County Data",
        "description": "Community Resilience Estimates (CRE) county-level data from the US Census Bureau measuring social vulnerability to disasters",
        "tools": [
            {
                "name": "get_cre_county_data",
                "description": "Pulls county-level Community Resilience Estimates (CRE) data measuring social vulnerability to disasters using 10 risk factors",
                "parameters": {
                    "geo_fips": {"type": "array", "items": {"type": "string"}, "description": "County FIPS code(s). Array of strings (e.g., ['031'] for single county or ['031', '045'] for multiple counties)"},
                    "state_fips": {"type": "string", "description": "State FIPS code as a string (e.g., '17' for Illinois)"},
                    "year": {"type": "string", "description": "Year of CRE data. Available years: 2019, 2021, 2022, 2023 (defaults to 2023)", "optional": True}
                }
            }
        ]
    },
    "cre_state": {
        "name": "CRE State Data", 
        "description": "Community Resilience Estimates (CRE) state-level data from the US Census Bureau measuring social vulnerability to disasters",
        "tools": [
            {
                "name": "get_cre_state_data",
                "description": "Pulls state-level Community Resilience Estimates (CRE) data measuring social vulnerability to disasters using 10 risk factors",
                "parameters": {
                    "state_fips": {"type": "array", "items": {"type": "string"}, "description": "State FIPS code(s). Array of strings (e.g., ['17'] for single state or ['17', '26'] for multiple states)"},
                    "year": {"type": "string", "description": "Year of CRE data. Available years: 2019, 2021, 2022, 2023 (defaults to 2023)", "optional": True}
                }
            }
        ]
    }
}

PROMPT_CONFIGS = {
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