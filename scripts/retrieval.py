"""
TripLens - Semantic Candidate Retrieval
Queries ChromaDB for top-K semantically similar packages, then hydrates
each hit with its row from packages_enriched (real feature data — no
invented fields).
"""
import sqlite3
import os
import re
import chromadb
from chromadb.utils import embedding_functions

from config.ranking_weights import RETRIEVAL_TOP_K

DB_PATH = "database/triplens.db"
CHROMA_PATH = "database/chroma_db"

_collection = None


def _get_collection():
    """Load embeddings only when semantic search is actually requested.

    The app remains usable in offline demonstrations when the embedding model
    is not already cached locally.
    """
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        _collection = client.get_or_create_collection(
            name="travel_packages", embedding_function=embedding_func
        )
    return _collection


def build_semantic_query(prefs: dict, original_prompt: str) -> str:
    """Prefer the user's own words for semantic search (captures nuance
    like 'peaceful trip surrounded by greenery') over a re-templated string."""
    return original_prompt


def get_candidates(prefs: dict, original_prompt: str, top_k: int = RETRIEVAL_TOP_K):
    query_text = build_semantic_query(prefs, original_prompt)
    # Default to the local, deterministic path. Enable semantic retrieval only
    # where the model is intentionally provisioned (e.g. deployment/CI).
    if os.getenv("TRIPLENS_USE_SEMANTIC_RETRIEVAL") != "1":
        return _get_lexical_candidates(query_text, top_k)
    try:
        results = _get_collection().query(query_texts=[query_text], n_results=top_k)
    except Exception:
        # Deterministic offline fallback: rank real package rows by overlap with
        # the user's words. This does not create or substitute package data.
        return _get_lexical_candidates(query_text, top_k)

    ids = results["ids"][0]
    distances = results["distances"][0]
    # Chroma returns cosine distance; convert to a 0-1 similarity score
    similarity_by_id = {
        pkg_id: max(0.0, 1.0 - dist) for pkg_id, dist in zip(ids, distances)
    }

    if not ids:
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    placeholders = ",".join("?" for _ in ids)
    rows = conn.execute(
        f"SELECT * FROM packages_enriched WHERE package_id IN ({placeholders})",
        ids,
    ).fetchall()
    conn.close()

    candidates = []
    for row in rows:
        pkg = dict(row)
        pkg["semantic_similarity"] = similarity_by_id.get(pkg["package_id"], 0.0)
        candidates.append(pkg)

    return candidates


def _get_lexical_candidates(query_text: str, top_k: int) -> list:
    tokens = {t for t in re.findall(r"[a-zA-Z]{3,}", query_text.lower())}
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM packages").fetchall()
    conn.close()

    scored = []
    for row in rows:
        pkg = dict(row)
        pkg["theme_clean"] = str(pkg.get("theme") or "").lower().strip()
        pkg["itinerary_pace_inferred"] = pkg.get("itinerary_pace") or "Moderate"
        searchable = " ".join(str(pkg.get(key) or "") for key in (
            "package_name", "destinations", "theme_clean", "suited_for",
            "itinerary_pace_inferred", "start_location"
        )).lower()
        matches = sum(token in searchable for token in tokens)
        pkg["semantic_similarity"] = matches / max(len(tokens), 1)
        scored.append(pkg)
    scored.sort(key=lambda pkg: pkg["semantic_similarity"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    from scripts.preference_extraction import extract_preferences

    sample = "I want a relaxed 5-day Kerala trip from Kochi for 2 people under ₹30,000 with beaches, nature and sightseeing."
    prefs = extract_preferences(sample)
    candidates = get_candidates(prefs, sample, top_k=5)
    for c in candidates:
        print(c["package_id"], c["package_name"], "| sim:", round(c["semantic_similarity"], 3), "| price:", c["price"])
