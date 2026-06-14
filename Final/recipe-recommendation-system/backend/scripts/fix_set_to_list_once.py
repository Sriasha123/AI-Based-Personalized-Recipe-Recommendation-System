from app.database import SessionLocal
from app.models import Recipe

def fix_sets():
    db = SessionLocal()
    fixed = 0

    recipes = db.query(Recipe).all()

    for r in recipes:
        changed = False

        if isinstance(r.steps, set):
            r.steps = list(r.steps)
            changed = True

        if isinstance(r.ingredients, set):
            r.ingredients = list(r.ingredients)
            changed = True

        if isinstance(r.dietary_tags, set):
            r.dietary_tags = list(r.dietary_tags)
            changed = True

        if isinstance(r.allergens, set):
            r.allergens = list(r.allergens)
            changed = True

        if changed:
            fixed += 1

    db.commit()
    db.close()
    print(f"✅ Fixed {fixed} recipes (set → list)")

if __name__ == "__main__":
    fix_sets()
