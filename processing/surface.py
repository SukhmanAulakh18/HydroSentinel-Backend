"""
processing/surface.py

Reads NDWI raster, computes water mask, healthy mask,
and returns metrics & bounds for the AOI.
"""

import numpy as np

NDWI_PATH = "data/ndwi_lake.tif"

def get_surface_health():
    """
    Load NDWI raster, calculate water mask, healthy mask,
    and return metrics & bounds for the API contract.
    
    Returns:
        dict: {
            "aoi": str,
            "bounds": {"south": float, "west": float, "north": float, "east": float},
            "metrics": {
                "water_pixel_count": int,
                "healthy_water_percent": float,
                "turbidity_index": float
            },
            "overlay_url": str
        }
    """
    try:
        # Import rasterio lazily so the module can be analyzed/run when rasterio is not installed.
        import rasterio
    except ImportError:
        return {"error": "rasterio library not installed. Install with: pip install rasterio"}

    try:
        with rasterio.open(NDWI_PATH) as src:
            ndwi = src.read(1)
            bounds = src.bounds
    except FileNotFoundError:
        print(f"Error: {NDWI_PATH} not found. Check data/ folder.")
        return {"error": "NDWI file not found"}
    except Exception as e:
        print(f"Error opening NDWI file: {e}")
        return {"error": "Failed to open NDWI file"}

    water_mask = ndwi > 0.1
    healthy_mask = ndwi > 0.3
    water_pixels = int(water_mask.sum())
    healthy_percent = float(healthy_mask.sum() * 100.0 / water_pixels) if water_pixels > 0 else 0.0

    bounds_dict = {
        "south": float(bounds.bottom),
        "west": float(bounds.left),
        "north": float(bounds.top),
        "east": float(bounds.right),
    }

    return {
        "aoi": "Lake Ontario - Demo Zone",
        "bounds": bounds_dict,
        "metrics": {
            "water_pixel_count": water_pixels,
            "healthy_water_percent": healthy_percent,
            "turbidity_index": 0.21,
        },
        "overlay_url": "http://localhost:8000/static/ndwi_overlay.png",
    }

if __name__ == "__main__":
    result = get_surface_health()
    import json
    print(json.dumps(result, indent=2))
