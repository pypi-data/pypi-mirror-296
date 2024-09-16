from rich import *
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
import contextlib
from rich.errors import NotRenderableError
from rich import box
import utils


def welcome_banner():
    console = Console()
    text = """
****************************************************************
*                                                              *
*       _______ __  _____ __              __           __      *
*      / ____(_) /_/ ___// /_  ___  _____/ /___  _____/ /__    *
*     / / __/ / __/\__ \/ __ \/ _ \/ ___/ / __ \/ ___/ //_/    *
*    / /_/ / / /_ ___/ / / / /  __/ /  / / /_/ / /__/ ,<       *
*    \____/_/\__//____/_/ /_/\___/_/  /_/\____/\___/_/|_|      *
*                                                              *
*                                                              *
****************************************************************
    """
    console.print(f"[bold cyan]{text}[/bold cyan]")
    #return print(text)



def loading_anim(function):
    console = Console()
    with console.status("Please wait - cloning repo... \n", spinner="earth"):
        result = function()

    return result


def rich_display_dataframe(df) -> None:
    from rich.table import Table
    from rich.console import Console

    console = Console()
    
    df = df.astype(str)     # Ensure dataframe contains only string values
    table = Table(padding=(1, 3), box=box.MINIMAL)

    row_colors = ["yellow", "cyan", "green", "purple"]
    for i, col in enumerate(df.columns):
        table.add_column(col, justify="left", style=row_colors[i % len(row_colors)])  # Center column titles

    for row in df.values:
        with contextlib.suppress(NotRenderableError):
            table.add_row(*row)

    panel = Panel(table, title="Analysis", border_style="cyan", title_align="right", padding=(1, 5))
    console.print(panel)

def display_summary_and_tree(url, repo_name):
    from utils import generate_readme_summary, get_repo_details
    from rich.columns import Columns

    try:
        console = Console()

        #summary_and_details = display_colored_text(generate_readme_summary(), "yellow") + "\n\n" + display_colored_text(get_repo_details(url), "cyan")
        summary_and_details = display_markdown(generate_readme_summary() + "\n\n" + get_repo_details(url))
        tree = display_tree()

        table = Table(show_header=True, header_style="bold magenta", padding=(1,3), box=box.MINIMAL)
        table.add_column("Summary", width=None, justify="left", ratio=4)
        table.add_column("Tree", width=None, justify="left", ratio=3)

        table.add_row(summary_and_details, tree)
        panel = Panel(table, title=f"{repo_name} Summary", border_style="cyan", title_align="right")

        console.print(panel)
    except Exception as e:
        import traceback
        print(f"Failed to display summary tree: {e}")
        traceback.print_exc()

def display_markdown(text):
    from rich.markdown import Markdown
    console = Console()
    md = Markdown(text)
    return md

def display_colored_text(text, color):
    return f"[bold {color}]{text}[/bold {color}]"

def display_tree():
    colors = ["yellow", "cyan", "green", "magenta", "blue", "red"]

    def get_color(depth):
        return colors[depth % len(colors)]

    def process_line(line):
        depth = line.count("│   ") + line.count("    ")
        color = get_color(depth)

        if "├──" in line or "└──" in line:
            structure, name = line.rsplit(" ", 1)
            return f"[yellow]{structure} [/][bold {color}]{name}[/bold {color}]"
        else:
            return f"[yellow]{line}[/yellow]"

    panel_content = []
    from utils import tree
    from utils import temp_dir
    for line in tree(temp_dir):
        panel_content.append(process_line(line))

    # Join all processed lines into a single string with newlines
    panel_content = "\n".join(panel_content)
    return panel_content

def rich_warning(string):
    string = f"[bold red]{string}[/bold red]"
    return print(string)