import json

with open("verified_candidates.json") as f:
    data = json.load(f)

print(f"Total verified candidates: {len(data)}")
cycles = set(item.get("cycle") for item in data)
print(f"Cycles available: {cycles}")

for item in data:
    if item.get("cycle") in ["028", "032", "033"]:
        print(f"Cycle: {item.get('cycle')} | Granule: {item.get('granule')} | URL: {item.get('downloadUrl')}")
