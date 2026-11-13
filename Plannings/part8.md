# PART 8 OF 12 — End-to-End Integration and Data Contracts



System integration

Multi-agent workflow



## 8.1 Objective

So far, we have designed the individual parts:

- OpenCode: data extraction, validation, and local execution.
- Claude: ML implementation.
- Antigravity: main application and backend integration.
- NISAR: the underlying scientific observations.

Now we need to make these components work together without conflicting assumptions.

The most important rule: every component must consume verified outputs from the previous stage, not invent its own interpretation of the data.

Think of this like an assembly line: each workstation receives a standardized component, checks it, performs its assigned task, and passes a documented result to the next workstation.

## 8.2 Final system architecture

ORIGINAL NISAR DATA

Three L2 GCOV acquisitions · HH/HV · HDF5

OPENCODE — DATA ENGINEERING

Inspect · Validate · Extract · Prepare · Verify

Prepared rasters

Feature metadata

Validation reports

Statistics

CLAUDE

Develop ML engine

Model source code, tests, configuration

ANTIGRAVITY

Build main application

Frontend, backend, visualization, integration

OpenCode executes and validates ML; Antigravity consumes verified outputs

INTEGRATED APPLICATION

Interactive NISAR map · Temporal analysis · ML insights · Reports

This is the target workflow. Claude and Antigravity can work in parallel after agreeing on the data contract.

## 8.3 Define one source of truth

Create a central project manifest:

`data/project_manifest.json`

This file describes the dataset and the outputs actually available.

Example:

```
{
  "project": {
    "name": "Dancing with SARs",
    "study_area": "Potengi Estuary, Natal, Brazil",
    "product": "NISAR L2 GCOV"
  },
  "observations": [
    {
      "cycle": 28,
      "date": "2026-08-22",
      "polarizations": ["HH", "HV"]
    },
    {
      "cycle": 32,
      "date": "2026-10-09",
      "polarizations": ["HH", "HV"]
    },
    {
      "cycle": 33,
      "date": "2026-10-21",
      "polarizations": ["HH", "HV"]
    }
  ],
  "spatial_reference": {
    "crs": "EPSG:32725",
    "pixel_spacing_m": 10
  },
  "processing_status": {
    "extraction": "verified",
    "temporal_differences": "pending",
    "ml": "pending"
  }
}
```

This is a schema example. The final file must be generated from verified metadata.

### Why this matters

Without a shared manifest, different agents may accidentally use:

- Different AOI dimensions.
- Different acquisition dates.
- Different feature orders.
- Different CRS assumptions.
- Different NoData conventions.
- Different layer filenames.

A shared manifest prevents these inconsistencies.

## 8.4 Establish the canonical directory structure

Use one repository as the integration point.

```
dancing-with-sars/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── config/
│   ├── project.json
│   ├── aoi.json
│   └── processing.yaml
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   │
│   ├── extracted/
│   │   └── .gitkeep
│   │
│   ├── processed/
│   │   └── .gitkeep
│   │
│   ├── ml/
│   │   └── .gitkeep
│   │
│   ├── previews/
│   │   └── .gitkeep
│   │
│   ├── reports/
│   │   └── .gitkeep
│   │
│   └── project_manifest.json
│
├── ml_engine/
│   ├── src/
│   ├── tests/
│   ├── config/
│   └── README.md
│
├── backend/
│   ├── app/
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── scripts/
│   ├── validate_project.py
│   ├── generate_manifest.py
│   └── prepare_demo.py
│
└── docs/
    ├── architecture.md
    ├── methodology.md
    ├── data_dictionary.md
    └── validation_summary.md
```

### Important storage decision

Do not commit the original multi-gigabyte HDF5 granules to GitHub.

Use Git for:

- Source code.
- Configuration.
- Documentation.
- Small metadata files.
- Small preview images.
- Test fixtures.

Keep large source and generated raster files outside Git, and provide instructions for obtaining or preparing them.

For a fully offline demonstration, the required prepared AOI outputs must be supplied separately with the project.

## 8.5 Agent responsibility matrix

This matrix defines ownership and prevents duplicated work.

| Task                        | OpenCode           | Claude                 | Antigravity           |
| --------------------------- | ------------------ | ---------------------- | --------------------- |
| HDF5 inspection             | Owner              | —                      | —                     |
| AOI verification            | Owner              | —                      | —                     |
| Raster extraction           | Owner              | —                      | —                     |
| Data validation             | Owner              | Review logic           | —                     |
| Feature engineering         | Execute/verify     | Implement ML-side code | —                     |
| ML algorithm implementation | Execute/test       | Owner                  | Integrate             |
| ML model execution          | Owner              | Support                | —                     |
| Backend                     | Verify integration | —                      | Owner                 |
| Frontend                    | —                  | —                      | Owner                 |
| Map visualization           | Verify outputs     | —                      | Owner                 |
| API integration             | Test               | —                      | Owner                 |
| End-to-end testing          | Owner for data     | Owner for ML           | Owner for application |

