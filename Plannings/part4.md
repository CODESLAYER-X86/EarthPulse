# PART 4 OF 12 — ML Implementation, Model Lifecycle and Execution Architecture



Implementation specification

Claude → OpenCode → Antigravity



In Part 3, we selected a hybrid ML approach:

- Statistical change detection for measurable HH/HV changes.
- MiniBatch K-Means for grouping similar temporal radar patterns.
- Optional Isolation Forest for unusual radar responses.

Now we need to turn that design into a complete software implementation that Claude can write, OpenCode can execute, and Antigravity can integrate.

The main decision for Part 4: The ML engine must be an independent Python module. It should not depend on the frontend, and it should not require Antigravity to execute scientific calculations in the browser.

Think of it like a car engine: it should operate independently and expose a predictable interface to the rest of the vehicle.

## 4.1 ML engine architecture

The ML engine will have six major layers.

1\. INPUT LAYER

GeoTIFF feature stack · Validity mask · AOI metadata

2\. DATA VALIDATION

CRS · Dimensions · NoData · Feature names · Finite values

3\. FEATURE ENGINE

Feature selection · Sampling · Scaling · Feature preparation

Statistical engine

Threshold calculation

Directional change

ML engine

MiniBatch K-Means

Optional anomaly detection

5\. OUTPUT GENERATION

Prediction rasters · Statistics · Model artifacts

6\. INTEGRATION INTERFACE

Standardized files and metadata for Antigravity

Each layer should have a separate Python module so a failure in one component does not require rewriting the entire engine.

## 4.2 Recommended Python project structure

Claude should produce a structure similar to this:

```
ml_engine/
│
├── README.md
├── requirements.txt
├── pyproject.toml
│
├── config/
│   ├── model_config.yaml
│   └── feature_schema.json
│
├── src/
│   └── nisar_ml/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       │
│       ├── data/
│       │   ├── loader.py
│       │   ├── validator.py
│       │   └── metadata.py
│       │
│       ├── features/
│       │   ├── builder.py
│       │   ├── scaler.py
│       │   └── sampler.py
│       │
│       ├── models/
│       │   ├── clustering.py
│       │   └── anomaly.py
│       │
│       ├── analysis/
│       │   ├── change_detection.py
│       │   ├── cluster_interpretation.py
│       │   └── statistics.py
│       │
│       ├── outputs/
│       │   ├── raster_writer.py
│       │   ├── json_writer.py
│       │   └── report_writer.py
│       │
│       └── validation/
│           ├── model_validation.py
│           └── stability.py
│
├── tests/
│   ├── test_inputs.py
│   ├── test_features.py
│   ├── test_change_detection.py
│   ├── test_clustering.py
│   └── test_outputs.py
│
├── artifacts/
│   └── .gitkeep
│
└── outputs/
    └── .gitkeep
```

This is a logical separation, not unnecessary complexity. Each module has one clear responsibility.

## 4.3 Input contract — exactly what Claude's code receives

The most important input should be a machine-readable manifest.

Recommended location:

`data/ml/feature_metadata.json`

Example:

```
{
  "project": "Dancing with SARs",
  "aoi_id": "potengi_estuary_primary",
  "crs": "EPSG:32725",
  "resolution_m": 10,
  "shape": {
    "rows": 500,
    "columns": 500
  },
  "acquisitions": [
    {
      "cycle": 28,
      "date": "2026-08-22"
    },
    {
      "cycle": 32,
      "date": "2026-10-09"
    },
    {
      "cycle": 33,
      "date": "2026-10-21"
    }
  ],
  "feature_stack": "feature_stack.tif",
  "common_valid_mask": "common_valid_mask.tif",
  "features": [
    "HH_028_db",
    "HH_032_db",
    "HH_033_db",
    "HV_028_db",
    "HV_032_db",
    "HV_033_db",
    "HH_diff_028_032",
    "HH_diff_032_033",
    "HH_diff_028_033",
    "HV_diff_028_032",
    "HV_diff_032_033",
    "HV_diff_028_033"
  ],
  "data_type": "float32",
  "nodata": null
}
```

This is an illustrative schema. OpenCode must populate the actual dimensions, file paths, geotransform, and metadata from the generated rasters.

### Why the manifest matters

Suppose Claude's code expects 12 bands but OpenCode produces 10.

Without a manifest, the model might silently interpret the wrong band as the wrong feature.

With a manifest, the ML engine can compare:

- Expected feature names.
- Actual raster band count.
- Feature ordering.
- Spatial dimensions.
- Coordinate reference system.

If anything disagrees, it should stop and report the problem.

## 4.4 Feature engineering implementation

We should separate the feature-generation process from the clustering model.

### A. Primary features

Six backscatter features:

```
HH_028_db
HH_032_db
HH_033_db

HV_028_db
HV_032_db
HV_033_db
```

Six temporal differences:

```
HH_diff_028_032
HH_diff_032_033
HH_diff_028_033

HV_diff_028_032
HV_diff_032_033
HV_diff_028_033
```

### B. Additional derived features

Potential additional features:

```
HH_HV_ratio_028
HH_HV_ratio_032
HH_HV_ratio_033

HH_temporal_std
HV_temporal_std
```

