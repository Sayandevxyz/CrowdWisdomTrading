from typing import List, Literal
from pydantic import BaseModel, Field

class SourceItem(BaseModel):
    """Source traceability record for every market insight."""
    claim: str
    source: str
    source_type: Literal["Tavily", "Exa", "Apify", "CrowdWisdom"]
    retrieved_at: str

class PainPoint(BaseModel):
    """Specific trader pain point supported by empirical evidence."""
    pain: str
    evidence: List[str] = Field(default_factory=list)
    source_urls: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.85)

class PainPointPayload(BaseModel):
    """Stored structure in analysis/pain_points.json."""
    retrieved_at: str
    search_queries: List[str] = Field(default_factory=list)
    pain_points: List[PainPoint]
    sources: List[SourceItem] = Field(default_factory=list)
