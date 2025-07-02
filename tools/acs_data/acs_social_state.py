from datetime import datetime
from typing import Dict, Optional, Union, Any
import requests

def acs_social_state_pull(
    state_fips: str, 
    year: Optional[str] = None
) -> Dict[str, Any]:
    """
    Pulls data from the US Census Bureau's American Community Survey (ACS) 5-year estimates.
    
    This function is restricted to state-level social characteristics data (DP02 profile only).
    This includes data such as household types, relationships, marital status, fertility, education,
    veteran status, disability, residence history, citizenship, language, ancestry, and computer/internet use.
    Total Population is found under PLACE OF BIRTH category.

    Args:
        state_fips (str): The FIPS code for the state (e.g., "17" for Illinois)
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
        
        if not isinstance(state_fips, str) or not state_fips.isdigit():
            return _error_response("state_fips must be a string of digits.")

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
        
        params = {
            "get": f"NAME,group(DP02)",
            "for": f"state:{state_fips}",
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
                if isinstance(header, str) and header.startswith("DP02_"):
                    if not (header.endswith("M") or header.endswith("A")):
                        indices_to_keep.append(i)
                else:
                    # Keep non-DP02 columns (like NAME, GEO_ID, etc.)
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
    print(acs_social_state_pull("17", "2018"))