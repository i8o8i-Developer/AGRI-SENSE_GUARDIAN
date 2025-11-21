import os
import aiohttp
from typing import Any, Dict, Tuple
from google.adk.tools.tool_context import ToolContext


async def WeatherTool(
    Location: str,
    DaysAhead: int,
    ToolContextInstance: ToolContext
) -> Dict[str, Any]:
    """
    Retrieve Comprehensive Agricultural Weather Intelligence For Indian Farming.
    
    This Tool Serves As The Primary Weather Data Provider For AgriSenseGuardian,
    Leveraging Multiple Free And Reliable APIs To Deliver Accurate, Localized
    Weather Forecasts Optimized For Agricultural Decision Making. All Data Is
    Sourced From Authoritative Meteorological Services And Processed To Highlight
    Farming-Relevant Parameters And Risk Indicators.
    
    Key Features:
    -------------
    - Real-Time Temperature Forecasts (Min/Max/Average) For Crop Stress Assessment
    - Precipitation Predictions (Amount + Probability) For Irrigation Planning
    - Wind Speed Data For Optimal Pesticide Application Timing
    - Humidity Levels For Disease Risk Monitoring
    - Solar Radiation Measurements For Photosynthesis And Growth Modeling
    - Automated Agricultural Risk Analysis (Drought, Flood, Heat, Disease)
    
    Data Sources:
    -------------
    - Open-Meteo API (Primary): Free, No API Key Required, Global Coverage
    - OpenWeatherMap API (Fallback): When Available, Enhanced Geocoding
    - OpenStreetMap Nominatim: Free Geocoding Service For Location Resolution
    
    Args:
        Location: Geographic Location As City Name, Full Address, Or Coordinates
                 (e.g., "Pune, Maharashtra" or "18.5204,73.8567")
        DaysAhead: Forecast Duration In Days (1-14 Day Range Supported)
        ToolContextInstance: Google ADK Context For Tool Execution Management
        
    Returns:
        Structured Dictionary Containing:
        - Complete Weather Forecast Data With Statistical Aggregations
        - Agricultural Risk Assessments Based On Weather Conditions
        - Data Source Metadata And Confidence Indicators
        - Geographic Coordinates And Location Validation
        - Timestamp And Processing Information
    
    """
    
    # Resolve Location To Precise Geographic Coordinates For Accurate Forecasting
    geo = await _GeocodeLocation(Location)
    if isinstance(geo, dict) and geo.get('Status') == 'Error':
        return geo

    Lat, Lon = geo

    # Fetch Weather From Open-Meteo (Real Only)
    WeatherData = await _FetchOpenMeteoWeather(Lat, Lon, DaysAhead)
    if WeatherData.get('Status') != 'Success':
        return {
            'Status': 'Error',
            'Message': WeatherData.get('Message', 'Open-Meteo Request Failed'),
            'Location': Location
        }

    # Analyze Agricultural Risks Based On Returned Weather
    RiskAnalysis = _AnalyzeAgriculturalRisks(WeatherData)

    return {
        'Status': 'Success',
        'Location': Location,
        'ForecastDays': DaysAhead,
        'Coordinates': {'Lat': Lat, 'Lon': Lon},
        **WeatherData,
        'RiskFactors': RiskAnalysis,
        'DataSource': 'Open-Meteo',
        'Timestamp': WeatherData.get('Timestamp') or '2025-11-17T12:00:00Z'
    }