I recommend that Claude initially implement the 12 primary features and make the additional features configurable.

Why? Adding many highly correlated features can distort clustering. More features do not automatically mean a better model.

### C. Feature scaling

Use `RobustScaler` as the initial choice.

It scales using the median and interquartile range, making it less sensitive to extreme values than standard mean/variance scaling.

However, the implementation should:

1. Fit the scaler only on valid training samples.
2. Save the fitted scaler.
3. Reuse it for full-AOI inference.
4. Record its parameters.
5. Never refit it independently for each date or inference batch.

### D. Memory-efficient processing

Do not create a huge 12-band array if the AOI grows substantially.

The implementation should support chunked processing:

1. Read a block of raster pixels.
2. Apply the common-valid mask.
3. Build the feature matrix for that block.
4. Apply the saved scaler.
5. Run predictions.
6. Write the output block.
7. Continue to the next block.

This is similar to processing a large spreadsheet in sections instead of opening every record simultaneously.

## 4.5 Model configuration

Claude should not hardcode algorithm settings throughout the source code.

Use one configuration file:

`ml_engine/config/model_config.yaml`

Example:

```
project:
  name: "Dancing with SARs"
  version: "1.0.0"

input:
  manifest: "data/ml/feature_metadata.json"
  require_common_valid_mask: true

clustering:
  algorithm: "MiniBatchKMeans"
  n_clusters: 4
  batch_size: 4096
  max_iter: 200
  n_init: 5
  random_state: 42
  sample_size: 100000

scaling:
  method: "RobustScaler"

change_detection:
  method: "median_absolute_deviation"
  multiplier: 3.0
  minimum_threshold_db: null

anomaly_detection:
  enabled: false
  algorithm: "IsolationForest"
  contamination: "auto"

processing:
  chunk_size: 50000
  output_dtype: "uint8"
  preserve_nodata: true

validation:
  test_reproducibility: true
  test_cluster_population: true
  test_centroid_separation: true
```

These are starting parameters, not scientifically established optimal values.

In particular:

- Four clusters must be tested against alternatives such as three and five.
- The MAD multiplier must be evaluated against actual observed distributions.
- The minimum threshold should be selected only after inspecting the data.
- The sample size should adapt to the number of valid pixels.

The configuration must make these settings adjustable without modifying the source code.

## 4.6 Model lifecycle

The ML system needs two separate execution modes.

Mode A

Model fitting

1. Read feature manifest.
2. Validate feature stack and mask.
3. Select valid representative samples.
4. Fit RobustScaler.
5. Fit MiniBatch K-Means.
6. Evaluate cluster quality.
7. Save model and scaler artifacts.

Mode B

Inference

1. Load fitted model and scaler.
2. Validate feature schema compatibility.
3. Read the full AOI in chunks.
4. Apply the saved scaler.
5. Generate cluster predictions.
6. Write georeferenced prediction rasters.
7. Generate statistics and reports.

Important: If we later introduce another acquisition date, we cannot simply feed an extra band into the existing 12-feature model. The feature schema changes, so the model must be retrained or a specifically designed temporal model must be used.

## 4.7 Statistical change detection implementation

This should be a separate module, not hidden inside the K-Means implementation.

Recommended functions:

| Function                           | Responsibility                              |
| ---------------------------------- | ------------------------------------------- |
| `calculate_temporal_differences()` | Calculate HH/HV dB differences              |
| `estimate_robust_threshold()`      | Calculate robust thresholds                 |
| `classify_directional_change()`    | Produce increase/stable/decrease categories |
| `calculate_change_statistics()`    | Calculate pixel counts and area             |
| `write_change_raster()`            | Export georeferenced classifications        |

Suggested output encoding:

| Value | Meaning   |
| ----- | --------- |
| 0     | Stable    |
| 1     | Increased |
| 2     | Decreased |
| 255   | NoData    |

This encoding is for the change-category rasters only. It must not be confused with the original NISAR mask convention.

HH and HV should have separate category rasters.

The system should also provide a combined interpretation layer if justified by both channels.

For example, it could distinguish:

- Both channels increased.
- Both channels decreased.
- HH and HV changed in opposing directions.
- Only one channel changed significantly.
- No significant change.

Do not force these combined categories if the observations do not support them.

## 4.8 Model artifacts and version management

Every fitting run should produce a self-contained artifact directory.

Recommended:

```
ml_engine/
└── outputs/
    └── run_001/
        ├── model/
        │   ├── kmeans.joblib
        │   └── scaler.joblib
        │
        ├── predictions/
        │   ├── cluster_map.tif
        │   ├── hh_change_categories.tif
        │   ├── hv_change_categories.tif
        │   └── anomaly_score.tif
        │
        ├── statistics/
        │   ├── cluster_statistics.json
        │   ├── cluster_statistics.csv
        │   └── cluster_centroids.json
        │
        ├── metadata/
        │   ├── model_metadata.json
        │   └── feature_metadata.json
        │
        └── reports/
            └── execution_report.md
```

The anomaly raster should only exist when anomaly detection is enabled and successfully executed.

### Model metadata

The model metadata should contain:

- Model name and version.
- Algorithm and parameters.
- Random seed.
- Training sample count.
- Feature names and order.
- Scaling method.
- AOI identifier.
- Input dataset identifiers.
- Acquisition dates.
- Software and dependency versions.
- Execution timestamp.
- Validation results.

