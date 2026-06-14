"""
Advanced Recipe Data Preprocessor
backend/scripts/advanced_preprocessing.py

High-accuracy preprocessing pipeline:
- Dataset schema normalization
- Text cleaning & normalization
- Rich combined text creation
- Sentence-BERT embeddings generation
- Saves embeddings + metadata for recommendations
"""

import pandas as pd
import numpy as np
import pickle
import re
import ast
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

# =====================================================
# PATH SETUP (ROBUST & VS-CODE FRIENDLY)
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
DATA_PATH = BASE_DIR / "data"
RAW_PATH = DATA_PATH / "raw"
PROCESSED_PATH = DATA_PATH / "processed"
MODEL_PATH = BASE_DIR / "ml_models"

RAW_PATH.mkdir(parents=True, exist_ok=True)
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
MODEL_PATH.mkdir(parents=True, exist_ok=True)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def safe_parse_list(val):
    """Safely parse stringified lists or comma-separated text"""
    if pd.isna(val):
        return []
    if isinstance(val, list):
        return val
    try:
        return ast.literal_eval(val)
    except:
        return [v.strip() for v in str(val).split(",") if v.strip()]

# =====================================================
# MAIN PREPROCESSOR CLASS
# =====================================================

class AdvancedRecipePreprocessor:
    """High-accuracy recipe preprocessing with SBERT embeddings"""

    def __init__(self):
        print("🚀 Initializing Advanced Recipe Preprocessor")
        print("=" * 70)

        print("\n📦 Loading Sentence-BERT model...")
        print("   Model: all-mpnet-base-v2")
        self.embedding_model = SentenceTransformer("all-mpnet-base-v2")
        print("   ✅ Model loaded!")

    # ----------------------------
    # TEXT NORMALIZATION
    # ----------------------------

    def normalize_text(self, text):
        if pd.isna(text):
            return ""
        text = str(text).lower()
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s,.-]", "", text)
        return text.strip()

    def normalize_ingredient(self, ingredient):
        ingredient = self.normalize_text(ingredient)
        ingredient = re.sub(
            r"\d+\.?\d*\s*(cup|cups|tablespoon|tablespoons|tsp|tbsp|oz|ounce|pound|lb|gram|g|kg|ml|liter)s?",
            "",
            ingredient,
            flags=re.IGNORECASE,
        )
        ingredient = re.sub(r"\d+\.?\d*", "", ingredient)
        ingredient = re.sub(r"\(.*?\)", "", ingredient)
        ingredient = re.sub(r"\s+", " ", ingredient).strip(" ,-")
        return ingredient

    # ----------------------------
    # FEATURE ENGINEERING
    # ----------------------------

    def create_combined_text(self, row):
        parts = []

        if pd.notna(row.get("name")):
            parts.append(f"Recipe: {self.normalize_text(row['name'])}")

        if pd.notna(row.get("cuisine")):
            parts.append(f"Cuisine: {self.normalize_text(row['cuisine'])}")

        if isinstance(row.get("tags"), list) and row["tags"]:
            tag_text = ", ".join(self.normalize_text(t) for t in row["tags"][:10])
            parts.append(f"Tags: {tag_text}")

        if isinstance(row.get("ingredients"), list) and row["ingredients"]:
            ing_text = ", ".join(
                self.normalize_ingredient(i) for i in row["ingredients"][:15]
            )
            parts.append(f"Ingredients: {ing_text}")

        if pd.notna(row.get("description")):
            desc = self.normalize_text(row["description"])
            parts.append(f"Description: {desc[:200]}")

        return " | ".join(parts)

    # ----------------------------
    # MAIN PIPELINE
    # ----------------------------

    def process_recipes(self, input_file="recipes.csv", max_recipes=500):
        print(f"\n{'='*70}")
        print("STEP 1: Loading Raw Data")
        print(f"{'='*70}")

        recipes_df = pd.read_csv(RAW_PATH / input_file)
        print(f"   ✅ Loaded {len(recipes_df)} recipes")

        # ---- Normalize dataset column names ----
        recipes_df = recipes_df.rename(columns={
            "RecipeId": "id",
            "Name": "name",
            "Description": "description",
            "RecipeIngredientParts": "ingredients",
            "Keywords": "tags",
            "RecipeCategory": "cuisine",
            "TotalTime": "minutes"
        })

        if max_recipes and max_recipes < len(recipes_df):
            recipes_df = recipes_df.head(max_recipes)
            print(f"   📊 Using first {max_recipes} recipes")

        # ---- Parse list-like columns ----
        recipes_df["ingredients"] = recipes_df["ingredients"].apply(safe_parse_list)
        recipes_df["tags"] = recipes_df["tags"].apply(safe_parse_list)

        # ---- Nutrition aggregation ----
        nutrition_cols = [
            "Calories", "FatContent", "SaturatedFatContent",
            "CholesterolContent", "SodiumContent",
            "CarbohydrateContent", "FiberContent",
            "SugarContent", "ProteinContent"
        ]

        recipes_df["nutrition"] = recipes_df[nutrition_cols].to_dict("records")

        print(f"\n{'='*70}")
        print("STEP 2: Text Normalization & Feature Engineering")
        print(f"{'='*70}")

        recipes_df["name_clean"] = recipes_df["name"].apply(self.normalize_text)
        recipes_df["description_clean"] = recipes_df["description"].apply(self.normalize_text)

        print("   🔗 Creating combined feature text...")
        recipes_df["combined_text"] = recipes_df.apply(self.create_combined_text, axis=1)

        print("   ✅ Combined text created")
        print("   📝 Sample:", recipes_df["combined_text"].iloc[0][:200], "...")

        print(f"\n{'='*70}")
        print("STEP 3: Generating SBERT Embeddings")
        print(f"{'='*70}")

        embeddings = self.embedding_model.encode(
            recipes_df["combined_text"].tolist(),
            show_progress_bar=True,
            batch_size=32
        )

        embeddings = normalize(embeddings, norm="l2")
        print(f"   ✅ Embeddings shape: {embeddings.shape}")

        print(f"\n{'='*70}")
        print("STEP 4: Saving Outputs")
        print(f"{'='*70}")

        recipes_df.to_csv(PROCESSED_PATH / "cleaned_recipes.csv", index=False)
        np.save(MODEL_PATH / "recipe_embeddings.npy", embeddings)

        with open(MODEL_PATH / "recipe_id_to_index.pkl", "wb") as f:
            pickle.dump(recipes_df["id"].tolist(), f)

        metadata = recipes_df[
            ["id", "name", "cuisine", "minutes", "nutrition", "ingredients", "tags", "description"]
        ].to_dict("records")

        with open(MODEL_PATH / "recipe_metadata.pkl", "wb") as f:
            pickle.dump(metadata, f)

        print("   ✅ All files saved successfully")
        print("\n🎉 PREPROCESSING COMPLETE!")

        return recipes_df, embeddings


# =====================================================
# SCRIPT ENTRY POINT
# =====================================================

def main():
    preprocessor = AdvancedRecipePreprocessor()
    preprocessor.process_recipes(
        input_file="recipes.csv",
        max_recipes=500   # increase later (5000 / full dataset)
    )

if __name__ == "__main__":
    main()
