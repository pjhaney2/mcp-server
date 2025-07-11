#https://educationdata.urban.org/documentation/
#https://educationdata.urban.org/documentation/colleges.html#ipeds_directory

import requests
from typing import List, Dict, Optional, Any
from datetime import datetime

def get_postsecondary_institutions(
    state_fips: Optional[List[str]] = None,
    county_fips: Optional[List[str]] = None,
    cbsa: Optional[List[str]] = None,
    year: Optional[List[str]] = None,
    inst_category: Optional[List[str]] = None,
    inst_keywords: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Get institution directory from Integrated Postsecondary Education Data System (IPEDS) data
    from National Center for Education Statistics (NCES) from 1984 to present (well, current year minus 2).
    This is the IPEDS Directory of Postsecondary Institutions.
    
    WARNING: This API endpoint can be slow (30-60+ seconds per year). For better performance, 
    limit your query to specific states and single years when possible.
    
    Args:
        state_fips: State FIPS code(s) - list of strings (e.g. ["17"] for Illinois)
        county_fips: County FIPS code(s) - can be 3-digit (e.g. ["031"]) or full 5-digit codes (e.g. ["17031"]). If 5-digit, will extract county part automatically.
        cbsa: Core Based Statistical Area code(s) (otherwise known as Metropolitan/Micropolitan Statistical Area or MSA/Micro Area) - list of strings (e.g. ["16980"] for Chicago-Naperville-Joliet, IL-IN-WI)
        year: Year(s) of data - list of strings (defaults to [current year - 2]) (e.g. ["2022"] or ["2021", "2022"])
        inst_category: Institution category code(s) - list of strings
                      "1"=Graduate only, "2"=Primarily bachelor's+, "3"=Not primarily bachelor's+, 
                      "4"=Associate's & certificates, "5"=Nondegree above bachelor's, "6"=Nondegree sub-bachelor's
        inst_keywords: Optional keyword(s) to filter institution names (case-insensitive) - list of strings
                      (e.g. ["university"] or ["college", "community"])
        
    Returns:
        List of dictionaries containing institution information with fields:
        - unitid: Institution ID
        - inst_name: Institution name
        - year: Year of data
        - state_abbr: State abbreviation
        - zip: ZIP code
        - county_fips: County FIPS code
        - county_name: County name
        - cbsa: CBSA code
        - inst_category: Institution category code
    """
    # Default to current year minus 2 if not specified
    if year is None:
        year = [str(datetime.now().year - 2)]
        
    # For single year, use original efficient approach; for multiple years, aggregate
    if len(year) == 1:
        # Single year - use original efficient approach
        single_year = year[0]
        url = f"https://educationdata.urban.org/api/v1/college-university/ipeds/directory/{single_year}/"
        params = {}
        
        # Handle API-supported parameters
        if state_fips:
            params["fips"] = ",".join(state_fips)
        
        if county_fips:
            # Handle county FIPS codes - can be 3-digit or 5-digit
            processed_county_fips = []
            for cf in county_fips:
                if len(cf) == 5:
                    # Extract county part from full FIPS (e.g., "17031" -> "031")
                    processed_county_fips.append(cf[2:])
                elif len(cf) == 3:
                    # Already county part
                    processed_county_fips.append(cf)
                else:
                    # Invalid format, skip
                    continue
            
            if processed_county_fips and state_fips:
                # Combine state and county FIPS codes
                if len(state_fips) == 1:
                    full_county_fips_list = [state_fips[0] + cf for cf in processed_county_fips]
                    params["county_fips"] = ",".join(full_county_fips_list)
                else:
                    # If multiple states, combine with first state (or handle differently if needed)
                    full_county_fips_list = [state_fips[0] + cf for cf in processed_county_fips]
                    params["county_fips"] = ",".join(full_county_fips_list)
        
        if cbsa:
            params["cbsa"] = ",".join(cbsa)
        
        if inst_category:
            params["inst_category"] = ",".join(inst_category)
        
        try:
            response = requests.get(url, params=params, timeout=30)  # Back to original timeout
            response.raise_for_status()
            data = response.json()
            results = data.get('results', [])
        except requests.exceptions.Timeout:
            return [{"error": "Request timed out - try filtering your search"}]
        except requests.exceptions.RequestException as e:
            return [{"error": f"Request failed: {str(e)}"}]
        except Exception as e:
            return [{"error": f"Unexpected error: {str(e)}"}]
    
    else:
        # Multiple years - aggregate results (slower but necessary)
        all_results = []
        
        try:
            for single_year in year:
                url = f"https://educationdata.urban.org/api/v1/college-university/ipeds/directory/{single_year}/"
                params = {}
                
                # Handle API-supported parameters (same logic as above)
                if state_fips:
                    params["fips"] = ",".join(state_fips)
                
                if county_fips:
                    processed_county_fips = []
                    for cf in county_fips:
                        if len(cf) == 5:
                            processed_county_fips.append(cf[2:])
                        elif len(cf) == 3:
                            processed_county_fips.append(cf)
                        else:
                            continue
                    
                    if processed_county_fips and state_fips:
                        if len(state_fips) == 1:
                            full_county_fips_list = [state_fips[0] + cf for cf in processed_county_fips]
                            params["county_fips"] = ",".join(full_county_fips_list)
                        else:
                            full_county_fips_list = [state_fips[0] + cf for cf in processed_county_fips]
                            params["county_fips"] = ",".join(full_county_fips_list)
                
                if cbsa:
                    params["cbsa"] = ",".join(cbsa)
                
                if inst_category:
                    params["inst_category"] = ",".join(inst_category)
                
                response = requests.get(url, params=params, timeout=60)
                response.raise_for_status()
                data = response.json()
                year_results = data.get('results', [])
                all_results.extend(year_results)
                
        except requests.exceptions.Timeout:
            return [{"error": "Request timed out - try filtering your search"}]
        except requests.exceptions.RequestException as e:
            return [{"error": f"Request failed: {str(e)}"}]
        except Exception as e:
            return [{"error": f"Unexpected error: {str(e)}"}]
        
        results = all_results
    
    # Filter by institution name keywords if specified
    if inst_keywords:
        keyword_list_lower = [k.lower() for k in inst_keywords]
        results = [inst for inst in results 
                  if any(keyword in inst.get('inst_name', '').lower() 
                        for keyword in keyword_list_lower)]
    
    return [{
        'unitid': inst.get('unitid', ''),
        'inst_name': inst.get('inst_name', ''),
        'year': inst.get('year', ''),
        'state_abbr': inst.get('state_abbr', ''),
        'zip': inst.get('zip', ''),
        'county_fips': inst.get('county_fips', ''),
        'county_name': inst.get('county_name', ''),
        'cbsa': inst.get('cbsa', ''),
        'inst_category': inst.get('inst_category', ''),
    } for inst in results]

if __name__ == "__main__":
    print(get_postsecondary_institutions(state_fips=["17"], year=["2022"]))