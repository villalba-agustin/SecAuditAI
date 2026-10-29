from typing import Optional

from pydantic import BaseModel


class SoAFilter(BaseModel):
    category: Optional[str] = None
    is_applicable: Optional[bool] = None
    implementation_status: Optional[str] = None
    search: Optional[str] = None
