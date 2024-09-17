"""Command-line interface for the Nest project."""

import asyncio
import os

import typer
from rich.console import Console
from rich.prompt import Prompt

from eloqent.engine import DialogContext, DialogManager, DialogPlanner
from eloqent.engine.planner import DummyDialogPlanner
from eloqent.utils.loaders import load_assistant_config

app = typer.Typer()


@app.command()
def init():
    """Initialize a new nest project."""
    typer.echo("Initializing nest project")


@app.command()
def add():
    """Add a new skill to your nest project."""
    typer.echo("Adding skill to nest project")


@app.command()
def build():
    """Build your nest project."""
    typer.echo("Building nest project")


@app.command()
def run(
    assistant: str = typer.Option(
        ...,  # This makes the option mandatory
        "-a",
        "--assistant",
        help="Path to directory with YAML files for the assistant",
    ),
    use_dummy_planner: bool = typer.Option(
        False,
        "--dummy",
        "-d",
        help="Use a dummy planner for testing",
    ),
):
    """Run your nest project."""
    console = Console()
    console.print("[bold green]Running nest project[/bold green]")

    if not os.path.isdir(assistant):
        console.print(
            f"[bold red]Error: {assistant} is not a valid directory[/bold red]"
        )
        return

    console.print(f"[bold blue]Loading assistant from: {assistant}[/bold blue]")
    domain = load_assistant_config(assistant)

    if use_dummy_planner:
        planner = DummyDialogPlanner()
        console.print("[bold yellow]Using dummy planner for testing[/bold yellow]")
    else:
        planner = DialogPlanner()

    context = DialogContext()
    dialog_manager = DialogManager(domain, planner, context)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        while True:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")

            if user_input.lower() in ["exit", "quit", "q"]:
                raise KeyboardInterrupt

            async def process_response():
                first_response = True
                async for response in dialog_manager.process_user_message(user_input):
                    await asyncio.sleep(0.4)
                    if first_response:
                        console.print()  # Add a newline before the first response
                        first_response = False
                    console.print(f"[bold magenta]Nest AI[/bold magenta]: {response}")

            with console.status("[bold blue]Thinking...[/bold blue]", spinner="dots"):
                loop.run_until_complete(process_response())

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Exiting gracefully...[/bold yellow]")
    finally:
        loop.close()

    console.print("[bold green]Thank you for using Nest AI. Goodbye![/bold green]")


@app.command()
def deploy():
    """Deploy your nest project."""
    typer.echo("Deploying nest project")
