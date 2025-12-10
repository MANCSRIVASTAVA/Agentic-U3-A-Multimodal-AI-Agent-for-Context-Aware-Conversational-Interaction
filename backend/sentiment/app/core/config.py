import os
import yaml
import logging.config
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv(override=True)

try:
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "configs", "logging.yaml"), "r") as f:
        logging.config.dictConfig(yaml.safe_load(f))
except FileNotFoundError:
    import logging
    logging.basicConfig(level=logging.INFO)

@dataclass
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "sentiment")
    port: int = int(os.getenv("SERVICE_PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    feature_return_style: bool = os.getenv("FEATURE_RETURN_STYLE", "true").lower() == "true"
    feature_prosody: bool = os.getenv("FEATURE_PROSODY", "false").lower() == "true"

    sentiment_model: str = os.getenv("SENTIMENT_MODEL", "textmini")
    emotion_model: str = os.getenv("EMOTION_MODEL", "emomini")

    cors_allow_origins: str = os.getenv("CORS_ALLOW_ORIGINS", "*")

    min_confidence: float = float(os.getenv("SENTIMENT_MIN_CONFIDENCE", "0.6"))

settings = Settings()
