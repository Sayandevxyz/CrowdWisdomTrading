import re
from typing import List

def clean_text(text: str) -> str:
    """Normalize whitespace and remove non-printable characters."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def estimate_speech_duration(text: str, words_per_minute: int = 140) -> float:
    """Estimate speech duration in seconds based on word count."""
    words = len(text.split())
    if words == 0:
        return 0.0
    seconds = (words / words_per_minute) * 60.0
    return max(1.0, round(seconds, 2))

def slugify(text: str) -> str:
    """Convert string to safe filename slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text
