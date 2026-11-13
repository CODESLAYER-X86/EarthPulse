import json

with open("verified_candidates.json", "r") as f:
    data = json.load(f)

for item in data:
    granule = item.get("granule", "")
    version = item.get("pgeVersion", "N/A")
    if "P05023" in granule or "P05036" in granule:
        print(f"Granule: {granule}, Version: {version}")