The user coordinates the three agents and approves the final scientific interpretation.

### Ownership rule

Only one agent should be responsible for modifying a particular module at a time.

For example, Claude owns the ML source code. Antigravity should consume its public interface rather than independently rewriting the model.

## 8.6 The canonical data contract

This is the most important integration artifact.

Create:

`docs/data_dictionary.md`

It must document the following.

| Field            | Required definition            |
| ---------------- | ------------------------------ |
| `feature_names`  | Exact feature order            |
| `feature_units`  | dB, dimensionless, or other    |
| `shape`          | Raster rows and columns        |
| `crs`            | Coordinate reference system    |
| `transform`      | Affine geotransform            |
| `resolution`     | Pixel spacing                  |
| `nodata`         | NoData representation          |
| `mask_rule`      | Exact validity rule            |
| `acquisitions`   | Dates and cycles               |
| `aoi`            | Verified extent and dimensions |
| `dtype`          | Raster data type               |
| `source_product` | NISAR product identification   |

### Feature ordering

The 12-feature ML vector should have a fixed order.

Proposed order:

```
FEATURE_NAMES = [    "hh_028_db",    "hh_032_db",    "hh_033_db",    "hv_028_db",    "hv_032_db",    "hv_033_db",    "hh_diff_028_032",    "hh_diff_032_033",    "hh_diff_028_033",    "hv_diff_028_032",    "hv_diff_032_033",    "hv_diff_028_033"]
```

This is a proposed contract, not proof that all 12 arrays already exist.

The actual feature metadata must confirm that the names, units, shapes, and order match the generated arrays.

Never let Claude assume feature order based on alphabetical sorting or directory listing.

Analogy: a 12-pin connector works only if every pin is connected to the correct socket. The number of pins alone does not guarantee compatibility.

## 8.7 Standard ML input contract

Claude's ML engine should receive a documented input package, not a collection of files it must guess how to interpret.

Recommended input:

```
data/ml/
├── feature_stack.tif
├── common_valid_mask.tif
├── feature_metadata.json
└── input_validation.json
```

### `feature_metadata.json`

Example:

```
{
  "schema_version": "1.0",
  "feature_stack": "feature_stack.tif",
  "feature_count": 12,
  "feature_names": [
    "hh_028_db",
    "hh_032_db",
    "hh_033_db",
    "hv_028_db",
    "hv_032_db",
    "hv_033_db",
    "hh_diff_028_032",
    "hh_diff_032_033",
    "hh_diff_028_033",
    "hv_diff_028_032",
    "hv_diff_032_033",
    "hv_diff_028_033"
  ],
  "feature_units": "dB",
  "mask": "common_valid_mask.tif",
  "mask_valid_value": 1,
  "crs": "EPSG:32725",
  "width": 500,
  "height": 500,
  "nodata": null
}
```

The dimensions and feature count are illustrative. Populate them from the actual generated dataset.

### Why use a feature stack?

A multiband GeoTIFF gives the ML engine a consistent spatial structure:

- Band 1 = HH Cycle 028.
- Band 2 = HH Cycle 032.
- Band 3 = HH Cycle 033.
- Bands 4–6 = HV observations.
- Bands 7–12 = temporal differences.

The feature metadata defines the meaning of each band.

The common-valid mask defines which pixels are eligible for complete-vector analysis.

This avoids a situation where Claude reads the bands in the wrong order and produces technically valid but scientifically meaningless results.

## 8.8 Standard ML output contract

Claude should implement the model, but OpenCode should execute it and verify the resulting artifacts.

Recommended structure:

```
data/ml/
└── outputs/
    ├── cluster_map.tif
    ├── cluster_statistics.json
    ├── cluster_centroids.json
    ├── model_metadata.json
    ├── model_validation.json
    ├── statistical_change_hh.tif
    ├── statistical_change_hv.tif
    ├── model/
    │   ├── kmeans.joblib
    │   └── scaler.joblib
    └── previews/
        ├── cluster_map.png
        ├── hh_change.png
        └── hv_change.png
```

### Required output definitions

`cluster_map.tif`

- Integer raster.
- Cluster ID for valid pixels.
- NoData for invalid pixels.
- Same spatial reference as the input.

