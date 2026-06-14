from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import random

from app.database import get_db
from app.models import User, MealPlan, Recipe
from app.schemas import MealPlanCreate, MealPlanResponse
from app.auth.routes import get_current_user
from app.utils.profile_rules import violates_profile
from app.utils.cleaners import clean_foodcom_list

router = APIRouter(
    prefix="/meal-planner",
    tags=["Meal Planning"]
)

# --------------------------------------------------
# Generate Personalized Meal Plan
# --------------------------------------------------

@router.post("/generate", response_model=MealPlanResponse)
def generate_meal_plan(
    plan: MealPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1️⃣ Fetch all recipes
    all_recipes = db.query(Recipe).all()

    # 2️⃣ Apply PROFILE RULES (diet + allergy + health)
    valid_recipes = []
    for r in all_recipes:
        meta = {
            "ingredients": r.ingredients,
            "nutrition": r.nutrition,
            "cuisine": r.cuisine
        }
        if not violates_profile(current_user, meta):
            valid_recipes.append(r)

    if len(valid_recipes) < 21:
        raise HTTPException(
            status_code=400,
            detail="Not enough recipes matching your profile"
        )

    # 3️⃣ Calorie planning
    target_calories = plan.target_calories or 2000
    per_meal_target = target_calories / 3

    weekly_plan = {}
    total_calories = 0
    used_recipe_ids = set()

    # 4️⃣ Build 7-day meal plan
    for day in range(7):
        date = plan.week_start_date + timedelta(days=day)
        meals = {}

        for meal_type in ["breakfast", "lunch", "dinner"]:
            candidates = [
                r for r in valid_recipes
                if r.recipe_id not in used_recipe_ids
            ]

            if not candidates:
                candidates = valid_recipes  # fallback

            recipe = random.choice(candidates)
            used_recipe_ids.add(recipe.recipe_id)

            calories = (
                recipe.nutrition.get("calories", 0)
                if isinstance(recipe.nutrition, dict)
                else 0
            )

            meals[meal_type] = {
                "recipe_id": recipe.recipe_id,
                "name": recipe.name,
                "calories": calories
            }

            total_calories += calories

        weekly_plan[date.strftime("%A")] = {
            "date": date.strftime("%Y-%m-%d"),
            "meals": meals
        }

    # 5️⃣ Save meal plan
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


# --------------------------------------------------
# Get All Meal Plans (User)
# --------------------------------------------------

@router.get("/plans", response_model=List[MealPlanResponse])
def get_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return (
        db.query(MealPlan)
        .filter(MealPlan.user_id == current_user.id)
        .order_by(MealPlan.created_at.desc())
        .all()
    )


# --------------------------------------------------
# Get Single Meal Plan
# --------------------------------------------------

@router.get("/plans/{plan_id}", response_model=MealPlanResponse)
def get_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = (
        db.query(MealPlan)
        .filter(
            MealPlan.id == plan_id,
            MealPlan.user_id == current_user.id
        )
        .first()
    )

    if not plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    return plan
