from app.schemas.analysis import StyleDirectives

def map_signals_to_style(emotion: str, valence: float, arousal: float, confidence: float, tone=None) -> StyleDirectives:
    if emotion in {"anger", "fear"} or (valence is not None and valence < -0.3):
        style = "calm"
        instr = "Acknowledge feelings; be extra polite, concise, and propose one actionable next step."
    elif emotion in {"sadness"}:
        style = "warm"
        instr = "Be supportive, reassuring, and gentle; offer help and avoid overwhelming detail."
    elif emotion in {"joy", "surprise"} and valence is not None and valence > 0.3:
        style = "concise"
        instr = "Keep a friendly tone; deliver the answer succinctly with a brief confirmation."
    else:
        style = "neutral"
        instr = "Provide a clear, helpful answer in a neutral tone."

    if tone:
        if tone.get("pitch") == "high":
            instr += " Keep sentences shorter to reduce perceived intensity."
        if tone.get("energy") == "high" and style != "calm":
            instr += " Avoid sounding abrupt; add one empathy sentence."

    return StyleDirectives(style_enum=style, system_instructions=instr)
