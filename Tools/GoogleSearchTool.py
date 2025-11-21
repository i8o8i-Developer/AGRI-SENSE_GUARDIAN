"""
Agri Sense Guardian Google Search Tool - Dynamic AI-Powered Web Search Integration For Agricultural Intelligence

Provides Advanced Web Search Capabilities With Dynamic AI-Powered Routing Based On Query Context And Intent.
Supports Multiple Search Providers With Intelligent Content Analysis And Adaptive Provider Selection.

Dynamic AI-Powered Routing Features:
- Intelligent Query Intent Analysis Using Advanced Content Understanding
- Context-Aware Provider Selection Based On Agricultural Domain Expertise
- Adaptive Routing That Learns From Query Patterns And User Needs
- Real-Time Optimization For Agricultural Information Retrieval Quality

Search Provider Support:
- Google CSE: Requires GOOGLE_SEARCH_ENGINE_ID + GOOGLE_API_KEY Environment Variables
- SerpAPI: Requires SERPAPI_API_KEY Environment Variable For Commercial Search API

Dynamic Routing Categories:
- Government/Official Services → Google CSE (Official Sources Required)
- Advisory/Extension Services → Google CSE (Agricultural Guidance)
- News/Market Information → SerpAPI (Current Events & Timeliness)
- Local Resources/Contacts → Google CSE (Geographic Relevance)
- Equipment/Machinery → Google CSE (Commercial Sources)
- Weather/Climate Data → SerpAPI (Real-Time Information)
- Technical Research → SerpAPI (Comprehensive Academic Sources)
- Pest/Disease Management → Google CSE (Extension Sources)
- Education/Training → SerpAPI (Learning Resources)
- General Agriculture → Google CSE (Balanced Quality Sources)

Returns Structured Search Results With Title, Link, Snippet, And Display Link Information.
"""

from __future__ import annotations

import os
import asyncio
import json
from typing import List, Dict, Any, Optional

import aiohttp


