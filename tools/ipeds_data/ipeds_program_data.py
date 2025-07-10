#https://educationdata.urban.org/documentation/
#https://educationdata.urban.org/documentation/colleges.html#ipeds_directory

import requests
from typing import List, Dict, Optional, Any
from datetime import datetime
try:
    from .get_cip_codes import CIP_CODES
    from .get_award_levels import AWARD_LEVELS
except ImportError:
    # Fallback for direct execution
    from get_cip_codes import CIP_CODES
    from get_award_levels import AWARD_LEVELS

# Define CIP category mappings
CIP_CATEGORIES = {
    # STEM Fields
    'STEM': {
        'name': 'Science, Technology, Engineering & Mathematics',
        'codes': [110000, 140000, 150000, 260000, 270000, 400000, 410000]
    },
    # Health Professions
    'Health': {
        'name': 'Health Professions & Related Programs',
        'codes': [510000, 510101, 510401, 511201, 511701, 511901, 512001, 512101, 512401, 512704]
    },
    # Business & Management
    'Business': {
        'name': 'Business, Management & Marketing',
        'codes': [520000, 80000]
    },
    # Liberal Arts & Humanities
    'Liberal Arts': {
        'name': 'Liberal Arts, Humanities & Social Sciences',
        'codes': [230000, 240000, 160000, 380000, 450000, 540000, 50000]
    },
    # Education & Human Services
    'Education': {
        'name': 'Education & Human Services',
        'codes': [130000, 190000, 440000]
    },
    # Professional Services
    'Professional': {
        'name': 'Professional Services & Public Administration',
        'codes': [220000, 220101, 390000, 390602, 390603, 390605, 430000]
    },
    # Technical & Trades
    'Technical': {
        'name': 'Technical, Trades & Applied Sciences',
        'codes': [460000, 470000, 480000, 490000, 100000, 120000, 200000, 290000]
    },
    # Arts & Creative
    'Arts': {
        'name': 'Visual & Performing Arts',
        'codes': [500000]
    },
    # Agriculture & Natural Resources
    'Agriculture': {
        'name': 'Agriculture & Natural Resources',
        'codes': [10000, 20000, 30000]
    },
    # Architecture & Design
    'Architecture': {
        'name': 'Architecture & Environmental Design',
        'codes': [40000]
    },
    # Communications & Media
    'Communications': {
        'name': 'Communications & Media Studies',
        'codes': [90000]
    },
    # Interdisciplinary & General
    'Interdisciplinary': {
        'name': 'Interdisciplinary & General Studies',
        'codes': [300000, 310000, 250000]
    },
    # All Programs (total across all fields)
    'All Programs': {
        'name': 'All Programs (Total)',
        'codes': [990000]
    },
    # Other/Unspecified
    'Other': {
        'name': 'Other/Unspecified Programs',
        'codes': [950000, -1, -2, -3]
    }
}

def get_cip_category(cipcode: int) -> Dict[str, str]:
    """
    Determine the high-level category for a given CIP code.
    
    Args:
        cipcode: The CIP code as an integer
        
    Returns:
        Dictionary with 'category_id' and 'category_name'
    """
    for category_id, category_info in CIP_CATEGORIES.items():
        if cipcode in category_info['codes']:
            return {
                'category_id': category_id,
                'category_name': category_info['name']
            }
    
    # If not found in specific mappings, categorize by first digit
    first_digit = int(str(cipcode)[0]) if str(cipcode)[0].isdigit() else 0
    
    if first_digit == 1:
        return {'category_id': 'STEM', 'category_name': 'Science, Technology, Engineering & Mathematics'}
    elif first_digit == 2:
        return {'category_id': 'Liberal Arts', 'category_name': 'Liberal Arts, Humanities & Social Sciences'}
    elif first_digit == 3:
        return {'category_id': 'Interdisciplinary', 'category_name': 'Interdisciplinary & General Studies'}
    elif first_digit == 4:
        return {'category_id': 'Liberal Arts', 'category_name': 'Liberal Arts, Humanities & Social Sciences'}
    elif first_digit == 5:
        return {'category_id': 'Health', 'category_name': 'Health Professions & Related Programs'}
    else:
        return {'category_id': 'Other', 'category_name': 'Other/Unspecified Programs'}

