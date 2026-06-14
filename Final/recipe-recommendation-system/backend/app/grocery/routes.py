from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import MealPlan, Recipe, User
from app.auth.routes import get_current_user
from app.utils.cleaners import clean_foodcom_list

router = APIRouter(
    prefix="/grocery",
    tags=["Grocery"]
)

@router.get("/list/{meal_plan_id}")
def get_grocery_list(
    meal_plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1️⃣ Fetch meal plan
    plan = db.query(MealPlan).filter(
        MealPlan.id == meal_plan_id,
        MealPlan.user_id == current_user.id
    ).first()

    if not plan:
        raise HTTPException(404, "Meal plan not found")

    # 2️⃣ Collect recipe IDs
    recipe_ids = set()
    for day in plan.meals.values():
        for meal in day["meals"].values():
            recipe_ids.add(meal["recipe_id"])

    # 3️⃣ Fetch recipes
    recipes = db.query(Recipe).filter(
        Recipe.recipe_id.in_(recipe_ids)
    ).all()

    # 4️⃣ Collect ingredients
    ingredients = []
    for r in recipes:
        ingredients.extend(clean_foodcom_list(r.ingredients))

    # 5️⃣ Normalize ingredients
    normalized = sorted(
        set(i.lower().strip() for i in ingredients if i)
    )

    return {
        "total": len(normalized),
        "ingredients": normalized
    }
