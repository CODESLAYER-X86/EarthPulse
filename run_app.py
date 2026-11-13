#!/usr/bin/env python3
"""
Launcher for Dancing with SARs
Starts the FastAPI application serving both backend APIs and the built React frontend.
"""

import sys
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("   Dancing with SARs — Multi-Temporal NISAR Analysis   ")
    print("   Potengi Estuary, Natal, Brazil (EPSG:32725)         ")
    print("=" * 60)
    print("Application launching at: http://localhost:8000")
    print("API Documentation:        http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)
