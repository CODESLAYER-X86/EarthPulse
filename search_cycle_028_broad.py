import asf_search as asf
import json

# Broader search for Cycle 028
# NISAR_L2_PR_GCOV_028_*
results = asf.granule_search(['NISAR_L2_PR_GCOV_028_*'])

report_data = []
for r in results:
    props = r.properties
    report_data.append({
        "fileName": props.get('fileName', ''),
        "cycle": '028',
        "relativeOrbit": props.get('pathNumber'),
        "url": props.get('url')
    })

with open("cycle_028_broad.json", "w") as f:
    json.dump(report_data, f, indent=2)

print(f"Found {len(report_data)} results for Cycle 028.")
