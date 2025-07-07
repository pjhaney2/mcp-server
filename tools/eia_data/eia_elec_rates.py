import requests
import csv
import io
from typing import List, Dict, Any


def get_electricity_rates(zipcodes: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch electricity rates for specified zipcodes and return as a flat list. Data is from EIA's OpenEI for 2023. 
    Here is the link to all the data listings:https://data.openei.org/submissions/all, or in this case: https://data.openei.org/submissions/6225
    
    Args:
        zipcodes: List of zipcode strings to filter for
        
    Returns:
        List of dictionaries containing utility rate data with added 'utility_type' field
    """
    csv_urls = {
        "iou": "https://data.openei.org/files/6225/iou_zipcodes_2023.csv",
        "non_iou": "https://data.openei.org/files/6225/non_iou_zipcodes_2023.csv",
    }
    
    all_rates = []
    
    for utility_type, url in csv_urls.items():
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            csv_content = io.StringIO(response.text)
            reader = csv.DictReader(csv_content)
            
            for row in reader:
                if row.get("zip") in zipcodes:
                    # Add utility type to the row data
                    row["utility_type"] = utility_type
                    all_rates.append(row)
                    
        except requests.RequestException as e:
            print(f"Error fetching {utility_type} data: {e}")
            continue
    
    return all_rates

if __name__ == "__main__":
    zipcodes = ["60067", "60622"]
    rates = get_electricity_rates(zipcodes)
    print(rates)