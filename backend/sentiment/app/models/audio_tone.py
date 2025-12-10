from typing import Optional, Dict

def estimate_tone_from_prosody(prosody: Optional[dict]) -> Dict[str, str | float] | None:
    if not prosody:
        return None
    pitch = prosody.get("pitch_hz")
    energy = prosody.get("energy_rms")
    tone = {}
    if pitch is not None:
        tone["pitch"] = "high" if pitch >= 220 else "low"
    if energy is not None:
        tone["energy"] = "high" if energy >= 0.6 else "low"
    return tone or None
