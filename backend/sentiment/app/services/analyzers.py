from typing import Optional
from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.utils.text_utils import normalize_and_tokenize
from app.models.text_sentiment import score_sentiment
from app.models.emotion_classifier import classify_emotion
from app.models.audio_tone import estimate_tone_from_prosody
from app.services.style_adapter import map_signals_to_style
from app.core.config import settings

def analyze_text(req: AnalyzeRequest, correlation_id: Optional[str] = None) -> AnalyzeResponse:
    tokens = normalize_and_tokenize(req.text)
    sentiment_label, valence = (None, None)
    emotion_label, arousal, emo_conf = (None, None, None)

    feats = set(req.features or ["sentiment","emotion"])

    if "sentiment" in feats:
        sentiment_label, valence = score_sentiment(tokens)
    if "emotion" in feats:
        emotion_label, arousal, emo_conf = classify_emotion(tokens)

    conf_parts = []
    if emo_conf is not None:
        conf_parts.append(emo_conf)
    if valence is not None:
        conf_parts.append(0.5 + 0.5 * abs(valence))
    confidence = round(sum(conf_parts)/len(conf_parts), 3) if conf_parts else 0.7

    tone = None
    if settings.feature_prosody and req.prosody:
        tone = estimate_tone_from_prosody(req.prosody.model_dump())

    style = map_signals_to_style(
        emotion=emotion_label or "neutral",
        valence=valence if valence is not None else 0.0,
        arousal=arousal if arousal is not None else 0.5,
        confidence=confidence,
        tone=tone
    ) if settings.feature_return_style and req.return_style else None

    meta = {"model": f"{settings.sentiment_model}/{settings.emotion_model}"}
    return AnalyzeResponse(
        sentiment=sentiment_label,
        emotion=emotion_label or "neutral",
        valence=valence,
        arousal=arousal,
        confidence=confidence,
        style_directives=style,
        meta=meta,
    )
