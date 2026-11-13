import requests
import json

# CMR Search URL
CMR_URL = "https://cmr.earthdata.nasa.gov/search/granules.json"

# Define the acquisitions to search for
# Cycle 028: 2026-08-22
# Cycle 032: 2026-10-09
# Cycle 033: 2026-10-21
targets = [
    {"cycle": "028", "date": "2026-08-22", "orbit": 139},
    {"cycle": "032", "date": "2026-10-09", "orbit": 139},
    {"cycle": "033", "date": "2026-10-21", "orbit": 139}
]

results = []

for target in targets:
    # Need to query for the same acquisition and look for alternative versions
    # Use the Orbit and Date as constraints
    params = {
        "provider": "POCLOUD",
        "short_name": "NISAR_L2_PR_GCOV",
        "temporal": f"{target['date']}T00:00:00Z,{target['date']}T23:59:59Z",
        "options[relative_orbit][pattern]": "true",
        "relative_orbit": target['orbit'],
        "page_size": 100
    }
    
    response = requests.get(CMR_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        for granule in data.get("feed", {}).get("entry", []):
            granule_id = granule.get("producer_granule_id")
            # We want to find versions that differ from the current known P05023/P05036
            # Current known: P05023 for 028, 032; P05036 for 033
            # We are searching for alternatives to these
            results.append({
                "cycle": target['cycle'],
                "granule": granule_id
            })
    else:
        print(f"Error querying CMR for {target['date']}: {response.status_code}")

print(json.dumps(results, indent=2))