This lets us identify exactly which model generated a particular prediction map.

### Reproducibility

If we run the same configuration against the same inputs, the result should be reproducible to the extent supported by the algorithm and numerical environment.

The report should record any differences between repeated runs rather than simply claiming perfect reproducibility.

## 4.9 Command-line interface

OpenCode should be able to run the ML engine through simple commands.

I recommend these commands:

```
# Inspect and validate input data
python -m nisar_ml.cli validate

# Fit the clustering model
python -m nisar_ml.cli fit

# Run full-AOI inference
python -m nisar_ml.cli predict

# Run statistical change detection
python -m nisar_ml.cli change

# Generate model and analysis reports
python -m nisar_ml.cli report

# Run all core stages
python -m nisar_ml.cli run-all
```

Each command should:

1. Read the central configuration.
2. Validate its required inputs.
3. Create the appropriate output directory.
4. Save execution logs.
5. Return a meaningful exit code.
6. Report errors clearly.

The `run-all` command must not silently refit an existing model if a compatible saved model already exists. It should require an explicit refit option.

## 4.10 Error handling and recovery

We need to prevent one missing file or incompatible raster from corrupting the entire workflow.

| Problem                   | Expected behavior                                |
| ------------------------- | ------------------------------------------------ |
| Missing feature raster    | Stop and identify the missing file               |
| Incorrect number of bands | Stop and report expected versus actual           |
| CRS mismatch              | Stop before processing                           |
| Dimension mismatch        | Stop before processing                           |
| Invalid pixels            | Exclude using validity mask                      |
| NaN/Infinity              | Exclude or handle according to explicit rules    |
| Empty valid dataset       | Stop and report insufficient data                |
| Too few samples           | Reduce complexity or report insufficient samples |
| Missing model artifact    | Require fitting before inference                 |
| Output already exists     | Avoid accidental overwrite                       |
| Processing interruption   | Preserve completed outputs and permit restart    |

A failed model run must never produce an apparently successful report.

### Logging

Use Python's standard `logging` module.

Record:

- Execution start and end.
- Configuration used.
- Input files.
- Number of valid pixels.
- Sample count.
- Model parameters.
- Processing time.
- Output paths.
- Errors and warnings.

## 4.11 Testing strategy

Claude should create automated tests before declaring the engine complete.

Test categories

1\. Input tests

- Correct feature names.
- Correct band count.
- Correct CRS.
- Correct raster dimensions.
- Correct validity-mask values.

2\. Feature tests

- Difference calculations.
- HH/HV ratio calculations.
- Robust scaling.
- NoData exclusion.

3\. Model tests

- Model fitting completes.
- Predictions are within expected cluster IDs.
- Invalid pixels remain NoData.
- Saved model can be reloaded.

4\. Raster tests

- Output dimensions match input.
- CRS and transform are preserved.
- NoData is correct.
- Output values are valid.

5\. Reproducibility tests

- Fixed random seed.
- Repeatable sample selection.
- Stable model outputs under the same environment.

A tiny synthetic raster can be used for software tests. However, synthetic test results must never be presented as actual NISAR findings.

## 4.12 How Antigravity will consume the ML outputs

Antigravity should not directly import the Python model implementation into its frontend.

Instead, it should consume the output files through a backend data service.

The application needs access to:

- Cluster prediction raster.
- HH change raster.
- HV change raster.
- Cluster statistics.
- Model metadata.
- Execution report.
- AOI and acquisition metadata.

The backend should expose a consistent interface.

For example, these are proposed API endpoints:

| Endpoint                        | Function                               |
| ------------------------------- | -------------------------------------- |
| `GET /api/ml/status`            | Check whether ML results are available |
| `GET /api/ml/metadata`          | Retrieve model information             |
| `GET /api/ml/clusters`          | Retrieve cluster statistics            |
| `GET /api/ml/change`            | Retrieve change statistics             |
| `GET /api/ml/layers`            | List available prediction layers       |
| `GET /api/ml/layers/{layer_id}` | Access a prediction layer              |

These are architectural proposals, not existing endpoints. Antigravity will implement them.

The backend can serve raster tiles or suitable raster previews rather than transmitting entire GeoTIFF files to the browser.

## 4.13 Final Claude implementation assignment

This is the expanded instruction for Claude. It builds on Part 3 and specifies how the code must be structured, executed, tested, and delivered.

# CLAUDE DEVELOPMENT TASK — COMPLETE NISAR ML ENGINE

## Project

Dancing with SARs — NASA Space Apps 2026

## Your responsibility

Develop a complete, modular, executable Python machine-learning engine for multi-temporal NISAR L2 GCOV analysis.

The main application is developed using Antigravity with Gemini 3.8 Flash.

OpenCode executes and validates your Python implementation locally.

You are responsible for the ML implementation, not the main application.

## 1. Architecture

Implement six independent layers:

1. Input loading and validation.
2. Feature engineering.
3. Feature scaling and representative sampling.
4. Statistical change detection.
5. Machine-learning clustering and optional anomaly detection.
6. Prediction export, statistics and validation reporting.

## 2. Technology

Target:

