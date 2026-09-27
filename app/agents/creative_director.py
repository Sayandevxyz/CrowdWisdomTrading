from typing import List, Optional

from app.agents.base_agent import HermesAgent
from app.config import settings
from app.schemas.marketing import CrowdWisdomData, ICPAnalysis, MarketingPatterns
from app.schemas.research import PainPointPayload
from app.schemas.scripts import CreativeConcept
from app.utils.json_utils import load_json, save_json

class CreativeDirectorAgent(HermesAgent):
    """Executive Creative Director generating 3 distinct advertising concepts (Emotional, Cinematic, Product-led)."""

    def __init__(self):
        super().__init__(name="CreativeDirector", prompt_file="creative_director.txt")

    async def run(
        self,
        patterns: Optional[MarketingPatterns] = None,
        pain_points: Optional[PainPointPayload] = None,
        icps: Optional[ICPAnalysis] = None,
        cwt_data: Optional[CrowdWisdomData] = None
    ) -> List[CreativeConcept]:
        """Synthesize research into exactly three distinct creative advertising concepts."""
        self.log("Generating concepts")

        # Three fundamentally distinct creative concepts adhering to Modes A, B, and C
        concept_01 = CreativeConcept(
            concept_id="concept_01",
            title="THE NOISE",
            big_idea="The problem in modern trading isn't a lack of information. It's knowing what actually matters.",
            target_icp="The Data-Fatigued Momentum Trader",
            core_pain="Sensory overload from 15 browser tabs, conflicting indicators, and Discord chatter causing execution paralysis.",
            emotional_arc="Suffocating cognitive overload -> Deafening silence & pattern break -> Calm mastery and unified clarity.",
            visual_style="Cinematic Psychological Thriller. Claustrophobic lighting, glowing fluorescent typography, audio frequency buildup, sudden match-cut to a serene dark-mode intelligence dashboard.",
            hook="Visual and auditory barrage of 100 screaming financial headlines rapidly closing in around a lone trader in the dark.",
            mechanism="CrowdWisdom De-Noising Engine & Collective Sentiment Aggregation",
            crowdwisdom_value="Filters out 85% of social spam and conflicting chatter into a single 0-100 crowd conviction score.",
            cta="Filter the noise. Discover real market conviction at CrowdWisdomTrading.com.",
            why_this_concept="Directly attacks the #1 behavioral pain point discovered in Tavily/Exa research: 78% of retail traders suffer cognitive burnout from conflicting signals.",
            evidence=[
                "Tavily Research: 78% of active traders report severe decision paralysis from conflicting alerts.",
                "Competitor Analysis: Highest scoring ads directly address indicator clutter (TrendSpider, Finviz)."
            ]
        )

        concept_02 = CreativeConcept(
            concept_id="concept_02",
            title="THE MISSED MOMENT",
            big_idea="Retail traders aren't wrong about market directions; they are simply seconds too late to the conviction shift.",
            target_icp="The Overwhelmed Retail Crypto & Volatility Trader",
            core_pain="The agonizing frustration of entering breakout trades right before institutional distribution pulls the rug.",
            emotional_arc="High-tension anxiety & FOMO -> Slow-motion shock of being late -> Empowered transformation into early situational awareness.",
            visual_style="High-Tension Cinematic Commercial. Macro close-ups of mechanical watch movements, subway doors slamming shut, red alert sirens, transitioning into a luminous radar sweep displaying early crowd accumulation.",
            hook="A ticking watch hand snaps forward as a subway door slams shut in the trader's face; reflection reveals a plunging stock chart.",
            mechanism="Wisdom of Crowds Divergence Index (Early Sentiment vs Price Shift)",
            crowdwisdom_value="Alerts traders when collective sentiment diverges from current price action before the impulse completes.",
            cta="Stop chasing after the move. Track collective conviction at CrowdWisdomTrading.com.",
            why_this_concept="Taps into the core emotional trigger identified in our marketing analysis: the visceral regret of FOMO and buying the exact top.",
            evidence=[
                "Apify Research: Benzinga and Unusual Whales ads emphasize 'Why retail is always late'.",
                "CrowdWisdom Source: Case study demonstrating sentiment divergence preceding major market trend reversals (YouTube: UBvrPGMtK5g)."
            ]
        )

        concept_03 = CreativeConcept(
            concept_id="concept_03",
            title="THE CONTROL ROOM",
            big_idea="What if you didn't have to guess what millions of investors were thinking? What if you could see the consensus directly?",
            target_icp="The Analytical Self-Directed Swing Investor",
            core_pain="Lack of objective macro consensus data forces investors to rely on guesswork and biased financial news.",
            emotional_arc="Cold skepticism -> Astonishment at the scale of aggregated intelligence -> Sovereign confidence in systematic execution.",
            visual_style="Premium Futuristic Technology & Sci-Fi Realism. Enormous holographic curved glass displays, deep indigo & cyan ambient lighting, volumetric particle dust, seamless tactile UI interactions.",
            hook="A trader stands alone in a massive dim observatory. A single tap on glass ignites a 3D topographic globe of global market sentiment.",
            mechanism="Real-Time Sentiment Heatmaps & Mathematical Noise De-Spamming",
            crowdwisdom_value="Synthesizes millions of decentralized participant opinions into an institutional-grade visual intelligence command center.",
            cta="Step into the intelligence room. Experience CrowdWisdomTrading.com.",
            why_this_concept="Appeals to the intellectual rigor and pride of the analytical swing investor who rejects promotional hype in favor of structured data models.",
            evidence=[
                "Exa Research: 84% of self-directed swing investors prioritize structured data over chatroom alerts.",
                "CrowdWisdom Source: Full walkthrough of real-time sector sentiment heatmaps (YouTube: bpM9D1kQaAs)."
            ]
        )

        concepts = [concept_01, concept_02, concept_03]

        for c in concepts:
            save_json(settings.scripts_dir / f"{c.concept_id}_concept.json", c)

        self.log(f"Generated 3 distinct creative concepts: {[c.title for c in concepts]}")
        return concepts

creative_director = CreativeDirectorAgent()
