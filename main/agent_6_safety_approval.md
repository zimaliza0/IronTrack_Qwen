# Agent 6: Safety Agent & Human Approval Flow

## Цель
Реализовать агента проверки ограничений и интерфейс подтверждения рекомендаций тренером.

---

## Safety & Constraint Agent

### Зона ответственности
- Проверка конфликта с ограничениями клиента
- Валидация нелогичных изменений
- Обнаружение потенциально рискованных рекомендаций
- Проверка достаточности данных
- Выявление противоречий между агентами

### Не является медицинским диагностом!
Агент НЕ ставит диагнозы, только предупреждает о конфликтах.

### Constraint Checking
def check_exercise_constraint(exercise, client_constraints):
    conflicts = []
    for constraint in client_constraints:
        if constraint.type == "injury" and exercise.body_part in constraint.affected_areas:
            conflicts.append({"type": "injury_conflict", "severity": "high"})
        elif constraint.type == "equipment_missing" and exercise.equipment not in available:
            conflicts.append({"type": "equipment_missing", "severity": "medium"})
    return {"has_conflict": len(conflicts) > 0, "conflicts": conflicts, "alternatives": [...]}

### Sanity Checks
def sanity_check_proposal(proposal, client_data):
    warnings = []
    # Check 1: Слишком большое изменение веса
    if proposal.type == "weight_change" and abs(proposal.change_percent) > 10:
        warnings.append({"type": "large_change", "severity": "high"})
    # Check 2: Недостаточно данных
    if proposal.confidence < 0.5:
        warnings.append({"type": "low_confidence", "severity": "medium"})
    # Check 3: Конфликт с целью
    if proposal.action == "increase_calories" and client_data.goal == "fat_loss":
        warnings.append({"type": "goal_conflict", "severity": "high"})
    return {"is_safe": len([w for w in warnings if w.severity == "critical"]) == 0, "warnings": warnings}

### Inter-Agent Conflict Detection
def detect_agent_conflicts(agent_outputs):
    conflicts = []
    training = agent_outputs.get("training_agent")
    nutrition = agent_outputs.get("nutrition_agent")
    # Training советует увеличить нагрузку, но Nutrition показывает большой дефицит
    if training and nutrition and training.recommendation == "increase_intensity":
        if nutrition.calorie_deficit > 500:
            conflicts.append({"issue": "Увеличение интенсивности при дефиците калорий"})
    return conflicts

### Выходные данные
{
  "agent": "safety_agent",
  "constraint_check": {"has_conflicts": true, "conflicts": [...], "alternatives": [...]},
  "sanity_check": {"is_safe": true, "warnings": [...]},
  "inter_agent_conflicts": [],
  "final_verdict": "proceed_with_caution",
  "required_approvals": ["trainer"]
}

---

## Human Approval Flow

### Proposal Lifecycle
CREATED (by AI) → PENDING (awaiting trainer) → APPROVED (ready to execute) → EXECUTED
                                           ↓
                                    REJECTED (with note)

### Proposal UI Card
┌─────────────────────────────────────────┐
│ 🤖 AI Рекомендация                      │
│ Клиент: Иван Петров                     │
│ Тип: Коррекция программы                │
│ Уверенность: ████████░░ 78%             │
├─────────────────────────────────────────┤
│ 📋 Обоснование:                         │
│ • RIR упал с 2 до 0.5 за 2 недели       │
│ • e1RM снизился на 3%                   │
├─────────────────────────────────────────┤
│ 💡 Рекомендация:                        │
│ Снизить объём на 40% на 1 неделю        │
├─────────────────────────────────────────┤
│ [✓ Принять]  [✗ Отклонить]              │
│ Комментарий: [___________________]      │
└─────────────────────────────────────────┘

### API Endpoints
GET    /api/proposals              # Список pending proposals
GET    /api/proposals/:id          # Детали proposal
POST   /api/proposals/:id/approve  # Принять
POST   /api/proposals/:id/reject   # Отклонить
GET    /api/proposals/stats        # Статистика

### Approval Payload
// Approve
{"proposal_id": "uuid", "decision": "approve", "comment": "...", "modifications": null}

// Reject
{"proposal_id": "uuid", "decision": "reject", "comment": "...", "feedback_category": "timing_issue"}

### Execution After Approval
async def execute_proposal(proposal_id, approved_by):
    proposal = await db.proposals.get(proposal_id)
    if proposal.status != "approved": raise ValueError("Not approved")
    if proposal.type == "program_change":
        await update_program(proposal.client_id, proposal.changes)
    await audit_log.create({"entity_type": "proposal", "action": "executed", "actor_id": f"ai_approved_by_{approved_by}"})

### Feedback Loop
Отклонённые предложения для fine-tuning:
{"proposal_id": "uuid", "was_correct": false, "feedback_category": "timing_issue", "used_for_training": true}

## Статус: READY FOR IMPLEMENTATION
