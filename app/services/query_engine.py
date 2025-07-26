import os, pickle
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings


load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

VECTOR_DIR = "vectorstores"

def query_company_knowledge(slug: str, question: str):
    path = os.path.join(VECTOR_DIR, f"{slug}.pkl")
    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        vectordb = pickle.load(f)

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=OPENROUTER_API_KEY,
        model="mistralai/mistral-7b-instruct:free",  # or "gpt-4", "gemini-pro"
        temperature=0
    )

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa.run(question)
