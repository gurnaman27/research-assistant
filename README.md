# 🔬 Autonomous Multi-Agent Research Assistant

A collaborative multi-agent system using **LangGraph** featuring Planner, Search, Writer, and Critic agents to fully automate deep research and draft comprehensive reports.

## Architecture

```
User Query → Planner → Search (Tavily) → RAG Retriever (Qdrant) → Writer → Critic → Final Report
```

**Agents:**
- **Planner** — Breaks the research topic into structured sections
- **Search** — Gathers sources via Tavily API with Redis caching
- **RAG Retriever** — Indexes documents in Qdrant and retrieves the most relevant content
- **Writer** — Drafts a comprehensive, sourced research report
- **Critic** — Reviews and improves the draft for completeness and accuracy

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Orchestration | LangGraph |
| LLM | GPT-4o-mini (OpenAI) |
| Web Search | Tavily API |
| Vector Database | Qdrant |
| Caching | Redis |
| API Framework | FastAPI |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Containerization | Docker Compose |

## Quick Start

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key
- Tavily API Key

### Run

```bash
# Set your API keys
export OPENAI_API_KEY=your_key
export TAVILY_API_KEY=your_key

# Launch all services
docker compose up --build
```

Open **http://localhost:8000** in your browser.

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web UI |
| `POST` | `/research` | Run research pipeline |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Swagger API docs |

### Example API Call

```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"query": "Future of AI in Healthcare"}'
```

## Project Structure

```
├── agents/
│   ├── planner.py      # Research planning agent
│   ├── search.py       # Web search agent (Tavily + Redis cache)
│   ├── writer.py       # Report writing agent
│   └── critic.py       # Report review agent
├── graph/
│   └── workflow.py     # LangGraph state machine
├── rag/
│   ├── qdrant_store.py # Qdrant collection management
│   └── retriever.py    # Document indexing & retrieval
├── cache/
│   └── redis_client.py # Redis client
├── api/
│   └── main.py         # FastAPI application
├── static/
│   ├── index.html      # Frontend UI
│   ├── styles.css      # Styles
│   └── script.js       # Frontend logic
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
