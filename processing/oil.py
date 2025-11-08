"""
processing/oil.py

Detects oil slicks and chemical films from SAR imagery.
Uses dark patch detection with confidence scoring.
"""

import json

# Lazy imports for optional dependencies
try:
    import rasterio
    from rasterio.features import shapes
    import numpy as np
    RASTERIO_AVAILABLE = True
except ImportError:
    RASTERIO_AVAILABLE = False

try:
    from shapely.geometry import shape, mapping
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False

SAR_PATH = "data/sar_harbour.tif"
DARK_THRESHOLD = 0.3  # Values below this are potential oil slicks
MIN_AREA_PIXELS = 50  # Minimum slick size to report


def get_oil_slicks():
    """
    Load SAR raster, detect dark patches (oil slicks),
    and return GeoJSON features for the API contract.
    
    Returns:
        dict: {
            "aoi": str,
            "slick_count": int,
            "features": [
                {
                    "type": "Feature",
                    "properties": {"id": int, "area_km2": float, "confidence": float},
                    "geometry": {"type": "Polygon", "coordinates": [...]}
                },
                ...
            ]
        }
    """
    # Check if dependencies are available
    if not RASTERIO_AVAILABLE or not SHAPELY_AVAILABLE:
        print("Warning: rasterio or shapely not installed. Using demo data.")
        return _generate_demo_slicks()
    
    try:
        with rasterio.open(SAR_PATH) as src:
            sar = src.read(1)
            transform = src.transform
            crs = src.crs
            
            # Normalize SAR data to 0-1 range
            sar_normalized = (sar - sar.min()) / (sar.max() - sar.min() + 1e-8)
            
    except FileNotFoundError:
        print(f"Error: {SAR_PATH} not found. Generating demo data...")
        return _generate_demo_slicks()
    
    # Detect dark patches (potential oil slicks)
    dark_mask = sar_normalized < DARK_THRESHOLD
    
    # Extract polygon features from mask
    features = []
    feature_id = 1
    
    for geom, value in shapes(dark_mask.astype(np.uint8), transform=transform):
        if value == 1:  # Dark patch
            poly = shape(geom)
            area_pixels = poly.area / (transform.a * abs(transform.e))
            
            # Filter by minimum area
            if area_pixels >= MIN_AREA_PIXELS:
                # Calculate confidence based on darkness and size
                confidence = min(0.95, 0.5 + (area_pixels / 500) * 0.3)
                
                # Convert to geographic coordinates (rough estimate)
                area_km2 = area_pixels * (transform.a * abs(transform.e)) / 1e6
                
                features.append({
                    "type": "Feature",
                    "properties": {
                        "id": feature_id,
                        "area_km2": round(area_km2, 2),
                        "confidence": round(confidence, 2)
                    },
                    "geometry": mapping(poly)
                })
                feature_id += 1
    
    return {
        "aoi": "Toronto Harbour",
        "slick_count": len(features),
        "features": features[:10]  # Limit to top 10 detections
    }


def _generate_demo_slicks():
    """
    Generate demo oil slick data when SAR file is not available.
    Matches the mock data structure from main.py.
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


if __name__ == "__main__":
    result = get_oil_slicks()
    print(json.dumps(result, indent=2))
