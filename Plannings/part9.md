# PART 9 OF 12 — Testing, Validation, and Scientific Reliability



Verification strategy

Submission readiness



## 9.1 Objective

A working application is not necessarily a scientifically reliable application.

For this project, we need to establish four things:

1. Data correctness: Are the NISAR observations and spatial boundaries correct?
2. Computational correctness: Are the backscatter conversions, differences, masks, and statistics correct?
3. ML reliability: Does the model produce reproducible, interpretable outputs?
4. Application correctness: Does the interface display the actual outputs without misleading users?

Think of this as testing a calculator. It is not enough for the calculator to turn on and display numbers. We must verify that its calculations are correct.

## 9.2 Four-level validation framework

Level 1 — Source data validation

Mandatory

Verify HDF5 metadata, granule identity, acquisition dates, masks, CRS, and AOI alignment.

Level 2 — Scientific processing validation

Mandatory

Verify dB conversion, temporal differences, valid pixels, statistics, and raster exports.

Level 3 — ML validation

Required if ML is presented

Verify input compatibility, reproducibility, cluster population, spatial alignment, and model limitations.

Level 4 — Application validation

Mandatory

Verify API responses, raster visualization, user interactions, offline operation, and error handling.

## 9.3 Source data validation

OpenCode must independently inspect the actual three HDF5 granules.

Do not rely exclusively on previously generated Markdown reports.

### A. Granule identity

Verify:

- Granule ID.
- Product type.
- Processing version.
- Acquisition timestamp.
- Cycle number.
- Frequency.
- Polarization availability.

The acquisition date displayed in the application must correspond to the actual metadata.

### B. Spatial consistency

Verify all three observations have compatible:

- Raster dimensions.
- CRS.
- Geotransform.
- Pixel spacing.
- Spatial extent.

The reported EPSG:32725 and 10 m pixel spacing must be confirmed from the actual files.

### C. AOI consistency

The Potengi reference sites must be transformed and checked against the actual raster coordinates.

Previously reported reference locations:

| Reference | Latitude  | Longitude  |
| --------- | --------- | ---------- |
| Site 1    | -5.763056 | -35.236111 |
| Site 2    | -5.758611 | -35.199722 |

Previously proposed 25 km² window:

- Rows: 1480–1979.
- Columns: 13611–14110.
- Dimensions: 500 × 500 pixels.
- Nominal pixel area: 100 m².

These are candidate coordinates and window dimensions, not independently confirmed final AOI metadata.

OpenCode must verify them against the actual geotransform and coordinate arrays.

Important: A correct CRS does not automatically guarantee that the AOI window is correct. Both the transformation and pixel indexing must be verified.

### D. AOI coverage

Generate a report containing:

- Total AOI pixels.
- Valid pixels for each acquisition.
- HH common-valid pixels.
- HV common-valid pixels.
- Complete 12-feature valid pixels.
- Common-valid percentage.
- Actual AOI geographic extent.

This is especially important because the previously reported 58.26% common-valid coverage refers to the full granule, not necessarily the selected AOI.

## 9.4 Numerical validation of scientific calculations

Use small, independently constructed test arrays before trusting the full processing pipeline.

### Test 1 — Linear-to-dB conversion

Use:

```
import numpy as npvalues = np.array([0.01, 0.1, 1.0, 10.0])db = 10 * np.log10(values)print(db)
```

Expected approximate result:

```
[-20.0, -10.0, 0.0, 10.0]
```

Test zero, negative, NaN, and infinity separately. They must be excluded or marked invalid.

### Test 2 — Temporal differences

Construct a simple example:

```
date_028 = np.array([-12.0, -10.0, -8.0])date_032 = np.array([-10.0, -11.0, -8.0])date_033 = np.array([-9.0, -12.0, -7.0])diff_028_032 = date_032 - date_028diff_032_033 = date_033 - date_032diff_028_033 = date_033 - date_028
```

Expected results:

| Pixel | 028→032 | 032→033 | 028→033 |
| ----- | ------- | ------- | ------- |
| 1     | +2      | +1      | +3      |
| 2     | -1      | -1      | -2      |
| 3     | 0       | +1      | +1      |

The mathematical consistency check must pass:

\\[ \Delta\_{28,33} = \Delta\_{28,32}+\Delta\_{32,33} \\]

### Test 3 — Mask correctness

Create a small synthetic mask containing:

- Valid subswath values.
- Zero.
-

255.

1) Invalid HH.
2) Invalid HV.

Verify that the resulting common-valid mask excludes every pixel that fails the applicable validity conditions.

### Test 4 — Area calculations

For a 10 m × 10 m raster:

```
pixel_area_km2 = 100 / 1_000_000pixel_count = 10000area_km2 = pixel_count * pixel_area_km2print(area_km2)
```

Expected result:

```
1.0
```

These small tests establish whether the processing functions work independently of the full NISAR dataset.

