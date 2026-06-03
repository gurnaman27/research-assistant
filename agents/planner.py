from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def planner_agent(state):

    query = state["query"]

    prompt = f"""
    Create a research plan for:

    {query}

    Break it into sections.
    """

    response = llm.invoke(prompt)

    return {
        "plan": response.content
    }