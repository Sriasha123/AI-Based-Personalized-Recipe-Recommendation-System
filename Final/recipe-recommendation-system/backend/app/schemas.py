# backend/app/schemas.py
# Updated to handle all personalization fields

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    age: Optional[int] = None
    dietary_type: Optional[str] = None
    health_conditions: Optional[List[str]] = []
    allergies: Optional[List[str]] = []  # NEW
    preferred_cuisines: Optional[List[str]] = []  # NEW

class UserProfile(BaseModel):
    id: int
    email: str
    full_name: str
    age: Optional[int]
    dietary_type: Optional[str]
    health_conditions: Optional[List[str]]
    allergies: Optional[List[str]] = []  # NEW
    preferred_cuisines: Optional[List[str]] = []  # NEW
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class RecipeDetail(BaseModel):
    id: int
    recipe_id: int
    name: str
    minutes: Optional[int]
    tags: Optional[List[str]]
    nutrition: Dict[str, float]
    ingredients: Optional[List[str]]
    description: Optional[str]
    cuisine: Optional[str]
    steps: List[str]
  
    n_steps: Optional[int]
    n_ingredients: Optional[int]
    dietary_tags: Optional[List[str]]
    allergens: Optional[List[str]]
    
    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    recipe_id: int
    rating: float
    review_text: Optional[str] = ""

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    recipe_id: int
    rating: float
    review_text: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class MealPlanCreate(BaseModel):
    week_start_date: datetime
    dietary_goal: Optional[str] = "balanced"
    target_calories: Optional[int] = 2000

class MealPlanResponse(BaseModel):
    id: int
    week_start_date: datetime
    meals: Dict
    total_calories: float
    created_at: datetime
    
    class Config:
        from_attributes = True