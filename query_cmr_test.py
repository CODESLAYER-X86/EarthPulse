import requests
import json

# Target Metadata
# GranuleId: NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001
# Cycle: 033
# Relative orbit: 139
# Orbit direction: Descending
# Frame: 092
# Collection: NISAR_L2_GCOV_PROVISIONAL_V1 (ID: C2854338529-ASF)

# Search URL for CMR
# We can search by collection ID, relative orbit, and frame.
url = "https://cmr.earthdata.nasa.gov/search/granules.umm_json"

params = {
    "collection_concept_id": "C2854338529-ASF",
    "readable_granule_name[]": "NISAR_L2_PR_GCOV_*_139_*_092_*",
    "page_size": 100
}

# The field readable_granule_name doesn't seem to support wildcards like that directly in all APIs, 
# but let's try search by temporal or just all and filter in Python
# Actually, CMR supports specific parameters for orbit/frame if mapped.
# Let's try basic query first and filter.

response = requests.get(url, params=params)
data = response.json()

if 'items' in data:
    print(f"Found {len(data['items'])} granules")
    for item in data['items']:
        print(item['umm']['GranuleUR'])
else:
    print("No granules found.")
