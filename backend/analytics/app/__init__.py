"""
Analytics Service package.

Exposes `app` so you can also run with:
  uvicorn app:app --host 0.0.0.0 --port 8000
"""

from .main import app

__all__ = ["app"]
__version__ = "1.0.0"
