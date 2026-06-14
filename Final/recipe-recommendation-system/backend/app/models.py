from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
#from app.models.interaction import UserInteraction


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    age = Column(Integer)
    dietary_type = Column(String)
    allergies = Column(JSON, nullable=True)
    preferred_cuisines = Column(JSON, nullable=True)
    health_conditions = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    reviews = relationship("Review", back_populates="user")
    meal_plans = relationship("MealPlan", back_populates="user")

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, unique=True, index=True)
    name = Column(String, index=True)
    minutes = Column(Integer)
    tags = Column(JSON)
    nutrition = Column(JSON)
    n_steps = Column(Integer)
    steps = Column(Text)
    description = Column(Text)
    ingredients = Column(JSON)
    n_ingredients = Column(Integer)
    cuisine = Column(String, index=True)
    dietary_tags = Column(JSON)
    allergens = Column(JSON)
    
    reviews = relationship("Review", back_populates="recipe")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"))

    rating = Column(Float)
    review_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="reviews")
    recipe = relationship("Recipe", back_populates="reviews")

class MealPlan(Base):
    __tablename__ = "meal_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    week_start_date = Column(DateTime)
    meals = Column(JSON)
    total_calories = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="meal_plans")