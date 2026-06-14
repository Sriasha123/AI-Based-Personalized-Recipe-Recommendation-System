def is_recipe_allowed(recipe, user):
    name = recipe.name.lower()
    ingredients = " ".join(recipe.ingredients or []).lower()

    # Diet
    if user.dietary_type == "vegetarian" and any(x in name for x in ["chicken","beef","fish"]):
        return False

    if user.dietary_type == "vegan" and any(x in name for x in ["egg","milk","cheese"]):
        return False

    # Allergies
    if user.allergies:
        for a in user.allergies:
            if a.lower() in ingredients:
                return False

    return True
