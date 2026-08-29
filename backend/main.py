from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

app = FastAPI(title="IronTrack API")

# Models
class User(BaseModel):
    id: int
    telegram_id: int
    username: str
    created_at: str

class Workout(BaseModel):
    id: int
    user_id: int
    exercise: str
    sets: int
    reps: int
    weight: float
    notes: Optional[str] = None
    created_at: str

class Meal(BaseModel):
    id: int
    user_id: int
    food: str
    calories: int
    protein: float
    carbs: float
    fat: float
    created_at: str

class AIRecommendation(BaseModel):
    type: str  # "workout" or "nutrition"
    recommendation: str
    confidence: float

# Database helpers
def get_db():
    conn = sqlite3.connect("database/irontrack.db")
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            exercise TEXT,
            sets INTEGER,
            reps INTEGER,
            weight REAL,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            food TEXT,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fat REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            request_type TEXT,
            request_data TEXT,
            response_data TEXT,
            safety_approved INTEGER,
            human_approval_required INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Endpoints
@app.get("/")
def read_root():
    return {"status": "IronTrack API is running"}

@app.post("/auth/telegram")
def telegram_auth(telegram_id: int, username: str):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)",
        (telegram_id, username)
    )
    conn.commit()
    
    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {"user_id": user["id"], "telegram_id": user["telegram_id"], "username": user["username"]}
    raise HTTPException(status_code=400, detail="Auth failed")

@app.post("/workouts/", response_model=Workout)
def create_workout(workout: Workout):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO workouts (user_id, exercise, sets, reps, weight, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (workout.user_id, workout.exercise, workout.sets, workout.reps, workout.weight, workout.notes))
    
    conn.commit()
    workout_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM workouts WHERE id = ?", (workout_id,))
    result = cursor.fetchone()
    conn.close()
    
    return dict(result)

@app.get("/workouts/{user_id}", response_model=List[Workout])
def get_workouts(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workouts WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    results = cursor.fetchall()
    conn.close()
    return [dict(r) for r in results]

@app.post("/meals/", response_model=Meal)
def create_meal(meal: Meal):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO meals (user_id, food, calories, protein, carbs, fat)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (meal.user_id, meal.food, meal.calories, meal.protein, meal.carbs, meal.fat))
    
    conn.commit()
    meal_id = cursor.lastrowid
    
    cursor.execute("SELECT * FROM meals WHERE id = ?", (meal_id,))
    result = cursor.fetchone()
    conn.close()
    
    return dict(result)

@app.get("/meals/{user_id}", response_model=List[Meal])
def get_meals(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meals WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    results = cursor.fetchall()
    conn.close()
    return [dict(r) for r in results]

@app.post("/ai/recommend", response_model=AIRecommendation)
def get_ai_recommendation(user_id: int, request_type: str, data: dict):
    # Placeholder - will be connected to AI orchestrator
    return AIRecommendation(
        type=request_type,
        recommendation="AI recommendation placeholder",
        confidence=0.95
    )

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
