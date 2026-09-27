import pytest
from app.agents.ads_manager import ads_manager
from app.agents.data_agent import crowdwisdom_data_agent
from app.agents.pain_point_agent import pain_point_agent
from app.schemas.ads import CompetitorAd

def test_ad_scoring_algorithm():
    sample_ad = CompetitorAd(
        ad_id="ad_trend_test",
        brand="TrendSpider",
        platform="Meta Ads",
        url="https://trendspider.com/ad",
        first_seen="2026-09-01",
        last_seen="2026-09-25",
        active=True,
        headline="Stop staring at 50 lagging indicators and cut the noise",
        description="Sentiment reversed before the bell. Stop guessing.",
        cta="Start Free Trial",
        video_url="https://example.com/video.mp4",
        engagement_signals={"views": "1.2M"}
    )

    scored = ads_manager.score_ad(sample_ad)
    assert scored.ad_id == "ad_trend_test"
    assert scored.research_score >= 80.0
    assert scored.score_breakdown.recency > 0
    assert scored.score_breakdown.niche_relevance > 0
    assert scored.score_breakdown.hook_strength >= 10.0
    assert "Observed data" in scored.data_classification

@pytest.mark.asyncio
async def test_pain_point_agent_queries():
    queries = pain_point_agent.generate_dynamic_queries()
    assert len(queries) >= 3
    assert any("information overload" in q.lower() or "frustrations" in q.lower() for q in queries)

@pytest.mark.asyncio
async def test_crowdwisdom_data_compliance():
    cwt_data = await crowdwisdom_data_agent.run()
    assert len(cwt_data.source) >= 5
    # Verify strict financial safety compliance: no guarantees
    all_text = " ".join(cwt_data.capabilities + cwt_data.differentiators + cwt_data.customer_value).lower()
    assert "guaranteed profit" not in all_text
    assert "guaranteed returns" not in all_text
    assert "100% win" not in all_text