`cluster_statistics.json`

- Cluster ID.
- Pixel count.
- Area.
- Percentage of valid pixels.

`cluster_centroids.json`

- Cluster ID.
- Feature names.
- Centroid values.
- Units.

`model_metadata.json`

- Algorithm.
- Model configuration.
- Training sample size.
- Feature order.
- Scaler information.
- Random seed.
- Software versions.

`model_validation.json`

- Input validation status.
- Output validation status.
- Cluster population.
- Empty-cluster checks.
- Reproducibility checks.
- Known limitations.

The model should not silently label clusters as mangrove loss or gain.

## 8.9 Backend-to-frontend response contract

The backend is the single interface between the application and the scientific outputs.

For example, the frontend should receive a response like:

```
{
  "layer_id": "hh_diff_028_033",
  "name": "HH Backscatter Difference",
  "comparison": {
    "from_cycle": 28,
    "to_cycle": 33,
    "from_date": "2026-08-22",
    "to_date": "2026-10-21"
  },
  "polarization": "HH",
  "unit": "dB",
  "crs": "EPSG:32725",
  "available": true,
  "statistics": {
    "mean": null,
    "median": null,
    "valid_pixels": null
  },
  "preview_url": "/api/layers/hh_diff_028_033/preview"
}
```

Null values here are placeholders, not actual results.

### Contract requirements

Every response should make it clear:

- Which layer is being returned.
- What dates it represents.
- Which polarization it represents.
- What unit it uses.
- Whether it is available.
- What its spatial reference is.
- Where its visualization can be retrieved.

The frontend should not have to infer these facts from filenames.

## 8.10 End-to-end execution sequence

The following is the recommended integration order.

1. Stage 1 — Freeze verified inputs

   OpenCode confirms the three granules, AOI, dimensions, CRS, masks, and feature availability.

   Gate 1
2. Stage 2 — Prepare scientific outputs

   OpenCode generates the prepared backscatter layers, differences, validity masks, metadata, and statistics.

   Gate 2
3. Stage 3 — Parallel development

   Claude implements the ML engine against the frozen feature contract. Antigravity develops the application against the backend/API contract.

   Parallel work
4. Stage 4 — ML execution

   OpenCode runs the ML engine and validates its artifacts.

   Gate 3
5. Stage 5 — Backend integration

   Antigravity connects the API to the actual raster, statistics, report, and ML output locations.

   Gate 4
6. Stage 6 — Frontend integration

   The map, timeline, charts, and ML panels retrieve actual backend responses.
7. Stage 7 — Full application verification

   OpenCode executes the test plan and checks that the application behaves correctly with real data.

   Final gate

### Gate rule

Do not proceed to a stage that depends on an unverified artifact.

For example, Claude can develop against a documented sample schema, but the final model must not be considered integrated until the real feature stack passes validation.

## 8.11 Handling integration failures

The application must degrade gracefully.

| Failure                 | Required behavior                       |
| ----------------------- | --------------------------------------- |
| ML model unavailable    | Map and statistical analysis still work |
| One raster missing      | Hide or mark that layer unavailable     |
| Backend offline         | Show connection error                   |
| Invalid raster metadata | Reject layer and log the problem        |
| Missing report          | Show report unavailable                 |
| Model validation fails  | Do not display its predictions as valid |
| Basemap unavailable     | Keep local NISAR raster view accessible |
| Preview unavailable     | Provide a meaningful layer error        |

### Critical fallback

Your primary demonstration must not depend on the ML model.

The scientific foundation is the three-date NISAR comparison.

If the ML model fails, the project should still demonstrate:

- Actual NISAR observations.
- HH/HV comparison.
- Temporal differences.
- Common-valid coverage.
- Statistical change visualization.
- Spatial statistics.

This gives the project a reliable baseline.

## 8.12 Versioning and provenance

Every major output should be traceable to the inputs and processing configuration that produced it.

Create:

`data/reports/processing_provenance.json`

Example:

```
{
  "pipeline_version": "1.0.0",
  "source_product": "NISAR L2 GCOV",
  "acquisition_cycles": [28, 32, 33],
  "feature_schema_version": "1.0",
  "processing_config": "config/processing.yaml",
  "software": {
    "python": "record_actual_version",
    "numpy": "record_actual_version",
    "rasterio": "record_actual_version"
  },
  "outputs": [
    {
      "name": "hh_diff_028_033",
      "path": "data/processed/hh_diff_028_033.tif",
      "unit": "dB"
    }
  ]
}
```

For stronger provenance, calculate SHA-256 hashes for important inputs and outputs.

