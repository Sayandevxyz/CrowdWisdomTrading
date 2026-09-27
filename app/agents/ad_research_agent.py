from typing import List
from app.agents.base_agent import HermesAgent

class AdResearchAgent(HermesAgent):
    """Sub-agent specializing in trading ad keyword discovery and taxonomy expansion."""

    def __init__(self):
        super().__init__(name="AdResearch", prompt_file="ad_research.txt")

    def generate_trading_ad_taxonomies(self) -> List[str]:
        """Generate high-yield ad search terms across competitor ecosystems."""
        return [
            "crowd sentiment stock alerts",
            "options order flow unusual activity",
            "market noise reduction retail investor",
            "AI sentiment analysis trading terminal",
            "smart money vs retail sentiment divergence",
            "dark pool trade trackers"
        ]

ad_research_agent = AdResearchAgent()
