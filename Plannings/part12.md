PART 12 OF 12 — MASTER EXECUTION PLAN, AGENT COORDINATION, AND FINAL SUBMISSION CHECKLIST

Final master plan
 Execution-ready

This is the final operational plan for Dancing with SARs.

The purpose is to bring the entire project together and give each AI agent a clearly defined responsibility, execution order, input, and output.

You have three days. The priority is not to build the most complicated system possible. It is to deliver a scientifically defensible, functional, reproducible application.
12.1 Final system architecture
Your project has three primary development agents and one integrated application.
NASA NISAR L2 GCOV
Three acquisitions · HH/HV · Potengi Estuary


OpenCode
Data engineer
HDF5 extraction, AOI verification, preprocessing, validation, execution.


Claude
ML engineer
Independent Python ML implementation, testing, artifacts, and reports.




Shared data contract

GeoTIFF · JSON · Metadata · Validation reports


Antigravity + Gemini 3.8 Flash
Main application builder
Frontend · Backend · APIs · Map · Temporal analysis · ML integration


Dancing with SARs
Integrated local application

Interactive NISAR surface-change analysis platform


The agents must not independently redesign the same component.
Agent	Owns	Does not own
OpenCode	Scientific data pipeline and verification	Main UI
Claude	ML source code and model validation	Application architecture
Antigravity	Main application and integration	Reprocessing original granules independently

Important: OpenCode can execute Claude's ML code locally. Claude does not need direct access to your machine.

12.2 Freeze the final technical decisions
These decisions should remain stable unless an actual technical blocker requires a change.
Component	Final decision
Application builder	Antigravity
Application model	Gemini 3.8 Flash
Data engineering	OpenCode
ML implementation	Claude
ML execution	OpenCode
Backend	Python + FastAPI
Frontend	React + TypeScript + Vite
Mapping	MapLibre GL
Visualization	Recharts
Geospatial processing	Rasterio + NumPy
ML	Scikit-learn
Clustering	MiniBatch K-Means
Change detection	Statistical HH/HV temporal differences
Main raster format	GeoTIFF
Metadata	JSON
Reports	Markdown + JSON + CSV
Database	Not required
Cloud hosting	Not required
Primary deployment	Local/offline

Do not introduce:
- Kubernetes.
- Microservices.
- Cloud databases.
- Authentication systems.
- User accounts.
- Complex distributed processing.
- Unnecessary deep-learning models.
These do not improve the core scientific demonstration enough to justify their implementation cost.

12.3 The master dependency order
Not every task can start immediately. Some require verified outputs from earlier stages.
Critical development path
1. Verify the actual dataset
   
   OpenCode verifies granules, AOI, dates, CRS, masks, and spatial alignment.
   Foundation
2. Freeze the data contract
   
   Define exact filenames, dimensions, units, NoData conventions, feature ordering, and metadata.
3. Generate scientific outputs
   
   OpenCode generates HH/HV layers, temporal differences, common-valid masks, statistics, and previews.
4. Parallel development
   
   Claude develops ML against the frozen contract. Antigravity builds the application shell, API architecture, map interface, and visualization components.
5. Run and validate ML
   
   OpenCode executes the ML package against real outputs and checks the generated artifacts.
6. Integrate the complete application
   
   Antigravity connects the real GeoTIFFs, statistics, reports, and ML outputs.
7. Independent testing
   
   OpenCode checks scientific calculations, API results, spatial integrity, and reproducibility.
8. Package and demonstrate
   
   Prepare GitHub, offline execution, screenshots, slides, and the recorded demonstration.

Why parallel development matters
You should not make Claude wait until the entire application is built.

Once the feature contract is frozen, Claude can implement the ML engine while Antigravity builds the frontend and backend.

It is similar to building a house: the electrical team and interior team can work simultaneously once the structural layout is fixed.

12.4 Three-day execution schedule
The schedule is based on the remaining three-day deadline. Adjust the hours around your actual availability.
Day 1 — Establish the scientific foundation
Highest priority
Task	Owner	Deliverable
Verify three HDF5 granules	OpenCode	Metadata report
Verify Potengi AOI	OpenCode	AOI validation report
Verify common-valid coverage	OpenCode	Coverage statistics
Freeze feature contract	You + OpenCode	feature_metadata.json
Generate temporal differences	OpenCode	Difference GeoTIFFs
Build application shell	Antigravity	Running frontend/backend scaffold
Implement ML engine	Claude	ML source package

