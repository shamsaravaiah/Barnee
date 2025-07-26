from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.ingestion import ingest_text, ingest_url, ingest_file, ingest_api
from app.schemas import IngestRequest

router = APIRouter()
BASE_URL = "https://barnee.onrender.com"

@router.post("/ingest/{company_slug}/text")
def ingest_raw_text(company_slug: str, payload: IngestRequest):
    result = ingest_text(company_slug, payload.source_text)
    return JSONResponse({
        **result,
        "chat_url": f"{BASE_URL}/api/chat/{company_slug}"
    })

@router.post("/ingest/{company_slug}/url")
def ingest_from_url(company_slug: str, url: str = Form(...)):
    result = ingest_url(company_slug, url)
    return JSONResponse({
        **result,
        "chat_url": f"{BASE_URL}/api/chat/{company_slug}"
    })

@router.post("/ingest/{company_slug}/file")
def ingest_from_file(company_slug: str, file: UploadFile = File(...)):
    result = ingest_file(company_slug, file)
    return JSONResponse({
        **result,
        "chat_url": f"{BASE_URL}/api/chat/{company_slug}"
    })

@router.post("/ingest/{company_slug}/api")
def ingest_from_api(company_slug: str, api_url: str = Form(...)):
    result = ingest_api(company_slug, api_url)
    return JSONResponse({
        **result,
        "chat_url": f"{BASE_URL}/api/chat/{company_slug}"
    })
