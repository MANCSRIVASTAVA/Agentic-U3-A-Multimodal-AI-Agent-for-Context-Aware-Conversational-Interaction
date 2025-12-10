from prometheus_client import Counter, Histogram

tts_requests_total = Counter('tts_requests_total', 'Total TTS requests', ['provider'])
tts_fallback_total = Counter('tts_fallback_total', 'Total TTS fallbacks', ['reason'])
tts_errors_total = Counter('tts_errors_total', 'Total TTS errors', ['code'])
tts_latency_ms = Histogram('tts_latency_ms', 'TTS latency in ms', ['provider'])
