# Agent 3: Analytics Engine & Audit Trail

## Цель
Создать движок расчёта метрик и систему аудита всех изменений в приложении.

## KPI Calculations

### e1RM (Estimated 1 Rep Max)
Формула Epley: e1RM = weight × (1 + reps / 30)
RIR-коррекция: e1RM_adjusted = e1RM × (1 + (3 - actual_rir) × 0.05)

### Volume Load
Volume = Σ(weight × reps × sets)

### Progression Metrics
- Rep progression: план vs факт повторов
- Load progression: изменение рабочего веса
- Volume progression: недельный объём
- RIR trend: средняя утомляемость

### Adherence Score
Adherence = (completed_workouts / planned_workouts) × 100%
Nutrition adherence = (logged_days / total_days) × 100%

### Deload Signals — Алгоритм обнаружения
1. RIR падает на 2+ пункта при том же весе
2. e1RM снижается 2+ недели подряд
3. Session RPE растёт при снижении нагрузки
4. Восстановление < 6/10 более 5 дней
5. Пропуск 2+ тренировок подряд

## Audit Trail System

### Что логируется
| Entity | Actions | Fields Tracked |
|--------|---------|----------------|
| Client | create, update, delete, archive | all fields |
| Program | create, update, assign | structure, status |
| Workout | create, complete, modify | plan, actual, RIR, weight |
| Set | create, update | weight, reps, rir |
| Nutrition | log, update | calories, macros |
| Goal | create, update, complete | kpi, status |
| AI Proposal | create, approve, reject | recommendation, decision |

### Структура AuditLog
{
  "id": "uuid",
  "entity_type": "workout",
  "entity_id": "123",
  "action": "update_set",
  "old_value": {"weight": 80, "reps": 8, "rir": 2},
  "new_value": {"weight": 82.5, "reps": 8, "rir": 1},
  "actor_type": "client",
  "actor_id": "456",
  "timestamp": "2024-01-15T10:30:00Z"
}

### История параметра
GET /api/audit/:entity/:id/:field/history

## Graphs & Visualizations

### Weight Trend
- 7-day rolling average
- 14-day trend line
- 28-day comparison
- Target rate overlay (%/week)

### e1RM Progression
- По упражнениям
- Сравнение мезоциклов
- PR markers (новый лучший e1RM)

### Volume Chart
- Недельный объём по группам мышц

## Backup & Export

### Export Formats
- CSV: клиенты, тренировки, питание
- Excel: сводные отчёты с графиками
- PDF: клиентские отчёты

### Backup Strategy
- Автоматический daily backup БД
- Ручной trigger backup
- Export单个 клиента по запросу
- Восстановление из корзины (30 дней)

## Implementation

### Database Views
CREATE VIEW client_analytics AS
SELECT c.id, COUNT(DISTINCT w.id) as total_workouts,
       AVG(s.actual_rir) as avg_rir, MAX(e1rm_calculated) as peak_e1rm
FROM clients c JOIN workouts w ON w.client_id = c.id
JOIN sets s ON s.workout_id = w.id GROUP BY c.id;

### Aggregation Jobs
- Ежедневный пересчёт метрик
- Кэширование результатов (Redis)
- Invalidate cache при изменении данных

## Статус: READY FOR IMPLEMENTATION
