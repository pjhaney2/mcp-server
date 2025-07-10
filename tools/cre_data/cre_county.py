from datetime import datetime
from typing import Dict, Optional, Union, Any, List
import requests

def cre_county_pull(
    geo_fips: List[str], 
    state_fips: str, 
    year: Optional[str] = None
) -> Dict[str, Any]:
    """
    Pulls Community Resilience Estimates (CRE) data from the US Census Bureau.
    
    This function retrieves county-level Community Resilience Estimates data that measures 
    social vulnerability to disasters. The CRE tracks how socially vulnerable every 
    neighborhood is to the impacts of a disaster using 10 risk factors, providing 
    estimates for populations with 0, 1-2, and 3+ risk factors.

    Args:
        geo_fips (List[str]): The FIPS code(s) for the county(ies). 
                              List of strings (e.g., ["031"] or ["031", "045"])
        state_fips (str): The FIPS code for the state (e.g., "17" for Illinois)
        year (Optional[str]): Year of CRE data. Defaults to current year minus 1. 
                             Available years: 2019, 2021, 2022, 2023

    Returns:
        Dict[str, Any]: Response containing:
            - status: "success" or "error"
            - data: JSON response with CRE data (if successful)
            - error_message: Error details (if unsuccessful)
            
        CRE Variables returned:
            - NAME: Geographic area name
            - PRED0_E: Estimate of population with 0 risk factors (Low Vulnerability)
            - PRED12_E: Estimate of population with 1-2 risk factors (Medium Vulnerability)
            - PRED3_E: Estimate of population with 3 or more risk factors (High Vulnerability)
            - POPUNI: Population universe
            - PRED0_PCT: Percentage with 0 risk factors (calculated) (Low Vulnerability)
            - PRED12_PCT: Percentage with 1-2 risk factors (calculated) (Medium Vulnerability)
            - PRED3_PCT: Percentage with 3+ risk factors (calculated) (High Vulnerability)

    Note: 
        Margin of error fields (PRED0_M, PRED12_M, PRED3_M) are excluded for cleaner output.
        Focus is on estimates and calculated percentages for vulnerability analysis.
        The components of social vulnerability are:
            - Poverty status: Income below poverty threshold
            - Employment status: Unemployment
            - Disability status: Individuals with disabilities
            - Age: Advanced age (typically elderly populations)
            - Number of caregivers in the household: Caregiving responsibilities
            - Unit-level crowding: Household/housing crowding
            - Language barrier: Communication barriers/limited English proficiency
            - Vehicle access: Lack of access to vehicles/transportation
            - Broadband internet access: Lack of access to broadband internet
            - Health insurance coverage: Lack of health insurance coverage
    """
    try:
        def _error_response(message: str) -> Dict[str, str]:
            return {"status": "error", "error_message": message}

        # Validate inputs
        
        # Handle geo_fips as list
        if not isinstance(geo_fips, list):
            return _error_response("geo_fips must be a list of strings.")
        
        geo_fips_list = geo_fips
        
        # Validate all geo_fips codes
        for fips in geo_fips_list:
            if not isinstance(fips, str) or not fips.isdigit():
                return _error_response("All geo_fips must be strings of digits.")
        
        if not isinstance(state_fips, str) or not state_fips.isdigit():
            return _error_response("state_fips must be a string of digits.")

        # Handle year parameter and validate
        # Available CRE years: 2019, 2021, 2022, 2023
        available_years = ["2019", "2021", "2022", "2023"]
        
        if year is not None:
            if str(year) not in available_years:
                return _error_response(f"Year must be one of {available_years}. CRE data is only available for these years.")
            target_year = str(year)
        else:
            # Default to most recent available year (2023)
            target_year = "2023"
        
        # Create comma-separated string for multiple FIPS codes
        geo_fips_str = ",".join(geo_fips_list)
        
        # Define CRE variables to retrieve (excluding margin of error fields)
        cre_variables = "NAME,PRED0_E,PRED12_E,PRED3_E,POPUNI"
        
        params = {
            "get": cre_variables,
            "for": f"county:{geo_fips_str}",
            "in": f"state:{state_fips}",
            "key": "091b3e6e230ae7273599c133be45cec90de9e80a",
            "descriptive": "true",
        }

        url = f"https://api.census.gov/data/{target_year}/cre"
        response = requests.get(url, params=params, timeout=30)

        if response.status_code != 200:
            return _error_response(
                f"API request failed with status {response.status_code}: {response.text}"
            )

        data = response.json()
        
        # Add percentage calculations for CRE data
        if isinstance(data, list) and len(data) > 2:
            # Get header row to find column indices
            headers = data[0]
            
            # Find indices for the values we need
            try:
                pred0_e_idx = headers.index('PRED0_E')
                pred12_e_idx = headers.index('PRED12_E') 
                pred3_e_idx = headers.index('PRED3_E')
                popuni_idx = headers.index('POPUNI')
            except ValueError:
                # If headers not found, return data as-is
                return {"status": "success", "data": data}
            
            # Add percentage column headers
            new_headers = headers + ['PRED0_PCT', 'PRED12_PCT', 'PRED3_PCT']
            new_descriptive = data[1] + [
                'Percent, 0 components of social vulnerability',
                'Percent, 1-2 components of social vulnerability', 
                'Percent, 3+ components of social vulnerability'
            ]
            
            # Process data rows (skip header rows)
            processed_data = [new_headers, new_descriptive]
            
            for row in data[2:]:
                try:
                    # Get values and convert to numbers
                    pred0_e = float(row[pred0_e_idx]) if row[pred0_e_idx] and row[pred0_e_idx] != 'null' else 0
                    pred12_e = float(row[pred12_e_idx]) if row[pred12_e_idx] and row[pred12_e_idx] != 'null' else 0
                    pred3_e = float(row[pred3_e_idx]) if row[pred3_e_idx] and row[pred3_e_idx] != 'null' else 0
                    popuni = float(row[popuni_idx]) if row[popuni_idx] and row[popuni_idx] != 'null' else 0
                    
                    # Calculate percentages
                    if popuni > 0:
                        pred0_pct = round((pred0_e / popuni) * 100, 2)
                        pred12_pct = round((pred12_e / popuni) * 100, 2)
                        pred3_pct = round((pred3_e / popuni) * 100, 2)
                    else:
                        pred0_pct = 0
                        pred12_pct = 0
                        pred3_pct = 0
                    
                    # Add percentages to row
                    new_row = row + [str(pred0_pct), str(pred12_pct), str(pred3_pct)]
                    processed_data.append(new_row)
                    
                except (ValueError, IndexError):
                    # If calculation fails, add row without percentages
                    processed_data.append(row + ['', '', ''])
            
            return {"status": "success", "data": processed_data}
        
        return {"status": "success", "data": data}

    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Network error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "error_message": f"Unexpected error: {str(e)}"}
    
if __name__ == "__main__":
    # Single county example - Cook County, Illinois
    print(cre_county_pull(["031"], "17", "2023"))
    # Multiple counties example
    # print(cre_county_pull(["031", "043"], "17", "2023"))