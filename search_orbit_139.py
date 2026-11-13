import asf_search as asf
import json

# Search for relative orbit 139 GCOV products
results = asf.search(
    platform=asf.PLATFORM.NISAR,
    processingLevel='L2_PR_GCOV',
    pathNumber=139
)

print(f"Total results for orbit 139: {len(results)}")
report_data = []
for r in results:
    props = r.properties
    filename = props.get('fileName', '')
    report_data.append({
        "fileName": filename,
        "acquisitionDate": props.get('startTime'),
        "relativeOrbit": props.get('pathNumber'),
        "url": props.get('url')
    })

with open("orbit_139_all.json", "w") as f:
    json.dump(report_data, f, indent=2)
