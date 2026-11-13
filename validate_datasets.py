import json
from shapely.wkt import loads

# Load the candidates
with open("verified_candidates.json", "r") as f:
    candidates = json.load(f)

# The reference granule footprint
# Based on the previous grep results for the reference granule (or one similar), 
# I need to extract the footprint for the reference granule.
# The reference granule is: NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001
# Let's search verified_candidates.json for this specific granule to get its footprint.

ref_id = "NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001"
ref_footprint_wkt = None
for c in candidates:
    # Need to check in raw field too if needed, but looks like they are inside raw
    if c.get('raw', {}).get('granuleName') == ref_id:
        ref_footprint_wkt = c.get('raw', {}).get('stringFootprint')
        break

if not ref_footprint_wkt:
    # Fallback/Error if not found
    print(f"Error: Could not find reference granule {ref_id} or its footprint in verified_candidates.json")
    exit(1)

ref_geom = loads(ref_footprint_wkt)

results = []

for c in candidates:
    if c['granule'] == ref_id:
        continue # Skip reference

    # Access stringFootprint from the 'raw' dictionary
    footprint_wkt = c.get('raw', {}).get('stringFootprint')
    if not footprint_wkt:
        results.append({"granule": c['granule'], "overlap": "No footprint"})
        continue

    geom = loads(footprint_wkt)
    
    # Calculate intersection and percentage
    intersection = ref_geom.intersection(geom)
    overlap_area = intersection.area
    ref_area = ref_geom.area
    overlap_pct = (overlap_area / ref_area) * 100
    
    results.append({
        "granule": c['granule'],
        "cycle": c['cycle'],
        "overlap_pct": overlap_pct
    })

# Output results
print(json.dumps(results, indent=2))
