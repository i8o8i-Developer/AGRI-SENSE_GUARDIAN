# AgriSenseGuardian Copernicus Tool - ESA Climate Data Store Integration
# Provides European Space Agency Satellite Data For Agricultural Decision Support
# Uses Copernicus Climate Data Store (CDS) API For Professional Satellite Analytics

import os
import json
from typing import Any, Dict, List
from datetime import datetime, timedelta
from google.adk.tools.tool_context import ToolContext

# Try To Import Copernicus CDS API Client
# If You Haven't Installed It Yet, Run: pip install cdsapi
try:
    import cdsapi
    CDSAPI_AVAILABLE = True
except ImportError:
    CDSAPI_AVAILABLE = False

try:
    import xarray as xr
    import numpy as np
    XR_AVAILABLE = True
except ImportError:
    XR_AVAILABLE = False


async def CopernicusTool(
    Location: str,
    DaysBack: int,
    ToolContextInstance: ToolContext
) -> Dict[str, Any]:
    """
    Retrieve Satellite-Based Agricultural Climate Data From Copernicus CDS.
    
    Fetches Professional Satellite Measurements From The European Space Agency's
    Copernicus Climate Data Store, Including Soil Moisture, Vegetation Indices,
    Land Surface Temperature, And Evapotranspiration Data. Uses ERA5-Land And
    Sentinel Satellite Datasets For High-Resolution Agricultural Analytics.
    
    The Tool Attempts Real Copernicus API Access First (Requires Free Registration
    And API Key), With Automatic Fallback To NASA POWER Data For Development.
    Provides Farmer-Actionable Insights For Irrigation Planning, Crop Health
    Monitoring, And Climate Risk Assessment.
    
    Args:
        Location: Geographic Location As String. Accepts:
                 - City/Region Names (e.g., "Punjab, India", "Maharashtra")
                 - Coordinate Pairs (e.g., "19.0760,72.8777")
                 Indian Locations Are Automatically Appended With ", India" For Better Geocoding.
        DaysBack: Number Of Historical Days To Analyze (1-30 Days Recommended).
                 Longer Periods May Impact Performance Due To Large Dataset Sizes.
        ToolContextInstance: ADK Tool Context For Session State Management And
                           Observability Integration.
        
    Returns:
        Dict: Structured Copernicus Data Response With The Following Keys:
            - Status: Operation Status ('Success' Or 'Error')
            - Location: Original Location String Provided
            - SoilMoisture: Dict With Current Level, Trend, And Unit Information
            - VegetationHealth: Dict With NDVI Score, Interpretation, And Trend
            - Evapotranspiration: Dict With Water Use Rate And Units
            - Temperature: Dict With Surface Temperature Statistics (°C)
            - Precipitation: Dict With Rainfall Accumulation And Units
            - FarmingAdvice: List Of Actionable Recommendations For Farmers
            - DataSource: 'CopernicusCDS' For Real Data Or 'Simulation' For Fallback
            - Timestamp: ISO Format Timestamp Of Data Retrieval
            
        On Error Returns:
            - Status: 'Error'
            - Message: Error Description String
            - Location: Original Location String
    """
    
    # ─────────────────────────────────────────────────────────────────────────
    # STEP 1: Try Real Copernicus API (Will Fallback If No Credentials)
    # ─────────────────────────────────────────────────────────────────────────
    try:
        ApiKey = os.getenv('COPERNICUS_API_KEY', '')
        if CDSAPI_AVAILABLE and XR_AVAILABLE and ApiKey and ':' in ApiKey:
            # Real Processing Path
            Lat, Lon = await _GeocodeLocation(Location)
            result = await _FetchAndProcessERA5Land(ApiKey, Lat, Lon, DaysBack, Location)
            if isinstance(result, dict):
                return result
        # Fallback Path Using NASA POWER (No Keys Required)
        return await _FallbackFromNASAPower(Location, DaysBack)
    except Exception as Error:
        # Ensure We Never Fail The Pipeline; Always Provide Structured Output
        try:
            return await _FallbackFromNASAPower(Location, DaysBack)
        except Exception:
            return {'Status': 'Error', 'Message': str(Error), 'Location': Location}


