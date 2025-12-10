import os
import io
import asyncio
from typing import AsyncGenerator

import httpx
from gtts import gTTS

# ===== Env & defaults =====
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY", "")
ELEVEN_MODEL = os.getenv("ELEVEN_MODEL", "eleven_turbo_v2")
ELEVEN_STABILITY = float(os.getenv("ELEVEN_STABILITY", "0.5"))
ELEVEN_SIMILARITY = float(os.getenv("ELEVEN_SIMILARITY", "0.7"))
REQUEST_TIMEOUT_MS = int(os.getenv("REQUEST_TIMEOUT_MS", "15000"))

# Optional: set a concrete voice-id here for your alias(es)
# Get IDs from https://api.elevenlabs.io/v1/voices (needs api key)
VOICE_ALIAS = {
    # Examples:
    # "female_en": "21m00Tcm4TlvDq8ikWAM",  # Rachel
    # "male_en": "onwK4e9ZLuTAKqWW03F9",
}

def _resolve_voice(voice: str) -> str:
    """
    Accept either a voice-id or a simple alias (mapped above).
    If the string looks like a UUID-ish id, just return as-is.
    """
    if not voice:
        return voice
    v = voice.strip()
    # Heuristic: Eleven voice IDs are short strings; don’t over-validate.
    # Prefer explicit mapping when using aliases.
    return VOICE_ALIAS.get(v, v)

# ===========================
# ElevenLabs (primary)
# ===========================
async def elevenlabs_stream(text: str, voice: str, fmt: str = "mp3") -> AsyncGenerator[bytes, None]:
    """
    Stream raw audio bytes from ElevenLabs.
    """
    if not ELEVEN_API_KEY:
        raise RuntimeError("ELEVEN_API_KEY missing")

    # Prefer voice-id (recommended). If you pass a name/alias, map it to id.
    voice_id = _resolve_voice(voice or "Rachel")

    # ElevenLabs streaming endpoint
    # Docs: POST /v1/text-to-speech/{voice_id}/stream
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    # Choose content type based on requested format
    fmt = (fmt or "mp3").lower()
    accept = "audio/mpeg" if fmt == "mp3" else "audio/wav"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "accept": accept,
        "content-type": "application/json",
    }

    payload = {
        "text": text,
        "model_id": ELEVEN_MODEL,
        "voice_settings": {
            "stability": ELEVEN_STABILITY,
            "similarity_boost": ELEVEN_SIMILARITY,
        },
        # Optionally force an output format preset:
        # "output_format": "mp3_44100_128"  # or for wav: "pcm_16000"
    }

    timeout = httpx.Timeout(REQUEST_TIMEOUT_MS / 1000)
    async with httpx.AsyncClient(timeout=timeout) as client:
        async with client.stream("POST", url, headers=headers, json=payload) as resp:
            resp.raise_for_status()
            async for chunk in resp.aiter_bytes():
                if chunk:
                    yield chunk

# ===========================
# gTTS (fallback)
# ===========================
async def gtts_stream(text: str, voice: str, fmt: str = "mp3") -> AsyncGenerator[bytes, None]:
    """
    gTTS doesn’t provide true network streaming; synthesize to memory,
    then yield in manageable chunks.
    """
    # gTTS ignores voice; language fixed below (en).
    buf = io.BytesIO()

    def _synthesize():
        tts = gTTS(text=text, lang="en")  # change lang if needed
        tts.write_to_fp(buf)

    # Run CPU-bound synthesis off the event loop
    await asyncio.to_thread(_synthesize)
    buf.seek(0)

    # Stream out in chunks so your SSE loop emits multiple events
    chunk_size = 32 * 1024
    while True:
        data = buf.read(chunk_size)
        if not data:
            break
        yield data
