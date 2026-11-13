# NASA Earth Science Data: NISAR Granule Download Guide
**Project:** Dancing with SARs (EarthPulse) — NASA Space Apps Challenge 2026  
**Satellite Mission:** NASA-ISRO Synthetic Aperture Radar (NISAR)  
**Product Specification:** Level-2 Geocoded Polarimetric Covariance (L2 GCOV)  
**Product DOI:** [10.5067/NIL2GCOV-P1](https://doi.org/10.5067/NIL2GCOV-P1)  
**Study Area:** Potengi Estuary, Natal, Rio Grande do Norte, Brazil (Track 139, Frame 092)  

---

## 1. Verified NASA NISAR Granules Used in this Project

Our multi-temporal study utilizes three repeat-pass observations covering the exact same spatial grid footprint:

| Observation | Cycle | Acquisition Date | File Size | NASA Granule ID |
| :--- | :---: | :---: | :---: | :--- |
| **Baseline** | `028` | **2026-08-22** (20:37:40 UTC) | ~5.9 GB | `NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001` |
| **Intermediate** | `032` | **2026-10-09** (20:37:40 UTC) | ~5.9 GB | `NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001` |
| **Repeat Verification** | `033` | **2026-10-21** (20:37:40 UTC) | ~5.9 GB | `NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001` |

> [!NOTE]
> **Pre-Packaged Data:** All calibrated 10 m GeoTIFF subsets, validity masks, and ML artifacts are already included in `data/processed/`, so you do **not** need to download these 18 GB files to run the web application. Follow the instructions below only if you wish to re-process from the raw HDF5 files from scratch.

---

## 2. Prerequisite: Free NASA Earthdata Login

All NASA Earth Science Data requires a free **NASA Earthdata Login** account:
1. Go to [https://urs.earthdata.nasa.gov/](https://urs.earthdata.nasa.gov/).
2. Click **Register** to create a free account (takes 30 seconds).
3. Authorize the **Alaska Satellite Facility (ASF)** application in your account settings.

---

## 3. How to Download the Granules

### Method 1: Using the Automated Python Script (Recommended)

We provide an automated CLI script [`download_granules.py`](download_granules.py) in the root of the repository:

```bash
# 1. Install NASA's official ASF search library
pip install asf_search

# 2. Run the downloader with your Earthdata credentials
python download_granules.py --username YOUR_USERNAME --password YOUR_PASSWORD
```

*The script will query NASA CMR and download the three `.h5` files into `data/raw/`.*

---

### Method 2: NASA Earthdata Search (Web Interface)

1. Open **[NASA Earthdata Search](https://search.earthdata.nasa.gov/)**.
2. Log in with your NASA Earthdata account (top right).
3. In the search box, paste any of the Granule IDs:
   ```text
   NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001
   ```
4. Click on the matching granule and press **Download Data**.
5. Repeat for Cycle 032 and Cycle 033.

---

### Method 3: Alaska Satellite Facility (ASF Vertex)

1. Go to **[ASF Vertex](https://search.asf.alaska.edu/)**.
2. Set **Dataset** to `NISAR`.
3. In **Search Criteria**, set:
   - **Path (Relative Orbit):** `139`
   - **Frame:** `92`
   - **Processing Level:** `GCOV`
4. Select the three granules matching dates `2026-08-22`, `2026-10-09`, and `2026-10-21`.
5. Click **Add to Downloads** or download via the ASF Python metalink.

---

### Method 4: Direct Command-Line Download (`curl` / `wget`)

Create a `~/.netrc` file with your credentials:
```bash
cat << 'EOF' > ~/.netrc
machine urs.earthdata.nasa.gov login YOUR_USERNAME password YOUR_PASSWORD
EOF
chmod 600 ~/.netrc
```

Download directly using `curl`:
```bash
# Cycle 028 (Aug 22)
curl -b ~/.netrc -c ~/.netrc -L -O https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5

# Cycle 032 (Oct 09)
curl -b ~/.netrc -c ~/.netrc -L -O https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5

# Cycle 033 (Oct 21)
curl -b ~/.netrc -c ~/.netrc -L -O https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001/NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001.h5
```

---

## 4. How to Run the Pipeline with New Raw Data

Once downloaded, place the three `.h5` files into `data/` or `data/raw/`:

```bash
# 1. Run the SAR preprocessing, Enhanced Lee speckle filter & classification pipeline
python scripts/correct_sar_pipeline.py

# 2. Retrain the multi-temporal Machine Learning clustering engine
python ml_engine/run_ml.py run-all

# 3. Launch the interactive web platform to visualize the results
python run_app.py
```
Open **`http://localhost:8000`** in your browser.
