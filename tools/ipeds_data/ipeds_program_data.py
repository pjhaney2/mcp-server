#https://educationdata.urban.org/documentation/
#https://educationdata.urban.org/documentation/colleges.html#ipeds_directory

import requests
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from .get_cip_codes import CIP_CODES
from .get_award_levels import AWARD_LEVELS

logger = logging.getLogger(__name__)

def get_programs(
    state_fips: Optional[List[str]] = None,
    year: Optional[int] = None,
    award_levels: Optional[List[int]] = None,
    cip_keywords: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Get program completion data from Integrated Postsecondary Education Data System (IPEDS) data
    from National Center for Education Statistics (NCES) from 1984 to present (well, current year minus 3).
    This is the IPEDS Completions by CIP Code dataset showing degree/certificate awards by program.
    
    Args:
        state_fips: State FIPS code(s) - list of strings (e.g. ["17"] for Illinois)
        year: Year of data (defaults to current year - 3) (e.g. 2021)
        award_levels: Award level code(s) - list of integers
                     (defaults to [4, 7, 9, 22, 23, 24] for Associate's, Bachelor's, Master's, and Doctoral degrees)
                     4=Associate's degree, 7=Bachelor's degree, 9=Master's degree,
                     22=Doctor's degree research/scholarship, 23=Doctor's degree professional practice, 24=Doctor's degree other
        cip_keywords: Optional keyword(s) to filter CIP code descriptions (case-insensitive) - list of strings
                     (e.g. ["engineering"] or ["computer", "technology"])
        
    Returns:
        List of dictionaries containing program completion information with fields:
        - unitid: Institution ID
        - cipcode: CIP (Classification of Instructional Programs) code
        - cip_name: Human-readable CIP program name
        - award_level: Award level code
        - award_level_name: Human-readable award level description
        - awards: Number of awards/completions (filtered to exclude 0 awards)
    """
    
    # Default to current year minus 3 if not specified
    if year is None:
        year = datetime.now().year - 3
    
    # Default award levels if not specified
    if award_levels is None:
        award_levels = [4, 7, 9, 22, 23, 24]
        
    url = f"https://educationdata.urban.org/api/v1/college-university/ipeds/completions-cip-2/{year}/"
    params = {}
    
    # Handle API-supported parameters
    if state_fips:
        params["fips"] = ",".join(state_fips)
    
    if award_levels:
        params["award_level"] = ",".join(map(str, award_levels))
    
    # Add timeout and handle large responses
    try:
        logger.info(f"Fetching IPEDS program data from: {url}")
        logger.info(f"Parameters: {params}")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        results = data.get('results', [])
        logger.info(f"Received {len(results)} program records")
    except requests.exceptions.Timeout:
        logger.error("IPEDS program data request timed out")
        return [{"error": "Request timed out - try filtering by specific award levels or narrowing your search"}]
    except requests.exceptions.RequestException as e:
        logger.error(f"IPEDS program data request failed: {str(e)}")
        return [{"error": f"Request failed: {str(e)}"}]
    except Exception as e:
        logger.error(f"Unexpected error in get_programs: {str(e)}")
        return [{"error": f"Unexpected error: {str(e)}"}]
    
    # Filter out records with 0 awards
    filtered_results = [inst for inst in results if inst.get('awards', 0) > 0]
    
    # Filter by CIP code keywords if specified
    if cip_keywords:
        keyword_list_lower = [k.lower() for k in cip_keywords]
        filtered_results = [inst for inst in filtered_results 
                          if any(keyword in CIP_CODES.get(str(inst.get('cipcode', '')), '').lower() 
                                for keyword in keyword_list_lower)]
    
    logger.info(f"After filtering: {len(filtered_results)} records remain")
    
    # Limit results to prevent memory issues
    max_results = 1000
    if len(filtered_results) > max_results:
        logger.warning(f"Limiting results from {len(filtered_results)} to {max_results} to prevent memory issues")
        filtered_results = filtered_results[:max_results]
    
    # Process results in a more memory-efficient way
    processed_results = []
    for inst in filtered_results:
        try:
            processed_results.append({
                'unitid': inst.get('unitid', ''),
                'cipcode': inst.get('cipcode', ''),
                'cip_name': CIP_CODES.get(str(inst.get('cipcode', '')), 'Unknown CIP Code'),
                'award_level': inst.get('award_level', ''),
                'award_level_name': AWARD_LEVELS.get(str(inst.get('award_level', '')), 'Unknown Award Level'),
                'awards': inst.get('awards', ''),
            })
        except Exception as e:
            logger.error(f"Error processing record: {e}")
            continue
    
    logger.info(f"Successfully processed {len(processed_results)} records")
    return processed_results

if __name__ == "__main__":
    print(get_programs(state_fips="17"))