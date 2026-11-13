# PART 7 OF 12 — Scientific Visualization, Change Detection and Interpretation



Scientific methodology

Visualization specification



## 7.1 Objective

This part defines how the application converts prepared NISAR observations into interpretable scientific visualizations.

The central challenge is that a radar backscatter change is an observation, not automatically an environmental change classification.

The application must distinguish:

1. What NISAR actually measured.
2. What mathematical transformations were applied.
3. What changes were detected.
4. What the ML algorithm grouped together.
5. What environmental explanations remain hypotheses.

This distinction is essential for scientific credibility.

The analogy is a medical thermometer: a temperature reading is a measurement; diagnosing the underlying illness requires additional evidence.

## 7.2 Understanding the NISAR measurements

Your project uses the NISAR L2 GCOV product.

The relevant measurement channels are:

- HH: horizontal transmit, horizontal receive.
- HV: horizontal transmit, vertical receive.

These represent different polarization responses of the radar signal.

### What HH and HV can tell us

HH backscatter

Can provide information about surface scattering, including contributions from:

- Surface roughness.
- Water and soil conditions.
- Vegetation structure.
- Geometry and viewing conditions.

HV backscatter

Cross-polarized response can be sensitive to volume scattering and structural complexity, including vegetation-related scattering.

However, neither polarization uniquely identifies mangroves.

Water, soil moisture, surface roughness, vegetation structure, and other factors can influence both channels.

