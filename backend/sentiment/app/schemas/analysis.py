from pydantic import BaseModel, Field
from typing import Optional, List

class Prosody(BaseModel):
    pitch_hz: Optional[float] = Field(default=None, description="Fundamental frequency")
    energy_rms: Optional[float] = Field(default=None, description="Signal energy")
    speech_rate_wps: Optional[float] = Field(default=None, description="Words per second")

class AnalyzeRequest(BaseModel):
    text: str
    features: Optional[List[str]] = ["sentiment","emotion"]
    prosody: Optional[Prosody] = None
    return_style: bool = True

class StyleDirectives(BaseModel):
    style_enum: str
    system_instructions: str

class AnalyzeResponse(BaseModel):
    sentiment: Optional[str] = None
    emotion: Optional[str] = None
    valence: Optional[float] = None
    arousal: Optional[float] = None
    confidence: Optional[float] = None
    style_directives: Optional[StyleDirectives] = None
    meta: Optional[dict] = None