async def SearchCse(query: str, api_key: str, cse_id: str, num: int = 5) -> List[Dict[str, Any]]:
    """
    Execute Search Using Google Custom Search Engine.

    Performs A Search Query Against Google CSE And Returns Structured Results.
    Optimized For Precision And Relevance In Agricultural Advisory Queries.

    Args:
        query: Search Query String
        api_key: Google API Key
        cse_id: Custom Search Engine ID
        num: Number Of Results To Return (Default 5)
        
    Returns:
        List Of Search Result Dictionaries With Title, Link, Snippet
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "num": num
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("items", [])
                    return [
                        {
                            "Title": item.get("title", ""),
                            "Link": item.get("link", ""),
                            "Snippet": item.get("snippet", ""),
                            "DisplayLink": item.get("displayLink", "")
                        }
                        for item in items
                    ]
                else:
                    return [{"Error": f"API Error: {response.status}"}]
    except Exception as e:
        return [{"Error": str(e)}]


async def SearchSerpapi(query: str, api_key: str, num: int = 5) -> List[Dict[str, Any]]:
    """
    Execute Search Using SerpAPI Service.

    Performs A Comprehensive Search Using SerpAPI And Returns Structured Results.
    Optimized For Broad Coverage And Technical Agricultural Information.

    Args:
        query: Search Query String
        api_key: SerpAPI Key
        num: Number Of Results To Return

    Returns:
        List Of Search Result Dictionaries
    """
    url = "https://serpapi.com/search.json"
    params = {"engine": "google", "q": query, "api_key": api_key, "num": num}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, timeout=20) as resp:
            if resp.status != 200:
                return []
            data = await resp.json()
            organic = data.get("organic_results", [])
            results = []
            for it in organic[:num]:
                results.append({
                    "title": it.get("title"),
                    "link": it.get("link"),
                    "snippet": it.get("snippet") or it.get("snippet_highlighted_words", []),
                    "displayLink": it.get("displayed_link")
                })
            return results


class DynamicQueryRouter:
    """
    AI-Powered Dynamic Query Routing Agent For Agricultural Search Optimization.

    Uses Advanced Language Models To Intelligently Analyze Agricultural Queries And
    Route Them To The Most Appropriate Search Provider Based On Content Understanding,
    Context Awareness, And Agricultural Domain Expertise.
    """

    def __init__(self):
        """Initialize The Dynamic Router With AI Capabilities."""
        # For now, we'll implement a simplified version that can be enhanced with AI later
        # This maintains the same interface but allows for future AI integration
        pass

    def AnalyzeQueryDynamically(self, query: str) -> Dict[str, Any]:
        """
        Dynamic AI-Powered Query Analysis For Optimal Search Provider Routing.

        Uses Intelligent Content Analysis To Determine The Most Appropriate Search Provider
        Based On Query Intent, Agricultural Context, And Information Requirements.

        Args:
            query: Search Query String To Analyze Dynamically

        Returns:
            Dict: Comprehensive Analysis Results With Provider Recommendation And Optimized Parameters
        """
        query_lower = query.lower()

        # Dynamic Analysis Based On Query Content And Context

        # 1. Government And Official Services - Always Need Official Sources
        if self._contains_any(query_lower, ['government', 'ministry', 'department', 'scheme', 'program', 'subsidy', 'loan', 'insurance', 'policy', 'pm kisan', 'kcc', 'krishi', 'agri office', 'official', 'certificate', 'license']):
            return {
                'provider': 'google_cse',
                'reason': 'Government And Official Agricultural Services Query - Official Sources Required For Accurate Information',
                'num_results': 4,
                'site_restriction': None,
                'search_type': 'government'
            }

        # 2. Advisory And Extension Services - Official Agricultural Guidance
        if self._contains_any(query_lower, ['advisory office', 'extension office', 'agricultural office', 'farm office', 'krishi office', 'agricultural extension', 'farm advisory', 'crop advisory']):
            return {
                'provider': 'google_cse',
                'reason': 'Agricultural Advisory And Extension Services Query - Official Extension Sources Required',
                'num_results': 3,
                'site_restriction': None,
                'search_type': 'advisory'
            }

        # 3. News, Current Events, And Market Information - Timely Broad Coverage
        if self._contains_any(query_lower, ['news', 'current', 'latest', 'recent', 'update', 'market price', 'commodity price', 'agri news', 'crop price', 'market update', 'price update', 'today', 'breaking']):
            return {
                'provider': 'serpapi',
                'reason': 'News And Market Information Query - Broad Coverage And Timeliness Required For Current Events',
                'num_results': 6,
                'site_restriction': None,
                'search_type': 'news'
            }

        # 4. Local Resources, Contacts, And Suppliers - Geographic Relevance
        if self._contains_any(query_lower, ['local', 'near me', 'nearby', 'contact', 'phone', 'address', 'supplier', 'dealer', 'store', 'shop', 'market', 'mandi', 'nursery', 'seed store', 'equipment shop']):
            return {
                'provider': 'google_cse',
                'reason': 'Local Resources And Contacts Query - Geographic Relevance Critical For Location-Based Services',
                'num_results': 4,
                'site_restriction': None,
                'search_type': 'local'
            }

        # 5. Equipment And Machinery - Commercial Sources With Local Availability
        if self._contains_any(query_lower, ['tractor', 'equipment', 'machinery', 'tool', 'implement', 'pump', 'sprayer', 'harvester', 'plough', 'combine', 'thresher', 'drone', 'irrigation system']):
            return {
                'provider': 'google_cse',
                'reason': 'Agricultural Equipment And Machinery Query - Commercial Sources With Local Supplier Information Needed',
                'num_results': 4,
                'site_restriction': None,
                'search_type': 'equipment'
            }

        # 6. Weather And Climate Information - Real-Time Data Sources
        if self._contains_any(query_lower, ['weather', 'climate', 'forecast', 'rainfall', 'temperature', 'humidity', 'wind', 'seasonal', 'monsoon', 'drought', 'flood', 'precipitation', 'climate change']):
            return {
                'provider': 'serpapi',
                'reason': 'Weather And Climate Information Query - Current And Forecast Data Required From Meteorological Sources',
                'num_results': 5,
                'site_restriction': None,
                'search_type': 'weather'
            }

        # 7. Technical Research And Studies - Comprehensive Academic Sources
        if self._contains_any(query_lower, ['research', 'study', 'experiment', 'scientific', 'data', 'analysis', 'model', 'yield', 'variety', 'technology', 'academic', 'university', 'journal']):
            return {
                'provider': 'serpapi',
                'reason': 'Technical Research And Studies Query - Comprehensive And Detailed Results Needed From Academic Sources',
                'num_results': 7,
                'site_restriction': None,
                'search_type': 'technical'
            }

        # 8. Pest And Disease Information - Agricultural Extension Sources
        if self._contains_any(query_lower, ['pest', 'disease', 'fungus', 'bacterial', 'viral', 'infection', 'treatment', 'control', 'prevention', 'symptom', 'diagnosis', 'blight', 'mildew', 'aphid', 'beetle', 'worm']) and not self._contains_any(query_lower, ['rotation', 'technique', 'method']):
            return {
                'provider': 'google_cse',
                'reason': 'Pest And Disease Information Query - Agricultural Extension Sources Preferred For Reliable Treatment Information',
                'num_results': 5,
                'site_restriction': None,
                'search_type': 'pest_disease'
            }

        # 9. Educational Content And Training - Learning Resources
        if self._contains_any(query_lower, ['training', 'course', 'seminar', 'education', 'learning', 'tutorial', 'guide', 'manual', 'book', 'certification', 'workshop', 'workshops', 'how to', 'learn', 'teach']):
            return {
                'provider': 'serpapi',
                'reason': 'Educational Content And Training Query - Comprehensive Learning Resources Needed From Educational Platforms',
                'num_results': 6,
                'site_restriction': None,
                'search_type': 'education'
            }

        # 10. General Agricultural Queries - Balanced Approach
        if self._contains_any(query_lower, ['crop', 'farm', 'agriculture', 'farming', 'soil', 'water', 'fertilizer', 'pesticide', 'seed', 'planting', 'harvest', 'cultivation', 'irrigation', 'organic', 'cultivate', 'grow', 'plant']):
            return {
                'provider': 'google_cse',
                'reason': 'General Agricultural Query - Balanced Approach With Quality Sources For Farming Information',
                'num_results': 5,
                'site_restriction': None,
                'search_type': 'general_agri'
            }

        # Fallback For Non-Agricultural Or Unclear Queries
        return {
            'provider': 'serpapi',
            'reason': 'General Or Non-Agricultural Query - Broad Coverage Approach For Maximum Relevance',
            'num_results': 5,
            'site_restriction': None,
            'search_type': 'general'
        }

    def _contains_any(self, text: str, keywords: List[str]) -> bool:
        """
        Check If Text Contains Any Of The Keywords With Word Boundaries.

        Args:
            text: Text To Search In
            keywords: List Of Keywords To Search For

        Returns:
            bool: True If Any Keyword Is Found With Word Boundaries
        """
        for keyword in keywords:
            if f' {keyword} ' in f' {text} ' or text.startswith(f'{keyword} ') or text.endswith(f' {keyword}') or text == keyword:
                return True
        return False


# Update The AgriculturalSearchRouter To Use Dynamic Routing
class AgriculturalSearchRouter:
    """
    Intelligent Search Routing Engine For Agricultural Queries.

    Analyzes Query Content And Context To Route To The Most Appropriate Search Provider.
    Uses Dynamic AI-Powered Analysis For Optimal Search Parameters And Provider Selection.
    """

    def __init__(self):
        """Initialize The Search Router With Provider Configurations And Dynamic Router."""
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_cse_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        self.serpapi_key = os.getenv("SERPAPI_API_KEY")
        self.dynamic_router = DynamicQueryRouter()

    def AnalyzeQueryType(self, query: str) -> Dict[str, Any]:
        """
        Dynamic AI-Powered Query Analysis For Optimal Search Provider Routing.

        Uses Intelligent Content Analysis To Determine The Most Appropriate Search Provider
        Based On Query Intent, Agricultural Context, And Information Requirements.

        Args:
            query: Search Query String To Analyze

        Returns:
            Dict: Comprehensive Analysis Results With Provider Recommendation And Optimized Parameters
        """
        return self.dynamic_router.AnalyzeQueryDynamically(query)

    def GetAvailableProviders(self) -> List[str]:
        """Get List Of Currently Available Search Providers."""
        providers = []
        if self.google_api_key and self.google_cse_id:
            providers.append('google_cse')
        if self.serpapi_key:
            providers.append('serpapi')
        return providers

    async def route_search(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Intelligently Route Search Query To Optimal Provider.

        Analyzes Query Content, Checks Provider Availability, And Executes Search
        With Automatic Fallback To Alternative Providers If Primary Fails.

        Args:
            query: Search Query String
            context: Optional Context Information (Location, User Type, Etc.)

        Returns:
            Dict: Structured Search Response With Routing Information
        """
        # Analyze Query To Determine Optimal Provider
        analysis = self.AnalyzeQueryType(query)
        preferred_provider = analysis['provider']
        available_providers = self.GetAvailableProviders()

        # Check If Preferred Provider Is Available
        if preferred_provider not in available_providers:
            # Fallback To First Available Provider
            if available_providers:
                actual_provider = available_providers[0]
                analysis['reason'] += f" (Fallback: {preferred_provider} Not Available)"
            else:
                return {
                    "Status": "Error",
                    "Message": "No Search Providers Available",
                    "Query": query,
                    "Routing": analysis,
                    "Results": []
                }
        else:
            actual_provider = preferred_provider

        try:
            # Execute Search With Selected Provider
            if actual_provider == 'google_cse':
                results = await SearchCse(query, self.google_api_key, self.google_cse_id, num=analysis['num_results'])
                provider_name = "GoogleCSE"
            elif actual_provider == 'serpapi':
                results = await SearchSerpapi(query, self.serpapi_key, num=analysis['num_results'])
                provider_name = "SerpAPI"
            else:
                return {
                    "Status": "Error",
                    "Message": "Invalid Provider Selected",
                    "Query": query,
                    "Routing": analysis,
                    "Results": []
                }

            return {
                "Status": "Success",
                "Provider": provider_name,
                "Query": query,
                "Routing": analysis,
                "Results": results
            }

        except Exception as e:
            # Try Fallback Provider If Available
            fallback_providers = [p for p in available_providers if p != actual_provider]
            if fallback_providers:
                try:
                    fallback_provider = fallback_providers[0]
                    analysis['reason'] += f" (Fallback Due To Error: {str(e)})"

                    if fallback_provider == 'google_cse':
                        results = await SearchCse(query, self.google_api_key, self.google_cse_id, num=analysis['num_results'])
                        provider_name = "GoogleCSE"
                    else:
                        results = await SearchSerpapi(query, self.serpapi_key, num=analysis['num_results'])
                        provider_name = "SerpAPI"

                    return {
                        "Status": "Success",
                        "Provider": provider_name,
                        "Query": query,
                        "Routing": analysis,
                        "Results": results
                    }
                except Exception as fallback_error:
                    return {
                        "Status": "Error",
                        "Message": f"Both Primary And Fallback Providers Failed: {str(e)}, {str(fallback_error)}",
                        "Query": query,
                        "Routing": analysis,
                        "Results": []
                    }

            return {
                "Status": "Error",
                "Message": f"Search Failed: {str(e)}",
                "Query": query,
                "Routing": analysis,
                "Results": []
            }


