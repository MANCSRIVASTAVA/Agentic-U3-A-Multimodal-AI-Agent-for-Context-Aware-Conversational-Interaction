from typing import Tuple

POSITIVE_LEX = {
    "good": 0.7, "great": 0.9, "excellent": 1.0, "love": 0.9, "happy": 0.8,
    "thanks": 0.4, "helpful": 0.6, "success": 0.8, "works": 0.5, "resolved": 0.7
}
NEGATIVE_LEX = {
    "bad": -0.7, "terrible": -1.0, "awful": -0.9, "hate": -0.9, "angry": -0.8,
    "annoyed": -0.6, "frustrated": -0.7, "doesn't": -0.5, "didn't": -0.6, "broken": -0.8,
    "issue": -0.4, "problem": -0.5, "not": -0.2, "no": -0.2, "fail": -0.7
}

def score_sentiment(tokens: list[str]) -> Tuple[str, float]:
    s = 0.0
    for t in tokens:
        if t in POSITIVE_LEX:
            s += POSITIVE_LEX[t]
        if t in NEGATIVE_LEX:
            s += NEGATIVE_LEX[t]
    s = max(-1.0, min(1.0, s))
    if s > 0.15:
        return "positive", s
    if s < -0.15:
        return "negative", s
    return "neutral", s
