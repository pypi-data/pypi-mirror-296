import google.generativeai as genai
from pathlib import Path
from rich import *
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import utils

temp_dir = Path(__file__).parent / 'temp'
code_file_extensions = [
        ".py", ".js", ".java", ".cpp", ".c", ".cs", ".rb", ".php",
        ".html", ".css", ".swift", ".go", ".rs", ".ts", ".kt", ".m",
        ".sh", ".pl", ".r", ".scala", ".dart", ".lua", ".sql", ".xml",
        ".json", ".yml", ".bat", ".ps1", ".asm", ".txt"
    ]

def select_files_for_upload(temp_dir: Path) -> list[str]:
    while True:  # Loop until valid files are found
        if temp_dir.exists():
            files_to_upload = [
                str(file_path) for file_path in temp_dir.rglob('*')
                if file_path.is_file() and file_path.suffix.lower() in code_file_extensions
            ]

            if files_to_upload:  # Check if any valid files were found
                #print(f"Files that can be seen by chatbot: \n {files_to_upload}")
                return files_to_upload
            else:
                print("No valid code files found in the directory. Please enter a new repository URL.")
        
        # If directory doesn't exist or no valid files were found
        # FIX THE CASE WHERE USER STARTS CHAT AND REPO IS NOT DOWNLOADED
        url = input("Enter Repo URL: ").strip()
        utils.clone_repo(url, dest_folder=temp_dir)


def gemini_upload_files(parser, files_to_upload):
    console = Console()

    all_code = ""
    for file_path in files_to_upload:
        with open(file_path, "r") as file:
            file_content = file.read()
            all_code += f"\n---\n{file_content}\n---\n"  # Add a delimiter

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
            "You are a professional software engineer who is given all the code files from a git " 
            "repository as input and is expected to help the user understand it by answering their questions "
            f"The code is given below \n\n {all_code}\n"
        )
    )

    chat_session = model.start_chat()

    console.print("You can now start the conversation. Type 'exit' or 'quit' to stop.")

    while True:
        try:
            user_input = console.input("[bold yellow]>> [/bold yellow]").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("Ending the conversation.")
                break
            
            response = chat_session.send_message(user_input)
            output = Markdown(str(response.text))

            output_panel = Panel(output, title="Sherlock", border_style="cyan", title_align="left")

            console.print(output_panel)
        except KeyboardInterrupt:
            print("Returning to main menu.")
            break
