import re

WORD_RE = re.compile(r"[A-Za-z']+")

def normalize_and_tokenize(text: str) -> list[str]:
    text = (text or "").lower()
    return WORD_RE.findall(text)
