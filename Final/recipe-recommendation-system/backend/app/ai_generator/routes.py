"""
AI Recipe Generator API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import base64

from app.database import get_db
from app.models import Recipe, User
from app.auth.routes import get_current_user

from .generator import ai_generator
from .llm_generator import LLMRecipeGenerator

router = APIRouter(prefix="/ai-generator", tags=["AI Recipe Generator"])

llm_generator = LLMRecipeGenerator()

# =====================================================
# Request Models
# =====================================================

class RecipeGenerationRequest(BaseModel):
    ingredients: List[str]
    cuisine: Optional[str] = "any"
    cooking_time: int = 30
    difficulty: str = "medium"
    servings: int = 4


class SmartRecipeRequest(BaseModel):
    ingredients: List[str]


class IngredientSubstitutionRequest(BaseModel):
    ingredient: str
    diet_type: Optional[str] = None


# =====================================================
# 1️⃣ RULE-BASED AI GENERATOR
# =====================================================

@router.post("/generate")
def generate_custom_recipe(
    request: RecipeGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    if len(request.ingredients) < 2:
        raise HTTPException(400, "Provide at least 2 ingredients")

    recipe = ai_generator.generate_recipe(
        ingredients=request.ingredients,
        cuisine=request.cuisine,
        diet_type=current_user.dietary_type,
        cooking_time=request.cooking_time,
        difficulty=request.difficulty,
        servings=request.servings
    )

    if set(recipe.get("allergens", [])) & set(current_user.allergies or []):
        raise HTTPException(
            400,
            "Generated recipe violates your allergy profile"
        )

    return recipe


# =====================================================
# 2️⃣ SMART AI (TEXT INGREDIENTS)
# =====================================================

@router.post("/generate-smart")
def generate_smart_recipe(
    request: SmartRecipeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if len(request.ingredients) < 2:
        raise HTTPException(400, "Provide at least 2 ingredients")

    user_profile = {
        "dietary_type": current_user.dietary_type,
        "allergies": current_user.allergies or [],
        "health_conditions": current_user.health_conditions or [],
        "preferred_cuisines": current_user.preferred_cuisines or []
    }

    recipe = llm_generator.generate_recipe(
        ingredients=request.ingredients,
        user_profile=user_profile
    )

    return recipe


# =====================================================
# 3️⃣ 🖼️ IMAGE → INGREDIENTS → RECIPE (FIXED)
# =====================================================

@router.post("/generate-from-image")
async def generate_recipe_from_image(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(400, "Please upload a valid image")

    # 1️⃣ Read image bytes
    image_bytes = await image.read()

    if not image_bytes:
        raise HTTPException(400, "Empty image file")

    # 2️⃣ Convert image → base64
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # 3️⃣ Detect ingredients from image
    detected_ingredients = llm_generator.extract_ingredients_from_image(
        image_base64=base64_image
    )

    if len(detected_ingredients) < 2:
        raise HTTPException(
            400,
            "Could not detect enough ingredients from image"
        )

    # 4️⃣ User profile
    user_profile = {
        "dietary_type": current_user.dietary_type,
        "allergies": current_user.allergies or [],
        "health_conditions": current_user.health_conditions or [],
        "preferred_cuisines": current_user.preferred_cuisines or []
    }

    # 5️⃣ Generate recipe
    recipe = llm_generator.generate_recipe(
        ingredients=detected_ingredients,
        user_profile=user_profile
    )

    return {
        "detected_ingredients": detected_ingredients,
        "recipe": recipe
    }


# =====================================================
# 4️⃣ INGREDIENT SUBSTITUTION
# =====================================================

@router.post("/substitute")
def get_ingredient_substitutions(
    request: IngredientSubstitutionRequest
):
    return {
        "original": request.ingredient,
        "substitutions": ai_generator.suggest_ingredient_substitutions(
            ingredient=request.ingredient,
            diet_type=request.diet_type
        )
    }


# =====================================================
# 5️⃣ PANTRY-BASED MULTI-RECIPE
# =====================================================

@router.post("/generate-from-pantry")
def generate_from_pantry_items(
    pantry_items: List[str],
    current_user: User = Depends(get_current_user)
):
    if len(pantry_items) < 3:
        raise HTTPException(400, "Provide at least 3 pantry items")

    cuisines = ["italian", "indian", "mexican"]
    recipes = []

    for cuisine in cuisines:
        recipe = ai_generator.generate_recipe(
            ingredients=pantry_items,
            cuisine=cuisine,
            diet_type=current_user.dietary_type,
            cooking_time=30,
            difficulty="medium",
            servings=4
        )
        recipes.append(recipe)

    return {
        "message": "Generated multiple recipe options",
        "recipes": recipes
    }