[Synthetic Aperture Radar (SAR) Masterclass: Introduction to SAR](https://images.openai.com/static-rsc-4/1iOZT8Ory52qcuksC7bEZW6XAuDE0aCWul4UBWJCxV8t_37d8Ms49SbDkvlixshAiKgaoq2L5-stMXQ6Rn_kiPBiFKScoK922XZQwXDCoS4T1NZDu6xq6iBJlvPHDXlhdDklhSB2NBQA4_KFFnphqGh4HACSXIGBjTNkKXYQTrM?purpose=inline)

[Spaceborne L-Band Synthetic Aperture Radar Data for Geoscientific Analyses in Coastal Land Applications: A Review](https://images.openai.com/static-rsc-4/J_EFvErQV0GL_4LSROWRi39wr_cVF6PA4WZRj8dpvQjAgUSnzzxkxPVY-ppQN4sJvjy9oe8ouXiF-4icH7Z0n2J7hWP6R11v6fXPhUhLiTSKskhI5MbiDJK04hQkrgL55M9xc9DWB5z1GOcPiD8H-KKgTufIG91ZQZpiNCpEmIM?purpose=inline)

[Introducción a SAR—ArcGIS Pro | Documentación](https://images.openai.com/static-rsc-4/s4Id0YlCyOEptOMvcpsTe8hW21H_82jnxziTr3tJ0CR4CDwRGX2HyEF6mZWBCv9aZDIdAgdsir7M9ua-OU0-krCLb6Zx1PjVQhigydbK1qQdOPlbHKotHZa1xm7if3vVQ31p2YXJo0WjD1V_RhdvYSyHLDZNK5909XvY4V3s80A?purpose=inline)

8

The frontend should provide a short explanation of these differences through tooltips or an information panel.

## 7.3 Backscatter conversion: linear power to decibels

Your reported NISAR GCOV data contains calibrated gamma-zero backscatter in linear power.

For visualization and temporal comparison, convert positive finite values to decibels:

\\[ \sigma^0\_{\mathrm{dB}} = 10\log\_{10}(\sigma^0\_{\mathrm{linear}}) \\]

Example:

| Linear power | Backscatter |
| ------------ | ----------- |
| 0.01         | -20 dB      |
| 0.1          | -10 dB      |
| 1.0          | 0 dB        |
| 2.0          | 3.01 dB     |
| 10.0         | 10 dB       |

The conversion must only be applied to finite positive values.

Zero, negative, NaN, infinity, and invalid-mask pixels must not be converted into meaningful-looking values.

### Visualization rules

- Use dB for the primary backscatter map.
- Preserve the original linear data for reproducibility.
- Record the conversion method in metadata.
- Apply consistent display ranges when comparing dates.
- Do not independently stretch every image if the user is visually comparing absolute backscatter.

Why consistent ranges matter: If three photographs are independently brightened, they may appear equally bright even when their original brightness differs. The same problem occurs with independently stretched radar images.

## 7.4 Temporal observations

The project has three reported acquisitions:

## NISAR observation timeline

1. Cycle 028

   22 August 2026

   First observation · Baseline
2. Cycle 032

   9 October 2026

   Second observation · Intermediate
3. Cycle 033

   21 October 2026

   Third observation · Latest

There are three possible pairwise comparisons:

| Comparison | Purpose                    |
| ---------- | -------------------------- |
| 028 → 032  | Earlier temporal change    |
| 032 → 033  | Short-term temporal change |
| 028 → 033  | Overall observed change    |

The interval between the second and third acquisitions is only 12 days, whereas the first-to-third interval is 60 days.

The application should make these intervals visible.

Do not treat the three observations as equally spaced time-series samples.

## 7.5 Temporal difference calculations

For every polarization, calculate the pairwise difference in dB:

\\[ \Delta HH\_{28,32} = HH\_{32}-HH\_{28} \\]

\\[ \Delta HH\_{32,33} = HH\_{33}-HH\_{32} \\]

\\[ \Delta HH\_{28,33} = HH\_{33}-HH\_{28} \\]

Repeat the calculations for HV.

This produces six difference layers.

### Interpretation

| Difference           | Interpretation              |
| -------------------- | --------------------------- |
| Positive             | Later backscatter increased |
| Negative             | Later backscatter decreased |
| Near zero            | Relatively little change    |
| No valid observation | Cannot evaluate             |

For example:

- Earlier HH = -12 dB.
- Later HH = -9 dB.
- Difference = +3 dB.

This means the later observation has higher HH backscatter.

It does not independently prove that vegetation increased.

### Important mathematical property

The three pairwise differences are not independent:

\\[ \Delta\_{28,33} = \Delta\_{28,32}+\Delta\_{32,33} \\]

This identity should hold wherever all three dates are valid, subject to numerical precision.

OpenCode should verify this as a numerical consistency test.

## 7.6 Common-valid mask

This is one of the most important parts of the entire project.

You have reported the following mask convention:

| Mask value | Meaning                            |
| ---------- | ---------------------------------- |
| 0          | Invalid radar sample               |
| 1–254      | Valid subswath identifier          |
| 255        | Fill or outside acquisition extent |

Additionally, HH and HV must be finite and positive.

### Three-date validity

Define:

\\[ M\_{\mathrm{common}} = M\_{28}\land M\_{32}\land M\_{33} \\]

where each date's validity also requires finite, positive HH and HV values for the selected comparison.

For a complete HH/HV feature vector, require all six measurements to be valid.

For individual HH-only or HV-only comparisons, validity may be polarization-specific, but the application must report the corresponding valid-pixel count.

Conceptual common-valid coverage

Date 028

Valid

Date 032

Valid

Date 033

Valid

Common-valid pixel

If any required observation is invalid, the corresponding multi-date comparison pixel must be excluded.

### Required visualizations

Create:

1. Three-date common-valid mask.
2. Per-date valid coverage.
3. HH-specific common-valid coverage.
4. HV-specific common-valid coverage.
5. Six-feature or twelve-feature complete-vector coverage, as applicable.

Do not report the full-granule common-valid percentage as the AOI percentage.

## 7.7 Change detection categories

The application needs a categorical map to make difference layers easier to interpret.

Start with a transparent, configurable threshold-based approach.

For example:

\\[ C(x)= \begin{cases} 1 & \Delta(x)>\tau\\\ 2 & \Delta(x)<-\tau\\\ 0 & |\Delta(x)|\leq\tau\\\ 255 & \text{invalid} \end{cases} \\]

Where:

- 0 = Stable.
- 1 = Increased backscatter.
- 2 = Decreased backscatter.
- 255 = NoData.
- \\(\tau\\) = selected change threshold.

### Threshold selection

Do not assume a universal threshold without testing.

Use a starting threshold for exploratory visualization, then inspect the distribution of differences.

For example, test several candidate thresholds:

- 1 dB.
- 1.5 dB.
- 2 dB.

These are sensitivity-analysis candidates, not scientifically validated detection limits.

The project report must document the chosen threshold and explain that it is a heuristic.

### Recommended visual encoding

## Radar-change legend

Stable

Difference within threshold

Increased

Positive difference beyond threshold

Decreased

Negative difference beyond threshold

Complex

Conflicting temporal behavior

Insufficient data

Invalid or missing observation

The complex category can be introduced only if a documented rule defines it. For example, a pixel that increases in one interval and decreases in the next may be categorized as a mixed temporal response.

Do not add this category merely to make the map more colorful.

## 7.8 HH/HV combined analysis

HH and HV provide complementary information. Combining them can help identify different radar-response patterns, but their relationship must be interpreted carefully.

### A. HH/HV ratio

A useful derived feature is the difference between HH and HV in dB:

\\[ R\_{\mathrm{HH/HV}} = HH\_{\mathrm{dB}}-HV\_{\mathrm{dB}} \\]

This is equivalent to the logarithm of the linear-power ratio:

\\[ R\_{\mathrm{HH/HV}} = 10\log\_{10}\left(\frac{HH}{HV}\right) \\]

Example:

| Measurement      | Value  |
| ---------------- | ------ |
| HH               | -10 dB |
| HV               | -16 dB |
| HH/HV difference | 6 dB   |

This represents the relative relationship between the two polarization channels.

It can help characterize changes in scattering behavior, but it is not a direct vegetation-density measurement.

### B. Temporal polarization comparison

Calculate:

\\[ \Delta R = R\_{\mathrm{later}}-R\_{\mathrm{earlier}} \\]

This helps identify whether HH and HV are changing at different rates.

Example interpretations:

- HH increases while HV remains relatively stable.
- HV increases more strongly than HH.
- Both channels decrease.
- Both channels increase.

These patterns can be useful for further investigation, but they are not unique environmental signatures.

### C. Frontend presentation

Provide an optional polarization comparison panel:

Polarization comparison

HH difference

# +2.4 dB

Illustrative value

HV difference

# -1.1 dB

Illustrative value

These are demonstration values only. The actual application must populate this panel from calculated data.

A combined chart can display HH and HV differences side by side, with a clear unit label.

## 7.9 Spatial statistics and area calculations

A change map becomes more useful when the application quantifies the spatial extent of each category.

For a 10 m × 10 m pixel:

\\[ A\_{\mathrm{pixel}}=100\text{ m}^2 \\]

\\[ A\_{\mathrm{km}^2}=N\_{\mathrm{pixels}}\times0.0001 \\]

For example, if 10,000 valid pixels belong to a category:

\\[ 10,000\times0.0001=1\text{ km}^2 \\]

### Required statistics

For each change map, calculate:

- Total AOI pixels.
- Valid comparison pixels.
- Invalid or excluded pixels.
- Stable pixels.
- Increased pixels.
- Decreased pixels.
- Complex-response pixels, if implemented.
- Area of each category.
- Percentage of valid pixels in each category.

### Correct percentage denominator

For category \\(i\\):

\\[ P_i = \frac{N_i}{N\_{\mathrm{valid}}}\times100 \\]

Do not divide by the entire AOI pixel count if some pixels are invalid.

The report should show both:

- Coverage percentage of the AOI.
- Percentage of the valid comparison area belonging to each category.

This prevents a misleading result where a small valid area appears to represent the entire study region.

### Important spatial caveat

The reported raster spacing is 10 m, but a 10 m pixel does not guarantee that every mapped feature can be reliably identified at 10 m.

The application should describe this as the raster's nominal spatial sampling or pixel spacing, not claim that all ecological features are resolved at that scale.

## 7.10 Temporal consistency and spatial coherence

A scientifically credible result should be checked in both time and space.

### Temporal consistency

For each pixel, examine the sequence:

\\[ X=[X\_{028},X\_{032},X\_{033}] \\]

Possible response patterns include:

| Pattern       | Description                                  |
| ------------- | -------------------------------------------- |
| Stable        | Little variation across observations         |
| Increasing    | Progressive increase                         |
| Decreasing    | Progressive decrease                         |
| Reversal      | Increase followed by decrease, or vice versa |
| Abrupt change | Large difference between two observations    |

Do not assume that a pixel with an abrupt change has undergone permanent environmental transformation.

### Spatial coherence

Check whether detected changes appear as:

- Isolated pixels.
- Small patches.
- Connected spatial regions.
- Broad geographic patterns.

A cluster of adjacent changed pixels may deserve more investigation than scattered isolated pixels.

However, spatial coherence alone does not prove that a detected change is real. Radar noise, geometric effects, water conditions, and other factors can also produce spatial patterns.

### Optional visualization

Use a small spatial summary panel:

- Largest connected changed region.
- Number of connected regions.
- Median region area.
- Percentage of isolated changed pixels.

Only add these metrics if they can be calculated and validated within the available time.

## 7.11 Quality-control visualizations

These visualizations are particularly useful because they reveal where the analysis may be unreliable.

[Nodata Masks — rasterio 1.4.4 documentation](https://images.openai.com/static-rsc-4/wCSh96axgUyex0LiNqxgv27yptTKKSEjbuJqXE08cxWB_Ea8w6mLvK_Bk4quyTXqUalFpc6rR_9LSUDuhAfykkqVBgvFfWDtFGXCWGppiOfNsla_VdzYkfsjrGsw5b_EKb8NXqRfRblBvGRgITNi9yLWs6QDrlJSoB1UvThAwd8?purpose=inline)

1\. Validity mask

Shows where observations exist and where data is excluded.

[Development of a Semi-Supervised Learning Model for Disaster Object Reconstruction in Partially Cloud-Covered Areas Using Edge Computing on a CanSAT Platform | AeroSat Vision Lab](https://images.openai.com/static-rsc-4/DxhC2Jr3mIIu-z6w5cLNv8kI72fFYbtF5v1lLtONrcMblAMiich0PEo2usEhGQ86ClxqxVS6KcqJ28cE5HGTBlzDcrELf_tNiBxmrUiSrsu_kin3hW57LD0snZzIPrnIQslO1PvH4ACRI5Ec_tRKlgCf-jdCEESZ1QKc6t-bwFI?purpose=inline)

2\. Per-date coverage

Shows whether acquisition footprints and valid coverage differ between dates.

[Raster Data in R - The Basics | NSF NEON | Open Data to Understand our Ecosystems](https://images.openai.com/static-rsc-4/9wImyWwQh1MJTF6NXdRMHe9VeeLT4jO5gZx1TG4pHL_9ClwGr_U5eW1GqzLWfZ4GhJrstL-GdWNZkbLNN7W4072K4Hgo6GzZJdQSfe3CDTcY1ptqiKyP-xAV5V-8awLypLEP0MvN50yYc2dJFS1Isbj4fsNaybkpO4iFlbGajVw?purpose=inline)

3\. Backscatter distribution

Reveals unusual values, outliers, and distribution changes.

[Coarse-to-Fine Deep Metric Learning for Remote Sensing Image Retrieval | MDPI](https://images.openai.com/static-rsc-4/sSPRiwYP0nRj1Md3o9xQKgPaKBPF2aNpgwHMagddRC5xir4AjK54UlfbxGWO4LlLd_5uSurAtCzQ-t5_ZfB3tC4h7-nbV8DxSWAsoy5c4D7QXLzYUv9u9wikpw12Zsd7NWpbkv_2JnExWBFsykCi6-oviEqJJDJs-JVncvCi4Qk?purpose=inline)

4\. Difference distribution

Shows whether detected changes are widespread or concentrated in a small number of pixels.

### Minimum quality-control checks

1. All three rasters have matching dimensions and geotransforms.
2. All three rasters use the expected CRS.
3. HH and HV values are finite and positive where treated as valid.
4. The mask convention is applied consistently.
5. The common-valid mask is calculated correctly.
6. Difference calculations use the correct acquisition order.
7. The difference identity across the three dates is satisfied.
8. NoData pixels remain excluded from statistics.
9. Exported raster metadata is preserved.
10. Map legends use the correct units and category definitions.

These checks should be generated by OpenCode and made available in the validation report.

## 7.12 Scientific limitations and interpretation policy

This section should be visible in the application, not hidden exclusively in the technical report.

### What the application can claim

- It visualizes NISAR L2 GCOV backscatter observations.
- It compares HH and HV radar responses across three acquisition dates.
- It identifies pixels with increased or decreased backscatter.
- It groups similar temporal radar-response patterns using unsupervised clustering.
- It quantifies changes within the selected AOI and valid observation area.

### What the application cannot claim from these observations alone

- Confirmed mangrove deforestation.
- Confirmed mangrove growth or restoration.
- Exact biomass change.
- Exact vegetation density.
- Permanent land-cover conversion.
- Ecological damage or recovery.

### Additional environmental factors

Radar backscatter can be affected by:

- Soil moisture.
- Tidal conditions.
- Surface water.
- Vegetation structure.
- Surface roughness.
- Observation geometry.
- Radar acquisition conditions.
- Processing and measurement uncertainty.

If independent environmental reference data is available, it can support more specific interpretations. Without that evidence, use neutral radar-response terminology.

Recommended scientific statement:

> This application identifies and visualizes multi-temporal changes in NISAR radar backscatter over the Potengi Estuary. The detected patterns provide an opportunity to investigate changes in surface and vegetation scattering behavior. They should not be interpreted as confirmed ecological change without independent validation.

## 7.13 Data products required for visualization

OpenCode should prepare the following outputs, where supported by the actual processing pipeline.

| Output                         | Format            | Used by               |
| ------------------------------ | ----------------- | --------------------- |
| HH backscatter, three dates    | GeoTIFF           | Map                   |
| HV backscatter, three dates    | GeoTIFF           | Map                   |
| Six temporal difference layers | GeoTIFF           | Temporal analysis     |
| HH/HV ratio layers             | GeoTIFF, optional | Polarization analysis |
| Common-valid mask              | GeoTIFF           | Quality control       |
| Per-date validity masks        | GeoTIFF           | Quality control       |
| Statistical change categories  | GeoTIFF           | Change map            |
| ML cluster map                 | GeoTIFF           | ML insights           |
| Change statistics              | JSON/CSV          | Dashboard and charts  |
| Cluster statistics             | JSON/CSV          | ML insights           |
| Histograms                     | JSON/CSV          | Distribution charts   |
| Preview images                 | PNG               | Dashboard             |
| Processing metadata            | JSON              | Reports               |

The actual filenames should be registered centrally rather than independently hardcoded in the frontend.

## 7.14 OpenCode scientific validation assignment

# OPENCODE TASK — NISAR SCIENTIFIC VALIDATION AND VISUALIZATION OUTPUTS

## Objective

Validate the prepared three-date NISAR dataset and generate scientifically consistent outputs for the application.

## Observations

- Cycle 028: 2026-08-22
- Cycle 032: 2026-10-09
- Cycle 033: 2026-10-21

Polarizations:

- HH
- HV

Expected source CRS: EPSG:32725\
Reported pixel spacing: 10 m

Study area: Potengi Estuary, Natal, Brazil.

Inspect actual files and metadata before processing. Do not assume that previous reports are correct.

## 1. Input validation

Verify:

- Granule identity
- Acquisition date
- Cycle number
- Dimensions
- CRS
- Geotransform
- Pixel spacing
- HH/HV datasets
- Mask convention
- NoData representation

## 2. AOI validation

Verify the actual AOI coordinates and row/column window against the source geospatial metadata.

Do not reuse the rejected Rio Preguiças AOI.

Calculate:

- AOI dimensions
- AOI area
- Per-date valid pixels
- HH common-valid pixels
- HV common-valid pixels
- Complete feature-vector common-valid pixels

Report exact counts and percentages.

## 3. Backscatter preparation

For valid positive finite values:

dB = 10 \* log10(linear_power)

Preserve original linear data.

Generate:

- HH dB layers for all dates
- HV dB layers for all dates

Preserve CRS, transform, dimensions, resolution, and NoData.

## 4. Temporal differences

Generate all six pairwise differences:

- HH 028–032
- HH 032–033
- HH 028–033
- HV 028–032
- HV 032–033
- HV 028–033

Validate:\
Difference(028,033) = Difference(028,032) + Difference(032,033)

Perform this check on common-valid pixels.

## 5. Derived features

If computationally feasible, generate:

- HH/HV ratio in dB
- Temporal HH statistics
- Temporal HV statistics

Document formulas and validity requirements.

## 6. Change categories

Generate a threshold-based change map using configurable thresholds.

Test sensitivity to candidate thresholds such as 1, 1.5, and 2 dB.

Do not describe these thresholds as validated detection limits.

Keep NoData separate from stable pixels.

## 7. Spatial statistics

Calculate:

- Valid pixels
- Stable pixels
- Increased pixels
- Decreased pixels
- Category areas
- Category percentages
- Mean and median differences
- Standard deviation
- Histograms

Use valid comparison pixels as the percentage denominator.

## 8. Visualization outputs

Generate downsampled PNG previews for:

- HH and HV observations
- Temporal differences
- Common-valid mask
- Change categories

Use consistent display scales for date comparisons.

## 9. Validation report

Produce a detailed Markdown report covering:

- Inputs
- Metadata verification
- AOI verification
- Mask handling
- Conversion
- Difference calculations
- Statistics
- Raster export checks
- Known limitations
- Failed or incomplete tests

## 10. Final output

Save outputs in a documented directory structure.

Create a machine-readable manifest describing:

- File paths
- Acquisition dates
- Cycles
- Polarizations
- Units
- CRS
- Dimensions
- Resolution
- NoData
- Validity rules
- Processing methods

Do not fabricate measurements or results.

Do not overwrite original NISAR source granules.

## 7.15 Part 7 completion criteria

- Linear backscatter is converted correctly to dB.
- HH and HV are treated separately.
- All three acquisition dates are represented.
- Six pairwise difference layers are validated.
- The common-valid mask is correct.
- Invalid pixels are excluded from statistics.
- Change thresholds are documented.
- Area calculations use correct denominators.
- ML clusters remain separate from statistical categories.
- Legends and units are scientifically accurate.
- Scientific limitations are visible.
- Validation reports are generated.

My recommendation: Prioritize the common-valid mask, six difference layers, and statistical summaries. These are more important to the scientific credibility of the project than adding sophisticated visualization effects.

