from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from graph.workflow import graph

app = FastAPI(
    title="Multi-Agent Research Assistant",
    description="Autonomous research assistant using LangGraph with Planner, Search, Writer, and Critic agents",
    version="1.0.0"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


class ResearchRequest(BaseModel):
    query: str


@app.get("/")
def serve_frontend():
    """Serve the main UI."""
    return FileResponse("static/index.html")


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "research-assistant",
        "version": "1.0.0"
    }


@app.post("/research")
def research(request: ResearchRequest):
    """Run the full multi-agent research pipeline."""

    try:
        result = graph.invoke(
            {
                "query": request.query
            }
        )

        return {
            "query": request.query,
            "report":
            result["final_report"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(e)}"
        )