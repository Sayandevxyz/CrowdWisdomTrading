import pytest
from app.agents.orchestrator import orchestrator
from app.agents.qa_agent import qa_agent
from app.config import settings
from app.schemas.campaign import CampaignReport, KanbanState

@pytest.mark.asyncio
async def test_orchestrator_dry_run():
    report = await orchestrator.run_pipeline(dry_run=True)
    assert isinstance(report, CampaignReport)
    assert report.campaign_id == "CWT-001"
    assert len(report.creative_concepts) == 3
    assert len(report.generated_ads) == 3

    # Check that report files exist
    assert (settings.reports_dir / "campaign_report.json").exists()
    assert (settings.reports_dir / "kanban.json").exists()

def test_kanban_state_integrity():
    kanban = orchestrator.kanban
    assert isinstance(kanban, KanbanState)
    assert kanban.campaign == "CWT-001"
    assert "research" in kanban.tasks
    assert "video" in kanban.tasks
