"""
Profile-based HARD CONSTRAINT RULES
Used to strictly filter recipes before ranking
"""

# ==========================================================
# KEYWORD DICTIONARIES
# ==========================================================

NON_VEG_ITEMS = [
    "chicken", "beef", "pork", "mutton", "lamb",
    "fish", "shrimp", "prawn", "crab", "seafood",
    "bacon", "ham", "turkey"
]

DAIRY_ITEMS = [
    "milk", "cheese", "butter", "cream",
    "yogurt", "ghee", "paneer"
]

EGG_ITEMS = ["egg", "eggs"]

HIGH_CARB_ITEMS = [
    "rice", "bread", "pasta", "wheat", "corn",
    "potato", "sugar", "flour"
]

# Allergy keywords (frontend-aligned)
ALLERGY_KEYWORDS = {
    "peanut": ["peanut", "groundnut"],
    "dairy": DAIRY_ITEMS,
    "gluten": ["wheat", "barley", "rye", "flour"],
    "egg": EGG_ITEMS,
    "soy": ["soy", "soybean", "tofu"],
    "shellfish": ["shrimp", "prawn", "crab", "lobster"],
    "tree nut": ["almond", "cashew", "walnut", "pistachio"]
}

# ==========================================================
# DIET RULES
# ==========================================================

def violates_diet(user, ingredients_text: str) -> bool:
    """
    Returns True if recipe violates user's diet
    """
    diet = (user.dietary_type or "").lower()
    text = ingredients_text.lower()

    # Vegetarian: no meat, fish
    if diet == "vegetarian":
        return any(item in text for item in NON_VEG_ITEMS)

    # Vegan: no meat, fish, dairy, eggs
    if diet == "vegan":
        return any(item in text for item in (NON_VEG_ITEMS + DAIRY_ITEMS + EGG_ITEMS))

    # Keto: very low carb
    if diet == "keto":
        return any(item in text for item in HIGH_CARB_ITEMS)

    # Non-veg or no restriction → allow everything
    return False


# ==========================================================
# ALLERGY RULES (STRICT)
# ==========================================================

def violates_allergy(user, ingredients_text: str) -> bool:
    """
    Returns True if recipe contains any allergen
    """
    text = ingredients_text.lower()

    for allergy in user.allergies or []:
        allergy = allergy.lower()
        keywords = ALLERGY_KEYWORDS.get(allergy, [])
        if any(k in text for k in keywords):
            return True

    return False


# ==========================================================
# HEALTH RULES (STRICT)
# ==========================================================

def violates_health(user, nutrition: dict) -> bool:
    """
    Returns True if recipe violates health constraints
    """
    conditions = [c.lower() for c in (user.health_conditions or [])]

    calories = nutrition.get("calories", 0)
    fat = nutrition.get("fat", 0)
    sugar = nutrition.get("sugar", 0)
    sodium = nutrition.get("sodium", 0)
    cholesterol = nutrition.get("cholesterol", 0)

    # Diabetes → low sugar
    if "diabetes" in conditions and calories > 500:
        return True


    # High BP → low sodium
    if "high bp" in conditions and sodium > 600:
        return True

    # Heart disease → low fat & cholesterol
    if "heart disease" in conditions:
        if fat > 25 or cholesterol > 300:
            return True

    # High cholesterol
    if "high cholesterol" in conditions and cholesterol > 300:
        return True

    # Obesity → calorie control
    if "obesity" in conditions and calories > 600:
        return True

    # Cancer → avoid processed/high-fat foods
    if "cancer" in conditions and fat > 30:
        return True

    return False


# ==========================================================
# MASTER CHECK (USE THIS)
# ==========================================================

def violates_profile(user, recipe_meta: dict) -> bool:
    """
    Returns True if recipe should be EXCLUDED
    """
    ingredients_text = " ".join(map(str, recipe_meta.get("ingredients", [])))
    nutrition = recipe_meta.get("nutrition", {})

    if violates_diet(user, ingredients_text):
        return True

    if violates_allergy(user, ingredients_text):
        return True

    if violates_health(user, nutrition):
        return True

    return False
