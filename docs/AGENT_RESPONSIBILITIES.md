# Agent Responsibilities — Dancing with SARs

| Agent | Core Role | Scope / Deliverables | Boundaries |
| :--- | :--- | :--- | :--- |
| **Antigravity (Gemini 3.8 Flash)** | Application Architect & Lead Developer | Main application (FastAPI backend + React frontend), MapLibre GL map, UI/UX, Recharts data visualization, REST APIs, system coordination. | Does not waste tokens running local test loops or extraction jobs that OpenCode can run; does not write ML clustering algorithms. |
| **OpenCode** | Scientific Data Engineer & Execution QA | HDF5 windowed extraction, GeoTIFF generation, dB conversion, temporal differencing, common-valid masking, executing scripts, local test runs, and verifying ML outputs. | Does not build UI or independently redesign the ML/backend architecture. |
| **Claude.ai (Web App)** | Machine Learning Specialist | Standalone Python ML engine (`ml_engine/`): MiniBatch K-Means, statistical change detection, thresholding, clustering evaluation, model artifacts. | Runs in web app; does not interact directly with local disk or application server. |

---

## Shared Contracts
- Single source of truth for spatial data: `data/ml/feature_metadata.json` and `data/project_manifest.json`.
- All agents use the established 12-feature ordering and convention.
- No agent may invent synthetic scientific data or present unverified classifications as ground truth.
