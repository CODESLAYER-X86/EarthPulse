import json
import re

with open('asf_api_results.json', 'r') as f:
    data = json.load(f)

# The data structure in asf_api_results.json is a list of lists of results.
# Based on the read output, it's a list containing one list of items.
results = data[0]

# Filter and extract data
extracted = []
for item in results:
    granule_name = item.get('granuleName')
    if not granule_name:
        continue
    
    # Extract cycle from granule name
    match = re.search(r'GCOV_(\d{3})_', granule_name)
    cycle = match.group(1) if match else "Unknown"
    
    start_time = item.get('startTime', 'Unknown')
    acquisition_date = start_time[:10] if start_time != 'Unknown' else 'Unknown'
    
    flight_dir = item.get('flightDirection', 'Unknown')
    frame = item.get('frameNumber', 'Unknown')
    footprint = item.get('stringFootprint', 'Unknown')
    
    # Simple check for DHDH in name
    pol = "DHDH" if "DHDH" in granule_name else "Unknown"
    
    extracted.append({
        'granule': granule_name,
        'date': acquisition_date,
        'cycle': cycle,
        'orbit_dir': flight_dir,
        'frame': frame,
        'pol': pol,
        'footprint': footprint,
        'url': item.get('downloadUrl', 'N/A')
    })

# Deduplicate based on granule name as there might be different versions
unique_granules = {}
for item in extracted:
    if item['granule'] not in unique_granules:
        unique_granules[item['granule']] = item

# Sort by date
sorted_granules = sorted(unique_granules.values(), key=lambda x: x['date'])

# Generate Markdown table
print("# NISAR Repeat Observation Report\n")
print("## Parameters")
print("- **Relative Orbit:** 139")
print("- **Frame:** 092")
print("- **Orbit Direction:** Descending")
print("- **Polarization:** DHDH\n")
print("## Confirmed Repeat Observations\n")
print("| Granule Name | Acquisition Date | Cycle | Direction | Frame | Pol | Download |")
print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
for item in sorted_granules:
    # Truncate granule name for readability
    short_name = f"{item['granule'][:25]}...{item['granule'][-15:]}"
    print(f"| {short_name} | {item['date']} | {item['cycle']} | {item['orbit_dir']} | {item['frame']} | {item['pol']} | [Link]({item['url']}) |")
