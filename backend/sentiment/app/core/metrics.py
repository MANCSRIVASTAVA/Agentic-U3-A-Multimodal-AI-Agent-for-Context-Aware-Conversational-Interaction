from prometheus_client import Counter, Histogram

class _Metrics:
    def __init__(self):
        self.requests_total = Counter(
            "sentiment_requests_total", "Total requests", ["route", "code"]
        )
        self.latency_ms = Histogram(
            "sentiment_latency_ms_bucket", "Latency (ms)", buckets=(5,10,20,50,100,200,400,800,1600)
        )
        self.confidence = Histogram(
            "sentiment_confidence_bucket", "Confidence", buckets=(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0)
        )
        self.style_applied_total = Counter(
            "style_directives_applied_total", "Style directives applied", ["style"]
        )

metrics = _Metrics()
