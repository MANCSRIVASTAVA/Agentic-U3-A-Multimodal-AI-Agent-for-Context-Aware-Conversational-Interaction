from typing import Dict
import re

def simple_sentiment(text: str) -> float:
    pos_words = len(re.findall(r"\b(good|great|love|excellent|well done|nice)\b", text, flags=re.I))
    neg_words = len(re.findall(r"\b(bad|poor|hate|terrible|awful|sorry)\b", text, flags=re.I))
    return max(min((pos_words - neg_words) / 10.0 + 0.5, 1.0), 0.0)

def readability_fkgl(text: str) -> float:
    words = len(re.findall(r"\w+", text))
    sentences = max(len(re.findall(r"[.!?]", text)), 1)
    syllables = sum(len(re.findall(r"[aeiouyAEIOUY]", w)) for w in re.findall(r"\w+", text))
    return 0.39 * (words / sentences) + 11.8 * (syllables / max(words, 1)) - 15.59

def filler_ratio(text: str) -> float:
    fillers = len(re.findall(r"\b(um+|uh+|like|you know|er+|ah+)\b", text, flags=re.I))
    words = max(len(re.findall(r"\w+", text)), 1)
    return round(fillers / words, 3)

def analyze(text: str) -> Dict[str, float]:
    return {
        "sentiment_mean": round(simple_sentiment(text), 3),
        "readability_fkgl": round(readability_fkgl(text), 2),
        "filler_ratio": filler_ratio(text),
    }