End-of-day acceptance criteria:
- The actual AOI is verified.
- The three acquisition dates are confirmed.
- The primary feature stack is generated or its exact generation process is working.
- Antigravity has a running application scaffold.
- Claude has received the final input contract.
If the AOI verification fails, resolve that before presenting geographic results.
Day 2 — Integration and functionality
Main development day
Task	Owner	Deliverable
Execute ML implementation	OpenCode	Model artifacts
Validate cluster outputs	OpenCode	ML validation report
Integrate raster APIs	Antigravity	Functional backend
Implement MapLibre layers	Antigravity	Real NISAR map
Implement temporal comparison	Antigravity	Working date comparison
Integrate statistical changes	Antigravity	Change visualization
Integrate ML results	Antigravity	Cluster visualization
Implement report access	Antigravity	Reports page

End-of-day acceptance criteria:
- The application displays actual NISAR data.
- Temporal comparison works.
- Statistical change layers work.
- ML results are integrated, or the application clearly shows that ML is unavailable.
- The backend serves real metadata and statistics.
Day 3 — Validation and submission
Freeze development
Task	Owner	Deliverable
Run automated tests	OpenCode	Test results
Verify spatial alignment	OpenCode	Raster validation
Test application interactions	You + Antigravity	QA checklist
Test offline operation	You	Offline demo
Update documentation	Antigravity	README and guides
Capture screenshots	You	Evidence package
Prepare slides	You	Presentation
Record demonstration	You	Backup video
Final GitHub commit	You	Release candidate

End-of-day acceptance criteria:
- No critical scientific errors.
- Application starts locally.
- Primary demonstration works.
- README explains installation.
- Limitations are documented.
- Final repository is published.
Time-allocation recommendation
Do not let the ML component consume the entire project schedule.
Recommended allocation of the remaining development effort.



Application development

ML implementation and integration

Scientific data and validation

Testing and packaging















This is a planning allocation, not a requirement to work continuously for 32 hours.

12.5 Agent coordination protocol
This is one of the most important sections.

All three agents must share the same technical decisions.
A. Single source of truth
Maintain these files:
docs/
├── MASTER_PLAN.md
├── DATA_CONTRACT.md
├── AGENT_RESPONSIBILITIES.md
└── INTEGRATION_STATUS.md

data/
└── project_manifest.json


Their responsibilities:
File	Purpose
MASTER_PLAN.md	Overall project requirements
DATA_CONTRACT.md	Exact data formats and conventions
AGENT_RESPONSIBILITIES.md	Division of work
INTEGRATION_STATUS.md	Current task and blocker status
project_manifest.json	Actual available artifacts

Every agent must read the relevant documents before modifying project files.
B. Communication format
Require every agent to finish its task with this report:
TASK:
What was requested?

STATUS:
PASS / PARTIAL / BLOCKED

FILES CREATED:
Exact paths.

FILES MODIFIED:
Exact paths.

VALIDATION:
What tests were performed?

RESULT:
What actually works?

BLOCKERS:
What remains unresolved?

NEXT ACTION:
What should happen next?


This avoids vague messages such as:
- "Everything is completed."
- "The model is ready."
- "The integration is finished."
An agent must provide evidence.
C. Shared-file ownership
Avoid simultaneous edits to the same files.
File group	Owner
data/raw/ and processing scripts	OpenCode
ml_engine/	Claude
backend/	Antigravity
frontend/	Antigravity
docs/	Antigravity, with verified technical input
project_manifest.json	Updated through coordinated integration

OpenCode may execute and test Claude's code, but should not independently redesign the ML architecture during validation.

12.6 Master prompts for the three agents
These are the final coordination instructions. Use them in addition to the detailed implementation assignments from Parts 2–11.
Prompt A — OpenCode: Data engineering and independent verification
MASTER ASSIGNMENT — OPENCODE
Dancing with SARs: Scientific Data Engineer and QA Agent
You are responsible for scientific data engineering, execution, and independent verification.

The main application is developed by Antigravity. The ML source code is developed by Claude.

