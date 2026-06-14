from sentence_transformers import SentenceTransformer
import numpy as np
from app.models import Recipe
from sqlalchemy.orm import Session

model = SentenceTransformer("all-mpnet-base-v2")

def build_recipe_embeddings(db: Session):
    recipes = db.query(Recipe).all()

    texts = [
        f"{r.name}. {r.description}. Ingredients: {', '.join(r.ingredients)}"
        for r in recipes
    ]

    embeddings = model.encode(texts, show_progress_bar=True)
    ids = [r.id for r in recipes]

    np.save("data/processed/recipe_embeddings.npy", embeddings)
    np.save("data/processed/recipe_ids.npy", ids)
