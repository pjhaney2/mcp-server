from datetime import datetime
from typing import Dict, Optional, Any, List
import requests

def rank_acs_data_high(
    data_point: str,
    geo_type: str,
    state_fips: Optional[str] = None,
    year: Optional[str] = None,
    limit: Optional[int] = 20
) -> Dict[str, Any]:
    """
    Finds the top geographic areas (places, counties, etc.) based on a specific ACS data point.
    
    This function queries the US Census Bureau's American Community Survey (ACS) 5-year estimates
    to find the highest values for a specified data point across all geographic areas of a given type.

    Args:
        data_point (str): The ACS data point/variable to sort by (e.g., "DP02_0001E", "DP03_0062E")
        geo_type (str): The geographic type to query ("place", "county", "state", "metropolitan statistical area/micropolitan statistical area")
        state_fips (Optional[str]): The FIPS code for the state to limit results to. If None, queries all areas. Note: Not applicable for MSA queries.
        year (Optional[str]): Year of ACS data. Defaults to current year minus 2. Must be 2010 or later.
        limit (Optional[int]): Number of top results to return. Defaults to 20.

    Returns:
        Dict[str, Any]: Response containing:
            - status: "success" or "error"
            - data: List of top areas with their values (if successful)
            - error_message: Error details (if unsuccessful)
    """
    try:
        def _error_response(message: str) -> Dict[str, str]:
            return {"status": "error", "error_message": message}

        # Validate inputs
        if not isinstance(data_point, str) or not data_point.strip():
            return _error_response("data_point must be a non-empty string.")
        
        if not isinstance(geo_type, str) or geo_type.lower() not in ["place", "county", "state", "metropolitan statistical area/micropolitan statistical area"]:
            return _error_response("geo_type must be one of: 'place', 'county', 'state', 'metropolitan statistical area/micropolitan statistical area'.")
        
        geo_type = geo_type.lower()
        
        if state_fips is not None and (not isinstance(state_fips, str) or not state_fips.isdigit()):
            return _error_response("state_fips must be a string of digits or None.")
        
        if limit is not None and (not isinstance(limit, int) or limit < 1 or limit > 100):
            return _error_response("limit must be an integer between 1 and 100.")

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
        
        # Determine the data profile based on data_point prefix
        if data_point.startswith("DP02_"):
            profile_group = "DP02"  # Social characteristics
        elif data_point.startswith("DP03_"):
            profile_group = "DP03"  # Economic characteristics
        elif data_point.startswith("DP04_"):
            profile_group = "DP04"  # Housing characteristics
        elif data_point.startswith("DP05_"):
            profile_group = "DP05"  # Demographic characteristics
        else:
            return _error_response("data_point must start with DP02_, DP03_, DP04_, or DP05_.")
        
        # Build parameters based on geo_type and state_fips
        params = {
            "get": f"NAME,{data_point}",
            "for": f"{geo_type}:*",
            "key": "091b3e6e230ae7273599c133be45cec90de9e80a",
        }
        
        # Add state filter based on geo_type
        if geo_type in ["place", "county"]:
            # For place and county queries, we need to specify state
            if state_fips is None or state_fips == "":
                # Use wildcard to get all states
                params["in"] = "state:*"
            else:
                params["in"] = f"state:{state_fips}"
        elif geo_type == "state":
            # For state-level queries, we can't use "in" parameter
            if state_fips is not None and state_fips != "":
                params["for"] = f"state:{state_fips}"
        # For MSA queries, we don't use state filtering at all

        url = f"https://api.census.gov/data/{target_year}/acs/acs5/profile"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code != 200:
            return _error_response(
                f"API request failed with status {response.status_code}: {response.text}"
            )

        data = response.json()
        
        if not isinstance(data, list) or len(data) < 2:
            return _error_response("Invalid or empty data returned from API.")
        
        # Get header row and data rows
        headers = data[0]
        data_rows = data[1:]
        
        # Find the index of the data_point column
        data_point_index = None
        name_index = None
        for i, header in enumerate(headers):
            if header == data_point:
                data_point_index = i
            elif header == "NAME":
                name_index = i
        
        if data_point_index is None:
            return _error_response(f"Data point '{data_point}' not found in the response.")
        
        if name_index is None:
            return _error_response("NAME column not found in the response.")
        
        # Process and sort the data
        processed_data = []
        for row in data_rows:
            try:
                # Skip rows with null or invalid values
                if (len(row) <= data_point_index or 
                    row[data_point_index] is None or 
                    row[data_point_index] == "" or
                    row[data_point_index] == "null"):
                    continue
                
                value = float(row[data_point_index])
                name = row[name_index] if len(row) > name_index else "Unknown"
                
                # Include additional geographic identifiers if available
                geo_info = {
                    "name": name,
                    "value": value,
                    "data_point": data_point
                }
                
                # Add state and other geographic identifiers
                if len(row) > len(headers) - 3:  # Typically has state, county/place codes at the end
                    if geo_type == "place":
                        geo_info["state_fips"] = row[-2] if len(row) > len(headers) - 2 else None
                        geo_info["place_fips"] = row[-1] if len(row) > len(headers) - 1 else None
                    elif geo_type == "county":
                        geo_info["state_fips"] = row[-2] if len(row) > len(headers) - 2 else None
                        geo_info["county_fips"] = row[-1] if len(row) > len(headers) - 1 else None
                    elif geo_type == "state":
                        geo_info["state_fips"] = row[-1] if len(row) > len(headers) - 1 else None
                    elif geo_type == "metropolitan statistical area/micropolitan statistical area":
                        geo_info["msa_fips"] = row[-1] if len(row) > len(headers) - 1 else None
                
                processed_data.append(geo_info)
                
            except (ValueError, TypeError, IndexError):
                # Skip rows with invalid numeric values
                continue
        
        # Sort by value in descending order and limit results
        processed_data.sort(key=lambda x: x["value"], reverse=True)
        top_results = processed_data[:limit if limit else 20]
        
        return {
            "status": "success", 
            "data": top_results,
            "total_found": len(processed_data),
            "returned_count": len(top_results),
            "query_info": {
                "data_point": data_point,
                "geo_type": geo_type,
                "state_fips": state_fips,
                "year": target_year
            }
        }

    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Network error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "error_message": f"Unexpected error: {str(e)}"}
    
if __name__ == "__main__":
    # Test with state-specific queries (Illinois)
    print("Top 5 places in Illinois by population:")
    print(rank_acs_data_high("DP05_0001E", "place", "17", "2022", 5))
    print("\nTop 5 counties in Illinois by population:")
    print(rank_acs_data_high("DP05_0001E", "county", "17", "2022", 5))
    
    # Test with nationwide queries (no state specified)
    print("\nTop 5 places nationwide by population:")
    print(rank_acs_data_high("DP05_0001E", "place", None, "2022", 5))
    print("\nTop 5 counties nationwide by population:")
    print(rank_acs_data_high("DP05_0001E", "county", year="2022", limit=5))
    print("\nTop 5 states by population:")
    print(rank_acs_data_high("DP05_0001E", "state", limit=5))
    print("\nTop 5 MSAs by population:")
    print(rank_acs_data_high("DP05_0001E", "metropolitan statistical area/micropolitan statistical area", limit=5))