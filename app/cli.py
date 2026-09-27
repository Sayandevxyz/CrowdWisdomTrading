import asyncio
import sys
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.agents.ads_manager import ads_manager
from app.agents.creative_director import creative_director
from app.agents.data_agent import crowdwisdom_data_agent
from app.agents.icp_agent import icp_agent
from app.agents.marketing_analysis_agent import marketing_analysis_agent
from app.agents.orchestrator import orchestrator
from app.agents.pain_point_agent import pain_point_agent
from app.agents.qa_agent import qa_agent
from app.agents.script_agent import script_agent
from app.agents.storyboard_agent import storyboard_agent
from app.agents.video_agent import video_agent
from app.config import settings
from app.logging_config import logger
from app.schemas.campaign import KanbanState
from app.tools.apify_client import apify_client
from app.tools.exa_client import exa_client
from app.tools.llm_client import usage_tracker
from app.tools.tavily_client import tavily_client
from app.utils.json_utils import load_json

# Ensure UTF-8 stdout on Windows terminals
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

console = Console(force_terminal=True, legacy_windows=False)

def display_kanban(kanban: KanbanState):
    """Render beautiful visual Kanban status table in the terminal."""
    status_icons = {
        "done": "[bold green][DONE][/bold green]",
        "running": "[bold yellow][RUN ][/bold yellow]",
        "pending": "[dim][    ][/dim]",
        "skipped": "[cyan][SKIP][/cyan]"
    }

    table = Table(
        title="[bold cyan]CROWDWISDOM AI CREATIVE STUDIO[/bold cyan]\n[dim]Autonomous Video Ads Production Pipeline[/dim]",
        show_header=True,
        header_style="bold magenta",
        border_style="bright_blue"
    )
    table.add_column("Stage", style="bold white", width=30)
    table.add_column("Status", justify="center", width=12)
    table.add_column("State", style="italic")

    task_labels = [
        ("research", "Ad Intelligence Research"),
        ("analysis", "Competitor Ad Analysis"),
        ("pain_points", "Pain Point Extraction"),
        ("icp", "ICP Research & Persona"),
        ("crowdwisdom_data", "CrowdWisdom Data Ingestion"),
        ("creative", "Creative Concepts (3 Modes)"),
        ("scripts", "7-Beat Cinematic Scripts"),
        ("storyboards", "12-25 Shot Storyboards"),
        ("video", "Vertical Video Generation (9:16)"),
        ("qa", "QA & Compliance Audit"),
        ("final_export", "Final Delivery Package")
    ]

    for key, label in task_labels:
        raw_status = kanban.tasks.get(key, "pending")
        icon = status_icons.get(raw_status, "[ ]")
        state_color = "green" if raw_status == "done" else ("yellow" if raw_status == "running" else "dim")
        table.add_row(label, icon, f"[{state_color}]{raw_status.upper()}[/{state_color}]")

    console.print()
    console.print(table)
    console.print(f"[dim]Campaign: {kanban.campaign} | Last Updated: {kanban.updated_at}[/dim]\n")

def display_api_metrics():
    """Print API and LLM usage statistics."""
    summary = (
        f"[bold cyan]Research APIs:[/bold cyan]\n"
        f"  • Apify requests: [bold]{apify_client.request_count}[/bold]\n"
        f"  • Tavily searches: [bold]{tavily_client.request_count}[/bold]\n"
        f"  • Exa searches: [bold]{exa_client.request_count}[/bold]\n\n"
        f"[bold cyan]LLM Engine:[/bold cyan]\n"
        f"  • Total requests: [bold]{usage_tracker.total_requests}[/bold]\n"
        f"  • Estimated tokens: [bold]{usage_tracker.total_tokens}[/bold]\n"
        f"  • Est. cost: [bold green]${usage_tracker.estimated_cost_usd:.4f} USD[/bold green]"
    )
    console.print(Panel(summary, title="[bold green]API Cost & Telemetry Control[/bold green]", border_style="green"))


@click.group()
def cli():
    """CrowdWisdom AI Creative Studio CLI."""
    pass

