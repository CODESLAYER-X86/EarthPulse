Yes. Let's build the complete technical plan first, in multiple detailed parts. The objective is to give Antigravity, Claude, and OpenCode precise instructions so they can work with minimal back-and-forth.

My recommendation: Do not build the ML model first. We should design the ML model now, but implement it after defining the data pipeline and producing a small, representative dataset.

Why? An ML model is like an engine: before building it, we need to know the fuel, the input connections, and what the engine must power. Otherwise, Claude could generate a model that expects data in a format OpenCode does not produce.

# Complete project plan



Planning phase

Part 1 of 12



Here is the proposed structure. We can expand or adjust it as we go.

| Part | Subject                                | Main outcome                                  |
| ---- | -------------------------------------- | --------------------------------------------- |
| 1    | Product vision and system architecture | Overall blueprint                             |
| 2    | NISAR data architecture                | Data formats and processing pipeline          |
| 3    | ML model architecture                  | Model purpose, algorithms, inputs and outputs |
| 4    | ML implementation specification        | Claude-ready development instructions         |
| 5    | Backend architecture                   | APIs, processing services and data management |
| 6    | Frontend and UI/UX                     | Complete interface and user experience        |
| 7    | Geospatial visualization               | Maps, layers and spatial interaction          |
| 8    | Change detection and analytics         | Temporal analysis and statistics              |
| 9    | System integration                     | Connect all components                        |
| 10   | Testing and validation                 | Technical and scientific testing              |
| 11   | Deployment and reproducibility         | GitHub and offline execution                  |
| 12   | Final delivery and NASA presentation   | Documentation, demonstration and submission   |

The parts will be detailed enough to become implementation specifications, not just descriptions.

# PART 1 — Product vision and system architecture

## 1.1 Project identity

Working project name: Dancing with SARs

Project domain: Earth observation, synthetic aperture radar, environmental monitoring, geospatial analytics, and machine learning.

Primary technology: NASA-ISRO Synthetic Aperture Radar (NISAR).

Primary data product: NISAR L2 GCOV (Geocoded Polarimetric Covariance).

Study area: Potengi Estuary, Natal, Rio Grande do Norte, Brazil (provisional until the final AOI is locked).

Primary objective:

Develop an interactive application that uses multi-temporal NISAR observations and machine learning to identify, visualize, and explain changes in Earth's surface, with a focus on coastal wetlands and mangrove ecosystems.

The application should transform satellite observations into understandable information.

In simple terms:

- Satellite data tells us what the radar observed.
- Change detection tells us what changed between observations.
- Machine learning helps identify and characterize patterns.
- The application presents these results visually and interactively.

## 1.2 What are we actually building?

We are not building just a satellite image viewer.

We are building a multi-temporal Earth observation analysis platform.

It should have five main capabilities:

