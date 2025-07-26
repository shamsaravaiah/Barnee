# 📁 app/chains/qa_chains.py

import os
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Load API key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

company_chains = {}


# Embedding model
embedding = OpenAIEmbeddings(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=OPENROUTER_API_KEY
)

# LLM model
llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=OPENROUTER_API_KEY,
    model="mistral-7b",  # you can also try gpt-4 or gemini-pro
    temperature=0.3
)

def get_prompt(company_name: str) -> PromptTemplate:
    return PromptTemplate.from_template(f"""
You are {company_name}'s intelligent assistant.

Use the context to help users with product or service questions. Be honest. Do not make up facts and reply in accurate swedish.

Context:
{{context}}

Customer Question:
{{question}}

Response:
""")

def load_company_chain(company_id: str):
    vector_path = f"vector_stores/{company_id}"
    vs = FAISS.load_local(vector_path, embeddings=embedding, allow_dangerous_deserialization=True)
    retriever = vs.as_retriever(search_kwargs={"k": 5})
    prompt = get_prompt(company_id.capitalize())

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=False,
        combine_docs_chain_kwargs={"prompt": prompt}
    )

    return {"chain": chain, "memory": memory, "question_count": 0}

# Preload chains
company_chains = {
    "aprobo": load_company_chain("aprobo_en"),
    "stim": load_company_chain("stim"),
    "youngstival": load_company_chain("youngstival"),
}

def answer_company_question(company: str, question: str) -> str:
    if company not in company_chains:
        company_chains[company] = load_company_chain(company)

    session = company_chains[company]

    if session["question_count"] >= 5:
        return "You've reached the free limit. Want more? Contact us."

    session["question_count"] += 1

    result = session["chain"].invoke({"question": question})
    return result.get("answer") or result.get("result") or "No answer found."
