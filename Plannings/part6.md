# PART 6 OF 12 — Frontend Architecture and UI/UX Design



Antigravity implementation

Core application experience



## 6.1 Frontend objective

The frontend is where the scientific work becomes understandable and useful.

The application should let a user:

1. Explore the Potengi Estuary study area.
2. View the three NISAR acquisition dates.
3. Compare HH and HV backscatter across dates.
4. Visualize temporal radar changes.
5. Inspect statistical and ML-derived change categories.
6. Understand data quality, uncertainty, and limitations.
7. Export results and supporting reports.

Design principle: The map is the primary workspace. Charts, statistics, and analysis controls should support the map rather than compete with it.

Think of a professional GIS application: the map occupies the central workspace, while the surrounding panels help users control and interpret what they see.

## 6.2 Recommended visual identity

The application should have a scientific Earth-observation aesthetic.

[遥感智能解译平台 | 遥感数据处理平台](https://images.openai.com/static-rsc-4/AhQIc2d9ledCDu6gRBLb58TfU1moPujAos8AVy5nAjGL68f-_O-PuAeJXxVP4OGQFaIdvYUVRnngpib0vX9WsQYlVlgm6S7kfHNfxWWWuxL5QD73zXd6unW39WGchkZTxcgvMU-PjMHmhlB7CoQPCj2mtFstTRU30IwhYbgkoBA?purpose=inline)

[Ecosystem](https://images.openai.com/static-rsc-4/WahuqUAvRdtNPdsVpyv8Nk6PHi7cfuAVTPU1vCSKHN8DAKhwkK3A-vz5TRoScym6AH44dlxnTffZGdQra-YepHMruEFohU0wbF_R2W2zXICTfLnhsx4pU0IXCfA4SL7d2zg1yKKvrnnq_1xqBBbTrsQ-Wv11XAR1KxZSeDPu5_0?purpose=inline)

[Aurora by Pixxel | Next-Gen Satellite Analytics Platform](https://images.openai.com/static-rsc-4/wm0ph0pxgrLFlV-Pe40pzQJaTls1qVXplWYuIt6eChRA3bhevPS9cj8LmNoqJ-0KAju_dccyj8e8SOXz0_NNN6iMT1m4bW4La-UoG7fdBMjbu3tEl4MoCCvczbRL6oFi1iNJnzDxn304hVQ6l-F7UKLzbr7cCvhQKDIOvaciIHM?purpose=inline)

11

### Visual direction

| Element              | Recommendation                 |
| -------------------- | ------------------------------ |
| Theme                | Dark scientific interface      |
| Primary background   | Deep navy / charcoal           |
| Secondary surfaces   | Dark slate                     |
| Accent               | Cyan or electric blue          |
| Secondary accent     | Teal                           |
| Change visualization | Diverging color scale          |
| Typography           | Inter or equivalent            |
| Map                  | Large, high-contrast workspace |
| Charts               | Minimal, technical, readable   |

Avoid excessive gradients, glowing borders, glass effects, and decorative animations.

The interface should communicate scientific credibility, not gaming aesthetics.

### Color semantics

Use consistent colors throughout the application:

| Meaning                     | Suggested color          |
| --------------------------- | ------------------------ |
| Stable radar response       | Neutral grey             |
| Increased backscatter       | Orange                   |
| Decreased backscatter       | Blue                     |
| Complex temporal response   | Purple                   |
| Invalid / insufficient data | Dark grey or transparent |
| Selected layer              | Cyan                     |

These colors describe radar response, not ecological condition.

For example, blue must not automatically mean water loss or orange must not automatically mean mangrove growth.

## 6.3 Application navigation

Use a left sidebar with five primary sections.

DANCING WITH SARS

NISAR EARTH OBSERVATION PLATFORM

01 — Overview

02 — Explore Map

03 — Temporal Analysis

04 — ML Insights

05 — Reports

About the Project

Data & System Status

### Navigation responsibilities

1. Overview: Project summary, acquisition dates, coverage, and key findings.
2. Explore Map: Main geospatial visualization workspace.
3. Temporal Analysis: Date-to-date and polarization comparisons.
4. ML Insights: Cluster map, statistical change classes, and model limitations.
5. Reports: Dataset, processing, validation, and scientific methodology.

Do not create separate navigation items for every individual raster layer. Those belong in the map's layer controls.

## 6.4 Page 1 — Overview dashboard

[Site Sentry | From Noise to Signal — Gabriela Santos Rodriguez](https://images.openai.com/static-rsc-4/_UYFDo_6O_vzWLsrE0LbEFUIhyVeP_5HTyhMwgdR8ut78P514GyD5Qb072cEMsAspLJYhvf7zD-KhpLcK4exkKH7JPGCJJPfSLhsaGkUU4yXTAYPoCxyo6zHv9L8CEByjK56vNmEdKJq8srldjFw5SRwBikBcySuR7G4NE3Yv2Y?purpose=inline)

[gabrielasantosplot.com](https://www.gabrielasantosplot.com/site-sentry?utm_source=chatgpt.com)

The overview page should answer four questions immediately:

- What area is being studied?
- Which satellite observations are available?
- What has been analyzed?
- Where can the user explore the results?

### Layout

Header

- Application title.
- Study area: Potengi Estuary, Natal, Brazil.
- Data source: NISAR L2 GCOV.
- Dataset status indicator.

Summary cards

| Card                  | Content                        |
| --------------------- | ------------------------------ |
| Study area            | AOI area in km²                |
| Acquisitions          | 3 available dates              |
| Spatial resolution    | 10 m reported spacing          |
| Common-valid coverage | Actual AOI-specific percentage |

The common-valid coverage must be calculated from the real AOI mask, not copied from the full granule.

Main visualization

- Large study-area map.
- AOI boundary.
- Available geographic reference locations.
- Optional latest backscatter preview.

Temporal overview

- Acquisition timeline.
- HH and HV availability.
- Processing status.

Scientific summary

- A short explanation of what the analysis measures.
- A warning that backscatter changes are not direct proof of mangrove loss or gain.

### Important interaction

Clicking a summary card should navigate to the corresponding detailed section.

For example, clicking the acquisition count should open the acquisition timeline.

## 6.5 Page 2 — Explore Map

Most important frontend page

[TerraCroma | Platform Capabilities](https://images.openai.com/static-rsc-4/X0fp2DJpiudrhc-9_lVIneLPIkzhzcrDQr6_NDOWePyhX0qhYrVEkfW8n471q2IsLaRzRbTFMoSrJqpJ-v9ABHsUL23DyulHPpo0O8-YDolOM0Xn8_9r8RCNl1k353HJv79CB4uFJGks1fOxqgJISCshDBPFsThOlpe_F78ZZh4?purpose=inline)

[terracroma.ai](https://terracroma.ai/?utm_source=chatgpt.com)

This is the primary application workspace.

### Recommended layout

MAP EXPLORER

NISAR · EPSG:32725 source

LAYERS

☑ HH Backscatter

☐ HV Backscatter

☐ Change Map

☐ Cluster Map

DATE

Cycle 033

INTERACTIVE RASTER MAP

Backscatter · AOI · Change overlays

Map workspace

INSPECTOR

Layer details

Pixel values

Coordinates

Legend

ACQUISITION TIMELINE

22 Aug 2026

09 Oct 2026

21 Oct 2026

This is a layout specification, not a substitute for the real map implementation.

### Left panel — Layer controls

Organize layers into groups.

Backscatter

- HH — Cycle 028
- HH — Cycle 032
- HH — Cycle 033
- HV — Cycle 028
- HV — Cycle 032
- HV — Cycle 033

Temporal differences

- HH: Cycle 028 → 032
- HH: Cycle 032 → 033
- HH: Cycle 028 → 033
- HV: Cycle 028 → 032
- HV: Cycle 032 → 033
- HV: Cycle 028 → 033

Analysis

- Statistical change map
- ML cluster map
- Common-valid coverage mask

Only show layers that actually exist.

### Center — Map

Required capabilities:

- Zoom in and out.
- Pan.
- AOI boundary overlay.
- Layer switching.
- Opacity adjustment.
- Legend.
- Geographic coordinate display.
- Reset to AOI extent.

Optional:

- Pixel inspection.
- Layer comparison using swipe.
- Measurement tools.

### Right panel — Inspector

When a user selects a layer, show:

- Layer name.
- Acquisition date.
- Cycle number.
- Polarization.
- Unit.
- CRS.
- Resolution.
- Valid-pixel coverage.
- Data source and processing status.

If pixel inspection is implemented, display HH/HV values at the selected location, along with coordinates and validity status.

Do not interpolate or fabricate pixel values when the backend cannot provide them.

## 6.6 Page 3 — Temporal Analysis

[Explore Pixxel - Aurora, Our Earth Observation Studio’s impact across industries | Pixxel](https://images.openai.com/static-rsc-4/xFgKHZT8fPNV3NTaGedWv76sRPOyu3_wSiC8I7EDLrovIk55Qdg6BYbtBTqSbDPzZ4-3E9MdsRMmNiX5kilbRih9V36hSAG0ocbIH9X11YkYCWhjRbFrn-vW0mzRFuIlWxpst1rZ1l4QSGUPVmt4X5IzwBOAdQVfPgtqAjVFh5k?purpose=inline)

[pixxel.space](https://www.pixxel.space/knowledge-hub/explore-aurora-pixxels-earth-observation-studios-impact-across-industries?utm_source=chatgpt.com)

This page explains how radar backscatter changes between the three observations.

The key feature is a comparison workspace where users can select two acquisition dates and a polarization.

### Comparison controls

Provide three controls:

- First acquisition: Cycle 028, 032, or 033.
- Second acquisition: Cycle 028, 032, or 033.
- Polarization: HH or HV.

The same acquisition must not be selected twice.

### Main visualization components

A. Before-and-after map comparison

Display two maps side by side or use a swipe slider.

Example:

[BHOONIDHI | NISAR Release](https://images.openai.com/static-rsc-4/qSfb6RliSgXPDKsyauxZRBgxUfqIXhwyyOlyTReHZWVrEr25HnHSo9tcwf5Ll0WImCWANo2L7WM3ciIi9zsmMktXxYoxqvf_EIoYLyeFu6WrQeaak75SdhZJ7DeM5ctVBGxLd6o8HaR2dWmpHTPrS7gklQTXbqQ_UpSRKaEoa-o?purpose=inline)

Earlier observation

Cycle 028 · 22 August

[Mangrove Radar script | Sentinel Hub custom scripts](https://images.openai.com/static-rsc-4/F-6oMV_DQhYpOqw8E8UXKfo8n3ldHCvC3QzUAsMTcyLnobNbnPnHlvucL1nRYlJVVaTReYBqce25HCs28XB1_rct-EPM02PODUZx7Cr6nrBm6vHSdH7WDt2CkxPFrWDAz-6Eo4op6FRI3Nw0YQTof_na826XuoxIvKREe6RVsoI?purpose=inline)

Later observation

Cycle 033 · 21 October

These are illustrative visual references, not your actual NISAR observations. The application must display the generated project rasters.

B. Difference map

For each polarization:

\\[ \Delta \sigma^0\_{\mathrm{dB}} = \sigma^0\_{\mathrm{later,dB}} - \sigma^0\_{\mathrm{earlier,dB}} \\]

Interpretation:

- Positive difference: increased backscatter.
- Negative difference: decreased backscatter.
- Near-zero difference: relatively stable backscatter.

Use a diverging color scale centered at zero.

The legend should show the actual data range or selected display range. Do not choose a visually attractive range that hides extreme values or distorts the interpretation.

C. Temporal line chart

Display the mean and median backscatter for each acquisition.

Example structure:

| Acquisition | HH mean      | HV mean      |
| ----------- | ------------ | ------------ |
| Cycle 028   | Actual value | Actual value |
| Cycle 032   | Actual value | Actual value |
| Cycle 033   | Actual value | Actual value |

Use actual values calculated from valid pixels. Include the number of pixels contributing to each statistic.

D. Distribution chart

A histogram or box plot should show the distribution of backscatter values for the selected dates.

This is useful because a mean can hide spatially different responses.

For example, two dates might have nearly identical average backscatter even though some locations increased and others decreased.

### Scientific interpretation panel

For every comparison, display:

- Comparison dates.
- Polarization.
- Mean difference.
- Median difference.
- Standard deviation.
- Valid-pixel count.
- Percentage of common-valid coverage.
- Interpretation caveat.

The application should distinguish statistical observations from ecological explanations.

## 6.7 Page 4 — ML Insights

[TerraCroma | Platform Capabilities](https://images.openai.com/static-rsc-4/GY6A-k7PJQErBWZVtHPg8JC3UhEJCtDDQlwta9QtY9zZQ75Tanw-YtacfAeHLG-4Ddii3FI_9XzKhba9yiEaEaje0Evnzi75TTdr9RCXhdXHmsD0mIA0Eif1qiNPQaX-ANE2rdjXqUT_W2docS1jXmgzZ0XF3k9tpdEzZAtzFnU?purpose=inline)

[terracolor.ai](https://terracolor.ai/?utm_source=chatgpt.com)

This page presents the outputs of the separate ML engine.

It should not pretend that the application has a trained ecological classification model.

### A. Cluster map

Display the MiniBatch K-Means cluster output.

Each cluster should have:

- Cluster ID.
- Pixel count.
- Area in km².
- Percentage of valid AOI pixels.
- Centroid feature summary.
- Neutral interpretation based on the actual centroid behavior.

Example:

| Cluster   | Area          | Radar behavior          |
| --------- | ------------- | ----------------------- |
| Cluster 0 | Actual result | Relatively stable HH/HV |
| Cluster 1 | Actual result | Higher HH response      |
| Cluster 2 | Actual result | Lower HV response       |
| Cluster 3 | Actual result | Mixed temporal response |

The descriptions must be derived from the trained model's centroids, not hardcoded assumptions.

### B. Statistical change categories

Display the statistical change map independently from the ML cluster map.

Suggested categories:

1. Stable radar response.
2. Increased backscatter.
3. Decreased backscatter.
4. Complex temporal response.
5. Insufficient data.

Keep these categories separate from the K-Means cluster IDs.

Why? A cluster is a group discovered by an algorithm. A statistical category is a rule-based interpretation of measured differences. They are not interchangeable.

### C. Model information

Display a compact model information panel:

| Field           | Value                |
| --------------- | -------------------- |
| Algorithm       | MiniBatch K-Means    |
| Feature count   | 12 primary features  |
| Scaler          | RobustScaler         |
| Cluster count   | Actual trained model |
| Random seed     | Actual configuration |
| Training sample | Actual sample count  |
| Model status    | Loaded / unavailable |

### D. Model limitations

Include a visible methodology note:

> The unsupervised model identifies groups of similar temporal radar responses. These groups are not independently validated ecological classes. Cluster membership does not establish mangrove loss, gain, degradation, or recovery.

Also display a warning if the model was trained on a subset of the AOI or if input features were missing.

### E. Optional ML interaction

If time permits, allow users to:

- Toggle cluster layers.
- Select a cluster.
- Inspect its centroid summary.
- Highlight its spatial distribution.
- Compare its distribution with the statistical change categories.

Do not add an interactive model-training interface. Model fitting belongs to the offline processing workflow.

## 6.8 Page 5 — Reports and Scientific Methodology

[Dashboard UI - Dark and Light Modes :: Behance](https://images.openai.com/static-rsc-4/W3CXHWBd8Hlj0DVlHcCgntmcrJxizNxGdRm_l4XAOZ9kc5dToUZt5GP84Gvsr6dUATYDiBE1WLCS_7380w_xp8kLUjK5TQq1IY8P5KfZHSIL5dwsUTmZGA-4P-PSb2-GQiX8OkHUV-Dt5CaiER4AV9K8yx_EknruFgpL-CWUzmo?purpose=inline)

[behance.net](https://www.behance.net/gallery/114154045/Dashboard-UI-Dark-and-Light-Modes?utm_source=chatgpt.com)

The reports page is important because NASA Space Apps is not simply a UI competition. The team must explain what was measured, how the data was processed, and what conclusions can reasonably be drawn.

### Report sections

1\. Project overview

- Research question.
- Study area.
- NISAR data source.
- Observation dates.
- Objectives.

2\. Dataset report

- Product name and version.
- Granule identifiers.
- Acquisition cycles.
- Polarizations.
- CRS.
- Resolution.
- AOI dimensions.
- Common-valid coverage.

3\. Processing report

- Extraction procedure.
- Calibration units.
- Conversion to dB.
- Mask handling.
- Temporal differencing.
- Feature engineering.

4\. ML report

- Algorithm.
- Input features.
- Sampling strategy.
- Model configuration.
- Cluster distribution.
- Validation checks.
- Limitations.

5\. Results and limitations

- Observed radar changes.
- Spatial distribution.
- Temporal patterns.
- Data-quality limitations.
- Ecological interpretation constraints.

### Export functionality

MVP

Implement:

- Download dataset preparation report.
- Download validation report.
- Download ML metadata.
- Download statistics as CSV.
- Download processed GeoTIFF layers when available.

PDF report generation is optional. Do not spend valuable time building a sophisticated report editor.

## 6.9 Global application components

These components should be reusable across pages.

| Component             | Function                            |
| --------------------- | ----------------------------------- |
| `AppSidebar`          | Navigation                          |
| `AppHeader`           | Project title and system status     |
| `MetricCard`          | Summary statistics                  |
| `AcquisitionTimeline` | Three-date navigation               |
| `LayerSelector`       | Layer visibility and selection      |
| `RasterMap`           | Main geospatial visualization       |
| `MapLegend`           | Color interpretation                |
| `LayerInspector`      | Metadata and pixel information      |
| `ComparisonPanel`     | Before-and-after controls           |
| `TemporalChart`       | Time-series visualization           |
| `ChangeSummary`       | Change statistics                   |
| `ClusterSummary`      | ML cluster information              |
| `ReportViewer`        | Scientific reports                  |
| `DataStatus`          | Dataset and processing availability |

Use shared components to avoid building different versions of the same control on every page.

## 6.10 Frontend technology recommendations

Antigravity can select the exact framework based on the project scaffold, but the following stack is appropriate:

| Component            | Recommendation          |
| -------------------- | ----------------------- |
| Framework            | React                   |
| Language             | TypeScript              |
| Build tool           | Vite                    |
| Styling              | Tailwind CSS            |
| UI components        | shadcn/ui or equivalent |
| Map                  | MapLibre GL JS          |
| Raster visualization | Raster tile overlays    |
| Charts               | Recharts                |
| API communication    | Fetch or Axios          |
| State management     | React state initially   |

### Why MapLibre?

MapLibre is suitable for interactive maps and can display raster tile layers, vector overlays, and geographic boundaries.

The application should use the actual raster outputs prepared by the backend. Do not substitute a generic satellite basemap for the NISAR analysis layer.

A basemap can provide geographic context, but the NISAR raster must remain the primary scientific layer.

### Offline requirement

The application must be runnable locally.

However, there is an important distinction:

- Offline application: The application and prepared scientific datasets run without an internet connection.
- Offline basemap: Geographic background tiles are also available without internet.

If MapLibre uses an online basemap, the application is not completely offline.

For the submission demo, either bundle a small local basemap, use a local geographic background, or make the NISAR raster itself the main map surface.

Do not make the core application dependent on a paid mapping service.

## 6.11 Frontend state and data flow

Keep the application state simple.

The frontend should maintain:

```
selectedPage
selectedLayer
selectedCycle
selectedPolarization
comparisonStart
comparisonEnd
mapOpacity
selectedCluster
selectedCoordinates
```

The frontend should not calculate scientific change statistics itself.

Its role is to:

1. Request data from the backend.
2. Render the response.
3. Update the selected layer and comparison.
4. Display loading, unavailable, and error states.
5. Preserve the user's current map and analysis selections where appropriate.

### Example interaction

User selects:

```
Layer: HH difference
Comparison: Cycle 028 → Cycle 033
```

The frontend requests the corresponding registered layer from the backend, retrieves its metadata and raster visualization, and updates the map and legend.

It should not independently read HDF5 files or recreate the scientific calculation in JavaScript.

## 6.12 Loading, empty, and error states

Every major page needs three conditions.

Loading state

- Show a small progress indicator.
- Explain what is loading.
- Avoid a blank screen.

Unavailable state

Example:

> ML results are not available yet. The radar observations and statistical analysis remain accessible.

Error state

Example:

> The selected raster could not be loaded. Check the backend connection or select another available layer.

Do not show fake charts or invented statistics when an endpoint fails.

This is especially important for a live judging demonstration.

## 6.13 Frontend implementation assignment for Antigravity

# ANTIGRAVITY DEVELOPMENT TASK — FRONTEND

## Project

Dancing with SARs — NASA Space Apps 2026

## Primary objective

Build a professional, scientific web application for exploring multi-temporal NISAR L2 GCOV observations and visualizing radar backscatter changes around the Potengi Estuary, Natal, Brazil.

The map and scientific data must be the central focus of the application.

## 1. Technology

Preferred stack:

- React
- TypeScript
- Vite
- Tailwind CSS
- MapLibre GL JS
- Recharts
- Fetch or Axios

Reuse the existing project framework if one is already established and functional.

## 2. Design

Create a polished dark scientific Earth-observation interface.

Use:

- Deep navy or charcoal background
- Cyan/blue accents
- Teal secondary accents
- Consistent radar-change legends
- Readable scientific typography
- Responsive layouts
- Clear loading, error, and unavailable states

Avoid excessive animations, decorative gradients, and generic dashboard styling.

## 3. Navigation

Implement:

1. Overview
2. Explore Map
3. Temporal Analysis
4. ML Insights
5. Reports
6. About the Project
7. Data & System Status

Use a consistent sidebar and header.

## 4. Overview

Display:

- Project title and study area
- NISAR dataset information
- Three acquisition dates
- Actual AOI area
- Actual common-valid coverage
- Processing status
- Main raster preview
- Short scientific explanation

All measurements must come from backend data.

## 5. Explore Map

This is the highest-priority page.

Implement:

- Interactive map
- AOI boundary
- HH/HV layer selection
- Acquisition selection
- Temporal difference layers
- Statistical change layer
- ML cluster layer
- Map legend
- Opacity control
- Zoom and pan
- Reset extent
- Layer metadata inspector

Use backend raster previews or tiles.

Correctly handle the source CRS EPSG:32725 and the map's display CRS.

Never fabricate raster layers or display unrelated imagery as NISAR observations.

## 6. Temporal Analysis

Implement:

- Two acquisition selectors
- HH/HV polarization selector
- Before-and-after raster comparison
- Difference map
- Diverging legend centered at zero
- Temporal line chart
- Backscatter distribution visualization
- Valid-pixel count
- Common-valid coverage
- Statistical summary

Use backend-computed values.

## 7. ML Insights

Display:

- K-Means cluster map
- Cluster distribution
- Cluster area
- Centroid summaries
- Statistical change categories
- Model configuration
- Model metadata
- Validation information
- Limitations and uncertainty

Do not confuse ML clusters with statistical change classes.

Do not describe radar changes as confirmed mangrove loss or gain.

If ML artifacts are missing, clearly explain that ML results are unavailable while keeping the rest of the application functional.

## 8. Reports

Provide:

- Dataset preparation report
- Processing report
- Validation report
- ML report
- Statistics CSV export
- GeoTIFF download when available

Do not invent report contents.

## 9. API integration

Use the backend API contract:

GET /api/health\
GET /api/project\
GET /api/project/aoi\
GET /api/acquisitions\
GET /api/layers\
GET /api/layers/{layer_id}/metadata\
GET /api/layers/{layer_id}/preview\
GET /api/layers/{layer_id}/tiles/{z}/{x}/{y}.png\
GET /api/layers/{layer_id}/statistics\
GET /api/statistics/overview\
GET /api/statistics/temporal\
GET /api/statistics/area\
GET /api/statistics/clusters\
GET /api/ml/status\
GET /api/ml/metadata\
GET /api/ml/clusters\
GET /api/ml/change\
GET /api/ml/layers\
GET /api/reports

Adapt to the actual endpoints implemented by the backend, but keep a documented integration contract.

## 10. Data integrity

The application uses three NISAR acquisitions:

- Cycle 028 — 2026-08-22
- Cycle 032 — 2026-10-09
- Cycle 033 — 2026-10-21

Polarizations:

- HH
- HV

Reported source CRS: EPSG:32725.\
Reported pixel spacing: 10 m.

These are project-provided metadata and must be checked against actual files.

The study area is Potengi Estuary, Natal, Brazil. Do not use the previously rejected Rio Preguiças Estuary AOI or Dhaka.

Do not hardcode unverified statistics, coordinates, area measurements, or ecological classifications.

## 11. Offline demonstration

The application must run locally without paid cloud services.

Provide:

- Local frontend startup instructions
- Backend connection instructions
- Local data loading
- Clear handling of missing internet access
- No mandatory external API keys

If an online basemap is used, provide a fallback that allows the prepared NISAR data to remain explorable without it.

## 12. Performance

- Do not download full-resolution GeoTIFF arrays into the browser.
- Load only visible map tiles where tile support exists.
- Use PNG previews for lightweight visualization.
- Avoid unnecessary re-rendering.
- Use sensible loading states.
- Do not request all raster layers simultaneously.

## 13. Deliverables

Provide:

- Complete frontend source code
- Reusable components
- API integration
- Responsive interface
- Local run instructions
- README
- Functional testing results

## 14. Critical implementation rules

1. Inspect the existing repository before building.
2. Integrate with the real backend and actual scientific outputs.
3. Do not create fake scientific results to fill empty UI sections.
4. Prioritize a working map and temporal comparison over decorative features.
5. Keep the ML engine independent.
6. Preserve scientific units, CRS, dates, masks, and metadata.
7. Ensure the application remains usable when ML results are unavailable.

Build a working scientific application, not just a static UI mockup.

## 6.14 Frontend acceptance criteria

Before considering the frontend complete, verify the following:

- All five main navigation sections work.
- The overview displays real metadata.
- The map loads actual prepared NISAR data.
- HH and HV layers can be selected.
- All three acquisition dates are represented correctly.
- Temporal difference maps load.
- The difference legend is centered at zero.
- Charts use actual backend statistics.
- ML results are displayed only when available.
- ML clusters and statistical categories are clearly distinguished.
- Reports can be accessed.
- Missing data produces meaningful messages.
- The application works locally.
- The core demonstration does not depend on internet access.

## 6.15 What to build first

With three days remaining, use this order:

First — Demonstration-critical

Required

1. Application layout and navigation.
2. Real NISAR raster map.
3. HH/HV selection.
4. Three-date selection.
5. Temporal difference visualization.
6. Basic statistics and legends.

   Second — Scientific depth

   Important
7. ML cluster visualization.
8. Statistical change categories.
9. Temporal charts.
10. Dataset and validation reports.

    Third — Polish

    Optional
11. Pixel inspector.
12. Map swipe comparison.
13. Advanced filters.
14. Measurement tools.
15. PDF export.

My architectural decision: Keep Antigravity responsible for the entire user-facing application, including frontend and backend integration. Claude develops the independent ML code, and OpenCode handles local extraction, validation, execution, and verification. Do not split the application into unnecessary independent services.

