from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Review, Recipe, User
from ..schemas import ReviewCreate, ReviewResponse
from ..auth.routes import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewResponse)
def create_review(
    review: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == review.recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    new_review = Review(
        user_id=current_user.id,
        recipe_id=recipe.id,
        rating=review.rating,
        review_text=review.review_text
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/recipe/{recipe_id}", response_model=List[ReviewResponse])
def get_recipe_reviews(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    reviews = db.query(Review).filter(Review.recipe_id == recipe.id).all()
    return reviews