You must not take over either responsibility.
Your responsibilities
1. Inspect the actual three NISAR L2 GCOV HDF5 granules.
2. Verify acquisition identity and metadata.
3. Independently verify the Potengi Estuary AOI.
4. Verify coordinate transformations, grid alignment, and raster coverage.
5. Extract the required HH/HV data.
6. Generate valid masks and the common-valid mask.
7. Convert valid positive linear backscatter values into dB.
8. Generate all six pairwise temporal difference layers.
9. Generate the fixed 12-feature ML stack.
10. Generate statistics, previews, and metadata.
11. Validate Claude's ML implementation.
12. Execute ML training and inference locally.
13. Validate the actual generated outputs.
14. Test the integrated application and its scientific outputs.
15. Prepare evidence-based reports.
Non-negotiable rules
- Never invent results.
- Never assume AOI validity without checking actual source coordinates.
- Never silently change the feature ordering.
- Never mix linear and dB units.
- Never include invalid pixels in statistics.
- Never label backscatter decrease as confirmed mangrove loss.
- Never mark an untested task PASS.
- Never overwrite important source files without preserving the original.
Coordination
Read:
- docs/MASTER_PLAN.md
- docs/DATA_CONTRACT.md
- docs/AGENT_RESPONSIBILITIES.md
Update:
- docs/INTEGRATION_STATUS.md
- data/project_manifest.json
- data/reports/
Completion report
Use the shared task-report format.

Prioritize verified scientific outputs over optional improvements.




Prompt B — Claude: Independent ML engineer
MASTER ASSIGNMENT — CLAUDE
Dancing with SARs: Machine Learning Engineer
You are responsible for implementing an independent Python machine-learning engine.

The application is developed by Antigravity. Data preparation and local execution are handled by OpenCode.

You must implement a reproducible ML package that integrates through the agreed data contract.
Core objective
Group pixels with similar multi-temporal NISAR HH/HV radar-response patterns.
Input contract
Use the exact agreed feature order:
1. hh_028_db
2. hh_032_db
3. hh_033_db
4. hv_028_db
5. hv_032_db
6. hv_033_db
7. hh_diff_028_032
8. hh_diff_032_033
9. hh_diff_028_033
10. hv_diff_028_032
11. hv_diff_032_033
12. hv_diff_028_033
Use the common-valid mask.

Do not silently reorder or rename features.
Model requirements
- Implement MiniBatch K-Means.
- Use configurable parameters.
- Use a fixed random seed.
- Implement robust preprocessing.
- Support chunked prediction.
- Separate training and inference.
- Validate missing, infinite, and invalid features.
- Generate cluster statistics.
- Generate centroid summaries.
- Generate a cluster raster aligned with the input.
- Record complete model metadata.
Scientific restrictions
- Do not claim supervised accuracy.
- Do not invent ecological labels.
- Do not interpret clusters as mangrove loss or growth.
- Do not create fake probability scores.
- Do not hardcode semantic meanings into cluster IDs.
Outputs
Generate:
- cluster_map.tif
- cluster_statistics.json
- cluster_centroids.json
- model_metadata.json
- model_validation.json
- trained model artifact
- scaler artifact
- visualization preview
- README.md
Engineering requirements
- Modular Python package.
- CLI execution.
- Logging.
- Automated tests.
- Clear error handling.
- Reproducible training.
- Efficient memory use for a 16 GB RAM workstation.
Integration requirements
Provide OpenCode with exact installation and execution instructions.

Provide Antigravity with exact output filenames, raster metadata, API integration requirements, and artifact availability.

Do not modify the main application.

Finish with a detailed task report and unresolved blockers.




Prompt C — Antigravity: Main application architect and integrator
MASTER ASSIGNMENT — ANTIGRAVITY
Dancing with SARs: Application Architect and Integration Engineer
You are responsible for the entire main application.

Use Gemini 3.8 Flash.

OpenCode owns scientific data preparation and independent verification.

Claude owns ML implementation.

You own the frontend, backend, API design, visualization, application integration, and local execution.
Primary objective
Build a professional, scientifically transparent, interactive multi-temporal NISAR analysis application.
Technology
- React
- TypeScript
- Vite
- Tailwind CSS
- Python FastAPI
- MapLibre GL
- Recharts
- Rasterio-compatible backend raster access
Preserve existing working components when possible.
Main functionality
1. Project overview.
2. Interactive Potengi AOI map.
3. Three-date acquisition selection.
4. HH/HV polarization selection.
5. Temporal comparison.
6. Six pairwise difference layers.
7. Statistical change detection.
8. Common-valid coverage.
9. ML cluster visualization.
10. Cluster statistics.
11. Reports and downloads.
12. Data and system status.
Integration contracts
Read the shared DATA_CONTRACT.md before integrating scientific data.

Use actual outputs from OpenCode.

Use actual outputs from Claude.

Do not generate substitute mock scientific data.
Important behavior
- Show real dataset metadata.
- Show the correct acquisition dates.
- Show units and NoData.
- Handle missing layers gracefully.
- Do not display false ML results.
- Do not claim ecological accuracy.
- Keep the application usable without an online basemap.
- Do not require cloud hosting.
- Do not retrain ML automatically on application launch.
Development priorities
P0: Real NISAR data and working map.

