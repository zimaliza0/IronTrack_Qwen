# Agent 2: Telegram Auth & Mobile UI Core

## Цель
Реализовать авторизацию через Telegram и адаптивный мобильный интерфейс Mini App.

## Telegram Integration

### Auth Flow
1. Mini App открывает WebView
2. Telegram передаёт initData с подписью
3. Backend валидирует подпись через Bot Token
4. Создаётся/обновляется пользователь
5. Возвращается JWT session

### initData структура
{
  "user": { "id": 123456789, "first_name": "John", "username": "johndoe" },
  "chat_instance": "...",
  "hash": "...",
  "auth_date": 1234567890
}

## Mobile UI Components

### Navigation
- Bottom tab bar (5 max items)
- Safe area insets для iPhone
- Gesture-based back navigation

### Key Screens

#### 1. Dashboard — Список активных клиентов, Quick search, фильтры
#### 2. Client Profile — Информация, цели, программа, графики
#### 3. Workout View — Карточки упражнений с подходами
#### 4. RIR Input — Tap buttons: 0 | 1 | 2 | 3 | 4 | 5+
#### 5. Weight Input — Свободный ввод + quick adjust ±1.25, ±2.5 кг
#### 6. Calendar — Недельный view, перенос тренировок, авто-создание
#### 7. Analytics Dashboard — Графики веса, e1RM, adherence

## Offline-First Architecture

### Local Storage (IndexedDB)
- workouts: Активные тренировки
- queue: Очередь синхронизации
- lastSync: Время последней синхронизации
- pendingMutations: Ожидающие мутации

### Sync Queue
interface SyncItem {
  id: string;
  type: 'workout' | 'log' | 'measurement';
  payload: object;
  timestamp: number;
  retryCount: number;
}

### Conflict Resolution
- Last-write-wins для простых полей
- Merge для сложных структур
- Manual review для критических конфликтов

## Design System

### Colors
- Background: #1A1A1A (графит)
- Surface: #242424
- Primary: #E53935 (красный акцент)
- Text: #FFFFFF / #B0B0B0

### Typography
- Headings: 20-24px, Body: 16px, Small: 14px
- Touch targets: min 44×44px

### iOS-Specific
- Safe area padding (notch, home indicator)
- Keyboard handling
- No horizontal overflow
- Haptic feedback

## Tech Stack
- Frontend: React + TypeScript
- State: Zustand / Jotai
- HTTP: TanStack Query
- Storage: Dexie.js
- Styling: Tailwind CSS
- Telegram SDK: @twa-dev/sdk

## Статус: READY FOR IMPLEMENTATION
