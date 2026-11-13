import os
import io
import json
import csv
from pathlib import Path
from typing import Optional, Dict, Any, List

import numpy as np
import rasterio
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

app = FastAPI(
    title="Dancing with SARs — NISAR Analysis API",
    description="Multi-temporal NISAR L2 GCOV processing and change detection service for Potengi Estuary, Natal, Brazil.",
    version="2.0.0"
)

# Enable CORS for local development frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
FILTERED_DIR = DATA_DIR / "filtered"
TEMPORAL_DIR = DATA_DIR / "temporal"
TEMPORAL_FILTERED_DIR = FILTERED_DIR / "temporal"
CLASSIFIED_DIR = DATA_DIR / "classified"
ML_DIR = DATA_DIR / "ml"
REPORTS_DIR = DATA_DIR / "reports"

# In-memory PNG cache for fast client switching
_png_cache: Dict[str, bytes] = {}

# Canonical Potengi AOI WGS84 Coordinates derived from EPSG:32725 raster grid
POTENGI_BOUNDS_WGS84 = {
    "center": [-35.217996, -5.760797],
    "zoom": 12.5,
    "coordinates": [
        [-35.240560, -5.738110],  # NW (top-left)
        [-35.195432, -5.738285],  # NE (top-right)
        [-35.195432, -5.783483],  # SE (bottom-right)
        [-35.240560, -5.783307]   # SW (bottom-left)
    ],
    "bbox": [-35.240560, -5.783483, -35.195432, -5.738110],  # [min_lon, min_lat, max_lon, max_lat]
    "epsg": "EPSG:32725",
    "area_km2": 25.0,
    "dimensions": [500, 500],
    "resolution_m": 10.0
}

ACQUISITIONS = [
    {"cycle": "028", "date": "2026-08-22", "orbit": "139", "direction": "Descending"},
    {"cycle": "032", "date": "2026-10-09", "orbit": "139", "direction": "Descending"},
    {"cycle": "033", "date": "2026-10-21", "orbit": "139", "direction": "Descending"},
]


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Dancing with SARs Backend",
        "data_ready": (ML_DIR / "feature_metadata.json").exists(),
        "filtered_ready": (TEMPORAL_FILTERED_DIR / "HH_diff_028_033_filtered.tif").exists(),
        "classified_ready": (CLASSIFIED_DIR / "change_regions_HH_028_033.geojson").exists()
    }


@app.get("/api/metadata")
def get_metadata():
    metadata_file = ML_DIR / "feature_metadata.json"
    raw_meta = {}
    if metadata_file.exists():
        with open(metadata_file, "r") as f:
            raw_meta = json.load(f)

    return {
        "study_area": "Potengi Estuary, Natal, Brazil",
        "bounds": POTENGI_BOUNDS_WGS84,
        "acquisitions": ACQUISITIONS,
        "raster_metadata": raw_meta
    }


@app.get("/api/manifest")
def get_manifest():
    manifest_file = DATA_DIR / "project_manifest.json"
    if not manifest_file.exists():
        raise HTTPException(status_code=404, detail="project_manifest.json not found")
    with open(manifest_file, "r") as f:
        return json.load(f)


@app.get("/api/statistics")
def get_statistics():
    metadata_file = ML_DIR / "feature_metadata.json"
    if not metadata_file.exists():
        raise HTTPException(status_code=404, detail="feature_metadata.json not found")
    with open(metadata_file, "r") as f:
        data = json.load(f)
    return data.get("statistics", {})


