import asf_search as asf
import os

os.makedirs("data", exist_ok=True)

target_granules = [
    "NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001",
    "NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001"
]

results = asf.granule_search(target_granules)
print(f"Found {len(results)} granules for download.")

for r in results:
    print(f"Downloading {r.properties['fileName']}...")
    r.download(path="./data")
print("Download complete.")
