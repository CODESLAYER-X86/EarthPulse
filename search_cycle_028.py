import asf_search as asf
import json

# Search for Cycle 028
results = asf.granule_search(['NISAR_L2_PR_GCOV_028_139_D_050*'])

report_data = []
for r in results:
    props = r.properties
    filename = props.get('fileName', '')

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
        "collection": props.get('collectionName'),
        "version": props.get('crid'),
        "frameCoverage": props.get('frameCoverage'),
        "geometry": r.geometry,
        "url": props.get('url')
    })

with open("asf_results_028.json", "w") as f:
    json.dump(report_data, f, indent=2)

print(f"Processed {len(report_data)} results.")
