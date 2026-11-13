# TASK FOR OPENCODE: Launch & Verify "Dancing with SARs" Platform

## Objective
Verify the environment, execute the end-to-end integration tests, launch the local application server, and confirm that the web platform is live and healthy on port 8000.

## Working Directory
`/home/codeslayer_x86/CODESLAYER/projects/NASA`

---

## 1. Pre-Flight Verification
Before starting the server, run the automated integration test suite to verify data integrity, dynamic raster rendering, GeoJSON vector regions, and ML summaries:

```bash
./.venv/bin/python tests/test_integration.py
```
*Expected: 100% PASS RATE across all health, metadata, GeoJSON vector, raster rendering, and report endpoints.*

---

## 2. Launch the Application Server
Start the unified platform (FastAPI backend serving the React MapLibre SPA directly):

```bash
# Foreground launch:
./.venv/bin/python run_app.py

# Or background daemon launch:
nohup ./.venv/bin/python run_app.py > app.log 2>&1 &
```

---

## 3. Verify Server Status
Confirm the server is active and all scientific pipelines are ready:

```bash
curl -s http://localhost:8000/api/health
```

*Expected output:*
```json
{"status":"healthy","service":"Dancing with SARs Backend","data_ready":true,"filtered_ready":true,"classified_ready":true}
```

The application is accessible in the browser at:
- Web Application: **http://localhost:8000**
- Interactive Swagger API: **http://localhost:8000/docs**

---

## 4. Pipeline Reference Commands (If Re-execution is Needed)
- **Rebuild Frontend:** `cd frontend && npm run build && cd ..`
- **Re-run SAR Filtering & Vector Region Extraction:** `./.venv/bin/python scripts/correct_sar_pipeline.py`
- **Re-train / Re-run ML Pipeline:** `./.venv/bin/python ml_engine/run_ml.py run-all`

---

## Completion Report
Finish with a report matching the project protocol:

```
TASK: Launch & Verify Application
STATUS: PASS / PARTIAL / BLOCKED
PORT: 8000
HEALTH CHECK:
RESULT:
```
