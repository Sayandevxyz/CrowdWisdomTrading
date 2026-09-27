from typing import List
from pydantic import BaseModel, Field
from app.schemas.research import SourceItem

class AdAnalysis(BaseModel):
    """Detailed structural marketing breakdown of a single ad."""
    ad_id: str
    brand: str
    hook: str
    target_audience: str
    pain_point: str
    desire: str
    promise: str
    mechanism: str
    proof: str
    objection: str
    cta: str
    emotional_trigger: str
    visual_pattern: str
    story_structure: str
    creative_pattern: str

class MarketingPatterns(BaseModel):
    """Aggregated marketing intelligence across competitor landscape."""
    analyzed_at: str
    total_analyzed: int
    recurring_patterns: List[str]
    common_hooks: List[str]
    dominant_pain_points: List[str]
    key_emotional_triggers: List[str]
    visual_tropes_to_subvert: List[str]
    ad_analyses: List[AdAnalysis]

class ICPProfile(BaseModel):
    """Validated Ideal Customer Profile for trading/investing product."""
    name: str
    description: str
    behavior: List[str]
    pain_points: List[str]
    desired_outcomes: List[str]
    objections: List[str]
    language: List[str]
    content_consumption: List[str]
    evidence: List[str]

class ICPAnalysis(BaseModel):
    """Stored structure in analysis/icp.json."""
    generated_at: str
    icps: List[ICPProfile]
    sources: List[SourceItem] = Field(default_factory=list)

class CrowdWisdomData(BaseModel):
    """Verified capabilities from approved CrowdWisdomTrading sources."""
    product: str = "CrowdWisdomTrading Intelligence Platform"
    capabilities: List[str]
    differentiators: List[str]
    proof_points: List[str]
    data_examples: List[str]
    customer_value: List[str]
    source: List[str]
    retrieved_at: str
    compliance_statement: str = "Strict adherence to non-predictive intelligence: no guaranteed profit claims."
