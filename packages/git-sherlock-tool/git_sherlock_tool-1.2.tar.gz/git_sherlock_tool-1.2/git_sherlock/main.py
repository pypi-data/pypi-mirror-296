import argparse
import sys
import utils
import rich
import beautifying
import terminal
import conversation
from pathlib import Path

temp_dir = Path(__file__).parent / 'temp'

def main():
    try:
        parser = argparse.ArgumentParser(description="Check if a GitHub repository link is valid.", add_help=False)
        parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
        parser.add_argument("-u", "--url", help="The GitHub repository URL to check")
        parser.add_argument("-c", "--chat", action="store_true", help="Run a chat with the GitHub repository")
        parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode")
        parser.add_argument("-f", "--file", action="store_true", help="Run in interactive mode")
        args = parser.parse_args()
        
        terminal.clear_terminal()
        beautifying.welcome_banner()

        if args.help:
            terminal.display_help_in_panel(parser)

        elif args.interactive:
            terminal.interactive_mode(parser)
        
        elif args.chat:
            #gemini_chat(parser)
            files = conversation.select_files_for_upload(temp_dir)
            conversation.gemini_upload_files(parser, files)

        elif args.url:
            try:
                if utils.check_url(args.url):
                    utils.analyze_repo(args.url)
                else:
                    beautifying.rich_warning(f"The repository at {args.url} is not valid or does not exist.")
            except Exception as e:
                print(f"An error occurred: {e}", file=sys.stderr)
                utils.clear_temp_dir("temp/")
                sys.exit(1)
        else:
            terminal.display_help_in_panel(parser)
            terminal.interactive_mode(parser)
    except KeyboardInterrupt:
        utils.clear_temp_dir("temp/")
        beautifying.rich_warning("Operation cancelled by user")
        sys.exit(0)

if __name__ == "__main__":
    main()