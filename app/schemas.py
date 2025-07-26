from pydantic import BaseModel

class IngestRequest(BaseModel):
    source_text: str