async def _GeocodeLocation(Location: str) -> Tuple[float, float] | Dict[str, Any]:
    """
    Resolve Geographic Location Strings To Precise Latitude/Longitude Coordinates.
    
    This Function Implements A Robust Geocoding Strategy That Handles Various
    Location Input Formats And Leverages Multiple Free Geocoding Services To
    Ensure Reliable Coordinate Resolution For Weather API Queries. The Process
    Prioritizes Accuracy While Maintaining Fallback Options For Resilience.
    
    Resolution Strategy:
    -------------------
    1. Direct Coordinate Parsing: If Input Contains Numeric Lat/Lon Pairs
    2. OpenStreetMap Nominatim: Primary Free Geocoding Service (No API Key)
    3. OpenWeatherMap Geocoding: Enhanced Service When API Key Is Available
    4. Error Handling: Structured Error Responses For Failed Resolutions
    
    The Function Automatically Appends 'India' To Location Queries When Not
    Explicitly Specified To Improve Geocoding Accuracy For Indian Locations.
    
    Args:
        Location: Location Description (City Name, Address, Or Lat/Lon Coordinates)
        
    Returns:
        Tuple Of (Latitude, Longitude) As Floats If Successful, Or Error Dictionary
        With Status And Descriptive Message If Geocoding Fails
    """
    
    # Attempt Direct Parsing Of Coordinate Strings For Efficiency
    if ',' in Location and all(part.strip().replace('.', '').replace('-', '').isdigit() for part in Location.split(',')):
        try:
            Parts = Location.split(',')
            return float(Parts[0].strip()), float(Parts[1].strip())
        except Exception as e:
            return {'Status': 'Error', 'Message': f'Invalid Coordinate Format: {e}'}
    
    # Utilize OpenStreetMap Nominatim For Primary Geocoding (Completely Free)
    try:
        async with aiohttp.ClientSession() as Session:
            # Enhance Location Queries With Country Context For Better Accuracy
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
                        print(f"[WeatherTool] Geocoded '{Location}' → ({lat:.4f}, {lon:.4f})")
                        return lat, lon
    except Exception as e:
        return {'Status': 'Error', 'Message': f'Nominatim Geocoding Failed: {e}'}
    
    # Try OpenWeatherMap Geocoding (If API Key Available)
    OpenWeatherKey = os.getenv('OPENWEATHER_API_KEY', '')
    
    if OpenWeatherKey:
        try:
            async with aiohttp.ClientSession() as Session:
                SearchLocation = Location
                GeoUrl = f"http://api.openweathermap.org/geo/1.0/direct?q={SearchLocation}&limit=1&appid={OpenWeatherKey}"
                async with Session.get(GeoUrl, timeout=8) as Response:
                    if Response.status == 200:
                        GeoData = await Response.json()
                        if GeoData and len(GeoData) > 0:
                            return float(GeoData[0]['lat']), float(GeoData[0]['lon'])
        except Exception as e:
            return {'Status': 'Error', 'Message': f'OpenWeather Geocoding Failed: {e}'}

    return {'Status': 'Error', 'Message': 'Geocoding Failed. Provide Coordinates Like "lat,lon" Or A Resolvable Place Name.'}

async def _FetchOpenMeteoWeather(Lat: float, Lon: float, Days: int) -> Dict[str, Any]:
    """
    🌍 Fetch REAL Weather From Open-Meteo API (FREE, NO KEY REQUIRED!)
    
    Open-Meteo Is Amazing Because:
    - Completely Free For Up To 10,000 Requests/Day
    - No API Key Needed
    - High-Quality Weather Models
    - Perfect For Agricultural Applications
    """
    
    try:
        async with aiohttp.ClientSession() as Session:
            # Build Open-Meteo API Request
            # See: https://open-meteo.com/en/docs
            Params = {
                'latitude': Lat,
                'longitude': Lon,
                'daily': ','.join([
                    'temperature_2m_max',
                    'temperature_2m_min',
                    'precipitation_sum',
                    'precipitation_probability_max',
                    'windspeed_10m_max',
                    'shortwave_radiation_sum',
                    'relative_humidity_2m_mean'
                ]),
                'timezone': 'Asia/Kolkata',  # Indian Standard Time
                'forecast_days': min(Days, 16)  # Max 16 days
            }
            
            Url = "https://api.open-meteo.com/v1/forecast"
            
            async with Session.get(Url, params=Params, timeout=12) as Response:
                if Response.status == 200:
                    Data = await Response.json()
                    Daily = Data.get('daily', {})
                    
                    # Calculate Averages And Totals
                    TempMax = Daily.get('temperature_2m_max', [])
                    TempMin = Daily.get('temperature_2m_min', [])
                    PrecipSum = Daily.get('precipitation_sum', [])
                    PrecipProb = Daily.get('precipitation_probability_max', [])
                    WindSpeed = Daily.get('windspeed_10m_max', [])
                    SolarRad = Daily.get('shortwave_radiation_sum', [])
                    Humidity = Daily.get('relative_humidity_2m_mean', [])
                    
                    # Calculate Statistics
                    AvgTempMax = sum(TempMax) / len(TempMax) if TempMax else 0
                    AvgTempMin = sum(TempMin) / len(TempMin) if TempMin else 0
                    TotalPrecip = sum(PrecipSum) if PrecipSum else 0
                    AvgPrecipProb = sum(PrecipProb) / len(PrecipProb) if PrecipProb else 0
                    MaxWind = max(WindSpeed) if WindSpeed else 0
                    AvgSolar = sum(SolarRad) / len(SolarRad) if SolarRad else 0
                    AvgHumidity = sum(Humidity) / len(Humidity) if Humidity else 0
                    RainyDays = sum(1 for p in PrecipSum if p > 1.0)
                    
                    return {
                        'Status': 'Success',
                        'Temperature': {
                            'Min': round(min(TempMin) if TempMin else 20, 1),
                            'Max': round(max(TempMax) if TempMax else 35, 1),
                            'Average': round((AvgTempMax + AvgTempMin) / 2, 1),
                            'Unit': 'Celsius'
                        },
                        'Precipitation': {
                            'Total': round(TotalPrecip, 1),
                            'Probability': round(AvgPrecipProb, 0),
                            'Days': RainyDays,
                            'Unit': 'mm'
                        },
                        'WindSpeed': {
                            'Average': round(sum(WindSpeed) / len(WindSpeed) if WindSpeed else 15, 1),
                            'Max': round(MaxWind, 1),
                            'Unit': 'km/h'
                        },
                        'Humidity': {
                            'Average': round(AvgHumidity, 0),
                            'Unit': 'Percent'
                        },
                        'SolarRadiation': {
                            'Average': round(AvgSolar / 1000, 2),  # Convert Wh to kWh
                            'Unit': 'kWh/m²/day'
                        },
                        'RawData': Daily,
                        'Timestamp': Data.get('generationtime_ms', None)
                    }
                else:
                    return {'Status': 'Error', 'Message': f'Open-Meteo HTTP {Response.status}'}
    
    except Exception as Error:
        return {'Status': 'Error', 'Message': str(Error)}


