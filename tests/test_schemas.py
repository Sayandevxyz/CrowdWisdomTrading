import pytest
from app.schemas.ads import CompetitorAd, ScoreBreakdown, ScoredAd
from app.schemas.research import PainPoint, SourceItem
from app.schemas.marketing import AdAnalysis, ICPProfile, CrowdWisdomData
from app.schemas.scripts import CreativeConcept, Scene, Script
from app.schemas.storyboard import Shot, Storyboard
from app.schemas.campaign import QATechnical, QACreative, QAResult, KanbanState, CampaignReport

def test_competitor_ad_schema():
    ad = CompetitorAd(
        ad_id="ad_test_01",
        brand="TestPlatform",
        platform="Meta Ads",
        url="https://example.com/ad",
        first_seen="2026-09-01",
        last_seen="2026-09-25",
        active=True,
        headline="Cut Market Noise",
        description="Stop staring at 50 indicators.",
        cta="Learn More"
    )
    assert ad.ad_id == "ad_test_01"
    assert ad.active is True
    assert ad.source == "apify"

def test_scored_ad_schema():
    breakdown = ScoreBreakdown(
        recency=22.0,
        niche_relevance=24.0,
        creative_quality=18.0,
        hook_strength=14.0,
        pain_relevance=14.0
    )
    ad = CompetitorAd(
        ad_id="ad_test_01",
        brand="TestPlatform",
        platform="Meta Ads",
        url="https://example.com/ad",
        first_seen="2026-09-01",
        last_seen="2026-09-25",
        headline="Cut Market Noise",
        description="Stop staring at 50 indicators.",
        cta="Learn More"
    )
    scored = ScoredAd(
        ad_id="ad_test_01",
        research_score=92.0,
        score_breakdown=breakdown,
        ad=ad
    )
    assert scored.research_score == 92.0
    assert "Observed data" in scored.data_classification

def test_creative_concept_and_script_schema():
    concept = CreativeConcept(
        concept_id="concept_01",
        title="THE NOISE",
        big_idea="Knowing what matters in market noise",
        target_icp="Active Momentum Trader",
        core_pain="Information overload",
        emotional_arc="Chaos -> Silence -> Clarity",
        visual_style="Psychological Thriller",
        hook="Visual explosion of 50 tickers",
        mechanism="CrowdWisdom De-Noising Engine",
        crowdwisdom_value="Filters 85% of social spam",
        cta="Experience CrowdWisdomTrading.com",
        why_this_concept="Attacks core pain point"
    )
    scene = Scene(
        scene_number=1,
        duration=3.0,
        visual="Extreme close-up on dilated eye reflecting flashing tickers",
        camera="Macro push-in",
        action="Pupil contracts as chart flashes",
        voiceover="",
        sound_design="High frequency glitch",
        music="Subsonic rumble",
        on_screen_text="TOO MUCH NOISE",
        transition="Glitch cut"
    )
    script = Script(
        concept_id="concept_01",
        title="THE NOISE",
        concept=concept,
        scenes=[scene],
        total_duration=3.0
    )
    assert script.concept_id == "concept_01"
    assert len(script.scenes) == 1

def test_qa_result_schema():
    qa = QAResult(
        concept_id="concept_01",
        technical=QATechnical(duration=45.0, resolution="1080x1920", audio=True, valid=True),
        creative=QACreative(hook=9, story=8, clarity=9, visual_quality=9),
        compliance_passed=True,
        issues=[],
        approved=True
    )
    assert qa.approved is True
    assert qa.creative.hook == 9
