from typing import Tuple

EMO_LEX = {
    "anger": ["angry", "furious", "mad", "annoyed", "irritated", "frustrated"],
    "joy": ["happy", "glad", "great", "love", "awesome", "yay"],
    "sadness": ["sad", "unhappy", "upset", "disappointed", "depressed"],
    "fear": ["scared", "afraid", "worried", "anxious", "concerned"],
    "disgust": ["disgusted", "gross", "nasty", "ew"],
    "surprise": ["surprised", "shocked", "wow", "unexpected"]
}

def classify_emotion(tokens: list[str]) -> Tuple[str, float, float]:
    counts = {k: 0 for k in EMO_LEX}
    for t in tokens:
        for emo, words in EMO_LEX.items():
            if t in words:
                counts[emo] += 1
    if not any(counts.values()):
        return "neutral", 0.4, 0.5
    emo = max(counts, key=counts.get)
    arousal = {
        "anger": 0.8, "joy": 0.7, "sadness": 0.3, "fear": 0.7, "disgust": 0.6, "surprise": 0.9
    }.get(emo, 0.5)
    total = sum(counts.values())
    conf = min(1.0, counts[emo] / max(1, total) * 0.9 + 0.1)
    return emo, arousal, conf
