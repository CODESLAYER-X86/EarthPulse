import os
import requests
from asf_search import ASFSession

print("Checking ASFSession and environment...")
session = ASFSession()
# Check if netrc exists or can be found
netrc_path = os.path.expanduser("~/.netrc")
print(f"~/.netrc exists: {os.path.exists(netrc_path)}")

# Let's test a URL head request with ASFSession
url = "https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_032_139_D_050_0005_NASV_A_20261009T201350_20261009T201413_P05023_N_P_J_001/NISAR_L2_PR_GCOV_032_139_D_050_0005_NASV_A_20261009T201350_20261009T201413_P05023_N_P_J_001.h5"
try:
    resp = session.head(url, timeout=10)
    print(f"HTTP Status: {resp.status_code}")
except Exception as e:
    print(f"Exception: {e}")
