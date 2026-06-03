import os
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams
)

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
                size=384,
                distance=Distance.COSINE
            )
        )

        print("Collection Created")

    else:
        print("Collection Already Exists")