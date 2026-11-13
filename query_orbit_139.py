import requests
import json

# Search URL for CMR
url = "https://cmr.earthdata.nasa.gov/search/granules.umm_json"

# Try searching just by relative orbit and collection to see if we get anything
params = {
    "collection_concept_id": "C2854338529-ASF",
    "attribute[]": "string,RELATIVE_ORBIT,139",
    "page_size": 100
}

response = requests.get(url, params=params)
data = response.json()

if 'items' in data:
    print(f"Found {len(data['items'])} granules with relative orbit 139")
    for item in data['items'][:5]: # Print first 5
        print(item['umm']['GranuleUR'])
else:
    print("No granules found with that attribute.")