def _AnalyzeAgriculturalRisks(WeatherData: Dict[str, Any]) -> Dict[str, Any]:
    """
    🌾 Analyze Weather Data For Agricultural Risks Specific To Indian Farming.
    
    Considers:
    - Monsoon Patterns
    - Kharif/Rabi Season Requirements
    - Common Indian Crops (Rice, Wheat, Cotton, Sugarcane)
    """
    
    Temp = WeatherData.get('Temperature', {})
    Precip = WeatherData.get('Precipitation', {})
    Humidity = WeatherData.get('Humidity', {})
    Wind = WeatherData.get('WindSpeed', {})
    
    TempMax = Temp.get('Max', 30)
    TempMin = Temp.get('Min', 20)
    PrecipTotal = Precip.get('Total', 0)
    HumidityAvg = Humidity.get('Average', 70)
    
    # Drought Risk (Insufficient Rainfall)
    DroughtRisk = 'Low'
    if PrecipTotal < 10:
        DroughtRisk = 'High'
    elif PrecipTotal < 30:
        DroughtRisk = 'Medium'
    
    # Flood Risk (Excessive Rainfall)
    FloodRisk = 'Low'
    if PrecipTotal > 200:
        FloodRisk = 'High'
    elif PrecipTotal > 100:
        FloodRisk = 'Medium'
    
    # Heat Stress Risk (High Temperatures)
    HeatStressRisk = 'Low'
    if TempMax > 40:
        HeatStressRisk = 'High'
    elif TempMax > 35:
        HeatStressRisk = 'Medium'
    
    # Disease Risk (High Humidity + Moderate Temps)
    DiseaseRisk = 'Low'
    if HumidityAvg > 80 and 20 < TempMax < 35:
        DiseaseRisk = 'High'
    elif HumidityAvg > 70:
        DiseaseRisk = 'Medium'
    
    # Confidence Based On Data Completeness
    Confidence = 90 if all([Temp, Precip, Humidity]) else 70
    
    # Generate Farming Advice
    Advice = []
    if DroughtRisk == 'High':
        Advice.append('🚨 High Drought Risk - Ensure Irrigation Systems Are Ready')
        Advice.append('💧 Consider Drip Irrigation For Water Conservation')
    
    if FloodRisk == 'High':
        Advice.append('🌊 Flood Risk Detected - Improve Field Drainage')
        Advice.append('📍 Avoid Planting In Low-Lying Areas')
    
    if HeatStressRisk == 'High':
        Advice.append('☀️ Extreme Heat Expected - Provide Shade For Sensitive Crops')
        Advice.append('⏰ Schedule Activities For Early Morning/Late Evening')
    
    if DiseaseRisk == 'High':
        Advice.append('🍄 High Disease Risk - Monitor For Fungal Infections')
        Advice.append('💊 Keep Fungicides Ready, Check Crop Health Daily')
    
    if not Advice:
        Advice.append('✅ Weather Conditions Are Favorable For Farming Activities')
        Advice.append('🌱 Good Time For Field Preparation And Planting')
    
    return {
        'DroughtRisk': DroughtRisk,
        'FloodRisk': FloodRisk,
        'HeatStressRisk': HeatStressRisk,
        'DiseaseRisk': DiseaseRisk,
        'Confidence': Confidence,
        'FarmingAdvice': Advice
    }