@app.get("/api/layers")
def list_available_layers():
    layers = [
        # Filtered Backscatter Layers (Default)
        {"id": "cycle_028_hh_filtered_db", "name": "Cycle 028 HH (Filtered dB)", "category": "backscatter", "cycle": "028", "pol": "HH", "date": "2026-08-22", "filtered": True},
        {"id": "cycle_028_hv_filtered_db", "name": "Cycle 028 HV (Filtered dB)", "category": "backscatter", "cycle": "028", "pol": "HV", "date": "2026-08-22", "filtered": True},
        {"id": "cycle_032_hh_filtered_db", "name": "Cycle 032 HH (Filtered dB)", "category": "backscatter", "cycle": "032", "pol": "HH", "date": "2026-10-09", "filtered": True},
        {"id": "cycle_032_hv_filtered_db", "name": "Cycle 032 HV (Filtered dB)", "category": "backscatter", "cycle": "032", "pol": "HV", "date": "2026-10-09", "filtered": True},
        {"id": "cycle_033_hh_filtered_db", "name": "Cycle 033 HH (Filtered dB)", "category": "backscatter", "cycle": "033", "pol": "HH", "date": "2026-10-21", "filtered": True},
        {"id": "cycle_033_hv_filtered_db", "name": "Cycle 033 HV (Filtered dB)", "category": "backscatter", "cycle": "033", "pol": "HV", "date": "2026-10-21", "filtered": True},

        # Raw Backscatter Layers (For Comparative Verification)
        {"id": "cycle_028_hh_db", "name": "Cycle 028 HH (Raw dB)", "category": "backscatter", "cycle": "028", "pol": "HH", "date": "2026-08-22", "filtered": False},
        {"id": "cycle_028_hv_db", "name": "Cycle 028 HV (Raw dB)", "category": "backscatter", "cycle": "028", "pol": "HV", "date": "2026-08-22", "filtered": False},
        {"id": "cycle_032_hh_db", "name": "Cycle 032 HH (Raw dB)", "category": "backscatter", "cycle": "032", "pol": "HH", "date": "2026-10-09", "filtered": False},
        {"id": "cycle_032_hv_db", "name": "Cycle 032 HV (Raw dB)", "category": "backscatter", "cycle": "032", "pol": "HV", "date": "2026-10-09", "filtered": False},
        {"id": "cycle_033_hh_db", "name": "Cycle 033 HH (Raw dB)", "category": "backscatter", "cycle": "033", "pol": "HH", "date": "2026-10-21", "filtered": False},
        {"id": "cycle_033_hv_db", "name": "Cycle 033 HV (Raw dB)", "category": "backscatter", "cycle": "033", "pol": "HV", "date": "2026-10-21", "filtered": False},

        # Filtered Temporal Differences
        {"id": "diff_hh_028_033_filtered", "name": "Δ HH: Aug 22 → Oct 21 (Filtered)", "category": "difference", "pol": "HH", "baseline": "028", "target": "033", "filtered": True},
        {"id": "diff_hv_028_033_filtered", "name": "Δ HV: Aug 22 → Oct 21 (Filtered)", "category": "difference", "pol": "HV", "baseline": "028", "target": "033", "filtered": True},
        {"id": "diff_hh_028_032_filtered", "name": "Δ HH: Aug 22 → Oct 09 (Filtered)", "category": "difference", "pol": "HH", "baseline": "028", "target": "032", "filtered": True},
        {"id": "diff_hv_028_032_filtered", "name": "Δ HV: Aug 22 → Oct 09 (Filtered)", "category": "difference", "pol": "HV", "baseline": "028", "target": "032", "filtered": True},
        {"id": "diff_hh_032_033_filtered", "name": "Δ HH: Oct 09 → Oct 21 (Filtered)", "category": "difference", "pol": "HH", "baseline": "032", "target": "033", "filtered": True},
        {"id": "diff_hv_032_033_filtered", "name": "Δ HV: Oct 09 → Oct 21 (Filtered)", "category": "difference", "pol": "HV", "baseline": "032", "target": "033", "filtered": True},

        # Classified Change Rasters (5-Tier)
        {"id": "cls_hh_028_033", "name": "Classified Change: HH (Aug 22 → Oct 21)", "category": "classified", "pol": "HH", "baseline": "028", "target": "033"},
        {"id": "cls_hv_028_033", "name": "Classified Change: HV (Aug 22 → Oct 21)", "category": "classified", "pol": "HV", "baseline": "028", "target": "033"},

        # Masks
        {"id": "common_valid_mask", "name": "Common Valid Coverage Mask", "category": "mask"},

        # ML Predictions
        {"id": "ml_clusters", "name": "ML Unsupervised Radar Clusters (k=4)", "category": "ml"},
        {"id": "ml_change_hh", "name": "Statistical Change Classes: HH", "category": "ml"},
        {"id": "ml_change_hv", "name": "Statistical Change Classes: HV", "category": "ml"}
    ]
    return layers


