"""
Rule-Based AI Recipe Generator
Safe fallback when LLM is unavailable
Profile-aware (diet, allergies, health)
"""

from typing import List, Dict, Optional
import random


class AIRecipeGenerator:
    """
    Deterministic recipe generator (NO LLM)
    Always safe, predictable, schema-correct
    """

    # ----------------------------------
    # INIT
    # ----------------------------------

    def __init__(self):
        self.meat_items = {"chicken", "beef", "pork", "fish", "meat"}
        self.dairy_items = {"milk", "cheese", "butter", "cream", "yogurt"}
        self.gluten_items = {"wheat", "flour", "bread", "pasta"}

        self.cuisine_templates = {
            "indian": ["cumin", "turmeric", "ginger"],
            "italian": ["olive oil", "basil", "oregano"],
            "mexican": ["chili powder", "lime", "cumin"],
            "chinese": ["soy sauce", "ginger", "garlic"],
            "fusion": ["garlic", "pepper"]
        }

    # ----------------------------------
    # MAIN GENERATOR
    # ----------------------------------

    def generate_recipe(
        self,
        ingredients: List[str],
        cuisine: str = "any",
        diet_type: Optional[str] = None,
        cooking_time: int = 30,
        difficulty: str = "medium",
        servings: int = 4,
        user_profile: Optional[Dict] = None
    ) -> Dict:

        ingredients = [i.lower().strip() for i in ingredients]

        allergies = set(user_profile.get("allergies", [])) if user_profile else set()
        health = user_profile.get("health_conditions", []) if user_profile else []

        # ----------------------------------
        # FILTER INGREDIENTS (CRITICAL)
        # ----------------------------------

        safe_ingredients = []
        for ing in ingredients:
            if self._violates_diet(ing, diet_type):
                continue
            if self._violates_allergy(ing, allergies):
                continue
            safe_ingredients.append(ing)

        if not safe_ingredients:
            raise ValueError("No safe ingredients after applying profile rules")

        # ----------------------------------
        # CUISINE HANDLING
        # ----------------------------------

        cuisine = cuisine if cuisine in self.cuisine_templates else "fusion"
        flavors = self.cuisine_templates[cuisine]

        # ----------------------------------
        # BUILD RECIPE
        # ----------------------------------

        recipe_name = f"{cuisine.capitalize()} {safe_ingredients[0].capitalize()} Delight"

        all_ingredients = list(dict.fromkeys(
            safe_ingredients + flavors + ["salt", "pepper"]
        ))

        steps = self._generate_steps(all_ingredients, difficulty)

        nutrition = self._estimate_nutrition(
            all_ingredients, servings, health
        )

        dietary_tags = self._dietary_tags(all_ingredients, diet_type)
        allergens = self._detect_allergens(all_ingredients)

        return {
            "name": recipe_name,
            "description": f"A healthy {cuisine} recipe tailored to your profile",
            "ingredients": all_ingredients,
            "n_ingredients": len(all_ingredients),
            "steps": steps,
            "n_steps": len(steps),
            "minutes": cooking_time,
            "servings": servings,
            "difficulty": difficulty,
            "cuisine": cuisine,
            "tags": [cuisine, difficulty, "custom"],
            "nutrition": nutrition,
            "dietary_tags": dietary_tags,
            "allergens": allergens
        }

    # ----------------------------------
    # HELPERS
    # ----------------------------------

    def _violates_diet(self, ing: str, diet: Optional[str]) -> bool:
        if diet == "vegetarian" and ing in self.meat_items:
            return True
        if diet == "vegan" and (ing in self.meat_items or ing in self.dairy_items):
            return True
        if diet == "gluten-free" and ing in self.gluten_items:
            return True
        return False

    def _violates_allergy(self, ing: str, allergies: set) -> bool:
        for allergy in allergies:
            if allergy in ing:
                return True
        return False

    def _generate_steps(self, ingredients: List[str], difficulty: str) -> List[str]:
        steps = [
            f"Prepare ingredients: {', '.join(ingredients[:5])}."
        ]

        if difficulty == "easy":
            steps += [
                "Cook all ingredients together over medium heat.",
                "Season to taste and serve warm."
            ]
        elif difficulty == "medium":
            steps += [
                "Sauté aromatics until fragrant.",
                "Add remaining ingredients and simmer.",
                "Adjust seasoning and finish gently."
            ]
        else:
            steps += [
                "Prepare ingredients carefully.",
                "Cook in stages to develop flavors.",
                "Simmer slowly and adjust texture.",
                "Finish with garnish and rest before serving."
            ]

        steps.append("Serve hot and enjoy.")
        return steps

    def _estimate_nutrition(
        self,
        ingredients: List[str],
        servings: int,
        health_conditions: List[str]
    ) -> Dict:

        calories = 350
        protein = 20
        fat = 12
        carbs = 40

        if "diabetes" in health_conditions:
            carbs -= 10
        if "heart" in " ".join(health_conditions).lower():
            fat -= 5

        return {
            "calories": round(calories / servings, 1),
            "protein": round(protein / servings, 1),
            "fat": round(fat / servings, 1),
            "carbs": round(carbs / servings, 1)
        }

    def _dietary_tags(self, ingredients: List[str], diet: Optional[str]) -> List[str]:
        tags = []
        if diet:
            tags.append(diet)
        if not any(i in self.meat_items for i in ingredients):
            tags.append("vegetarian")
        return list(set(tags))

    def _detect_allergens(self, ingredients: List[str]) -> List[str]:
        allergens = []
        for ing in ingredients:
            if ing in self.dairy_items:
                allergens.append("dairy")
            if ing in self.gluten_items:
                allergens.append("gluten")
        return list(set(allergens))


# GLOBAL INSTANCE
ai_generator = AIRecipeGenerator()
