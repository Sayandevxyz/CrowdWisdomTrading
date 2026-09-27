import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from app.agents.base_agent import HermesAgent
from app.config import settings
from app.schemas.ads import (
    CompetitorAd,
    CompetitorResearchPayload,
    ScoreBreakdown,
    ScoredAd
)
from app.tools.apify_client import apify_client
from app.utils.json_utils import save_json
from app.utils.timestamps import now_iso

class AdsManagerAgent(HermesAgent):
    """Autonomous agent responsible for competitor ad research and multi-factor scoring."""

    def __init__(self):
        super().__init__(name="AdsManager", prompt_file="ad_research.txt")
        self.register_tool("apify_client", apify_client)

    def score_ad(self, ad: CompetitorAd) -> ScoredAd:
        """Compute objective relevance and creative quality scores separating observed vs interpreted data."""
        # 1. Recency Score (max 25): closer to today gets higher score
        recency_score = 22.0
        try:
            seen_dt = datetime.fromisoformat(ad.last_seen) if "T" in ad.last_seen else datetime.strptime(ad.last_seen, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            days_ago = (datetime.now(timezone.utc) - seen_dt).days
            recency_score = max(5.0, min(25.0, 25.0 - (days_ago * 0.7)))
        except Exception:
            recency_score = 20.0

        # 2. Niche Relevance Score (max 25)
        keywords = ["sentiment", "crowd", "noise", "options", "flow", "signal", "intel", "trader"]
        text_corpus = f"{ad.headline} {ad.description} {ad.brand}".lower()
        matched_kw = sum(1 for kw in keywords if kw in text_corpus)
        niche_score = min(25.0, 10.0 + (matched_kw * 3.0))

        # 3. Creative Quality Score (max 20)
        has_video = 10.0 if ad.video_url else 5.0
        has_cta = 5.0 if ad.cta else 2.0
        has_signals = 5.0 if ad.engagement_signals else 2.0
        creative_quality = min(20.0, has_video + has_cta + has_signals)

        # 4. Hook Strength Score (max 15)
        hook_triggers = ["stop", "why", "they know", "cut through", "look first", "actually"]
        has_hook_trigger = any(trig in ad.headline.lower() for trig in hook_triggers)
        hook_strength = 14.0 if has_hook_trigger else 10.0

        # 5. Pain Relevance Score (max 15)
        pain_keywords = ["fatigue", "late", "indicators", "noise", "guessing", "drawdown"]
        pain_matches = sum(1 for p in pain_keywords if p in text_corpus)
        pain_score = min(15.0, 8.0 + (pain_matches * 2.5))

        total_score = round(recency_score + niche_score + creative_quality + hook_strength + pain_score, 1)

        breakdown = ScoreBreakdown(
            recency=round(recency_score, 1),
            niche_relevance=round(niche_score, 1),
            creative_quality=round(creative_quality, 1),
            hook_strength=round(hook_strength, 1),
            pain_relevance=round(pain_score, 1)
        )

        return ScoredAd(
            ad_id=ad.ad_id,
            research_score=total_score,
            score_breakdown=breakdown,
            data_classification="Observed data (dates/views/copy) vs AI interpretation (hook & pain relevance)",
            ad=ad
        )

    async def run(self, max_ads: Optional[int] = None) -> CompetitorResearchPayload:
        """Execute competitor ad research, scoring, and persistence."""
        self.log("Starting research")
        target_count = max_ads or settings.max_competitor_ads

        # Fetch candidate ads via Apify
        raw_ads = await apify_client.search_competitor_ads(max_results=target_count)
        self.log(f"Found {len(raw_ads)} candidate ads")

        # Score all ads
        scored_ads = [self.score_ad(ad) for ad in raw_ads]
        # Sort by research score descending
        scored_ads.sort(key=lambda s: s.research_score, reverse=True)

        selected_scored = scored_ads[:target_count]
        self.log(f"Selected {len(selected_scored)} relevant ads")

        payload = CompetitorResearchPayload(
            collected_at=now_iso(),
            query="trading intelligence AND market sentiment AI",
            total_candidates=len(raw_ads),
            selected_count=len(selected_scored),
            ads=[s.ad for s in selected_scored],
            scored_ads=selected_scored
        )

        # Save to research/competitor_ads.json
        output_file = settings.research_dir / "competitor_ads.json"
        save_json(output_file, payload)
        self.log(f"Saved ad intelligence to {output_file.name}")

        return payload

ads_manager = AdsManagerAgent()
