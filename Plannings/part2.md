# PART 2 OF 12 — NISAR Data Architecture and Processing Pipeline



Technical specification

For OpenCode + Antigravity + Claude



First, one important update to our architecture:

Antigravity using Gemini 3.8 Flash will be the primary application development environment. It will build the frontend, backend, application logic, visualizations, and integration. We will give it a detailed implementation specification so it does not have to independently design the scientific processing pipeline.

The division of responsibilities is now:

| Tool                           | Responsibility                                            |
| ------------------------------ | --------------------------------------------------------- |
| ChatGPT                        | Architecture, technical planning, specifications          |
| Antigravity + Gemini 3.8 Flash | Main application development and integration              |
| Claude.ai                      | ML model code development                                 |
| OpenCode                       | NISAR extraction, local execution, validation and testing |

This part defines the data pipeline that connects all three development environments.

## 2.1 Available satellite data

Our primary data source is the NASA-ISRO Synthetic Aperture Radar (NISAR) mission.

[NISAR in Orbit (Artist's Concept) - NASA Science](https://images.openai.com/static-rsc-4/PGXqjDsKyjwmh7-nilHu87OcaYfOPNEl-qtmBO4Z3nV-XKlGWUgkGf4NEEZKPZ-1_yoUeHBTP93OUJL0rUdKPh-8SfNXbP8G4qhERnHt_sV2gcK9RipJ_on9AfxlufYSaMwl1miS83fL0DvIjDdHk6mStiiYBgBbONqpBlbUDn4?purpose=inline)

[Now That NISAR Launched, Here's What You Can Expect From the Data | NASA Earthdata](https://images.openai.com/static-rsc-4/GvAiwMjmvRVXrHsfUiXKPS_KXd9tdcWf6LSJdlchxdR8kB0XhAI8s1hfAymc8QLnD-5vhiQR_WnGwIN7Tsk2xqZKaB1d_C9DBp-F0t7ccB-fKQeFO5Xg4EW8EWdfrzospbQUhZuUvs4pIHiqV1ehlLTgxLYoo808nF0K6QkFv3U?purpose=inline)

[NISAR Satellite](https://images.openai.com/static-rsc-4/Q5Kc627i9dpBr6I8FDaVzQGPExZfC5QtTYBrfh2T730poJNSUpzB2DFTD48Ed7TftYQv1lqgzRPYAWQc_XlzVwtTa-SQTLuuV38V2IKGRjBHkuN0q_9w3sM87VUL5E4gJ8mkTFXZZI4GCE2dBcIcPQB_1_kzbguLdX_1cyoe8cs?purpose=inline)

4

We are using the L2 GCOV — Geocoded Polarimetric Covariance product.

Unlike an ordinary optical satellite image, SAR uses radar signals to observe the Earth's surface. It can collect observations regardless of sunlight and has useful capabilities in cloudy conditions.

Our selected observations:

| Cycle | Acquisition date | Role               |
| ----- | ---------------- | ------------------ |
| 028   | August 22, 2026  | First observation  |
| 032   | October 9, 2026  | Second observation |
| 033   | October 21, 2026 | Third observation  |

These observations give us two comparison periods:

- August 22 → October 9: 48 days.
- October 9 → October 21: 12 days.
- August 22 → October 21: 60 days.

The application should make these intervals visible because the amount of time between observations affects how changes should be interpreted.

## 2.2 NISAR product structure

The existing files are HDF5 files (`.h5`).

Think of an HDF5 file as a large organized warehouse. It contains multiple datasets, metadata, coordinate arrays, and scientific measurements rather than one ordinary image.

The processing pipeline must read only the necessary datasets.

Our relevant Frequency A datasets are:

| Dataset         | Purpose                                          |
| --------------- | ------------------------------------------------ |
| `HHHH`          | HH polarization backscatter                      |
| `HVHV`          | HV polarization backscatter                      |
| `mask`          | Radar validity and subswath information          |
| `numberOfLooks` | Number of independent looks used in the estimate |
| `xCoordinates`  | Projected horizontal coordinates                 |
| `yCoordinates`  | Projected vertical coordinates                   |

The exact HDF5 group paths must be read from the actual files. The names above are dataset names, not assumptions about their complete paths.

Important: We should use Frequency A consistently across all three dates unless a documented technical reason requires otherwise.

## 2.3 Coordinate system and spatial alignment

Our reported spatial configuration is:

| Property             | Value                        |
| -------------------- | ---------------------------- |
| CRS                  | EPSG:32725                   |
| Coordinate reference | WGS 84 / UTM Zone 25S        |
| Pixel spacing        | 10 metres                    |
| Frequency            | A                            |
| Raster dimensions    | 32,472 rows × 33,336 columns |
| Data type            | Float32 for backscatter      |
| Mask type            | UInt8                        |

The three acquisitions reportedly have identical coordinate arrays and raster dimensions.

This is extremely useful: if confirmed against the actual HDF5 files, we can compare corresponding pixels directly without resampling or reprojection.

For example, pixel `(1500, 14000)` in Cycle 028 should represent the same ground location as pixel `(1500, 14000)` in Cycle 032 and Cycle 033.

Processing rule: OpenCode must verify coordinate-array equality before assuming direct pixel-to-pixel comparison is valid.

It should check:

1. Raster dimensions.
2. CRS.
3. Pixel spacing.
4. Coordinate-array values.
5. Coordinate-array orientation.
6. Coordinate-array hashes.
7. Acquisition metadata.

If any of these differ, the pipeline must stop direct comparison and report the mismatch.

## 2.4 AOI configuration

The application should not hardcode AOI coordinates inside multiple scripts.

Instead, use one central configuration file.

Proposed location:

`config/aoi.json`

Example structure:

```
{
  "aoi_id": "potengi_estuary_primary",
  "name": "Potengi Estuary",
  "country": "Brazil",
  "crs": "EPSG:32725",
  "resolution_m": 10,
  "geometry": {
    "type": "Polygon",
    "coordinates": []
  },
  "raster_window": {
    "row_start": null,
    "row_end": null,
    "col_start": null,
    "col_end": null
  },
  "status": "provisional"
}
```

The actual coordinates and raster window must be inserted only after AOI verification.

Why centralize this?

Imagine changing the address of a building. You would not want to manually change that address in ten different documents. One central configuration prevents inconsistent AOIs across the application.

Requirement: Every processing script, ML inference script, and map component must use this configuration or its validated output.

## 2.5 Data processing pipeline

This is the exact sequence we should implement.

INPUT: THREE NISAR HDF5 FILES

Cycle 028 · Cycle 032 · Cycle 033

STAGE 1 — METADATA INSPECTION

Read product metadata, dimensions, CRS, coordinates and dataset paths.

STAGE 2 — SPATIAL VALIDATION

Confirm identical grids and locate the selected AOI.

STAGE 3 — WINDOWED EXTRACTION

Read only the AOI pixels from each HDF5 dataset.

STAGE 4 — QUALITY CONTROL

Apply mask, finite-value and positive-backscatter checks.

STAGE 5 — SCIENTIFIC PREPARATION

Convert linear power to dB, calculate common validity and prepare temporal features.

STAGE 6 — OUTPUT GENERATION

GeoTIFF / analysis arrays / previews / metadata / validation reports.

READY FOR APPLICATION AND ML

Antigravity application · Claude ML implementation

## 2.6 Data-quality filtering

This is one of the most important parts of the entire project.

NISAR data contains pixels that should not be used for analysis. We must distinguish usable radar observations from invalid or missing samples.

Our reported mask convention is:

| Mask value | Meaning                           | Treatment |
| ---------- | --------------------------------- | --------- |
| 0          | Invalid radar sample              | Exclude   |
| 1–254      | Valid subswath identifier         | Retain    |
| 255        | Fill / outside acquisition extent | Exclude   |

For each acquisition, a pixel is considered valid only when all of these conditions are met:

1. Mask value is between 1 and 254.
2. HH is finite.
3. HV is finite.
4. HH is greater than zero.
5. HV is greater than zero.

In logical notation:

\\[ V_t = (1 \leq M_t \leq 254) \land \operatorname{finite}(HH_t) \land \operatorname{finite}(HV_t) \land (HH_t > 0) \land (HV_t > 0) \\]

Here, \\(t\\) represents an acquisition date.

### Three-date common-valid mask

For a fair three-date comparison, we need pixels that are valid in all three acquisitions.

\\[ V\_{\text{common}} = V\_{028} \land V\_{032} \land V\_{033} \\]

This prevents a missing observation from being mistakenly interpreted as environmental change.

Example: If a pixel is valid in August but missing in October, it must not be displayed as a measured decrease in backscatter.

The application should offer:

- Per-date validity.
- Three-date common-valid coverage.
- Invalid-pixel visualization.
- Coverage statistics.

It should never silently turn invalid pixels into zero-valued radar measurements.

## 2.7 Backscatter conversion

The NISAR GCOV HH and HV values are reported as calibrated gamma-zero backscatter power in linear units, according to our existing product inspection.

For visualization, we should convert positive linear power into decibels:

\\[ \gamma^0\_{\mathrm{dB}} = 10\log\_{10}(\gamma^0\_{\mathrm{linear}}) \\]

This conversion must be applied only to finite, positive values.

Example:

| Linear power | Approximate dB |
| ------------ | -------------- |
| 1.0          | 0 dB           |
| 0.1          | -10 dB         |
| 0.01         | -20 dB         |
| 0.001        | -30 dB         |

The application should display HH and HV in dB because this makes radar backscatter easier to inspect visually.

Important implementation rule: Preserve the original linear values. Do not replace the source data with dB values.

We need both representations:

- Linear power: numerical processing and model input where appropriate.
- dB: human-readable visualization and some change-analysis features.

## 2.8 Temporal comparison features

After extracting and validating the three observations, the pipeline should prepare temporal features.

For each pixel:

\\[ \Delta HH\_{1,2} = HH\_{032,\mathrm{dB}} - HH\_{028,\mathrm{dB}} \\]

\\[ \Delta HH\_{2,3} = HH\_{033,\mathrm{dB}} - HH\_{032,\mathrm{dB}} \\]

\\[ \Delta HH\_{1,3} = HH\_{033,\mathrm{dB}} - HH\_{028,\mathrm{dB}} \\]

The same calculations apply to HV.

This gives us six primary temporal difference layers:

| Feature         | Comparison             |
| --------------- | ---------------------- |
| HH difference 1 | August → October 9     |
| HH difference 2 | October 9 → October 21 |
| HH difference 3 | August → October 21    |
| HV difference 1 | August → October 9     |
| HV difference 2 | October 9 → October 21 |
| HV difference 3 | August → October 21    |

The differences should only be calculated where both observations are valid.

### Interpreting the results

- Positive difference: backscatter increased.
- Negative difference: backscatter decreased.
- Near-zero difference: backscatter remained relatively similar.

However, a backscatter increase or decrease is not automatically mangrove growth or destruction.

Radar backscatter can change due to vegetation structure, soil moisture, surface water, acquisition conditions, and other factors.

Our application must describe these as observed radar changes unless independent evidence supports a stronger ecological interpretation.

## 2.9 Additional features for the ML model

We should prepare more than just six difference layers.

The following features are useful candidates:

| Feature                     | Description                            | Priority  |
| --------------------------- | -------------------------------------- | --------- |
| HH dB                       | HH backscatter at each date            | Essential |
| HV dB                       | HV backscatter at each date            | Essential |
| HH temporal differences     | HH changes between dates               | Essential |
| HV temporal differences     | HV changes between dates               | Essential |
| HH/HV ratio                 | Polarimetric relationship              | High      |
| Temporal mean               | Average backscatter across valid dates | High      |
| Temporal standard deviation | Variability across dates               | High      |
| Validity mask               | Identifies usable pixels               | Essential |
| Number of looks             | Radar observation quality context      | Optional  |

For the ratio, if we calculate it in dB:

\\[ R\_{\mathrm{dB}} = HH\_{\mathrm{dB}} - HV\_{\mathrm{dB}} \\]

This is equivalent to the logarithm of the linear HH/HV ratio.

The model should receive a documented feature schema. Claude must not invent additional features or assume that all inputs are interchangeable.

## 2.10 Output data architecture

I recommend a standardized directory structure.

```
project/
│
├── config/
│   ├── aoi.json
│   ├── acquisitions.json
│   └── processing.json
│
├── data/
│   ├── raw/
│   │   ├── cycle_028.h5
│   │   ├── cycle_032.h5
│   │   └── cycle_033.h5
│   │
│   ├── processed/
│   │   ├── cycle_028/
│   │   │   ├── HH_linear.tif
│   │   │   ├── HV_linear.tif
│   │   │   ├── HH_db.tif
│   │   │   ├── HV_db.tif
│   │   │   └── validity_mask.tif
│   │   │
│   │   ├── cycle_032/
│   │   └── cycle_033/
│   │
│   ├── temporal/
│   │   ├── HH_diff_028_032.tif
│   │   ├── HH_diff_032_033.tif
│   │   ├── HH_diff_028_033.tif
│   │   ├── HV_diff_028_032.tif
│   │   ├── HV_diff_032_033.tif
│   │   ├── HV_diff_028_033.tif
│   │   └── common_valid_mask.tif
│   │
│   ├── ml/
│   │   ├── feature_stack.tif
│   │   ├── feature_metadata.json
│   │   └── predictions/
│   │
│   ├── reference/
│   │   └── ...
│   │
│   ├── previews/
│   │   └── ...
│   │
│   └── reports/
│       └── ...
│
└── src/
    ├── data/
    ├── analysis/
    ├── ml/
    └── ...
```

This is the proposed logical organization. OpenCode and Antigravity may adjust filenames to fit the existing repository, but the data contracts must remain consistent.

## 2.11 File formats and metadata requirements

We should use different formats for different purposes.

| Format               | Use                                            |
| -------------------- | ---------------------------------------------- |
| HDF5 (`.h5`)         | Original NISAR source data                     |
| GeoTIFF (`.tif`)     | Georeferenced raster layers                    |
| JSON (`.json`)       | Configuration, metadata and processing results |
| CSV (`.csv`)         | Statistical summaries and tabular results      |
| PNG (`.png`)         | Lightweight previews                           |
| GeoJSON (`.geojson`) | AOI boundary and vector reference features     |
| Markdown (`.md`)     | Technical reports and documentation            |

### GeoTIFF requirements

Every processed raster should preserve:

- CRS: EPSG:32725.
- Spatial transform derived from the actual coordinate arrays.
- Correct pixel dimensions.
- Correct data type.
- NoData definition.
- Descriptive band name.
- Acquisition date.
- Processing metadata.

Use tiled and compressed GeoTIFFs where practical.

A Cloud Optimized GeoTIFF (COG) can also be generated if it helps with efficient map rendering. It is not mandatory for the local prototype.

Important: Do not assume that the raster's upper-left coordinate or pixel orientation can be reconstructed from approximate bounds. Use the actual HDF5 coordinate arrays to establish the transform.

## 2.12 Processing performance and hardware constraints

The original NISAR rasters contain over one billion pixels per acquisition.

We must not load the complete HH, HV, mask, and coordinate arrays into RAM just to process a small AOI.

Your available hardware:

- Intel i5-14500.
- Radeon RX 580 8 GB.
- 16 GB system RAM.
- 1 TB SSD.
- Linux Mint 22.3.

The data-processing pipeline should primarily use CPU-based, windowed HDF5 reads. There is no requirement to use the GPU for this processing stage.

### Required performance rules

1. Read only the selected AOI window.
2. Process one acquisition at a time where practical.
3. Avoid retaining unnecessary intermediate arrays.
4. Release memory after processing each stage.
5. Use NumPy vectorized operations rather than Python pixel-by-pixel loops.
6. Use compressed outputs.
7. Generate lower-resolution previews separately.
8. Support restarting interrupted processing without reprocessing completed stages.

For the proposed 25 km² AOI:

\\[ 500 \times 500 = 250,000 \text{ pixels} \\]

A single float32 array requires approximately 1 MB of memory.

This makes the selected AOI manageable on your hardware. The entire project should not require loading the original 1-billion-pixel rasters.

## 2.13 What OpenCode must produce

OpenCode's primary job is to turn the original HDF5 files into a verified, reusable data package.

Its deliverables should be:

| Deliverable            | Purpose                        |
| ---------------------- | ------------------------------ |
| AOI configuration      | Single source of spatial truth |
| Extracted HH/HV layers | Three acquisitions             |
| dB layers              | Visualization                  |
| Validity masks         | Quality control                |
| Temporal differences   | Change analysis                |
| Common-valid mask      | Fair three-date comparison     |
| ML feature stack       | Model input                    |
| Feature metadata       | Model input documentation      |
| Processing report      | Reproducibility                |
| Preview images         | Development and review         |

It should also record the exact source file, HDF5 dataset path, acquisition cycle, extraction window, processing parameters, and software versions.

## 2.14 The data contract between the three tools

This is where the architecture becomes important.

### OpenCode → Claude

Claude receives:

- The exact feature names.
- Feature order.
- Input data format.
- Array dimensions.
- Data types.
- NoData representation.
- Validity-mask definition.
- Normalization requirements.
- Expected model output.

Claude should write its code against this contract rather than making assumptions about the original HDF5 structure.

### Claude → OpenCode

Claude returns:

- Python source code.
- Model architecture or algorithm.
- Dependency requirements.
- Training or inference instructions.
- Model weights, if applicable.
- Input/output specifications.
- Evaluation metrics.

OpenCode executes the implementation locally and verifies its outputs.

### OpenCode → Antigravity

OpenCode supplies:

- Processed raster files.
- Geospatial metadata.
- Change layers.
- ML predictions.
- Model confidence or probability layers, where applicable.
- Data-quality statistics.
- Processing reports.

### Antigravity → User

Antigravity integrates these outputs into the final application.

The application should read processed outputs rather than attempting to reopen and process the original billion-pixel HDF5 datasets whenever a user changes a map layer.

## 2.15 Implementation instructions for OpenCode

The following is the actual execution specification for your local agent. It is not an instruction to start blindly: first inspect the repository and reconcile the existing work.

# OPEN CODE SPECIFICATION — NISAR DATA ENGINE

## Project role

You are the local NISAR data-processing, extraction, and validation engineer.

Your responsibility is to prepare reproducible, georeferenced, scientifically consistent datasets for the NASA Space Apps 2026 application.

The main application will be developed separately using Antigravity with Gemini 3.8 Flash. The ML source code will be developed using Claude.ai and executed locally by you.

## Input acquisitions

- Cycle 028: 2026-08-22
- Cycle 032: 2026-10-09
- Cycle 033: 2026-10-21

Product: NISAR L2 GCOV, Frequency A.

Relevant datasets:

- HHHH
- HVHV
- mask
- numberOfLooks
- xCoordinates
- yCoordinates

Discover the exact HDF5 paths from the actual files.

## Processing stages

### Stage 1: Inspect

- Identify all three HDF5 files.
- Verify granule identities.
- Verify acquisition dates.
- Verify Frequency A dataset paths.
- Inspect metadata, dimensions, CRS and coordinate arrays.
- Confirm spatial grid alignment.

### Stage 2: AOI

- Read the central AOI configuration.
- Verify geographic and projected coordinates.
- Verify raster row/column mapping.
- Check AOI boundaries against the actual coordinate arrays.
- Do not use an unverified or obsolete Rio Preguiças configuration.
- Do not claim reference-site containment without coordinate-based evidence.

### Stage 3: Extract

Use windowed HDF5 reads.

Extract only:

- HHHH
- HVHV
- mask
- numberOfLooks, if needed

Do not load entire source rasters into memory.

### Stage 4: Validate

Apply the reported mask convention:

- 0 = invalid radar sample
- 1–254 = valid subswath
- 255 = fill/outside acquisition extent

Require finite, positive HH and HV values for a valid observation.

Calculate per-date validity and three-date common validity.

### Stage 5: Prepare

- Preserve linear backscatter values.
- Convert valid positive power to dB using 10\*log10(power).
- Calculate HH/HV temporal differences.
- Calculate HH/HV ratios or equivalent dB differences where appropriate.
- Calculate temporal summary statistics.
- Maintain consistent NoData handling.

### Stage 6: Export

Produce georeferenced rasters, metadata, previews and reports.

Required outputs include:

- Three-date HH/HV linear rasters.
- Three-date HH/HV dB rasters.
- Per-date validity masks.
- Three-date common-valid mask.
- Six temporal difference layers.
- ML feature stack.
- Feature metadata JSON.
- Processing report.

### Stage 7: ML integration

When Claude's model code becomes available:

- Inspect its dependencies.
- Verify compatibility with the feature schema.
- Run inference locally.
- Preserve the original feature stack.
- Save prediction rasters and metadata.
- Record execution logs and evaluation results.

## Resource constraints

- 16 GB RAM.
- RX 580 8 GB.
- Linux Mint 22.3.
- Python 3.12.
- Existing HDF5 processing environment.

Use efficient windowed processing and avoid unnecessary GPU or large-model requirements.

## Required behavior

- Inspect existing scripts and reports before creating replacements.
- Reuse verified work.
- Never overwrite original HDF5 files.
- Never fabricate validation results.
- Keep processing scripts reproducible.
- Save logs and meaningful error messages.
- Make interrupted stages restartable.
- Report actual completion and remaining blockers.

Do not begin unrelated application development. Antigravity owns the main application.

## 2.16 Instructions for Antigravity

Antigravity needs to know the expected data interface before developing the application.

# ANTIGRAVITY SPECIFICATION — NISAR DATA INTEGRATION

You are developing the primary NASA Space Apps 2026 application using Gemini 3.8 Flash.

The data engine is developed and operated separately through OpenCode.

Build the application around preprocessed, georeferenced NISAR outputs.

### Required data support

Support:

- Three acquisition dates.
- HH backscatter.
- HV backscatter.
- Linear and dB representations.
- Per-date validity masks.
- Common-valid mask.
- Temporal difference rasters.
- ML prediction outputs.
- Spatial metadata and AOI geometry.

### Application requirements

1. Read raster metadata dynamically.
2. Identify the acquisition date from metadata or the manifest.
3. Display HH and HV layers.
4. Allow switching between acquisition dates.
5. Support date-to-date comparison.
6. Display temporal differences.
7. Respect NoData and validity masks.
8. Overlay AOI and reference layers.
9. Display data-quality statistics.
10. Integrate ML prediction outputs when available.

### Important restrictions

- Do not hardcode unverified AOI coordinates.
- Do not assume all raster layers have identical dimensions without checking metadata.
- Do not treat NoData as zero.
- Do not calculate scientific backscatter differences in the frontend.
- Do not invent ML results.
- Do not require original HDF5 files to be loaded by the browser.
- Use processed raster outputs as the application's data source.

### Deliverable

A modular application that can consume the standardized data package produced by OpenCode without changing the scientific processing pipeline.

## 2.17 Part 2 completion criteria

- Three acquisition files identified.
- HDF5 dataset structure defined.
- Spatial alignment requirements established.
- Central AOI configuration designed.
- Data-quality rules defined.
- Backscatter conversion defined.
- Temporal features specified.
- Output formats and directory structure defined.
- Hardware constraints incorporated.
- OpenCode responsibilities specified.
- Antigravity data contract specified.

The main outcome of Part 2: All three tools now have a common understanding of how NISAR data enters the system, how it is processed, and what the application and ML model will receive.

### Next: Part 3 — Machine Learning Model Architecture

This is where we make the most important scientific and technical decisions:

- What exactly should the ML model detect?
- Should it use CNN, U-Net, Random Forest, XGBoost, or unsupervised change detection?
- Does it need training data?
- Can we train it with only three NISAR acquisitions?
- What should Claude actually build?
- How will we evaluate whether its predictions are trustworthy?

I recommend making Part 3 the next priority, because the ML objective determines the features, labels, training strategy, and model outputs that the rest of the application must support.
