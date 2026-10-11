from fastapi import Header, HTTPException, status
from app.core.config import settings
import hmac

def verify_api_key(x_api_key: str | None = Header(None)) -> bool:
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="Missing API key")
    if not hmac.compare_digest(settings.SCRAPE_API_KEY, x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True