- Python 3.12.
- NumPy.
- SciPy.
- scikit-learn.
- Rasterio.
- Joblib.
- PyYAML.
- Pytest.

Use additional libraries only when necessary.

CPU execution is required. Do not require CUDA, ROCm or a dedicated GPU.

## 3. Input contract

Read a feature metadata JSON manifest.

The primary input contains:

- Six HH/HV backscatter features.
- Six HH/HV temporal differences.
- Common-valid mask.
- AOI metadata.
- Acquisition dates.
- CRS and raster transform.

Do not hardcode file paths, dimensions, or feature ordering.

Validate the manifest against actual raster files before processing.

## 4. Feature processing

Implement:

- Feature loading.
- Valid-pixel selection.
- Robust scaling.
- Deterministic representative sampling.
- Chunked inference.
- Optional feature selection.

Fit the scaler on the training sample and reuse it during inference.

Exclude all invalid pixels.

## 5. Statistical engine

Implement independent HH and HV change detection.

Calculate temporal differences and robust thresholds.

Produce:

- Stable category.
- Increased category.
- Decreased category.
- NoData.

Record actual thresholds and pixel counts.

Do not assume universal change thresholds.

## 6. ML engine

Implement MiniBatch K-Means.

Initial configuration:

- Four clusters.
- Batch size: 4096.
- Maximum iterations: 200.
- Five initializations.
- Fixed random seed: 42.
- Initial sample size: up to 100,000 valid pixels.

Make parameters configurable.

Test alternative cluster counts where practical.

Do not hardcode ecological meaning into cluster IDs.

Analyze centroids and derive descriptive labels only where supported.

Optional: implement Isolation Forest behind a configuration flag.

## 7. Model lifecycle

Provide separate fitting and inference operations.

Fitting:

- Validate inputs.
- Select samples.
- Fit scaler.
- Fit model.
- Evaluate clustering.
- Save artifacts.
- Generate metadata.

Inference:

- Load saved artifacts.
- Verify feature compatibility.
- Process data in chunks.
- Generate cluster predictions.
- Preserve NoData.
- Export prediction rasters.

Do not silently retrain an existing model.

## 8. Output requirements

Produce:

- cluster_map.tif
- hh_change_categories.tif
- hv_change_categories.tif
- cluster_statistics.json
- cluster_statistics.csv
- cluster_centroids.json
- model_metadata.json
- fitted_model.joblib
- fitted_scaler.joblib
- execution_report.md

Optional anomaly output:

- anomaly_score.tif

Preserve spatial metadata and NoData.

## 9. Configuration

Use YAML configuration for model parameters and JSON for the feature schema.

Avoid hardcoded scientific parameters throughout the code.

Record the effective configuration in every execution report.

## 10. CLI

Provide:

- validate
- fit
- predict
- change
- report
- run-all

Each command must validate prerequisites and return meaningful exit codes.

## 11. Performance

Target the user's environment:

- Intel i5-14500.
- 16 GB RAM.
- Radeon RX 580 8 GB.
- Linux Mint.
- Python 3.12.

Use chunked processing and avoid unnecessary full-raster copies.

## 12. Testing

Create automated tests for:

- Input validation.
- Feature calculations.
- Mask handling.
- Model fitting.
- Model persistence.
- Prediction.
- GeoTIFF export.
- Reproducibility.

Use small synthetic fixtures for software testing only.

Never represent synthetic outputs as real satellite findings.

## 13. Scientific integrity

Do not claim:

- Cluster labels are ground truth.
- Radar changes prove mangrove loss or gain.
- Unsupervised clustering accuracy without independent labels.
- Model confidence percentages without a defined calculation.

Clearly distinguish radar observations, model groupings, and ecological interpretations.

## 14. Delivery

Provide a complete project directory with:

- Source code.
- Configuration.
- Requirements.
- README.
- Tests.
- Model artifacts.
- Execution instructions.
- Output documentation.

Do not provide pseudocode or incomplete placeholder functions as the final implementation.

Before development, inspect the actual feature manifest and confirm compatibility.

If required input data is unavailable, report exactly what is missing.

## 4.14 Three important engineering decisions

I want to emphasize three things before we move on.

1\. Keep the ML engine independent. If we change the frontend, the model should still work. If we change the model, the frontend should not need a complete rewrite.

2\. Do not use ML as decoration. Every prediction layer must come from actual execution against the NISAR data. A beautiful colored map with invented predictions would weaken the project.

3\. Do not make the ML engine a bottleneck. The application must still provide its core NISAR visualizations and statistical change analysis if the ML model fails or is unavailable.

## 4.15 Part 4 completion checklist

- ML Python project structure defined.
- Input manifest contract defined.
- Feature engineering implementation specified.
- Model configuration defined.
- Training and inference separated.
- Statistical engine separated from ML.
- Model artifacts and versioning defined.
- CLI commands defined.
- Error handling and recovery specified.
- Automated tests specified.
- Antigravity integration interface defined.
- Claude implementation assignment prepared.

Next: Part 5 — Complete Backend Architecture.

We will design the application's backend: how Antigravity should organize the server, access GeoTIFF files, expose APIs, manage analysis results, communicate with the ML engine, and deliver raster data to the frontend without exhausting your computer's RAM.

