def apply_user_rules(recipes, user_profile):
    filtered = []

    diet = user_profile.get("diet")
    allergies = user_profile.get("allergies", [])
    conditions = user_profile.get("health_conditions", [])

    for r in recipes:
        ingredients = " ".join(r.get("ingredients", [])).lower()
        tags = " ".join(r.get("tags", [])).lower()

        # Diet rules
        if diet == "vegan" and any(x in ingredients for x in ["meat", "chicken", "egg", "milk", "cheese"]):
            continue
        if diet == "vegetarian" and any(x in ingredients for x in ["chicken", "fish", "meat"]):
            continue

        # Allergy rules
        if "gluten" in allergies and "gluten" in tags:
            continue
        if "nuts" in allergies and "nuts" in ingredients:
            continue
        if "dairy" in allergies and any(x in ingredients for x in ["milk", "cheese", "butter"]):
            continue

        # Health conditions
        if "diabetes" in conditions and "high sugar" in tags:
            continue
        if "high blood pressure" in conditions and "high sodium" in tags:
            continue

        filtered.append(r)

    return filtered
