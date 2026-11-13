# PART 5 OF 12 — Backend Architecture and Data-Service Design



Application architecture

Antigravity implementation



## 5.1 Backend's responsibility

The backend will connect the scientific processing pipeline to the web application.

It must handle five responsibilities:

1. Data access: Locate and read the prepared NISAR datasets and processed rasters.
2. API services: Provide acquisition metadata, change statistics, ML results, and map layers.
3. Analysis orchestration: Start or retrieve processing jobs when needed.
4. Geospatial delivery: Serve raster previews or tiles without transferring entire GeoTIFFs to the browser.
5. Reliability: Validate requests, report errors, and preserve scientific provenance.

The frontend should never need to understand HDF5 internals or implement SAR calculations.

Think of the backend as a restaurant's kitchen: the frontend takes orders, the backend prepares or retrieves the requested result, and the user receives a finished product.

## 5.2 Recommended architecture

For the three-day implementation window, I recommend a Python FastAPI backend, with a static or independently developed frontend.

Why FastAPI?

- It integrates naturally with the Python geospatial and ML ecosystem.
- It supports typed request and response schemas.
- It automatically generates OpenAPI documentation.
- It can expose the local ML engine through HTTP.
- It avoids introducing a separate backend language and runtime.

FRONTEND — Antigravity

Interactive map · Timeline · Charts · Analysis controls

HTTP / JSON / raster tiles

FASTAPI BACKEND

Metadata API

Raster API

Analysis API

ML Results API

DATA SERVICE

GeoTIFF · JSON · CSV

ML SERVICE

Model artifacts · Predictions

LOCAL DATA STORAGE

Prepared NISAR rasters · ML outputs · Metadata · Reports

## 5.3 Recommended backend technology stack

| Component              | Technology                   | Purpose                        |
| ---------------------- | ---------------------------- | ------------------------------ |
| Backend framework      | FastAPI                      | HTTP API                       |
| Server                 | Uvicorn                      | ASGI application server        |
| Geospatial access      | Rasterio                     | GeoTIFF reading                |
| Scientific computation | NumPy                        | Array operations               |
| Data validation        | Pydantic                     | Request/response validation    |
| ML integration         | Python module invocation     | Execute or retrieve ML results |
| Metadata storage       | JSON initially               | Lightweight metadata           |
| Statistics             | JSON/CSV                     | Analysis results               |
| Raster delivery        | Raster tiles or PNG previews | Map visualization              |
| API documentation      | OpenAPI/Swagger              | Testing and documentation      |

Do not introduce PostgreSQL, Redis, Celery, Kubernetes, or a separate microservice architecture for this prototype.

Those technologies may be useful in a larger production system, but they add deployment and debugging work without solving an immediate requirement.

A simple local FastAPI service is sufficient.

## 5.4 Backend project structure

The backend should remain separate from the ML engine.

Recommended layout:

```
backend/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── health.py
│   │   ├── metadata.py
│   │   ├── acquisitions.py
│   │   ├── layers.py
│   │   ├── statistics.py
│   │   ├── changes.py
│   │   ├── ml.py
│   │   └── reports.py
│   │
│   ├── services/
│   │   ├── data_service.py
│   │   ├── raster_service.py
│   │   ├── statistics_service.py
│   │   ├── ml_service.py
│   │   └── report_service.py
│   │
│   ├── schemas/
│   │   ├── metadata.py
│   │   ├── acquisition.py
│   │   ├── layer.py
│   │   └── analysis.py
│   │
│   └── utils/
│       ├── paths.py
│       ├── validation.py
│       └── errors.py
│
├── tests/
│   ├── test_health.py
│   ├── test_metadata.py
│   ├── test_layers.py
│   └── test_statistics.py
│
├── requirements.txt
└── README.md
```

The API routes should be thin. They receive requests, validate them, call services, and return responses. Actual raster reading and calculations belong in the service layer.

## 5.5 API design — exact endpoints

The frontend needs predictable endpoints. Antigravity should implement these contracts rather than inventing API structures independently.

### A. System and project metadata