def get_programs(
    state_fips: Optional[List[str]] = None,
    year: Optional[List[str]] = None,
    award_levels: Optional[List[str]] = None,
    cip_keywords: Optional[List[str]] = None,
    unitid: Optional[List[str]] = None,
    include_categories: bool = True,
    aggregate_by_category: bool = False,
) -> Dict[str, Any]:
    """
    Get program completion data from Integrated Postsecondary Education Data System (IPEDS) data
    from National Center for Education Statistics (NCES) from 1984 to present (well, current year minus 3).
    This is the IPEDS Completions by CIP Code dataset showing degree/certificate awards by program.
    
    Args:
        state_fips: State FIPS code(s) - list of strings (e.g. ["17"] for Illinois)
        year: Year(s) of data - list of strings (defaults to [current year - 3]) (e.g. ["2021"] or ["2020", "2021"])
        award_levels: Award level code(s) - list of strings
                     (defaults to ["4", "7", "9", "22", "23", "24"] for Associate's, Bachelor's, Master's, and Doctoral degrees)
                     "4"=Associate's degree, "7"=Bachelor's degree, "9"=Master's degree,
                     "22"=Doctor's degree research/scholarship, "23"=Doctor's degree professional practice, "24"=Doctor's degree other
        cip_keywords: Optional keyword(s) to filter CIP code descriptions (case-insensitive) - list of strings
                     (e.g. ["engineering"] or ["computer", "technology"])
        unitid: Optional institution ID(s) to filter results - list of strings (e.g. ["123456", "789012"])
        include_categories: Whether to include high-level CIP category information in results
        aggregate_by_category: Whether to aggregate results by CIP category instead of individual programs
        
    Returns:
        Dictionary containing:
        - filters_applied: Dictionary of all filters used in the query
            - year: Year of data used
            - state_fips: State FIPS codes filtered (if any)
            - award_levels: Award level codes filtered (if any)
            - award_level_names: Human-readable award level names
            - cip_keywords: CIP keywords used for filtering (if any)
            - unitid: Institution IDs filtered (if any)
        - unitids: List of all unique institution IDs in the dataset
        - unitid_count: Total count of unique institutions
        - total_programs: Total number of unique programs in results
        - total_awards: Sum of all awards across all programs
        - programs: List of dictionaries with aggregated program data, each containing:
            - cipcode: CIP (Classification of Instructional Programs) code
            - cip_name: Human-readable CIP program name
            - total_awards: Total number of awards across all institutions
            - institution_count: Number of institutions offering this program
        
        Programs are sorted by total_awards in descending order.
    """
    
    # Default to current year minus 3 if not specified
    if year is None:
        year = [str(datetime.now().year - 3)]
    
    # Default award levels if not specified
    if award_levels is None:
        award_levels = ["4", "7", "9", "22", "23", "24"]
        
    # For single year, use original efficient approach; for multiple years, aggregate
    if len(year) == 1:
        # Single year - use original efficient approach
        single_year = year[0]
        url = f"https://educationdata.urban.org/api/v1/college-university/ipeds/completions-cip-2/{single_year}/"
        params = {}
        
        # Add all filters as query parameters
        if state_fips:
            params["fips"] = ",".join(state_fips)
        
        if award_levels:
            params["award_level"] = ",".join(award_levels)
        
        if unitid:
            params["unitid"] = ",".join(unitid)
        
        # Handle pagination properly
        all_results = []
        current_url = url
        
        try:
            while current_url:
                response = requests.get(current_url, params=params if current_url == url else None, timeout=120)
                response.raise_for_status()
                data = response.json()
                
                # Extract results from this page
                page_results = data.get('results', [])
                all_results.extend(page_results)
                
                # Get next page URL
                current_url = data.get('next')
                
                # Progress indicator
                if len(all_results) % 10000 == 0 and len(all_results) > 0:
                    print(f"Retrieved {len(all_results)} records so far...")
            
            results = all_results
            
        except requests.exceptions.Timeout:
            return {"error": "Request timed out - the IPEDS programs API is currently slow or unavailable. Try again later or contact support."}
        except requests.exceptions.RequestException as e:
            if "524" in str(e) or "timeout" in str(e).lower():
                return {"error": "IPEDS programs API is experiencing server timeouts. This is a known issue with this specific endpoint. Try again later."}
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    else:
        # Multiple years - aggregate results (slower but necessary)
        all_results = []
        
        try:
            for single_year in year:
                # Use simple URL with all filters as query parameters
                url = f"https://educationdata.urban.org/api/v1/college-university/ipeds/completions-cip-2/{single_year}/"
                params = {}
                
                # Add all filters as query parameters
                if state_fips:
                    params["fips"] = ",".join(state_fips)
                
                if award_levels:
                    params["award_level"] = ",".join(award_levels)
                
                if unitid:
                    params["unitid"] = ",".join(unitid)
                
                # Handle pagination properly for this year
                year_results = []
                current_url = url
                
                while current_url:
                    response = requests.get(current_url, params=params if current_url == url else None, timeout=60)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Extract results from this page
                    page_results = data.get('results', [])
                    year_results.extend(page_results)
                    
                    # Get next page URL
                    current_url = data.get('next')
                    
                    # Progress indicator
                    if len(year_results) % 10000 == 0 and len(year_results) > 0:
                        print(f"Retrieved {len(year_results)} records for year {single_year} so far...")
                
                all_results.extend(year_results)
            
            results = all_results
            
        except requests.exceptions.Timeout:
            return {"error": "Request timed out - the IPEDS programs API is currently slow or unavailable. Try again later or contact support."}
        except requests.exceptions.RequestException as e:
            if "524" in str(e) or "timeout" in str(e).lower():
                return {"error": "IPEDS programs API is experiencing server timeouts. This is a known issue with this specific endpoint. Try again later."}
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    # Filter out records with 0 awards
    filtered_results = [inst for inst in results if inst.get('awards', 0) > 0]
    
    # Filter by CIP code keywords if specified
    if cip_keywords:
        keyword_list_lower = [k.lower() for k in cip_keywords]
        filtered_results = [inst for inst in filtered_results 
                          if any(keyword in CIP_CODES.get(str(inst.get('cipcode', '')), '').lower() 
                                for keyword in keyword_list_lower)]
    
    # Note: Removed the 1000 result limit to ensure we capture all institutions
    # The aggregation will reduce the final data size anyway
    
    # Collect all unique unitids
    all_unitids = sorted(list(set(inst.get('unitid', '') for inst in filtered_results if inst.get('unitid'))))
    
    # Process results - aggregate by CIP code
    cip_aggregates = {}
    
    for inst in filtered_results:
        try:
            cipcode = inst.get('cipcode', '')
            unitid = inst.get('unitid', '')
            awards = inst.get('awards', 0)
            
            # Create key for aggregation
            if cipcode not in cip_aggregates:
                cip_aggregates[cipcode] = {
                    'cipcode': cipcode,
                    'cip_name': CIP_CODES.get(str(cipcode), 'Unknown CIP Code'),
                    'total_awards': 0,
                    'unique_institutions': set()
                }
            
            # Sum awards and track unique institutions
            cip_aggregates[cipcode]['total_awards'] += awards
            if unitid:
                cip_aggregates[cipcode]['unique_institutions'].add(unitid)
        
        except Exception:
            continue
    
    # Convert to list and sort by total awards (descending)
    aggregated_results = []
    for cip_data in cip_aggregates.values():
        result = {
            'cipcode': cip_data['cipcode'],
            'cip_name': cip_data['cip_name'],
            'total_awards': cip_data['total_awards'],
            'institution_count': len(cip_data['unique_institutions'])
        }
        aggregated_results.append(result)
    
    # Sort by total awards (descending)
    aggregated_results.sort(key=lambda x: x['total_awards'], reverse=True)
    
    # Return results with metadata and unitids at the top
    return {
        'filters_applied': {
            'year': year,
            'state_fips': state_fips,
            'award_levels': award_levels,
            'award_level_names': [AWARD_LEVELS.get(str(level), f'Unknown ({level})') for level in (award_levels or [])],
            'cip_keywords': cip_keywords,
            'unitid': unitid
        },
        'unitids': all_unitids,
        'unitid_count': len(all_unitids),
        'total_programs': len(aggregated_results),
        'total_awards': sum(prog['total_awards'] for prog in aggregated_results),
        'programs': aggregated_results
    }

if __name__ == "__main__":
    print(get_programs(state_fips=["17"]))