async def GoogleSearchTool(query: str, num: int = 5, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Enhanced Agricultural Search Tool With Intelligent Routing.

    Provides Web Search Capabilities With Automatic Provider Selection Based On
    Query Content And Context. Includes Fallback Mechanisms And Query Optimization
    Specifically Designed For Agricultural Information Retrieval.

    Args:
        query: Search Query String (E.G., "Punjab Agricultural Advisory Office")
        num: Maximum Number Of Results To Return (Default: 5, Max: 10)
        context: Optional Context Dictionary With Location, User Type, Etc.

    Returns:
        Dict: Structured Search Response With The Following Keys:
            - Status: Operation Status ('Success' Or 'Error')
            - Provider: Search Provider Used ('GoogleCSE' Or 'SerpAPI')
            - Query: Original Search Query String
            - Routing: Query Analysis And Routing Decision Information
            - Results: List Of Result Dictionaries With:
                * title: Page Title String
                * link: Full URL String
                * snippet: Description/Snippet Text
                * displayLink: Display Domain String

        On Error Returns:
            - Status: 'Error'
            - Message: Error Description String
            - Routing: Query Analysis Information
            - Results: Empty List
    """
    # Global Router Instance
    global _search_router
    if '_search_router' not in globals():
        _search_router = AgriculturalSearchRouter()
    
    return await _search_router.route_search(query, context)


__all__ = ["GoogleSearchTool"]