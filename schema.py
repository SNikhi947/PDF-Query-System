from pydantic import BaseModel
from typing import Optional

class Entity(BaseModel):
    condition: Optional[str]
    document_section: Optional[str]

class ParsedQuery(BaseModel):
    intent: str
    entity: Entity