Type next when ready.# PART 4 OF 12 — ML Implementation, Model Lifecycle and Execution Architecture



Implementation specification

Claude → OpenCode → Antigravity



In Part 3, we selected a hybrid ML approach:

- Statistical change detection for measurable HH/HV changes.
- MiniBatch K-Means for grouping similar temporal radar patterns.
- Optional Isolation Forest for unusual radar responses.

Now we need to turn that design into a complete software implementation that Claude can write, OpenCode can execute, and Antigravity can integrate.

The main decision for Part 4: The ML engine must be an independent Python module. It should not depend on the frontend, and it should not require Antigravity to execute scientific calculations in the browser.

Think of it like a car engine: it should operate independently and expose a predictable interface to the rest of the vehicle.

## 4.1 ML engine architecture

The ML engine will have six major layers.

1\. INPUT LAYER

GeoTIFF feature stack · Validity mask · AOI metadata

2\. DATA VALIDATION

CRS · Dimensions · NoData · Feature names · Finite values

3\. FEATURE ENGINE

Feature selection · Sampling · Scaling · Feature preparation

Statistical engine

Threshold calculation

Directional change

ML engine

MiniBatch K-Means

Optional anomaly detection

5\. OUTPUT GENERATION

Prediction rasters · Statistics · Model artifacts

6\. INTEGRATION INTERFACE

Standardized files and metadata for Antigravity

Each layer should have a separate Python module so a failure in one component does not require rewriting the entire engine.

## 4.2 Recommended Python project structure

Claude should produce a structure similar to this:

```
ml_engine/
│
├── README.md
├── requirements.txt
├── pyproject.toml
│
├── config/
│   ├── model_config.yaml
│   └── feature_schema.json
│
├── src/
│   └── nisar_ml/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       │
│       ├── data/
│       │   ├── loader.py
│       │   ├── validator.py
│       │   └── metadata.py
│       │
│       ├── features/
│       │   ├── builder.py
│       │   ├── scaler.py
│       │   └── sampler.py
│       │
│       ├── models/
│       │   ├── clustering.py
│       │   └── anomaly.py
│       │
│       ├── analysis/
│       │   ├── change_detection.py
│       │   ├── cluster_interpretation.py
│       │   └── statistics.py
│       │
│       ├── outputs/
│       │   ├── raster_writer.py
│       │   ├── json_writer.py
│       │   └── report_writer.py
│       │
│       └── validation/
│           ├── model_validation.py
│           └── stability.py
│
├── tests/
│   ├── test_inputs.py
│   ├── test_features.py
│   ├── test_change_detection.py
│   ├── test_clustering.py
│   └── test_outputs.py
│
├── artifacts/
│   └── .gitkeep
│
└── outputs/
    └── .gitkeep
```

This is a logical separation, not unnecessary complexity. Each module has one clear responsibility.

## 4.3 Input contract — exactly what Claude's code receives

The most important input should be a machine-readable manifest.

Recommended location:

`data/ml/feature_metadata.json`

Example:

```
{
  "project": "Dancing with SARs",
  "aoi_id": "potengi_estuary_primary",
  "crs": "EPSG:32725",
  "resolution_m": 10,
  "shape": {
    "rows": 500,
    "columns": 500
  },
  "acquisitions": [
    {
      "cycle": 28,
      "date": "2026-08-22"
    },
    {
      "cycle": 32,
      "date": "2026-10-09"
    },
    {
      "cycle": 33,
      "date": "2026-10-21"
    }
  ],
  "feature_stack": "feature_stack.tif",
  "common_valid_mask": "common_valid_mask.tif",
  "features": [
    "HH_028_db",
    "HH_032_db",
    "HH_033_db",
    "HV_028_db",
    "HV_032_db",
    "HV_033_db",
    "HH_diff_028_032",
    "HH_diff_032_033",
    "HH_diff_028_033",
    "HV_diff_028_032",
    "HV_diff_032_033",
    "HV_diff_028_033"
  ],
  "data_type": "float32",
  "nodata": null
}
```

This is an illustrative schema. OpenCode must populate the actual dimensions, file paths, geotransform, and metadata from the generated rasters.

### Why the manifest matters

Suppose Claude's code expects 12 bands but OpenCode produces 10.

Without a manifest, the model might silently interpret the wrong band as the wrong feature.

With a manifest, the ML engine can compare:

- Expected feature names.
- Actual raster band count.
- Feature ordering.
- Spatial dimensions.
- Coordinate reference system.

If anything disagrees, it should stop and report the problem.

## 4.4 Feature engineering implementation

We should separate the feature-generation process from the clustering model.

### A. Primary features

Six backscatter features:

```
HH_028_db
HH_032_db
HH_033_db

HV_028_db
HV_032_db
HV_033_db
```

Six temporal differences:

```
HH_diff_028_032
HH_diff_032_033
HH_diff_028_033

HV_diff_028_032
HV_diff_032_033
HV_diff_028_033
```

### B. Additional derived features

Potential additional features:

```
HH_HV_ratio_028
HH_HV_ratio_032
HH_HV_ratio_033

HH_temporal_std
HV_temporal_std
```

I recommend that Claude initially implement the 12 primary features and make the additional features configurable.

