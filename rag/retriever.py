import os
from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient

from qdrant_client.models import PointStruct
import uuid

from rag.qdrant_store import create_collection


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY")) \
    if os.getenv("QDRANT_URL") else \
    QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=6333)

# Ensure the collection exists before indexing (called lazily)


def index_documents(results):
    # Create collection on first use
    create_collection()

    texts = [
        item.get("content", "")
        for item in results
    ]

    vectors = model.encode(texts)

    points = []

    for i, item in enumerate(results):

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vectors[i].tolist(),
                payload={
                    "text": item.get("content", ""),
                    "url": item.get("url", ""),
                    "title": item.get("title", "")
                }
            )
        )

    client.upsert(
        collection_name="research_docs",
        points=points
    )

    print("Documents Indexed")


def retrieve_docs(query):

    query_vector = model.encode(
        query
    )

    results = client.query_points(
        collection_name="research_docs",
        query=query_vector.tolist(),
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