from typing import Dict, List, Tuple
from .llm_client import narrate_with_llm

def tips_from_features(p: Dict[str, float], t: Dict[str, float]) -> List[str]:
    tips = []
    if p.get("speech_rate_wpm", 130) > 180: tips.append("Slow down slightly to improve clarity.")
    if p.get("pause_ratio", 0.1) > 0.25: tips.append("Reduce long pauses; aim for steady flow.")
    if t.get("filler_ratio", 0.02) > 0.05: tips.append("Cut filler words (um/uh/like) to sound more confident.")
    if t.get("readability_fkgl", 8) > 12: tips.append("Simplify wording for easier comprehension.")
    if not tips: tips.append("Great pacing and clarity — keep it up!")
    return tips[:3]

def mk_markdown(session_id: str, scores: Dict[str, float], p: Dict[str, float], t: Dict[str, float], tips: List[str]) -> str:
    return f"""# Feedback Report — Session {session_id}

**Overall Score:** {scores['overall']:.1f}/100  
**Prosody:** {scores['prosody']:.1f} | **Clarity:** {scores['clarity']:.1f} | **Etiquette:** {scores['etiquette']:.1f}

## Key Metrics
- Speech rate: {p.get('speech_rate_wpm','?')} wpm
- Pause ratio: {p.get('pause_ratio','?')}
- Readability (FKGL): {t.get('readability_fkgl','?')}
- Filler ratio: {t.get('filler_ratio','?')}

## Top Tips
- {tips[0] if len(tips)>0 else ''}
- {tips[1] if len(tips)>1 else ''}
- {tips[2] if len(tips)>2 else ''}

*Generated automatically from your conversation transcript and audio signals.*
"""

async def make_report_payload(session_id: str, prosody: Dict[str, float], text: Dict[str, float], scores: Dict[str, float]) -> Tuple[dict, str, list[str]]:
    features = {"prosody": prosody, "text": text, "scores": scores}
    # Try LLM narrative first
    try:
        md = await narrate_with_llm(features)
        tips: List[str] = []
    except Exception:
        tips = tips_from_features(prosody, text)
        md = mk_markdown(session_id, scores, prosody, text, tips)
    payload = {
        "session_id": session_id,
        "scores": scores,
        "tips": tips,
        "summary_md": md,
        "report_json": features | {"tips": tips},
    }
    return payload, md, tips
