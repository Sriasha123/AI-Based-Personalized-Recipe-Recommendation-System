# scripts/evaluate_recommendations.py

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Review, Recipe
from app.recommendation_engine.hybrid import get_hybrid_recommendations
from app.evaluation.metrics import precision_at_k, recall_at_k, f1_score

db: Session = SessionLocal()
K = 10

users = db.query(User).all()

precision_scores = []
recall_scores = []
f1_scores = []

print("\n📊 Recommendation Evaluation\n----------------------------")

for user in users:
    # Step 1: Get positive interactions
    reviews = db.query(Review).filter(
        Review.user_id == user.id,
        Review.rating >= 4
    ).all()

    if len(reviews) < 2:
        print(f"⚠️ Skipping user {user.email} (insufficient data)")
        continue

    # Step 2: Leave-one-out
    relevant = {reviews[-1].recipe_id}

    # Step 3: Get real recommendations
    recommended_recipes = get_hybrid_recommendations(
        user_id=user.id,
        db=db,
        limit=K
    )

    recommended_ids = [r.recipe_id for r in recommended_recipes]

    # Step 4: Metrics
    p = precision_at_k(recommended_ids, relevant, K)
    r = recall_at_k(recommended_ids, relevant, K)
    f1 = f1_score(p, r)

    precision_scores.append(p)
    recall_scores.append(r)
    f1_scores.append(f1)

    print(f"User {user.email}")
    print(f" Precision@{K}: {p:.2f}")
    print(f" Recall@{K}: {r:.2f}")
    print(f" F1@{K}: {f1:.2f}\n")

# Step 5: Safe aggregation
if precision_scores:
    print("✅ FINAL RESULTS")
    print("----------------")
    print("Avg Precision@10:", round(sum(precision_scores) / len(precision_scores), 3))
    print("Avg Recall@10:", round(sum(recall_scores) / len(recall_scores), 3))
    print("Avg F1 Score:", round(sum(f1_scores) / len(f1_scores), 3))
else:
    print("❌ Not enough data to compute metrics")

db.close()
