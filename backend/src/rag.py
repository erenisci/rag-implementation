import os

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.embedding import get_chroma_client
from src.settings import settings


def initialize_chain():
    """Initializes the AI model and retriever only when an API key is provided."""
    global chain
    api_key = os.getenv("API_KEY")

    if not api_key:
        print("Warning: No OpenAI API Key set. Model will not be initialized.")
        return None, None, None

    embedding_model = OpenAIEmbeddings(
        model=settings["EMBEDDING_MODEL"], openai_api_key=api_key)
    client, _ = get_chroma_client()

    vector_db = Chroma(
        client=client,
        collection_name=settings["COLLECTION_NAME"],
        embedding_function=embedding_model
    )

    retriever = vector_db.as_retriever(
        search_type="mmr", search_kwargs={"k": 20, "fetch_k": 100})
    llm = ChatOpenAI(model=settings["MODEL"], api_key=api_key, temperature=0.7)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", settings["SYSTEM_PROMPT"] +
             ". Document Context: {context}"),
            ("user", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)

    return llm, retriever, chain


_, _, chain = initialize_chain()
