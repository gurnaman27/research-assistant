from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def critic_agent(state):

    draft = state["draft"]

    prompt = f"""
    Review the report below.

    Check:

    - Completeness
    - Clarity
    - Missing sections
    - Factual consistency

    Report:

    {draft}

    Return an improved version.
    """

    response = llm.invoke(prompt)

    return {
        "final_report": response.content
    }