"""
test_endpoints.py

Quick test script to verify all API endpoints are working.
Run this after starting the server with: uvicorn main:app --reload
"""

import json

# Check for requests library
try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library not installed")
    print("📦 Install with: pip install requests")
    exit(1)

BASE_URL = "http://localhost:8000"

def test_endpoint(name, url):
    """Test a single endpoint and display results."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Status: {response.status_code} OK")
        print(f"\nResponse Preview:")
        print(json.dumps(data, indent=2)[:500] + "...")
        
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server not running?")
        print("   Start server with: uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("🌊 HydroSentinel API Endpoint Tests")
    print("="*60)
    
    endpoints = [
        ("Health Check", f"{BASE_URL}/api/health"),
        ("Surface Health", f"{BASE_URL}/api/surface-health"),
        ("Oil Slicks", f"{BASE_URL}/api/oil-slicks"),
        ("Risk Zones", f"{BASE_URL}/api/risk-zones"),
    ]
    
    results = []
    for name, url in endpoints:
        results.append(test_endpoint(name, url))
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    passed = sum(results)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All endpoints working! Ready for frontend integration.")
    else:
        print(f"\n⚠️  {total - passed} endpoint(s) failed. Check logs above.")
    
    print("\n📚 API Documentation:")
    print(f"   Swagger UI: {BASE_URL}/docs")
    print(f"   ReDoc:      {BASE_URL}/redoc")


if __name__ == "__main__":
    main()
