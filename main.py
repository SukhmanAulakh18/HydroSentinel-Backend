from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Try to import Dev 2 logic (processing layer)
try:
    from processing.surface import get_surface_health
    from processing.oil import get_oil_slicks
    from processing.risk import get_risk_zones

    DEV2_AVAILABLE = True
except ImportError:
    DEV2_AVAILABLE = False

# FastAPI app instance
app = FastAPI(
    title="HydroSentinel API",
    description="Backend for HydroSentinel – satellite-powered water intelligence platform",
    version="0.1.0",
)

# Serve static files (e.g. NDWI overlay PNGs) from /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS so the React frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # fine for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# 🩺 Health check
# -------------------------------
@app.get("/api/health")
def health_check():
    """Simple endpoint to verify that the backend is running."""
    return {"status": "ok", "service": "HydroSentinel"}


# -------------------------------
# 🌊 Surface Health (NDWI)
# -------------------------------
@app.get("/api/surface-health")
def surface_health():
    """
    NDWI-based surface water health metrics + overlay URL.

    Uses processing.surface.get_surface_health() when available,
    otherwise returns mock data so frontend can keep working.
    """
    if DEV2_AVAILABLE:
        return get_surface_health()

    # Fallback mock data
    return {
        "aoi": "Lake Ontario - Demo Zone",
        "bounds": {
            "south": 43.4,
            "west": -79.6,
            "north": 43.7,
            "east": -79.1,
        },
        "metrics": {
            "water_pixel_count": 234_567,
            "healthy_water_percent": 82.5,
            "turbidity_index": 0.21,
        },
        "overlay_url": "http://localhost:8000/static/ndwi_overlay.png",
    }


# -------------------------------
# 🛢 Oil & Chemical Films (SAR)
# -------------------------------
@app.get("/api/oil-slicks")
def oil_slicks():
    """
    Oil/chemical film polygons + summary count.

    Uses processing.oil.get_oil_slicks() when available,
    otherwise returns mock data.
    """
    if DEV2_AVAILABLE:
        return get_oil_slicks()

    # Fallback mock data
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
                        [-79.35, 43.63],
                    ]],
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
                        [-79.31, 43.61],
                    ]],
                },
            },
        ],
    }


# -------------------------------
# 💧 Leak / Contamination Risk Zones
# -------------------------------
@app.get("/api/risk-zones")
def risk_zones():
    """
    Risk polygons with risk_score + category.

    Uses processing.risk.get_risk_zones() when available,
    otherwise returns mock data.
    """
    if DEV2_AVAILABLE:
        return get_risk_zones()

    # Fallback mock data
    return {
        "aoi": "Peel Region Catchment Area",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Zone A",
                    "risk_score": 0.85,
                    "category": "High",
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.47, 43.60],
                        [-79.44, 43.60],
                        [-79.44, 43.63],
                        [-79.47, 43.63],
                        [-79.47, 43.60],
                    ]],
                },
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Zone B",
                    "risk_score": 0.44,
                    "category": "Medium",
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.42, 43.57],
                        [-79.39, 43.57],
                        [-79.39, 43.60],
                        [-79.42, 43.60],
                        [-79.42, 43.57],
                    ]],
                },
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Zone C",
                    "risk_score": 0.18,
                    "category": "Low",
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.37, 43.54],
                        [-79.34, 43.54],
                        [-79.34, 43.57],
                        [-79.37, 43.57],
                        [-79.37, 43.54],
                    ]],
                },
            },
        ],
    }