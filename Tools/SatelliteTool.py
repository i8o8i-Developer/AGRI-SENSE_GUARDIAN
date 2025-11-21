# AgriSenseGuardian Satellite Tool - NASA POWER Satellite Data Integration
# Provides Real Satellite-Derived Agricultural Parameters For Indian Farming
# Uses NASA's FREE POWER API For Global Agroclimatology Data Without API Keys

import os
import aiohttp
import datetime
from typing import Dict, Any


async def GetSatelliteData(
    Location: str,
    DaysBack: int = 7
) -> Dict[str, Any]:
    """
    Retrieve Satellite-Derived Agricultural Data From NASA POWER API.
    
    Fetches Real Satellite Measurements Including Solar Radiation, Temperature,
    Precipitation, Humidity, And Wind Speed Data From NASA's Prediction Of Worldwide
    Energy Resources (POWER) Database. This Free API Provides 40+ Years Of Global
    Agroclimatology Data Without Requiring API Key Registration.
    
    The Tool Performs Geocoding Using OpenStreetMap Nominatim (Primary) With
    OpenWeatherMap As Fallback, Then Queries NASA POWER For Agricultural Parameters
    Critical For Crop Planning And Risk Assessment.
    
    Args:
        Location: Location Name Or Coordinates As String. Accepts:
                 - City/Region Names (e.g., "Pune, India", "Punjab")
                 - Coordinate Pairs (e.g., "18.5204,73.8567")
                 Indian Locations Are Automatically Appended With ", India" For Better Geocoding.
        DaysBack: Number Of Historical Days To Retrieve Data For (Default: 7 Days).
                 Maximum Recommended Is 365 Days For Performance.
        
    Returns:
        Dict: Structured Satellite Data Response With The Following Keys:
            - Status: Operation Status ('Success' Or 'Error')
            - Location: Original Location String Provided
            - Coordinates: Dict With 'Lat' And 'Lon' Keys (Float Values)
            - DataSource: 'NASA POWER (FREE)' Identifier
            - Period: Date Range String In 'YYYYMMDD to YYYYMMDD' Format
            - DaysAnalyzed: Number Of Days Data Was Retrieved For
            - SolarRadiation: Dict With 'Average', 'Unit', And Raw 'Data'
            - Precipitation: Dict With 'Total', 'Average', 'Unit', And Raw 'Data'
            - Temperature: Dict With 'Average', 'Max', 'Min', And 'Unit'
            - Humidity: Dict With 'Average' And 'Unit'
            - WindSpeed: Dict With 'Average' And 'Unit'
            - Timestamp: ISO Format Timestamp Of Data Retrieval
            
        On Error Returns:
            - Status: 'Error'
            - Message: Error Description String
            - Location: Original Location String
            - Note: Additional Error Context Or Suggestions
    """
    
    # ───────────────────────────────────────────────────────────────────────────
    # STEP 1: Geocode location To Get Coordinates
    # ───────────────────────────────────────────────────────────────────────────
    # We Need lat/lon For NASA POWER API
    # ───────────────────────────────────────────────────────────────────────────
    
    Lat, Lon = None, None
    
    # Try Parsing Coordinates First
    if ',' in Location and all(part.replace('.', '').replace('-', '').isdigit() 
                               for part in Location.split(',')):
        try:
            Parts = Location.split(',')
            Lat = float(Parts[0].strip())
            Lon = float(Parts[1].strip())
        except:
            pass
    
    try:
        async with aiohttp.ClientSession() as Session:
            # Try OpenStreetMap Nominatim (FREE!)
            if Lat is None:
                try:
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
                                Lat = float(GeoData[0]['lat'])
                                Lon = float(GeoData[0]['lon'])
                                print(f"[SatelliteTool] Geocoded '{Location}' → ({Lat:.4f}, {Lon:.4f})")
                except Exception as e:
                    print(f"[SatelliteTool] Nominatim Geocoding Failed: {e}")
            
            # Fallback To OpenWeatherMap If Available
            if Lat is None:
                OpenWeatherKey = os.getenv('OPENWEATHER_API_KEY', '')
                if OpenWeatherKey:
                    try:
                        SearchLocation = Location
                        if 'India' not in Location and 'india' not in Location:
                            SearchLocation = f"{Location}, India"
                            
                        GeoUrl = f"http://api.openweathermap.org/geo/1.0/direct?q={SearchLocation}&limit=1&appid={OpenWeatherKey}"
                        async with Session.get(GeoUrl) as Response:
                            GeoData = await Response.json()
                            if GeoData:
                                Lat = GeoData[0]['lat']
                                Lon = GeoData[0]['lon']
                                print(f"[SatelliteTool] Geocoded '{Location}' → ({Lat:.4f}, {Lon:.4f})")
                    except Exception as e:
                        print(f"[SatelliteTool] OpenWeatherMap Geocoding Failed: {e}")
            
            # Return Error If Geocoding Failed
            if Lat is None:
                return {
                    'Status': 'Error',
                    'Message': f'Could Not Geocode Location: {Location}',
                    'Note': 'Provide Coordinates As "lat,lon" Or Ensure Location Name Is Valid'
                }
            
            # ───────────────────────────────────────────────────────────────────
            # STEP 2: Fetch Data From NASA POWER API (FREE, NO KEY!)
            # ───────────────────────────────────────────────────────────────────
            # NASA POWER API Provides Satellite-Derived Agroclimatology Data
            # Website: https://power.larc.nasa.gov/
            # ───────────────────────────────────────────────────────────────────
            
            EndDate = datetime.datetime.now()
            StartDate = EndDate - datetime.timedelta(days=DaysBack)
            
            StartStr = StartDate.strftime('%Y%m%d')
            EndStr = EndDate.strftime('%Y%m%d')
            
            # Agricultural Parameters from NASA POWER
            Params = "ALLSKY_SFC_SW_DWN,PRECTOTCORR,T2M,T2M_MAX,T2M_MIN,RH2M,WS2M"
            
            NasaUrl = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters={Params}&community=AG&longitude={Lon}&latitude={Lat}&start={StartStr}&end={EndStr}&format=JSON"
            
            async with Session.get(NasaUrl) as Response:
                NasaData = await Response.json()
                
                if 'parameters' not in NasaData:
                    return {'Error': 'NASA POWER API Error'}
                
                ParamData = NasaData['parameters']
                
                # Calculate Averages
                CalculateAvg = lambda Data: sum(Data.values()) / len(Data) if Data else 0
                
                return {
                    'Status': 'Success',
                    'Location': Location,
                    'Coordinates': {'Lat': Lat, 'Lon': Lon},
                    'DataSource': 'NASA POWER (FREE)',
                    'Period': f'{StartStr} to {EndStr}',
                    'DaysAnalyzed': DaysBack,
                    
                    # Solar Radiation - Critical For Crop Photosynthesis
                    'SolarRadiation': {
                        'Average': round(CalculateAvg(ParamData.get('ALLSKY_SFC_SW_DWN', {})), 2),
                        'Unit': 'kW-hr/m²/day',
                        'Data': ParamData.get('ALLSKY_SFC_SW_DWN', {})
                    },
                    
                    # Precipitation - For Irrigation Planning
                    'Precipitation': {
                        'Total': round(sum(ParamData.get('PRECTOTCORR', {}).values()), 2),
                        'Average': round(CalculateAvg(ParamData.get('PRECTOTCORR', {})), 2),
                        'Unit': 'mm',
                        'Data': ParamData.get('PRECTOTCORR', {})
                    },
                    
                    # Temperature - Crop Stress Monitoring
                    'Temperature': {
                        'Average': round(CalculateAvg(ParamData.get('T2M', {})), 2),
                        'Max': round(max(ParamData.get('T2M_MAX', {}).values()) if ParamData.get('T2M_MAX') else 0, 2),
                        'Min': round(min(ParamData.get('T2M_MIN', {}).values()) if ParamData.get('T2M_MIN') else 0, 2),
                        'Unit': 'Celsius'
                    },
                    
                    # Humidity - Disease Risk Assessment
                    'Humidity': {
                        'Average': round(CalculateAvg(ParamData.get('RH2M', {})), 2),
                        'Unit': 'Percent'
                    },
                    
                    # Wind Speed - For Spraying And Planting
                    'WindSpeed': {
                        'Average': round(CalculateAvg(ParamData.get('WS2M', {})), 2),
                        'Unit': 'm/s'
                    },
                    
                    'Timestamp': datetime.datetime.now().isoformat()
                }
                
    except Exception as E:
        return {
            'Status': 'Error',
            'Message': str(E),
            'Location': Location,
            'Note': 'Failed To Fetch NASA POWER Data'
        }