from prometheus_client import Counter, Histogram

stt_requests_total = Counter("stt_requests_total","Total number of STT websocket connections handled")

stt_segments_total = Counter("stt_segments_total","Total number of finalized transcript segments",
    ["engine","fallback_used","language"])

stt_vad_drops_total = Counter("stt_vad_drops_total","Number of audio frames dropped/ignored by VAD")

stt_partial_latency_ms = Histogram("stt_partial_latency_ms","Latency to first partial (ms)",
    buckets=(50,100,200,300,400,500,800,1200,2000,5000))

stt_segment_latency_ms = Histogram("stt_segment_latency_ms","End-to-finalized latency per segment (ms)",
    buckets=(100,300,600,1000,2000,3000,5000,10000,20000))
