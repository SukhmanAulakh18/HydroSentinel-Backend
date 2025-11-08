"""
processing/risk.py

Predicts contamination/leakage risk zones based on spatial analysis.
Can load from GeoJSON or generate risk zones programmatically.
"""

import json
import os
import numpy as np

# Lazy import for optional dependency
try:
    from shapely.geometry import Point, Polygon, mapping
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False

RISK_ZONES_PATH = "data/risk_zones.geojson"


def get_risk_zones():
    """
    Load or generate risk zone polygons with risk scores.
    Returns GeoJSON features for the API contract.
    
    Returns:
        dict: {
            "aoi": str,
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": str, "risk_score": float, "category": str},
                    "geometry": {"type": "Polygon", "coordinates": [...]}
                },
                ...
            ]
        }
    """
    try:
        if os.path.exists(RISK_ZONES_PATH):
            return _load_risk_zones_from_file()
        else:
            print(f"Info: {RISK_ZONES_PATH} not found. Generating demo risk zones...")
            return _generate_demo_risk_zones()
    except Exception as e:
        print(f"Error loading risk zones: {e}")
        return _generate_demo_risk_zones()


def _load_risk_zones_from_file():
    """
    Load risk zones from GeoJSON file and ensure proper structure.
    """
    with open(RISK_ZONES_PATH, 'r') as f:
        data = json.load(f)
    
    features = []
    for idx, feature in enumerate(data.get('features', [])):
        properties = feature.get('properties', {})
        
        # Ensure required properties exist
        risk_score = properties.get('risk_score', 0.5)
        category = _categorize_risk(risk_score)
        
        features.append({
            "type": "Feature",
            "properties": {
                "name": properties.get('name', f"Zone {idx + 1}"),
                "risk_score": round(risk_score, 2),
                "category": category
            },
            "geometry": feature.get('geometry')
        })
    
    return {
        "aoi": "Peel Region Catchment Area",
        "features": features
    }


def _generate_demo_risk_zones():
    """
    Generate demo risk zones when file is not available.
    Creates zones around industrial/urban areas with varying risk levels.
    """
    # Demo zones around Greater Toronto Area
    zones = [
        {
            "name": "Zone A - High Risk",
            "center": [-79.47, 43.615],
            "radius": 0.015,
            "risk_score": 0.85
        },
        {
            "name": "Zone B - Medium Risk",
            "center": [-79.405, 43.585],
            "radius": 0.015,
            "risk_score": 0.44
        },
        {
            "name": "Zone C - Low Risk",
            "center": [-79.355, 43.555],
            "radius": 0.015,
            "risk_score": 0.18
        },
        {
            "name": "Zone D - Industrial",
            "center": [-79.50, 43.58],
            "radius": 0.02,
            "risk_score": 0.72
        },
    ]
    
    features = []
    for idx, zone in enumerate(zones):
        # Create polygon around center point
        polygon_coords = _create_square_polygon(
            zone['center'][0], 
            zone['center'][1], 
            zone['radius']
        )
        
        category = _categorize_risk(zone['risk_score'])
        
        features.append({
            "type": "Feature",
            "properties": {
                "name": zone['name'],
                "risk_score": zone['risk_score'],
                "category": category
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [polygon_coords]
            }
        })
    
    return {
        "aoi": "Peel Region Catchment Area",
        "features": features
    }


def _create_square_polygon(lon, lat, radius):
    """
    Create a square polygon around a center point.
    
    Args:
        lon: Center longitude
        lat: Center latitude
        radius: Half-width of square in degrees
    
    Returns:
        list: Polygon coordinates [[lon, lat], ...]
    """
    return [
        [lon - radius, lat - radius],
        [lon + radius, lat - radius],
        [lon + radius, lat + radius],
        [lon - radius, lat + radius],
        [lon - radius, lat - radius]  # Close polygon
    ]


def _categorize_risk(risk_score):
    """
    Categorize risk score into High/Medium/Low.
    
    Args:
        risk_score: Float between 0-1
    
    Returns:
        str: "High", "Medium", or "Low"
    """
    if risk_score >= 0.7:
        return "High"
    elif risk_score >= 0.4:
        return "Medium"
    else:
        return "Low"


if __name__ == "__main__":
    result = get_risk_zones()
    print(json.dumps(result, indent=2))
