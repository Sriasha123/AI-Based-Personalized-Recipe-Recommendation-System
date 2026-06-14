# backend/app/recommendations/routes.py
# FINAL – High Accuracy Personalized Recommendation Engine

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import random
import logging

from ..database import get_db
from ..models import Recipe, User
from ..schemas import RecipeDetail
from ..auth.routes import get_current_user
from app.recommendation_engine.hybrid import get_hybrid_recommendations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])
logger = logging.getLogger(__name__)


# --------------------------------------------------
# 1️⃣ GENERAL RECOMMENDATIONS (NON-PERSONALIZED)
# --------------------------------------------------
@router.get("/", response_model=List[RecipeDetail])
def get_recommendations(
    cuisine: Optional[str] = None,
    max_calories: Optional[int] = None,
    n_recommendations: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    query = db.query(Recipe)

    if cuisine:
        query = query.filter(Recipe.cuisine == cuisine)

    recipes = query.limit(200).all()

    if max_calories:
        recipes = [
            r for r in recipes
            if r.nutrition and r.nutrition[0] <= max_calories
        ]

    if not recipes:
        return []

    return random.sample(recipes, min(n_recommendations, len(recipes)))


# --------------------------------------------------
# 2️⃣ PERSONALIZED RECOMMENDATIONS (CORE FEATURE)
# --------------------------------------------------
@router.get("/personalized", response_model=List[RecipeDetail])
def get_personalized_recommendations(
    current_user: User = Depends(get_current_user),
    n_recommendations: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    """
    🎯 HYBRID PERSONALIZED RECOMMENDATION SYSTEM
    Combines:
    - Rule-based safety filtering
    - Content-based ML (SBERT + FAISS)
    - Collaborative filtering
    """

    logger.info(f"Generating personalized recommendations for user {current_user.id}")

    recipes = db.query(Recipe).all()

    if not recipes:
        return []

    recommendations = get_hybrid_recommendations(
        db=db,
        user=current_user,
        recipes=recipes,
        top_k=n_recommendations
    )

    # 🔐 Fallback safety (never fail)
    if not recommendations:
        logger.warning("Hybrid engine returned empty results. Using fallback.")
        return recipes[:n_recommendations]

    return recommendations


# --------------------------------------------------
# 3️⃣ SIMILAR RECIPES
# --------------------------------------------------
@router.get("/similar/{recipe_id}", response_model=List[RecipeDetail])
def get_similar_recipes(
    recipe_id: int,
    n_recommendations: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        return []

    return (
        db.query(Recipe)
        .filter(
            Recipe.cuisine == recipe.cuisine,
            Recipe.recipe_id != recipe_id
        )
        .limit(n_recommendations)
        .all()
    )


# --------------------------------------------------
# 4️⃣ INGREDIENT-BASED RECOMMENDATION
# --------------------------------------------------
@router.get("/by-ingredients", response_model=List[RecipeDetail])
def recommend_by_ingredients(
    ingredients: str = Query(..., description="Comma-separated ingredients"),
    n_recommendations: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    ingredient_list = [i.strip().lower() for i in ingredients.split(",")]
    scored = []

    recipes = db.query(Recipe).all()

    for recipe in recipes:
        if not recipe.ingredients:
            continue

        recipe_ings = " ".join(recipe.ingredients).lower()
        match_count = sum(1 for ing in ingredient_list if ing in recipe_ings)

        if match_count > 0:
            scored.append((recipe, match_count))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [r for r, _ in scored[:n_recommendations]]
