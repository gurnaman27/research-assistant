from graph.workflow import graph

result = graph.invoke(
    {
        "query":
        "Future of AI in Healthcare"
    }
)

print(
    result["final_report"]
)