Why? Adding many highly correlated features can distort clustering. More features do not automatically mean a better model.

### C. Feature scaling

Use `RobustScaler` as the initial choice.

It scales using the median and interquartile range, making it less sensitive to extreme values than standard mean/variance scaling.

However, the implementation should:

1. Fit the scaler only on valid training samples.
2. Save the fitted scaler.
3. Reuse it for full-AOI inference.
4. Record its parameters.
5. Never refit it independently for each date or inference batch.

### D. Memory-efficient processing

Do not create a huge 12-band array if the AOI grows substantially.

The implementation should support chunked processing:

1. Read a block of raster pixels.
2. Apply the common-valid mask.
3. Build the feature matrix for that block.
4. Apply the saved scaler.
5. Run predictions.
6. Write the output block.
7. Continue to the next block.

This is similar to processing a large spreadsheet in sections instead of opening every record simultaneously.

## 4.5 Model configuration

Claude should not hardcode algorithm settings throughout the source code.

Use one configuration file:

`ml_engine/config/model_config.yaml`

Example:

```
project:
  name: "Dancing with SARs"
  version: "1.0.0"

input:
  manifest: "data/ml/feature_metadata.json"
  require_common_valid_mask: true

clustering:
  algorithm: "MiniBatchKMeans"
  n_clusters: 4
  batch_size: 4096
  max_iter: 200
  n_init: 5
  random_state: 42
  sample_size: 100000

scaling:
  method: "RobustScaler"

change_detection:
  method: "median_absolute_deviation"
  multiplier: 3.0
  minimum_threshold_db: null

anomaly_detection:
  enabled: false
  algorithm: "IsolationForest"
  contamination: "auto"

processing:
  chunk_size: 50000
  output_dtype: "uint8"
  preserve_nodata: true

validation:
  test_reproducibility: true
  test_cluster_population: true
  test_centroid_separation: true
```

These are starting parameters, not scientifically established optimal values.

In particular:

- Four clusters must be tested against alternatives such as three and five.
- The MAD multiplier must be evaluated against actual observed distributions.
- The minimum threshold should be selected only after inspecting the data.
- The sample size should adapt to the number of valid pixels.

The configuration must make these settings adjustable without modifying the source code.

## 4.6 Model lifecycle

The ML system needs two separate execution modes.

Mode A

Model fitting

1. Read feature manifest.
2. Validate feature stack and mask.
3. Select valid representative samples.
4. Fit RobustScaler.
5. Fit MiniBatch K-Means.
6. Evaluate cluster quality.
7. Save model and scaler artifacts.

Mode B

Inference

1. Load fitted model and scaler.
2. Validate feature schema compatibility.
3. Read the full AOI in chunks.
4. Apply the saved scaler.
5. Generate cluster predictions.
6. Write georeferenced prediction rasters.
7. Generate statistics and reports.

Important: If we later introduce another acquisition date, we cannot simply feed an extra band into the existing 12-feature model. The feature schema changes, so the model must be retrained or a specifically designed temporal model must be used.

## 4.7 Statistical change detection implementation

This should be a separate module, not hidden inside the K-Means implementation.

Recommended functions:

| Function                           | Responsibility                              |
| ---------------------------------- | ------------------------------------------- |
| `calculate_temporal_differences()` | Calculate HH/HV dB differences              |
| `estimate_robust_threshold()`      | Calculate robust thresholds                 |
| `classify_directional_change()`    | Produce increase/stable/decrease categories |
| `calculate_change_statistics()`    | Calculate pixel counts and area             |
| `write_change_raster()`            | Export georeferenced classifications        |

Suggested output encoding:

| Value | Meaning   |
| ----- | --------- |
| 0     | Stable    |
| 1     | Increased |
| 2     | Decreased |
| 255   | NoData    |

This encoding is for the change-category rasters only. It must not be confused with the original NISAR mask convention.

HH and HV should have separate category rasters.

The system should also provide a combined interpretation layer if justified by both channels.

For example, it could distinguish:

- Both channels increased.
- Both channels decreased.
- HH and HV changed in opposing directions.
- Only one channel changed significantly.
- No significant change.

Do not force these combined categories if the observations do not support them.

## 4.8 Model artifacts and version management

Every fitting run should produce a self-contained artifact directory.

Recommended:

```
ml_engine/
└── outputs/
    └── run_001/
        ├── model/
        │   ├── kmeans.joblib
        │   └── scaler.joblib
        │
        ├── predictions/
        │   ├── cluster_map.tif
        │   ├── hh_change_categories.tif
        │   ├── hv_change_categories.tif
        │   └── anomaly_score.tif
        │
        ├── statistics/
        │   ├── cluster_statistics.json
        │   ├── cluster_statistics.csv
        │   └── cluster_centroids.json
        │
        ├── metadata/
        │   ├── model_metadata.json
        │   └── feature_metadata.json
        │
        └── reports/
            └── execution_report.md
```

The anomaly raster should only exist when anomaly detection is enabled and successfully executed.

### Model metadata

The model metadata should contain:

- Model name and version.
- Algorithm and parameters.
- Random seed.
- Training sample count.
- Feature names and order.
- Scaling method.
- AOI identifier.
- Input dataset identifiers.
- Acquisition dates.
- Software and dependency versions.
- Execution timestamp.
- Validation results.

