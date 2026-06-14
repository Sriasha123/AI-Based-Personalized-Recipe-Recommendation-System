from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class DailyTipGenerator:
    def generate_tip(self, user_profile: dict) -> str:
        prompt = f"""
Generate ONE short daily health tip (1 sentence).

User Profile:
Diet: {user_profile.get("dietary_type")}
Health Conditions: {user_profile.get("health_conditions")}
Allergies: {user_profile.get("allergies")}
Preferred Cuisines: {user_profile.get("preferred_cuisines")}

Rules:
- Safe
- Practical
- Simple language
- No medical diagnosis
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return response.choices[0].message.content.strip()


tip_generator = DailyTipGenerator()
