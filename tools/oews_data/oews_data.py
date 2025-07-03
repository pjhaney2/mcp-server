import requests
import json
from typing import Dict, Any, List


def get_oews_data(geo_codes: List[str], occ_codes: List[str]) -> Dict[str, Any]:
    """
    Get simplified OEWS occupation and wage data for multiple locations and occupations.
    Calculate location quotients for employment and wage data.
    
    Args:
        geo_codes (list): List of geographic area codes (e.g., ["0000000", "0011500"])
        occ_codes (list): List of occupation codes (e.g., ["111011", "111021"])
    
    Returns:
        dict: JSON data containing employment and wage data with location quotients
    """
    base_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {"Content-Type": "application/json"}

    # Define data types for series ID construction
    oews_data_types = {
        "01": "Employment",
        "08": "Hourly median wage"
    }

    # Always include US total and all occupations total
    all_geo_codes = ["0000000"] + geo_codes
    all_occ_codes = ["000000"] + occ_codes
    
    # Generate series IDs for all combinations
    series_ids = []
    for geo_code in all_geo_codes:
        # Determine area type:
        # N for national (0000000)
        # S for state (2-digit state FIPS)
        # M for metro/nonmetro (all others)
        if geo_code == "0000000":
            area_type = "N"
        elif len(geo_code) >= 2 and all(c == '0' for c in geo_code[2:]):
            area_type = "S"
        else:
            area_type = "M"
            
        for occ_code in all_occ_codes:
            for data_code in oews_data_types.keys():
                series_ids.append(f"OEU{area_type}{geo_code}000000{occ_code}{data_code}")
    
    # Initialize data structure
    result = {
        "locations": {},
        "national_totals": {
            "employment": {},
            "wage": {}
        }
    }
    
    # Process in batches of 50 series IDs
    for i in range(0, len(series_ids), 50):
        batch = series_ids[i:i + 50]
        
        # OEWS only provides latest data, so always use latest=true regardless of year parameter
        params = {
            "seriesid": batch,
            "latest": "true",
            "registrationkey": "243f61eeaa6c450db0a2ecb8dc08c44f",
        }
        
        try:
            response = requests.post(base_url, data=json.dumps(params), headers=headers)
            response.raise_for_status()
            json_response = response.json()
            
            if json_response.get("status") != "REQUEST_SUCCEEDED":
                continue
                
            for series in json_response.get("Results", {}).get("series", []):
                series_id = series["seriesID"]
                geo_code = series_id[4:11]
                occ_code = series_id[17:23]
                data_type = oews_data_types.get(series_id[23:], "Unknown")
                
                # Initialize location if not exists
                if geo_code not in result["locations"]:
                    result["locations"][geo_code] = {
                        "occupations": {},
                        "total_employment": 0,
                        "total_wage": 0
                    }
                
                # Initialize occupation if not exists
                if occ_code not in result["locations"][geo_code]["occupations"]:
                    result["locations"][geo_code]["occupations"][occ_code] = {
                        "occupation_name": occ_code,
                        "employment": 0,
                        "hourly_wage": 0,
                        "periodName": None,
                        "year": None
                    }
                
                # OEWS only provides latest data, so always use the latest flag
                target_data = next((item for item in series.get("data", []) if item.get("latest") == "true"), None)
                
                if target_data:
                    value = float(target_data["value"]) if target_data["value"] != "-" else 0
                    
                    # Update period and year
                    result["locations"][geo_code]["occupations"][occ_code]["periodName"] = target_data["periodName"]
                    result["locations"][geo_code]["occupations"][occ_code]["year"] = target_data["year"]
                    
                    if data_type == "Employment":
                        employment = int(value)
                        result["locations"][geo_code]["occupations"][occ_code]["employment"] = employment
                        # Only update total employment from the "all occupations" code
                        if occ_code == "000000":
                            result["locations"][geo_code]["total_employment"] = employment
                    elif data_type == "Hourly median wage":
                        hourly_wage = value
                        result["locations"][geo_code]["occupations"][occ_code]["hourly_wage"] = hourly_wage
                        # Only update total wage from the "all occupations" code
                        if occ_code == "000000":
                            result["locations"][geo_code]["total_wage"] = hourly_wage
                        
        except Exception as e:
            print(f"Error processing batch: {str(e)}")
            continue
    
    # Get national totals from the "all occupations" data
    national_data = result["locations"].get("0000000", {}).get("occupations", {}).get("000000", {})
    total_national_employment = national_data.get("employment", 0)
    total_national_wage = national_data.get("hourly_wage", 0)
    
    # Calculate Location Quotients using the all occupations totals
    for location in result["locations"].values():
        total_location_employment = location["total_employment"]
        total_location_wage = location["total_wage"]
        
        for occ_code, occ_data in location["occupations"].items():
            if occ_code != "000000":  # Skip LQ calculation for all occupations total
                # Calculate Employment LQ
                local_employment_share = occ_data["employment"] / total_location_employment if total_location_employment > 0 else 0
                national_employment_share = result["locations"]["0000000"]["occupations"][occ_code]["employment"] / total_national_employment if total_national_employment > 0 else 0
                employment_lq = local_employment_share / national_employment_share if national_employment_share > 0 else 0
                
                # Calculate Wage LQ
                local_wage = occ_data["hourly_wage"]
                national_wage = result["locations"]["0000000"]["occupations"][occ_code]["hourly_wage"]
                wage_lq = (local_wage / total_location_wage) / (national_wage / total_national_wage) if total_location_wage > 0 and total_national_wage > 0 and national_wage > 0 else 0
                
                # Add LQs to occupation data
                occ_data["employment_lq"] = round(employment_lq, 2)
                occ_data["wage_lq"] = round(wage_lq, 2)
    
    return result

if __name__ == "__main__":
    result = get_oews_data(["0000000"], ["111011"])
    print(json.dumps(result, indent=2))