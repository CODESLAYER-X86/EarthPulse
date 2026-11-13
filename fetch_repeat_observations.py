import requests
import json
from datetime import datetime

url = "https://api.daac.asf.alaska.edu/services/search/param"
params = {
    "platform": "NISAR",
    "processingLevel": "GCOV",
    "relativeOrbit": 139,
    "frame": 92,
    "flightDirection": "DESCENDING",
    "output": "json"
}

response = requests.get(url, params=params)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    # ASF API returns a list of lists or list of dicts
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
        items = data[0]
    elif isinstance(data, list):
        items = data
    else:
        items = [data]
        
    print(f"Found {len(items)} results for Orbit 139, Frame 92, Descending")
    
    records = []
    for item in items:
        # handle items whether dict or list
        if not isinstance(item, dict):
            continue
        granule = item.get('granuleName') or item.get('fileName')
        start_time = item.get('startTime')
        orbit = item.get('relativeOrbit') or item.get('pathNumber')
        frame = item.get('frameNumber')
        direction = item.get('flightDirection')
        download_url = item.get('downloadUrl') or item.get('url')
        
        # Extract cycle from granule name if possible, e.g. NISAR_L2_PR_GCOV_033_...
        cycle = "N/A"
        if granule:
            parts = granule.split('_')
            if len(parts) > 5:
                cycle = parts[4]
                
        nisar_meta = item.get('nisar', {})
        main_pol = nisar_meta.get('mainBandPolarization', [])
        side_pol = nisar_meta.get('sideBandPolarization', [])
        pge_version = nisar_meta.get('pgeVersion', item.get('version', 'N/A'))
        frame_coverage = nisar_meta.get('frameCoverage', 'N/A')
        geometry = item.get('geometry')
        
        records.append({
            "granule": granule,
            "cycle": cycle,
            "startTime": start_time,
            "relativeOrbit": orbit,
            "frame": frame,
            "direction": direction,
            "mainPol": main_pol,
            "sidePol": side_pol,
            "pgeVersion": pge_version,
            "frameCoverage": frame_coverage,
            "geometry": geometry,
            "downloadUrl": download_url,
            "raw": item
        })
        
    with open("verified_candidates.json", "w") as f:
        json.dump(records, f, indent=2)
    print(f"Saved {len(records)} records to verified_candidates.json")
else:
    print("Error:", response.text[:500])
