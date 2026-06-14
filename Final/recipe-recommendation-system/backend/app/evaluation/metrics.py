from typing import List, Set

# -----------------------------
# Precision@K
# -----------------------------
def precision_at_k(
    recommended: List[int],
    relevant: Set[int],
    k: int
) -> float:
    """
    Precision@K = Relevant recipes in top K / K
    """
    if not recommended or k == 0:
        return 0.0

    recommended_k = recommended[:k]
    hits = len(set(recommended_k) & relevant)

    return round(hits / k, 4)


# -----------------------------
# Recall@K
# -----------------------------
def recall_at_k(
    recommended: List[int],
    relevant: Set[int],
    k: int
) -> float:
    """
    Recall@K = Relevant recipes in top K / Total relevant recipes
    """
    if not relevant:
        return 0.0

    recommended_k = recommended[:k]
    hits = len(set(recommended_k) & relevant)

    return round(hits / len(relevant), 4)


# -----------------------------
# F1 Score
# -----------------------------
def f1_score(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return round(
        2 * (precision * recall) / (precision + recall),
        4
    )


# -----------------------------
# Coverage
# -----------------------------
def catalog_coverage(
    recommended_items: Set[int],
    total_items: int
) -> float:
    """
    Coverage = unique recommended recipes / total recipes
    """
    if total_items == 0:
        return 0.0

    return round(len(recommended_items) / total_items, 4)
