# backend/utils/vector_store.py

import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

API_KEY = os.getenv("PINECONE_API_KEY")
REGION = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
INDEX_NAME = os.getenv("INDEX_NAME", "html-chunks")

if not API_KEY:
    raise RuntimeError("PINECONE_API_KEY is not set in .env")

pc = Pinecone(api_key=API_KEY)

# Create index if it doesn't exist
existing = pc.list_indexes().names()
if INDEX_NAME not in existing:
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=REGION),
    )

index = pc.Index(INDEX_NAME)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def insert_chunks(chunks):
    """
    chunks: list of {id, title, path, html, text}
    """
    vectors = []
    for ch in chunks:
        emb = model.encode(ch["text"]).tolist()
        vectors.append(
            (
                ch["id"],
                emb,
                {
                    "title": ch["title"],
                    "path": ch["path"],
                    "html": ch["html"],
                },
            )
        )

    if vectors:
        index.upsert(vectors=vectors)


def search_chunks(query: str, top_k: int = 10):
    """Semantic search over chunks and return formatted results."""
    q_vec = model.encode(query).tolist()
    res = index.query(vector=q_vec, top_k=top_k, include_metadata=True)

    formatted = []
    for match in res.matches:
        md = match.metadata or {}
        formatted.append(
            {
                "title": md.get("title", "Untitled section"),
                "path": md.get("path", "/"),
                "html": md.get("html", ""),
                "score": round(match.score * 100, 1),
            }
        )
    return formatted
