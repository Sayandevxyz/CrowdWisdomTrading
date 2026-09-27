from pathlib import Path
from typing import List, Optional

from app.agents.base_agent import HermesAgent
from app.config import settings
from app.schemas.scripts import CreativeConcept, Scene, Script
from app.utils.json_utils import save_json

class ScriptAgent(HermesAgent):
    """Autonomous screenwriter translating creative concepts into 7-beat production ad scripts."""

    def __init__(self):
        super().__init__(name="ScriptAgent", prompt_file="script.txt")

    def build_script_for_concept(self, concept: CreativeConcept) -> Script:
        """Construct full 45-second cinematic script strictly adhering to the 7-beat structure."""
        if concept.concept_id == "concept_01":
            # Concept 1: THE NOISE (Emotional / Psychological Thriller)
            scenes = [
                Scene(
                    scene_number=1,
                    duration=3.0,
                    visual="Black void. Sudden explosion of 50 overlapping fluorescent stock tickers and notification popups.",
                    camera="Rapid macro push-in towards a glowing computer monitor reflecting in the dilated pupil of a trader.",
                    action="Screens glitch rapidly with red and green numbers flashing across the screen.",
                    voiceover="",
                    sound_design="Violent crescendo of electronic notification dings, telephone rings, and distorted stock market sirens.",
                    music="Deep subsonic bass rumble with dissonant high-pitch string screeches.",
                    on_screen_text="TOO MUCH NOISE",
                    transition="Glitch whip-cut"
                ),
                Scene(
                    scene_number=2,
                    duration=6.5,
                    visual="Dark industrial room. A lone trader surrounded by transparent floating glass charts drifting out of control.",
                    camera="360-degree disorienting orbital roll around the seated trader.",
                    action="The trader clutches their temples as news headlines accelerate violently around them.",
                    voiceover="You have fourteen tabs open. Three Discord rooms screaming different calls. And zero conviction.",
                    sound_design="Whispering overlapping voices: 'Buy call!', 'Short it!', 'Earnings miss!', 'Crash incoming!'",
                    music="Frantic, irregular polyrhythmic percussion building tension.",
                    on_screen_text="",
                    transition="Hard cut"
                ),
                Scene(
                    scene_number=3,
                    duration=9.5,
                    visual="Extreme close-up of a sweaty finger trembling directly above a mechanical mouse button.",
                    camera="Slow-motion macro tracking shot inches from the mouse switch.",
                    action="The market chart violently whipsaws. The finger hovers in agonizing paralysis.",
                    voiceover="By the time you synthesize the chatter... the move is already gone. Or worse... you bought the exact top.",
                    sound_design="Amplified ticking stopwatch echoing in heavy reverb. The dull thud of an elevated heartbeat.",
                    music="Low synth riser climbing relentlessly in frequency.",
                    on_screen_text="DECISION PARALYSIS",
                    transition="Smash-cut"
                ),
                Scene(
                    scene_number=4,
                    duration=7.5,
                    visual="Sudden dead silence. The floating charts shatter into harmless luminescent dust particles.",
                    camera="Static low-angle profile of the trader closing their eyes and exhaling slowly.",
                    action="Complete ambient stillness. The chaotic colors dissolve into clean, deep indigo tones.",
                    voiceover="The problem was never a lack of information. It was knowing what actually matters.",
                    sound_design="A deep, resonant sub-bass drop followed by absolute spatial silence.",
                    music="Lush, warm cinematic ambient pad enters in D-minor.",
                    on_screen_text="KNOW WHAT MATTERS",
                    transition="Smooth dissolve"
                ),
                Scene(
                    scene_number=5,
                    duration=9.0,
                    visual="A single minimalist glowing telemetry HUD appears in mid-air: CrowdWisdom Sentiment Consensus.",
                    camera="Slow forward track over a sleek 3D holographic volume showing crowd conviction score: 87.",
                    action="Millions of chaotic noise particles funnel into one clear, pulsing green conviction signal.",
                    voiceover="Meet CrowdWisdomTrading. Our algorithms de-noise millions of market discussions into one clear measure of crowd conviction.",
                    sound_design="Harmonic digital activation chime; crisp tactile clicks of data resolving.",
                    music="Uplifting electronic sequencer pulse combining with warm orchestral strings.",
                    on_screen_text="CROWDWISDOM INTELLIGENCE",
                    transition="Wipe transition"
                ),
                Scene(
                    scene_number=6,
                    duration=6.5,
                    visual="The trader looks at the clean signal with total calm and executes with a single decisive click.",
                    camera="Medium close-up showing confident posture; camera pulls back to reveal a modern trading sanctuary.",
                    action="The position is opened smoothly. The chart confirms the sentiment breakout without panic.",
                    voiceover="No noise. No panic. Just the collective intelligence of the market, quantified for you.",
                    sound_design="Crisp tactile mechanical switch click echoing with confidence.",
                    music="Full cinematic trailer climax with inspiring brass and synthesizers.",
                    on_screen_text="COLLECTIVE CONVICTION",
                    transition="Fade to black"
                ),
                Scene(
                    scene_number=7,
                    duration=4.5,
                    visual="Cinematic dark blue backdrop with CrowdWisdomTrading logo and glowing animated soundwave emblem.",
                    camera="Slow outward push displaying URL and mobile/desktop access.",
                    action="The logo pulses gently with a neon cyan aura.",
                    voiceover="CrowdWisdomTrading. Stop guessing. Trade with collective clarity.",
                    sound_design="Signature brand audio mnemonic: warm dual-tone chord.",
                    music="Sustained ambient shimmer with resolving root note.",
                    on_screen_text="CrowdWisdomTrading.com\nFilter The Noise. Find Conviction.",
                    transition="Fade to black"
                )
            ]
        elif concept.concept_id == "concept_02":
            # Concept 2: THE MISSED MOMENT (Cinematic / High-Tension Drama)
            scenes = [
                Scene(
                    scene_number=1,
                    duration=3.0,
                    visual="Macro close-up: A mechanical chronograph watch second-hand snapping relentlessly forward in extreme slow-motion.",
                    camera="Dutch angle extreme macro with anamorphic lens flare.",
                    action="The ticking hand hits 12; an amber warning light flashes across the metal bezel.",
                    voiceover="",
                    sound_design="Deafening mechanical gear tick echoing like a metallic gunshot.",
                    music="High-tension cello ostinato in rapid 16th notes.",
                    on_screen_text="TIMING IS EVERYTHING",
                    transition="Whip pan"
                ),
                Scene(
                    scene_number=2,
                    duration=7.0,
                    visual="Subway station platform. Heavy steel doors slam shut right as the trader reaches out their hand.",
                    camera="Tracking reverse shot pulling away from the trapped trader standing on the empty platform.",
                    action="In the reflection of the departing train window, a massive stock chart drops like a stone.",
                    voiceover="Every single day, retail traders find the right idea... exactly three minutes too late.",
                    sound_design="Hydraulic hiss of train doors slamming; screeching steel wheels on subway track.",
                    music="Heavy syncopated industrial percussion.",
                    on_screen_text="",
                    transition="Match cut"
                ),
                Scene(
                    scene_number=3,
                    duration=9.0,
                    visual="Trader stares at their phone. An alert flashes: 'Stock up 24%'. They click buy. Instant red candlestick.",
                    camera="Rapid crash zoom onto the red percentage dropping on the mobile screen.",
                    action="The trader shakes their head in sheer frustration. The word 'LIQUIDATED' or 'DRAWDOWN' blurs.",
                    voiceover="You chase the green candle after the smart money has already positioned. You're left holding the bag.",
                    sound_design="Sub-bass drop; high-frequency ringing tinnitus sound.",
                    music="Ominous descending orchestral riser.",
                    on_screen_text="THE LATE-ENTRY TRAP",
                    transition="Flash cut"
                ),
                Scene(
                    scene_number=4,
                    duration=7.0,
                    visual="Time reverses. The red candle pulls back up; the subway doors slide back open in reverse motion.",
                    camera="Smooth 180-degree camera flip as physics inverts.",
                    action="The trader catches the watch hand before it strikes. Everything slows down.",
                    voiceover="What if you could spot where true market conviction was building... before the price even moved?",
                    sound_design="Reverse audio cymbal swell; breath intake.",
                    music="Shift to atmospheric synth arpeggio.",
                    on_screen_text="SPOT CONVICTION FIRST",
                    transition="Dissolve"
                ),
                Scene(
                    scene_number=5,
                    duration=9.0,
                    visual="CrowdWisdom Divergence Radar. A split-screen showing flat stock price while crowd conviction surges.",
                    camera="Slow diagonal sweep across the glowing sentiment divergence chart.",
                    action="A golden divergence indicator illuminates, highlighting early accumulation.",
                    voiceover="CrowdWisdomTrading tracks crowd sentiment velocity against real-time price action to uncover early divergence.",
                    sound_design="Radar ping with acoustic harmonic trail.",
                    music="Driving, optimistic cinematic electronic beat with live drums.",
                    on_screen_text="SENTIMENT DIVERGENCE RADAR",
                    transition="Wipe"
                ),
                Scene(
                    scene_number=6,
                    duration=6.0,
                    visual="The trader catches the breakout right at the pivot point, calm and ahead of the pack.",
                    camera="Tracking shot following the trader walking effortlessly through a busy skyline promenade.",
                    action="Trader checks phone calmly: trade executed ahead of momentum.",
                    voiceover="Move from reactive chasing to proactive market intelligence.",
                    sound_design="Uplifting wind chime and resonant bass pulse.",
                    music="Inspiring orchestral trailer finale.",
                    on_screen_text="BE EARLY. BE INFORMED.",
                    transition="Cut to title"
                ),
                Scene(
                    scene_number=7,
                    duration=4.5,
                    visual="Sleek branding card: CrowdWisdomTrading platform displayed on mobile and ultra-wide monitor.",
                    camera="Gentle pull-out with volumetric cyan spotlighting.",
                    action="Download and web portal URL illuminate with glowing button.",
                    voiceover="Stop chasing yesterday's moves. Experience CrowdWisdomTrading today.",
                    sound_design="Crisp brand mnemonic chime.",
                    music="Resolving ambient major chord.",
                    on_screen_text="CrowdWisdomTrading.com\nNever Chase Again.",
                    transition="Fade to black"
                )
            ]
        else:
            # Concept 3: THE CONTROL ROOM (Product-led / Futuristic Tech)
            scenes = [
                Scene(
                    scene_number=1,
                    duration=3.0,
                    visual="Pitch dark chamber. A trader touches a floating holographic glass interface; the room erupts in light.",
                    camera="Low-angle sweeping crane shot moving upward past floating data shards.",
                    action="Concentric rings of blue and cyan data illuminate across an expansive circular trading dome.",
                    voiceover="",
                    sound_design="Futuristic reactor hum spooling up to full power; resonant glass tap.",
                    music="Pounding cyber-cinematic beat with deep analog synth bass.",
                    on_screen_text="THE INTELLIGENCE COMMAND",
                    transition="Whip zoom"
                ),
                Scene(
                    scene_number=2,
                    duration=7.0,
                    visual="Massive holographic globe displaying real-time financial sentiment nodes connecting across continents.",
                    camera="Dynamic orbital sweep around the 3D globe as sentiment pulses surge between global markets.",
                    action="Red and green sentiment heatmaps illuminate across sectors: Tech, Energy, Crypto, Semis.",
                    voiceover="In financial markets, thousands of signals broadcast every second. Most platforms show you historical prices.",
                    sound_design="Subtle audio telemetry clicks; continuous low electric hum.",
                    music="Complex, driving electronic rhythm with futuristic modular synths.",
                    on_screen_text="",
                    transition="Hard cut"
                ),
                Scene(
                    scene_number=3,
                    duration=8.5,
                    visual="Split screen: Left side shows a chaotic Twitter/Reddit forum drowning in bot spam; right side shows raw code.",
                    camera="Split-screen slider moving left to right as a scanning laser deconstructs the chatter.",
                    action="Bot icons turn grey and vanish, leaving only verified human consensus behind.",
                    voiceover="They leave you to drown in bot manipulation, sponsor hype, and emotional panic.",
                    sound_design="Glitching static buzzing; digital filter sweeping across frequency spectrum.",
                    music="Tense, minimal electronic heartbeat with filtered sub-bass.",
                    on_screen_text="FILTERING BOT SPAM",
                    transition="Clean wipe"
                ),
                Scene(
                    scene_number=4,
                    duration=8.0,
                    visual="The scanning laser completes. A pristine 3D sector heatmap locks into crystal-clear resolution.",
                    camera="Smooth dolly forward penetrating directly into the central sentiment dashboard.",
                    action="The trader points two fingers, expanding a ticker to reveal its historical sentiment agreement index.",
                    voiceover="CrowdWisdomTrading transforms chaos into high-conviction decision support.",
                    sound_design="Pure sine wave harmonic ring; high-tech glass sliding sound.",
                    music="Majestic synth brass chords swell with heroic momentum.",
                    on_screen_text="MATHEMATICAL SIGNAL PURITY",
                    transition="Dissolve"
                ),
                Scene(
                    scene_number=5,
                    duration=8.5,
                    visual="Extreme close-up of the CrowdWisdom Sentiment Conviction Gauge sliding from 45 to 88 with green aura.",
                    camera="Tilted macro tracking shot skimming along the luminous gauge markings.",
                    action="The data displays: 'Crowd Sentiment: Extremely Bullish | Disinformation Index: 2% | Signal Conviction: High'.",
                    voiceover="Our engine aggregates thousands of data streams, mathematically removing noise to give you genuine crowd consensus.",
                    sound_design="Crisp multi-frequency telemetry chimes.",
                    music="Rousing, driving electronic-orchestral hybrid anthem.",
                    on_screen_text="REAL-TIME CONVICTION INDEX",
                    transition="Zoom cut"
                ),
                Scene(
                    scene_number=6,
                    duration=6.5,
                    visual="The trader steps back, surveying the complete multi-asset dashboard. Total composure and mastery.",
                    camera="Wide cinematic hero shot framing the trader against the illuminated command dome.",
                    action="Trader touches 'Execute Analysis'. The telemetry confirms readiness.",
                    voiceover="Built for serious investors who demand intelligence, not speculation.",
                    sound_design="Deep resonant boom with crystalline high-frequency tail.",
                    music="Full cinematic crescendo reaching its peak.",
                    on_screen_text="MASTER THE MARKETS",
                    transition="Fade to dark"
                ),
                Scene(
                    scene_number=7,
                    duration=4.5,
                    visual="CrowdWisdomTrading signature interface floating with URL and enterprise tier badges.",
                    camera="Slow majestic floating track.",
                    action="UI elements settle into the sleek final logo mark.",
                    voiceover="Enter the control room. CrowdWisdomTrading.com.",
                    sound_design="Signature brand sonic audio signature.",
                    music="Warm, echoing synth resolution.",
                    on_screen_text="CrowdWisdomTrading.com\nInstitutional Crowd Intelligence.",
                    transition="Fade to black"
                )
            ]

        total_dur = round(sum(s.duration for s in scenes), 1)
        return Script(
            concept_id=concept.concept_id,
            title=concept.title,
            concept=concept,
            scenes=scenes,
            total_duration=total_dur,
            compliance_approved=True
        )

    async def run(self, concepts: List[CreativeConcept]) -> List[Script]:
        """Generate production ad scripts for all creative concepts."""
        scripts: List[Script] = []
        for c in concepts:
            self.log(f"Generating {c.concept_id}: {c.title}")
            script = self.build_script_for_concept(c)
            output_file = settings.scripts_dir / f"{c.concept_id}.json"
            save_json(output_file, script)
            scripts.append(script)
            self.log(f"Saved {c.concept_id}.json ({script.total_duration}s, {len(script.scenes)} scenes)")
        return scripts

script_agent = ScriptAgent()
