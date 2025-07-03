from datetime import datetime
from typing import Dict, Optional, Union, Any, List
import requests

def acs_demographics_msa_pull(
    msa_fips: List[str], 
    year: Optional[str] = None
) -> Dict[str, Any]:
    """
    Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates.
    
    This function is restricted to MSA/Micropolitan area-level demographic data (DP05 profile only).
    This includes data for total population, sex (male/female distribution), age distribution, 
    race, and voting age population.

    Args:
        msa_fips (List[str]): The FIPS code(s) for the MSA/Micropolitan area(s). 
                              List of strings (e.g., ["16980"] or ["16980", "35620"])
        year (Optional[str]): Year of ACS data. Defaults to current year minus 2. Must be 2010 or later.

    Returns:
        Dict[str, Any]: Response containing:
            - status: "success" or "error"
            - data: JSON response with ACS data (if successful)
            - error_message: Error details (if unsuccessful)
    """
    try:
        def _error_response(message: str) -> Dict[str, str]:
            return {"status": "error", "error_message": message}

        # Validate inputs
        
        # Handle msa_fips as list
        if not isinstance(msa_fips, list):
            return _error_response("msa_fips must be a list of strings.")
        
        msa_fips_list = msa_fips
        
        # Validate all msa_fips codes
        for fips in msa_fips_list:
            if not isinstance(fips, str) or not fips.isdigit():
                return _error_response("All msa_fips must be strings of digits.")

        # Handle year parameter and validate
        if year is not None:
            try:
                year_int = int(year)
                if year_int < 2010:
                    return _error_response("Year must be 2010 or later.")
                if year_int > datetime.now().year:
                    return _error_response(f"Year cannot be in the future. Current year is {datetime.now().year}.")
                target_year = year
            except (ValueError, TypeError):
                return _error_response("Year must be a valid integer string.")
        else:
            target_year = str(datetime.now().year - 2)
        
        # Create comma-separated string for multiple FIPS codes
        msa_fips_str = ",".join(msa_fips_list)
        
        params = {
            "get": f"NAME,group(DP05)",
            "for": f"metropolitan statistical area/micropolitan statistical area:{msa_fips_str}",
            "key":"091b3e6e230ae7273599c133be45cec90de9e80a",
            "descriptive": "true",
        }

        url = f"https://api.census.gov/data/{target_year}/acs/acs5/profile"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code != 200:
            return _error_response(
                f"API request failed with status {response.status_code}: {response.text}"
            )

        data = response.json()
        
        # Filter out columns ending with "M" or "A"
        if isinstance(data, list) and len(data) > 0:
            # Get header row
            headers = data[0]
            
            # Find indices of columns to keep (not ending with M or A)
            indices_to_keep = []
            for i, header in enumerate(headers):
                if isinstance(header, str) and header.startswith("DP05_"):
                    if not (header.endswith("M") or header.endswith("A")):
                        indices_to_keep.append(i)
                else:
                    # Keep non-DP05 columns (like NAME, GEO_ID, etc.)
                    indices_to_keep.append(i)
            
            # Filter all rows to keep only selected columns
            filtered_data = []
            for row in data:
                filtered_row = [row[i] for i in indices_to_keep]
                filtered_data.append(filtered_row)
            
            return {"status": "success", "data": filtered_data}
        
        return {"status": "success", "data": data}

    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Network error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "error_message": f"Unexpected error: {str(e)}"}
    
if __name__ == "__main__":
    # Single MSA example (Chicago-Naperville-Elgin, IL-IN-WI MSA)
    print(acs_demographics_msa_pull(["16980"], "2018"))
    # Multiple MSAs example
    # print(acs_demographics_msa_pull(["16980", "35620"], "2018"))