from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Graph is initialized after uvicorn binds the port
_graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load heavy resources after the port is bound, not before."""
    global _graph
    from graph.workflow import graph
    _graph = graph
    yield


app = FastAPI(
    title="Multi-Agent Research Assistant",
    description="Autonomous research assistant using LangGraph",
    version="1.0.0",
    lifespan=lifespan
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
        result = _graph.invoke({"query": request.query})
        return {
            "query": request.query,
            "report": result["final_report"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(e)}"
        )