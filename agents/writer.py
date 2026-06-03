from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


def writer_agent(state):

    query = state["query"]

    docs = state["retrieved_docs"]

    context = ""

    for doc in docs:

        context += f"""
        Source Title:
        {doc['title']}

        Source URL:
        {doc['url']}

        Content:
        {doc['text']}

        --------------------------
        """

    prompt = f"""
    You are a professional research analyst.

    Topic:
    {query}

    Sources:
    {context}

    Write a detailed research report with:

    1. Introduction
    2. Main Findings
    3. Challenges
    4. Future Outlook
    5. Conclusion

    Rules:
    - Use only the provided sources.
    - Mention source URLs when referencing important facts.
    - Do not make up information.
    - Keep the report professional and well-structured.
    """

    response = llm.invoke(prompt)

    return {
        "draft": response.content
    }