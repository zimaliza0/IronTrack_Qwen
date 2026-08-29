"""
AI Orchestrator for IronTrack
Routes requests to specialized agents with safety checks
"""

from typing import Dict, Any
import json

class AIOrchestrator:
    def __init__(self):
        self.safety_agent = SafetyAgent()
        self.training_agent = TrainingAgent()
        self.nutrition_agent = NutritionAgent()
    
    async def process_request(self, user_id: int, request_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # Step 1: Safety check
        safety_result = await self.safety_agent.check(data)
        
        if not safety_result["safe"]:
            return {
                "type": request_type,
                "recommendation": "⚠️ Request flagged for safety review. Please consult a professional.",
                "confidence": 0.0,
                "requires_human_approval": True
            }
        
        # Step 2: Route to specialized agent
        if request_type == "workout":
            response = await self.training_agent.generate_advice(user_id, data)
        elif request_type == "nutrition":
            response = await self.nutrition_agent.generate_advice(user_id, data)
        else:
            response = {"recommendation": "Unknown request type", "confidence": 0.0}
        
        # Step 3: Log for audit
        self._log_request(user_id, request_type, data, response)
        
        return response
    
    def _log_request(self, user_id: int, request_type: str, request_data: Dict, response: Dict):
        # Log to database for audit trail
        pass


class SafetyAgent:
    """Checks for dangerous recommendations"""
    
    async def check(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Check for extreme values
        dangerous_keywords = ["extreme", "dangerous", "harmful", "injury"]
        
        text_data = str(data).lower()
        for keyword in dangerous_keywords:
            if keyword in text_data:
                return {"safe": False, "reason": f"Contains dangerous keyword: {keyword}"}
        
        return {"safe": True}


class TrainingAgent:
    """Generates workout recommendations"""
    
    async def generate_advice(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder - will be enhanced with ML model
        return {
            "type": "workout",
            "recommendation": "💪 Based on your history, try 4 sets of 8-12 reps with progressive overload.",
            "confidence": 0.85,
            "requires_human_approval": False
        }


class NutritionAgent:
    """Generates nutrition recommendations"""
    
    async def generate_advice(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder - will be enhanced with ML model
        return {
            "type": "nutrition",
            "recommendation": "🥗 Aim for 1.6-2.2g protein per kg bodyweight for muscle gain.",
            "confidence": 0.90,
            "requires_human_approval": False
        }


# Example usage
if __name__ == "__main__":
    orchestrator = AIOrchestrator()
    import asyncio
    
    async def main():
        result = await orchestrator.process_request(
            user_id=1,
            request_type="workout",
            data={"exercise": "bench_press", "goal": "strength"}
        )
        print(json.dumps(result, indent=2))
    
    asyncio.run(main())
