"""
generate_demo_data.py

Generates synthetic GeoTIFF and GeoJSON files for testing
the HydroSentinel processing modules.
"""

import json

# Check for required dependencies
try:
    import numpy as np
    import importlib
    # Import rasterio dynamically to avoid static "could not be resolved" diagnostics
    rasterio = importlib.import_module("rasterio")
    transform_module = importlib.import_module("rasterio.transform")
    from_bounds = transform_module.from_bounds
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    MISSING_PACKAGE = str(e)


def generate_ndwi_raster():
    """Generate a synthetic NDWI raster for Lake Ontario."""
    print("Generating NDWI raster (data/ndwi_lake.tif)...")
    
    # Define bounds (Lake Ontario region)
    west, south = -79.6, 43.4
    east, north = -79.1, 43.7
    width, height = 500, 300
    
    # Create synthetic NDWI data
    # Higher values = healthier water
    np.random.seed(42)
    ndwi = np.random.rand(height, width) * 0.6 + 0.2  # Range: 0.2 to 0.8
    
    # Add some "unhealthy" patches
    ndwi[100:150, 200:250] = 0.1
    ndwi[200:220, 300:350] = 0.15
    
    # Create transform
    transform = from_bounds(west, south, east, north, width, height)
    
    # Write raster
    with rasterio.open(
        'data/ndwi_lake.tif',
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=ndwi.dtype,
        crs='EPSG:4326',
        transform=transform,
    ) as dst:
        dst.write(ndwi, 1)
    
    print("✅ Created data/ndwi_lake.tif")


def generate_sar_raster():
    """Generate a synthetic SAR raster for oil slick detection."""
    print("Generating SAR raster (data/sar_harbour.tif)...")
    
    # Define bounds (Toronto Harbour)
    west, south = -79.4, 43.6
    east, north = -79.25, 43.7
    width, height = 400, 300
    
    # Create synthetic SAR data (normalized backscatter)
    np.random.seed(123)
    sar = np.random.rand(height, width) * 0.7 + 0.3  # Range: 0.3 to 1.0
    
    # Add dark patches (oil slicks)
    sar[150:180, 100:140] = 0.15  # Oil slick 1
    sar[220:240, 250:280] = 0.20  # Oil slick 2
    sar[80:95, 300:330] = 0.18    # Oil slick 3
    
    # Create transform
    transform = from_bounds(west, south, east, north, width, height)
    
    # Write raster
    with rasterio.open(
        'data/sar_harbour.tif',
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=sar.dtype,
        crs='EPSG:4326',
        transform=transform,
    ) as dst:
        dst.write(sar, 1)
    
    print("✅ Created data/sar_harbour.tif")


def generate_risk_zones_geojson():
    """Generate synthetic risk zone GeoJSON."""
    print("Generating risk zones (data/risk_zones.geojson)...")
    
    risk_zones = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "name": "Industrial Zone A",
                    "risk_score": 0.85,
                    "description": "High contamination risk near factories"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.47, 43.60],
                        [-79.44, 43.60],
                        [-79.44, 43.63],
                        [-79.47, 43.63],
                        [-79.47, 43.60]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Urban Runoff Zone B",
                    "risk_score": 0.44,
                    "description": "Medium risk from urban drainage"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.42, 43.57],
                        [-79.39, 43.57],
                        [-79.39, 43.60],
                        [-79.42, 43.60],
                        [-79.42, 43.57]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "name": "Residential Zone C",
                    "risk_score": 0.18,
                    "description": "Low risk residential area"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-79.37, 43.54],
                        [-79.34, 43.54],
                        [-79.34, 43.57],
                        [-79.37, 43.57],
                        [-79.37, 43.54]
                    ]]
                }
            }
        ]
    }
    
    with open('data/risk_zones.geojson', 'w') as f:
        json.dump(risk_zones, f, indent=2)
    
    print("✅ Created data/risk_zones.geojson")


if __name__ == "__main__":
    print("🚀 Generating demo data for HydroSentinel...\n")
    
    if not DEPENDENCIES_AVAILABLE:
        print(f"❌ Error: Required dependencies not installed")
        print(f"   {MISSING_PACKAGE}")
        print("\n📦 Please install required packages:")
        print("   pip install rasterio numpy")
        print("\nAlternative: The processing modules will work with fallback demo data")
        print("even without these files. You can skip data generation for now.")
        exit(1)
    
    try:
        generate_ndwi_raster()
        generate_sar_raster()
        generate_risk_zones_geojson()
        
        print("\n✅ All demo data generated successfully!")
        print("You can now test the processing modules:")
        print("  python processing/surface.py")
        print("  python processing/oil.py")
        print("  python processing/risk.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have installed: pip install rasterio numpy shapely")
