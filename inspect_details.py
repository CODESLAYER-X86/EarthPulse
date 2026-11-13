import asf_search as asf
import json

results = asf.granule_search(['NISAR_L2_PR_GCOV_03*_139_D_050*'])

details = []
for r in results:
    p = r.properties
    details.append({
        "fileName": p.get('fileName'),
        "startTime": p.get('startTime'),
        "stopTime": p.get('stopTime'),
        "pathNumber": p.get('pathNumber'),
        "frameNumber": p.get('frameNumber'),
        "flightDirection": p.get('flightDirection'),
        "orbit": p.get('orbit'),
        "collectionName": p.get('collectionName'),
        "crid": p.get('crid'),
        "frameCoverage": p.get('frameCoverage'),
        "mainBandPolarization": p.get('mainBandPolarization'),
        "sideBandPolarization": p.get('sideBandPolarization'),
        "polarization": p.get('polarization'),
        "url": p.get('url'),
        "geometry": r.geometry
    })

print(json.dumps(details, indent=2))
