from typing import Dict, Any, List
from sqlalchemy import text
from .db import SessionLocal

async def insert_report(report: Dict[str, Any]) -> None:
    q = text("""    INSERT INTO feedback_reports
    (id, session_id, overall_score, prosody_score, clarity_score, etiquette_score,
     summary_md, report_json, report_url_md, report_url_pdf)
    VALUES (gen_random_uuid(), :session_id, :overall, :prosody, :clarity, :etiquette,
            :summary_md, :report_json::jsonb, :report_url_md, :report_url_pdf)
    """)
    async with SessionLocal() as s:
        await s.execute(q, {
            "session_id": report["session_id"],
            "overall": report["scores"]["overall"],
            "prosody": report["scores"]["prosody"],
            "clarity": report["scores"]["clarity"],
            "etiquette": report["scores"]["etiquette"],
            "summary_md": report["summary_md"],
            "report_json": report["report_json"],
            "report_url_md": report.get("report_url_md"),
            "report_url_pdf": report.get("report_url_pdf"),
        })
        await s.commit()

async def insert_features(session_id: str, features: Dict[str, Any]) -> None:
    rows: List[Dict[str, Any]] = []
    for group, kv in features.items():
        if group == "meta":
            continue
        for name, val in kv.items():
            rows.append({"session_id": session_id, "feature_group": group, "feature_name": name, "feature_value": float(val)})
    if not rows:
        return
    async with SessionLocal() as s:
        await s.execute(text("""        INSERT INTO feedback_features (session_id, feature_group, feature_name, feature_value)
        VALUES (:session_id, :feature_group, :feature_name, :feature_value)
        """), rows)
        await s.commit()

async def get_report(session_id: str) -> Dict[str, Any] | None:
    q = text("""    SELECT session_id, overall_score, prosody_score, clarity_score, etiquette_score,
           summary_md, report_json, report_url_md, report_url_pdf
    FROM feedback_reports WHERE session_id = :session_id
    """)
    async with SessionLocal() as s:
        res = await s.execute(q, {"session_id": session_id})
        row = res.mappings().first()
        return dict(row) if row else None
