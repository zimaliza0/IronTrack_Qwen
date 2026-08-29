from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from database import SessionLocal, User, Workout, Exercise, NutritionLog, Measurement, AIRecommendation, init_db

app = FastAPI(title="IronTrack API", description="Fitness tracking backend with AI recommendations")

# CORS for Telegram Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    telegram_id: str
    username: Optional[str] = None
    full_name: str

class UserResponse(BaseModel):
    id: int
    telegram_id: str
    username: Optional[str]
    full_name: str
    created_at: datetime
    class Config:
        from_attributes = True

class ExerciseCreate(BaseModel):
    name: str
    sets: int
    reps: int
    weight_kg: Optional[float] = None
    duration_seconds: Optional[int] = None

class WorkoutCreate(BaseModel):
    workout_type: str
    duration_minutes: int
    calories_burned: int
    notes: Optional[str] = None
    exercises: List[ExerciseCreate] = []

class WorkoutResponse(BaseModel):
    id: int
    user_id: int
    date: datetime
    workout_type: str
    duration_minutes: int
    calories_burned: int
    notes: Optional[str]
    class Config:
        from_attributes = True

class NutritionLogCreate(BaseModel):
    meal_type: str
    food_name: str
    calories: int
    protein_g: float
    carbs_g: float
    fats_g: float

class MeasurementCreate(BaseModel):
    weight_kg: float
    body_fat_percent: Optional[float] = None
    muscle_mass_kg: Optional[float] = None
    waist_cm: Optional[float] = None
    chest_cm: Optional[float] = None
    arms_cm: Optional[float] = None

class AIRecommendationCreate(BaseModel):
    recommendation_type: str
    content: str
    confidence_score: float

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.telegram_id == user.telegram_id).first()
    if db_user:
        return db_user
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/workouts/", response_model=WorkoutResponse)
def create_workout(workout: WorkoutCreate, user_id: int, db: Session = Depends(get_db)):
    new_workout = Workout(
        user_id=user_id,
        workout_type=workout.workout_type,
        duration_minutes=workout.duration_minutes,
        calories_burned=workout.calories_burned,
        notes=workout.notes
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    
    for ex in workout.exercises:
        exercise = Exercise(workout_id=new_workout.id, **ex.model_dump())
        db.add(exercise)
    db.commit()
    return new_workout

@app.get("/workouts/user/{user_id}", response_model=List[WorkoutResponse])
def get_user_workouts(user_id: int, db: Session = Depends(get_db)):
    workouts = db.query(Workout).filter(Workout.user_id == user_id).order_by(Workout.date.desc()).all()
    return workouts

@app.post("/nutrition/", response_model=dict)
def log_nutrition(log: NutritionLogCreate, user_id: int, db: Session = Depends(get_db)):
    new_log = NutritionLog(user_id=user_id, **log.model_dump())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return {"status": "success", "id": new_log.id}

@app.post("/measurements/", response_model=dict)
def add_measurement(measurement: MeasurementCreate, user_id: int, db: Session = Depends(get_db)):
    new_measurement = Measurement(user_id=user_id, **measurement.model_dump())
    db.add(new_measurement)
    db.commit()
    db.refresh(new_measurement)
    return {"status": "success", "id": new_measurement.id}

@app.post("/ai/recommend/", response_model=dict)
def generate_recommendation(rec: AIRecommendationCreate, user_id: int, db: Session = Depends(get_db)):
    new_rec = AIRecommendation(
        user_id=user_id,
        recommendation_type=rec.recommendation_type,
        content=rec.content,
        confidence_score=rec.confidence_score,
        is_approved=True
    )
    db.add(new_rec)
    db.commit()
    db.refresh(new_rec)
    return {"status": "success", "recommendation_id": new_rec.id}

@app.get("/stats/{user_id}")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    total_workouts = db.query(Workout).filter(Workout.user_id == user_id).count()
    latest_measurement = db.query(Measurement).filter(Measurement.user_id == user_id).order_by(Measurement.date.desc()).first()
    return {
        "total_workouts": total_workouts,
        "current_weight": latest_measurement.weight_kg if latest_measurement else None,
        "last_updated": datetime.utcnow()
    }

@app.get("/")
def root():
    return {"message": "IronTrack API is running!", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
