import asf_search as asf
import json

# Search query
results = asf.search(
    relativeOrbit=[139],
    frame=[50],
    platform=['NISAR'],
    processingLevel=['GCOV'],
    flightDirection='DESCENDING'
)

print(f"Found {len(results)} results")
report_data = []
for r in results:
    props = r.properties
    filename = props.get('fileName', '')
    # Filename format: NISAR_L2_PR_GCOV_CCC_139_D_050...
    # parts: [0:NISAR, 1:L2, 2:PR, 3:GCOV, 4:Cycle, ...]
    parts = filename.split('_')
    cycle = parts[4] if len(parts) > 4 else 'N/A'

    report_data.append({
        "fileName": filename,
        "acquisitionDate": props.get('startTime'),
        "cycle": cycle,
        "relativeOrbit": props.get('pathNumber'),
        "direction": props.get('flightDirection'),
        "frame": props.get('frameNumber'),
        "mainPol": props.get('mainBandPolarization'),
        "sidePol": props.get('sideBandPolarization'),
        "version": props.get('crid'),
        "url": props.get('url'),
        "geometry": r.geometry
    })

with open("asf_results.json", "w") as f:
    json.dump(report_data, f, indent=2)