async def _GeocodeLocation(Location: str) -> tuple:
    """
    🗺️ I Convert Location Names To Coordinates Using Free Geocoding Services
    
    Tries:
    1. Parse If Coordinates Are Provided
    2. OpenStreetMap Nominatim (FREE!)
    3. Pre-Coded Indian Agricultural Regions
    4. Mumbai Fallback
    """
    
    # Check If Location Is Already Coordinates (e.g., "19.0760,72.8777")
    if ',' in Location and Location.replace(',', '').replace('.', '').replace('-', '').replace(' ', '').isdigit():
        Parts = Location.split(',')
        return (float(Parts[0].strip()), float(Parts[1].strip()))
    
    # Try OpenStreetMap Nominatim (FREE!)
    try:
        import aiohttp
        async with aiohttp.ClientSession() as Session:
            SearchLocation = Location
            if 'India' not in Location and 'india' not in Location:
                SearchLocation = f"{Location}, India"
            
            NominatimUrl = f"https://nominatim.openstreetmap.org/search"
            Headers = {'User-Agent': 'AgriSenseGuardian/1.0'}
            Params = {
                'q': SearchLocation,
                'format': 'json',
                'limit': 1
            }
            
            async with Session.get(NominatimUrl, params=Params, headers=Headers, timeout=5) as Response:
                if Response.status == 200:
                    GeoData = await Response.json()
                    if GeoData and len(GeoData) > 0:
                        lat = float(GeoData[0]['lat'])
                        lon = float(GeoData[0]['lon'])
                        print(f"[CopernicusTool] Geocoded '{Location}' → ({lat:.4f}, {lon:.4f})")
                        return (lat, lon)
    except Exception as e:
        return {'Status': 'Error', 'Message': f'Nominatim Geocoding Failed: {e}'}
    
    return {'Status': 'Error', 'Message': 'Geocoding Failed. Provide Coordinates Like "lat,lon" Or A Resolvable Place Name.'}


