from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class CompetitorAd(BaseModel):
    """Raw and structured competitor advertisement intelligence item."""
    ad_id: str
    brand: str
    platform: str
    url: str
    first_seen: str
    last_seen: str
    active: bool = True
    creative_type: str = "video"
    headline: str
    description: str
    cta: str
    video_url: Optional[str] = None
    landing_page: str = ""
    engagement_signals: Dict[str, Any] = Field(default_factory=dict)
    source: str = "apify"

class ScoreBreakdown(BaseModel):
    """Breakdown of ad creative and research scoring."""
    recency: float = Field(ge=0, le=25)
    niche_relevance: float = Field(ge=0, le=25)
    creative_quality: float = Field(ge=0, le=20)
    hook_strength: float = Field(ge=0, le=15)
    pain_relevance: float = Field(ge=0, le=15)

class ScoredAd(BaseModel):
    """Scored competitor ad with explicit distinction of observed data vs AI interpretation."""
    ad_id: str
    research_score: float = Field(ge=0, le=100)
    score_breakdown: ScoreBreakdown
    data_classification: str = "Observed data vs AI interpretation"
    ad: CompetitorAd

class CompetitorResearchPayload(BaseModel):
    """Collection payload for research/competitor_ads.json."""
    collected_at: str
    query: str
    total_candidates: int
    selected_count: int
    ads: List[CompetitorAd]
    scored_ads: List[ScoredAd] = Field(default_factory=list)
