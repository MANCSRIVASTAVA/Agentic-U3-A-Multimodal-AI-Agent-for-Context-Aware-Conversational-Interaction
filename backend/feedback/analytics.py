from time import perf_counter
from .db import ch_client

def log_job(session_id: str, corr_id: str | None, stage: str, status: str, latency_ms: int, error_msg: str = ""):
    try:
        ch_client.insert(
            "analytics.feedback_jobs_log",
            [{"corr_id": corr_id or "", "session_id": session_id, "stage": stage, "status": status, "latency_ms": latency_ms, "error_msg": error_msg}],
            column_names=["corr_id","session_id","stage","status","latency_ms","error_msg"]
        )
    except Exception:
        # ClickHouse optional; ignore if not available
        pass

class StageTimer:
    def __init__(self, session_id: str, corr_id: str | None, stage: str):
        self.session_id, self.corr_id, self.stage = session_id, corr_id, stage
        self.t0 = perf_counter()
    def ok(self):
        ms = int((perf_counter() - self.t0) * 1000)
        log_job(self.session_id, self.corr_id, self.stage, "ok", ms)
    def error(self, msg: str):
        ms = int((perf_counter() - self.t0) * 1000)
        log_job(self.session_id, self.corr_id, self.stage, "error", ms, msg)