| Method | Endpoint                    | Purpose                     |
| ------ | --------------------------- | --------------------------- |
| GET    | `/api/health`               | Check backend availability  |
| GET    | `/api/project`              | Project information         |
| GET    | `/api/project/aoi`          | Study-area metadata         |
| GET    | `/api/acquisitions`         | Available NISAR dates       |
| GET    | `/api/acquisitions/{cycle}` | Details for one acquisition |

Example response for `/api/acquisitions`:

```
{
  "acquisitions": [
    {
      "cycle": 28,
      "date": "2026-08-22",
      "polarizations": ["HH", "HV"],
      "available": true
    },
    {
      "cycle": 32,
      "date": "2026-10-09",
      "polarizations": ["HH", "HV"],
      "available": true
    },
    {
      "cycle": 33,
      "date": "2026-10-21",
      "polarizations": ["HH", "HV"],
      "available": true
    }
  ]
}
```

The dates and cycles are based on the dataset preparation information already reported. The backend must derive availability from actual files and metadata, not simply return this hardcoded example.

### B. Raster layer API

| Method | Endpoint                                       | Purpose               |
| ------ | ---------------------------------------------- | --------------------- |
| GET    | `/api/layers`                                  | List available layers |
| GET    | `/api/layers/{layer_id}/metadata`              | Layer metadata        |
| GET    | `/api/layers/{layer_id}/preview`               | Small raster preview  |
| GET    | `/api/layers/{layer_id}/tiles/{z}/{x}/{y}.png` | Map tile              |
| GET    | `/api/layers/{layer_id}/statistics`            | Raster statistics     |

Possible layer identifiers:

```
hh_028
hv_028
hh_032
hv_032
hh_033
hv_033

hh_diff_028_032
hh_diff_032_033
hh_diff_028_033

hv_diff_028_032
hv_diff_032_033
hv_diff_028_033

cluster_map
hh_change_categories
hv_change_categories
```

These identifiers should map to approved files in a server-side registry. Never allow the frontend to send an arbitrary filesystem path.

### C. Statistics API

| Method | Endpoint                   | Purpose                    |
| ------ | -------------------------- | -------------------------- |
| GET    | `/api/statistics/overview` | Overall dataset statistics |
| GET    | `/api/statistics/temporal` | Changes between dates      |
| GET    | `/api/statistics/area`     | Area calculations          |
| GET    | `/api/statistics/clusters` | ML cluster distribution    |

Example:

```
{
  "comparison": "028_to_033",
  "polarization": "HH",
  "valid_pixel_count": 125000,
  "stable_pixel_count": 90000,
  "increased_pixel_count": 15000,
  "decreased_pixel_count": 20000,
  "resolution_m": 10
}
```

The numbers above are placeholders, not actual findings.

For area calculations:

\\[ A\_{\text{km}^2} = \frac{N\_{\text{valid pixels}}\times 100}{1,000,000} \\]

At 10 m × 10 m resolution, one valid pixel represents 100 m², or 0.0001 km².

Always calculate the denominator using the appropriate valid-pixel mask. Do not calculate change percentages using invalid or unobserved pixels.

### D. ML API

| Method | Endpoint                    | Purpose                      |
| ------ | --------------------------- | ---------------------------- |
| GET    | `/api/ml/status`            | Check ML result availability |
| GET    | `/api/ml/metadata`          | Model metadata               |
| GET    | `/api/ml/clusters`          | Cluster statistics           |
| GET    | `/api/ml/change`            | Statistical change results   |
| GET    | `/api/ml/layers`            | Available ML layers          |
| GET    | `/api/ml/layers/{layer_id}` | Layer details                |

For this prototype, the ML API should primarily serve existing outputs. It should not automatically retrain the model whenever a user opens the application.

### E. Reports API

| Method | Endpoint                  | Purpose                    |
| ------ | ------------------------- | -------------------------- |
| GET    | `/api/reports`            | List reports               |
| GET    | `/api/reports/execution`  | Processing report          |
| GET    | `/api/reports/validation` | Validation report          |
| GET    | `/api/reports/dataset`    | Dataset preparation report |

The frontend should be able to display the report contents or provide a link to download them.

