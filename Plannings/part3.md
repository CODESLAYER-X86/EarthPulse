# PART 3 OF 12 — Machine Learning Model Architecture



Scientific and technical design

Claude + OpenCode + Antigravity



This is one of the most important parts of our project. We need to decide exactly what the ML model will do before Claude writes its code.

My recommendation: Build a lightweight, pixel-based change-analysis model that combines NISAR's HH/HV backscatter observations across the three dates. Use an unsupervised or weakly supervised approach for the initial prototype, with independent reference data to help interpret the results.

I would not start with a large deep-learning model such as U-Net. We have three acquisitions, limited time, and no confirmed ground-truth training dataset. A complex model could produce impressive-looking predictions without scientifically reliable labels.

## 3.1 What problem should the ML model solve?

Our project should answer this question:

> Where did radar-observed surface characteristics change across the Potengi Estuary between August and October 2026, and what types of changes might those observations indicate?

We can divide this into three analytical tasks.

Primary task

Task A — Detect spatial changes

Identify pixels or spatial regions where HH/HV backscatter changes significantly between acquisitions.

[Urban Building Change Detection in SAR Images Using Combined Differential Image and Residual U-Net Network](https://images.openai.com/static-rsc-4/FkA3UC9UnAN5x6n2PbopgW1LJgDHirCBo-HaxuBwwPdep0hYdoWNML93JPPLcQ4lYOMGdSqSBWKRy9pS2ZF9VGUsTiXlmetW7WOL_eJQMzMQw1HoYRtYh8jmJzemrOncsp0pri7EZITyz-gQW4CdeTzoFRsj2vBFp0JlbIDr_dQ?purpose=inline)

[mdpi.com](https://www.mdpi.com/2072-4292/11/9/1091?utm_source=chatgpt.com)

Secondary task

Task B — Group similar changes

Group pixels into categories such as stable radar response, increased response, decreased response, and unusual temporal behavior.

[Unsupervised Classification using Google Earth Engine - CUOSGwiki](https://images.openai.com/static-rsc-4/CW8RmtfMMKAQ7gs_PJrE-imzjjnrJdQWCl6HhBpxY_R850TvnOcrB68l14OkYa4GIKsbDc700xk1_tbHoDpG2VPAP4Xu41k6TueA9YxKW0LrD7apMvjTTO8xPe44ZHEhmAWTTdyZyLkTEuRJSPD9N3GAU8aqYs_U-IF_etk8Hds?purpose=inline)

[dges.carleton.ca](https://dges.carleton.ca/CUOSGwiki/index.php/Unsupervised_Classification_using_Google_Earth_Engine?utm_source=chatgpt.com)

Interpretation task

Task C — Support ecological interpretation

Compare detected radar changes with mangrove reference information, surface-water data, and other available evidence.

[Discrimination of Mangrove Stages Using Multitemporal Sentinel-1 C-Band Backscatter and Sentinel-2 Data—A Case Study in Samut Songkhram Province, Thailand | MDPI](https://images.openai.com/static-rsc-4/-hv_UN1_QFPNvxd4j6ZxD1hmoBvdcLCerJwn59G_ML4b0aQZyxJNsT0ihUyF4b8MOl_8sQKOtkxcmXVXJDoD4OVpDDtdO2J64-5kOBLuSKihsv4BkE_gpzIszJFlwMDdIZLsptOcKOUSq3cxWMJnWW796Arzi3VzD5QsHX511XI?purpose=inline)

[mdpi.com](https://www.mdpi.com/1999-4907/13/9/1433?utm_source=chatgpt.com)

These tasks must remain distinct. Detecting a radar change is not the same as proving mangrove loss.

## 3.2 What should the model predict?

I recommend the following initial output classes:

| Class | Name                  | Meaning                                   |
| ----- | --------------------- | ----------------------------------------- |
| 0     | Stable                | No significant detected radar change      |
| 1     | Increased backscatter | HH/HV response increased                  |
| 2     | Decreased backscatter | HH/HV response decreased                  |
| 3     | Complex change        | Unusual or inconsistent temporal response |
| 4     | Insufficient data     | Invalid or inadequate observations        |

These are radar-change categories, not ecological labels.

For example:

- Class 1 does not automatically mean mangrove growth.
- Class 2 does not automatically mean deforestation.
- Class 3 may reflect multiple environmental or observational factors.
- Class 4 must not be confused with Class 0.

This distinction is essential to the scientific credibility of the project.

## 3.3 Recommended model architecture

I recommend a hybrid change-detection architecture with three components.

NISAR FEATURE STACK

HH/HV · Temporal differences · Polarimetric ratios · Validity

COMPONENT 1 — STATISTICAL CHANGE DETECTION

Identify significant HH/HV increases and decreases.

COMPONENT 2 — UNSUPERVISED ML

MiniBatch K-Means groups pixels with similar temporal radar behavior.

COMPONENT 3 — CHANGE INTERPRETATION

Combine statistical evidence, cluster behavior, and reference data.

OUTPUT

Change map · Cluster map · Change statistics · Confidence/quality indicators

Why this architecture?

- Statistical detection provides understandable, reproducible measurements.
- Unsupervised ML finds groups of pixels with similar patterns without requiring manually labeled training data.
- Reference datasets help interpret those patterns without pretending they are perfect ground truth.

The analogy is a medical examination: statistical tests identify measurable abnormalities, ML groups similar patterns, and additional clinical evidence helps interpret what those patterns might mean.

### Selected algorithms

| Component                 | Algorithm                     | Decision                                 |
| ------------------------- | ----------------------------- | ---------------------------------------- |
| Directional change        | Robust statistical thresholds | Required                                 |
| Temporal pattern grouping | MiniBatch K-Means             | Recommended ML model                     |
| Anomaly scoring           | Isolation Forest              | Optional                                 |
| Supervised classification | Random Forest / XGBoost       | Only if reliable labels become available |
| Image segmentation        | U-Net / CNN                   | Not recommended for this deadline        |

Why MiniBatch K-Means?

It is lightweight, CPU-friendly, and suitable for grouping a large number of pixel feature vectors. It does not require a GPU or thousands of manually labeled images.

It is also relatively easy for Claude to implement and OpenCode to run.

## 3.4 Model input features

The model needs a consistent numerical representation of each valid pixel.

For every pixel, we have three observations:

- HH at Cycle 028, 032, and 033.
- HV at Cycle 028, 032, and 033.

That gives six primary backscatter features.

We then calculate six temporal differences.

Primary feature vector

\\[ X = [HH_1, HH_2, HH_3, HV_1, HV_2, HV_3] \\]

Temporal feature vector

\\[ D = [\Delta HH\_{12},\Delta HH\_{23},\Delta HH\_{13}, \Delta HV\_{12},\Delta HV\_{23},\Delta HV\_{13}] \\]

Combined feature vector

\\[ F = [X,D] \\]

12 primary features per pixel

Additional candidate features:

| Feature                     | Purpose                                           |
| --------------------------- | ------------------------------------------------- |
| HH/HV ratio in dB           | Compare co-polarized and cross-polarized response |
| Temporal mean               | Represent typical backscatter                     |
| Temporal standard deviation | Represent temporal variability                    |
| Local spatial variability   | Distinguish isolated pixels from coherent regions |

These additional features should be optional until we test whether they improve the results. Avoid unnecessary feature duplication.

### Normalization

Before clustering, Claude should apply robust feature scaling.

For example, a feature with values between -30 and 0 should not dominate another feature merely because of its numerical range.

Use a robust scaler based on median and interquartile range, fitted on the valid training sample only.

The same fitted scaler must be reused during inference.

Do not independently normalize each acquisition or each inference batch; doing so can distort temporal relationships.

## 3.5 How the ML model learns patterns

MiniBatch K-Means groups pixels based on similarity.

Imagine sorting thousands of photographs into four piles based on their visual characteristics. You do not initially tell the algorithm which pile means forest loss or water change. It discovers groups with similar features.

For our project:

1. Select valid pixel feature vectors.
2. Fit a scaler.
3. Fit MiniBatch K-Means with an initial target of four clusters.
4. Assign each valid pixel to a cluster.
5. Analyze the cluster centroids.
6. Compare the temporal signatures of each cluster.
7. Give clusters descriptive labels only when their behavior supports those labels.

For example:

| Cluster behavior                     | Possible descriptive label       |
| ------------------------------------ | -------------------------------- |
| Small changes in both HH and HV      | Relatively stable radar response |
| Predominantly positive differences   | Increased backscatter pattern    |
| Predominantly negative differences   | Decreased backscatter pattern    |
| Opposing or inconsistent differences | Complex temporal response        |

The model's cluster numbers are arbitrary. Cluster `0` does not inherently mean stable, and cluster `1` does not inherently mean vegetation loss.

The code must determine descriptive labels from the actual cluster centroids rather than hardcoding cluster IDs.

Important: If the clusters do not separate into four meaningful patterns, the system must report that result rather than force a misleading interpretation.

## 3.6 Statistical change detection

This component works alongside the ML model.

For every valid pixel, calculate the temporal difference in dB.

For example:

\\[ \Delta HH = HH\_{033,\mathrm{dB}} - HH\_{028,\mathrm{dB}} \\]

We can initially define three directional categories:

- Significant increase.
- Relatively stable.
- Significant decrease.

However, we should not invent a universal threshold such as ±3 dB without examining the actual data.

### Recommended threshold method

Use a robust, data-driven threshold based on the distribution of observed changes.

One option is:

\\[ T = \max(T\_{\min}, k \times MAD) \\]

Where:

- \\(MAD\\) is the median absolute deviation of the change distribution.
- \\(k\\) is a configurable multiplier.
- \\(T\_{\min}\\) is a minimum practical threshold.

Then:

\\[ \text{Class} = \begin{cases} \text{Increase}, & \Delta > T\\\ \text{Decrease}, & \Delta < -T\\\ \text{Stable}, & -T \leq \Delta \leq T \end{cases} \\]

The threshold should be estimated from appropriate valid pixels and documented.

We should also inspect HH and HV separately. A strong HH change with little HV change may represent a different scattering response from a simultaneous change in both channels.

### Why use this alongside ML?

The statistical layer gives us a transparent answer to:

"How much did the radar backscatter change?"

The ML layer gives us a different answer:

"Which pixels have similar multi-temporal radar behavior?"

Combining them gives a stronger analytical platform than relying on clustering alone.

## 3.7 Anomaly detection — optional extension

If time permits, add Isolation Forest.

It can identify pixels with unusual feature combinations compared with the wider AOI.

Potential outputs:

- Anomaly score raster.
- Binary unusual-response mask.
- Ranked anomalous regions.

But an anomaly is not automatically an environmental event. It may also reflect noise, water conditions, or unusual acquisition behavior.

I recommend making this a P1 feature, not a dependency for the first working model.

## 3.8 Training and inference strategy

We need to distinguish training from inference.

For our unsupervised model:

Training / fitting

1. Read valid pixel feature vectors.
2. Select a reproducible representative sample.
3. Fit the feature scaler.
4. Fit MiniBatch K-Means.
5. Save the model and scaler.
6. Save cluster centroids and descriptive cluster metadata.

Inference

1. Read the full AOI feature stack.
2. Apply the saved scaler.
3. Assign each valid pixel to its nearest cluster.
4. Generate prediction rasters.
5. Apply the validity mask.
6. Calculate cluster statistics.

For the 25 km² candidate, there are 250,000 pixels. This is manageable for the proposed model on your CPU.

A sample of up to 100,000 valid pixels is a reasonable starting point, but the actual sample size should depend on available valid pixels and runtime.

Use a fixed random seed so the results are reproducible.

### What we should not do

- Do not train on invalid pixels.
- Do not treat three acquisitions as three independent ground-truth labels.
- Do not report supervised accuracy when there are no verified labels.
- Do not randomly split neighboring pixels and claim that this demonstrates geographic generalization.
- Do not claim that the model detects deforestation simply because a cluster has decreasing backscatter.

## 3.9 Validation strategy

An unsupervised model does not have conventional classification accuracy unless independent reference labels are available.

We need several different checks.

| Validation                  | What it tells us                                                    |
| --------------------------- | ------------------------------------------------------------------- |
| Valid-pixel coverage        | How much of the AOI can be analyzed                                 |
| Cluster population          | Whether clusters contain meaningful numbers of pixels               |
| Cluster centroid inspection | Whether clusters represent distinct temporal patterns               |
| Sampling stability          | Whether results change drastically with different samples           |
| Spatial coherence           | Whether results form meaningful regions rather than random speckles |
| Reference-layer comparison  | Whether detected patterns overlap relevant ecological features      |
| Temporal consistency        | Whether the two intervals show plausible behavior                   |

For Global Mangrove Watch, ESA WorldCover, JRC Surface Water, and Sentinel-2, the model should use only data that has actually been acquired and inspected.

Reference layers should not be treated as interchangeable ground truth.

For example, an annual mangrove map cannot directly prove that a specific pixel lost mangroves between two NISAR acquisitions only 12 days apart.

## 3.10 Model outputs

The ML pipeline must produce outputs that Antigravity can display directly.

| Output                                 | Format               | Purpose                        |
| -------------------------------------- | -------------------- | ------------------------------ |
| Cluster classification                 | GeoTIFF              | Spatial cluster map            |
| Cluster statistics                     | JSON/CSV             | Pixel counts and area          |
| Anomaly scores                         | GeoTIFF, optional    | Unusual-response visualization |
| Change categories                      | GeoTIFF              | Increase/stable/decrease       |
| Feature importance or centroid summary | JSON                 | Explain model behavior         |
| Model metadata                         | JSON                 | Reproducibility                |
| Model artifact                         | Joblib or equivalent | Reuse fitted model             |

For every prediction output, retain:

- CRS.
- Spatial transform.
- Raster dimensions.
- NoData definition.
- AOI identifier.
- Acquisition dates.
- Model version.
- Processing version.

### Confidence and uncertainty

Do not call the distance to a K-Means centroid a calibrated probability.

Instead, expose it as a distance or cluster-fit measure, and clearly document its meaning.

Similarly, any statistical confidence indicator must have a defined calculation. Do not manufacture confidence percentages just to make the dashboard look impressive.

## 3.11 What the user will see in the application

The ML results should appear as a dedicated analysis section.

[Enterprise-Grade Crop Intelligence | Optimize Farming with Satellite Analytics | EarthDaily](https://images.openai.com/static-rsc-4/If2wWQwo0j9Q-P1JR6rdkW8YKIEnCI_rfVyYl-NK3CYpKpshgIAIxiSint5-5Pd1uv0GuWoBJ8Pv1HIHCtSMxTlNmAt7CPLE9yn6YHYe76caoA1K0Bl8PHiAbe9CQAep7VMut557exN8_w7m9pKDa7v8SC56XZh92yo-WFQeH0A?purpose=inline)

[earthdaily.com](https://earthdaily.com/digital-ag?utm_source=chatgpt.com)

Proposed interface:

Change Analysis

- Cluster map.
- Radar-change category map.
- HH/HV change comparison.
- Cluster area distribution.
- Number of valid and invalid pixels.
- Selected date interval.
- Model method and parameters.
- Explanation of each detected pattern.

The user should be able to select a cluster and inspect its HH/HV temporal signature.

For example, clicking a cluster should show:

- Number of pixels.
- Approximate area.
- Mean HH/HV for each acquisition.
- Mean temporal difference.
- Cluster centroid.
- Related reference-layer overlap, if available.

This makes the ML result interpretable rather than just displaying an unexplained colored map.

## 3.12 Exact implementation instructions for Claude.ai

This is the most important deliverable from this part. Claude will write the ML source code, so it needs a precise technical assignment.

# ML DEVELOPMENT SPECIFICATION

## NASA Space Apps 2026 — NISAR Multi-Temporal Change Analysis

### 1. Your role

Act as a remote-sensing and machine-learning engineer.

Develop a lightweight, reproducible machine-learning pipeline for analyzing multi-temporal NISAR L2 GCOV Frequency A observations over the Potengi Estuary, Brazil.

The application is being developed separately using Antigravity and Gemini 3.8 Flash.

OpenCode will execute your Python implementation locally and validate the outputs.

### 2. Scientific objective

Identify and group spatial pixels with similar radar backscatter behavior across three NISAR acquisitions:

- Cycle 028: 2026-08-22
- Cycle 032: 2026-10-09
- Cycle 033: 2026-10-21

The model must identify radar-observed changes, not automatically classify those changes as mangrove loss or gain.

### 3. Recommended architecture

Implement a hybrid approach:

A. Statistical change detection:

- HH and HV temporal differences in dB.
- Robust, data-driven change thresholds.
- Stable, increased, and decreased backscatter categories.
- Separate HH/HV results.

B. Unsupervised machine learning:

- MiniBatch K-Means.
- Initial target: four clusters.
- RobustScaler or an appropriately justified alternative.
- Reproducible representative sampling.
- Fixed random seed.
- Saved model and scaler.

C. Optional anomaly detection:

- Isolation Forest.
- Include only if it can be implemented and tested without compromising the core pipeline.

### 4. Expected model inputs

The primary feature stack contains:

1. HH dB Cycle 028
2. HH dB Cycle 032
3. HH dB Cycle 033
4. HV dB Cycle 028
5. HV dB Cycle 032
6. HV dB Cycle 033
7. HH difference 028–032
8. HH difference 032–033
9. HH difference 028–033
10. HV difference 028–032
11. HV difference 032–033
12. HV difference 028–033

Optional features may include:

- HH/HV ratios.
- Temporal mean.
- Temporal standard deviation.
- Local spatial variability.

Do not require optional features unless their usefulness is demonstrated.

### 5. Input contract

OpenCode will provide:

- Georeferenced raster layers.
- A common-valid mask.
- Feature metadata JSON.
- AOI configuration.
- Acquisition metadata.

Do not assume filenames or dataset paths without reading the provided feature metadata.

Validate all input dimensions, data types, CRS and NoData definitions.

Use only common-valid pixels for the primary three-date model.

### 6. Processing requirements

- Read raster data efficiently.
- Avoid unnecessary memory copies.
- Exclude invalid pixels.
- Handle NaN and infinity safely.
- Fit the scaler only on the representative training sample.
- Reuse the same scaler for inference.
- Use deterministic sampling.
- Keep the implementation CPU-friendly.
- Support the user's 16 GB RAM environment.

### 7. Cluster interpretation

Do not assign semantic meaning to cluster numbers directly.

Analyze cluster centroids and temporal feature patterns.

Derive descriptive labels from actual cluster behavior:

- Relatively stable radar response.
- Increased backscatter response.
- Decreased backscatter response.
- Complex temporal response.

If the clusters do not clearly support these labels, use neutral names such as Cluster A, B, C and D.

Do not force ecological interpretations.

### 8. Statistical change detection

Implement HH and HV differences independently.

Estimate robust thresholds using the observed valid-pixel distributions.

Make threshold parameters configurable.

Document the threshold method and actual values.

### 9. Outputs

Produce:

- cluster_map.tif
- hh_change_categories.tif
- hv_change_categories.tif
- optional anomaly_score.tif
- cluster_statistics.json
- cluster_statistics.csv
- cluster_centroids.json
- model_metadata.json
- fitted_model.joblib
- fitted_scaler.joblib
- model_execution_report.md

Preserve the original feature stack.

All prediction rasters must retain the correct spatial reference, transform, dimensions and NoData handling.

### 10. Validation

Evaluate:

- Cluster populations.
- Cluster centroid separation.
- Reproducibility across repeated sampling.
- Sensitivity to the number of clusters.
- Spatial coherence.
- Reference-layer overlap, where reference data is available.

Do not report conventional classification accuracy without independent ground-truth labels.

Do not invent model confidence or probabilities.

### 11. Code organization

Provide modular Python code with separate functions for:

- Input loading.
- Input validation.
- Feature preparation.
- Sampling.
- Scaling.
- Model fitting.
- Inference.
- Statistical change detection.
- Cluster interpretation.
- Raster export.
- Validation.
- Reporting.

Provide:

- requirements.txt
- README.md
- execution instructions
- expected input directory structure
- expected output directory structure

### 12. Execution compatibility

Target:

- Python 3.12.
- Linux.
- CPU execution.
- NumPy, SciPy, scikit-learn, rasterio and other dependencies only where needed.

Avoid unnecessary large frameworks and GPU dependencies.

### 13. Development rules

Before writing code, inspect the actual input metadata and confirm the feature contract.

Do not invent missing datasets.

If the expected input files are unavailable, provide a clear list of missing requirements rather than generating fabricated data.

Write complete executable code, not pseudocode.

The final implementation must be runnable by OpenCode locally and produce georeferenced prediction outputs that Antigravity can integrate.

## 3.13 Exact integration contract for Antigravity

Antigravity should not need to understand the internal ML implementation. It needs to understand the model's inputs and outputs.

# ANTIGRAVITY — ML INTEGRATION SPECIFICATION

The application must integrate a separately developed NISAR machine-learning engine.

The ML engine is developed by Claude.ai and executed locally through OpenCode.

### ML outputs to support

1. Cluster classification GeoTIFF.
2. HH change-category GeoTIFF.
3. HV change-category GeoTIFF.
4. Optional anomaly-score GeoTIFF.
5. Cluster statistics JSON.
6. Model metadata JSON.
7. Cluster centroid information.

### Required interface

Create an ML Analysis section with:

- Enable/disable ML result layers.
- Cluster map visualization.
- HH change categories.
- HV change categories.
- Cluster selection.
- Cluster statistics.
- Temporal feature summaries.
- Model method and parameters.
- Data-quality indicators.

### Cluster details

When a user selects a cluster, display:

- Cluster description.
- Pixel count.
- Area in km².
- Percentage of valid AOI.
- Mean HH/HV backscatter by date.
- Mean temporal differences.
- Reference-layer overlap, if available.

### Scientific requirements

- Preserve NoData areas.
- Never treat invalid pixels as stable.
- Never label decreasing backscatter as confirmed deforestation.
- Do not represent cluster distance as a probability.
- Display the model method and limitations.
- Do not fabricate results when model outputs are missing.

### Integration behavior

The application must remain functional if optional anomaly detection is unavailable.

Use the model metadata and raster metadata to identify compatible outputs.

Do not hardcode arbitrary prediction values or example results as actual scientific findings.

## 3.14 Recommended implementation order

Here is how I want the tools to work together:

1. Finalize the feature contract

   OpenCode verifies the AOI, extraction dimensions and feature names.
2. Generate a representative dataset

   OpenCode exports the small AOI feature stack and metadata.
3. Develop the ML engine

   Claude receives the exact feature contract and creates the complete Python implementation.
4. Execute and validate

   OpenCode runs the model and inspects the resulting prediction rasters.
5. Integrate the results

   Antigravity connects the verified outputs to the ML Analysis interface.

The frontend and backend can be developed in parallel with ML implementation, provided the output contract is agreed upon first.

## 3.15 Final technical decisions

Primary ML approach

Selected

MiniBatch K-Means + statistical change detection.

Optional model

Isolation Forest for unusual radar-response patterns.

Not recommended for initial delivery

U-Net, large CNNs, and supervised deep learning without suitable labels.

Primary model inputs

12 temporal HH/HV features, using the common-valid mask.

Primary model output

Georeferenced cluster map and interpretable temporal change categories.

Execution

Local CPU inference through OpenCode.

## Part 3 completion checklist

- Scientific ML objective defined.
- Prediction categories defined.
- Hybrid architecture selected.
- Feature vector specified.
- Normalization strategy specified.
- Training and inference strategy defined.
- Validation strategy established.
- Output formats defined.
- Claude implementation specification prepared.
- Antigravity integration specification prepared.

My recommendation: Do not ask Claude to start coding the model until OpenCode can provide the actual feature metadata and a representative extracted dataset. Claude can prepare the implementation structure now, but the final code must match real inputs.

### Next: Part 4 — Complete ML Implementation and Execution Architecture

We will specify the Python project structure, model lifecycle, training/inference commands, configuration files, dependency management, error handling, model artifacts, and the exact handoff between Claude and OpenCode.

Type next when ready.
