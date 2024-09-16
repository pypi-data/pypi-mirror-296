import os
import sys
import platform
from rich import *
from rich import print as rprint
from rich.style import Style
from rich.console import Console
from rich.table import Table
from rich.text import Text
from pathlib import Path
from rich.panel import Panel

#from .utils import *
#from .beautifying import *
#from .conversation import *

import utils
import beautifying
import conversation

temp_dir = Path(__file__).parent / 'temp'

def clear_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')

def interactive_mode(parser):
    console = Console()
    while True:
        try:
            command = console.input("[bold cyan]>>> [/bold cyan]").strip()
            
            if command.lower() in ['q', 'e', 'quit', 'exit']:
                utils.clear_temp_dir("temp/")
                break

            if command.lower() == 'help':
                display_help_in_panel(parser)
                continue
            
            if command.lower() in ['c', 'chat']:
                #gemini_chat(parser)
                files = conversation.select_files_for_upload(temp_dir)
                conversation.gemini_upload_files(parser, files)
                continue

            try:
                if utils.check_url(command):
                    url = command
                    utils.analyze_repo(url)
                else:
                    beautifying.rich_warning(f"The repository at {url} is not valid or does not exist.")
            except Exception as e:
                print(f"An error occurred: {e}", file=sys.stderr)
        except KeyboardInterrupt:
            beautifying.rich_warning("\nExiting...")
            sys.exit(0)


def display_help_in_panel(parser):
    console = Console()
    
    # Calculate half of the terminal width
    max_width = console.width // 2

    # Create the main table
    table = Table(show_header=False, box=None, padding=(0, 1), expand=False, width=max_width)
    table.add_column("Short Option", width=int(max_width * 0.2))
    table.add_column("Long Option", width=int(max_width * 0.2))
    table.add_column("Description", width=int(max_width * 0.6))

    # Add usage information
    usage = parser.format_usage().strip()
    usage = usage.split(": ")[1]
    table.add_row("", "", Text(usage, style="bold", justify="left"))
    table.add_row()  # Empty row for spacing

    # Add arguments to the table
    for action in parser._actions:
        if action.option_strings:  # Skip positional arguments
            short_opt = ""
            long_opt = ""
            if len(action.option_strings) == 2:
                short_opt = action.option_strings[0]
                long_opt = action.option_strings[1]
            elif len(action.option_strings) == 1:
                if action.option_strings[0].startswith("--"):
                    long_opt = action.option_strings[0]
                else:
                    short_opt = action.option_strings[0]
            
            # Apply styles directly to the text
            short_opt_styled = Text(short_opt, style="bold green")
            long_opt_styled = Text(long_opt, style="bold cyan")
            help_text = action.help if action.help else ""
            table.add_row(short_opt_styled, long_opt_styled, Text(help_text))

    # Create a panel with the table
    panel = Panel(
        table,
        title="[bold cyan]GitSherlock Help[/bold cyan]",
        title_align="left",
        expand=False,
        border_style="blue",
        width=max_width,
    )

    # Print the panel
    console.print(panel)