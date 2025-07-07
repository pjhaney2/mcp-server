from typing import List, Dict, Optional, Any

# CIP Code Dictionary
CIP_CODES = {
    "990000": "All programs",
    "10000": "Agriculture, agriculture operations, and related sciences",
    "20000": "Agricultural sciences",
    "30000": "Natural resources and conservation",
    "40000": "Architecture and related services",
    "50000": "Area, ethnic, cultural, and gender studies",
    "80000": "Marketing and distribution",
    "90000": "Communication, journalism, and related programs",
    "100000": "Communications technologies/technicians and support services",
    "110000": "Computer and information sciences and support services",
    "120000": "Personal and culinary services",
    "130000": "Education",
    "140000": "Engineering",
    "150000": "Engineering technologies/technicians",
    "160000": "Foreign languages, literatures, and linguistics",
    "190000": "Family and consumer sciences/human sciences",
    "200000": "Vocational home economics",
    "220000": "Legal professions and studies",
    "220101": "Law (LLB, JD)",
    "230000": "English language and literature/letters",
    "240000": "Liberal arts and sciences, general studies and humanities",
    "250000": "Library science",
    "260000": "Biological and biomedical sciences",
    "270000": "Mathematics and statistics",
    "290000": "Military technologies",
    "300000": "Multi/interdisciplinary studies",
    "310000": "Parks, recreation, leisure, and fitness studies",
    "380000": "Philosophy and religious studies",
    "390000": "Theology and religious vocations",
    "390602": "Divinity/ministry (BD, MDiv)",
    "390603": "Rabbinical studies",
    "390605": "Rabbinical studies (MHL/Rav)",
    "400000": "Physical sciences",
    "410000": "Science technologies/technicians",
    "420000": "Psychology",
    "430000": "Security and protective services",
    "440000": "Public administration and social service professions",
    "450000": "Social sciences",
    "460000": "Construction trades",
    "470000": "Mechanic and repair technologies/technicians",
    "480000": "Precision production",
    "490000": "Transportation and materials moving",
    "500000": "Visual and performing arts",
    "510000": "Health professions and related clinical sciences",
    "510101": "Chiropractic (DC)",
    "510401": "Dentistry (DDS, DMD)",
    "511201": "Medicine (MD)",
    "511701": "Optometry (OD)",
    "511901": "Osteopathic medicine/osteopathy (DO)",
    "512001": "Pharmacy (PharmD [USA] PharmD, BS/BPharm [Canada])",
    "512101": "Podiatric medicine/podiatry (DPM)",
    "512401": "Veterinary medicine (DVM)",
    "512704": "Naturopathic medicine",
    "520000": "Business, management, marketing, and related support services",
    "540000": "History (new)",
    "950000": "Undesignated field of study",
    "-1": "Missing/not reported",
    "-2": "Not applicable",
    "-3": "Suppressed data"
}

def get_cip_codes(
    search_term: Optional[str] = None,
    cip_codes: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Get CIP code information from IPEDS data.
    
    Args:
        search_term: Optional search term to filter CIP code names (case-insensitive)
        cip_codes: Optional CIP code(s) to look up specific codes - list of strings
        
    Returns:
        List of dictionaries containing CIP code information with fields:
        - code: CIP code
        - name: CIP code description
    """
    results = []
    
    # If specific codes are requested
    if cip_codes:
        for code in cip_codes:
            if str(code) in CIP_CODES:
                results.append({
                    'code': code,
                    'name': CIP_CODES[str(code)]
                })
    else:
        # Return all CIP codes
        for code, name in CIP_CODES.items():
            results.append({
                'code': code,
                'name': name
            })
    
    # Filter by search term if provided
    if search_term:
        search_lower = search_term.lower()
        results = [item for item in results if search_lower in item['name'].lower()]
    
    return results