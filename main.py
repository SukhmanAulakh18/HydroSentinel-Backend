from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


# This MUST be named "app" so that `uvicorn main:app` can find it
app = FastAPI(title="HydroSentinel API")

# ✅ CORRECT CORS setup (no parentheses after CORSMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # fine for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple test endpoint
@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "HydroSentinel"}

# -----------------------------------------------
# 🌊 Surface Health Endpoint (NDWI mock)
# -----------------------------------------------
@app.get("/api/surface-health")
def surface_health():
    """
    Simulated NDWI-based surface water quality data.
    Frontend can display overlay + basic stats.
    """
    return {
        "aoi": "Lake Ontario - Demo Zone",
        "bounds": {
            "south": 43.4,
            "west": -79.6,
            "north": 43.7,
            "east": -79.1,
        },
        "metrics": {
            "water_pixel_count": 234567,
            "healthy_water_percent": 82.5,
            "turbidity_index": 0.21,
        },
        "overlay_url": "http://localhost:8000/static/ndwi_overlay.png"
    }


# -----------------------------------------------
# 🛢 Oil Slicks / Chemical Films (SAR mock)
# -----------------------------------------------
@app.get("/api/oil-slicks")
def oil_slicks():
    """
    Mock oil slick detection results using SAR imagery.
    Returns polygons with confidence levels.
    """
    return {
        "aoi": "Toronto Harbour",
        "slick_count": 2,
        "features": [
            {
                "type": "Feature",
                "properties": {"id": 1, "area_km2": 0.12, "confidence": 0.82},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.35, 43.63],
                        [-79.33, 43.63],
                        [-79.33, 43.65],
                        [-79.35, 43.65],
                        [-79.35, 43.63]
                    ]]
                },
            },
            {
                "type": "Feature",
                "properties": {"id": 2, "area_km2": 0.08, "confidence": 0.71},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.31, 43.61],
                        [-79.29, 43.61],
                        [-79.29, 43.63],
                        [-79.31, 43.63],
                        [-79.31, 43.61]
                    ]]
                },
            },
        ],
    }


# -----------------------------------------------
# 💧 Leak / Risk Zones (Prediction mock)
# -----------------------------------------------
@app.get("/api/risk-zones")
def risk_zones():
    """
    Mock contamination/leakage risk zones.
    Each zone has a risk_score and category.
    """
    return {
        "aoi": "Peel Region Catchment Area",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Zone A", "risk_score": 0.85, "category": "High"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.47, 43.60],
                        [-79.44, 43.60],
                        [-79.44, 43.63],
                        [-79.47, 43.63],
                        [-79.47, 43.60]
                    ]]
                },
            },
            {
                "type": "Feature",
                "properties": {"name": "Zone B", "risk_score": 0.44, "category": "Medium"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.42, 43.57],
                        [-79.39, 43.57],
                        [-79.39, 43.60],
                        [-79.42, 43.60],
                        [-79.42, 43.57]
                    ]]
                },
            },
            {
                "type": "Feature",
                "properties": {"name": "Zone C", "risk_score": 0.18, "category": "Low"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.37, 43.54],
                        [-79.34, 43.54],
                        [-79.34, 43.57],
                        [-79.37, 43.57],
                        [-79.37, 43.54]
                    ]]
                },
            },
        ],
    }
