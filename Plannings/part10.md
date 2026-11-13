# PART 10 OF 12 — NASA SPACE APPS PRESENTATION, JUDGING STRATEGY, AND DEMONSTRATION SCRIPT



Competition preparation

Final demonstration



## 10.1 Objective

The objective of this part is to communicate the project's scientific value clearly and demonstrate that it actually works.

A technically sophisticated application can still perform poorly in a competition if judges cannot quickly understand:

- What problem it addresses.
- Why NISAR data is appropriate.
- What the team built.
- What the results mean.
- What makes the solution useful.

Your presentation should tell one coherent story:

NISAR observations → temporal radar analysis → surface-change patterns → interactive exploration → evidence-based interpretation.

Think of the presentation like a scientific investigation. The audience needs to understand the question, the evidence, the method, and the conclusion.

## 10.2 Project identity and positioning

Working title: Dancing with SARs

Recommended technical subtitle:

An Interactive Multi-Temporal NISAR SAR Visualization and Surface-Change Analysis Platform

The title provides a memorable identity, while the subtitle explains the actual technical contribution.

### Project positioning

The project is an interactive Earth-observation analysis platform that uses multi-temporal NISAR L2 GCOV observations to explore radar backscatter variations across the Potengi Estuary.

It combines:

1. Multi-date HH/HV radar observations.
2. Temporal backscatter comparison.
3. Statistical change detection.
4. Unsupervised machine-learning clustering.
5. Geospatial visualization.
6. Reproducible, locally executable analysis.

### The problem statement

Satellite observations contain valuable information about Earth's changing surface, but interpreting multiple radar acquisitions requires specialized processing and technical knowledge.

Users need a way to compare observations across dates, identify spatially distributed radar-response changes, and inspect the underlying evidence without manually processing large scientific datasets.

### The proposed solution

An interactive application that transforms selected NISAR observations into spatially aligned, comparable radar layers and provides temporal analysis, statistical change detection, and exploratory ML-based clustering.

Important distinction: This is a radar-response analysis platform, not a validated mangrove-deforestation detector.

## 10.3 Explain why NISAR matters

