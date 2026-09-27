import pytest
from app.agents.creative_director import creative_director
from app.agents.script_agent import script_agent
from app.agents.storyboard_agent import storyboard_agent

@pytest.mark.asyncio
async def test_three_creative_concepts():
    concepts = await creative_director.run()
    assert len(concepts) == 3
    ids = [c.concept_id for c in concepts]
    assert "concept_01" in ids
    assert "concept_02" in ids
    assert "concept_03" in ids

    # Check distinct modes
    titles = [c.title for c in concepts]
    assert "THE NOISE" in titles
    assert "THE MISSED MOMENT" in titles
    assert "THE CONTROL ROOM" in titles

@pytest.mark.asyncio
async def test_script_7_beat_structure_and_duration():
    concepts = await creative_director.run()
    scripts = await script_agent.run(concepts)
    assert len(scripts) == 3

    for script in scripts:
        # Check target duration between 30 and 60 seconds
        assert 30.0 <= script.total_duration <= 60.0, f"Script {script.concept_id} duration {script.total_duration} out of bounds"
        # Check 7 beats (scenes)
        assert len(script.scenes) == 7
        # First beat must be 0-3 sec hook
        assert script.scenes[0].duration <= 3.5

@pytest.mark.asyncio
async def test_storyboard_shot_count():
    concepts = await creative_director.run()
    scripts = await script_agent.run(concepts)
    storyboards = await storyboard_agent.run(scripts)

    for sb in storyboards:
        # Must target 12-25 shots per spec (avoid single static shot)
        assert 12 <= len(sb.shots) <= 25, f"Storyboard {sb.concept_id} shot count {len(sb.shots)} out of bounds"
        assert sb.aspect_ratio == "9:16"
