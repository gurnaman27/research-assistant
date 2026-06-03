from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END

from agents.planner import planner_agent
from agents.search import search_agent
from agents.writer import writer_agent
from agents.critic import critic_agent

from rag.retriever import (
    index_documents,
    retrieve_docs
)
class ResearchState(TypedDict):

    query: str

    plan: str

    search_results: list

    retrieved_docs: list

    draft: str

    final_report: str

def retrieval_node(state):

    index_documents(
        state["search_results"]
    )

    docs = retrieve_docs(
        state["query"]
    )

    return {
        "retrieved_docs": docs
    }
builder = StateGraph(
    ResearchState
)
builder.add_node(
    "planner",
    planner_agent
)

builder.add_node(
    "search",
    search_agent
)

builder.add_node(
    "retriever",
    retrieval_node
)

builder.add_node(
    "writer",
    writer_agent
)

builder.add_node(
    "critic",
    critic_agent
)
builder.set_entry_point(
    "planner"
)

builder.add_edge(
    "planner",
    "search"
)

builder.add_edge(
    "search",
    "retriever"
)

builder.add_edge(
    "retriever",
    "writer"
)

builder.add_edge(
    "writer",
    "critic"
)

builder.add_edge(
    "critic",
    END
)
graph = builder.compile()