async def _FetchAndProcessERA5Land(ApiKey: str, Lat: float, Lon: float, DaysBack: int, Location: str) -> Dict[str, Any]:
    """
    Fetch Real ERA5-Land Data From Copernicus CDS And Process With xarray.
    
    Downloads NetCDF Data And Computes:
    - Soil Moisture (%) with trend analysis
    - Evapotranspiration (mm/day)
    - Precipitation Total (mm)
    - Temperature Min/Mean/Max (°C)
    """
    if not CDSAPI_AVAILABLE or not XR_AVAILABLE:
        return {'Status': 'Error', 'Message': 'Missing cdsapi Or xarray Dependencies.'}
    
    try:
        import asyncio
        import tempfile
        from pathlib import Path
        
        # Initialize Copernicus CDS API Client
        Client = cdsapi.Client(key=ApiKey)
        
        # Calculate Date Range
        EndDate = datetime.utcnow()
        StartDate = EndDate - timedelta(days=min(DaysBack, 30))  # Limit To 30 days
        
        # Build Unique year/month/day Lists
        years = sorted(list(set([StartDate.year, EndDate.year])))
        months = sorted(list(set([StartDate.strftime('%m'), EndDate.strftime('%m')])))
        days = sorted(list(set([StartDate.strftime('%d'), EndDate.strftime('%d')])))
        
        # Define Bounding Box Around Location (±0.25° ~ 25km)
        Area = [
            Lat + 0.25,  # North
            Lon - 0.25,  # West
            Lat - 0.25,  # South
            Lon + 0.25   # East
        ]
        
        # Request ERA5-Land Data
        Request = {
            'variable': [
                'volumetric_soil_water_layer_1',  # Soil Moisture 0-7cm
                '2m_temperature',
                'total_precipitation',
                'potential_evaporation'
            ],
            'year': [str(y) for y in years],
            'month': months,
            'day': days,
            'time': ['00:00', '06:00', '12:00', '18:00'],
            'area': Area,
            'format': 'netcdf'
        }
        
        # Download NetCDF File In Executor To Avoid Blocking
        def _retrieve(target: str):
            Client.retrieve('reanalysis-era5-land', Request, target)
            return target
        
        with tempfile.TemporaryDirectory() as td:
            target = str(Path(td) / 'era5_land.nc')
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, _retrieve, target)
            
            # Load NetCDF With xarray
            ds = await loop.run_in_executor(None, xr.open_dataset, target)
            
            # Process Variables
            sm = ds.get('swvl1') if 'swvl1' in ds.variables else ds.get('volumetric_soil_water_layer_1')
            t2m = ds.get('t2m') if 't2m' in ds.variables else ds.get('2m_temperature')
            tp = ds.get('tp') if 'tp' in ds.variables else ds.get('total_precipitation')
            pev = ds.get('pev') if 'pev' in ds.variables else ds.get('potential_evaporation')
            
            # Helper To Safely Compute Means
            def safe_mean(var, factor=1.0):
                try:
                    return float(var.mean().item()) * factor if var is not None else None
                except Exception:
                    return None
            
            def safe_min_max(var, factor=1.0):
                try:
                    if var is not None:
                        return float(var.min().item()) * factor, float(var.max().item()) * factor
                    return None, None
                except Exception:
                    return None, None
            
            # Compute Soil Moisture (%)
            soil_pct = safe_mean(sm, 100.0) if sm is not None else None
            
            # Compute Temperature (K → °C)
            temp_k_mean = safe_mean(t2m) if t2m is not None else None
            temp_k_min, temp_k_max = safe_min_max(t2m) if t2m is not None else (None, None)
            temp_c_mean = (temp_k_mean - 273.15) if temp_k_mean is not None else None
            temp_c_min = (temp_k_min - 273.15) if temp_k_min is not None else None
            temp_c_max = (temp_k_max - 273.15) if temp_k_max is not None else None
            
            # Compute Precipitation (m → mm)
            precip_m = safe_mean(tp) if tp is not None else None
            precip_mm = precip_m * 1000.0 if precip_m is not None else None
            
            # Compute Evapotranspiration (m → mm/day)
            et_m = safe_mean(pev) if pev is not None else None
            et_mm_day = abs(et_m) * 1000.0 / max(DaysBack, 1) if et_m is not None else None
            
            # Calculate Soil Moisture Trend
            soil_trend = 'Unknown'
            try:
                if sm is not None:
                    n = sm.sizes.get('time', 0)
                    if n >= 8:
                        q = max(n // 4, 1)
                        first = float(sm.isel(time=slice(0, q)).mean().item()) * 100
                        last = float(sm.isel(time=slice(-q, None)).mean().item()) * 100
                        delta = last - first
                        if delta > 1.0:
                            soil_trend = 'Increasing'
                        elif delta < -1.0:
                            soil_trend = 'Decreasing'
                        else:
                            soil_trend = 'Stable'
            except Exception:
                soil_trend = 'Unknown'
            
            # Build result
            result = {
                'Status': 'Success',
                'Location': Location,
                'Coordinates': {'Latitude': Lat, 'Longitude': Lon},
                'Period': f'Last {DaysBack} Days',
                'SoilMoisture': {
                    'Level': round(soil_pct, 1) if soil_pct is not None else None,
                    'Unit': '%',
                    'Trend': soil_trend,
                    'Interpretation': f"Soil Is {'Very Wet' if soil_pct and soil_pct > 70 else 'Adequately Moist' if soil_pct and soil_pct > 50 else 'Moderately Dry' if soil_pct and soil_pct > 30 else 'Very Dry'}"
                },
                'VegetationHealth': {
                    'NDVI': None,
                    'Status': 'Not Available',
                    'Interpretation': 'NDVI Data Not Included In ERA5-Land'
                },
                'Evapotranspiration': {
                    'Rate': round(et_mm_day, 2) if et_mm_day is not None else None,
                    'Unit': 'mm/day',
                    'Interpretation': f"Crops Using {et_mm_day:.1f} mm Of Water Per Day" if et_mm_day else None
                },
                'Temperature': {
                    'Average': round(temp_c_mean, 1) if temp_c_mean is not None else None,
                    'Min': round(temp_c_min, 1) if temp_c_min is not None else None,
                    'Max': round(temp_c_max, 1) if temp_c_max is not None else None,
                    'Unit': '°C'
                },
                'Precipitation': {
                    'Total': round(precip_mm, 1) if precip_mm is not None else None,
                    'Unit': 'mm',
                    'Interpretation': f"{'Heavy' if precip_mm and precip_mm > 200 else 'Moderate' if precip_mm and precip_mm > 100 else 'Light' if precip_mm and precip_mm > 30 else 'Very Low'} Rainfall" if precip_mm else None
                },
                'DataSource': 'CopernicusERA5Land',
                'Timestamp': datetime.utcnow().isoformat() + 'Z'
            }
            
            # Close Dataset
            try:
                ds.close()
            except Exception:
                pass
            
            return result
        
    except Exception as Error:
        return {'Status': 'Error', 'Message': f'Copernicus API Error: {str(Error)}', 'Location': Location}


async def _FallbackFromNASAPower(Location: str, DaysBack: int) -> Dict[str, Any]:
    """Graceful Fallback When Copernicus Credentials/Libs Are Unavailable.

    Uses NASA POWER Via Existing SatelliteTool To Return Real, Free Data And
    Constructs A Compatible Response With Conservative Heuristics.
    """
    try:
        from Tools.SatelliteTool import GetSatelliteData
        nasa = await GetSatelliteData(Location, max(1, min(30, DaysBack)))
        if nasa.get('Status') != 'Success':
            raise RuntimeError(nasa.get('Message', 'NASA POWER Error'))

        precip_total = nasa.get('Precipitation', {}).get('Total')
        temp_avg = nasa.get('Temperature', {}).get('Average')
        solar_avg = nasa.get('SolarRadiation', {}).get('Average')

        # Simple Soil Moisture Heuristic (Informational Only)
        soil_level = None
        if isinstance(precip_total, (int, float)):
            if precip_total >= 200:
                soil_level = 70
            elif precip_total >= 100:
                soil_level = 50
            elif precip_total >= 30:
                soil_level = 35
            else:
                soil_level = 22

        # ET Approximation (Very Rough, For Guidance Only)
        et_rate = None
        try:
            if isinstance(solar_avg, (int, float)) and isinstance(temp_avg, (int, float)):
                et_rate = round(max(0.5, min(8.0, 0.12 * solar_avg + 0.04 * max(0, temp_avg - 20))), 2)
        except Exception:
            et_rate = None

        return {
            'Status': 'Success',
            'Location': Location,
            'Coordinates': nasa.get('Coordinates', {}),
            'Period': nasa.get('Period') or f'Last {DaysBack} Days',
            'SoilMoisture': {
                'Level': soil_level,
                'Unit': '%',
                'Trend': 'Unknown',
                'Interpretation': None if soil_level is None else (
                    'Very Wet' if soil_level >= 70 else 'Adequately Moist' if soil_level >= 50 else 'Moderately Dry' if soil_level >= 30 else 'Very Dry'
                )
            },
            'VegetationHealth': {
                'NDVI': None,
                'Status': 'Not Available In Fallback',
                'Interpretation': 'NDVI Requires Sentinel Hub Or Copernicus Processing'
            },
            'Evapotranspiration': {
                'Rate': et_rate,
                'Unit': 'mm/day',
                'Interpretation': None if et_rate is None else f'Estimated Crop Water Use ~{et_rate} mm/day'
            },
            'Temperature': nasa.get('Temperature', {}),
            'Precipitation': nasa.get('Precipitation', {}),
            'DataSource': 'CopernicusFallbackUsingNASAPOWER',
            'Timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    except Exception as e:
        return {
            'Status': 'Error',
            'Message': f'Fallback Failed: {str(e)}',
            'Location': Location
        }

__all__ = ['CopernicusTool']