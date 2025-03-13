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
    api_key = os.getenv("API_KEY")
    
    if not api_key:
        print("Warning: No OpenAI API Key set. Model will not be initialized.")
        return None, None, None
    
    embedding_model = OpenAIEmbeddings(model=settings["EMBEDDING_MODEL"], openai_api_key=api_key)
    client, _ = get_chroma_client()
    
    vector_db = Chroma(
        client=client,
        collection_name=settings["COLLECTION_NAME"],
        embedding_function=embedding_model
    )

    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model=settings["MODEL"], api_key=api_key, temperature=0.7)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", settings["SYSTEM_PROMPT"] + ". Document Context: {context}"),
            ("user", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return llm, retriever, chain


def ask_question(question):
    """Handles question processing only if the model is initialized."""
    llm, retriever, chain = initialize_chain()
    
    if not os.getenv("API_KEY"):
        return "API Key is missing. Please update the settings."
    
    if not llm or not retriever:
        return "ChromaDB is not properly initialized. Please update the settings."

    try:
        response = chain.invoke({"input": question})
        return response["answer"]
    except Exception as e:
        return f"Error processing question: {e}"