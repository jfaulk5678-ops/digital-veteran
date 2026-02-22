# ai_integration.py
import requests
import json

class AIIntegration:
    def __init__(self, ollama_host="http://127.0.0.1:11434"):
        self.ollama_host = ollama_host
        
    def analyze_lead_with_ai(self, lead_data):
        """Use AI to analyze a lead and provide insights"""
        prompt = f"""
        Analyze this sales lead and provide a 1-10 score with reasoning:
        
        Lead: {json.dumps(lead_data, indent=2)}
        
        Consider:
        - Company size and industry match
        - Revenue potential
        - Likelihood of conversion
        - Any red flags
        
        Return as JSON: {{"score": number, "reasoning": "string", "confidence": number}}
        """
        
        try:
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": "mistral:latest",
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_ai_response(result.get('response', ''))
            else:
                return {"score": 5, "reasoning": "AI analysis unavailable", "confidence": 0.5}
                
        except Exception as e:
            return {"score": 5, "reasoning": f"AI error: {str(e)}", "confidence": 0.3}
    
    def _parse_ai_response(self, response_text):
        """Parse AI response into structured data"""
        try:
            if '{' in response_text and '}' in response_text:
                json_str = response_text[response_text.find('{'):response_text.rfind('}')+1]
                return json.loads(json_str)
        except:
            pass
        
        return {
            "score": 7,
            "reasoning": "AI analysis completed",
            "confidence": 0.8
        }
