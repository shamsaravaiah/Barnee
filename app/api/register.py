from fastapi import APIRouter, HTTPException
from app.models.company import CompanyRegisterIn, CompanyRegisterOut
from app.core.utils import slugify
from app.core.database import db, save_db
import uuid

router = APIRouter()

@router.post("/company/register", response_model=CompanyRegisterOut)
def register_company(payload: CompanyRegisterIn):
    if not payload.company_name or payload.company_name.strip() == "":
        raise HTTPException(status_code=400, detail="Company name cannot be empty.")

    slug = slugify(payload.company_name)
    if slug in db:
        raise HTTPException(status_code=409, detail="Company already registered.")

    company_id = str(uuid.uuid4())
    db[slug] = {
        "id": company_id,
        "name": payload.company_name,
        "slug": slug
    }
    save_db()

    return {
        "message": f"Registration successful for '{payload.company_name}'.",
        "company_id": company_id,
        "company_slug": slug
        
    }



