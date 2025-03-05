from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.settings import settings


# Check if API Key exists
openai_api_key = settings.get("API_KEY", "")

if not openai_api_key:
    print("⚠️ Warning: No OpenAI API Key set. Model will not be initialized.")
    llm = None
    embedding_model = None
else:
    # Initialize OpenAI embeddings with API Key
    embedding_model = OpenAIEmbeddings(
        model=settings["EMBEDDING_MODEL"], openai_api_key=openai_api_key
    )

    vector_db = Chroma(
        collection_name=settings["COLLECTION_NAME"],
        embedding_function=embedding_model,
        persist_directory=settings["CHROMA_DB_DIR"],
    )

    llm = ChatOpenAI(model=settings["MODEL"], api_key=openai_api_key, temperature=0.7)

retriever = vector_db.as_retriever(search_kwargs={"k": 3}) if llm else None

prompt = (
    ChatPromptTemplate.from_messages(
        [
            ("system", settings["SYSTEM_PROMPT"]),
            ("user", "{input}"),
        ]
    )
    if llm
    else None
)

question_answer_chain = create_stuff_documents_chain(llm, prompt) if llm else None
chain = create_retrieval_chain(retriever, question_answer_chain) if llm else None


def ask_question(question):
    """Handles question processing only if the model is initialized."""
    if not llm:
        return "⚠️ API Key is missing. Please update it in the settings."

    response = chain.invoke({"input": question})
    return response["answer"]
