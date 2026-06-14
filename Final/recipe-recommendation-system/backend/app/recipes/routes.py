from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Recipe
from app.schemas import RecipeDetail
from app.utils.cleaners import clean_steps, clean_foodcom_list

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("/search", response_model=List[RecipeDetail])
def search_recipes(
    query: Optional[str] = None,
    cuisine: Optional[str] = None,
    max_calories: Optional[int] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Recipe)

    if query:
        q = q.filter(Recipe.name.ilike(f"%{query}%"))

    if cuisine:
        q = q.filter(Recipe.cuisine.ilike(f"%{cuisine}%"))

    recipes = q.limit(20).all()
    results = []

    for r in recipes:
        steps = clean_steps(r.steps)
        raw_ingredients = clean_foodcom_list(r.ingredients)
        tags = clean_foodcom_list(r.tags)

        ingredients = []
        for ing in raw_ingredients:
            if isinstance(ing, dict):
                name = ing.get("name", "")
                qty = ing.get("quantity", "")
                notes = ing.get("notes", "")
                combined = " ".join(x for x in [qty, name, notes] if x)
                ingredients.append(combined.strip())
            else:
                ingredients.append(str(ing))

        results.append({
            "id": r.id,
            "recipe_id": r.recipe_id,
            "name": r.name,
            "minutes": r.minutes or 0,
            "description": None,
            "steps": steps,
            "ingredients": ingredients,
            "tags": tags,
            "n_steps": len(steps),
            "n_ingredients": len(ingredients),
            "cuisine": r.cuisine or "General",
            "nutrition": r.nutrition or {},
            "dietary_tags": r.dietary_tags or [],
            "allergens": r.allergens or []
        })

    return results

