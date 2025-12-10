# Feedback Service

FastAPI microservice that consumes `session.completed` events, extracts audio/text features,
scores engagement/clarity, and produces a human-readable report. Exposes endpoints to fetch
the report and an SSE stream to notify the frontend when analysis is ready.

Run: `uvicorn services.feedback.app:app --reload` (adjust PYTHONPATH).
