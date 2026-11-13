import asf_search as asf
import os

os.makedirs("data", exist_ok=True)

target_granules = [
    "NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001"
]

# Remove the corrupted file first to ensure a clean download
file_path = "./data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"
if os.path.exists(file_path):
    print(f"Removing corrupted file: {file_path}")
    os.remove(file_path)

results = asf.granule_search(target_granules)
print(f"Found {len(results)} granule for Cycle 032.")

for r in results:
    print(f"Downloading {r.properties['fileName']}...")
    r.download(path="./data")
print("Download of Cycle 032 complete.")