This lets us identify exactly which model generated a particular prediction map.

### Reproducibility

If we run the same configuration against the same inputs, the result should be reproducible to the extent supported by the algorithm and numerical environment.

The report should record any differences between repeated runs rather than simply claiming perfect reproducibility.

## 4.9 Command-line interface

OpenCode should be able to run the ML engine through simple commands.

I recommend these commands:

```
# Inspect and validate input data
python -m nisar_ml.cli validate

# Fit the clustering model
python -m nisar_ml.cli fit

# Run full-AOI inference
python -m nisar_ml.cli predict

# Run statistical change detection
python -m nisar_ml.cli change

# Generate model and analysis reports
python -m nisar_ml.cli report

# Run all core stages
python -m nisar_ml.cli run-all
```

Each command should:

1. Read the central configuration.
2. Validate its required inputs.
3. Create the appropriate output directory.
4. Save execution logs.
5. Return a meaningful exit code.
6. Report errors clearly.

The `run-all` command must not silently refit an existing model if a compatible saved model already exists. It should require an explicit refit option.

## 4.10 Error handling and recovery

We need to prevent one missing file or incompatible raster from corrupting the entire workflow.

| Problem                   | Expected behavior                                |
| ------------------------- | ------------------------------------------------ |
| Missing feature raster    | Stop and identify the missing file               |
| Incorrect number of bands | Stop and report expected versus actual           |
| CRS mismatch              | Stop before processing                           |
| Dimension mismatch        | Stop before processing                           |
| Invalid pixels            | Exclude using validity mask                      |
| NaN/Infinity              | Exclude or handle according to explicit rules    |
| Empty valid dataset       | Stop and report insufficient data                |
| Too few samples           | Reduce complexity or report insufficient samples |
| Missing model artifact    | Require fitting before inference                 |
| Output already exists     | Avoid accidental overwrite                       |
| Processing interruption   | Preserve completed outputs and permit restart    |

A failed model run must never produce an apparently successful report.

### Logging

Use Python's standard `logging` module.

Record:

- Execution start and end.
- Configuration used.
- Input files.
- Number of valid pixels.
- Sample count.
- Model parameters.
- Processing time.
- Output paths.
- Errors and warnings.

## 4.11 Testing strategy

Claude should create automated tests before declaring the engine complete.

Test categories

1\. Input tests

- Correct feature names.
- Correct band count.
- Correct CRS.
- Correct raster dimensions.
- Correct validity-mask values.

2\. Feature tests

- Difference calculations.
- HH/HV ratio calculations.
- Robust scaling.
- NoData exclusion.

3\. Model tests

- Model fitting completes.
- Predictions are within expected cluster IDs.
- Invalid pixels remain NoData.
- Saved model can be reloaded.

4\. Raster tests

- Output dimensions match input.
- CRS and transform are preserved.
- NoData is correct.
- Output values are valid.

5\. Reproducibility tests

- Fixed random seed.
- Repeatable sample selection.
- Stable model outputs under the same environment.

A tiny synthetic raster can be used for software tests. However, synthetic test results must never be presented as actual NISAR findings.

## 4.12 How Antigravity will consume the ML outputs

Antigravity should not directly import the Python model implementation into its frontend.

Instead, it should consume the output files through a backend data service.

The application needs access to:

- Cluster prediction raster.
- HH change raster.
- HV change raster.
- Cluster statistics.
- Model metadata.
- Execution report.
- AOI and acquisition metadata.

The backend should expose a consistent interface.

For example, these are proposed API endpoints:

| Endpoint                        | Function                               |
| ------------------------------- | -------------------------------------- |
| `GET /api/ml/status`            | Check whether ML results are available |
| `GET /api/ml/metadata`          | Retrieve model information             |
| `GET /api/ml/clusters`          | Retrieve cluster statistics            |
| `GET /api/ml/change`            | Retrieve change statistics             |
| `GET /api/ml/layers`            | List available prediction layers       |
| `GET /api/ml/layers/{layer_id}` | Access a prediction layer              |

These are architectural proposals, not existing endpoints. Antigravity will implement them.

The backend can serve raster tiles or suitable raster previews rather than transmitting entire GeoTIFF files to the browser.

## 4.13 Final Claude implementation assignment

This is the expanded instruction for Claude. It builds on Part 3 and specifies how the code must be structured, executed, tested, and delivered.

# CLAUDE DEVELOPMENT TASK — COMPLETE NISAR ML ENGINE

## Project

Dancing with SARs — NASA Space Apps 2026

## Your responsibility

Develop a complete, modular, executable Python machine-learning engine for multi-temporal NISAR L2 GCOV analysis.

The main application is developed using Antigravity with Gemini 3.8 Flash.

OpenCode executes and validates your Python implementation locally.

You are responsible for the ML implementation, not the main application.

## 1. Architecture

Implement six independent layers:

1. Input loading and validation.
2. Feature engineering.
3. Feature scaling and representative sampling.
4. Statistical change detection.
5. Machine-learning clustering and optional anomaly detection.
6. Prediction export, statistics and validation reporting.

## 2. Technology

Target:

