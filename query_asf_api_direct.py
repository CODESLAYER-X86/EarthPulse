import requests
import json

url = "https://search.asf.alaska.edu/api/v2/search"
params = {
    "platform": "NISAR",
    "processingLevel": "GCOV",
    "relativeOrbit": "139",
    "frame": "92",
    "flightDirection": "DESCENDING",
    "output": "json"
}

# The ASF API returns a list of results
response = requests.get(url, params=params)

if response.status_code == 200:
    results = response.json()
    with open("asf_results_api.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Successfully retrieved {len(results)} results.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    print(response.text)
