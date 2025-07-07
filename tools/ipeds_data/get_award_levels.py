from typing import List, Dict, Optional

# Award Level Dictionary
AWARD_LEVELS = {
    "1": "Award of less than one academic year",
    "2": "Award of less than two academic years",
    "3": "Award of at least one but less than two academic years",
    "4": "Associate's degree",
    "5": "Award of at least one but less than four academic years",
    "6": "Award of at least two but less than four academic years",
    "7": "Bachelor's degree",
    "8": "Postbaccalaureate or post-master's certificate",
    "9": "Master's degree",
    "20": "Doctor's degree (until 2008)",
    "21": "First-professional degree (until 2008)",
    "22": "Doctor's degree, research/scholarship (starting 2007)",
    "23": "Doctor's degree, professional practice (starting 2007)",
    "24": "Doctor's degree, other (starting 2007)",
    "30": "Certificate of less than 12 weeks",
    "31": "Certificates of at least 12 weeks but less than 1 year",
    "32": "Certificate of at least 1 year but less than 2 years",
    "33": "Certificate of at least 2 years but less than 4 years",
    "99": "Total",
    "-1": "Missing/not reported",
    "-2": "Not applicable",
    "-3": "Suppressed data"
}

def get_award_levels(
    search_term: Optional[str] = None,
    award_level_codes: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Get award level information from IPEDS data.
    
    Args:
        search_term: Optional search term to filter award level names (case-insensitive)
        award_level_codes: Optional award level code(s) to look up specific levels - list of strings
        
    Returns:
        List of dictionaries containing award level information with fields:
        - code: Award level code
        - name: Award level description
    """
    results = []
    
    # If specific codes are requested
    if award_level_codes:
        for code in award_level_codes:
            if str(code) in AWARD_LEVELS:
                results.append({
                    'code': code,
                    'name': AWARD_LEVELS[str(code)]
                })
    else:
        # Return all award levels
        for code, name in AWARD_LEVELS.items():
            results.append({
                'code': code,
                'name': name
            })
    
    # Filter by search term if provided
    if search_term:
        search_lower = search_term.lower()
        results = [item for item in results if search_lower in item['name'].lower()]
    
    return results