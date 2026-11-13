import json

with open("verified_candidates.json", "r") as f:
    data = json.load(f)

print(f"Total candidates: {len(data)}")
for item in data:
    print(f"Cycle: {item.get('cycle')}, Granule: {item.get('granule')}, PGE Version: {item.get('pgeVersion')}")
