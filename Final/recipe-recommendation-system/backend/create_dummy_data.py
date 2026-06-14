"""
Dummy Data Generator - Creates sample recipes for testing
Save as: create_dummy_data.py
Run from: backend folder
No CSV needed! Creates 50 sample recipes
"""

from sqlalchemy.orm import Session
from app.database import engine, Base
from app.models import Recipe
import random

def create_dummy_recipes():
    print("="*70)
    print("🎲 DUMMY DATA GENERATOR - Creating Sample Recipes")
    print("="*70)
    print()
    
    # Create tables
    print("1️⃣ Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("   ✅ Done")
    
    # Sample data
    recipe_templates = [
        {
            "name": "Classic Spaghetti Carbonara",
            "minutes": 25,
            "ingredients": ["spaghetti", "eggs", "bacon", "parmesan cheese", "black pepper"],
            "description": "A creamy Italian pasta dish with bacon and eggs",
            "cuisine": "italian",
            "tags": ["italian", "pasta", "dinner", "30-minutes-or-less"],
            "nutrition": [520, 25, 8, 650, 28, 12, 45]
        },
        {
            "name": "Chicken Tikka Masala",
            "minutes": 45,
            "ingredients": ["chicken", "yogurt", "tomatoes", "cream", "garam masala", "garlic", "ginger"],
            "description": "Spicy Indian curry with tender chicken in creamy tomato sauce",
            "cuisine": "indian",
            "tags": ["indian", "curry", "chicken", "spicy", "main-dish"],
            "nutrition": [480, 22, 6, 720, 35, 10, 38]
        },
        {
            "name": "Greek Salad",
            "minutes": 15,
            "ingredients": ["tomatoes", "cucumber", "feta cheese", "olives", "red onion", "olive oil"],
            "description": "Fresh Mediterranean salad with feta cheese",
            "cuisine": "greek",
            "tags": ["greek", "salad", "vegetarian", "healthy", "15-minutes-or-less"],
            "nutrition": [220, 18, 4, 420, 8, 6, 12]
        },
        {
            "name": "Beef Tacos",
            "minutes": 30,
            "ingredients": ["ground beef", "taco shells", "lettuce", "cheese", "tomatoes", "sour cream"],
            "description": "Classic Mexican tacos with seasoned beef",
            "cuisine": "mexican",
            "tags": ["mexican", "tacos", "beef", "dinner", "30-minutes-or-less"],
            "nutrition": [380, 19, 5, 580, 26, 8, 32]
        },
        {
            "name": "Caesar Salad",
            "minutes": 20,
            "ingredients": ["romaine lettuce", "parmesan cheese", "croutons", "caesar dressing", "chicken"],
            "description": "Classic Caesar salad with grilled chicken",
            "cuisine": "american",
            "tags": ["salad", "chicken", "american", "lunch"],
            "nutrition": [320, 24, 3, 680, 28, 5, 18]
        },
        {
            "name": "Margherita Pizza",
            "minutes": 35,
            "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "basil", "olive oil"],
            "description": "Classic Italian pizza with fresh mozzarella and basil",
            "cuisine": "italian",
            "tags": ["italian", "pizza", "vegetarian", "dinner"],
            "nutrition": [680, 28, 8, 920, 26, 12, 85]
        },
        {
            "name": "Pad Thai",
            "minutes": 30,
            "ingredients": ["rice noodles", "shrimp", "peanuts", "bean sprouts", "tamarind", "eggs"],
            "description": "Thai stir-fried noodles with shrimp and peanuts",
            "cuisine": "thai",
            "tags": ["thai", "noodles", "shrimp", "asian"],
            "nutrition": [450, 16, 12, 920, 24, 3, 58]
        },
        {
            "name": "Vegetable Stir Fry",
            "minutes": 20,
            "ingredients": ["broccoli", "carrots", "bell peppers", "soy sauce", "garlic", "ginger", "rice"],
            "description": "Healthy vegetable stir fry with Asian flavors",
            "cuisine": "chinese",
            "tags": ["chinese", "vegetarian", "healthy", "stir-fry", "vegan"],
            "nutrition": [280, 8, 6, 720, 8, 1, 48]
        },
        {
            "name": "Grilled Salmon",
            "minutes": 25,
            "ingredients": ["salmon fillet", "lemon", "dill", "garlic", "olive oil"],
            "description": "Perfectly grilled salmon with herbs",
            "cuisine": "american",
            "tags": ["seafood", "healthy", "grilled", "low-carb", "keto"],
            "nutrition": [420, 26, 2, 380, 42, 5, 4]
        },
        {
            "name": "Chocolate Chip Cookies",
            "minutes": 30,
            "ingredients": ["flour", "butter", "sugar", "chocolate chips", "eggs", "vanilla"],
            "description": "Classic homemade chocolate chip cookies",
            "cuisine": "american",
            "tags": ["dessert", "cookies", "baking", "sweet"],
            "nutrition": [180, 9, 18, 140, 2, 5, 24]
        }
    ]
    
    # Create variations
    print("\n2️⃣ Creating recipes...")
    session = Session(engine)
    
    # Clear existing
    session.query(Recipe).delete()
    session.commit()
    
    loaded = 0
    
    # Create 50 recipes (5 of each template)
    for i in range(50):
        template = recipe_templates[i % len(recipe_templates)]
        
        # Add variation to names
        variation = i // len(recipe_templates) + 1
        name = f"{template['name']}" if variation == 1 else f"{template['name']} (Style {variation})"
        
        # Add slight calorie variation
        nutrition = template['nutrition'].copy()
        nutrition[0] += random.randint(-50, 50)  # Vary calories
        
        # Create recipe
        recipe = Recipe(
            recipe_id=i + 1,
            name=name,
            minutes=template['minutes'] + random.randint(-5, 5),
            tags=template['tags'],
            nutrition=nutrition,
            n_steps=random.randint(4, 8),
            steps=f"Step 1: Prepare ingredients\nStep 2: Cook\nStep 3: Season\nStep 4: Serve",
            description=template['description'],
            ingredients=template['ingredients'],
            n_ingredients=len(template['ingredients']),
            cuisine=template['cuisine'],
            dietary_tags=[],
            allergens=[]
        )
        
        session.add(recipe)
        loaded += 1
        
        if loaded % 10 == 0:
            print(f"   📦 Created {loaded} recipes...")
    
    session.commit()
    session.close()
    
    # Verify
    print(f"\n3️⃣ Verification:")
    session = Session(engine)
    count = session.query(Recipe).count()
    
    if count > 0:
        sample = session.query(Recipe).first()
        print(f"   ✅ Total recipes: {count}")
        print(f"\n   📋 Sample Recipe:")
        print(f"      ID: {sample.recipe_id}")
        print(f"      Name: {sample.name}")
        print(f"      Time: {sample.minutes} min")
        print(f"      Calories: {sample.nutrition[0]} cal")
        print(f"      Cuisine: {sample.cuisine}")
        print(f"      Ingredients: {len(sample.ingredients)}")
    
    session.close()
    
    print("\n" + "="*70)
    print("🎉 SUCCESS! Dummy recipes created!")
    print("="*70)
    print("\n✅ Next steps:")
    print("   1. Restart backend: uvicorn app.main:app --reload")
    print("   2. Go to: http://localhost:3000")
    print("   3. Try signup and browse recipes!")
    print("\n💡 This is dummy data for testing.")
    print("   Replace with your real CSV data later.")
    print()

if __name__ == "__main__":
    create_dummy_recipes()