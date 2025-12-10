from typing import Dict
DEFAULT_WEIGHTS = {
    "prosody": {"speech_rate_wpm": 0.25, "pause_ratio": 0.25, "rms_loudness": 0.25, "f0_var": 0.25},
    "text":    {"sentiment_mean": 0.4, "readability_fkgl": 0.3, "filler_ratio": 0.3},
}
def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def normalize_features(prosody: Dict[str, float], text: Dict[str, float]) -> Dict[str, Dict[str, float]]:
    p = {
        "speech_rate_wpm": clamp01((prosody.get("speech_rate_wpm", 130) - 90) / 120),
        "pause_ratio": clamp01(1.0 - prosody.get("pause_ratio", 0.1) * 2),
        "rms_loudness": clamp01(prosody.get("rms_loudness", 0.5)),
        "f0_var": clamp01(prosody.get("f0_var", 15) / 40),
    }
    t = {
        "sentiment_mean": clamp01(text.get("sentiment_mean", 0.5)),
        "readability_fkgl": clamp01(1.0 - abs(text.get("readability_fkgl", 8) - 8) / 12),
        "filler_ratio": clamp01(1.0 - text.get("filler_ratio", 0.02) * 10),
    }
    return {"prosody": p, "text": t}

def score(prosody: Dict[str, float], text: Dict[str, float]) -> Dict[str, float]:
    norm = normalize_features(prosody, text)
    p = norm["prosody"]; t = norm["text"]
    prosody_score = sum(DEFAULT_WEIGHTS["prosody"][k] * p[k] for k in DEFAULT_WEIGHTS["prosody"]) * 100
    clarity_score = sum(DEFAULT_WEIGHTS["text"][k] * t[k] for k in DEFAULT_WEIGHTS["text"]) * 100
    etiquette_score = (t["sentiment_mean"] * 0.6 + p["f0_var"] * 0.4) * 100
    overall = 0.4 * prosody_score + 0.4 * clarity_score + 0.2 * etiquette_score
    return {
        "overall": round(overall, 2),
        "prosody": round(prosody_score, 2),
        "clarity": round(clarity_score, 2),
        "etiquette": round(etiquette_score, 2),
    }
