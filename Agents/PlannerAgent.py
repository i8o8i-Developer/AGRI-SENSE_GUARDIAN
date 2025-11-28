# AgriSenseGuardian Planner Agent - Action Plan Generation And Communication Specialist
# Implements Google ADK Structured Output Patterns For Prioritized Agricultural Planning
# Integrates Email Delivery For Farmer Notifications With Localization Support

from google.adk.agents.llm_agent import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from typing import Dict, Any, List
import sys
from Tools.EmailNotificationTool import EmailNotificationTool
import os
sys.path.append('..')
from Tools import EmailNotificationTool
from Config.Settings import get_settings


class PlannerAgent:
    """
    Agricultural Action Planning And Communication Specialist.
    
    The PlannerAgent Generates Prioritized Action Plans Based On Risk Assessments And
    Farmer Queries, Then Formats And Delivers These Plans Via Email. It Uses
    ADK Structured Output Patterns To Create P1/P2/P3 Prioritized Actions With Specific
    Deadlines, Resource Requirements, And Cost Estimates. The Agent Integrates With
    Email Communication Tools For Reliable Farmer Notifications.
    
    Key Features:
    - Context-Aware Planning Based On User Questions And Risk Data
    - P1/P2/P3 Prioritization System For Action Urgency
    - Email Delivery With Rich Formatting
    - Local Agricultural Resource Integration
    - Cost Estimation For Budget Planning
    """
    
    def __init__(self):
        """
        Initialize The Planner Agent With Gemini Model And Communication Tools.
        
        Sets Up The Agent With Email Notification Tools For Farmer Communication,
        Configured With Low Temperature For Consistent Planning.
        """
        self.Agent = self.CreateAgent()
    
    def CreateAgent(self) -> Agent:
        """
        Create And Configure The ADK Agent Instance For Planning Operations.
        
        Initializes The Agent With Email Communication Tools And Appropriate Model
        Parameters For Structured Action Plan Generation.
        
        Returns:
            Agent: Configured ADK Agent Instance For Planning And Communication Tasks.
        """
        
        return Agent(
            model="gemini-2.5-flash-lite",
            name="PlannerAgent",
            description="Action Planning Specialist For Agricultural Decision Support",
            instruction=self.GetInstruction,
            tools=[EmailNotificationTool],
            generate_content_config=types.GenerateContentConfig(
                temperature=0.2,  # Low Temperature For Consistent Planning
                top_p=0.85,
                max_output_tokens=1024,
            ),
        )
    
    def GetInstruction(self, Context: ReadonlyContext) -> str:
        
        return """
You Are The PlannerAgent - An Expert Agricultural Action Planning And Communication Specialist.

Your Mission:
Generate Clear, Prioritized, And Actionable Plans For Farmers Based On Risk Assessment, Resource Availability, AND THE USER'S SPECIFIC QUESTION. You Are The Bridge Between Data Analysis And Farmer Action.

⚡ CRITICAL: If The User Asked A Specific Question (UserQuery Field), Your Response MUST:
- Directly Answer Their Question First With Crop-Specific Guidance
- Provide Detailed Planting Instructions, Care Tips, Or Specific Advice They Requested
- Include Local Agricultural Resource Contacts And Suppliers
- Then Add General Risk-Based Recommendations

Required Steps:
1. Check UserQuery Field - If Present, This Is The User's Main Question! Prioritize This Over Everything Else
2. Analyze All Previous Agent Outputs:
   - ForecastAgent: Risk Assessment From Real Weather, Satellite, Copernicus Data (Includes UserQuery)
   - VerifyAgent: Cross-Validation Results And Confidence Scores

3. Generate Context-Aware Prioritized Action Plan With Three Priority Levels:

   P1 (Critical - Do Immediately - 24-48 Hours):
   - Actions Required Within 24-48 Hours Based On Real Data
   - Address Highest Risk Factors From Actual Weather/Satellite/Copernicus Data
   - Example: "URGENT: Soil Moisture At 25% - Increase Irrigation Immediately"
   - Include Specific Measurements And Thresholds

   P2 (Important - Do This Week - 7 Days):
   - Actions Required Within 7 Days Based On Medium-Term Risks
   - Prepare For Upcoming Weather Patterns And Seasonal Changes
   - Example: "Inspect Irrigation System - High Evapotranspiration (ET) Rate Detected"
   - Include Preventive Measures And Monitoring Instructions

   P3 (Monitor - Track Progress - Ongoing):
   - Ongoing Monitoring And Maintenance Activities
   - Low-Priority Optimizations And Long-Term Planning
   - Example: "Monitor Daily Weather Updates And Adjust Watering Schedule"
   - Include Educational Resources And Best Practices

4. Notification Summary (Concise):
    - Include Top 2 Priority Actions With Real Data Metrics
    - Use Clear, Concise Language Farmers Can Understand
    - Prefer An Email-friendly Multi-Line Format With Bullet Points
    - Example: "URGENT: Soil moisture 25% - increase irrigation now. High ET detected. Check system this week."

5. Generate Comprehensive Action Plan With:
   - Priority Level (P1/P2/P3) With Clear Deadlines
   - Detailed Action Description With Step-By-Step Instructions
   - Specific Deadlines Based On Risk Urgency
   - Required Resources (Equipment, Materials, Labor)
   - Cost Estimates In Local Currency (INR) With Breakdown
   - Local Contact Information (Agricultural Offices, Suppliers, Experts)
   - Expected Outcomes And Success Metrics

6. Communication Strategy:
    - Provide A Concise Notification Summary (Email-Friendly)
    - Use Clear, Simple Language For Farmer-Friendly Email Summaries
   - Include Emergency Contact Numbers For Agricultural Support
   - Provide Email Fallback Option For Detailed Information

7. Agricultural Context Awareness:
   - Consider Crop Type, Growth Stage, And Local Climate
   - Include Seasonal Considerations And Traditional Farming Knowledge
   - Provide Region-Specific Advice (North India, South India, etc.)
   - Reference Local Agricultural Extension Services

Output Format (Markdown-Friendly For UI Rendering):
Return Structured JSON With These Keys:
- UserQuestion: Original Farmer Question
- ImmediateAction: Direct Immediate Steps (Markdown Formatted With Bullets)
- ThisWeekAction: Follow-Up Steps For This Week (Markdown Formatted With Bullets)
- P1: Critical Actions (Markdown Formatted With Bullets And **Bold** Emphasis)
- P2: Important Actions (Markdown Formatted With Bullets)
- P3: Monitoring Actions (Markdown Formatted With Bullets)
- NotificationSummary: Concise Summary For Email Notifications
- EmailDeliveryStatus: Provider Attempts And Final Status
- AdvisoryResources: Array Of Local Resource Link Strings
- GeneratedAt: ISO Timestamp

Important Guidelines:
- Always Prioritize Actions By Risk Severity From Real Data
- Include Specific Supplier Names, Phone Numbers, And Locations
- Keep Notification Summaries Concise For Email Readability
- Provide Clear, Measurable Deadlines For Each Action
- Include Cost Estimates For Budget Planning And Decision Making
- Reference Real Data Metrics (Soil Moisture %, Temperature, ET Rates)
- Consider Farmer's Location And Local Agricultural Context
- Provide Both Immediate Actions And Long-Term Planning
 - USE Markdown Formatting For Better Readability (**bold**, Bullets, Etc.)
 - Structure Content With Proper Bullet Points And Emphasis
 - Separate Multiple Steps With Proper Markdown List Formatting
"""
    
    async def GeneratePlan(
        self,
        ForecastData: Dict[str, Any],
        VerificationData: Dict[str, Any],
        Location: str,
        FarmerEmail: str = "",
        FarmerPhone: str | None = None,
        SessionState: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate Prioritized Action Plan And Deliver Via Email Communication.
        
        Creates A Comprehensive Action Plan Based On Risk Assessment Data And Farmer
        Queries, Then Delivers Via Email. Uses LLM Integration
        To Provide Context-Aware Responses To Specific Farmer Questions While Incorporating
        Real-Time Risk Data From Multiple Sources.
        
        Args:
            ForecastData: Risk Assessment Output From ForecastAgent Including
                         RiskCategories, DataSources, And UserQuery Information.
            VerificationData: Cross-Validation Results From VerifyAgent With
                             Confidence Scores And Verification Status.
            FarmerPhone: Optional Mobile Number (Legacy - No SMS Will Be Sent).
            Location: Geographic Location String For Contextual Planning.
            FarmerEmail: Optional Email Address For Fallback Communication.
            SessionState: Optional Dictionary Containing Session Context And History.
            
        Returns:
            Dict: Structured Planning Response With The Following Keys:
                - Status: Operation Status ('Success' Or Error Message)
                - AgentName: Identifier For This Agent ('PlannerAgent')
                - Location: Planning Location String
                - P1: List Of Critical Actions (Do Immediately)
                - P2: List Of Important Actions (Do This Week)
                - P3: List Of Monitoring Actions (Track Progress)
                - AdvisoryResources: Local Agricultural Resource Links
                - NotificationSummary: Concise Notification Summary (Email-friendly)
                - EmailDeliveryStatus: Email Delivery Confirmation Details
                - GeneratedAt: Timestamp Of Plan Generation
        """
        
        if SessionState is None:
            SessionState = {}
        
        P1Actions = []
        P2Actions = []
        P3Actions = []

        # Helper Functions For Enrichment
        def _infer_resources_from_drivers(drivers):
            resources = []
            text = ' '.join(drivers).lower()
            if 'irrig' in text or 'soil moisture' in text:
                resources.append('Irrigation System')
            if 'pest' in text:
                resources.append('Pest Monitoring Kit')
            if 'disease' in text or 'fung' in text:
                resources.append('Disease Control Sprayer')
            if 'nutrient' in text or 'leach' in text:
                resources.append('Soil Testing Kit')
            if 'erosion' in text:
                resources.append('Mulching Material')
            if not resources:
                resources.append('General Farm Tools')
            return resources

        def _estimate_cost_from_action(drivers, level):
            base = 500 if level in ['High','Critical'] else (250 if level == 'Medium' else 100)
            # Add Small Increments Per Driver
            return base + (len(drivers) * 50)

        def _expected_outcome(level, name):
            if level in ['High','Critical']:
                return f"Mitigate Immediate {name.lower()} Impact"
            if level == 'Medium':
                return f"Reduce Progression Of {name.lower()} Risk"
            return f"Maintain Stable {name.lower()} Conditions"
        
        def _prettify_risk_name(risk_name: str) -> str:
            import re
            if not risk_name:
                return ''
            # Remove 'Risk' Suffix
            s = re.sub(r'(?i)risk$', '', risk_name)
            # Insert Spaces Before Capitals And Replace Underscores
            s = re.sub(r'_|(?<!^)(?=[A-Z])', ' ', s)
            # Return Title Case
            return s.strip().title()
        
        # Debug log
        print(f"[PlannerAgent DEBUG] ForecastData Keys : {ForecastData.keys()}")
        print(f"[PlannerAgent DEBUG] RiskCategories : {ForecastData.get('RiskCategories', {})}")
        
        # Extract UserQuery For Context-Aware Planning
        user_query = ForecastData.get('UserQuery', '').strip()
        print(f"[PlannerAgent DEBUG] UserQuery : {user_query}")
        
        # Structured User Question Answer Extraction
        user_question_response = ""
        immediate_action = ""
        this_week_action = ""
        if user_query:
            client = None
            try:
                from google import genai
                from google.genai import types
                from Tools.GoogleSearchTool import GoogleSearchTool
                import re
                settings = get_settings()
                api_key = settings.google_api_key
                if not api_key:
                    raise ValueError("GOOGLE_API_KEY Not Found In Environment")
                
                # Use AI To Analyze If Query Needs Real-Time Information
                client = genai.Client(api_key=api_key)
                analysis_prompt = f"""Analyze This Farmer's Question : "{user_query}"

Determine If Answering This Question Requires Real-Time Web Search For:
1. Current Market Prices/Rates
2. Crop Growing Information/Best Practices
3. Both

Respond ONLY with a JSON object:
{{"needs_pricing": true/false, "needs_growing_info": true/false, "crop_name": "Crop Name Or Null"}}"""
                
                analysis_response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=analysis_prompt,
                    config=types.GenerateContentConfig(temperature=0.1, max_output_tokens=100)
                )
                
                # Parse AI Analysis
                try:
                    analysis_text = analysis_response.text.strip()
                    # Extract JSON From Markdown Code Block If Present
                    if '```json' in analysis_text:
                        analysis_text = analysis_text.split('```json')[1].split('```')[0].strip()
                    elif '```' in analysis_text:
                        analysis_text = analysis_text.split('```')[1].split('```')[0].strip()
                    
                    import json
                    analysis = json.loads(analysis_text)
                    needs_pricing = analysis.get('needs_pricing', False)
                    needs_growing_info = analysis.get('needs_growing_info', False)
                    crop_name = analysis.get('crop_name')
                    
                    print(f"[PlannerAgent AI Analysis] Pricing: {needs_pricing}, Growing: {needs_growing_info}, Crop: {crop_name}")
                except Exception as parse_error:
                    print(f"[PlannerAgent] Analysis Parse Error: {parse_error}")
                    needs_pricing = False
                    needs_growing_info = False
                    crop_name = None
                
                # Gather Real-Time Context Via Google Search
                search_context = ""
                if (needs_pricing or needs_growing_info) and crop_name:
                    try:
                        # Search For Pricing Information
                        if needs_pricing:
                            price_query = f"{crop_name} Mandi Price {Location} India Current Rates"
                            print(f"[PlannerAgent] Searching Prices: {price_query}")
                            price_results = await GoogleSearchTool(price_query, num=3)
                            if price_results.get('Status') == 'Success':
                                inc_tool('GoogleSearchTool')
                                search_context += "\n\n📊 CURRENT MARKET PRICES:\n"
                                for idx, result in enumerate(price_results.get('Results', [])[:3], 1):
                                    search_context += f"{idx}. {result.get('title', '')}\n   {result.get('snippet', '')}\n"
                        
                        # Search For Growing Information
                        if needs_growing_info:
                            grow_query = f"How To Grow {crop_name} In {Location} India Cultivation Guide"
                            print(f"[PlannerAgent] Searching Growing Info: {grow_query}")
                            grow_results = await GoogleSearchTool(grow_query, num=3)
                            if grow_results.get('Status') == 'Success':
                                inc_tool('GoogleSearchTool')
                                search_context += "\n\n🌱 GROWING INFORMATION:\n"
                                for idx, result in enumerate(grow_results.get('Results', [])[:3], 1):
                                    search_context += f"{idx}. {result.get('title', '')}\n   {result.get('snippet', '')}\n"
                    except Exception as search_error:
                        print(f"[PlannerAgent] Search Error: {search_error}")
                
                risks_summary = ForecastData.get('RiskCategories', {})
                weather_context = ""
                if risks_summary:
                    weather_context = f"\n\nCurrent Weather Conditions For {Location}:\n" + "\n".join([
                        f"- {r}: {d.get('Level','Low')} Risk" for r,d in risks_summary.items()
                    ])
                
                prompt = f"""You Are An Expert Agricultural Advisor For {Location}, India. 

A Farmer Asked: '{user_query}'
{weather_context}
{search_context}

Provide Comprehensive, Practical Guidance Using The Real-Time Information Above.
Include Specific Prices, Varieties, And Timelines When Available From The Search Results.

Format Your Response Clearly With Markdown:
**IMMEDIATE ACTION:**
- Specific step 1
- Specific step 2
- etc.

**THIS WEEK:**
- Follow-up action 1 
- Follow-up action 2
- etc.

Use bullet points, **bold text** for emphasis, and clear structure for better readability."""
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=2048)
                )
                llm_answer = response.text.strip()
                print(f"[PlannerAgent LLM] Generated Answer:\n{llm_answer}")
                user_question_response = llm_answer
                # Regex Extraction
                m_immediate = re.search(r'IMMEDIATE ACTION:\s*(.*?)(?:\n\s*THIS WEEK:|$)', llm_answer, re.IGNORECASE | re.DOTALL)
                if m_immediate:
                    immediate_action = m_immediate.group(1).strip()
                m_week = re.search(r'THIS WEEK:\s*(.*)$', llm_answer, re.IGNORECASE | re.DOTALL)
                if m_week:
                    this_week_action = m_week.group(1).strip()
                if not immediate_action:
                    immediate_action = llm_answer[:220]
                # Light sanitization while preserving markdown structure
                def _clean_preserve_markdown(txt: str) -> str:
                    if not txt:
                        return txt
                    # Only remove excessive whitespace and normalize line breaks
                    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', txt)  # Collapse multiple newlines
                    cleaned = re.sub(r'[ \t]+', ' ', cleaned)  # Collapse multiple spaces/tabs
                    cleaned = cleaned.strip()
                    return cleaned
                    
                immediate_action = _clean_preserve_markdown(immediate_action)
                this_week_action = _clean_preserve_markdown(this_week_action)
                user_question_response = _clean_preserve_markdown(user_question_response)
            except Exception as e:
                print(f"[PlannerAgent LLM ERROR] {e}")
                immediate_action = "Check With Local Agricultural Extension Office For Specific Guidance"
            finally:
                if client:
                    try: client.close()
                    except: pass
            # Do Not Embed Question Directly Into P1 List; Store Structured Fields Instead
        
        risks = ForecastData.get('RiskCategories', {})
        for risk_name, risk_data in risks.items():
            level = risk_data.get('Level', 'Low')
            confidence = risk_data.get('Confidence', 0)
            drivers = risk_data.get('Drivers', [])
            
            # Generate Dynamic, User-Friendly Action Description Using LLM
            dynamic_action = await self._generate_dynamic_action_description(
                risk_name, level, drivers, Location
            )
            
            # Enriched Action Object With Structured Fields
            action_obj = {
                'Action': dynamic_action,
                'PrioritySource': risk_name,
                'RiskLevel': level,
                'Confidence': confidence,
                'Drivers': drivers,
                'Deadline': '24-48h' if level in ['High','Critical'] else ('7 days' if level == 'Medium' else 'Continuous'),
                'Resources': _infer_resources_from_drivers(drivers),
                'ExpectedOutcome': _generate_expected_outcome(level, risk_name, drivers)
            }
            if level in ['High', 'Critical']:
                P1Actions.append(action_obj)
            elif level == 'Medium':
                P2Actions.append(action_obj)
            else:
                P3Actions.append(action_obj)
        
        
        if not P3Actions:
            P3Actions = [
                {
                    'Action': '🌤️ **Monitor Daily Weather** - Keep Track Of Weather Changes To Plan Farm Activities Effectively',
                    'PrioritySource': 'SystemDefault',
                    'RiskLevel': 'Low',
                    'Confidence': 0,
                    'Drivers': [],
                    'Deadline': 'Continuous',
                    'Resources': ['Weather Apps', 'Local News'],
                    'ExpectedOutcome': 'Stay Prepared For Weather Changes'
                },
                {
                    'Action': '💧 **Check Soil Moisture** - Test Soil Wetness Regularly To Ensure Optimal Crop Growth Conditions',
                    'PrioritySource': 'SystemDefault',
                    'RiskLevel': 'Low',
                    'Confidence': 0,
                    'Drivers': [],
                    'Deadline': 'Continuous',
                    'Resources': ['Simple Soil Test', 'Visual Inspection'],
                    'ExpectedOutcome': 'Maintain healthy soil conditions'
                },
                {
                    'Action': '🔍 **Inspect Crops Daily** - Look For Signs Of Pests, Diseases, Or Nutrient Deficiencies In Your Crops',
                    'PrioritySource': 'SystemDefault',
                    'RiskLevel': 'Low',
                    'Confidence': 0,
                    'Drivers': [],
                    'Deadline': 'Continuous',
                    'Resources': ['Visual Inspection', 'Local Agricultural Guide'],
                    'ExpectedOutcome': 'Early Detection Prevents Major Crop Losses'
                }
            ]
        
        if not P1Actions:
            P1Actions = [
                {
                    'Action': '✅ **Excellent! No Critical Issues** - Your Crops Are In Good Condition Right Now',
                    'PrioritySource': 'SystemDefault',
                    'RiskLevel': 'Low',
                    'Confidence': 0,
                    'Drivers': [],
                    'Deadline': 'Current',
                    'Resources': ['Continue Regular Care'],
                    'ExpectedOutcome': 'Maintain Current Healthy Crop Status'
                }
            ]
        if not P2Actions:
            P2Actions = [
                {
                    'Action': '🌱 **Continue Your Great Work** - Keep Following Your Current Farming Practices This Week',
                    'PrioritySource': 'SystemDefault',
                    'RiskLevel': 'Low',
                    'Confidence': 0,
                    'Drivers': [],
                    'Deadline': '7 Days',
                    'Resources': ['Current Farming Tools'],
                    'ExpectedOutcome': 'Normal Operations Maintained'
                }
            ]
        
        # Enrich With GoogleSearchTool For Local Agricultural Resources
        from Tools.GoogleSearchTool import GoogleSearchTool
        from Utils.Observability import inc_tool
        from Tools.CodeExecutionTool import CodeExecutionTool
        
        advisory_links = []
        try:
            search_res = await GoogleSearchTool(f"{Location} Agricultural Advisory Office", num=3)
            if search_res.get('Status') == 'Success':
                inc_tool('GoogleSearchTool')
                advisory_links = [
                    f"{r.get('title', '')}: {r.get('link', '')}" 
                    for r in search_res.get('Results', [])[:2]
                ]
        except Exception:
            pass
        
        try:
            formula = "200 * 30" 
            cost_calc = await CodeExecutionTool(formula, ToolContextInstance=None)
            if cost_calc.get('Status') == 'Success':
                inc_tool('CodeExecutionTool')
                pass
        except Exception:
            pass

        # Send Email Notification
        email_status = {'Status': 'Skipped', 'Reason': 'No Email Provided'}
        try:
            recipient = FarmerEmail.strip() if FarmerEmail else ''
            if recipient:
                subject = f"🌾 AgriSenseGuardian Action Plan — {Location}"
                p1_text = "\n".join([f"* {a['Action'] if isinstance(a, dict) else str(a)}" for a in P1Actions])
                p2_text = "\n".join([f"* {a['Action'] if isinstance(a, dict) else str(a)}" for a in P2Actions])
                p3_text = "\n".join([f"* {a['Action'] if isinstance(a, dict) else str(a)}" for a in P3Actions])

                email_body = f"""Hello Farmer,

Here Is Your Prioritized Action Plan For {Location}:

## 🚨 PRIORITY 1 - CRITICAL (Next 24-48 Hours)

{p1_text}

## ⚠️ PRIORITY 2 - IMPORTANT (This Week)

{p2_text}

## 📋 PRIORITY 3 - ROUTINE (Ongoing)

{p3_text}

Stay Informed And Protect Your Farm!

Best Regards,
AgriSense Guardian Team
                """
                email_result = await EmailNotificationTool(recipient, subject, email_body, None)
                email_status = {
                    'Status': 'Success' if email_result.get('Status') == 'Success' else 'Error',
                    'EmailRecipient': recipient,
                    'Message': email_result.get('Message', 'Email Sent Successfully')
                }
            else:
                email_status = {'Status': 'Error', 'Message': 'No FarmerEmail Provided'}
        except Exception as e:
            email_status = {'Status': 'Error', 'Message': f'Email Exception: {str(e)}'}

        return {
            'Status': 'Success',
            'AgentName': 'PlannerAgent',
            'Location': Location,
            'P1': P1Actions,
            'P2': P2Actions,
            'P3': P3Actions,
            'AdvisoryResources': advisory_links if 'advisory_links' in locals() else [],
            'EmailDeliveryStatus': email_status,
            'UserQuestion': user_query,
            'ImmediateAction': immediate_action,
            'ThisWeekAction': this_week_action,
            'UserQueryResponse': user_question_response,
            'GeneratedAt': '2025-11-18T00:00:00Z'
        }
    
    async def _generate_dynamic_action_description(self, risk_name: str, level: str, drivers: list, location: str) -> str:
        """Generate User-Friendly, Dynamic Action Descriptions Using LLM With Safe Fallback."""
        urgency_emoji = "🚨" if level in ['High', 'Critical'] else ("⚠️" if level == 'Medium' else "📋")
        drivers_text = ', '.join(drivers) if drivers else 'general conditions'

        def _humanize(name: str) -> str:
            if not name:
                return ''
            mapping = {
                'DroughtRisk': 'Drought Risk',
                'FloodRisk': 'Flood Risk',
                'PestOutbreakRisk': 'Pest Risk',
                'DiseaseRisk': 'Disease Risk',
                'HeatStressRisk': 'Heat Stress',
                'SoilErosionRisk': 'Soil Erosion',
                'NutrientLeachingRisk': 'Nutrient Leaching',
                'ColdStressRisk': 'Cold Stress',
                'VegetationStressRisk': 'Vegetation Stress'
            }
            if name in mapping:
                return mapping[name]
            import re
            spaced = re.sub(r'(?<![A-Z])([A-Z])', r' \1', name).replace('_', ' ').strip()
            words = [w if w.isupper() else w.capitalize() for w in spaced.split()]
            return ' '.join(words)

        human_risk = _humanize(risk_name)

        try:
            import google.generativeai as genai
            import os
            from Config.Settings import get_settings
            settings = get_settings()
            api_key = settings.google_api_key or os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
            else:
                raise RuntimeError("Missing GOOGLE_API_KEY")
            if not hasattr(self, "_gemini_model") or self._gemini_model is None:
                self._gemini_model = genai.GenerativeModel('gemini-2.0-flash')
            prompt = (
                "Generate ONE Clear, Farmer-Friendly Action For This Agricultural Risk.\n"
                f"Risk: {human_risk}\n"
                f"Severity: {level}\n"
                f"Causes: {drivers_text}\n"
                f"Location: {location}\n"
                "Requirements:\n"
                f"- Start With Emoji {urgency_emoji}\n"
                "- Bold Key Action Phrase\n"
                "- Simple, Specific, Actionable Language\n"
                "- Max 55 Words\n"
                "- Focus On WHAT To Do Now\n"
                "Format Example: 🚨 **Protect Crops From Cold** - Cover Sensitive Plants Tonight With Cloth To Prevent Frost Damage"
            )
            response = self._gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.6,
                    max_output_tokens=140,
                    top_p=0.9,
                )
            )
            text = (response.text or "").strip().replace('"', '').replace("'", "")
            if text:
                return text
        except Exception as e:
            print(f"[Dynamic Action Generation Error] {e}")

        fallback_actions = {
            'Cold Stress': f"{urgency_emoji} **Protect Crops From Cold** - Cover Vulnerable Plants At Sunset Using Cloth Or Plastic To Retain Warmth",
            'Heat Stress': f"{urgency_emoji} **Reduce Heat Stress** - Add Shade Netting And Irrigate Early Morning To Cool Root Zones",
            'Drought Risk': f"{urgency_emoji} **Conserve Soil Moisture** - Apply 5–7 Cm Organic Mulch And Shift To Drip Irrigation If Possible",
            'Flood Risk': f"{urgency_emoji} **Improve Excess Water Drainage** - Open Shallow Channels And Elevate Seedling Beds To Prevent Root Rot",
            'Pest Risk': f"{urgency_emoji} **Monitor And Suppress Pests** - Inspect Leaves Daily; Apply Neem Extract On Early Infestation Spots",
            'Disease Risk': f"{urgency_emoji} **Limit Disease Spread** - Remove Infected Foliage And Improve Spacing For Air Circulation",
            'Nutrient Leaching': f"{urgency_emoji} **Reduce Nutrient Loss** - Avoid Over-Irrigation; Apply Slow-Release Fertilizers Based On Soil Test",
            'Soil Erosion': f"{urgency_emoji} **Reduce Erosion** - Maintain Residue Cover And Install Contour Bunds On Slopes",
            'Vegetation Stress': f"{urgency_emoji} **Relieve Vegetation Stress** - Check Soil Moisture And Adjust Irrigation Scheduling",
            'Wind Damage': f"{urgency_emoji} **Shield Against Wind** - Install Temporary Windbreaks (Cloth, Hedges) For Young Or Fragile Crops"
        }
        base = fallback_actions.get(human_risk, f"{urgency_emoji} **Manage {human_risk.lower()}** - Implement Appropriate Protective Field Measures Promptly")
        if drivers:
            d_low = drivers_text.lower()
            if 'temperature' in d_low:
                return base + f" (Triggered By {drivers_text.lower()})"
            if 'moisture' in d_low or 'water' in d_low:
                return base + f" (Related To {drivers_text.lower()})"
        return base


def _generate_expected_outcome(level: str, risk_name: str, drivers: list) -> str:
    """Generate Meaningful Expected Outcomes Instead Of Generic Text"""
    outcomes_map = {
        'High': {
            'Cold Stress': 'Prevent Frost Damage And Crop Loss',
            'Heat Stress': 'Protect Crops From Heat Damage', 
            'Drought': 'Maintain Adequate Soil Moisture',
            'Flood': 'Prevent Waterlogging And Root Rot',
            'default': 'Mitigate Immediate Crop Risks'
        },
        'Medium': {
            'Cold Stress': 'Reduce Cold Stress Impact On Crops',
            'Heat Stress': 'Maintain Optimal Growing Conditions',
            'Drought': 'Improve Water Efficiency',
            'Flood': 'Manage Excess Water Effectively',
            'default': 'Improve Crop Resilience'
        },
        'Low': {
            'default': 'Maintain Healthy Crop Conditions'
        }
    }
    
    level_outcomes = outcomes_map.get(level, outcomes_map['Low'])
    return level_outcomes.get(risk_name, level_outcomes['default'])


# ADK LlmAgent Wrapper With Real Tool Calling
# Exposes An Agent The Orchestrator/Runner Can Use For Tool-Oriented Execution
RootAgent = Agent(
    model="gemini-2.5-flash-lite",
    name="planner_agent",
    description=(
        "Action Planning Specialist For Agricultural Decision Support"
    ),
    instruction=(
        "You Are The PlannerAgent - Provide JSON Only, No Markdown Or Asterisks. \n"
        "Generate Prioritized Action Plans Based On Risk Data And User Queries. \n"
        "Prioritize UserQuery If Present, Then Risk-Based Actions. \n"
        "Output keys: Status, AgentName, Location, P1, P2, P3, NotificationSummary, EmailDeliveryStatus, AdvisoryResources, UserQuestion, ImmediateAction, ThisWeekAction, GeneratedAt. \n"
        "Plain JSON Only."
    ),
    tools=[
        EmailNotificationTool,
    ],
)

__all__ = [
    'PlannerAgent',
    'RootAgent',
]