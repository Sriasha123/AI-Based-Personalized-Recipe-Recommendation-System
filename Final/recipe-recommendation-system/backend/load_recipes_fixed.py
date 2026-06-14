"""
FOOD.COM DATA LOADER (CORRECT MAPPING)
Run from: backend/
"""

import json
import pandas as pd
from sqlalchemy.orm import Session
from app.database import engine, Base
from app.models import Recipe

def parse_list(value):
    if pd.isna(value):
        return []
    try:
        return json.loads(value.replace("'", '"'))
    except:
        return [v.strip() for v in value.split(",") if v.strip()]

def parse_time(value):
    if pd.isna(value):
        return 0
    if isinstance(value, str) and value.startswith("PT"):
        # PT1H30M → minutes
        h = 0
        m = 0
        if "H" in value:
            h = int(value.split("H")[0].replace("PT", ""))
            value = value.split("H")[1]
        if "M" in value:
            m = int(value.replace("M", ""))
        return h * 60 + m
    return 0

def load_recipes():
    print("=" * 70)
    print("🚀 FOOD.COM DATA LOADER (CORRECT)")
    print("=" * 70)

    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    df = pd.read_csv("data/raw/recipes.csv")
    print(f"✅ Recipes found: {len(df)}")

    # Clear existing recipes
    session.query(Recipe).delete()
    session.commit()
    print("🗑️ Cleared old recipes")

    df = df.head(500)  # you can increase later
    loaded = 0

    for _, row in df.iterrows():
        try:
            recipe = Recipe(
                recipe_id=int(row["RecipeId"]),
                name=str(row["Name"])[:200],
                description=str(row["Description"])[:500],

                ingredients=parse_list(row["RecipeIngredientParts"]),
                steps=str(row["RecipeInstructions"])[:2000],

                minutes=parse_time(row["TotalTime"]),
                cuisine=str(row["RecipeCategory"]) if not pd.isna(row["RecipeCategory"]) else "other",

                tags=parse_list(row["Keywords"]),
                dietary_tags=[],
                allergens=[],

                nutrition={
                    "calories": row.get("Calories", 0),
                    "fat": row.get("FatContent", 0),
                    "protein": row.get("ProteinContent", 0),
                },

                n_steps=len(parse_list(row["RecipeInstructions"])),
                n_ingredients=len(parse_list(row["RecipeIngredientParts"]))
            )

            session.add(recipe)
            loaded += 1

            if loaded % 50 == 0:
                session.commit()
                print(f"📦 Loaded {loaded}")

        except Exception as e:
            print(f"⚠️ Skipped: {e}")

    session.commit()
    session.close()

    print(f"🎉 Loaded {loaded} Food.com recipes successfully")

if __name__ == "__main__":
    load_recipes()
