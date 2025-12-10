from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SessionBundleRef(BaseModel):
    session_id: str
    corr_id: Optional[str] = None
    transcript_uri: Optional[str] = None
    audio_uri: Optional[str] = None
    consent_audio_analytics: bool = True

class FeatureVector(BaseModel):
    prosody: Dict[str, float] = Field(default_factory=dict)
    text: Dict[str, float] = Field(default_factory=dict)
    meta: Dict[str, Any] = Field(default_factory=dict)

class FeedbackScores(BaseModel):
    overall: float
    prosody: float
    clarity: float
    etiquette: float

class FeedbackReport(BaseModel):
    session_id: str
    scores: FeedbackScores
    tips: List[str]
    summary_md: str
    report_json: Dict[str, Any]
    report_url_md: Optional[str] = None
    report_url_pdf: Optional[str] = None