## 5.6 Raster delivery — the most important geospatial backend decision

Your raster dimensions are approximately 32,472 × 33,336 pixels per full granule, according to the reported metadata.

Even one float32 band at that size occupies approximately:

\\[ 32,472 \times 33,336 \times 4 \approx 4.33\text{ GB} \\]

That is the uncompressed size of one full band. A frontend must never receive the entire raster as a normal API response.

There are three possible delivery methods.

[How to Clip a Raster to a Polygon or an Extent with Python (Extract by Mask) | by Konrad Hafen | Medium](https://images.openai.com/static-rsc-4/F8AVFpfii9buBwZtnTyUxnK7rYZeu0rREm4tFjGTPBXYhf2N8C5YCkTrPtUDznPOC009xWR9Kk-MA7C7n2HF2Ev04P1WBXMtWEMYC2fP4supMt8q_TIRxu-4_RkxbkTUbtgQfrMAZIzRENQaEnlIqsuwQZZk4umcDg_YXGCE4f8?purpose=inline)

Option A — PNG previews

Essential MVP

- Generate small images from processed rasters.
- Display quickly in the application.
- Suitable for initial layer previews and report figures.
- Not suitable for detailed interactive map navigation.

[French imagery ready for your next project with MapTiler | MapTiler](https://images.openai.com/static-rsc-4/sv5kowsLvcflIdEe1RwIRr7FGINMQbiVXLk-j5OeMRmj3zZwn8QAMW32u9PE1rGKrsWnZRJs27IPmM-JDkoV4IjEBsQWiIqC3ohvIXIzOnksBZARSEC7a5BwxKy3oO5ArLF1KuNyDXbGQa9I_rM53Mqi_l-rH0YNhaaOQ6kI760?purpose=inline)

Option B — Raster tiles

Recommended map delivery

- Serve individual map tiles.
- Load only the visible geographic area.
- Support zoom and pan.
- Avoid sending the entire GeoTIFF.

[How to Add Satellite Imagery to QGIS (Free & Easy Guide)](https://images.openai.com/static-rsc-4/nsf3syiNQMgODvyfF0J_JSRjobvqQk6hxZhQ_bAcgU3M6DmjykBv3Jw8KH_T5xFrcs-q09zs_eWpzQXq3QfuSqifJ6LYp8N2rCGXZK533qBbd9u-8vgN67h2VKHj5BRlM8NkVp4N8pq6GubEV28vt7tuuEpeDct5BHrpgTJqQ-4?purpose=inline)

Option C — Direct GeoTIFF download

Download feature

- Provide original processed raster files.
- Useful for researchers and GIS software.
- Not intended for ordinary browser rendering.

### Recommended implementation

Use:

- PNG previews for the dashboard and layer thumbnails.
- Raster tiles for the interactive map.
- GeoTIFF downloads for research and reproducibility.

For raster tiles, Antigravity can implement a tile endpoint using Rasterio and a suitable reprojection/resampling workflow.

A useful alternative is to pre-generate tiles for the small AOI during preprocessing. This can simplify the backend and reduce repeated computation.

Important CRS consideration: Your reported source CRS is EPSG:32725, whereas many web-map libraries expect EPSG:3857 tiles. The backend must correctly reproject data or tiles. It must not simply label EPSG:32725 coordinates as EPSG:3857.

For a three-day deadline, I would first make PNG previews work, then add tiled delivery if the map requires zoomable raster layers.

## 5.7 Layer registry and metadata

Create a central file:

`backend/data/layer_registry.json`

Example:

```
{
  "layers": [
    {
      "id": "hh_033",
      "name": "HH Backscatter",
      "date": "2026-10-21",
      "cycle": 33,
      "polarization": "HH",
      "type": "backscatter",
      "unit": "dB",
      "path": "data/processed/hh_033_db.tif",
      "available": true
    },
    {
      "id": "hv_033",
      "name": "HV Backscatter",
      "date": "2026-10-21",
      "cycle": 33,
      "polarization": "HV",
      "type": "backscatter",
      "unit": "dB",
      "path": "data/processed/hv_033_db.tif",
      "available": true
    }
  ]
}
```

This is an example schema; actual paths and availability must be generated from the files produced by OpenCode.

The registry provides a single source of truth for the frontend.

For example, if a layer does not exist, the backend should report it as unavailable rather than returning a broken image.

## 5.8 Backend-to-ML communication

There are two possible approaches.

| Approach             | How it works                   | Recommendation                         |
| -------------------- | ------------------------------ | -------------------------------------- |
| Direct Python import | Backend calls ML functions     | Good for lightweight operations        |
| Separate process     | Backend starts ML CLI commands | Better isolation for long-running work |

I recommend a hybrid approach.

- Import lightweight functions for reading metadata and statistics.
- Use a separate process for expensive ML fitting or inference.
- Serve completed model outputs through the ordinary API.

The backend should not block all incoming requests while a model is fitting.

### Analysis job lifecycle

If you add a Run Analysis button, the backend should use a job lifecycle:

POST /api/analysis/jobs

Request analysis

Job created

Return a job ID

Worker process

Execute the ML or statistical pipeline

Save outputs and execution report

Job completed

Frontend retrieves results

Suggested endpoints:

```
POST /api/analysis/jobs
GET  /api/analysis/jobs/{job_id}
GET  /api/analysis/jobs/{job_id}/results
```

Possible statuses:

```
queued
running
completed
failed
cancelled
```

For this prototype, a lightweight subprocess and JSON job-status file are sufficient. Do not introduce a distributed task queue.

If all analysis is already completed before the demonstration, you can omit job execution entirely and serve the precomputed results. That is the lower-risk option.

## 5.9 File access and security

Even though this is a local scientific application, file access should be controlled.

### Required protections

1. No arbitrary paths: The browser can request a layer ID, not a filesystem path.
2. Path validation: Resolve registered paths and ensure they remain inside the approved project data directory.
3. Read-only scientific inputs: The API should not modify original NISAR HDF5 granules.
4. Controlled outputs: Write generated files only into designated output directories.
5. Input validation: Validate cycle IDs, layer IDs, dates, and request parameters.
6. Safe subprocess execution: Use argument arrays rather than constructing shell commands from user input.
7. Error sanitization: Do not expose full filesystem paths, environment variables, or stack traces to ordinary frontend users.

For example, the backend should accept:

```
GET /api/layers/hh_033/metadata
```

It should not accept:

```
GET /api/file?path=/home/user/private/file
```

This is a basic application-security boundary, even for a demonstration.

## 5.10 Backend configuration

Use a single configuration file or environment variables.

Recommended:

`backend/.env.example`

```
APP_NAME=Dancing with SARs
APP_ENV=development
API_HOST=127.0.0.1
API_PORT=8000

PROJECT_ROOT=.
DATA_ROOT=./data
PROCESSED_ROOT=./data/processed
ML_OUTPUT_ROOT=./ml_engine/outputs

ENABLE_ANALYSIS_EXECUTION=false
ENABLE_FILE_DOWNLOADS=true
```

The actual `.env` should not be committed if it contains secrets. This project should not need API keys for its core offline demonstration.

### CORS

If Antigravity produces a frontend running on a different local port, configure CORS for that exact development origin.

For example:

```
http://localhost:5173
```

Do not use unrestricted wildcard origins with credentials.

If frontend and backend are served from the same origin in the final demo, CORS may not be necessary.

## 5.11 Performance and memory management

Your computer has 16 GB RAM. The backend must not accidentally duplicate large raster arrays in memory.

Recommended rules:

| Operation          | Requirement                            |
| ------------------ | -------------------------------------- |
| Raster reading     | Windowed Rasterio reads                |
| Raster writing     | Block-based writing                    |
| Preview generation | Downsample before returning            |
| Tile generation    | Process only requested tiles           |
| Statistics         | Use masked or windowed computation     |
| ML inference       | Separate worker process                |
| HTTP responses     | Return small JSON or image payloads    |
| Caching            | Cache small metadata and previews only |

Additional requirements:

- Reuse raster datasets carefully.
- Close file handles after operations.
- Avoid loading multiple full-resolution bands simultaneously.
- Avoid keeping large NumPy arrays in global variables.
- Set reasonable request and processing timeouts.
- Do not run multiple memory-intensive ML jobs simultaneously.

A useful analogy: the backend should behave like a water tap, delivering only the amount of data requested, rather than opening a dam and flooding the entire application.

## 5.12 Error response format

Every API should return predictable error structures.

Example:

```
{
  "error": {
    "code": "LAYER_NOT_AVAILABLE",
    "message": "The requested raster layer is unavailable.",
    "details": {
      "layer_id": "cluster_map"
    }
  }
}
```

Recommended error codes:

| Code                  | Meaning                     |
| --------------------- | --------------------------- |
| `DATASET_NOT_FOUND`   | Required dataset missing    |
| `LAYER_NOT_AVAILABLE` | Requested layer unavailable |
| `INVALID_LAYER_ID`    | Unknown layer               |
| `INVALID_PARAMETER`   | Invalid request parameter   |
| `RASTER_READ_ERROR`   | Raster could not be read    |
| `CRS_MISMATCH`        | Unexpected CRS              |
| `ANALYSIS_NOT_READY`  | Results not yet generated   |
| `ANALYSIS_FAILED`     | Processing failed           |
| `INTERNAL_ERROR`      | Unexpected server error     |

Do not return HTTP 200 for failed operations.

## 5.13 Backend acceptance criteria

Antigravity should not consider the backend complete merely because the server starts.

It must pass these tests:

| Test                | Acceptance condition                                     |
| ------------------- | -------------------------------------------------------- |
| Health check        | Returns successful status                                |
| Project metadata    | Returns correct project information                      |
| Acquisition listing | Reflects actual available datasets                       |
| Layer listing       | Lists only registered, available layers                  |
| Layer metadata      | Returns correct CRS, dimensions, resolution and date     |
| Preview             | Returns a valid image                                    |
| Statistics          | Uses correct valid-pixel denominators                    |
| ML status           | Reports actual artifact availability                     |
| Report endpoint     | Retrieves existing reports                               |
| Invalid layer       | Returns controlled error                                 |
| Missing file        | Reports unavailable data without crashing                |
| Path traversal      | Cannot access arbitrary files                            |
| Memory behavior     | Does not load full source granules for ordinary requests |

A particularly important check: compare backend-reported raster metadata with the original GeoTIFF metadata. The backend must not silently change the coordinate system or spatial extent.

## 5.14 Final Antigravity backend implementation assignment

# ANTIGRAVITY DEVELOPMENT TASK — NISAR BACKEND

## Project

Dancing with SARs — NASA Space Apps 2026

## Your responsibility

Implement the application backend using Python FastAPI.

The backend must connect the frontend to locally prepared NISAR datasets, processed geospatial rasters, statistical results, ML outputs, and scientific reports.

The Python ML engine is developed separately and must not be rewritten inside the backend.

## 1. Technology

Use:

- FastAPI
- Uvicorn
- Pydantic
- Rasterio
- NumPy
- Python logging

Use a lightweight architecture suitable for a local offline demonstration.

Do not introduce unnecessary databases, distributed queues, or microservices.

## 2. Project structure

Implement separate:

- API routes
- Service modules
- Request/response schemas
- Configuration
- Utilities
- Tests

Keep API routes thin and put raster operations in service modules.

## 3. Required APIs

System:

- GET /api/health
- GET /api/project
- GET /api/project/aoi

Acquisitions:

- GET /api/acquisitions
- GET /api/acquisitions/{cycle}

Layers:

- GET /api/layers
- GET /api/layers/{layer_id}/metadata
- GET /api/layers/{layer_id}/preview
- GET /api/layers/{layer_id}/tiles/{z}/{x}/{y}.png
- GET /api/layers/{layer_id}/statistics

Analysis:

- GET /api/statistics/overview
- GET /api/statistics/temporal
- GET /api/statistics/area
- GET /api/statistics/clusters

ML:

- GET /api/ml/status
- GET /api/ml/metadata
- GET /api/ml/clusters
- GET /api/ml/change
- GET /api/ml/layers

Reports:

- GET /api/reports
- GET /api/reports/execution
- GET /api/reports/validation
- GET /api/reports/dataset

Implement only endpoints that have meaningful underlying data. Return explicit unavailable states when outputs do not exist.

## 4. Raster handling

Use Rasterio.

Preserve:

- CRS
- Transform
- Resolution
- Dimensions
- NoData
- Spatial extent

Use windowed reads and appropriate resampling.

Never transmit full-resolution GeoTIFF arrays through ordinary JSON endpoints.

Implement:

- PNG previews
- Raster tile delivery if feasible
- GeoTIFF downloads where appropriate

Correctly reproject EPSG:32725 data for web-map tile delivery. Never mislabel CRS.

## 5. Layer registry

Create a centralized JSON registry.

Register layers by stable IDs, not user-provided filesystem paths.

Verify file existence before reporting a layer as available.

## 6. ML integration

Read ML metadata and outputs from the separate ML engine.

Do not automatically retrain models on application startup.

If analysis execution is implemented, run long jobs outside the HTTP request thread and expose job status.

For a precomputed demonstration, prioritize reading completed results over executing expensive analysis.

## 7. Security

- Prevent arbitrary file access.
- Validate layer identifiers and request parameters.
- Restrict file access to approved project directories.
- Use safe subprocess argument handling.
- Do not expose secrets or internal stack traces.
- Configure CORS for the actual frontend origin.

## 8. Performance

Target a local machine with 16 GB RAM.

Use windowed raster reads, downsampled previews, controlled caching, and bounded processing concurrency.

Avoid unnecessary full-raster arrays and simultaneous ML jobs.

## 9. Error handling

Use consistent JSON error responses and correct HTTP status codes.

Handle missing data, missing ML artifacts, invalid layers, CRS mismatches, and raster-read failures without crashing the service.

## 10. Tests

Create tests for:

- Health endpoint
- Project metadata
- Acquisition availability
- Layer registry
- Raster metadata
- Preview generation
- Statistics
- ML artifact availability
- Invalid requests
- Path traversal protection

## 11. Delivery

Provide:

- Complete backend source code
- requirements.txt
- .env.example
- README
- API documentation
- Automated tests
- Local execution instructions

The application must work without paid cloud infrastructure or external API dependencies.

## 12. Critical instruction

Inspect the existing project files before implementing.

Reuse the actual paths, reports, feature metadata, and raster outputs produced by OpenCode.

Do not invent data, dates, AOI coordinates, raster statistics, or ML results.

Keep the backend compatible with the frontend integration contract.

## 5.15 Implementation priority for the remaining three days

Do not implement every backend feature at once. Build in this order:

Priority 1 — Core backend

Must have

- FastAPI startup and health check.
- Project and acquisition metadata.
- Layer registry.
- Raster metadata and PNG previews.
- Change statistics.

Priority 2 — Scientific integration

Important

- ML artifact access.
- Cluster statistics.
- Analysis reports.
- GeoTIFF downloads.

Priority 3 — Advanced functionality

If time permits

- Interactive raster tiles.
- Analysis job execution.
- Job cancellation and progress tracking.
- Advanced caching.

My recommendation: Get the backend serving real NISAR previews and statistics before implementing advanced raster tiling. The actual satellite data and scientific comparison are more important than sophisticated server infrastructure.

## Part 5 completion checklist

- FastAPI architecture defined.
- Backend directory structure defined.
- API endpoints specified.
- Raster delivery strategy selected.
- CRS handling specified.
- Layer registry defined.
- ML integration defined.
- Analysis job lifecycle designed.
- File-access security specified.
- Performance requirements defined.
- Error handling and tests specified.
- Antigravity implementation assignment prepared.

Next: Part 6 — Frontend Architecture and UI/UX Design.

We will design the actual application interface: the dashboard, interactive NISAR map, acquisition timeline, HH/HV visualization controls, comparison workspace, ML results panel, and scientific reporting interface.

The objective is to make the application feel like a professional Earth-observation analysis platform rather than a generic dashboard with a satellite image placed inside it.

