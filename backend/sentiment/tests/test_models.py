from app.utils.text_utils import normalize_and_tokenize
from app.models.text_sentiment import score_sentiment
from app.models.emotion_classifier import classify_emotion

def test_sentiment_basic():
    tokens = normalize_and_tokenize("I am happy, this is great!")
    label, valence = score_sentiment(tokens)
    assert label == "positive"
    assert valence > 0

def test_emotion_basic():
    tokens = normalize_and_tokenize("I am very angry about this")
    emo, arousal, conf = classify_emotion(tokens)
    assert emo == "anger"
    assert arousal >= 0.7
    assert 0 <= conf <= 1
