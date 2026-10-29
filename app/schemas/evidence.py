from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EvidenceBase(BaseModel):
    original_filename: str
    file_size: int
    mime_type: str
    sha256_hash: str
    status: str
    has_extractable_text: bool


class EvidenceResponse(EvidenceBase):
    id: int
    stored_filename: str
    created_at: datetime
    extraction_notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class EvidenceMappingCreate(BaseModel):
    evidence_id: int
    requirement_id: Optional[int] = None
    control_id: Optional[int] = None
    reason: Optional[str] = None
    quote: Optional[str] = None
