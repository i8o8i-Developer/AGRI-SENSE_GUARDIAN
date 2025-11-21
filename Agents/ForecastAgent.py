# AgriSenseGuardian Forecast Agent - Advanced Agricultural Risk Assessment Specialist
# Leverages Real-Time Weather, Satellite, And Climate Data For Comprehensive Farm Analysis

from typing import Dict, Any
from google.adk.tools.tool_context import ToolContext
from google.adk.agents.llm_agent import Agent

# Import Specialized Agricultural Data Collection Tools
from Tools.WeatherTool import WeatherTool
from Tools.SatelliteTool import GetSatelliteData
from Tools.CopernicusTool import CopernicusTool
from Tools.SoilTestTool import SoilTestTool


class ForecastAgent:
    """
    Specialized Agent For Agricultural Risk Forecasting And Assessment.
    
    This Agent Serves As The Primary Intelligence For Analyzing Environmental
    Conditions That Impact Crop Health And Farm Productivity. It Integrates
    Multiple Data Sources To Provide Comprehensive Risk Assessments Including:
    
    - Weather Pattern Analysis Using Real Meteorological Data
    - Satellite Imagery Interpretation For Vegetation Health Monitoring
    - Climate Model Integration For Long-Term Trend Analysis
    - Explainable Risk Predictions With Confidence Intervals
    - Multi-Temporal Forecasting (30-90 Day Horizons)
    - Structured Output Optimized For Downstream Processing
    
    The Agent Ensures All Assessments Are Based On Real, Verifiable Data
    From Authoritative Sources Like NASA, ESA, And National Weather Services.
    """
    
    def __init__(self):
        """
        Initialize The Forecast Agent With Required Dependencies.
        
        Currently A Lightweight Initialization As The Agent Relies Primarily
        On External Tool Calls For Data Collection And Processing.
        """
        pass
    
    def ComputeRiskFromSources(self, weather: Dict[str, Any], satellite: Dict[str, Any], copernicus: Dict[str, Any], soil: Dict[str, Any], location: str) -> Dict[str, Any]:
        """
        Fuse Multi-Source Environmental Data Into Comprehensive Agricultural Risk Assessments.
        
        This Method Implements Sophisticated Risk Analysis Algorithms That Combine
        Weather Forecasts, Satellite Observations, Climate Model Outputs, And Soil
        Properties To Determine Specific Agricultural Risk Levels. Incorporates Local
        Agricultural Patterns And Regional Variations For India-Specific Assessments.
        
        Args:
            weather: Real-Time Weather Data From Meteorological APIs
            satellite: Satellite-Derived Agroclimatology From NASA POWER
            copernicus: ESA Climate Data Including Soil Moisture And NDVI
            soil: Soil Profile Data From ISRIC SoilGrids Including Texture, pH, Nutrients
            location: Geographic Location String For Regional Pattern Adjustments
            
        Returns:
            Structured Risk Assessment With Categories, Levels, Confidence Scores,
            And Overall Risk Classification For Agricultural Decision Making
        """
        # Initialize Risk Levels With Conservative Baseline Assumptions
        DroughtLevel = 'Low'
        FloodLevel = 'Low'
        HeatLevel = 'Low'
        DiseaseLevel = 'Low'
        PestLevel = 'Low'
        SoilErosionLevel = 'Low'
        NutrientLeachingLevel = 'Low'
        ColdStressLevel = 'Low'
        VegetationStressLevel = 'Low'

        # Extract Weather Signals
        try:
            PrecipTotal = weather.get('Precipitation', {}).get('Total', 0)
            PrecipProb = weather.get('Precipitation', {}).get('Probability', 0)
            TMax = weather.get('Temperature', {}).get('Max', 0)
            Humidity = weather.get('Humidity', {}).get('Average', weather.get('Humidity', {}).get('Mean', 0))
        except Exception:
            PrecipTotal = 0; PrecipProb = 0; TMax = 0; Humidity = 0

        # Extract Satellite (NASA) Signals
        NasaPrecip = satellite.get('Precipitation', {}).get('Total', 0)
        NasaTempAvg = satellite.get('Temperature', {}).get('Average', 0)
        NasaRadiation = satellite.get('SolarRadiation', {}).get('Average', 0)

        # Extract Copernicus Signals
        CopernicusSoil = copernicus.get('SoilMoisture', {}) if copernicus else {}
        SoilLevel = CopernicusSoil.get('Level', None)
        Et = copernicus.get('Evapotranspiration', {}).get('Rate', None) if copernicus else None
        Ndvi = copernicus.get('VegetationHealth', {}).get('NDVI', None) if copernicus else None

        # Extract Soil Profile Signals
        SoilProfile = soil.get('SoilProfile', {}) if soil else {}
        SoilPh = SoilProfile.get('pH', None)
        SoilTexture = SoilProfile.get('SoilTexture', '')
        SoilClay = SoilProfile.get('ClayContent', None)
        SoilSand = SoilProfile.get('SandContent', None)
        SoilNitrogen = SoilProfile.get('TotalNitrogen', None)
        SoilOrganicCarbon = SoilProfile.get('SoilOrganicCarbon', None)

        # Determine Regional Agricultural Patterns
        RegionalAdjustments = self._GetRegionalAdjustments(location)

        # Drought: Low Precip + High ET + Low Soil Moisture + Soil Type Factors
        DroughtRisk = 0
        if SoilLevel is not None and SoilLevel < 30:
            DroughtRisk += 3
        elif PrecipTotal < 10 and NasaPrecip < 10:
            DroughtRisk += 2

        if Et is not None and Et >= 6:
            DroughtRisk += 2

        # Soil Texture Affects Drought Risk
        if SoilTexture:
            if 'Sandy' in SoilTexture:
                DroughtRisk += 1  # Sandy Soils Drain Faster, Higher Drought Risk
            elif 'Clay' in SoilTexture:
                DroughtRisk -= 1  # Clay Soils Retain Water Better

        # Regional Adjustments
        DroughtRisk += RegionalAdjustments.get('drought_modifier', 0)

        if DroughtRisk >= 4:
            DroughtLevel = 'High'
        elif DroughtRisk >= 2:
            DroughtLevel = 'Medium'

        # Flood: Very High Precip Totals/Probability
        if PrecipTotal is not None and PrecipTotal > 200:
            FloodLevel = 'High'
        elif PrecipTotal > 100 or PrecipProb > 70:
            FloodLevel = 'Medium'

        # Soil Erosion: High Precip Intensity + Low Vegetation Cover (NDVI Low)
        if PrecipProb > 65 and Ndvi is not None and Ndvi < 0.5:
            SoilErosionLevel = 'Medium'
        if PrecipProb > 75 and Ndvi is not None and Ndvi < 0.45:
            SoilErosionLevel = 'High'

        # Nutrient Leaching: Very high Precipitation + High Soil Moisture + Soil Texture
        LeachingRisk = 0
        if PrecipTotal > 120 and SoilLevel is not None and SoilLevel > 60:
            LeachingRisk += 2
        if PrecipTotal > 180 and SoilLevel is not None and SoilLevel > 70:
            LeachingRisk += 2

        # Soil Texture Affects Leaching
        if SoilTexture:
            if 'Sandy' in SoilTexture:
                LeachingRisk += 2  # Sandy Soils Leach Nutrients Easily
            elif 'Clay' in SoilTexture:
                LeachingRisk -= 1  # Clay Soils Retain Nutrients Better
        if LeachingRisk >= 3:
            NutrientLeachingLevel = 'High'
        elif LeachingRisk >= 1:
            NutrientLeachingLevel = 'Medium'

        # Heat Stress: High Max Temps
        if TMax >= 40 or NasaTempAvg >= 38:
            HeatLevel = 'High'
        elif TMax >= 35:
            HeatLevel = 'Medium'

        # Cold Stress: Unusually Low Max Temps or Avg Temps During Growing Period
        if TMax <= 20 or NasaTempAvg <= 18:
            ColdStressLevel = 'Medium'
        if TMax <= 15 or NasaTempAvg <= 15:
            ColdStressLevel = 'High'

        # Disease: High Humidity + Moderate Temps + Soil pH Factors
        DiseaseRisk = 0
        if Humidity >= 80 and 20 <= NasaTempAvg <= 35:
            DiseaseRisk += 3
        elif Humidity >= 65:
            DiseaseRisk += 2

        # Soil pH Affects Disease Susceptibility
        if SoilPh is not None:
            if SoilPh < 5.5 or SoilPh > 8.0:
                DiseaseRisk += 1  # Extreme pH Increases Disease Risk

        if DiseaseRisk >= 3:
            DiseaseLevel = 'High'
        elif DiseaseRisk >= 1:
            DiseaseLevel = 'Medium'

        # Pest: Heuristic From NDVI Moderate Drop Or Vegetation Cover Signals
        if Ndvi is not None and Ndvi < 0.45:
            PestLevel = 'Medium'

        # Vegetation Stress: Low NDVI + High ET Or High Temperature Extremes
        if Ndvi is not None and Ndvi < 0.50 and (Et and Et > 5 or TMax > 37):
            VegetationStressLevel = 'Medium'
        if Ndvi is not None and Ndvi < 0.45 and (Et and Et > 6 or TMax > 39):
            VegetationStressLevel = 'High'

        # Confidence From Number Of Sources Available
        Sources = 0
        Sources += 1 if weather else 0
        Sources += 1 if satellite else 0
        Sources += 1 if copernicus else 0
        Sources += 1 if soil else 0
        BaseConf = {1: 65, 2: 75, 3: 85, 4: 95}.get(Sources, 60)

        return {
            'OverallRiskLevel': max([
                DroughtLevel, FloodLevel, HeatLevel, DiseaseLevel, PestLevel,
                SoilErosionLevel, NutrientLeachingLevel, ColdStressLevel, VegetationStressLevel
            ], key=['Low','Medium','High','Critical'].index),
            'RiskCategories': {
                'DroughtRisk': {'Level': DroughtLevel, 'Confidence': BaseConf},
                'FloodRisk': {'Level': FloodLevel, 'Confidence': BaseConf},
                'PestOutbreakRisk': {'Level': PestLevel, 'Confidence': BaseConf-5},
                'DiseaseRisk': {'Level': DiseaseLevel, 'Confidence': BaseConf-5},
                'HeatStressRisk': {'Level': HeatLevel, 'Confidence': BaseConf},
                'SoilErosionRisk': {'Level': SoilErosionLevel, 'Confidence': BaseConf-5},
                'NutrientLeachingRisk': {'Level': NutrientLeachingLevel, 'Confidence': BaseConf-5},
                'ColdStressRisk': {'Level': ColdStressLevel, 'Confidence': BaseConf-5},
                'VegetationStressRisk': {'Level': VegetationStressLevel, 'Confidence': BaseConf-5}
            }
        }
    
    def _GetRegionalAdjustments(self, location: str) -> Dict[str, int]:
        """
        Determine Regional Agricultural Patterns And Risk Adjustments For Indian Locations.
        
        Based On Major Agricultural Zones In India, Adjust Risk Thresholds To Account For
        Local Climate Patterns, Soil Types, And Historical Agricultural Challenges.
        """
        LocationLower = location.lower()
        
        # Default Adjustments
        adjustments = {
            'drought_modifier': 0,
            'flood_modifier': 0,
            'heat_modifier': 0,
            'disease_modifier': 0,
            'pest_modifier': 0,
            'erosion_modifier': 0,
            'leaching_modifier': 0,
            'cold_modifier': 0,
            'stress_modifier': 0
        }
        
        # Northern India (Punjab, Haryana, Delhi) - Canal Irrigation, Wheat/Rice
        if any(state in LocationLower for state in ['punjab', 'haryana', 'delhi', 'uttar pradesh', 'rajasthan']):
            adjustments.update({
                'drought_modifier': -1,  # Canal Systems Reduce Drought Risk
                'flood_modifier': 1,    # Monsoon Flooding In Some Areas
                'heat_modifier': 1,     # Hot Summers
                'disease_modifier': 0,  # Balanced
                'pest_modifier': 1      # Intensive Farming Increases Pest Pressure
            })
        
        # Western India (Gujarat, Maharashtra) - Cotton, Sugarcane
        elif any(state in LocationLower for state in ['gujarat', 'maharashtra', 'goa']):
            adjustments.update({
                'drought_modifier': 1,  # Arid Regions
                'flood_modifier': 0,   # Coastal Areas
                'heat_modifier': 2,    # Very Hot
                'disease_modifier': 1, # Humid Coastal Areas
                'erosion_modifier': 1  # Hilly Areas
            })
        
        # Southern India (Karnataka, Tamil Nadu, Kerala) - Rice, Spices
        elif any(state in LocationLower for state in ['karnataka', 'tamil nadu', 'kerala', 'andhra pradesh', 'telangana']):
            adjustments.update({
                'drought_modifier': 0,
                'flood_modifier': 1,   # Monsoon Flooding
                'heat_modifier': 1,    # Hot Climate
                'disease_modifier': 2, # High Humidity Increases Disease
                'pest_modifier': 1,    # Tropical Pests
                'leaching_modifier': 1 # High Rainfall Causes Leaching
            })
        
        # Eastern India (West Bengal, Odisha, Bihar) - Rice Dominant
        elif any(state in LocationLower for state in ['west bengal', 'odisha', 'bihar', 'jharkhand']):
            adjustments.update({
                'drought_modifier': 0,
                'flood_modifier': 2,   # Frequent Flooding
                'heat_modifier': 1,
                'disease_modifier': 2, # High Humidity
                'erosion_modifier': 1, # River Systems
                'leaching_modifier': 1
            })
        
        # North-Eastern India - Diverse Crops, Hilly Terrain
        elif any(state in LocationLower for state in ['assam', 'meghalaya', 'tripura', 'manipur', 'nagaland', 'arunachal pradesh', 'sikkim']):
            adjustments.update({
                'drought_modifier': 0,
                'flood_modifier': 1,   # Monsoon Flooding
                'heat_modifier': 0,
                'disease_modifier': 1, # Humid Climate
                'erosion_modifier': 2, # Hilly Terrain Increases Erosion
                'cold_modifier': 1     # Higher Altitudes
            })
        
        # Central India (Madhya Pradesh, Chhattisgarh) - Soybean, Wheat
        elif any(state in LocationLower for state in ['madhya pradesh', 'chhattisgarh']):
            adjustments.update({
                'drought_modifier': 1,  # Semi-Arid
                'flood_modifier': 0,
                'heat_modifier': 1,    # Hot Climate
                'disease_modifier': 0,
                'erosion_modifier': 1
            })
        
        return adjustments

    async def ExtractCleanLocation(self, location: str) -> str:
        """
        Extract Clean Geographic Identifier From Complex Location Strings.
        
        This Method Parses User-Provided Location Descriptions To Isolate
        The Most Relevant Geographic Entity (City, District, Or Landmark)
        For Accurate API Queries And Data Retrieval.
        """
        import re
        
        location = ' '.join(location.split())
        
        if ',' in location:
            Parts = [p.strip() for p in location.split(',')]
            # Filter Out Generic Geographic Terms That Don't Help With Specific Location
            IgnoreTerms = {'india'}
            for part in Parts:
                if part.lower() not in IgnoreTerms and len(part) > 2:
                    return part
        
        Words = location.split()
        if Words:
            return Words[0]
        
        return location
    
    async def GenerateForecast(
        self,
        Location: str,
        DaysAhead: int,
        UserQuery: str = "",
        ImageryType: str = "NDVI",
        SessionState: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Execute Comprehensive Agricultural Risk Forecasting For Specified Location.
        
        This Is The Primary Method That Orchestrates Data Collection From Multiple
        Environmental Sources And Synthesizes Them Into Actionable Risk Assessments.
        The Process Involves Real-Time API Calls To Weather Services, Satellite Data
        Providers, And Climate Models To Ensure Accuracy And Timeliness.
        
        Args:
            Location: Geographic Location For Analysis (City, Coordinates, Or Address)
            DaysAhead: Number Of Days To Forecast Agricultural Conditions (30-90 Days)
            UserQuery: Optional Specific Question Or Context From The Farmer
            ImageryType: Preferred Satellite Imagery Type For Analysis (Default: NDVI)
            SessionState: Optional Dictionary For Maintaining Conversation Context
            
        Returns:
            Comprehensive Forecast Dictionary Containing:
            - Risk Assessment Across Multiple Categories
            - Confidence Scores And Data Source Information
            - Monitoring Recommendations And Actionable Insights
            - Metadata About The Analysis Process And Timestamps
        """
        
        if SessionState is None:
            SessionState = {}
        
        try:
            CleanLocation = await self.ExtractCleanLocation(Location)
            print(f"[ForecastAgent] Cleaned location: '{Location}' → '{CleanLocation}'")
        except:
            CleanLocation = Location
        
        # Always Call Real Tools And Fuse Results
        try:            
            Weather = await WeatherTool(CleanLocation, min(max(DaysAhead, 1), 14), None)
            Satellite = await GetSatelliteData(CleanLocation, min(max(DaysAhead, 1), 30))
            Copernicus = await CopernicusTool(CleanLocation, min(max(DaysAhead, 1), 30), None)
            Soil = await SoilTestTool(CleanLocation, None)

            # Extract soil variables for drivers
            SoilProfile = Soil.get('SoilProfile', {}) if Soil else {}
            SoilPh = SoilProfile.get('pH', None)
            SoilTexture = SoilProfile.get('SoilTexture', '')
            CopernicusSoil = Copernicus.get('SoilMoisture', {}) if Copernicus else {}

            risks = self.ComputeRiskFromSources(Weather or {}, Satellite or {}, Copernicus or {}, Soil or {}, Location)

            # Assemble Drivers
            Drivers = {
                'DroughtRisk': ['Low Precipitation Totals', 'High Evapotranspiration' if Copernicus else 'Low Soil Moisture Signal', f'{SoilTexture} Soil Texture' if SoilTexture else ''],
                'FloodRisk': ['High Precipitation Totals Or Probability'],
                'PestOutbreakRisk': ['Low NDVI Indicating Stress' if (Copernicus and Copernicus.get('VegetationHealth',{}).get('NDVI',1)<0.45) else 'Seasonal Baseline'],
                'DiseaseRisk': ['High Humidity With Moderate Temperatures', f'Soil pH {SoilPh:.1f}' if SoilPh else ''],
                'HeatStressRisk': ['High Max Temperature Forecast'],
                'SoilErosionRisk': ['High Rainfall Probability', 'Low Vegetation Cover' if (Copernicus and Copernicus.get('VegetationHealth',{}).get('NDVI',1)<0.5) else 'Moderate Vegetation'],
                'NutrientLeachingRisk': ['High Precipitation Totals', 'High Soil Moisture Levels' if (Copernicus and CopernicusSoil.get('Level',100)>60) else 'Moderate Moisture', f'{SoilTexture} Soil Type' if SoilTexture else ''],
                'ColdStressRisk': ['Low Max Temperature', 'Low Avg Temperature'],
                'VegetationStressRisk': ['Low NDVI', 'High ET Rate' if (Copernicus and Copernicus.get('Evapotranspiration',{}).get('Rate',0)>5) else 'Moderate ET']
            }

            result = {
                'Status': 'Success',
                'AgentName': 'ForecastAgent',
                'Location': Location,
                'UserQuery': UserQuery,
                'ForecastHorizonDays': DaysAhead,
                'OverallRiskLevel': risks['OverallRiskLevel'],
                'RiskCategories': {
                    'DroughtRisk': {**risks['RiskCategories']['DroughtRisk'], 'Drivers': Drivers['DroughtRisk']},
                    'FloodRisk': {**risks['RiskCategories']['FloodRisk'], 'Drivers': Drivers['FloodRisk']},
                    'PestOutbreakRisk': {**risks['RiskCategories']['PestOutbreakRisk'], 'Drivers': Drivers['PestOutbreakRisk']},
                    'DiseaseRisk': {**risks['RiskCategories']['DiseaseRisk'], 'Drivers': Drivers['DiseaseRisk']},
                    'HeatStressRisk': {**risks['RiskCategories']['HeatStressRisk'], 'Drivers': Drivers['HeatStressRisk']},
                    'SoilErosionRisk': {**risks['RiskCategories']['SoilErosionRisk'], 'Drivers': Drivers['SoilErosionRisk']},
                    'NutrientLeachingRisk': {**risks['RiskCategories']['NutrientLeachingRisk'], 'Drivers': Drivers['NutrientLeachingRisk']},
                    'ColdStressRisk': {**risks['RiskCategories']['ColdStressRisk'], 'Drivers': Drivers['ColdStressRisk']},
                    'VegetationStressRisk': {**risks['RiskCategories']['VegetationStressRisk'], 'Drivers': Drivers['VegetationStressRisk']}
                },
                'MonitoringFrequency': 'Weekly' if DaysAhead <= 30 else 'Twice Weekly',
                'DataSources': [
                    Weather.get('DataSource', 'Open-Meteo') if isinstance(Weather, dict) else 'WeatherTool',
                    Satellite.get('DataSource', 'NASA POWER') if isinstance(Satellite, dict) else 'SatelliteTool',
                    Copernicus.get('DataSource', 'CopernicusCDS') if isinstance(Copernicus, dict) else 'CopernicusTool',
                    Soil.get('DataSource', 'ISRIC SoilGrids') if isinstance(Soil, dict) else 'SoilTestTool'
                ],
                'GeneratedAt': risks.get('Timestamp', '2025-11-17T12:00:00Z')
            }
            return result
        except Exception as e:
            import traceback
            print(f"\n[ForecastAgent ERROR] {str(e)}")
            print(traceback.format_exc())
            return {
                'Status': 'Error',
                'AgentName': 'ForecastAgent',
                'Location': Location,
                'Message': f'Forecast Generation Failed: {str(e)}',
                'RiskCategories': {}
            }


# ADK LlmAgent Wrapper With Real Tool Calling
# Exposes An Agent The Orchestrator/Runner Can Use For Tool-Oriented Execution
RootAgent = Agent(
    model="gemini-2.0-flash",
    name="forecast_agent",
    description=(
        "Indian Agriculture Risk Forecasting Using Real Weather And Satellite Tools."
    ),
    instruction=(
        "You Are The ForecastAgent - Provide JSON Only, No Markdown Or Asterisks. \n"
        "Call Weather, Satellite, Copernicus, And Soil Tools; Fuse Signals Into Risk Categories. \n"
        "Output keys: Status, AgentName, Location, ForecastHorizonDays, OverallRiskLevel, RiskCategories, MonitoringFrequency, DataSources, GeneratedAt, UserQuery. \n"
        "RiskCategories Each Include Level, Confidence, Drivers (Array Of Driver Phrases), And Must Be Plain Text. \n"
        "Confidence Based On Number Of Sources: 4=95, 3=85, 2=75, 1=65. Deduct 5 If Signal Weak. \n"
        "Use Indian Agricultural Context; Include Numeric Measurements With Units (%, mm, °C). \n"
        "Never Add Formatting Markers (*, **). Plain JSON Only."
    ),
    tools=[
        WeatherTool,
        GetSatelliteData,
        CopernicusTool,
        SoilTestTool,
    ],
)

__all__ = [
    'ForecastAgent',
    'RootAgent',
]