"""
FAISS-based Vector Search Engine
backend/scripts/build_faiss_index.py

High-accuracy semantic search using FAISS
"""

import numpy as np
import faiss
import pickle
from pathlib import Path

# =====================================================
# PATH SETUP
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml_models"

# =====================================================
# FAISS SEARCH ENGINE
# =====================================================

class FAISSSearchEngine:
    """Fast semantic search using FAISS"""

    def __init__(self):
        self.index = None
        self.recipe_ids = None
        self.metadata = None

    # ----------------------------
    # BUILD INDEX
    # ----------------------------

    def build_index(self, embeddings_file="recipe_embeddings.npy"):
        print("=" * 70)
        print("🏗️  Building FAISS Index")
        print("=" * 70)

        print("\n📦 Loading embeddings...")
        embeddings = np.load(MODEL_PATH / embeddings_file)
        print(f"   ✅ Loaded {embeddings.shape[0]} vectors")
        print(f"   📐 Dimension: {embeddings.shape[1]}")

        with open(MODEL_PATH / "recipe_id_to_index.pkl", "rb") as f:
            self.recipe_ids = pickle.load(f)

        with open(MODEL_PATH / "recipe_metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)

        dimension = embeddings.shape[1]

        print("\n🔨 Creating FAISS index...")

        if len(embeddings) < 10000:
            print("   Using IndexFlatIP (exact cosine similarity)")
            self.index = faiss.IndexFlatIP(dimension)
        else:
            print("   Using IndexIVFFlat (approximate search)")
            nlist = min(100, len(embeddings) // 10)
            quantizer = faiss.IndexFlatIP(dimension)
            self.index = faiss.IndexIVFFlat(quantizer, dimension, nlist)

            print(f"   Training index with {nlist} clusters...")
            self.index.train(embeddings.astype("float32"))

        print("   Adding vectors to index...")
        self.index.add(embeddings.astype("float32"))

        if isinstance(self.index, faiss.IndexIVFFlat):
            self.index.nprobe = 10  # IMPORTANT for accuracy

        print(f"   ✅ Index built with {self.index.ntotal} vectors")

        index_file = MODEL_PATH / "faiss_index.bin"
        faiss.write_index(self.index, str(index_file))
        print(f"\n💾 Saved index: {index_file}")

        print("\n" + "=" * 70)
        print("✅ FAISS Index Ready!")
        print("=" * 70)

        return self.index

    # ----------------------------
    # SEARCH
    # ----------------------------

    def search(self, query_vector, k=10):
        if self.index is None:
            self.load_index()

        if len(query_vector.shape) == 1:
            query_vector = query_vector.reshape(1, -1)

        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(query_vector.astype("float32"), k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx < len(self.recipe_ids):
                meta = self.metadata[idx]
                results.append({
                    "recipe_id": self.recipe_ids[idx],
                    "score": float(score),
                    "name": meta["name"],
                    "cuisine": meta.get("cuisine"),
                    "minutes": meta.get("minutes"),
                    "nutrition": meta.get("nutrition"),
                    "ingredients": meta.get("ingredients"),
                    "tags": meta.get("tags"),
                })

        return results

    # ----------------------------
    # LOAD INDEX
    # ----------------------------

    def load_index(self):
        print("📦 Loading FAISS index...")

        self.index = faiss.read_index(str(MODEL_PATH / "faiss_index.bin"))

        if isinstance(self.index, faiss.IndexIVFFlat):
            self.index.nprobe = 10

        with open(MODEL_PATH / "recipe_id_to_index.pkl", "rb") as f:
            self.recipe_ids = pickle.load(f)

        with open(MODEL_PATH / "recipe_metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)

        print(f"   ✅ Loaded index with {self.index.ntotal} vectors")

# =====================================================
# TESTING
# =====================================================

def main():
    engine = FAISSSearchEngine()
    engine.build_index()

    print("\n🧪 Testing search...")
    print("=" * 70)

    embeddings = np.load(MODEL_PATH / "recipe_embeddings.npy")
    test_query = embeddings[0]

    results = engine.search(test_query, k=5)

    print("\n📋 Top 5 similar recipes:")
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['name']}")
        print(f"   Score: {r['score']:.4f}")
        print(f"   Cuisine: {r['cuisine']}")
        print(f"   Time: {r['minutes']} min")

if __name__ == "__main__":
    main()
