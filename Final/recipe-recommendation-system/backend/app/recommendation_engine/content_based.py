from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-mpnet-base-v2")

def build_embeddings(recipes):
    texts = [
        f"{r.name}. {' '.join(r.ingredients or [])}. {r.description or ''}"
        for r in recipes
    ]
    embeddings = model.encode(texts, show_progress_bar=True)
    return np.array(embeddings).astype("float32")

def build_faiss_index(embeddings):
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index

def get_similar_recipes(query_text, recipes, index, embeddings, top_k=10):
    query_vec = model.encode([query_text]).astype("float32")
    distances, indices = index.search(query_vec, top_k)
    return [recipes[i] for i in indices[0]]

