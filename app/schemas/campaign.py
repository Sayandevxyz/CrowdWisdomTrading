from typing import Any, Dict, List
from pydantic import BaseModel, Field

class QATechnical(BaseModel):
    """Technical video verification parameters."""
    duration: float
    resolution: str
    audio: bool
    valid: bool

class QACreative(BaseModel):
    """Creative evaluation diagnostics (internal scores, not performance claims)."""
    hook: int = Field(ge=1, le=10)
    story: int = Field(ge=1, le=10)
    clarity: int = Field(ge=1, le=10)
    visual_quality: int = Field(ge=1, le=10)

class QAResult(BaseModel):
    """Autonomous QA Agent assessment."""
    concept_id: str
    technical: QATechnical
    creative: QACreative
    compliance_passed: bool = True
    issues: List[str] = Field(default_factory=list)
    approved: bool

class KanbanState(BaseModel):
    """Lightweight Kanban state representation for campaign workflow."""
    campaign: str = "CWT-001"
    status: str = "RESEARCH"
    tasks: Dict[str, str] = Field(
        default_factory=lambda: {
            "research": "pending",
            "analysis": "pending",
            "pain_points": "pending",
            "icp": "pending",
            "crowdwisdom_data": "pending",
            "creative": "pending",
            "scripts": "pending",
            "storyboards": "pending",
            "video": "pending",
            "qa": "pending",
            "final_export": "pending"
        }
    )
    updated_at: str

class CampaignReport(BaseModel):
    """Comprehensive end-to-end campaign intelligence and production report."""
    campaign_id: str
    generated_at: str
    research_summary: Dict[str, Any]
    competitor_patterns: List[str]
    pain_points: List[Dict[str, Any]]
    icps: List[Dict[str, Any]]
    creative_concepts: List[Dict[str, Any]]
    generated_ads: List[Dict[str, Any]]
    qa_results: List[QAResult]
    sources: List[Dict[str, Any]]
    run_metadata: Dict[str, Any]
