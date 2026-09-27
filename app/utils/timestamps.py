from datetime import datetime, timezone, timedelta

def now_iso() -> str:
    """Return current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()

def get_days_ago_iso(days: int = 30) -> str:
    """Return ISO timestamp for N days ago."""
    dt = datetime.now(timezone.utc) - timedelta(days=days)
    return dt.isoformat()

def get_date_str(days_ago: int = 0) -> str:
    """Return YYYY-MM-DD date string."""
    dt = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return dt.strftime("%Y-%m-%d")
