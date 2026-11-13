#!/usr/bin/env python3
"""
End-to-End System Integration & Scientific Verification Test (Updated)
Tests Phase 1 through Phase 9 of Dancing with SARs
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.main import app

client = TestClient(app)

def test_health():
    print("[TEST] Checking /api/health ...")
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["data_ready"] is True
    assert data["filtered_ready"] is True
    assert data["classified_ready"] is True
    print("  ✓ Health check passed (Filtered & Classified data ready).")

def test_metadata():
    print("[TEST] Checking /api/metadata ...")
    resp = client.get("/api/metadata")
    assert resp.status_code == 200
    data = resp.json()
    assert data["study_area"] == "Potengi Estuary, Natal, Brazil"
    assert len(data["acquisitions"]) == 3
    print("  ✓ Metadata check passed.")

def test_regions_and_geojson():
    print("[TEST] Checking /api/regions/summary & GeoJSON vector endpoints ...")
    sum_resp = client.get("/api/regions/summary")
    assert sum_resp.status_code == 200
    summaries = sum_resp.json()
    assert len(summaries) == 6
    print(f"  ✓ Region summaries passed ({len(summaries)} intervals).")

    geo_resp = client.get("/api/geojson/change-regions/HH_028_033")
    assert geo_resp.status_code == 200
    geo_data = geo_resp.json()
    assert geo_data["type"] == "FeatureCollection"
    assert len(geo_data["features"]) > 0
    first_prop = geo_data["features"][0]["properties"]
    assert "mean_diff_db" in first_prop
    assert "area_ha" in first_prop
    print(f"  ✓ GeoJSON change regions passed ({len(geo_data['features'])} vector polygons in HH 028→033).")

def test_csv_export():
    print("[TEST] Checking /api/export/summary.csv ...")
    resp = client.get("/api/export/summary.csv")
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]
    assert "Polarization,Interval,Pair" in resp.text
    print("  ✓ CSV export passed.")

def test_raster_rendering():
    print("[TEST] Checking dynamic raster rendering (Filtered, Classified, Differences, ML) ...")
    layers = [
        "cycle_028_hh_filtered_db",
        "cycle_028_hh_db",
        "diff_hh_028_033_filtered",
        "cls_hh_028_033",
        "ml_clusters",
        "common_valid_mask"
    ]
    for l in layers:
        resp = client.get(f"/api/raster/{l}.png")
        assert resp.status_code == 200, f"Layer {l} failed: {resp.status_code}"
        assert resp.headers["content-type"] == "image/png"
        assert len(resp.content) > 1000
        print(f"  ✓ Layer '{l}.png' rendered successfully ({len(resp.content)} bytes).")

def test_reports():
    print("[TEST] Checking /api/reports ...")
    resp = client.get("/api/reports")
    assert resp.status_code == 200
    reports = resp.json()
    report_ids = [r["id"] for r in reports]
    for required in [
        "visualization_pipeline_audit",
        "sar_processing_validation",
        "change_detection_validation",
        "ml_validation_report",
        "final_implementation_report"
    ]:
        assert required in report_ids, f"Missing report: {required}"
        print(f"  ✓ Verified report: {required}.md")

def test_frontend_serving():
    print("[TEST] Checking root frontend SPA serving ...")
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Dancing with SARs" in resp.text
    print("  ✓ Static SPA delivery passed.")

def run_all():
    print("\n=======================================================")
    print("   RUNNING UPDATED SCIENTIFIC INTEGRATION TESTS        ")
    print("=======================================================\n")
    try:
        test_health()
        test_metadata()
        test_regions_and_geojson()
        test_csv_export()
        test_raster_rendering()
        test_reports()
        test_frontend_serving()
        print("\n>>> ALL TESTS PASSED SUCCESSFULLY! (100% PASS RATE) <<<\n")
    except AssertionError as e:
        print(f"\n[FAIL] Test assertion error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_all()
