# Agent 5: Specialized AI Agents (Training + Nutrition)

## Цель
Реализовать специализированных агентов для анализа тренировок и питания.

---

## Training Scientist Agent

### Зона ответственности
- Анализ RIR/RPE, e1RM динамика
- Объём и интенсивность, прогрессия нагрузок
- Deload signals, Exercise selection
- Альтернативы упражнений, периодизация

### Анализ

#### 1. RIR Compliance
def analyze_rir_compliance(workouts, target_rir):
    avg_rir = mean([s.actual_rir for w in workouts for s in w.sets])
    if avg_rir < target_rir - 1: return "overreaching"
    elif avg_rir > target_rir + 1: return "undereffort"
    return "on_track"

#### 2. e1RM Trend
def analyze_e1rm_trend(exercise_history):
    recent = exercise_history[-4:]
    trend = linear_regression(recent.e1rm_values)
    if trend.slope > 0.02: return "progressing"
    elif trend.slope < -0.02: return "declining"
    return "stalled"

#### 3. Progression Recommendation
def recommend_progression(last_workout, target_rir):
    if all(s.actual_reps >= s.planned_reps_max and s.actual_rir >= target_rir - 0.5 for s in sets):
        return {"action": "increase_weight", "amount": 2.5}
    avg_rir = mean([s.actual_rir for s in sets])
    if avg_rir < 1: return {"action": "maintain_or_reduce"}
    return {"action": "maintain"}

### Выходные данные
{
  "agent": "training_scientist",
  "analysis": {"rir_status": "overreaching", "e1rm_trend": "stalled", "deload_recommended": true},
  "recommendations": [{"type": "deload", "details": "Снизить объём на 40% на 1 неделю", "confidence": 0.82}]
}

---

## Nutrition Analyst Agent

### Зона ответственности
- Калории и макросы, Adherence к плану
- Динамика веса (7/14/28 дней)
- Качество данных, Корректировка КБЖУ

### Data Quality Assessment
def assess_data_quality(nutrition_logs, weigh_ins, window_days=7):
    logged_days = count_unique_days(nutrition_logs)
    data_score = {"nutrition": logged_days/window_days, "weigh_ins": min(len(weigh_ins)/2, 1.0)}
    avg_score = mean(data_score.values())
    if avg_score < 0.5: return "low"
    elif avg_score < 0.8: return "medium"
    return "high"

### Weight Trend Analysis
def analyze_weight_trend(weigh_ins, window='14d'):
    recent = filter_by_window(weigh_ins, window)
    trend = linear_regression(recent.weights)
    weekly_rate = trend.slope * 7
    percent_rate = (weekly_rate / recent.avg_weight) * 100
    return {"weekly_change_percent": percent_rate, "trend": "losing" if weekly_rate < 0 else "gaining"}

### Calorie Adjustment Logic
def recommend_calorie_adjustment(current_calories, weight_trend, goal):
    target_rate = get_target_rate(goal)  # -0.5%/week для сушки
    diff = weight_trend.weekly_change_percent - target_rate
    if abs(diff) < 0.2: return {"decision": "maintain"}
    adjustment = clamp(int((diff / 0.1) * 100), -300, 300)
    return {"decision": "adjust", "new_calories": current_calories + adjustment}

### Macro Adjustment Options
def generate_macro_options(calorie_change, current_macros):
    return [
        {"name": "Изменить углеводы", "carbs": current_macros.carbs + calorie_change // 4},
        {"name": "Углеводы + жиры", "carbs": current_macros.carbs + (calorie_change//4)//2, "fat": current_macros.fat + (calorie_change//9)//2},
        {"name": "Добавить кардио", "action": "add_cardio", "details": "+20 мин LISS 3x/нед"}
    ]

### Выходные данные
{
  "agent": "nutrition_analyst",
  "data_quality": {"score": "medium", "warning": "Мало данных питания"},
  "weight_analysis": {"14day_trend": "-0.4%/week"},
  "recommendations": [{"type": "calorie_adjustment", "options": [...], "confidence": 0.71}]
}

---

## Integration with Orchestrator
Оба агента возвращают данные в едином формате для агрегации Orchestrator'ом.

## Статус: READY FOR IMPLEMENTATION