## 9.5 Raster integrity validation

Every exported GeoTIFF must pass structural and spatial checks.

| Check           | Expected result         |
| --------------- | ----------------------- |
| Width           | Matches the AOI         |
| Height          | Matches the AOI         |
| CRS             | Correct                 |
| Transform       | Correct                 |
| Resolution      | Expected                |
| Data type       | Appropriate             |
| NoData          | Explicit and consistent |
| Band count      | Matches product         |
| Raster bounds   | Matches AOI             |
| Pixel alignment | Matches source grid     |

### Additional checks

- Difference rasters must have the same dimensions and transform as their inputs.
- The cluster map must align exactly with the feature stack.
- The change category map must not encode invalid pixels as stable.
- NoData must not accidentally be included in the color stretch.
- Raster previews must preserve the intended spatial orientation.

A visually attractive raster can still be spatially incorrect. Structural validation is therefore essential.

## 9.6 ML validation

Your project uses unsupervised clustering. This creates a specific validation challenge: there are no confirmed ecological labels against which to measure classification accuracy.

Therefore, use internal consistency, reproducibility, and spatial diagnostics, rather than claiming ecological classification accuracy.

### A. Input validation

Before training, check:

- Feature count.
- Feature ordering.
- Feature units.
- Raster dimensions.
- CRS and geotransform.
- Common-valid mask.
- NaN and infinite values.
- Feature distributions.

### B. Cluster population

For each cluster, report:

- Number of pixels.
- Percentage of valid samples.
- Area.
- Centroid values.
- Minimum and maximum feature values, where useful.

Look for:

- Empty clusters.
- Extremely small clusters.
- One cluster dominating almost the entire sample.
- Unusual centroid values.

These conditions do not automatically invalidate the model, but they require investigation.

### C. Reproducibility

Run the model twice with identical:

- Input data.
- Feature order.
- Scaler.
- Configuration.
- Random seed.
- Software environment.

Compare:

- Cluster population.
- Centroid locations.
- Model configuration.
- Predicted partitions.

Cluster IDs can be permuted between runs. For example, cluster 0 and cluster 2 may exchange labels without changing the underlying partition. Compare partitions or aligned centroids rather than demanding identical numeric cluster IDs.

### D. Sensitivity analysis

If time allows, test:

- Three clusters.
- Four clusters.
- Five clusters.

Compare the resulting partitions and cluster sizes.

Do not automatically select the model with the highest number of clusters. More clusters do not necessarily mean better scientific information.

### E. Spatial diagnostics

Check whether clusters are:

- Spatially distributed.
- Concentrated in a small area.
- Fragmented into isolated pixels.
- Associated with particular temporal responses.

These checks help determine whether the outputs are useful for exploration.

### F. Validation statement

Use this language:

> The unsupervised clustering model was evaluated using input integrity checks, cluster-population analysis, centroid inspection, and reproducibility tests. Its clusters represent groups of similar radar-response patterns, not independently validated ecological classes.

## 9.7 Application and API testing

The application must be tested with real data, not only sample JSON.

### Backend tests

Test:

| Endpoint                    | Test                               |
| --------------------------- | ---------------------------------- |
| `/api/health`               | Server availability                |
| `/api/project`              | Correct project metadata           |
| `/api/acquisitions`         | Correct three dates                |
| `/api/layers`               | Only available layers registered   |
| `/api/layers/{id}/metadata` | Correct CRS, dimensions, and units |
| `/api/layers/{id}/preview`  | Valid preview returned             |
| `/api/statistics/overview`  | Correct statistics                 |
| `/api/ml/status`            | Actual ML status                   |
| `/api/reports`              | Actual report availability         |

Also test invalid layer IDs and missing files.

### Frontend tests

Verify:

- Navigation works.
- The map displays the actual AOI.
- Layer selection changes the map.
- Date selection changes the displayed observation.
- HH/HV selection works.
- Difference maps use correct legends.
- Statistics correspond to the selected layer.
- ML unavailable state works.
- Reports open and download correctly.
- Loading and error states are visible.

### Offline test

Disconnect the internet and restart the application.

Verify that:

1. The frontend loads.
2. The backend starts.
3. Local raster data loads.
4. The temporal analysis works.
5. ML artifacts can be read locally.
6. No mandatory external API key is required.

If the basemap disappears, the NISAR raster must remain explorable.

## 9.8 Performance testing

Your hardware has an Intel i5-14500, RX 580 8 GB, and 16 GB RAM.

The application and processing pipeline should be designed around these constraints.

### Recommended performance rules

- Use windowed HDF5 extraction.
- Do not load complete granules into memory.
- Avoid keeping multiple full-size feature arrays in RAM.
- Use raster windows or chunked processing.
- Use downsampled PNG previews.
- Serve map tiles or small raster windows.
- Avoid transferring full-resolution GeoTIFF arrays to the browser.
- Keep ML sample sizes configurable.
- Avoid retraining the model on every application launch.

