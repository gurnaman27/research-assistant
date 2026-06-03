import os
import uuid

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from rag.qdrant_store import create_collection

# Lightweight OpenAI embeddings — no PyTorch, no heavy dependencies
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

_qdrant_url = os.getenv("QDRANT_URL")
client = QdrantClient(url=_qdrant_url, api_key=os.getenv("QDRANT_API_KEY")) \
    if _qdrant_url else \
    QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=6333)


def get_embedding(text: str) -> list:
    """Get embedding vector from OpenAI text-embedding-3-small."""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def index_documents(results):
    # Create collection on first use
    create_collection()

    points = []

    for item in results:
        text = item.get("content", "")
        if not text:
            continue

        vector = get_embedding(text)

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": text,
                    "url": item.get("url", ""),
                    "title": item.get("title", "")
                }
            )
        )

    if points:
        client.upsert(
            collection_name="research_docs",
            points=points
        )

    print("Documents Indexed")


def retrieve_docs(query):

    query_vector = get_embedding(query)

    results = client.query_points(
        collection_name="research_docs",
        query=query_vector,
        limit=5
    ).points

    docs = []

    for item in results:
        docs.append(
            {
                "title": item.payload.get("title", ""),
                "url": item.payload.get("url", ""),
                "text": item.payload.get("text", "")
            }
        )

    return docs