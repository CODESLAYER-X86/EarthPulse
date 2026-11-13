import json
from datetime import datetime

# Read the candidates
with open("verified_candidates.json", "r") as f:
    candidates = json.load(f)

# Define reference
ref_granule = "NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001"
ref_orbit = 139
ref_frame = 92
ref_dir = "DESCENDING"

# Sort candidates by time
candidates.sort(key=lambda x: x['startTime'])

results = []
for c in candidates:
    # Basic validation
    is_valid = True
    reasons = []
    
    if c['relativeOrbit'] != ref_orbit:
        is_valid = False
        reasons.append(f"Orbit mismatch: {c['relativeOrbit']}")
    if c['frame'] != ref_frame:
        is_valid = False
        reasons.append(f"Frame mismatch: {c['frame']}")
    if c['direction'] != ref_dir:
        is_valid = False
        reasons.append(f"Direction mismatch: {c['direction']}")
    
    # Polarization check (DHDH = HH/HV)
    main_pol = set(c.get('mainPol', []))
    ref_pol = {"HH", "HV"}
    if not ref_pol.issubset(main_pol):
        is_valid = False
        reasons.append(f"Polarization mismatch: {main_pol}")
        
    overlap_pct = "N/A"
    
    results.append({
        "cycle": c['cycle'],
        "date": c['startTime'],
        "granule": c['granule'],
        "orbit": c['relativeOrbit'],
        "frame": c['frame'],
        "polarization": c['mainPol'],
        "coverage": c['frameCoverage'],
        "overlap": overlap_pct,
        "verdict": "Confirmed" if is_valid else f"Rejected: {', '.join(reasons)}"
    })

# Format for output
with open("verified_repeat_observations.md", "w") as f:
    f.write("# Verified Repeat Observations\n\n")
    f.write("| Cycle | Date | Full Granule ID | Orbit | Frame | Polarization | Coverage | Overlap % | Verdict |\n")
    f.write("|---|---|---|---|---|---|---|---|---|\n")
    for r in results:
        f.write(f"| {r['cycle']} | {r['date']} | {r['granule']} | {r['orbit']} | {r['frame']} | {r['polarization']} | {r['coverage']} | {r['overlap']} | {r['verdict']} |\n")

print("Created verified_repeat_observations.md")
