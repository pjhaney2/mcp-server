from typing import Dict, List, Tuple, Optional
import re

"""
FIPS State Search Tool

This module provides a keyword search function to find state FIPS codes.
It searches through state names and returns matching results with their FIPS codes.
This is designed for use as an LLM tool to provide manageable result sets.
"""

def _get_state_fips_data() -> Dict[str, str]:
    """Internal function containing the complete state FIPS dictionary."""
    return {
        "Alabama": "01",
        "Alaska": "02",
        "Arizona": "04",
        "Arkansas": "05",
        "California": "06",
        "Colorado": "08",
        "Connecticut": "09",
        "Delaware": "10",
        "District of Columbia": "11",
        "Florida": "12",
        "Georgia": "13",
        "Hawaii": "15",
        "Idaho": "16",
        "Illinois": "17",
        "Indiana": "18",
        "Iowa": "19",
        "Kansas": "20",
        "Kentucky": "21",
        "Louisiana": "22",
        "Maine": "23",
        "Maryland": "24",
        "Massachusetts": "25",
        "Michigan": "26",
        "Minnesota": "27",
        "Mississippi": "28",
        "Missouri": "29",
        "Montana": "30",
        "Nebraska": "31",
        "Nevada": "32",
        "New Hampshire": "33",
        "New Jersey": "34",
        "New Mexico": "35",
        "New York": "36",
        "North Carolina": "37",
        "North Dakota": "38",
        "Ohio": "39",
        "Oklahoma": "40",
        "Oregon": "41",
        "Pennsylvania": "42",
        "Rhode Island": "44",
        "South Carolina": "45",
        "South Dakota": "46",
        "Tennessee": "47",
        "Texas": "48",
        "Utah": "49",
        "Vermont": "50",
        "Virginia": "51",
        "Washington": "53",
        "West Virginia": "54",
        "Wisconsin": "55",
        "Wyoming": "56",
        "American Samoa": "60",
        "Guam": "66",
        "Northern Mariana Islands": "69",
        "Puerto Rico": "72",
        "Virgin Islands": "78"
    }

def search_state_fips(keyword: str, max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """
    Search for US states by keyword and return their FIPS codes.
    
    This function searches through state names and returns a list of matching 
    states with their FIPS codes. The search is case-insensitive and uses
    three priority levels for matching:
    
    Priority 1: Exact word matches (highest priority)
    Priority 2: All search terms found as words in the state name
    Priority 3: All search terms found as substrings (partial matches)
    
    Args:
        keyword (str): Search term to match against state names (case-insensitive)
        max_results (Optional[int]): Maximum number of results to return (default: 20)
    
    Returns:
        List[Tuple[str, str]]: List of tuples containing (state_name, fips_code)
                              sorted by relevance (priority level, then alphabetically)
    
    Examples:
        >>> search_state_fips("new")
        [('New Hampshire', '33'), ('New Jersey', '34'), ('New Mexico', '35'), ('New York', '36')]
        
        >>> search_state_fips("north")
        [('North Carolina', '37'), ('North Dakota', '38')]
        
        >>> search_state_fips("cal", 5)
        [('California', '06'), ('North Carolina', '37'), ('South Carolina', '45')]
    """
    if not keyword or not keyword.strip():
        return []
    
    # Get the state data
    state_data = _get_state_fips_data()
    
    # Normalize search terms
    search_terms = re.findall(r'\b\w+\b', keyword.lower())
    if not search_terms:
        return []
    
    # Results organized by priority
    priority_1_results = []  # Exact word matches
    priority_2_results = []  # All words match
    priority_3_results = []  # Partial matches
    
    for state_name, fips_code in state_data.items():
        state_lower = state_name.lower()
        state_words = re.findall(r'\b\w+\b', state_lower)
        
        # Check for exact word matches (Priority 1)
        exact_matches = [term for term in search_terms if term in state_words]
        if len(exact_matches) == len(search_terms):
            priority_1_results.append((state_name, fips_code))
            continue
            
        # Check if all search terms are found as words (Priority 2)
        word_matches = [term for term in search_terms if any(term == word for word in state_words)]
        if len(word_matches) == len(search_terms):
            priority_2_results.append((state_name, fips_code))
            continue
            
        # Check if all search terms are found as substrings (Priority 3)
        substring_matches = [term for term in search_terms if term in state_lower]
        if len(substring_matches) == len(search_terms):
            priority_3_results.append((state_name, fips_code))
    
    # Sort each priority group alphabetically
    priority_1_results.sort(key=lambda x: x[0])
    priority_2_results.sort(key=lambda x: x[0])
    priority_3_results.sort(key=lambda x: x[0])
    
    # Combine results by priority and limit
    all_results = priority_1_results + priority_2_results + priority_3_results
    
    if max_results:
        return all_results[:max_results]
    
    return all_results

if __name__ == "__main__":
    # Test the search function
    print("Testing state FIPS search:")
    print("Search 'new':", search_state_fips("new"))
    print("Search 'north':", search_state_fips("north"))
    print("Search 'cal':", search_state_fips("cal", 5))
    print("Search 'texas':", search_state_fips("texas"))