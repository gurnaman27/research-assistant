import os
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams
)

_url = os.getenv("QDRANT_URL")
_api_key = os.getenv("QDRANT_API_KEY")

if _url:
    # Qdrant Cloud
    client = QdrantClient(url=_url, api_key=_api_key)
else:
    # Local Docker
    client = QdrantClient(
        host=os.getenv("QDRANT_HOST", "localhost"),
        port=6333
    )

def create_collection():

    collections = client.get_collections()

    names = [
        c.name
        for c in collections.collections
    ]

    if "research_docs" not in names:

        client.create_collection(
            collection_name="research_docs",
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )

        print("Collection Created")

    else:
        print("Collection Already Exists")