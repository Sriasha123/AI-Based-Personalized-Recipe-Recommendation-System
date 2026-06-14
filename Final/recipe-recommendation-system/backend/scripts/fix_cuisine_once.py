from app.database import SessionLocal
from app.models import Recipe
from app.utils.cleaners import infer_cuisine

db = SessionLocal()

updated = 0

print("🚀 Fixing cuisines permanently...")

recipes = db.query(Recipe).all()

for r in recipes:
    new_cuisine = infer_cuisine(
        tags=r.tags,
        ingredients=r.ingredients,
        name=r.name
    )

    if new_cuisine and new_cuisine != r.cuisine:
        r.cuisine = new_cuisine
        updated += 1

db.commit()
db.close()

print(f"✅ Updated cuisine for {updated} recipes")
