import requests
import json
from typing import Dict, Any, List

def get_qcew_data(geo_codes: List[str], industry_codes: List[str], year: str = None) -> Dict[str, Any]:
    """
    Get simplified QCEW industry establishment and employee data for multiple locations and industries.
    Calculate location quotients for establishment and employee metrics.
    
    Args:
        geo_codes (list): List of geographic area codes (e.g., ["US000", "C1954"])
        industry_codes (list): List of industry codes (e.g., ["10", "111"])
        year (str, optional): Specific year to retrieve data for (e.g., "2023"). If not provided, gets latest data.
        For example, to get manufacturing (1013) data for DuPage County Illinois (17043), you would use get_qcew_data(["17043"], ["1013"])
    
    Returns:
        dict: JSON data containing employment and establishment data with location quotients
    """
    base_url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {"Content-Type": "application/json"}

    # Define data types for series ID construction
    qcew_data_types = {
        "1": "All Employees",
        "2": "Establishments"
    }

    # Define ownership codes for series ID construction
    qcew_ownership_codes = {
        "0": "Total Covered",
        "5": "Private",
    }
    
    # Define size codes for series ID construction
    qcew_size_codes = {
        "0": "All sizes",
    }

    # Always include US total and all industries total
    all_geo_codes = ["US000"] + geo_codes
    all_industry_codes = ["10"] + industry_codes
    
    # Generate series IDs for all combinations
    series_ids = []
    for geo_code in all_geo_codes:
        for industry_code in all_industry_codes:
            for data_code in qcew_data_types.keys():
                for ownership_code in qcew_ownership_codes.keys():
                    for size_code in qcew_size_codes.keys():
                        series_ids.append(f"ENU{geo_code}{data_code}{size_code}{ownership_code}{industry_code}")
    
    # Initialize data structure
    location_data = {}
    
    # Process in batches of 50 series IDs
    for i in range(0, len(series_ids), 50):
        batch = series_ids[i:i + 50]
        api_key = "243f61eeaa6c450db0a2ecb8dc08c44f"
        
        # Set up parameters based on whether year is specified
        if year:
            params = {
                "seriesid": batch,
                "startyear": year,
                "endyear": year,
                "registrationkey": api_key,
            }
        else:
            params = {
                "seriesid": batch,
                "latest": "true",
                "registrationkey": api_key,
            }
        
        try:
            response = requests.post(base_url, data=json.dumps(params), headers=headers)
            response.raise_for_status()
            json_response = response.json()
            
            if json_response.get("status") != "REQUEST_SUCCEEDED":
                continue
                
            for series in json_response.get("Results", {}).get("series", []):
                series_id = series["seriesID"]
                geo_code = series_id[3:8]
                industry_code = series_id[11:]
                data_type = qcew_data_types.get(series_id[8:9], "Unknown")
                size_code = qcew_size_codes.get(series_id[9:10], "Unknown")
                ownership_code = qcew_ownership_codes.get(series_id[10:11], "Unknown")
                
                # Only process data for total covered (0) and private (5) ownership
                if ownership_code not in ["Total Covered", "Private"]:
                    continue
                
                # Initialize location if not exists
                if geo_code not in location_data:
                    location_data[geo_code] = {
                        "industries": {},
                        "total_employees": 0,
                        "total_establishments": 0
                    }
                
                # Initialize industry if not exists
                if industry_code not in location_data[geo_code]["industries"]:
                    location_data[geo_code]["industries"][industry_code] = {
                        "industry_name": industry_code,
                        "employees": 0,
                        "establishments": 0,
                        "ownership": ownership_code,
                        "size": size_code,
                        "periodName": None,
                        "year": None
                    }
                
                # Get the data value (either latest or for specified year)
                if year:
                    data_item = next((item for item in series.get("data", []) if item.get("year") == year), None)
                else:
                    data_item = next((item for item in series.get("data", []) if item.get("latest") == "true"), None)
                
                if data_item:
                    value = int(data_item["value"]) if data_item["value"] != "-" else 0
                    
                    # Update period and year
                    location_data[geo_code]["industries"][industry_code]["periodName"] = data_item["periodName"]
                    location_data[geo_code]["industries"][industry_code]["year"] = data_item["year"]
                    
                    if data_type == "All Employees":
                        location_data[geo_code]["industries"][industry_code]["employees"] = value
                        location_data[geo_code]["total_employees"] += value
                    elif data_type == "Establishments":
                        location_data[geo_code]["industries"][industry_code]["establishments"] = value
                        location_data[geo_code]["total_establishments"] += value
                        
        except Exception as e:
            print(f"Error processing batch: {str(e)}")
            continue
    
    # Calculate Location Quotients
    # First, get national totals from US data
    us_data = location_data.get("US000", {})
    us_industries = us_data.get("industries", {})
    
    # Calculate LQs for each location and industry
    for geo_code, geo_info in location_data.items():
        # Skip US total when calculating LQs
        if geo_code == "US000":
            # Set LQs to 1.0 for US total
            for industry_code, industry_info in geo_info["industries"].items():
                industry_info["establishment_lq"] = 1.0
                industry_info["employee_lq"] = 1.0
            continue
            
        # Get the all industries total (10) for this location
        all_industries_data = geo_info["industries"].get("10", {})
        all_industries_employees = all_industries_data.get("employees", 0)
        all_industries_establishments = all_industries_data.get("establishments", 0)
        
        # Get the all industries total (10) for US
        us_all_industries_data = us_industries.get("10", {})
        us_all_industries_employees = us_all_industries_data.get("employees", 0)
        us_all_industries_establishments = us_all_industries_data.get("establishments", 0)
        
        for industry_code, industry_info in geo_info["industries"].items():
            # Skip the all industries total (10) when calculating LQs
            if industry_code == "10":
                continue
                
            # Get the US total for this industry
            us_industry_data = us_industries.get(industry_code, {})
            us_industry_employees = us_industry_data.get("employees", 0)
            us_industry_establishments = us_industry_data.get("establishments", 0)
            
            # Calculate Employee LQ
            if all_industries_employees > 0 and us_all_industries_employees > 0:
                local_employee_share = industry_info["employees"] / all_industries_employees
                national_employee_share = us_industry_employees / us_all_industries_employees
                employee_lq = local_employee_share / national_employee_share if national_employee_share > 0 else 0
            else:
                employee_lq = 0
            
            # Calculate Establishment LQ
            if all_industries_establishments > 0 and us_all_industries_establishments > 0:
                local_establishment_share = industry_info["establishments"] / all_industries_establishments
                national_establishment_share = us_industry_establishments / us_all_industries_establishments
                establishment_lq = local_establishment_share / national_establishment_share if national_establishment_share > 0 else 0
            else:
                establishment_lq = 0
            
            # Add LQs to industry info
            industry_info["establishment_lq"] = round(establishment_lq, 2)
            industry_info["employee_lq"] = round(employee_lq, 2)
    
    return location_data

if __name__ == "__main__":
    # Test with latest data (default)
    print("Testing with latest data:")
    result = get_qcew_data(["17043"], ["1013"])
    print(json.dumps(result, indent=2))
    
    # Test with specific year
    print("\n\nTesting with year 2023:")
    result_2023 = get_qcew_data(["17043"], ["1013"], year="2023")
    print(json.dumps(result_2023, indent=2))