- Python 3.12.
- NumPy.
- SciPy.
- scikit-learn.
- Rasterio.
- Joblib.
- PyYAML.
- Pytest.

Use additional libraries only when necessary.

CPU execution is required. Do not require CUDA, ROCm or a dedicated GPU.

## 3. Input contract

Read a feature metadata JSON manifest.

The primary input contains:

- Six HH/HV backscatter features.
- Six HH/HV temporal differences.
- Common-valid mask.
- AOI metadata.
- Acquisition dates.
- CRS and raster transform.

Do not hardcode file paths, dimensions, or feature ordering.

Validate the manifest against actual raster files before processing.

## 4. Feature processing

Implement:

- Feature loading.
- Valid-pixel selection.
- Robust scaling.
- Deterministic representative sampling.
- Chunked inference.
- Optional feature selection.

Fit the scaler on the training sample and reuse it during inference.

Exclude all invalid pixels.

## 5. Statistical engine

Implement independent HH and HV change detection.

Calculate temporal differences and robust thresholds.

Produce:

- Stable category.
- Increased category.
- Decreased category.
- NoData.

Record actual thresholds and pixel counts.

Do not assume universal change thresholds.

## 6. ML engine

Implement MiniBatch K-Means.

Initial configuration:

- Four clusters.
- Batch size: 4096.
- Maximum iterations: 200.
- Five initializations.
- Fixed random seed: 42.
- Initial sample size: up to 100,000 valid pixels.

Make parameters configurable.

Test alternative cluster counts where practical.

Do not hardcode ecological meaning into cluster IDs.

Analyze centroids and derive descriptive labels only where supported.

Optional: implement Isolation Forest behind a configuration flag.

## 7. Model lifecycle

Provide separate fitting and inference operations.

Fitting:

- Validate inputs.
- Select samples.
- Fit scaler.
- Fit model.
- Evaluate clustering.
- Save artifacts.
- Generate metadata.

Inference:

- Load saved artifacts.
- Verify feature compatibility.
- Process data in chunks.
- Generate cluster predictions.
- Preserve NoData.
- Export prediction rasters.

Do not silently retrain an existing model.

## 8. Output requirements

Produce:

- cluster_map.tif
- hh_change_categories.tif
- hv_change_categories.tif
- cluster_statistics.json
- cluster_statistics.csv
- cluster_centroids.json
- model_metadata.json
- fitted_model.joblib
- fitted_scaler.joblib
- execution_report.md

Optional anomaly output:

- anomaly_score.tif

Preserve spatial metadata and NoData.

## 9. Configuration

Use YAML configuration for model parameters and JSON for the feature schema.

Avoid hardcoded scientific parameters throughout the code.

Record the effective configuration in every execution report.

## 10. CLI

Provide:

- validate
- fit
- predict
- change
- report
- run-all

Each command must validate prerequisites and return meaningful exit codes.

## 11. Performance

Target the user's environment:

- Intel i5-14500.
- 16 GB RAM.
- Radeon RX 580 8 GB.
- Linux Mint.
- Python 3.12.

Use chunked processing and avoid unnecessary full-raster copies.

## 12. Testing

Create automated tests for:

- Input validation.
- Feature calculations.
- Mask handling.
- Model fitting.
- Model persistence.
- Prediction.
- GeoTIFF export.
- Reproducibility.

Use small synthetic fixtures for software testing only.

Never represent synthetic outputs as real satellite findings.

## 13. Scientific integrity

Do not claim:

- Cluster labels are ground truth.
- Radar changes prove mangrove loss or gain.
- Unsupervised clustering accuracy without independent labels.
- Model confidence percentages without a defined calculation.

Clearly distinguish radar observations, model groupings, and ecological interpretations.

## 14. Delivery

Provide a complete project directory with:

- Source code.
- Configuration.
- Requirements.
- README.
- Tests.
- Model artifacts.
- Execution instructions.
- Output documentation.

Do not provide pseudocode or incomplete placeholder functions as the final implementation.

Before development, inspect the actual feature manifest and confirm compatibility.

If required input data is unavailable, report exactly what is missing.

## 4.14 Three important engineering decisions

I want to emphasize three things before we move on.

1\. Keep the ML engine independent. If we change the frontend, the model should still work. If we change the model, the frontend should not need a complete rewrite.

2\. Do not use ML as decoration. Every prediction layer must come from actual execution against the NISAR data. A beautiful colored map with invented predictions would weaken the project.

3\. Do not make the ML engine a bottleneck. The application must still provide its core NISAR visualizations and statistical change analysis if the ML model fails or is unavailable.

## 4.15 Part 4 completion checklist

- ML Python project structure defined.
- Input manifest contract defined.
- Feature engineering implementation specified.
- Model configuration defined.
- Training and inference separated.
- Statistical engine separated from ML.
- Model artifacts and versioning defined.
- CLI commands defined.
- Error handling and recovery specified.
- Automated tests specified.
- Antigravity integration interface defined.
- Claude implementation assignment prepared.

Next: Part 5 — Complete Backend Architecture.

We will design the application's backend: how Antigravity should organize the server, access GeoTIFF files, expose APIs, manage analysis results, communicate with the ML engine, and deliver raster data to the frontend without exhausting your computer's RAM.

Type next when ready.
