import json
import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def extract_needs(raw_text: str, location: str) -> list:
    prompt = f"""
    You are an emergency needs analyzer for an NGO 
    coordination system in Mumbai, India.
    
    Analyze this raw community survey report and extract 
    all distinct needs. 
    Return ONLY a valid JSON array.
    No markdown. No backticks. No explanation. Just JSON.
    
    Location context: {location}
    Raw report: "{raw_text}"
    
    Return this exact format:
    [
      {{
        "urgency": "critical",
        "category": "medical",
        "description": "Clear one line description",
        "skills_required": ["Medical", "First Aid"],
        "estimated_people_affected": 5
      }}
    ]
    
    Urgency rules:
    - critical: immediate threat to life
    - high: serious problem within 24 hours
    - medium: important but not immediately dangerous
    - low: can wait a few days
    
    Categories: food, medical, shelter, 
                transport, education, other
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    text = response.text.strip()
    # Strip markdown if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)

def match_volunteer(need: dict, volunteers: list) -> dict:
    prompt = f"""
    You are a volunteer matching AI for an NGO 
    coordination platform in Mumbai, India.
    
    Match the best volunteer for this community need.
    Return ONLY valid JSON. No markdown. No explanation.
    
    Community need:
    {json.dumps(need, indent=2)}
    
    Available volunteers:
    {json.dumps(volunteers, indent=2)}
    
    Return this exact format:
    {{
      "volunteer_id": "exact_id_from_list",
      "match_score": 85,
      "reason": "Two sentence explanation of why this volunteer is the best match.",
      "urgency_flag": true
    }}
    
    Match based on: skills alignment first, 
    then location proximity, then availability.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)

def get_dashboard_summary(needs: list) -> dict:
    prompt = f"""
    You are summarizing active community needs for 
    an NGO coordinator dashboard in Mumbai.
    
    Return ONLY valid JSON. No markdown. No explanation.
    
    Active needs data:
    {json.dumps(needs, indent=2)}
    
    Return this exact format:
    {{
      "critical_count": 2,
      "high_count": 3,
      "top_priority_need": "One sentence about most urgent need",
      "recommended_action": "What coordinator should do right now",
      "areas_most_affected": ["Dharavi", "Govandi"],
      "total_people_affected": 150
    }}
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)
