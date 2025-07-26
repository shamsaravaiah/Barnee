from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest
from app.services.query_engine import query_company_knowledge

router = APIRouter()

@router.post("/chat/{company_slug}")
def chat(company_slug: str, payload: ChatRequest):
    if not payload.question or payload.question.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        result = query_company_knowledge(company_slug, payload.question)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No knowledge base found for company '{company_slug}'. Please ingest data first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    if result is None:
        raise HTTPException(status_code=404, detail="Knowledge base found but failed to retrieve answer.")

    return {"response": result}