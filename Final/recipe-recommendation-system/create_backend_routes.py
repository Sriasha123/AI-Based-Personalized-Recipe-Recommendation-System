"""
Create All Backend Route Files
Save as: create_backend_routes.py
Run from: Desktop/Final/recipe-recommendation-system/
"""

import os

files = {
    "backend/app/auth/password_utils.py": """from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
""",

    "backend/app/auth/jwt_handler.py": """from datetime import datetime, timedelta
from jose import JWTError, jwt
from ..config import settings

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
""",

    "backend/app/auth/routes.py": """from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, Token, UserProfile
from .password_utils import hash_password, verify_password
from .jwt_handler import create_access_token, verify_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

@router.post("/signup", response_model=UserProfile)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
        age=user.age,
        dietary_type=user.dietary_type,
        health_conditions=user.health_conditions
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
""",

    "backend/app/recipes/routes.py": """from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from ..database import get_db
from ..models import Recipe
from ..schemas import RecipeDetail

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/search", response_model=List[RecipeDetail])
def search_recipes(
    query: Optional[str] = None,
    cuisine: Optional[str] = None,
    max_calories: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    filters = []
    if query:
        filters.append(or_(
            Recipe.name.ilike(f"%{query}%"),
            Recipe.description.ilike(f"%{query}%")
        ))
    if cuisine:
        filters.append(Recipe.cuisine == cuisine)
    
    q = db.query(Recipe)
    if filters:
        q = q.filter(and_(*filters))
    
    recipes = q.offset(skip).limit(limit).all()
    
    if max_calories:
        recipes = [r for r in recipes if r.nutrition and r.nutrition[0] <= max_calories]
    
    return recipes

@router.get("/{recipe_id}", response_model=RecipeDetail)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
""",

    "backend/app/reviews/routes.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Review, Recipe, User
from ..schemas import ReviewCreate, ReviewResponse
from ..auth.routes import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewResponse)
def create_review(
    review: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == review.recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    new_review = Review(
        user_id=current_user.id,
        recipe_id=recipe.id,
        rating=review.rating,
        review_text=review.review_text
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/recipe/{recipe_id}", response_model=List[ReviewResponse])
def get_recipe_reviews(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    reviews = db.query(Review).filter(Review.recipe_id == recipe.id).all()
    return reviews
""",

    "backend/app/recommendations/routes.py": """from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Recipe, User
from ..schemas import RecipeDetail
from ..auth.routes import get_current_user
import random

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/", response_model=List[RecipeDetail])
def get_recommendations(
    cuisine: Optional[str] = None,
    max_calories: Optional[int] = None,
    n_recommendations: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    q = db.query(Recipe)
    
    if cuisine:
        q = q.filter(Recipe.cuisine == cuisine)
    
    recipes = q.limit(100).all()
    
    if max_calories:
        recipes = [r for r in recipes if r.nutrition and r.nutrition[0] <= max_calories]
    
    return random.sample(recipes, min(n_recommendations, len(recipes)))

@router.get("/personalized", response_model=List[RecipeDetail])
def get_personalized_recommendations(
    current_user: User = Depends(get_current_user),
    n_recommendations: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    q = db.query(Recipe)
    
    if current_user.dietary_type:
        q = q.filter(Recipe.dietary_tags.contains([current_user.dietary_type]))
    
    recipes = q.limit(n_recommendations).all()
    return recipes

@router.get("/similar/{recipe_id}", response_model=List[RecipeDetail])
def get_similar_recipes(
    recipe_id: int,
    n_recommendations: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        return []
    
    similar = db.query(Recipe).filter(
        Recipe.cuisine == recipe.cuisine,
        Recipe.recipe_id != recipe_id
    ).limit(n_recommendations).all()
    
    return similar
""",

    "backend/app/meal_planner/routes.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models import User, MealPlan, Recipe
from ..schemas import MealPlanCreate, MealPlanResponse
from ..auth.routes import get_current_user
import random

router = APIRouter(prefix="/meal-planner", tags=["Meal Planning"])

@router.post("/generate", response_model=MealPlanResponse)
def generate_meal_plan(
    plan: MealPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recipes = db.query(Recipe).limit(100).all()
    
    if len(recipes) < 21:
        raise HTTPException(status_code=400, detail="Not enough recipes available")
    
    weekly_plan = {}
    total_calories = 0
    
    for day in range(7):
        date = plan.week_start_date + timedelta(days=day)
        selected = random.sample(recipes, min(3, len(recipes)))
        
        day_calories = sum([r.nutrition[0] if r.nutrition else 0 for r in selected])
        total_calories += day_calories
        
        weekly_plan[date.strftime("%A")] = {
            "date": date.strftime("%Y-%m-%d"),
            "meals": {
                "breakfast": {
                    "recipe_id": selected[0].recipe_id,
                    "name": selected[0].name,
                    "calories": selected[0].nutrition[0] if selected[0].nutrition else 0
                },
                "lunch": {
                    "recipe_id": selected[1].recipe_id,
                    "name": selected[1].name,
                    "calories": selected[1].nutrition[0] if selected[1].nutrition else 0
                },
                "dinner": {
                    "recipe_id": selected[2].recipe_id,
                    "name": selected[2].name,
                    "calories": selected[2].nutrition[0] if selected[2].nutrition else 0
                }
            },
            "total_calories": day_calories
        }
    
    meal_plan = MealPlan(
        user_id=current_user.id,
        week_start_date=plan.week_start_date,
        meals=weekly_plan,
        total_calories=total_calories
    )
    
    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)
    return meal_plan

@router.get("/plans", response_model=List[MealPlanResponse])
def get_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(MealPlan).filter(
        MealPlan.user_id == current_user.id
    ).order_by(MealPlan.created_at.desc()).all()

@router.get("/plans/{plan_id}", response_model=MealPlanResponse)
def get_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = db.query(MealPlan).filter(
        MealPlan.id == plan_id,
        MealPlan.user_id == current_user.id
    ).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    
    return plan
""",

    "backend/app/grocery/routes.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import MealPlan, Recipe, User
from ..auth.routes import get_current_user
from collections import defaultdict

router = APIRouter(prefix="/grocery", tags=["Grocery Lists"])

@router.get("/list/{meal_plan_id}")
def get_grocery_list(
    meal_plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = db.query(MealPlan).filter(
        MealPlan.id == meal_plan_id,
        MealPlan.user_id == current_user.id
    ).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    
    recipe_ids = set()
    for day_data in plan.meals.values():
        for meal_type, meal_data in day_data.get('meals', {}).items():
            if 'recipe_id' in meal_data:
                recipe_ids.add(meal_data['recipe_id'])
    
    recipes = db.query(Recipe).filter(Recipe.recipe_id.in_(recipe_ids)).all()
    
    ingredients_list = []
    for recipe in recipes:
        if recipe.ingredients:
            ingredients_list.extend(recipe.ingredients)
    
    unique_ingredients = list(set(ingredients_list))
    
    return {
        "meal_plan_id": meal_plan_id,
        "ingredients": unique_ingredients,
        "total": len(unique_ingredients),
        "week_start": plan.week_start_date
    }
"""
}

print("Creating all backend route files...\n")

for filepath, content in files.items():
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"✅ Created: {filepath}")
    except Exception as e:
        print(f"❌ Error creating {filepath}: {e}")

print("\n✅ All backend route files created!")
print("\n📋 NEXT STEP: Create frontend files")