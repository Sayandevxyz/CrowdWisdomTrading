import asyncio
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.agents.ads_manager import ads_manager
from app.agents.base_agent import HermesAgent
from app.agents.creative_director import creative_director
from app.agents.data_agent import crowdwisdom_data_agent
from app.agents.icp_agent import icp_agent
from app.agents.marketing_analysis_agent import marketing_analysis_agent
from app.agents.pain_point_agent import pain_point_agent
from app.agents.qa_agent import qa_agent
from app.agents.script_agent import script_agent
from app.agents.storyboard_agent import storyboard_agent
from app.agents.video_agent import video_agent
from app.config import settings
from app.schemas.campaign import CampaignReport, KanbanState, QAResult
from app.tools.apify_client import apify_client
from app.tools.exa_client import exa_client
from app.tools.llm_client import usage_tracker
from app.tools.tavily_client import tavily_client
from app.utils.json_utils import load_json, save_json
from app.utils.timestamps import now_iso

class Orchestrator(HermesAgent):
    """Lead Orchestrator coordinating the Hermes multi-agent pipeline and campaign state."""

    def __init__(self):
        super().__init__(name="Orchestrator")
        self.campaign_id = "CWT-001"
        self.kanban_file = settings.reports_dir / "kanban.json"
        self.report_file = settings.reports_dir / "campaign_report.json"
        self.kanban = self._init_kanban()

    def _init_kanban(self) -> KanbanState:
        if self.kanban_file.exists():
            try:
                data = load_json(self.kanban_file)
                return KanbanState.model_validate(data)
            except Exception:
                pass
        return KanbanState(campaign=self.campaign_id, status="RESEARCH", updated_at=now_iso())

    def update_kanban(self, status: str, task_updates: Dict[str, str]):
        self.kanban.status = status
        self.kanban.tasks.update(task_updates)
        self.kanban.updated_at = now_iso()
        save_json(self.kanban_file, self.kanban)

    async def run_pipeline(
        self,
        dry_run: bool = False,
        concept_filter: Optional[int] = None,
        render_quality: str = "standard"
    ) -> CampaignReport:
        """Run the end-to-end Hermes agent studio pipeline."""
        settings.init_directories()
        self.log(f"Starting CrowdWisdom AI Creative Studio Pipeline [DryRun={dry_run}]")

        # 1. Research Phase
        self.update_kanban("RESEARCH", {"research": "running"})
        research_payload = await ads_manager.run()
        self.update_kanban("ANALYSIS", {"research": "done", "analysis": "running"})

        # 2. Competitor Ad Analysis
        marketing_patterns = await marketing_analysis_agent.run(ads=research_payload.ads)
        self.update_kanban("ANALYSIS", {"analysis": "done", "pain_points": "running"})

        # 3. Pain Point Discovery
        pain_payload = await pain_point_agent.run()
        self.update_kanban("ICP", {"pain_points": "done", "icp": "running"})

        # 4. ICP Construction
        icp_payload = await icp_agent.run()
        self.update_kanban("CREATIVE", {"icp": "done", "crowdwisdom_data": "running"})

        # 5. CrowdWisdom Data Ingestion
        cwt_data = await crowdwisdom_data_agent.run()
        self.update_kanban("CREATIVE", {"crowdwisdom_data": "done", "creative": "running"})

        # 6. Creative Director (3 Concepts)
        concepts = await creative_director.run(
            patterns=marketing_patterns,
            pain_points=pain_payload,
            icps=icp_payload,
            cwt_data=cwt_data
        )
        self.update_kanban("SCRIPT", {"creative": "done", "scripts": "running"})

        # 7. Script Writing (3 Scripts)
        scripts = await script_agent.run(concepts=concepts)
        self.update_kanban("STORYBOARD", {"scripts": "done", "storyboards": "running"})

        # 8. Storyboarding (12-25 shots each)
        storyboards = await storyboard_agent.run(scripts=scripts)
        self.update_kanban("VIDEO", {"storyboards": "done", "video": "running" if not dry_run else "skipped"})

        # 9. Video Production
        qa_results: List[QAResult] = []
        if not dry_run:
            render_results = await video_agent.run(
                storyboards=storyboards,
                concept_filter=concept_filter,
                render_quality=render_quality
            )
            self.update_kanban("QA", {"video": "done", "qa": "running"})

            # 10. QA Audit & Final Packaging
            qa_results = await qa_agent.run(render_results=render_results)
            self.update_kanban("COMPLETE", {"qa": "done", "final_export": "done"})
        else:
            self.log("[Orchestrator] Dry-run enabled: skipped rendering and QA video audit.")
            self.update_kanban("COMPLETE", {"qa": "skipped", "final_export": "done"})

        # 11. Final Report Generation
        total_shots = sum(len(sb.shots) for sb in storyboards)
        all_sources = pain_payload.sources + icp_payload.sources + [
            {"claim": "Approved CrowdWisdom capabilities", "source": s, "source_type": "CrowdWisdom", "retrieved_at": now_iso()}
            for s in cwt_data.source
        ]

        report = CampaignReport(
            campaign_id=self.campaign_id,
            generated_at=now_iso(),
            research_summary={
                "total_competitor_ads_evaluated": research_payload.total_candidates,
                "selected_ads": research_payload.selected_count,
                "dominant_platforms": ["Meta", "YouTube", "Twitter/X"],
                "target_niche": "Trading Intelligence, Crowd Sentiment, Options Flow"
            },
            competitor_patterns=marketing_patterns.recurring_patterns,
            pain_points=[p.model_dump() for p in pain_payload.pain_points],
            icps=[i.model_dump() for i in icp_payload.icps],
            creative_concepts=[c.model_dump() for c in concepts],
            generated_ads=[
                {
                    "concept_id": s.concept_id,
                    "title": s.title,
                    "duration": s.total_duration,
                    "scenes_count": len(s.scenes),
                    "video_path": f"videos/{s.concept_id}.mp4" if not dry_run else None
                }
                for s in scripts
            ],
            qa_results=qa_results,
            sources=[s if isinstance(s, dict) else s.model_dump() for s in all_sources],
            run_metadata={
                "dry_run": dry_run,
                "apify_requests": apify_client.request_count,
                "tavily_searches": tavily_client.request_count,
                "exa_searches": exa_client.request_count,
                "llm_requests": usage_tracker.total_requests,
                "llm_tokens": usage_tracker.total_tokens,
                "estimated_llm_cost_usd": round(usage_tracker.estimated_cost_usd, 4),
                "total_shots_planned": total_shots,
                "render_engine": "OpenMontage/Hyperframes adapter with procedural FFmpeg engine"
            }
        )

        save_json(self.report_file, report)
        # Also copy campaign report to final/ directory
        save_json(settings.final_dir / "campaign_report.json", report)
        self.log(f"Campaign execution complete! Report saved to {self.report_file.name} and final/")

        return report

orchestrator = Orchestrator()