def _resolve_layer_path(layer_id: str) -> Optional[Path]:
    mapping = {
        # Filtered
        "cycle_028_hh_filtered_db": FILTERED_DIR / "cycle_028" / "HH_filtered_db.tif",
        "cycle_028_hv_filtered_db": FILTERED_DIR / "cycle_028" / "HV_filtered_db.tif",
        "cycle_032_hh_filtered_db": FILTERED_DIR / "cycle_032" / "HH_filtered_db.tif",
        "cycle_032_hv_filtered_db": FILTERED_DIR / "cycle_032" / "HV_filtered_db.tif",
        "cycle_033_hh_filtered_db": FILTERED_DIR / "cycle_033" / "HH_filtered_db.tif",
        "cycle_033_hv_filtered_db": FILTERED_DIR / "cycle_033" / "HV_filtered_db.tif",

        # Raw
        "cycle_028_hh_db": PROCESSED_DIR / "cycle_028" / "HH_db.tif",
        "cycle_028_hv_db": PROCESSED_DIR / "cycle_028" / "HV_db.tif",
        "cycle_032_hh_db": PROCESSED_DIR / "cycle_032" / "HH_db.tif",
        "cycle_032_hv_db": PROCESSED_DIR / "cycle_032" / "HV_db.tif",
        "cycle_033_hh_db": PROCESSED_DIR / "cycle_033" / "HH_db.tif",
        "cycle_033_hv_db": PROCESSED_DIR / "cycle_033" / "HV_db.tif",

        # Filtered Differences
        "diff_hh_028_033_filtered": TEMPORAL_FILTERED_DIR / "HH_diff_028_033_filtered.tif",
        "diff_hv_028_033_filtered": TEMPORAL_FILTERED_DIR / "HV_diff_028_033_filtered.tif",
        "diff_hh_028_032_filtered": TEMPORAL_FILTERED_DIR / "HH_diff_028_032_filtered.tif",
        "diff_hv_028_032_filtered": TEMPORAL_FILTERED_DIR / "HV_diff_028_032_filtered.tif",
        "diff_hh_032_033_filtered": TEMPORAL_FILTERED_DIR / "HH_diff_032_033_filtered.tif",
        "diff_hv_032_033_filtered": TEMPORAL_FILTERED_DIR / "HV_diff_032_033_filtered.tif",

        # Raw Differences
        "diff_hh_028_033": TEMPORAL_DIR / "HH_diff_028_033.tif",
        "diff_hv_028_033": TEMPORAL_DIR / "HV_diff_028_033.tif",
        "diff_hh_028_032": TEMPORAL_DIR / "HH_diff_028_032.tif",
        "diff_hv_028_032": TEMPORAL_DIR / "HV_diff_028_032.tif",
        "diff_hh_032_033": TEMPORAL_DIR / "HH_diff_032_033.tif",
        "diff_hv_032_033": TEMPORAL_DIR / "HV_diff_032_033.tif",

        # Classified Rasters
        "cls_hh_028_033": CLASSIFIED_DIR / "HH_change_classified_028_033.tif",
        "cls_hv_028_033": CLASSIFIED_DIR / "HV_change_classified_028_033.tif",

        # Masks & ML
        "common_valid_mask": TEMPORAL_DIR / "common_valid_mask.tif",
        "ml_clusters": ML_DIR / "predictions" / "cluster_map.tif",
        "ml_change_hh": ML_DIR / "predictions" / "hh_change_categories.tif",
        "ml_change_hv": ML_DIR / "predictions" / "hv_change_categories.tif",
    }
    return mapping.get(layer_id)


