# 🌊 HydroSentinel Backend

AI-powered water quality monitoring system using satellite imagery and geospatial analysis.

## 📁 Project Structure

```
HydroSentinel-Backend/
├── main.py                  # FastAPI application with endpoints
├── requirements.txt         # Python dependencies
├── generate_demo_data.py   # Script to create test data
│
├── processing/             # Analysis modules
│   ├── surface.py          # NDWI water quality analysis
│   ├── oil.py              # SAR oil slick detection
│   └── risk.py             # Contamination risk prediction
│
├── data/                   # Geospatial data (generated)
│   ├── ndwi_lake.tif      # NDWI raster for Lake Ontario
│   ├── sar_harbour.tif    # SAR imagery for Toronto Harbour
│   └── risk_zones.geojson # Risk zone polygons
│
└── static/                 # Static assets
    └── test.txt
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `rasterio` - Geospatial raster I/O
- `numpy` - Numerical computing
- `shapely` - Geometric operations

### 2. Generate Demo Data

```bash
python generate_demo_data.py
```

This creates synthetic test data in the `data/` folder.

### 3. Test Processing Modules

Test each module individually:

```bash
python processing/surface.py
python processing/oil.py
python processing/risk.py
```

### 4. Start the API Server

```bash
uvicorn main:app --reload
```

Server runs at: **http://localhost:8000**

## 🔗 API Endpoints

### Health Check
```
GET /api/health
```
Returns server status.

### Surface Water Quality
```
GET /api/surface-health
```
Returns NDWI-based water quality metrics and bounds.

**Response:**
```json
{
  "aoi": "Lake Ontario - Demo Zone",
  "bounds": {"south": 43.4, "west": -79.6, "north": 43.7, "east": -79.1},
  "metrics": {
    "water_pixel_count": 150000,
    "healthy_water_percent": 82.5,
    "turbidity_index": 0.21
  },
  "overlay_url": "http://localhost:8000/static/ndwi_overlay.png"
}
```

### Oil Slick Detection
```
GET /api/oil-slicks
```
Returns detected oil slicks from SAR imagery.

**Response:**
```json
{
  "aoi": "Toronto Harbour",
  "slick_count": 2,
  "features": [
    {
      "type": "Feature",
      "properties": {"id": 1, "area_km2": 0.12, "confidence": 0.82},
      "geometry": {"type": "Polygon", "coordinates": [...]}
    }
  ]
}
```

### Risk Zones
```
GET /api/risk-zones
```
Returns contamination risk zones.

**Response:**
```json
{
  "aoi": "Peel Region Catchment Area",
  "features": [
    {
      "type": "Feature",
      "properties": {"name": "Zone A", "risk_score": 0.85, "category": "High"},
      "geometry": {"type": "Polygon", "coordinates": [...]}
    }
  ]
}
```

## 🧪 Testing

### Browser Testing
- Open http://localhost:8000/api/health
- Test all endpoints in your browser

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Postman Testing
Import endpoints and test with various parameters.

## 📊 Processing Modules

### `processing/surface.py`
- Reads NDWI raster from `data/ndwi_lake.tif`
- Calculates water mask and health metrics
- Returns bounds and statistics

### `processing/oil.py`
- Analyzes SAR imagery from `data/sar_harbour.tif`
- Detects dark patches (oil slicks)
- Returns GeoJSON features with confidence scores

### `processing/risk.py`
- Loads risk zones from `data/risk_zones.geojson`
- Calculates risk scores and categories
- Can generate demo zones if file missing

## 🔧 Configuration

### Data Paths
Update paths in processing modules if needed:
- `NDWI_PATH` in `surface.py`
- `SAR_PATH` in `oil.py`
- `RISK_ZONES_PATH` in `risk.py`

### CORS
CORS is configured to allow all origins for development. Update in production:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    ...
)
```

## 📦 Dependencies

- **FastAPI**: Modern web framework
- **Rasterio**: Read/write geospatial rasters (GeoTIFF)
- **NumPy**: Array operations for raster processing
- **Shapely**: Geometric operations (polygons, points)
- **Uvicorn**: ASGI server for FastAPI

## 🐛 Troubleshooting

### Rasterio Installation Issues
If `rasterio` fails to install:
```bash
# Option 1: Use conda
conda install -c conda-forge rasterio

# Option 2: Install GDAL first
# Download GDAL wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/
pip install GDAL-3.X.X-cpXX-cpXX-win_amd64.whl
pip install rasterio
```

### Module Import Errors
Ensure you're in the project root when running:
```bash
cd HydroSentinel-Backend
python -m processing.surface
```

### Missing Data Files
Run `generate_demo_data.py` to create test files.

## 🚢 Deployment

For production deployment:
1. Update CORS settings
2. Use environment variables for paths
3. Add authentication if needed
4. Deploy with Docker or cloud platform

## 📝 Notes

- All modules have fallback to demo data if files missing
- GeoJSON follows standard format for GIS compatibility
- Raster processing is optimized for hackathon speed
- CORS allows all origins (development only)

## 👨‍💻 Dev 2 Tasks Checklist

✅ **Completed:**
- [x] `processing/surface.py` - NDWI analysis
- [x] `processing/oil.py` - Oil slick detection
- [x] `processing/risk.py` - Risk zone prediction
- [x] Demo data generation script
- [x] FastAPI endpoint integration
- [x] Documentation

🔲 **To Do:**
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Generate demo data: `python generate_demo_data.py`
- [ ] Test modules individually
- [ ] Start server: `uvicorn main:app --reload`
- [ ] Test all endpoints in browser/Postman
- [ ] Replace demo data with real satellite imagery (if available)

---

**Questions?** Check the inline code comments or run modules with `--help`
