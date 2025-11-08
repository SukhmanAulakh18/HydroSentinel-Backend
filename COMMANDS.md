# 🎯 QUICK COMMAND REFERENCE

## Installation
```bash
pip install -r requirements.txt
```

## Generate Demo Data
```bash
python generate_demo_data.py
```

## Test Individual Modules
```bash
python processing/surface.py    # Test NDWI analysis
python processing/oil.py         # Test oil detection
python processing/risk.py        # Test risk zones
```

## Start Server
```bash
uvicorn main:app --reload
```

## Test Endpoints
```bash
# Option 1: Python script
python test_endpoints.py

# Option 2: Browser
# Visit: http://localhost:8000/api/health

# Option 3: curl
curl http://localhost:8000/api/health
curl http://localhost:8000/api/surface-health
curl http://localhost:8000/api/oil-slicks
curl http://localhost:8000/api/risk-zones
```

## All-in-One (Windows)
```bash
start.bat
```

## API Documentation
```
Swagger UI:  http://localhost:8000/docs
ReDoc:       http://localhost:8000/redoc
```

## Troubleshooting
```bash
# Rasterio install issues (Windows)
pip install pipwin
pipwin install gdal
pipwin install rasterio

# Or use conda
conda install -c conda-forge rasterio

# Check server status
curl http://localhost:8000/api/health

# Different port
uvicorn main:app --reload --port 8001
```
