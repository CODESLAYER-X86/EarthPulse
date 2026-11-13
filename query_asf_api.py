import requests
import json

url = "https://api.daac.asf.alaska.edu/services/search/param"
params = {
    "platform": "NISAR",
    "processingLevel": "GCOV",
    "relativeOrbit": 139,
    "frame": 92,
    "output": "json"
}

response = requests.get(url, params=params)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    try:
        data = response.json()
        print(f"Found {len(data)} results")
        if data:
            with open("asf_api_results.json", "w") as f:
                json.dump(data, f, indent=2)
            print("Saved results to asf_api_results.json")
            for item in data[:5]:
                print(item.get('granuleName') or item.get('fileName'))
    except Exception as e:
        print("Failed to parse JSON:", e)
        print(response.text[:500])
else:
    print(response.text[:500])
