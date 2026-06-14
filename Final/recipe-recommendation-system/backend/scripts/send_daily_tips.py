from app.database import SessionLocal
from app.models import User
from app.tips.tip_generator import tip_generator
from app.utils.email_service import send_email


db = SessionLocal()

users = db.query(User).all()

for user in users:
    if not user.email:
        continue

    profile = {
        "dietary_type": user.dietary_type,
        "health_conditions": user.health_conditions or [],
        "allergies": user.allergies or [],
        "preferred_cuisines": user.preferred_cuisines or []
    }

    try:
        tip = tip_generator.generate_tip(profile)

        send_email(
            to_email=user.email,
            subject="🌿 Your Daily Health Tip",
            body=f"Hello {user.full_name or 'User'},\n\n{tip}\n\nStay healthy!"
        )

        print(f"✅ Sent tip to {user.email}")

    except Exception as e:
        print(f"❌ Failed for {user.email}: {e}")

db.close()