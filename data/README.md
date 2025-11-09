# Data Directory

This directory will contain geospatial data files:

- `ndwi_lake.tif` - NDWI raster for Lake Ontario
- `sar_harbour.tif` - SAR imagery for Toronto Harbour  
- `risk_zones.geojson` - Risk zone polygons

## Generate Demo Data

Run the following command to generate sample data:

```bash
python generate_demo_data.py
```

## Real Data

If you have real satellite imagery, place your GeoTIFF files here with the correct filenames.

**Note:** The processing modules will work with fallback demo data even if these files are missing.
