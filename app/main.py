from fastapi import FastAPI
from app.api import register, ingest, chat

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.include_router(register.router, prefix="/api")
app.include_router(ingest.router, prefix="/api")
app.include_router(chat.router, prefix="/api")