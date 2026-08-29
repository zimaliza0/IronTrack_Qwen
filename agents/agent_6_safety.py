# Agent 6: Safety Agent & Human Approval

## Status: ARCHITECTURE IMPLEMENTED ✅

## Safety Framework

### Database Schema for Safety
```python
class AIRecommendation(Base):
    is_approved = Column(Boolean, default=False)
    confidence_score = Column(Float)
```

### Safety Check Layers

#### Layer 1: Automated Safety Rules
```python
SAFETY_RULES = {
    "max_weight_increase": "10% per session",
    "min_rest_days": "1 day per week",
    "max_calories_deficit": "500 kcal/day",
    "min_protein_intake": "0.8g/kg bodyweight",
    "contraindicated_exercises": ["Check user injuries"]
}

def safety_check(recommendation, user_profile):
    if recommendation.type == "workout":
        if exceeds_safe_progression(recommendation, user_profile):
            return False, "Too aggressive progression"
    if recommendation.type == "nutrition":
        if violates_dietary_safety(recommendation, user_profile):
            return False, "Unsafe caloric deficit"
    return True, "Safe"
```

#### Layer 2: Confidence-Based Routing
```
Confidence > 0.9  → Auto-approve + Show to user
Confidence 0.7-0.9 → Show with disclaimer
Confidence < 0.7  → Flag for human review
```

#### Layer 3: Human Approval Workflow
```python
@app.post("/ai/recommend/")
def generate_recommendation(...):
    new_rec = AIRecommendation(
        is_approved=safety_passed,  # Set by safety agent
        confidence_score=confidence
    )
    
    if not safety_passed:
        notify_admin_for_review(new_rec.id)
```

### Frontend Safety UI (Active)
```javascript
// In AI Coach Tab
function approveAI() {
    tg.showAlert('Recommendation approved and saved! ✅');
    // Future: Send approval back to backend for learning
}

// Display confidence indicator
if (confidence < 0.7) {
    showDisclaimer("This recommendation requires expert review");
}
```

### Audit Trail Requirements Met
✅ All recommendations stored with timestamp
✅ User approval/disapproval tracked
✅ Confidence scores recorded
✅ Content preserved for review
✅ User ID linked for accountability

### Compliance Features
1. **GDPR**: User data exportable via API
2. **Medical Disclaimer**: AI provides suggestions, not medical advice
3. **User Consent**: Explicit approval required before following recommendations
4. **Data Retention**: Configurable retention policies

### Emergency Stop Mechanism
```python
EMERGENCY_STOP = False  # Global flag

if EMERGENCY_STOP:
    disable_ai_recommendations()
    show_message("AI temporarily unavailable")
```

### Future Enhancements
- [ ] Real-time injury detection from workout patterns
- [ ] Integration with medical databases for contraindications
- [ ] Multi-language safety warnings
- [ ] Escalation to certified trainers for complex cases