@app.get("/api/raster/{layer_id}.png")
def get_raster_png(layer_id: str, colormap: Optional[str] = None, transparent_stable: bool = True):
    cache_key = f"{layer_id}_{colormap or 'default'}_{transparent_stable}"
    if cache_key in _png_cache:
        return Response(content=_png_cache[cache_key], media_type="image/png")

    file_path = _resolve_layer_path(layer_id)
    if not file_path or not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Layer '{layer_id}' file not found.")

    with rasterio.open(file_path) as src:
        arr = src.read(1)
        nodata = src.nodata if src.nodata is not None else -9999.0

    valid_mask = np.isfinite(arr) & (arr != nodata)
    h, w = arr.shape
    rgba = np.zeros((h, w, 4), dtype=np.uint8)

    if "mask" in layer_id:
        is_valid = (arr == 1)
        rgba[is_valid] = [34, 197, 94, 140]
        rgba[~is_valid] = [0, 0, 0, 0]

    elif "cls_" in layer_id:
        # 5-Tier Classified Change Raster
        # -2: Significant Decrease (Red)
        # -1: Moderate Decrease (Orange)
        #  0: Stable (Transparent)
        #  1: Moderate Increase (Cyan)
        #  2: Significant Increase (Teal/Blue)
        rgba[valid_mask & (arr == -2)] = [239, 68, 68, 220]    # Vibrant Red
        rgba[valid_mask & (arr == -1)] = [249, 115, 22, 190]   # Orange
        rgba[valid_mask & (arr == 0)] = [0, 0, 0, 0]           # Stable -> Completely Transparent!
        rgba[valid_mask & (arr == 1)] = [6, 182, 212, 190]     # Cyan
        rgba[valid_mask & (arr == 2)] = [16, 185, 129, 220]    # Emerald/Teal
        rgba[~valid_mask] = [0, 0, 0, 0]

    elif "ml_clusters" in layer_id:
        palette = [
            [59, 130, 246, 210],   # 0: Blue (Water/Mudflats)
            [16, 185, 129, 210],   # 1: Green (Mangrove Canopy)
            [245, 158, 11, 210],   # 2: Amber (Scrub/Transitional)
            [239, 68, 68, 210]     # 3: Red (Urban/Structures)
        ]
        for c_id, col in enumerate(palette):
            mask_c = valid_mask & (arr == c_id)
            rgba[mask_c] = col
        rgba[~valid_mask] = [0, 0, 0, 0]

    elif "ml_change" in layer_id:
        rgba[valid_mask & (arr == -1)] = [239, 68, 68, 200]
        rgba[valid_mask & (arr == 0)] = [0, 0, 0, 0]  # Stable is transparent
        rgba[valid_mask & (arr == 1)] = [34, 197, 94, 200]
        rgba[~valid_mask] = [0, 0, 0, 0]

    elif "diff" in layer_id:
        # Diverging colormap centered at 0 dB
        cmap_name = colormap or "RdBu_r"
        cmap = plt.get_cmap(cmap_name)
        norm = mcolors.Normalize(vmin=-4.0, vmax=4.0, clip=True)
        colors = cmap(norm(arr))
        rgba_float = colors * 255
        rgba[valid_mask] = rgba_float[valid_mask].astype(np.uint8)

        # Set alpha: If transparent_stable is True, make values within noise floor (|delta| <= 1.25 dB) semi-transparent
        if transparent_stable:
            stable_mask = valid_mask & (np.abs(arr) <= 1.25)
            active_mask = valid_mask & (np.abs(arr) > 1.25)
            rgba[stable_mask, 3] = 40   # 15% opacity for stable noise floor
            rgba[active_mask, 3] = 220  # 86% opacity for real changes
        else:
            rgba[valid_mask, 3] = 200
        rgba[~valid_mask] = [0, 0, 0, 0]

    else:
        # Decibel backscatter (-25 dB to 0 dB)
        cmap_name = colormap or "viridis"
        cmap = plt.get_cmap(cmap_name)
        norm = mcolors.Normalize(vmin=-25.0, vmax=0.0, clip=True)
        colors = cmap(norm(arr))
        rgba_float = colors * 255
        rgba[valid_mask] = rgba_float[valid_mask].astype(np.uint8)
        rgba[valid_mask, 3] = 220
        rgba[~valid_mask] = [0, 0, 0, 0]

    # Save to PNG buffer
    fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.axis("off")
    ax.imshow(rgba)
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png", transparent=True, pad_inches=0)
    plt.close(fig)
    
    png_bytes = buf.getvalue()
    _png_cache[cache_key] = png_bytes
    return Response(content=png_bytes, media_type="image/png")


@app.get("/api/geojson/change-regions/{pol}_{c1}_{c2}")
def get_change_regions(pol: str, c1: str, c2: str):
    """Serve precomputed vector change regions as GeoJSON (WGS84)."""
    p = CLASSIFIED_DIR / f"change_regions_{pol.upper()}_{c1}_{c2}.geojson"
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"GeoJSON not found for {pol}_{c1}_{c2}")
    with open(p, "r") as f:
        return json.load(f)


