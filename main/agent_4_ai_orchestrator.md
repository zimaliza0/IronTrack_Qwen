# Agent 4: AI Orchestrator & Tool Layer

## Цель
Реализовать главного координатора AI-агентов с системой инструментов и безопасным доступом к данным.

## Architecture
User Request → ORCHESTRATOR AGENT → TOOL LAYER → PERMISSION CHECK → PROPOSAL ENGINE → HUMAN APPROVAL UI

## Orchestrator Prompts

### System Prompt
Ты — главный координатор системы фитнес-тренировок.
Задача: классифицировать запрос, определить агентов, собрать ответы, проверить противоречия, сформировать рекомендацию.
Важно: не принимать решения самостоятельно, указывать confidence (0-1), предложения должны быть actionable.

## Tool Definitions

### get_client_context(client_id)
Получить полную информацию о клиенте: profile, goals, constraints, current_program, equipment

### get_training_history(client_id, days=30)
История тренировок: workouts, avg_volume, avg_rir, e1rm_trend

### get_nutrition_data(client_id, days=14)
Данные питания: avg_calories, avg_macros, adherence, data_quality, weigh_ins

### check_constraints(client_id, exercise)
Проверить ограничения: has_conflict, conflicts[], alternatives[]

## Structured Output Format
{
  "intent": "progression_recommendation",
  "agents_used": ["training", "nutrition", "client_context"],
  "confidence": 0.78,
  "data_quality": {"training": "high", "nutrition": "medium"},
  "findings": [{"source": "training_agent", "statement": "...", "evidence": [...]}],
  "recommendations": [{"action": "reduce_volume", "details": "...", "requires_approval": true}],
  "warnings": ["Недостаточно данных питания"]
}

## Intent Classification
| Intent Pattern | Agents to Call |
|---------------|----------------|
| почему падает сила | training, nutrition, recovery |
| как изменить программу | training, client_context, safety |
| скорректировать питание | nutrition, measurements, goals |
| готов ли к deload | training, recovery, analytics |
| конфликт целей | client_context, goals, training |

## Confidence Scoring
def calculate_confidence(data_quality, sample_size, consistency):
    base = sum(data_quality.values()) / len(data_quality)
    size_factor = min(sample_size / 30, 1.0) * 0.3
    consistency_factor = consistency * 0.2
    return min(base * 0.5 + size_factor + consistency_factor, 1.0)

## Proposal Queue API
GET /api/ai/proposals?status=pending
POST /api/ai/proposals/:id/approve
POST /api/ai/proposals/:id/reject
GET /api/ai/proposals/:id/explanation

## Статус: READY FOR IMPLEMENTATION
