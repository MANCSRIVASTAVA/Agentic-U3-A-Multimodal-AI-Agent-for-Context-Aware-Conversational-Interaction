import asyncio, json
import redis.asyncio as aioredis
from .config import settings
from .features_audio import analyze as analyze_audio
from .features_text import analyze as analyze_text
from .scoring import score
from .repository import insert_report, insert_features
from .analytics import StageTimer
from .eventbus import publish
from .report import make_report_payload

async def _process_session(bundle_json: str):
    bundle = json.loads(bundle_json)
    session_id = bundle["session_id"]; corr_id = bundle.get("corr_id")
    # 1) Fetch data (replace with actual fetches from your stores)
    t_ingest = StageTimer(session_id, corr_id, "ingest")
    transcript_text = bundle.get("transcript_text", "")
    audio_duration = float(bundle.get("audio_duration_sec", 0))
    words_count = len(transcript_text.split())
    pauses_sec = bundle.get("pauses_sec", [])
    t_ingest.ok()

    # 2) Feature extraction
    t_audio = StageTimer(session_id, corr_id, "audio_features")
    prosody = analyze_audio(audio_duration, words_count, pauses_sec)
    t_audio.ok()

    t_text = StageTimer(session_id, corr_id, "text_features")
    textf = analyze_text(transcript_text)
    t_text.ok()

    # 3) Scoring
    t_scoring = StageTimer(session_id, corr_id, "scoring")
    scores = score(prosody, textf)
    t_scoring.ok()

    # 4) Report (LLM narrative if available, else rule-based)
    payload, md, tips = await make_report_payload(session_id, prosody, textf, scores)

    # Persist
    await insert_features(session_id, {"prosody": prosody, "text": textf})
    await insert_report({
        "session_id": session_id,
        "scores": scores,
        "summary_md": payload["summary_md"],
        "report_json": payload["report_json"],
        "report_url_md": None,
        "report_url_pdf": None,
    })

    # 5) Notify SSE subscribers
    await publish(session_id, {"event": "feedback.ready", "session_id": session_id, "scores": scores})

async def consumer_loop():
    r = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    stream = settings.REDIS_STREAM_SESSION_COMPLETED
    last_id = "$"
    while True:
        events = await r.xread({stream: last_id}, block=10000, count=10)
        if not events:
            await asyncio.sleep(0.2); continue
        for _, msgs in events:
            for msg_id, fields in msgs:
                last_id = msg_id
                bundle_json = fields.get("data") or fields.get("bundle") or "{}"
                try:
                    await _process_session(bundle_json)
                except Exception as e:
                    # TODO: log error, write to ClickHouse
                    pass
