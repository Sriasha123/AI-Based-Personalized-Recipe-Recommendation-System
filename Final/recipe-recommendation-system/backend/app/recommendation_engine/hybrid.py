from .content_based import build_embeddings, build_faiss_index
from .collaborative import get_user_preference_scores
from .rules import is_recipe_allowed

def get_hybrid_recommendations(db, user, recipes, top_k=10):
    # Rule filter
    safe_recipes = [r for r in recipes if is_recipe_allowed(r, user)]

    if not safe_recipes:
        return recipes[:top_k]

    # Content-based
    embeddings = build_embeddings(safe_recipes)
    index = build_faiss_index(embeddings)

    query_text = " ".join(user.preferred_cuisines or []) or "healthy food"
    similar_recipes = safe_recipes[:top_k * 2]

    # Collaborative
    user_scores = get_user_preference_scores(db, user.id)

    scored = []
    for r in similar_recipes:
        score = 0
        score += user_scores.get(r.recipe_id, 0) * 2
        score += 3 if r.cuisine in (user.preferred_cuisines or []) else 0
        scored.append((r, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [r for r, _ in scored[:top_k]]