@cli.command()
def status():
    """Show Kanban pipeline status."""
    settings.init_directories()
    kanban_file = settings.reports_dir / "kanban.json"
    if kanban_file.exists():
        data = load_json(kanban_file)
        kanban = KanbanState.model_validate(data)
    else:
        kanban = KanbanState(updated_at="Not Started")
    display_kanban(kanban)

@cli.command()
def research():
    """Research competitor advertisements using Apify."""
    settings.init_directories()
    console.print("[bold cyan]Executing Competitor Ad Research...[/bold cyan]")
    asyncio.run(ads_manager.run())
    console.print("[bold green]Competitor ad research complete. Saved to research/competitor_ads.json[/bold green]")

@cli.command()
def analyze():
    """Analyze competitor ads, extract pain points, ICPs, and CrowdWisdom truth."""
    settings.init_directories()
    console.print("[bold cyan]Executing Multi-Agent Market & ICP Analysis...[/bold cyan]")
    async def _analyze():
        await marketing_analysis_agent.run()
        await pain_point_agent.run()
        await icp_agent.run()
        await crowdwisdom_data_agent.run()
    asyncio.run(_analyze())
    console.print("[bold green]Analysis complete. Saved to analysis/ directory.[/bold green]")

@cli.command(name="generate-scripts")
def generate_scripts():
    """Generate 3 creative concepts, scripts, and storyboards."""
    settings.init_directories()
    console.print("[bold cyan]Executing Creative Director, Scriptwriter, and Storyboard Artists...[/bold cyan]")
    async def _scripts():
        cwt_data = await crowdwisdom_data_agent.run()
        concepts = await creative_director.run(cwt_data=cwt_data)
        scripts = await script_agent.run(concepts=concepts)
        await storyboard_agent.run(scripts=scripts)
    asyncio.run(_scripts())
    console.print("[bold green]Scripts and storyboards generated in scripts/ and storyboards/.[/bold green]")

@cli.command()
@click.option("--concept", type=int, default=None, help="Render specific concept (1, 2, or 3)")
@click.option("--quality", type=str, default="standard", help="Render quality: 'fast' or 'standard'")
def render(concept: Optional[int], quality: str):
    """Render videos from storyboards."""
    settings.init_directories()
    console.print(f"[bold cyan]Rendering video advertisements (Quality: {quality})...[/bold cyan]")
    async def _render():
        render_results = await video_agent.run(concept_filter=concept, render_quality=quality)
        await qa_agent.run(render_results=render_results)
    asyncio.run(_render())
    console.print("[bold green]Video rendering and QA audit complete. Outputs saved in videos/ and final/[/bold green]")

@cli.command()
@click.option("--concept", type=int, default=None, help="Run specific concept only (1, 2, or 3)")
@click.option("--dry-run", is_flag=True, default=False, help="Skip video rendering")
@click.option("--quality", type=str, default="standard", help="Render quality: 'fast' or 'standard'")
def run(concept: Optional[int], dry_run: bool, quality: str):
    """Run complete autonomous Hermes pipeline."""
    settings.init_directories()
    asyncio.run(orchestrator.run_pipeline(dry_run=dry_run, concept_filter=concept, render_quality=quality))
    display_kanban(orchestrator.kanban)
    display_api_metrics()

@cli.command()
def demo():
    """Run full demonstration pipeline offline/sample mode without requiring paid API keys."""
    settings.init_directories()
    console.print("[bold magenta]Starting CrowdWisdom AI Creative Studio in DEMO MODE[/bold magenta]")
    console.print("[dim]Using deterministic high-fidelity models and built-in procedural rendering engine...[/dim]\n")
    
    # Run full pipeline with fast procedural render to guarantee fast execution and zero API dependence
    asyncio.run(orchestrator.run_pipeline(dry_run=False, render_quality="fast"))
    display_kanban(orchestrator.kanban)
    display_api_metrics()
    console.print("[bold green]DEMO MODE completed successfully! Check final/ directory for rendered ads and reports.[/bold green]")

if __name__ == "__main__":
    cli()