[NASA-ISRO's NISAR Mission Marks Turning Point for Indian SpaceTech | Entrepreneur](https://images.openai.com/static-rsc-4/ahtD-885lI_f7gEYjU-GQTM335nhyE6vwnpb_Q1JH6tqEiUOdxqvwN-lkrQOevSwciVWO7KCbdfDITdubw58nWeCFv0yMn1oyXtlfQdUNe99g7G3RytbAZdNYHk7A3Y9L1mfJyHUfCK9kOwBMTvN050PoxmkGM0Jqp0q_jAfQ_U?purpose=inline)

NISAR

NASA and ISRO's joint Earth-observation mission uses synthetic aperture radar to observe changes in Earth's surface.

Your presentation should explain three relevant concepts.

### A. Radar observation

Unlike optical imagery, SAR uses microwave signals to observe the Earth's surface.

Analogy: An optical satellite is like taking a photograph with a camera. A radar satellite is more like sending out an echo and analyzing how the surroundings reflect it.

### B. Polarization

Your project uses two polarization channels:

- HH
- HV

They provide different radar-response measurements and can help characterize differences in surface scattering.

Do not claim that either channel uniquely identifies mangroves or any other land-cover class.

### C. Multi-temporal analysis

Your project uses three observations:

| Acquisition | Date            |
| ----------- | --------------- |
| Cycle 028   | 22 August 2026  |
| Cycle 032   | 9 October 2026  |
| Cycle 033   | 21 October 2026 |

The comparison intervals are:

- 028 → 032: 48 days.
- 032 → 033: 12 days.
- 028 → 033: 60 days.

The project investigates how the radar response changes between these observations.

## 10.4 The five-minute demonstration

This is the recommended demonstration sequence. It prioritizes real functionality over decorative interface features.

## Live demonstration timeline

1. 0:00–0:40 — Introduce the problem

   Explain why multi-temporal radar observations are useful and why comparing them manually is difficult.
2. 0:40–1:20 — Introduce the dataset

   Show the three NISAR acquisition dates, the Potengi AOI, and HH/HV polarization.
3. 1:20–2:20 — Explore the observations

   Switch between dates and polarizations. Show the actual radar layers and geographic coverage.
4. 2:20–3:20 — Demonstrate temporal analysis

   Select two dates. Display their backscatter difference, common-valid coverage, and statistics.
5. 3:20–4:10 — Demonstrate ML

   Display the cluster map, cluster distribution, and centroid summaries. Explain that these are radar-response groups.
6. 4:10–5:00 — Show scientific evidence

   Open the validation report, explain limitations, and demonstrate that the application runs locally.

### Demonstration rule

Never navigate through features that are not fully functional just to make the application appear more sophisticated.

A working temporal comparison is more valuable than five unfinished dashboard pages.

## 10.5 Presentation slide structure

I recommend eight slides.

[Monitoring Coastal Zone Changes from Space - Eos](https://images.openai.com/static-rsc-4/J48-ajhnW1IRflVjnuWLU641L372jD0AtaA1FVLoTycR2kdG7CP9EArLZuubJx3iLAVzuefJbXC2ybZZLlzTJuvLaPJA6rc4ZpvNInC2omVP-YIVNhZIxCYVFFg3DSfYhNDWiLooeJmDIhxrVPZaVsGrXjrlEuw_Eb2iC4JZgCI?purpose=inline)

Slide 1 — Project introduction

- Dancing with SARs
- Technical subtitle
- Team members
- NASA Space Apps Challenge 2026

[Inside the quiet $30k win for Queensland's first-home buyers  - Mortgage Choice](https://images.openai.com/static-rsc-4/xvXGbUfyAZV78I3JlKNZ9e3kfTv3NunpIMzRIWJqUVvY9uf7Ytu3H7cxq4wk8evkar3c2lCtXSkCSrq88nuLMCOyks2YqtswDxdMELHzDUwXpK4cQpzKv9bYDEzDbNBaIUCNYhY57xxaUfHaEbVwHm8bZEl0AE_aGG05eYehxto?purpose=inline)

Slide 2 — The problem

- Difficulty comparing multi-date radar observations.
- Need for accessible spatial analysis.
- Why coastal wetland environments are relevant.

[NISAR in Orbit (Artist's Concept) - NASA Science](https://images.openai.com/static-rsc-4/PGXqjDsKyjwmh7-nilHu87OcaYfOPNEl-qtmBO4Z3nV-XKlGWUgkGf4NEEZKPZ-1_yoUeHBTP93OUJL0rUdKPh-8SfNXbP8G4qhERnHt_sV2gcK9RipJ_on9AfxlufYSaMwl1miS83fL0DvIjDdHk6mStiiYBgBbONqpBlbUDn4?purpose=inline)

Slide 3 — NISAR data

- NISAR L2 GCOV.
- Three acquisitions.
- HH/HV polarization.
- AOI: Potengi Estuary, Brazil.

[Getting Started with Satellite Data Processing | by Hannah Peterson | GSI Technology | Medium](https://images.openai.com/static-rsc-4/5XAnwwhR7jxgFDvfTKguf1_Q6ld8kPz2bfUZ-Nrjqt4dE7Sq5a0s6zKaNb6aZ1-y8BJHEMje-qHjCFD-kHe0XG7vXpR-u7hY9qF_Dhf-z0PR9PK0uUVxfQjk4kL0d2EoMJZoLHW-rcMbt3T0O4NW8AlW8-CNe60lxEpMtoepk60?purpose=inline)

Slide 4 — Methodology

- Data validation.
- Backscatter conversion.
- Common-valid masking.
- Temporal differences.
- Statistical analysis.

[Coarse-to-Fine Deep Metric Learning for Remote Sensing Image Retrieval | MDPI](https://images.openai.com/static-rsc-4/sSPRiwYP0nRj1Md3o9xQKgPaKBPF2aNpgwHMagddRC5xir4AjK54UlfbxGWO4LlLd_5uSurAtCzQ-t5_ZfB3tC4h7-nbV8DxSWAsoy5c4D7QXLzYUv9u9wikpw12Zsd7NWpbkv_2JnExWBFsykCi6-oviEqJJDJs-JVncvCi4Qk?purpose=inline)

Slide 5 — Machine learning

- Feature engineering.
- MiniBatch K-Means.
- Cluster analysis.
- Unsupervised interpretation.

[Sentinel-1 | Terrascope](https://images.openai.com/static-rsc-4/KDPuCocxzJ1cATPWfv5msQhUsXS5_lRPua3LpqPnbosmQC2vOuILYMLsGJ_d5z36zPSYa7vpxrMWsCtXEpZQQVqOK8w36Ge-aFneOwRC8HYCvElyi8hdWWEiNXxr6b_8BQYpae0u5HGpzvK33TB_6HJdVVz16HFQ0gUQW9PUN-Y?purpose=inline)

Slide 6 — Application demonstration

- Interactive map.
- Temporal comparison.
- Change layers.
- ML insights.

[Imágenes de Satélite - Análisis Geoespacial | Cartomex](https://images.openai.com/static-rsc-4/PwwfRNdyusEVj3rYe9hvF1wb6m2pgw0760HFb269DhVYkLhBIkBRxkG8CTbFFdkMWg7T1EyL1JuqgdL8c7inqdTZvmd_nni-Ztwf9i7gbdMMecTEY4IbyNQ6j-cgJ9nYNJdchfiBObnSEOS5eiUg_Cdh-nUwHe5ToJ39iWY6xu4?purpose=inline)

Slide 7 — Results and limitations

- Verified outputs.
- Quantitative statistics.
- Validation results.
- Scientific limitations.

[Murmuration](https://images.openai.com/static-rsc-4/04nAUSWEcAWLM7scDUGhnLiN7CQkXA7Hf63Hm_glZyugtjnKVGiR79hNuBJA3CS1XOIZM8oYEdzVv3_pPOXMIyIP5pXxMItVypmVbYyk06MBh6XOLY0aKpVo5s-E7ZPcydM_jvE6bPUTvam0hH9hsq3apG2katl95Gjn7RaVP70?purpose=inline)

Slide 8 — Impact and future work

- Accessible SAR analysis.
- Potential research applications.
- More acquisitions and independent validation.

## 10.6 What results should you present?

Do not invent results before processing is complete.

Prepare these figures from actual outputs:

| Result                | Presentation            |
| --------------------- | ----------------------- |
| AOI coverage          | Geographic boundary map |
| HH observations       | Three-date comparison   |
| HV observations       | Three-date comparison   |
| Temporal differences  | Difference maps         |
| Common-valid coverage | Percentage chart        |
| Statistical change    | Category distribution   |
| ML clustering         | Cluster map             |
| Cluster population    | Bar chart               |
| Model behavior        | Centroid comparison     |

### Recommended quantitative results

Prioritize these five:

1. Number of valid pixels in the AOI.
2. Percentage of AOI pixels valid across all three dates.
3. Median and mean HH/HV temporal differences.
4. Percentage of pixels in each statistical change category.
5. Area represented by each radar-response cluster.

Always state the denominator and units.

For example:

> 18.4% of complete-valid AOI pixels fell into the decreased-backscatter category under the selected threshold.

That is a useful statement only if the actual processing produces that result. It does not mean 18.4% of the mangroves were lost.

## 10.7 Likely judges' questions and recommended answers

These questions are particularly important because your project combines remote sensing, scientific analysis, and ML.

Q1. Why did you choose NISAR?

NISAR provides SAR observations that enable surface monitoring independent of ordinary optical-image illumination conditions. We use its multi-temporal observations to examine changes in radar backscatter.

Q2. Why did you choose the Potengi Estuary?

It is a coastal estuarine environment with mangrove and wetland relevance. The selected region also needs to be supported by actual NISAR spatial coverage, which is why we verified the AOI against the available granules.

Q3. Why only three acquisitions?

We selected three available observations with compatible spatial characteristics for a focused demonstration. The current analysis is exploratory; additional observations would improve temporal characterization.

Q4. How do you detect change?

We convert valid positive linear backscatter measurements into dB, align observations on a common grid, calculate pairwise differences, and categorize radar-response changes using explicitly configured thresholds.

Q5. Why use machine learning?

MiniBatch K-Means groups pixels with similar multi-temporal HH/HV radar-response patterns. This helps explore spatially distributed behavior without pretending that we have independently labeled ecological training data.

Q6. How accurate is your model?

We do not claim supervised classification accuracy because we do not have independent ground-truth labels for the clusters. We evaluate input integrity, reproducibility, cluster population, centroid behavior, and spatial patterns.

Q7. Can you detect mangrove deforestation?

Not conclusively with the current three-date dataset and unsupervised approach. We can identify radar-response changes that may warrant further investigation. Confirming deforestation requires independent reference data and additional validation.

Q8. What happens when more NISAR data becomes available?

The processing architecture can incorporate additional compatible acquisitions, expand the temporal series, and support more robust change analysis.

Q9. Does the application require cloud hosting?

No. The demonstration is designed to run locally using prepared datasets and model outputs. This improves reproducibility and avoids making the core application dependent on internet connectivity.

Q10. What is the main contribution of your project?

We bring multi-temporal NISAR radar observations, reproducible scientific processing, statistical change analysis, exploratory clustering, and interactive geospatial visualization into one accessible workflow.

## 10.8 Demonstration fallback strategy

Live demonstrations can fail because of memory limitations, application bugs, or slow processing.

Prepare three levels of demonstration readiness.

Level 1 — Full demonstration

Preferred

Run the local application with all verified raster layers, statistics, and ML artifacts.

Level 2 — Precomputed results

Fallback

Use precomputed GeoTIFFs, JSON statistics, and cluster outputs if ML inference or extraction is slow.

Level 3 — Recorded demonstration

Emergency

Use a short screen recording showing the actual application and real project data.

Keep a backup copy of the final demo data and application on a separate storage device if possible.

Do not rely on an internet connection for your primary presentation.

## 10.9 Ready-to-paste Antigravity presentation preparation assignment

# ANTIGRAVITY — NASA SPACE APPS PRESENTATION READINESS

Prepare the existing Dancing with SARs application for a NASA Space Apps Challenge 2026 technical demonstration.

Do not redesign the application unnecessarily. Focus on making its real scientific functionality understandable and demonstrable.

## Required application presentation features

1. Project overview:
   - Project title and technical subtitle.
   - Research problem.
   - Dataset overview.
   - Study area.
2. Dataset transparency:
   - Three acquisition dates.
   - HH/HV polarization.
   - CRS and spatial resolution.
   - AOI information.
   - Data coverage and quality indicators.
3. Temporal analysis:
   - Before/after comparison.
   - Difference visualization.
   - Common-valid coverage.
   - Statistical summaries.
4. ML insights:
   - Cluster visualization.
   - Cluster population.
   - Centroid summaries.
   - Explicit unsupervised-model limitations.
5. Validation:
   - Dataset validation status.
   - Processing validation status.
   - ML validation status.
   - Known limitations.
6. Offline readiness:
   - Local datasets.
   - Local backend.
   - No mandatory external service.
   - Graceful missing-basemap behavior.

## Demonstration requirements

The primary demonstration must take no more than five minutes.

Prioritize:

1. Opening the application.
2. Showing the Potengi AOI.
3. Switching acquisition dates.
4. Comparing HH/HV.
5. Showing temporal differences.
6. Showing statistical change categories.
7. Showing ML clusters.
8. Opening validation evidence.

## Important restrictions

- Do not fabricate scientific results.
- Do not describe radar-response clusters as ecological classifications.
- Do not claim mangrove loss or growth without independent evidence.
- Do not display fake accuracy scores.
- Do not hide missing or unavailable functionality.
- Do not make external basemaps mandatory.

## Deliverables

Prepare:

- A stable presentation configuration.
- A preloaded demonstration dataset.
- A predictable application startup procedure.
- A five-minute demonstration sequence.
- A backup demonstration mode.
- A list of known limitations.

The final interface must display real project outputs, not mock data.

## 10.10 Three-day presentation preparation priorities

Because the submission deadline is close, do not spend an entire day polishing slides.

| Priority | Task                              | Importance |
| -------- | --------------------------------- | ---------- |
| 1        | Working application demonstration | Critical   |
| 2        | Verified temporal comparison      | Critical   |
| 3        | Actual quantitative results       | Critical   |
| 4        | Scientific limitations            | Critical   |
| 5        | Five-minute presentation script   | High       |
| 6        | Eight-slide presentation          | High       |
| 7        | Visual polish and animations      | Low        |

One important recommendation: Record the full demonstration once the application is stable. This gives you a reliable fallback and exposes confusing navigation before the actual presentation.

## Part 10 recap

You now have:

- Project positioning and problem statement.
- NISAR explanation for a non-specialist audience.
- Five-minute demonstration sequence.
- Eight-slide presentation structure.
- Quantitative result requirements.
- Ten likely judging questions.
- Three-level demo fallback.
- Antigravity presentation-readiness assignment.

