"""
Enhanced Recommendation API
FINAL – Stable, Profile Aware, Schema Safe
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
import pickle
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

from app.database import get_db
from app.models import User, Recipe, Review
from app.schemas import RecipeDetail
from app.auth.routes import get_current_user
from app.utils.profile_rules import violates_profile
from app.utils.cleaners import clean_steps, clean_foodcom_list

router = APIRouter(
    prefix="/recommendations/enhanced",
    tags=["Enhanced Recommendations"]
)

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "ml_models"

embedding_model = None
faiss_index = None
recipe_id_to_index = None
recipe_metadata = None


# --------------------------------------------------
# Load FAISS + metadata once
# --------------------------------------------------
def load_models():
    global embedding_model, faiss_index, recipe_id_to_index, recipe_metadata

    if embedding_model is None:
        embedding_model = SentenceTransformer("all-mpnet-base-v2")

    if faiss_index is None:
        faiss_index = faiss.read_index(str(MODEL_DIR / "faiss_index.bin"))

        with open(MODEL_DIR / "recipe_id_to_index.pkl", "rb") as f:
            recipe_id_to_index = pickle.load(f)  # LIST

        with open(MODEL_DIR / "recipe_metadata.pkl", "rb") as f:
            recipe_metadata = pickle.load(f)     # LIST of dicts


# --------------------------------------------------
# Build semantic query
# --------------------------------------------------
def build_user_query(user: User) -> str:
    return " ".join([
        user.dietary_type or "",
        " ".join(user.preferred_cuisines or []),
        " ".join(user.health_conditions or []),
        "without",
        " ".join(user.allergies or [])
    ]).strip()


# --------------------------------------------------
# Hybrid ranking
# --------------------------------------------------
def hybrid_rank(user, candidates, db, top_k):
    scores = [c["score"] for c in candidates]
    min_s, max_s = min(scores), max(scores)

    def norm(x):
        return (x - min_s) / (max_s - min_s + 1e-8)

    reviews = db.query(Review).filter(Review.user_id == user.id).all()
    liked = {r.recipe_id for r in reviews if r.rating >= 4}

    ranked = []

    for c in candidates:
        semantic = norm(c["score"])
        collaborative = 1.0 if c["recipe_id"] in liked else 0.5

        preference = 0.5
        if c["meta"].get("cuisine", "").lower() in [
            x.lower() for x in (user.preferred_cuisines or [])
        ]:
            preference += 0.3

        final_score = (
            0.4 * semantic +
            0.2 * collaborative +
            0.4 * preference
        )

        ranked.append((c["recipe_id"], final_score))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in ranked[:top_k]]


# --------------------------------------------------
# API
# --------------------------------------------------
@router.get("/smart-personalized", response_model=List[RecipeDetail])
def smart_personalized_recommendations(
    n_recommendations: int = Query(10, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    load_models()

    query = build_user_query(current_user)
    query_vec = normalize(
        embedding_model.encode([query])
    ).astype("float32")

    scores, indices = faiss_index.search(query_vec, n_recommendations * 5)

    candidates = []

    for idx, score in zip(indices[0], scores[0]):
        if idx >= len(recipe_id_to_index):
            continue

        meta = recipe_metadata[idx]

        if violates_profile(current_user, meta):
            continue

        candidates.append({
            "recipe_id": recipe_id_to_index[idx],
            "score": float(score),
            "meta": meta
        })

    if not candidates:
        raise HTTPException(404, "No recipes match your profile")

    top_ids = hybrid_rank(current_user, candidates, db, n_recommendations)

    recipes = db.query(Recipe).filter(
        Recipe.recipe_id.in_(top_ids)
    ).all()

    recipe_map = {r.recipe_id: r for r in recipes}

    results = []

    for rid in top_ids:
        if rid not in recipe_map:
            continue

        r = recipe_map[rid]

        # 🔥 THIS IS THE FIX
        r.steps = clean_steps(r.steps)
        r.ingredients = clean_foodcom_list(r.ingredients)
        r.tags = clean_foodcom_list(r.tags)
        r.description = None
        results.append(r)

    return results
