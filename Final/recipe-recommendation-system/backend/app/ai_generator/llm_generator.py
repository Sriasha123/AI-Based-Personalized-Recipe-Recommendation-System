from dotenv import load_dotenv
load_dotenv()

from typing import Dict, List
import json
import re
import os
import requests


# -----------------------------------
# 🔥 GROQ API CALL FUNCTION (FREE)
# -----------------------------------
def call_groq(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4
        }
    )

    data = response.json()

    # Optional debug
    if "choices" not in data:
        raise ValueError(f"Groq API error: {data}")

    return data["choices"][0]["message"]["content"]


# -----------------------------------
# MAIN CLASS
# -----------------------------------
class LLMRecipeGenerator:
    """
    Groq-powered recipe generator (FREE)
    """

    # -----------------------------------
    # JSON extractor
    # -----------------------------------
    def _extract_json(self, text: str) -> Dict:
        if not text:
            raise ValueError("Empty response from LLM")

        text = re.sub(r"```json|```", "", text).strip()

        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError("No JSON object found")

        json_str = match.group(0)

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    # -----------------------------------
    # Recipe generator
    # -----------------------------------
    def generate_recipe(
        self,
        ingredients: List[str],
        user_profile: Dict
    ) -> Dict:

        prompt = f"""
You are a professional chef and nutrition expert.

Generate ONE recipe in STRICT JSON ONLY.
Do not add explanations or markdown.

User Profile:
- Diet: {user_profile.get("dietary_type")}
- Allergies: {user_profile.get("allergies")}
- Health Conditions: {user_profile.get("health_conditions")}
- Preferred Cuisines: {user_profile.get("preferred_cuisines")}

Available Ingredients:
{", ".join(ingredients)}

STRICT RULES:
- DO NOT include allergens
- Follow diet strictly
- Consider health conditions
- Use healthy cooking methods
- Provide clear steps
- Output VALID JSON ONLY

JSON FORMAT:
{{
  "name": "",
  "description": "",
  "ingredients": [],
  "steps": [],
  "minutes": 30,
  "servings": 2,
  "nutrition": {{
    "calories": 0,
    "protein": 0,
    "fat": 0,
    "carbs": 0
  }},
  "cuisine": "",
  "dietary_tags": [],
  "allergens": []
}}
"""

        raw = call_groq(prompt)
        recipe = self._extract_json(raw)

        # Safety defaults
        recipe.setdefault("name", "Custom AI Recipe")
        recipe.setdefault("description", "")
        recipe.setdefault("minutes", 30)
        recipe.setdefault("servings", 2)
        recipe.setdefault("cuisine", "General")

        recipe["ingredients"] = recipe.get("ingredients") or []
        recipe["steps"] = recipe.get("steps") or []
        recipe["dietary_tags"] = recipe.get("dietary_tags") or []
        recipe["allergens"] = recipe.get("allergens") or []

        if not isinstance(recipe.get("nutrition"), dict):
            recipe["nutrition"] = {}

        recipe["nutrition"].setdefault("calories", 0)
        recipe["nutrition"].setdefault("protein", 0)
        recipe["nutrition"].setdefault("fat", 0)
        recipe["nutrition"].setdefault("carbs", 0)

        return recipe

    # -----------------------------------
    # Image → Ingredients (basic fallback)
    # -----------------------------------
    def extract_ingredients_from_image(self, image_base64: str) -> List[str]:
        prompt = """
You are a food recognition system.

Identify ingredients from an image description.

Return JSON only:
{
  "ingredients": ["item1", "item2"]
}
"""

        raw = call_groq(prompt)

        try:
            data = self._extract_json(raw)
            ingredients = data.get("ingredients", [])
            return [str(i).lower() for i in ingredients if isinstance(i, str)]

        except Exception:
            words = re.findall(r"[a-zA-Z]+", raw.lower())
            return list(set(words))[:10]