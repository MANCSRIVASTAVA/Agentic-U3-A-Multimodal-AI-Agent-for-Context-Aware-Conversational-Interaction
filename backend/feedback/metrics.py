from prometheus_client import Counter, Histogram, CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest

registry = CollectorRegistry()
jobs_total = Counter("feedback_jobs_total", "Total feedback jobs by status", ["status"], registry=registry)
feature_latency = Histogram("feedback_feature_latency_seconds", "Per-feature extraction latency", ["feature"], registry=registry)
inference_latency = Histogram("feedback_model_inference_seconds", "LLM narrative inference latency", registry=registry)

def metrics_response():
    return CONTENT_TYPE_LATEST, generate_latest(registry)
