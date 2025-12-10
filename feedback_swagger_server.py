#!/usr/bin/env python3
"""
Temporary Swagger server for Feedback service
This serves the existing OpenAPI spec when the main service is not working
"""

import json
import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(title="Feedback Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"], 
    allow_credentials=True,
)

# Load the comprehensive OpenAPI spec
with open("backend/feedback/contracts/feedback.openapi.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)

# Update the spec to match the running server
openapi_spec["info"]["title"] = "Feedback Service"
openapi_spec["info"]["version"] = "1.0.0"

@app.get("/openapi.json")
async def get_openapi():
    return openapi_spec

# Add the actual feedback endpoints
@app.get("/v1/health")
async def health():
    return {"status": "ok", "service": "feedback"}

@app.get("/v1/metrics")
async def metrics():
    return {"metrics": "prometheus metrics endpoint"}

@app.post("/v1/feedback/analyze")
async def analyze_feedback(request: dict):
    return {"message": "Session queued for analysis", "status": "accepted"}

@app.get("/v1/feedback/{session_id}")
async def get_feedback_report(session_id: str):
    return {
        "session_id": session_id,
        "scores": {
            "overall": 0.85,
            "prosody": 0.80,
            "clarity": 0.90,
            "etiquette": 0.85
        },
        "tips": ["Speak more clearly", "Maintain professional tone"],
        "summary_md": "## Feedback Summary\n\nOverall performance was good...",
        "report_json": {"detailed": "analysis"},
        "report_url_md": None,
        "report_url_pdf": None
    }

@app.get("/v1/feedback/stream")
async def feedback_stream(session_id: str):
    return {"message": "SSE stream endpoint", "session_id": session_id}

@app.get("/docs", response_class=HTMLResponse)
async def get_docs():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
        <title>Feedback Service - Swagger UI</title>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
        const ui = SwaggerUIBundle({
            url: '/openapi.json',
            "dom_id": "#swagger-ui",
            "layout": "BaseLayout",
            "deepLinking": true,
            "showExtensions": true,
            "showCommonExtensions": true,
            oauth2RedirectUrl: window.location.origin + '/docs/oauth2-redirect',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
            ],
        })
        </script>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "ok", "service": "feedback"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8800)