This lets the team distinguish between two files with the same filename but different contents.

A file's name is like a person's name: two people can share it. A content hash is closer to a fingerprint.

## 8.13 GitHub integration strategy

The GitHub repository should contain the application and its reproducible workflow, not necessarily the full scientific dataset.

### Commit to GitHub

- Frontend source.
- Backend source.
- ML engine source.
- Configuration files.
- Documentation.
- Unit tests.
- Small previews.
- Example metadata.
- Installation scripts.
- Data download/preparation instructions.

### Keep outside Git

- Original HDF5 granules.
- Large intermediate rasters.
- Large trained model artifacts.
- Temporary extraction files.
- Local environment files.
- Sensitive credentials.

Use `.gitignore`:

```
.env
.venv/
venv/
__pycache__/
*.pyc

data/raw/*
data/extracted/*
data/processed/*
data/ml/outputs/

!data/raw/.gitkeep
!data/extracted/.gitkeep
!data/processed/.gitkeep
!data/ml/outputs/.gitkeep

node_modules/
dist/
build/

*.log
.DS_Store
```

If you want a self-contained offline demonstration, distribute a separate demo-data archive containing the necessary AOI outputs and small model artifacts. Document its size, contents, and checksum.

Do not assume GitHub will accept large data archives or that a judge will have access to your local machine.

## 8.14 Ready-to-paste integration instructions

These instructions should be sent to each agent separately.

### A. OpenCode — integration and verification

# OPENCODE — SYSTEM INTEGRATION AND VERIFICATION

You are responsible for data engineering, local execution, and independent verification of the Dancing with SARs project.

The main application is developed by Antigravity. The ML engine is developed by Claude. Do not take ownership of their source modules unless explicitly requested.

## Your responsibilities

1. Inspect the complete repository before executing tasks.
2. Verify the three NISAR L2 GCOV source granules.
3. Verify the Potengi AOI and spatial alignment.
4. Prepare and validate the actual raster outputs.
5. Generate the canonical project manifest and feature metadata.
6. Validate the 12-feature ML input contract.
7. Execute Claude's ML engine against the actual prepared data.
8. Validate all generated ML outputs.
9. Verify Antigravity's backend responses against actual files.
10. Execute end-to-end tests.
11. Generate final validation and execution reports.

## Integration rules

- Do not invent data.
- Do not change the AOI without documenting the change.
- Do not overwrite original HDF5 files.
- Do not silently modify feature order.
- Do not accept missing or invalid values as valid measurements.
- Do not accept ML artifacts without checking dimensions, CRS, NoData, and feature metadata.
- Do not report application functionality as verified unless it has been tested.

## Final deliverables

Generate:

- project_manifest.json
- feature_metadata.json
- input_validation.json
- processing_provenance.json
- integration_validation_report.md
- end_to_end_test_report.md

Use actual execution results and record failures honestly.

Prioritize the functioning scientific demonstration over optional functionality.

### B. Claude — ML contract compliance

# CLAUDE — ML ENGINE INTEGRATION CONTRACT

Develop the independent NISAR ML engine for Dancing with SARs.

The input contract is defined in:

- data/ml/feature_metadata.json
- docs/data_dictionary.md

The feature stack is expected to contain 12 ordered features:

- Three HH observations
- Three HV observations
- Three HH temporal differences
- Three HV temporal differences

Never assume the order without reading the metadata.

## Required behavior

1. Validate input metadata before processing.
2. Validate the common-valid mask.
3. Reject incompatible raster dimensions, transforms, or CRS.
4. Process valid pixels only.
5. Implement MiniBatch K-Means with a configurable number of clusters.
6. Preserve a fitted scaler and model artifact.
7. Generate cluster maps with explicit NoData.
8. Generate cluster statistics and centroid metadata.
9. Generate model validation reports.
10. Preserve spatial metadata when exporting rasters.

Do not assign ecological meanings to cluster IDs.

Do not claim classification accuracy without independent reference labels.

The statistical change-detection engine must remain separate from the unsupervised clustering engine.

## Integration requirement

Provide:

- Stable Python API
- CLI execution
- Configuration file
- requirements.txt
- Tests
- README
- Output metadata schema

The ML engine must run locally without cloud inference dependencies.

OpenCode will execute and validate the implementation against the actual dataset.

### C. Antigravity — integration ownership

# ANTIGRAVITY — APPLICATION INTEGRATION CONTRACT

You own the main Dancing with SARs application.

Your application includes:

- Frontend
- Backend
- Map visualization
- Temporal analysis interface
- Statistics
- ML result visualization
- Reports

## Integration responsibilities

