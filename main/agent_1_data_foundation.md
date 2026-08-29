# Agent 1: Data Foundation & Backend API

## Цель
Спроектировать и реализовать структуру БД и REST API для хранения всех данных приложения.

## Ключевые сущности БД

### Trainer
- telegram_user_id (PK)
- display_name
- created_at

### Client
- id (PK)
- trainer_id (FK)
- telegram_user_id
- username
- display_name
- status (active/pause/inactive/archive)
- profile_data (JSONB)
- created_at

### Program
- id (PK)
- client_id (FK)
- name
- is_active
- is_template
- template_link (nullable FK)
- structure (JSONB: mesocycles → weeks → days → exercises → sets)

### Workout
- id (PK)
- program_id (FK)
- scheduled_date
- completed_at
- plan (JSONB)
- actual (JSONB)
- duration_seconds
- comments

### Exercise
- id (PK)
- name
- muscles (array)
- equipment (array)
- movement_type
- is_custom
- trainer_id (nullable FK)

### Set
- id (PK)
- workout_id (FK)
- exercise_id (FK)
- planned_weight
- actual_weight
- planned_reps
- actual_reps
- planned_rir
- actual_rir
- set_order

### NutritionLog
- id (PK)
- client_id (FK)
- date
- calories
- protein
- fat
- carbs
- adherence_notes

### Measurement
- id (PK)
- client_id (FK)
- date
- weight
- body_fat (optional)
- custom_metrics (JSONB)

### Goal
- id (PK)
- client_id (FK)
- name
- priority
- kpi_definitions (JSONB)
- target_value
- deadline
- status

### AuditLog
- id (PK)
- entity_type
- entity_id
- action
- old_value (JSONB)
- new_value (JSONB)
- actor_type (trainer/client/ai)
- actor_id
- timestamp

## REST API Endpoints

### Auth
- POST /api/auth/telegram — авторизация через Telegram WebApp

### Clients
- GET /api/clients — список клиентов с фильтрами
- GET /api/clients/:id — профиль клиента
- PUT /api/clients/:id — обновление профиля
- DELETE /api/clients/:id — удаление (soft delete → archive → basket)

### Programs
- GET /api/programs — программы клиента
- POST /api/programs — создание программы
- PUT /api/programs/:id — обновление
- POST /api/programs/:id/assign-template — назначение шаблона

### Workouts
- GET /api/workouts — тренировки
- POST /api/workouts — создание
- PUT /api/workouts/:id — обновление
- POST /api/workouts/:id/complete — завершение тренировки

### Analytics
- GET /api/analytics/client/:id — аналитика клиента
- GET /api/analytics/e1rm/:id — график e1RM
- GET /api/analytics/adherence/:id — приверженность

### AI Proposals
- GET /api/ai/proposals — pending рекомендации
- POST /api/ai/proposals/:id/approve — подтвердить
- POST /api/ai/proposals/:id/reject — отклонить

## Permission Layer
Все API запросы проходят через:
1. Authentication (Telegram JWT)
2. Authorization (trainer owns client)
3. Rate limiting
4. Input validation

## Offline Sync Queue
- Локальное хранилище тренировок
- Queue для отложенной синхронизации
- Защита от дублей (idempotency keys)
- Conflict resolution

## Статус: READY FOR IMPLEMENTATION
