import asf_search as asf
import json

# Target Metadata
# GranuleId: NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001
# Cycle: 033
# Relative orbit: 139
# Orbit direction: Descending
# Frame: 092
# Polarization: DHDH (HH/HV)

print("Searching for NISAR GCOV, RelOrbit 139, Frame 92, Descending...")

# Query ASF
# Note: Polarization in asf_search often uses just 'HH', 'HV', 'VV', etc.
# The request specified DHDH which implies dual-pol.
# Let's search by orbit and frame first, then filter for polarization if needed.
results = asf.search(
    platform='NISAR',
    processingLevel='GCOV',
    relativeOrbit=139,
    frame=92,
    flightDirection='DESCENDING'
)

print(f"Found {len(results)} results")

report_data = []
for r in results:
    props = r.properties
    filename = props.get('fileName', '')
    # Extract cycle from filename format: NISAR_L2_PR_GCOV_CCC_...
    parts = filename.split('_')
    cycle = parts[5] if len(parts) > 5 else 'N/A'

    report_data.append({
        "fileName": filename,
        "cycle": cycle,
        "startTime": props.get('startTime'),
        "relativeOrbit": props.get('relativeOrbit'),
        "frameNumber": props.get('frameNumber'),
        "flightDirection": props.get('flightDirection'),
        "polarization": props.get('polarization'),
        "url": props.get('url'),
        "geometry": r.geometry
    })

with open("asf_results_v3.json", "w") as f:
    json.dump(report_data, f, indent=2)
