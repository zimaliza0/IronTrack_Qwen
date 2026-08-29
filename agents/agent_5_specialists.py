# Agent 5: Specialized Agents (Training + Nutrition)

## Status: FRAMEWORK READY ✅

## Specialist Agents Architecture

### Training Agent
**Purpose**: Generate personalized workout recommendations

**Input Data**:
- User's workout history
- Current fitness level
- Available equipment
- Goals (strength, hypertrophy, endurance)
- Recovery status

**Output Format**:
```json
{
    "type": "workout",
    "recommendation": "Add 2.5kg to your bench press this session",
    "confidence": 0.92,
    "reasoning": "Based on 3 successful sessions at current weight"
}
```

**Implementation Points**:
```python
def training_recommendation(user_id):
    workouts = get_user_workouts(user_id)
    # Analyze progressive overload
    # Check volume/frequency
    # Suggest adjustments
    return recommendation
```

### Nutrition Agent
**Purpose**: Provide meal and macro guidance

**Input Data**:
- Daily calorie intake
- Macro breakdown
- Meal timing
- User goals (cut, bulk, maintain)
- Dietary restrictions

**Output Format**:
```json
{
    "type": "nutrition",
    "recommendation": "Increase protein by 30g daily",
    "confidence": 0.88,
    "reasoning": "Current intake 1.2g/kg, goal is 1.8g/kg for muscle gain"
}
```

**Implementation Points**:
```python
def nutrition_recommendation(user_id):
    logs = get_nutrition_logs(user_id)
    # Calculate average macros
    # Compare to goals
    # Suggest adjustments
    return recommendation
```

### Frontend Integration (Active)
```javascript
// AI Coach Tab in frontend/index.html
function getAIRecommendation() {
    // Simulated AI responses (ready for real backend integration)
    const recommendations = [
        "Based on your recent workouts, consider adding a rest day...",
        "Your protein intake seems low. Try adding Greek yogurt...",
        "Great progress on strength training! Consider increasing weights...",
        "Don't forget to stretch after workouts...",
        "Hydration tip: Drink 500ml water 2 hours before..."
    ];
}
```

### Data Flow
```
User → Frontend → API /ai/recommend/ → Orchestrator → 
Specialist Agent → Tool Execution → Safety Check → Response
```

### Ready for Enhancement
1. Connect to real AI models
2. Implement user feedback loop
3. Add personalization based on history
4. Create A/B testing for recommendation effectiveness
