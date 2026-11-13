# NASA Space Apps Challenge 2026: Video Script & Screenplay Specification
**Project:** Dancing with SARs — NISAR L2 GCOV Temporal Environmental Analysis  
**Repository:** [EarthPulse (GitHub)](https://github.com/CODESLAYER-X86/EarthPulse.git)  
**Study Area:** Potengi Estuary, Natal, Rio Grande do Norte, Brazil  
**Satellite Mission:** NASA-ISRO Synthetic Aperture Radar (NISAR)  

---

## 1. NASA Space Apps Challenge Video Submission Requirements

Based on the official NASA Space Apps Challenge Global Project Submission Guidelines:

| Guideline | Official Requirement | Implementation Strategy for Dancing with SARs |
| :--- | :--- | :--- |
| **Duration Limit** | **Maximum 30 seconds** strictly for the Global Judging Pitch video ("30 Seconds of Glory"). | Script Option 1 is formatted strictly to **29.5 seconds** (approx. 72 spoken words). |
| **Extended Demo** | Highly recommended for YouTube description, project portfolio, or local presentations (up to 2 minutes). | Script Option 2 is formatted for a comprehensive **2-minute** deep-dive walkthrough. |
| **Hosting & Access** | Upload to YouTube, Vimeo, or Google Drive; must be **Public** or **Unlisted** (no password/permission requests required). | Provide link directly in the Space Apps project submission dashboard. |
| **Language & Subtitles** | Spoken in English or native language; **must include English subtitles/captions**. | Full timecoded subtitle cues provided for instant `.srt` export or video editor burn-in. |
| **No Copyright Violations** | Audio/music must be royalty-free or Creative Commons Zero (CC0). | Recommended ambient tracks: NASA audio archive or YouTube Audio Library synthwave/ambient. |

### Global Judging Criteria Alignment
1. **Impact (20%):** Demonstrates real-world monitoring of fragile coastal mangrove ecosystems and flood plains.
2. **Creativity (20%):** Replaces noisy raw pixels with an interactive side-by-side swipe comparator and automated vector Hotspot Tour.
3. **Validity (20%):** Mathematically rigorous: linear-power Enhanced Lee speckle filtering, 5-tier $\sigma$-thresholding, and unsupervised MiniBatch $K$-Means ($k=4$).
4. **Relevance (20%):** Directly tackles the NISAR L2 GCOV challenge prompt using authentic multi-temporal observations (Cycles 028, 032, 033).
5. **Presentation (20%):** Concise storytelling, professional UI, cinematic pacing, and clear scientific communication.

---

## 2. Option 1: Official 30-Second Global Submission Video ("30 Seconds of Glory")

> **Target Length:** 0:00 – 0:29.8  
> **Pacing:** High-tempo, confident, clear, 140–145 words per minute.  
> **Word Count:** 74 words.  
> **Background Music:** Ambient electronic / uplifting cinematic pulse (low volume, ducked under voiceover).

```
TIMELINE (0:00 - 0:30)
|--- 0:00 - 0:06 ---|--- 0:06 - 0:13 ---|--- 0:13 - 0:22 ---|--- 0:22 - 0:28 ---|--- 0:28 - 0:30 ---|
     THE PROBLEM        THE BREAKTHROUGH       INTERACTIVE UI         THE IMPACT          CALL TO ACTION
```

### Second-by-Second Screenplay & Voiceover

| Time | Visual / Screenplay Cue | On-Screen Text / Lower Third | Voiceover (Spoken Audio) |
| :--- | :--- | :--- | :--- |
| **0:00 – 0:06** | **Shot 1:** Quick cut from noisy raw SAR pixels to satellite orbit animation over Natal, Brazil. Zoom into Potengi Estuary. | **DANCING WITH SARS**<br>*NISAR L2 GCOV Temporal Analysis* | *"Radar sees through clouds, but raw SAR data looks like incomprehensible noise."* |
| **0:06 – 0:13** | **Shot 2:** Quick split screen showing linear-power Enhanced Lee filtering cutting speckle noise by 62%, revealing crisp tidal channels. | **62% Speckle Noise Reduction**<br>*Linear Power Enhanced Lee Filter* | *"We transformed raw NISAR covariance data using physics-based speckle filtering and five-tier statistical change detection."* |
| **0:13 – 0:22** | **Shot 3:** Screen capture of the web app: cursor swipes the Dual-Map view, scrubs the Time-Lapse player, and clicks a mangrove vector region. | **Interactive Vector Intelligence**<br>*Dual-Map Swipe • Hotspot Tour* | *"Our platform clusters radar scattering into four ecological biomes and converts pixel shifts into interactive, polygonized change hotspots."* |
| **0:22 – 0:28** | **Shot 4:** Zoom out to show real-time backscatter graphs and the 25 km² Potengi Estuary coastal map glowing with vector insights. | **From Raw Pixels to Planetary Action** | *"Turning invisible microwave pulses into actionable environmental intelligence for our changing coasts."* |
| **0:28 – 0:30** | **Shot 5:** Closing title card with NASA Space Apps Challenge logo and GitHub repository link. | **EarthPulse**<br>*NASA Space Apps Challenge 2026* | *(Musical resolve / logo chord)* |

---

## 3. Option 2: Extended 2-Minute Project Demonstration Video

> **Target Length:** 2:00  
> **Format:** Documentary pitch & software demonstration for local judging and YouTube deep-dive.

### Scene 1: The Challenge & The Problem (0:00 – 0:25)
- **Visuals:** 
  - Cinematic opening: Satellite view of Earth rotating into the coast of Natal, Brazil.
  - Cut to the original viewer showing raw red-and-blue noisy pixels over the Potengi Estuary.
  - Text overlay: *The Challenge: Dancing with SARs*.
- **Voiceover:**  
  *"Synthetic Aperture Radar is one of Earth observation’s most powerful tools—piercing clouds and darkness to measure surface structure. But when NISAR orbits over the Potengi Estuary in Natal, Brazil, users are often met with a wall of noisy, raw pixels. Without scientific calibration, distinguishing tidal shifts from deforestation is nearly impossible."*

### Scene 2: The Science — From Speckle Noise to Calibrated Signal (0:25 – 0:50)
- **Visuals:**
  - Transition into the backend architecture diagram.
  - Side-by-side comparison of raw gamma-zero ($\gamma^0$) vs. Enhanced Lee filtered backscatter.
  - Highlight metric cards: Water ENL increased from 1.6 to 4.3 (62.5% speckle variance reduction); mangrove boundary preservation.
- **Voiceover:**  
  *"To solve this, we built a mathematically rigorous pipeline. Operating strictly in the linear power domain, our adaptive Enhanced Lee filter suppresses Rayleigh fading speckle by over 60 percent while preserving narrow tidal channels. We calibrated three repeat NISAR cycles—August, early October, and late October 2026—establishing a rock-solid, zero-hallucination baseline."*

### Scene 3: The Machine Learning & Vector Extraction Engine (0:50 – 1:20)
- **Visuals:**
  - Fast montage of the ML classification map.
  - Show the 4 unsupervised clusters: Water (20%), Mangroves (30%), Transitional flats (22%), Urban (28%).
  - Highlight the connected-component vectorizer turning $>1,500\text{ m}^2$ change clusters into glowing GeoJSON polygons with bounding boxes.
- **Voiceover:**  
  *"Next, our multi-temporal machine learning engine partitions the radar state space. Using MiniBatch K-Means and RobustScaler across 12 feature bands, the model accurately classifies water bodies, dense mangrove canopies, and urban embankments. 
  Instead of leaving users with a static heatmap, our vector engine isolates statistically significant anomalies above three standard deviations, automatically extracting vector boundaries with exact area and decibel shift metrics."*

### Scene 4: Live Platform Tour (1:20 – 1:45)
- **Visuals:**
  - Screen capture of the web interface at `localhost:8000`.
  - Action 1: Click "Dual-Map View" and drag the comparison slider across August and October.
  - Action 2: Click the "Hotspot Tour" button; camera smoothly flies to "Rio Potengi Main Estuary Channel" and pops up the region telemetry card.
  - Action 3: Hit Play on the "Temporal Time-Lapse" to show backscatter changes flowing dynamically over time.
- **Voiceover:**  
  *"In our interactive web application, researchers and municipal planners can swipe between observation cycles with our Dual-Map view, step through time with automated multi-temporal playback, and navigate our guided Hotspot Tour to inspect critical estuarine ecosystems instantly."*

### Scene 5: Real-World Impact & Vision (1:45 – 2:00)
- **Visuals:**
  - Drone footage / coastal satellite view of Natal coastline blending into the EarthPulse dashboard.
  - Animated summary stats: *100% Open Source • 10m Resolution • Ready for NISAR Global Rollout*.
  - Final splash screen with GitHub link and team credits.
- **Voiceover:**  
  *"As NISAR begins its worldwide mission, our platform turns petabytes of raw radar waves into clear, actionable environmental intelligence. This is Dancing with SARs—making Earth’s pulse visible to everyone."*

---

## 4. Screen Recording Shot List (Recording from `localhost:8000`)

To capture the footage for your video, use **OBS Studio** or your preferred screen recorder at **1920×1080 (60 FPS)**:

| Shot # | Tab / View | Specific Action to Record | Duration |
| :---: | :--- | :--- | :---: |
| **Shot A** | **Observation Tab** | Select **Cycle 028 (Aug 22) HV (dB)**. Zoom smoothly into the river bend of Potengi Estuary. Toggle opacity slider from 0% to 100% to show how the SAR layer matches the underlying basemap. | 4 sec |
| **Shot B** | **Differences Tab** | Select **Full Baseline Comparison (Aug 22 → Oct 21)**. Show the 5-tier colorized divergence (red = decrease, blue = increase). | 3 sec |
| **Shot C** | **Dual Map Swipe** | Click **"Dual Map (Side-by-Side)"** toggle in the top-right toolbar. Drag the vertical divider bar back and forth across the estuary to show the instant before/after view. | 5 sec |
| **Shot D** | **Time-Lapse Player** | Click the **Play button** in the bottom Time-Lapse controller. Watch the scrubber advance from Aug 22 to Oct 09 to Oct 21. | 4 sec |
| **Shot E** | **Hotspot Tour** | Click **"Start Hotspot Tour"**. Let the camera fly to Hotspot 1 (Mangrove Forest / Tidal Flat), then click "Next Hotspot" to jump to the Urban Port area. | 5 sec |
| **Shot F** | **Analysis / ML Tab** | Switch to the **Analysis / ML** tab. Hover over the cluster donut chart and temporal backscatter line graph at the bottom. | 4 sec |

---

## 5. Ready-to-Use Subtitle / Caption File (`.srt` format)

You can copy and save this content as `subtitles.srt` to upload directly to YouTube:

```srt
1
00:00:00,000 --> 00:00:06,000
Radar sees through clouds, but raw SAR data looks like incomprehensible noise.

2
00:00:06,000 --> 00:00:13,000
We transformed raw NISAR covariance data using physics-based speckle filtering and five-tier statistical change detection.

3
00:00:13,000 --> 00:00:22,000
Our platform clusters radar scattering into four ecological biomes and converts pixel shifts into interactive, polygonized change hotspots.

4
00:00:22,000 --> 00:00:28,500
Turning invisible microwave pulses into actionable environmental intelligence for our changing coasts.

5
00:00:28,500 --> 00:00:30,000
EarthPulse — Dancing with SARs.
```

---

## 6. Recommended Production Workflow & Free Tools

1. **Voiceover Recording:**
   - Record with your own microphone, or use high-fidelity AI narration (e.g., ElevenLabs "Adam" or "Rachel", or Clipchamp text-to-speech) with neutral, authoritative pacing.
2. **Video Editing:**
   - **CapCut** (Free, automated auto-captions) or **DaVinci Resolve** (Free, professional grading).
   - Set project resolution to **1920×1080 (16:9)**.
3. **Background Music:**
   - Search the free YouTube Audio Library for *Cinematic Ambient*, *Atmospheric Electronic*, or *Deep Space Synth*.
   - Keep background music at **-20 dB** to keep the voiceover crisp and prominent.
4. **Publishing Checklist:**
   - [ ] Video length is $\le 30.0$ seconds (Option 1) or $\le 2:00$ (Option 2).
   - [ ] Uploaded to YouTube as **Public** or **Unlisted**.
   - [ ] Closed Captions (CC) enabled.
   - [ ] Link added to the NASA Space Apps Project submission page.
