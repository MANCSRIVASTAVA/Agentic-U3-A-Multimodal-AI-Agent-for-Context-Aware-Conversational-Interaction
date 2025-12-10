from typing import Dict, List

def analyze(audio_duration_sec: float, words_count: int, pauses_sec: List[float] | None = None) -> Dict[str, float]:
    pauses = pauses_sec or []
    speech_rate_wpm = (words_count / max(audio_duration_sec, 1e-6)) * 60.0
    pause_ratio = (sum(pauses) / max(audio_duration_sec, 1e-6)) if pauses else 0.0
    avg_pause = (sum(pauses) / len(pauses)) if pauses else 0.0
    # Placeholders for loudness/pitch until real DSP is wired
    rms_loudness = 0.5
    f0_mean = 150.0
    f0_var = 15.0
    return {
        "speech_rate_wpm": round(speech_rate_wpm, 2),
        "pause_ratio": round(pause_ratio, 3),
        "avg_pause_s": round(avg_pause, 2),
        "rms_loudness": rms_loudness,
        "f0_mean": f0_mean,
        "f0_var": f0_var,
    }
