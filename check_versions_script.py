import json

# Load verified_candidates.json
with open("verified_candidates.json", "r") as f:
    data = json.load(f)

# Define the cycles and frames to check (based on the initial setup)
# All are Relative Orbit 139, Descending, Frame 92, MainPol [HH, HV]
target_cycles = {"028", "032", "033"}

# To store found granules and their versions
found_versions = {}

for item in data:
    cycle = item.get("cycle")
    if cycle in target_cycles:
        granule = item.get("granule")
        version = item.get("pgeVersion")
        # Extract the processing version identifier from the granule name (e.g., P05036)
        # It's at the end, just before the 'N_F_J_001' part.
        parts = granule.split('_')
        # Based on: NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05036_N_F_J_001
        # The version is parts[-4]
        proc_id = parts[-4]
        
        if cycle not in found_versions:
            found_versions[cycle] = {}
        
        if proc_id not in found_versions[cycle]:
            found_versions[cycle][proc_id] = []
            
        found_versions[cycle][proc_id].append({"granule": granule, "version": version})

print(json.dumps(found_versions, indent=2))
