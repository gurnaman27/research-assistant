import threading

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(
    title="Multi-Agent Research Assistant",
    description="Autonomous research assistant using LangGraph",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# Graph initialized lazily on first request (not at startup)
# so uvicorn binds the port immediately and Render can detect it
_graph = None
_graph_lock = threading.Lock()


def get_graph():
    global _graph
    if _graph is None:
        with _graph_lock:
            if _graph is None:
                from graph.workflow import graph
                _graph = graph
    return _graph


class ResearchRequest(BaseModel):
    query: str


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "research-assistant",
        "version": "1.0.0"
    }


@app.post("/research")
def research(request: ResearchRequest):
    try:
        result = get_graph().invoke({"query": request.query})
        return {
            "query": request.query,
            "report": result["final_report"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(e)}"
        )