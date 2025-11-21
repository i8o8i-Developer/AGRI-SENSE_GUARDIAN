# AgriSenseGuardian MCP Tools - Satellite Fetch Tool For Retrieving Satellite Imagery And Analysis
# Follows Official Google ADK Tool Registration And MCP Tool Patterns

import os
from typing import Any, Dict
from google.adk.tools.tool_context import ToolContext


async def SatelliteFetchTool(
    Location: str,
    ImageryType: str,
    ToolContextInstance: ToolContext
) -> Dict[str, Any]:
    """
    Retrieve Satellite Imagery And Analysis Data For A Given Location.
    
    Args:
        Location: The Location Name Or Coordinates For Satellite Analysis
        ImageryType: Type Of Satellite Data To Retrieve (E.g., "NDVI", "TrueColor", "Thermal")
        ToolContextInstance: ADK Tool Context For State And Observability
        
    Returns:
        Dict Containing Satellite Imagery Metadata And Analysis Metrics (Real Only)
    """
    # Real Sentinel Hub API (Research/small-farm free tier)
    try:
        # ───────────────────────────────────────────────────────────────────
        # SENTINEL HUB CONFIGURATION
        # ───────────────────────────────────────────────────────────────────
        # FREE Tier: 10,000 Processing Units/Month
        # Sign Up: https://www.sentinel-hub.com/
        # Perfect For Indian Farmers - Covers All Of India With 10m Resolution
        # ───────────────────────────────────────────────────────────────────
        
        SentinelClientId = os.getenv('SENTINEL_CLIENT_ID', '')
        SentinelClientSecret = os.getenv('SENTINEL_CLIENT_SECRET', '')
        
        # Strict: Require Sentinel Hub credentials
        if not SentinelClientId or not SentinelClientSecret:
            return {
                'Status': 'Error',
                'Message': 'SENTINEL_CLIENT_ID/SECRET Not Configured',
                'Location': Location
            }
        
        # ───────────────────────────────────────────────────────────────────
        # STEP 1: Geocode Location
        # ───────────────────────────────────────────────────────────────────
        Lat, Lon = await _GeocodeLocation(Location)
        
        # ───────────────────────────────────────────────────────────────────
        # STEP 2: Get Sentinel Hub OAuth Token
        # ───────────────────────────────────────────────────────────────────
        import aiohttp
        import base64
        from datetime import datetime, timedelta
        from io import BytesIO
        from PIL import Image
        import numpy as np
        
        async with aiohttp.ClientSession() as Session:
            # Get OAuth2 Token
            TokenUrl = "https://services.sentinel-hub.com/oauth/token"
            AuthStr = f"{SentinelClientId}:{SentinelClientSecret}"
            AuthB64 = base64.b64encode(AuthStr.encode()).decode()
            
            Headers = {
                'Authorization': f'Basic {AuthB64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            Data = {'grant_type': 'client_credentials'}
            
            async with Session.post(TokenUrl, headers=Headers, data=Data) as Response:
                if Response.status != 200:
                    return {
                        'Status': 'Error',
                        'Message': f'Sentinel Auth Failed: HTTP {Response.status}',
                        'Location': Location
                    }
                
                TokenData = await Response.json()
                AccessToken = TokenData['access_token']
            
            # ───────────────────────────────────────────────────────────────
            # STEP 3: Request Sentinel-2 Imagery
            # ───────────────────────────────────────────────────────────────
            # Bounding Box Around Location (±0.05° ≈ 5.5km)
            Bbox = [Lon - 0.05, Lat - 0.05, Lon + 0.05, Lat + 0.05]
            
            # Date Range (Last 30 Days To Avoid Clouds)
            EndDate = datetime.now()
            StartDate = EndDate - timedelta(days=30)
            
            # Evalscript For NDVI Calculation
            Evalscript = """
            //VERSION=3
            function setup() {
                return {
                    input: ["B04", "B08", "SCL"],
                    output: { bands: 1 }
                };
            }
            function evaluatePixel(sample) {
                // Calculate NDVI: (NIR - Red) / (NIR + Red)
                let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
                // Filter clouds (SCL = 3,8,9,10,11 are clouds/shadows)
                if ([3,8,9,10,11].includes(sample.SCL)) {
                    return [NaN];
                }
                return [ndvi];
            }
            """
            
            ApiUrl = "https://services.sentinel-hub.com/api/v1/process"
            Headers = {
                'Authorization': f'Bearer {AccessToken}',
                'Content-Type': 'application/json'
            }
            
            Payload = {
                "input": {
                    "bounds": {
                        "bbox": Bbox,
                        "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}
                    },
                    "data": [{
                        "type": "sentinel-2-l2a",
                        "dataFilter": {
                            "timeRange": {
                                "from": StartDate.strftime("%Y-%m-%dT00:00:00Z"),
                                "to": EndDate.strftime("%Y-%m-%dT23:59:59Z")
                            },
                            "maxCloudCoverage": 30
                        }
                    }]
                },
                "output": {
                    "width": 512,
                    "height": 512,
                    "responses": [{
                        "identifier": "default",
                        "format": {"type": "image/tiff"}
                    }]
                },
                "evalscript": Evalscript
            }
            
            async with Session.post(ApiUrl, headers=Headers, json=Payload) as Response:
                if Response.status != 200:
                    return {
                        'Status': 'Error',
                        'Message': f'Sentinel Processing Failed: HTTP {Response.status}',
                        'Location': Location
                    }
                
                # Read NDVI GeoTIFF Bytes And Compute Stats (Real)
                ImageData = await Response.read()
                img = Image.open(BytesIO(ImageData))
                ndvi_arr = np.array(img).astype('float32')
                
                # Compute Statistics Using NaN-Safe Operations
                with np.errstate(invalid='ignore'):
                    mean = float(np.nanmean(ndvi_arr))
                    std = float(np.nanstd(ndvi_arr))
                    total = ndvi_arr.size
                    nan_count = int(np.count_nonzero(~np.isfinite(ndvi_arr)))
                    cloud_cov = (nan_count / total) * 100.0 if total else 0.0
                    veg_cover = float(np.count_nonzero(ndvi_arr > 0.4)) / total * 100.0 if total else 0.0
                
                return {
                    'Status': 'Success',
                    'Location': Location,
                    'Coordinates': {'Lat': Lat, 'Lon': Lon},
                    'ImageryType': ImageryType,
                    'CaptureDate': EndDate.strftime('%Y-%m-%d'),
                    'Resolution': '10m (Sentinel-2)',
                    'DataSource': 'Sentinel Hub (ESA)',
                    'Analysis': {
                        'NDVI': {
                            'AverageValue': round(mean, 3),
                            'StandardDeviation': round(std, 3)
                        },
                        'VegetationCover': round(veg_cover, 1),
                        'CloudCoverage': round(cloud_cov, 1),
                        'SatellitePlatform': 'Sentinel-2 L2A'
                    },
                    'Timestamp': datetime.utcnow().isoformat() + 'Z'
                }
        
    except Exception as Error:
        return {
            'Status': 'Error',
            'Message': f'SatelliteFetchTool Error: {str(Error)}',
            'Location': Location
        }


async def _GeocodeLocation(Location: str) -> tuple:
    """Convert Location Name To Coordinates Using OpenStreetMap; No Defaults."""
    # Already Coordinates
    if ',' in Location and all(p.strip().replace('.', '').replace('-', '').isdigit() for p in Location.split(',')):
        parts = Location.split(',')
        return float(parts[0].strip()), float(parts[1].strip())
    
    import aiohttp
    # OSM Nominatim (Free)
    async with aiohttp.ClientSession() as Session:
        try:
            search = Location if ('india' in Location.lower()) else f"{Location}, India"
            url = "https://nominatim.openstreetmap.org/search"
            headers = {'User-Agent': 'AgriSenseGuardian/1.0'}
            params = {'q': search, 'format': 'json', 'limit': 1}
            async with Session.get(url, params=params, headers=headers, timeout=8) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data:
                        return float(data[0]['lat']), float(data[0]['lon'])
        except Exception:
            pass
        
        # Optional OpenWeather Geocoding If Key Present
        key = os.getenv('OPENWEATHER_API_KEY', '')
        if key:
            try:
                search = Location if ('india' in Location.lower()) else f"{Location}, India"
                geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={search}&limit=1&appid={key}"
                async with Session.get(geo_url, timeout=8) as resp2:
                    if resp2.status == 200:
                        g = await resp2.json()
                        if g:
                            return float(g[0]['lat']), float(g[0]['lon'])
            except Exception:
                pass
    
            raise ValueError(f"Could Not Geocode Location: {Location}")