from pydantic import BaseModel

class CompanyRegisterIn(BaseModel):
    company_name: str

class CompanyRegisterOut(BaseModel):
    company_id: str
    company_slug: str
