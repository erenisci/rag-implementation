from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.embedding import client
from src.settings import settings


openai_api_key = settings.get("API_KEY", "")

if not openai_api_key:
    print("Warning: No OpenAI API Key set. Model will not be initialized.")
    llm = None
    retriever = None
    chain = None
else:
    embedding_model = OpenAIEmbeddings(model=settings["EMBEDDING_MODEL"], openai_api_key=openai_api_key)

    vector_db = Chroma(
        client=client,
        collection_name=settings["COLLECTION_NAME"],
        embedding_function=embedding_model
    )

    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model=settings["MODEL"], api_key=openai_api_key, temperature=0.7)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", settings["SYSTEM_PROMPT"] + ". Document Context: {context}"),
            ("user", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)

def ask_question(question):
    """Handles question processing only if the model is initialized."""
    if not llm or not retriever:
        return "API Key is missing or ChromaDB is not properly initialized. Please update the settings."

    try:
        response = chain.invoke({"input": question})
        return response["answer"]
    except Exception as e:
        return f"Error processing question: {e}"
