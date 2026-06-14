# scripts/clean_database_once.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Recipe
from app.utils.cleaners import (
    clean_foodcom_list,
    clean_steps,
    infer_cuisine
)

db: Session = SessionLocal()

print("🚀 Starting permanent DB cleaning...")

recipes = db.query(Recipe).all()
count = 0

for recipe in recipes:
    # ✅ Clean lists FIRST
    recipe.ingredients = clean_foodcom_list(recipe.ingredients)
    recipe.tags = clean_foodcom_list(recipe.tags)
    recipe.steps = clean_steps(recipe.steps)

    # ✅ Infer cuisine AFTER cleaning
    recipe.cuisine = infer_cuisine(
        tags=recipe.tags,
        ingredients=recipe.ingredients,
        name=recipe.name
    )

    # ✅ Remove Food.com boilerplate description
    recipe.description = None

    # ✅ Fix counters
    recipe.n_steps = len(recipe.steps)
    recipe.n_ingredients = len(recipe.ingredients)

    count += 1

db.commit()
db.close()

print(f"✅ Cleaned {count} recipes permanently")
