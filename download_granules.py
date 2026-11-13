#!/usr/bin/env python3
"""
NASA NISAR L2 GCOV Granule Downloader
Project: Dancing with SARs (EarthPulse) - NASA Space Apps Challenge 2026

Downloads the three verified repeat-pass NISAR L2 GCOV observation granules
covering the Potengi Estuary, Natal, Brazil directly from NASA Earthdata / ASF DAAC.

Requirements:
  pip install asf_search
  A free NASA Earthdata login (https://urs.earthdata.nasa.gov/)
"""

import os
import sys
import argparse

try:
    import asf_search as asf
except ImportError:
    print("Error: 'asf_search' is not installed.")
    print("Install it with: pip install asf_search")
    sys.exit(1)

# The 3 verified NISAR observation granules (Track 139, Frame 092)
GRANULES = [
    {
        "cycle": "028",
        "date": "2026-08-22",
        "role": "Baseline Observation",
        "granule_id": "NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001",
        "url": "https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5"
    },
    {
        "cycle": "032",
        "date": "2026-10-09",
        "role": "Intermediate Observation (48-Day Shift)",
        "granule_id": "NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001",
        "url": "https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"
    },
    {
        "cycle": "033",
        "date": "2026-10-21",
        "role": "Repeat Verification (12-Day Orbital Repeat)",
        "granule_id": "NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001",
        "url": "https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001/NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001.h5"
    }
]

def main():
    parser = argparse.ArgumentParser(description="Download NISAR L2 GCOV repeat granules from NASA Earthdata.")
    parser.add_argument("--output-dir", default="data/raw", help="Destination folder for .h5 files (default: data/raw)")
    parser.add_argument("--username", help="NASA Earthdata username (or set via EARTHDATA_USERNAME env var)")
    parser.add_argument("--password", help="NASA Earthdata password (or set via EARTHDATA_PASSWORD env var)")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 65)
    print("   NASA NISAR L2 GCOV Repeat Observation Downloader")
    print("   Study Area: Potengi Estuary, Natal, Brazil (Track 139, Frame 092)")
    print("=" * 65)

    granule_ids = [g["granule_id"] for g in GRANULES]
    print(f"Querying NASA ASF DAAC for {len(granule_ids)} granules...")

    results = asf.granule_search(granule_ids)
    print(f"Found {len(results)} matching granules in NASA CMR.")

    if not results:
        print("No granules found. You can also download them directly via URL:")
        for g in GRANULES:
            print(f"  - Cycle {g['cycle']}: {g['url']}")
        return

    username = args.username or os.environ.get("EARTHDATA_USERNAME")
    password = args.password or os.environ.get("EARTHDATA_PASSWORD")

    session = None
    if username and password:
        session = asf.ASFSession().auth_with_creds(username, password)
    else:
        print("\nNote: No Earthdata credentials provided in arguments.")
        print("asf_search will look for credentials in your ~/.netrc file.")

    for item in results:
        fname = item.properties.get("fileName")
        dest_path = os.path.join(args.output_dir, fname)
        if os.path.exists(dest_path):
            print(f"✓ Already downloaded: {fname}")
            continue

        print(f"\nDownloading: {fname} (~5.9 GB)...")
        try:
            if session:
                item.download(path=args.output_dir, session=session)
            else:
                item.download(path=args.output_dir)
            print(f"✓ Download complete: {dest_path}")
        except Exception as e:
            print(f"Download failed: {e}")
            print(f"Alternative direct URL: {item.properties.get('url')}")

if __name__ == "__main__":
    main()
