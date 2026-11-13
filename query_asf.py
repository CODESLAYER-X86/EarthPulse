import asf_search as asf
import json

print(f"ASF Search version: {asf.__version__}")

# Search using relative orbit 139, frame 50, descending, platform/processing level for NISAR GCOV
results = asf.search(
    platform='NISAR',
    processingLevel='GCOV',
    relativeOrbit=139,
    frame=50,
    flightDirection='DESCENDING'
)

print(f"Found {len(results)} results")

report_data = []
for r in results:
    props = r.properties
    # Extract cycle from filename if possible, it's not a direct property
    # Filename format: NISAR_L2_PR_GCOV_CCC_... where CCC is cycle
    filename = props.get('fileName', '')
    cycle = 'N/A'
    if filename:
        parts = filename.split('_')
        if len(parts) > 5:
            cycle = parts[5]

    print("---")
    print("Filename:", filename)
    print("Cycle:", cycle)
    print("Start Time:", props.get('startTime'))
    print("Relative Orbit:", props.get('relativeOrbit'))
    print("Frame:", props.get('frameNumber'))
    print("URL:", props.get('url'))
    
    # Store data for report
    report_data.append({
        "fileName": filename,
        "cycle": cycle,
        "startTime": props.get('startTime'),
        "relativeOrbit": props.get('relativeOrbit'),
        "frameNumber": props.get('frameNumber'),
        "flightDirection": props.get('flightDirection'),
        "url": props.get('url'),
        "version": props.get('version'),
        "geometry": r.geometry
    })

with open("asf_results.json", "w") as f:
    json.dump(report_data, f, indent=2)