@app.get("/api/regions/summary")
def get_regions_summary():
    """Returns total change area and count for all pairwise intervals."""
    summary = []
    comparisons = [
        ("HH", "028", "033", "Aug 22 → Oct 21 (60-day)"),
        ("HV", "028", "033", "Aug 22 → Oct 21 (60-day)"),
        ("HH", "028", "032", "Aug 22 → Oct 09 (48-day)"),
        ("HV", "028", "032", "Aug 22 → Oct 09 (48-day)"),
        ("HH", "032", "033", "Oct 09 → Oct 21 (12-day)"),
        ("HV", "032", "033", "Oct 09 → Oct 21 (12-day)")
    ]
    for pol, c1, c2, desc in comparisons:
        p = CLASSIFIED_DIR / f"change_regions_{pol}_{c1}_{c2}.geojson"
        if p.exists():
            with open(p) as f:
                data = json.load(f)
            feats = data.get("features", [])
            total_ha = sum(f["properties"].get("area_ha", 0) for f in feats)
            sig_dec = sum(1 for f in feats if f["properties"].get("category") == "Significant Decrease")
            sig_inc = sum(1 for f in feats if f["properties"].get("category") == "Significant Increase")
            summary.append({
                "pol": pol,
                "interval": desc,
                "pair": f"{c1}_{c2}",
                "total_regions": len(feats),
                "total_area_ha": round(total_ha, 1),
                "significant_decreases": sig_dec,
                "significant_increases": sig_inc
            })
    return summary


@app.get("/api/export/summary.csv")
def export_summary_csv():
    """Exports multi-temporal backscatter and change metrics as downloadable CSV."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Polarization", "Interval", "Pair", "Total_Regions", "Total_Change_Area_ha", "Significant_Decreases", "Significant_Increases"])

    summary = get_regions_summary()
    for row in summary:
        writer.writerow([row["pol"], row["interval"], row["pair"], row["total_regions"], row["total_area_ha"], row["significant_decreases"], row["significant_increases"]])

    csv_data = output.getvalue()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=dancing_with_sars_change_summary.csv"}
    )


@app.get("/api/ml/status")
def get_ml_status():
    cluster_tif = ML_DIR / "predictions" / "cluster_map.tif"
    model_meta = ML_DIR / "metadata" / "model_metadata.json"
    stats_file = ML_DIR / "statistics" / "cluster_statistics.json"

    available = cluster_tif.exists() and model_meta.exists()
    return {
        "available": available,
        "files_ready": {
            "cluster_map": cluster_tif.exists(),
            "model_metadata": model_meta.exists(),
            "cluster_statistics": stats_file.exists()
        }
    }


@app.get("/api/ml/summary")
def get_ml_summary():
    stats_file = ML_DIR / "statistics" / "cluster_statistics.json"
    centroids_file = ML_DIR / "statistics" / "cluster_centroids.json"
    meta_file = ML_DIR / "metadata" / "model_metadata.json"

    result = {}
    if stats_file.exists():
        with open(stats_file, "r") as f:
            result["statistics"] = json.load(f)
    if centroids_file.exists():
        with open(centroids_file, "r") as f:
            result["centroids"] = json.load(f)
    if meta_file.exists():
        with open(meta_file, "r") as f:
            result["metadata"] = json.load(f)

    if not result:
        raise HTTPException(status_code=404, detail="ML results have not been generated yet.")
    return result


@app.get("/api/reports")
def list_reports():
    reports = []
    if REPORTS_DIR.exists():
        for p in sorted(REPORTS_DIR.glob("*.md")):
            reports.append({
                "id": p.stem,
                "filename": p.name,
                "title": p.stem.replace("_", " ").title()
            })
    return reports


@app.get("/api/reports/{report_id}")
def get_report(report_id: str):
    p = REPORTS_DIR / f"{report_id}.md"
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"Report '{report_id}' not found.")
    with open(p, "r", encoding="utf-8") as f:
        return {"id": report_id, "content": f.read()}


# Mount built frontend static files if available
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