### What to measure

Record:

| Metric                  | Measurement    |
| ----------------------- | -------------- |
| HDF5 extraction time    | Actual seconds |
| Feature generation time | Actual seconds |
| ML training time        | Actual seconds |
| ML prediction time      | Actual seconds |
| Backend startup time    | Actual seconds |
| Frontend startup time   | Actual seconds |
| Peak RAM usage          | Actual MB/GB   |
| Largest output size     | Actual MB      |
| Map layer loading time  | Actual seconds |

Do not invent benchmark figures. Measure the actual system.

## 9.9 Automated test organization

Recommended test layout:

```
tests/
├── test_metadata.py
├── test_aoi.py
├── test_masks.py
├── test_backscatter.py
├── test_temporal_differences.py
├── test_statistics.py
├── test_raster_export.py
├── test_ml_inputs.py
├── test_ml_outputs.py
├── test_api.py
└── test_integration.py
```

Use `pytest` for Python-side tests.

A minimum viable test suite should cover:

1. Metadata.
2. AOI mapping.
3. Mask handling.
4. Backscatter conversion.
5. Temporal difference calculations.
6. Area calculations.
7. Raster alignment.
8. ML input validation.
9. API health and layer availability.

Do not spend the remaining time building an elaborate testing framework. A small set of meaningful automated tests is better than a large set of superficial tests.

## 9.10 Final scientific validation report

Create:

`data/reports/final_validation_report.md`

Recommended sections:

1. Project and dataset identification.
2. Granule metadata verification.
3. AOI spatial verification.
4. Acquisition coverage.
5. Data preprocessing.
6. Backscatter conversion.
7. Temporal difference validation.
8. Common-valid mask validation.
9. Raster integrity.
10. ML validation.
11. Application integration.
12. Performance measurements.
13. Known limitations.
14. Final validation status.

Use three statuses:

PASS

The check passed with recorded evidence.

PARTIAL

Some functionality works, but validation is incomplete.

FAIL

The check failed or produced an unacceptable result.

Never mark an untested feature as PASS.

## 9.11 Ready-to-paste OpenCode validation assignment

# OPENCODE — FINAL SCIENTIFIC AND TECHNICAL VALIDATION

## Role

Act as the independent QA and verification engineer for Dancing with SARs.

Your job is to establish whether the project works correctly, not to make the reports appear successful.

## Validation scope

### 1. Source data

Verify the three NISAR L2 GCOV granules:

- Cycle 028
- Cycle 032
- Cycle 033

Check identity, dates, polarization, dimensions, CRS, geotransform, resolution, and mask convention.

### 2. AOI

Verify the Potengi Estuary AOI using actual coordinate transformations and source raster metadata.

Do not trust previously generated AOI reports without checking the underlying data.

Calculate actual per-date and common-valid AOI coverage.

### 3. Scientific processing

Test:

- Linear-to-dB conversion.
- HH/HV separation.
- Temporal differences.
- Common-valid mask.
- Change categories.
- Area calculations.
- Summary statistics.

Use synthetic unit tests and actual-data validation.

### 4. Raster integrity

Check CRS, dimensions, transform, bounds, NoData, data type, and pixel alignment for every major output.

### 5. ML

Validate:

- Feature order.
- Feature count.
- Mask compatibility.
- Scaler and model artifacts.
- Cluster population.
- Centroid values.
- Reproducibility.
- Spatial alignment.

Do not claim ecological accuracy without independent labels.

### 6. Backend and frontend

Test all implemented APIs and the main user interactions.

Use real project files. Check that missing layers and unavailable ML results are handled honestly.

### 7. Offline execution

Test the complete application with internet disconnected.

### 8. Performance

Measure actual execution time, peak memory, output sizes, and layer-loading time.

## Evidence requirements

For each test record:

- Test identifier.
- Procedure.
- Expected result.
- Actual result.
- PASS / PARTIAL / FAIL.
- Relevant output or log.
- Any limitation.

## Final deliverables

Generate:

- final_validation_report.md
- automated_test_results.md
- application_integration_report.md
- performance_report.md

Do not modify source scientific data to make a test pass.

Do not fabricate test results.

Prioritize correctness of the AOI, actual NISAR observations, temporal calculations, and application visualization.

## 9.12 Final acceptance criteria

Submission-critical checks

0 / 11 completed

0%

Three NISAR acquisitions independently verified

Potengi AOI spatial mapping verified

HH/HV data and masks validated

Six temporal differences numerically validated

Common-valid coverage calculated for the AOI

GeoTIFF spatial metadata verified

Actual NISAR layers visible in application

Statistics match independent calculations

ML limitations documented

Application works locally

Final validation report generated

My recommendation: Do not sacrifice AOI verification or temporal-difference validation to add more ML features. Those two areas have a direct impact on whether the scientific demonstration is credible.


