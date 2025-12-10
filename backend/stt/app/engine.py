# Simplified enriched engine stub for Phase 6 compatibility
import uuid, time
from dataclasses import dataclass

@dataclass
class EngineConfig:
    sample_rate:int=16000
    first_partial_sla_ms:int=800
    stall_timeout_sec:float=2.0
    backpressure_warn:int=25

class StreamingSTTEngine:
    def __init__(self,cfg:EngineConfig,session_id=None,correlation_id=None):
        self.cfg=cfg
        import random
        self.session_id=session_id or str(uuid.uuid4())
        self.correlation_id=correlation_id or str(uuid.uuid4())
        self.segment_counter=0
        self.closed=False
    def push_audio(self,chunk:bytes): pass
    def iter_events(self):
        # Dummy yield to show structure
        self.segment_counter+=1
        yield ("transcript.final",{"text":"hello world","language":"en",
            "segment_id":f"{self.session_id}-{self.segment_counter}",
            "session_id":self.session_id,"correlation_id":self.correlation_id,
            "engine":"whisper","fallback_used":False,"latency_ms":123})
    def close(self): self.closed=True
