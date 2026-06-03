import os
import json

from dotenv import load_dotenv
from tavily import TavilyClient

from cache.redis_client import redis_client

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def search_agent(state):

    query = state["query"]

    # Try cache first, but don't fail if Redis is down
    try:
        cached_results = redis_client.get(query)

        if cached_results:

            print("Retrieved from Redis Cache")

            return {
                "search_results":
                json.loads(cached_results)
            }

    except Exception as e:
        print(f"Redis unavailable, skipping cache: {e}")

    results = client.search(
        query=query,
        max_results=5
    )

    # Try to cache results, but don't fail if Redis is down
    try:
        redis_client.set(
            query,
            json.dumps(results["results"]),
            ex=3600
        )
    except Exception as e:
        print(f"Redis cache write failed: {e}")

    print("Retrieved from Tavily")

    return {
        "search_results":
        results["results"]
    }