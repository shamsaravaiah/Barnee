import os, pickle, requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from app.services.embedding import embedding_model


VECTOR_DIR = "vectorstores"
os.makedirs(VECTOR_DIR, exist_ok=True)

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def _store_vectorstore(slug: str, docs: list):
 
    vectordb = FAISS.from_documents(docs, embedding_model)
    with open(os.path.join(VECTOR_DIR, f"{slug}.pkl"), "wb") as f:
        pickle.dump(vectordb, f)

def _text_to_docs(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100) # Adjust chunk size and overlap as needed
    return splitter.create_documents([text])

def ingest_text(slug: str, raw_text: str):
    docs = _text_to_docs(raw_text)
    _store_vectorstore(slug, docs)
    return {"status": "text ingested"}

def ingest_url(slug: str, url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    docs = _text_to_docs(text)
    _store_vectorstore(slug, docs)
    return {"status": "url ingested"}

def ingest_file(slug: str, file):
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
    else:
        text = file.file.read().decode("utf-8")
    docs = _text_to_docs(text)
    _store_vectorstore(slug, docs)
    return {"status": "file ingested"}

def ingest_api(slug: str, api_url: str):
    response = requests.get(api_url)
    text = response.text
    docs = _text_to_docs(text)
    _store_vectorstore(slug, docs)
    return {"status": "api response ingested"}