P0: Temporal comparison and difference layers.

P0: Correct scientific metadata and statistics.

P1: ML integration.

P1: Reports and offline execution.

P2: Additional decoration and optional features.
Deliverables
- Complete frontend.
- Complete backend.
- Real raster integration.
- API documentation.
- Startup scripts.
- Validation support.
- README.
- Offline demonstration.
- Final integration report.
Do not spend the remaining deadline implementing unnecessary architecture.

Prioritize a functional and reliable scientific demonstration.





12.7 Final end-to-end acceptance test
Before declaring the project complete, perform this exact sequence.
The final demonstration test
1. Start the application from the documented startup script.
2. Confirm the application loads the real project manifest.
3. Open the Potengi Estuary AOI.
4. Select Cycle 028 and display HH.
5. Select Cycle 032 and display HH.
6. Display the 028→032 HH difference.
7. Repeat for HV.
8. Display the 028→033 temporal comparison.
9. Open common-valid coverage statistics.
10. Display the statistical change categories.
11. Open ML clustering and inspect its statistics.
12. Open the scientific validation report.
13. Download or inspect one generated report.
14. Disconnect the internet and repeat the core demonstration.

If the ML component fails, continue the demonstration using verified statistical outputs. Do not let an optional model failure invalidate the primary application.

12.8 What to cut if the deadline becomes critical
This is your emergency scope-control policy.
Feature	Decision
Actual NISAR visualization	Keep
Temporal comparison	Keep
HH/HV difference layers	Keep
Common-valid mask	Keep
Statistical summaries	Keep
ML clustering	Keep if validated
Cluster centroid charts	Keep if available
Advanced animation	Cut first
User authentication	Cut
Cloud deployment	Cut
Complex 3D visualization	Cut
Deep-learning segmentation	Do not implement
Live model retraining	Do not implement

The core product is the scientific analysis and visualization, not the number of features.

12.9 Submission-day checklist
Final readiness
0%



Scientific correctness
[ ] Correct three NISAR granules
[ ] Correct Potengi AOI
[ ] Correct acquisition dates
[ ] Correct HH/HV measurements
[ ] Correct dB conversion
[ ] Correct temporal differences
[ ] Correct common-valid mask
[ ] Accurate area calculations
[ ] Limitations documented

Application
[ ] Local startup works
[ ] Actual raster layers load
[ ] Temporal comparison works
[ ] Statistics match the source outputs
[ ] ML outputs are genuine or explicitly unavailable
[ ] Offline operation works
[ ] No critical errors

Submission
[ ] GitHub repository public or accessible as required
[ ] README complete
[ ] Installation instructions tested
[ ] Project screenshots captured
[ ] Presentation complete
[ ] Demo recording available
[ ] Final validation report included
[ ] No credentials or private files exposed


12.10 My final technical recommendations
There are five decisions I want you to keep in mind throughout execution.

1. Scientific correctness comes before visual sophistication.

A beautiful map showing incorrectly aligned pixels is worse than a simple map showing the correct observations.

2. Do not make the project dependent on ML.

Your statistical temporal analysis is the primary scientific functionality. ML adds exploratory value, but the application must remain functional without it.

3. Freeze the data contract early.

This prevents Claude and Antigravity from producing incompatible outputs.

4. Make every important claim traceable to an output.

If you say a percentage of the AOI changed, you should be able to identify the raster, threshold, denominator, and calculation behind it.

5. Stop adding features before the deadline.

Reserve the final development period for testing, documentation, and demonstration preparation.

Complete 12-part plan — consolidated
Dancing with SARs — Master project plan
All 12 planning modules
01
Project scope and scientific foundation


02
Data engineering and processing pipeline


03
ML model architecture


04
ML implementation and execution architecture


05
Backend architecture


06
Frontend architecture and user experience


07
Scientific visualization and change interpretation


08
End-to-end integration and data contracts


09
Testing and scientific reliability


10
Presentation and judging strategy


11
GitHub and submission packaging


12
Master execution and agent coordination



What happens now?
The planning phase is complete. The next step should be execution, not another architectural redesign.

I recommend beginning with a single master execution document containing all 12 parts, then giving each agent its own responsibility-specific instructions and the shared data contract.

One critical detail: before allowing the three agents to proceed independently, make sure OpenCode has verified the AOI and generated the actual feature metadata. That is the interface contract on which the rest of the project depends.

I can now consolidate all 12 parts into one comprehensive, structured MASTER_PLAN.md file suitable for Antigravity, Claude, and OpenCode to use as their shared project specification.
