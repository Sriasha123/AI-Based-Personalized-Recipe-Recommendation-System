from sqlalchemy.orm import Session
from app.models import Review

def get_user_preference_scores(db: Session, user_id: int):
    reviews = db.query(Review).filter(Review.user_id == user_id).all()
    scores = {}

    for r in reviews:
        scores[r.recipe_id] = scores.get(r.recipe_id, 0) + r.rating

    return scores

