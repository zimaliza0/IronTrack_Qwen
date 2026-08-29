# IronTrack - AI-Powered Fitness Tracker for Telegram

## Overview
IronTrack is a Telegram Mini App that helps users track workouts, nutrition, and get AI-powered fitness recommendations.

## Features
- 🏋️ Workout tracking with exercise library
- 🥗 Nutrition logging with macro tracking
- 🤖 AI Coach for personalized recommendations
- ✅ Safety checks on all AI advice
- 📊 Progress analytics

## Tech Stack
- **Backend**: Python FastAPI
- **Frontend**: HTML/CSS/JS (Telegram Mini App)
- **Database**: SQLite (upgradeable to PostgreSQL)
- **AI**: Custom orchestrator with specialized agents

## Project Structure
```
/workspace
├── backend/          # FastAPI server
│   └── main.py
├── frontend/         # Telegram Mini App
│   └── index.html
├── database/         # DB initialization
│   └── init_db.py
├── ai_agents/        # AI orchestrator
│   └── orchestrator.py
├── main/             # Agent specifications
├── tests/            # Test files
├── docs/             # Documentation
├── plan.md           # Development plan
└── README.md         # This file
```

## Quick Start

### 1. Initialize Database
```bash
python database/init_db.py
```

### 2. Run Backend
```bash
cd backend
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Deploy Frontend
Host `frontend/index.html` on any static hosting and set the URL in your Telegram Bot settings.

## API Endpoints
- `GET /` - Health check
- `POST /auth/telegram` - Telegram authentication
- `POST /workouts/` - Add workout
- `GET /workouts/{user_id}` - Get user workouts
- `POST /meals/` - Add meal
- `GET /meals/{user_id}` - Get user meals
- `POST /ai/recommend` - Get AI recommendation

## Development Plan
See `plan.md` for the 6-point development roadmap.

## License
MIT