1. Inspect the existing repository and actual data directory.
2. Implement the FastAPI backend.
3. Implement the frontend.
4. Read the canonical project manifest.
5. Read registered raster layers.
6. Retrieve actual statistics from backend services.
7. Integrate Claude's ML outputs without rewriting the ML engine.
8. Display ML results only after their availability and metadata are verified.
9. Preserve scientific units, CRS, acquisition dates, and validity rules.
10. Make the core demonstration usable offline.

## Required integration behavior

- Do not fabricate charts or measurements.
- Do not create substitute satellite data.
- Do not invent ML cluster labels.
- Do not assume that missing files are available.
- Do not silently fall back to unrelated online satellite imagery.
- Keep the application functional if ML artifacts are unavailable.

## Important priority

The application must demonstrate actual three-date NISAR observations and temporal change analysis before advanced features are implemented.

## Delivery

Provide:

- Working frontend
- Working backend
- Documented API
- Local startup instructions
- Integration tests
- Screenshots of the actual application using real project data

Do not deliver only a visual mockup.

## 8.15 End-to-end acceptance test

This is the final integration test. It should be run after the agents have completed their respective tasks.

| No. | Test                        | Expected result                             |
| --- | --------------------------- | ------------------------------------------- |
| 1   | Start backend               | Server starts successfully                  |
| 2   | Open frontend               | Application loads                           |
| 3   | Check health API            | Backend reports healthy                     |
| 4   | Check project metadata      | Correct Potengi project information         |
| 5   | Open acquisition list       | Three actual acquisitions appear            |
| 6   | Select HH Cycle 028         | Correct raster loads                        |
| 7   | Select HV Cycle 033         | Correct raster loads                        |
| 8   | Open 028–033 difference     | Correct difference layer appears            |
| 9   | Check difference statistics | Match independently calculated values       |
| 10  | Open common-valid mask      | Invalid areas are represented correctly     |
| 11  | Open ML insights            | Validated ML results appear, if available   |
| 12  | Open reports                | Real processing and validation reports load |
| 13  | Disconnect internet         | Core local application remains usable       |
| 14  | Remove a test layer         | Application shows unavailable state         |
| 15  | Restart application         | Results remain available without retraining |

For numerical tests, use a tolerance appropriate to the data type and calculation precision.

## 8.16 Three-day execution schedule

Because you have only three days remaining, this is the recommended execution schedule.

Day 1 — Scientific foundation

Highest priority

- Freeze AOI and feature contract.
- Verify actual NISAR data.
- Generate temporal differences.
- Generate common-valid masks.
- Start Claude's ML implementation.
- Start Antigravity's application scaffold.

Day 2 — Integration

- Run and validate ML.
- Complete backend APIs.
- Connect real raster layers.
- Implement temporal comparison.
- Integrate ML results.
- Generate reports.

Day 3 — Demonstration and submission

- Run end-to-end tests.
- Fix critical issues.
- Test offline execution.
- Prepare demo data.
- Finalize GitHub repository.
- Prepare presentation and demonstration sequence.

These are work priorities, not guaranteed completion times. If a stage takes longer than expected, drop optional features rather than weakening data validation.

## 8.17 Final integration decisions

These are the decisions I recommend freezing now:

| Decision                       | Final choice                                     |
| ------------------------------ | ------------------------------------------------ |
| Main application builder       | Antigravity                                      |
| ML implementation              | Claude                                           |
| Data engineering and execution | OpenCode                                         |
| Backend                        | FastAPI                                          |
| ML algorithm                   | MiniBatch K-Means + statistical change detection |
| Scientific input               | Three verified NISAR acquisitions                |
| ML input                       | Fixed 12-feature contract                        |
| Raster format                  | GeoTIFF                                          |
| Metadata format                | JSON                                             |
| Primary application map        | MapLibre                                         |
| Data storage                   | Local project directories                        |
| Database                       | Not required for MVP                             |
| Hosting                        | Not required                                     |
| Primary demo                   | Local/offline                                    |

One critical decision: Freeze the data contract before Claude and Antigravity independently finalize their implementations. Changing the feature order, AOI, or raster conventions after integration will create avoidable rework.

## Part 8 completion checklist

- System architecture established.
- Agent responsibilities separated.
- Canonical directory structure defined.
- Project manifest specified.
- ML input contract specified.
- ML output contract specified.
- Backend/frontend response contract specified.
- Integration sequence defined.
- Failure-handling behavior defined.
- Provenance and versioning defined.
- GitHub storage strategy defined.
- Three-day execution schedule established.
- Agent-specific integration prompts prepared.