[NISAR Handbook - NASA Science](https://images.openai.com/static-rsc-4/BnRd_TN9qQcIWQ4XTDUd5GjpQXaXqNmgKtXUVfkmOQX1j-yldwrjfTlH4R8yZyXL2sP_EEChHkF_5QD8t02jOBRA0eyNWfPecSTGWwFQuoklwLka1A0Xsn9U5cY23HnK6iOt7H7HkZ5p0HKm5T6NqOVAdykK-qKoJg9DlB9kF6w?purpose=inline)

1\. Satellite data ingestion

Load and process NISAR observations from different acquisition dates.

[Evaluation of Polarimetric SAR Decomposition for Classifying Wetland Vegetation Types](https://images.openai.com/static-rsc-4/fl3f_PMDTH-NSVrsAA21CGRYElUeEwD5YQ-mTs8e3LLp4-cWnaoCzLO_i6jXudkzmFuGXb98FkJWf-S7459LxZY2pUBh5KZMxroa4groOxPSrV6SHAc66Z74nM36ZInjvbEp0XLETxX1gHK1gq6LAOgKlFOz47z_OwIgj86JTuE?purpose=inline)

2\. SAR visualization

Display HH and HV backscatter, acquisition dates, and spatial information.

[Coarse-to-Fine Deep Metric Learning for Remote Sensing Image Retrieval | MDPI](https://images.openai.com/static-rsc-4/sSPRiwYP0nRj1Md3o9xQKgPaKBPF2aNpgwHMagddRC5xir4AjK54UlfbxGWO4LlLd_5uSurAtCzQ-t5_ZfB3tC4h7-nbV8DxSWAsoy5c4D7QXLzYUv9u9wikpw12Zsd7NWpbkv_2JnExWBFsykCi6-oviEqJJDJs-JVncvCi4Qk?purpose=inline)

3\. Change detection

Compare multiple observations and highlight areas with significant backscatter changes.

[Land Cover Classification with eo-learn: Part 3 | by Matic Lubej | Planet Stories | Medium](https://images.openai.com/static-rsc-4/uHz3FfVIopYLWH-zcqZyjst8BQPPfJ666h4wRROdp-mBU67gN7r3SUsoL9eAIBB2HTzyVQjLoY3nEMgw_fMwGx9w5hLYvW7rfnSOIz3NaksxXxiQ2Jmb-o4HD6W9feCfz0NJIyAw4BV1s9glff7txrlEUoajThmlfmlxyMvarnU?purpose=inline)

4\. Machine learning analysis

Classify relevant spatial patterns and help distinguish different types of surface change.

[EarthEye - Agriculture Dashboard Design by Shakuro on Dribbble](https://images.openai.com/static-rsc-4/bFhxB1xZeDvTG6HIAIF7I6bV99P4tdih8ykm2Hp1_qmyUjARgdJ52UrNq-AxKvia92bjX2CPUE1zbiHwH0lUAFYjiS65BmmBx_2jdSxcLV6_MpuakUO15ZGO-aVcXZKX2RNttMPbA4KvErakABOSIz1vumTaKiNeTPiW-QEfClA?purpose=inline)

5\. Interactive analysis platform

Present maps, comparisons, statistics, model results, and explanations.

## 1.3 Target users

The platform should be understandable to three groups.

| User                   | What they need                                                   |
| ---------------------- | ---------------------------------------------------------------- |
| Researchers            | Backscatter observations, temporal analysis and spatial evidence |
| Environmental analysts | Potential changes in wetlands and mangroves                      |
| General users          | Understandable maps, visual comparisons and explanations         |

This means the interface must support both technical and nontechnical users.

For example, a researcher should be able to inspect HH/HV values, while a general user should be able to select two dates and see where the radar observations differ.

## 1.4 Core user experience

The user should follow a straightforward workflow:

1. Open the application

   The user sees the study area and an overview of available satellite observations.
2. Select an acquisition date

   Choose August 22, October 9, or October 21, 2026.
3. Explore satellite observations

   Switch between HH and HV backscatter layers.
4. Compare dates

   Select two or three acquisitions and inspect temporal differences.
5. Run ML analysis

   Access the model's predictions and spatial classifications.
6. Inspect detected changes

   Explore potential changes on the map and view associated statistics.
7. Export results

   Download maps, analysis results, and supporting data where supported.

## 1.5 System architecture

This is the proposed architecture for the entire project.

DATA SOURCES

NISAR L2 GCOV · Reference datasets · AOI

DATA PROCESSING PIPELINE

Extraction · Masking · Calibration conversion · Normalization · Raster preparation

ANALYSIS ENGINE

Temporal comparison

Backscatter differences

Statistical analysis

ML ENGINE

Feature extraction

Classification

Change characterization

BACKEND / APPLICATION SERVICES

Data access · Analysis orchestration · API · Results management

FRONTEND APPLICATION

Interactive map · Date comparison · ML results · Dashboard · Export

USER

Explore · Compare · Understand · Export

This is a logical architecture, not a commitment to separate servers or microservices. For a three-day project, a modular monolithic application may be faster and more reliable.

## 1.6 Responsibilities of the AI tools

We need clear boundaries so that the tools do not duplicate work.

| Tool        | Assigned responsibility             | Main deliverable                              |
| ----------- | ----------------------------------- | --------------------------------------------- |
| ChatGPT     | Technical architect and coordinator | Detailed specifications and prompts           |
| Antigravity | Main application developer          | Complete working application                  |
| Claude.ai   | ML specialist                       | ML source code, model and instructions        |
| OpenCode    | Local data engineer and verifier    | Extracted data, execution, tests and evidence |

Important: OpenCode is not simply a terminal. It is the local execution and verification agent with access to your actual project files and HDF5 datasets.

### How they communicate

We will establish shared contracts between the tools.

For example:

- Claude must know exactly what data OpenCode will provide.
- OpenCode must know exactly what files Claude's ML code expects.
- Antigravity must know exactly what the ML engine returns.
- The frontend must display the outputs using the agreed format.

No tool should independently invent its own file formats or coordinate conventions.

## 1.7 Project priorities

We should divide features into three levels.

P0 — Essential

- Three-date NISAR data support.
- HH/HV visualization.
- Interactive study-area map.
- Temporal comparison.
- Change-detection visualization.
- ML model integration.
- Data-quality information.
- Working local execution.

P1 — Important

- Detailed change statistics.
- Mangrove/reference-layer comparison.
- ML prediction confidence.
- Before-and-after comparison.
- Exportable analysis results.
- Methodology and dataset information.

P2 — Optional

- Additional study areas.
- Advanced time-series analytics.
- AI-generated natural-language explanations.
- User-defined AOIs.
- Additional satellite data sources.
- Cloud deployment.

We should finish P0 before spending time on P2.

# 1.8 Should we build the ML model first?

My final decision is:

Design it now. Implement it after the data contract and representative extraction are ready.

The sequence should be:

1. Define what the model is supposed to detect.
2. Decide what input features it needs.
3. Define its expected output.
4. OpenCode extracts a small representative dataset.
5. Claude writes the model code using that exact dataset structure.
6. OpenCode runs it locally.
7. Antigravity integrates the model into the application.

We can have Claude prepare the model implementation in parallel with Antigravity's frontend development once the interface contracts are agreed.

One critical scientific point: three NISAR dates alone do not automatically provide ground-truth labels for mangrove loss or gain. We must decide whether the model performs unsupervised change detection, supervised classification with reference labels, or another defensible task. We will make that decision in Part 3.

Part 1 completion criteria

- Project objective established.
- Main application capabilities defined.
- User workflow defined.
- System architecture established.
- AI tool responsibilities separated.
- Feature priorities established.
- ML implementation sequence established.

Next: Part 2 — Complete NISAR data architecture and processing pipeline.

That will specify exactly how OpenCode extracts your three HDF5 acquisitions, which datasets it reads, how it prepares the rasters, what files it produces, and precisely what Claude and Antigravity receive.

When you're ready, type next.
