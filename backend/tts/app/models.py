from pydantic import BaseModel
from typing import Optional

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None
    format: str = "mp3"
    correlation_id: Optional[str] = None
    session_id: Optional[str] = None
