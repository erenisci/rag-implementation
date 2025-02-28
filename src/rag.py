import os

from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import config


load_dotenv()

embedding_model = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
vector_db = Chroma(
    collection_name=config.COLLECTION_NAME,
    embedding_function=embedding_model,
    persist_directory="data/chroma_db",
)

llm = ChatOpenAI(
    model=config.GPT_MODEL, api_key=os.getenv("OPENAI_API_KEY"), temperature=0.7
)

retriever = vector_db.as_retriever(search_kwargs={"k": 3})

system_prompt = (
    "You are an AI assistant that answers user questions strictly based on the provided document. "
    "ONLY use the given document context to generate responses. "
    "Do NOT use external knowledge, make assumptions, or generate false information. "
    "If the document does not contain enough information to answer the question, simply state that you don't know. "
    "Keep your answers clear, accurate, and concise, with a maximum of five sentences. "
    "Maintain a professional yet friendly tone. "
    "Document Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, question_answer_chain)


def ask_question(question):
    """Takes a user query, searches ChromaDB, and generates an LLM response."""
    response = chain.invoke({"input": question})

    return response["answer"]
