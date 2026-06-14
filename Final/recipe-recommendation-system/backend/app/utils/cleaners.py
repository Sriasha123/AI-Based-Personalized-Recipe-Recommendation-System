# backend/app/utils/cleaners.py
import re
import ast

def parse_foodcom_list(raw):
    if raw is None:
        return []

    if isinstance(raw, list):
        return raw

    if not isinstance(raw, str):
        return []

    matches = re.findall(r'"(.*?)"', raw)
    return [m.strip() for m in matches if m.strip()]


def clean_foodcom_list(value):
    """
    ALWAYS returns List[str]
    Handles:
    - Food.com strings
    - AI ingredient dicts
    - Mixed lists
    """
    if not value:
        return []

    cleaned = []

    # Case 1: Already a list
    if isinstance(value, list):
        for item in value:
            # String ingredient
            if isinstance(item, str):
                cleaned.append(item.strip())

            # AI-generated ingredient object
            elif isinstance(item, dict):
                name = item.get("name", "").strip()
                qty = item.get("quantity", "").strip()
                notes = item.get("notes", "").strip()

                text = name
                if qty:
                    text += f" ({qty})"
                if notes:
                    text += f" - {notes}"

                if text:
                    cleaned.append(text)

            else:
                cleaned.append(str(item))

        return cleaned

    # Case 2: Food.com string like c("a","b")
    if isinstance(value, str):
        try:
            if value.startswith("c("):
                value = value.replace("c(", "[").replace(")", "]")

            if value.startswith("{") and value.endswith("}"):
                value = value.replace("{", "[").replace("}", "]")

            parsed = ast.literal_eval(value)
            return [str(x).strip() for x in parsed]

        except Exception:
            return []

    return []


def clean_steps(steps):
    return clean_foodcom_list(steps)


def infer_cuisine(tags=None, ingredients=None, name=None) -> str:
    text = " ".join(
        str(x).lower()
        for x in (tags or []) + (ingredients or []) + [name or ""]
    )

    CUISINE_KEYWORDS = {
        "Indian": ["curry", "masala", "garam", "paneer", "dal"],
        "Italian": ["pasta", "pizza", "basil", "parmesan"],
        "Chinese": ["soy", "noodle", "wok"],
        "Mexican": ["taco", "salsa", "tortilla"],
        "Mediterranean": ["olive oil", "feta", "hummus"],
    }

    for cuisine, keywords in CUISINE_KEYWORDS.items():
        if any(k in text for k in keywords):
            return cuisine

    return "General"
