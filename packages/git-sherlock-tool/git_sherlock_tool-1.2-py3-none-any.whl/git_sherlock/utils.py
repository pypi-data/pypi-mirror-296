import re
import zipfile
import shutil
import os
import time
import ftfy
import json
import requests
from io import BytesIO
from pathlib import Path
from rich import *
from time import sleep
from github import Github
from urllib.parse import urlparse
from rich.console import Console
import beautifying
import gemini

space =  '    '
branch = '│   '
tee =    '├── '
last =   '└── '
temp_dir = Path(__file__).parent / 'temp'
exclude_extensions=('.jpg', '.jpeg', '.png', '.txt', '.svg', '.md', '')

def analyze_repo(url):
    beautifying.loading_anim(lambda: clone_repo(url))
    repo_name = extract_repo_name(url)
    #url = create_download_link(url)
    remove_excessive_rows(temp_dir)
    time.sleep(3)
    try:
        beautifying.display_summary_and_tree(url, repo_name)
        file_names, descriptions, functions, func_descriptions = summarize_all_files()
        df = tabulate(file_names, descriptions, functions, func_descriptions)
        beautifying.rich_display_dataframe(df)
    except Exception as e:
        print("Failed to analyze repo: " + str(e))
    clear_temp_dir("temp/")

def check_url(url):     # Uses the GitHub API to check if the repository exists
    parsed_url = urlparse(url)

    if parsed_url.netloc != 'github.com':   # Check if the domain is github.com
        return False
    
    path_parts = parsed_url.path.strip('/').split('/')  # Extract the owner and repo name from the path
    
    if len(path_parts) < 2:
        return False
    
    owner, repo = path_parts[:2]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(api_url)
    return response.status_code == 200

def extract_repo_name(url):
    return urlparse(url).path.split('/')[2]

def create_download_link(url):
    netloc = urlparse(url).netloc
    path = urlparse(url).path
    creator = "/" + path.split('/')[1]
    name = "/" + path.split('/')[2]
    return "https://" + netloc + creator + name + "/archive/refs/heads/master.zip"

def count_files(directory):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

def get_repo_size(github_url):
    """Fetches the size of the GitHub repository using the GitHub API."""
    # Extract the owner and repo name from the URL
    parts = github_url.rstrip('/').split('/')
    owner, repo = parts[-2], parts[-1]

    # GitHub API URL to get the repository details
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(api_url)
    response.raise_for_status()

    # Extract the repository size in kilobytes (KB)
    repo_data = response.json()
    size_kb = repo_data.get('size', 0)
    size_mb = size_kb / 1024  # Convert to MB
    return size_mb

def clone_repo(github_url, dest_folder="temp"):
    """Downloads and extracts a GitHub repository into the specified folder."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__)) # Current dir
        dest_path = os.path.join(script_dir, dest_folder)
        
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        
        download_url = create_download_link(github_url)     # Adjust the GitHub URL for downloading the ZIP file
        response = requests.get(download_url)               # Download the ZIP file
        response.raise_for_status()                         # Check for request errors

        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref: # Extract the ZIP file
            zip_ref.extractall(dest_path)

    except Exception as e:
        print(f"Failed to clone repo: {e}")
        return None
    
    return os.path.abspath(dest_path)

def clear_temp_dir(dir):
    try:
        shutil.rmtree(dir)
    except Exception as e:
        print(f"An error occurred while clearing the temporary directory: {e}")

def remove_excessive_rows(path):     # Cuts down csv and json files
    for file_path in path.rglob('*'):
        try:
            if file_path.is_file():
                if file_path.suffix.lower() == '.csv':
                    import csv
                    with open(file_path, 'r', newline='') as infile, open(file_path, 'w', newline='') as outfile:
                        reader = csv.reader(infile)
                        writer = csv.writer(outfile)

                        for i, row in enumerate(reader):
                            if i < 50:
                                writer.writerow(row)
                            else:
                                break
                elif file_path.suffix.lower() == '.json':
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        data = infile.readlines()[:150]
                    with open(file_path, 'w') as outfile:
                        outfile.writelines(data)
        except Exception as e:
            print(f"Failed to remove excessive rows: {e}")

def generate_readme_summary():      # Finds the readme.md file and sends it to gemini
    for file_path in temp_dir.rglob('*'):
        if file_path.is_file() and (file_path.name.lower() == 'readme.md' or file_path.name.lower() == 'readme.rst'):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                if content == '':
                    return ""
                else:
                    return gemini.gemini_summarize_readme(content)


def get_repo_details(api_url):  
    parsed_url = urlparse(api_url)
    path_parts = parsed_url.path.strip('/').split('/')

    owner, repo_name = path_parts[:2]

    g = Github()
    try:
        repo = g.get_repo(f"{owner}/{repo_name}")

        """details = {
            " --> [bold yellow]OWNER[/bold yellow]": str(repo.owner.login),
            " --> [bold yellow]FILE_COUNT[/bold yellow]": count_files(temp_dir),
            " --> [bold yellow]STARS[/bold yellow]": str(repo.stargazers_count),
            " --> [bold yellow]FORKS[/bold yellow]": str(repo.forks_count),
            " --> [bold yellow]OPEN_ISSUES[/bold yellow]": str(repo.open_issues_count),
            " --> [bold yellow]LANGUAGES[/bold yellow]": str(repo.language or "None"),
            " --> [bold yellow]CREATED_AT[/bold yellow]": str(repo.created_at).split("+")[0],
            " --> [bold yellow]UPDATED_AT[/bold yellow]": str(repo.updated_at).split("+")[0],
            " --> [bold yellow]CLONE_URL[/bold yellow]": str(repo.clone_url),
            " --> [bold yellow]HOMEPAGE[/bold yellow]": str(repo.homepage or "None")
        }"""
        
        details = {
            " - OWNER": f"{repo.owner.login or 'N/A'}\n",
            " - FILE_COUNT": f"{count_files(temp_dir) if temp_dir else 'N/A'}\n",
            " - STARS": f"{repo.stargazers_count or 0}\n",
            " - FORKS": f"{repo.forks_count or 0}\n",
            " - OPEN_ISSUES": f"{repo.open_issues_count or 0}\n",
            " - LANGUAGES": f"{repo.language or 'None'}\n",
            " - CREATED_AT": f"{str(repo.created_at).split('+')[0] if repo.created_at else 'N/A'}\n",
            " - UPDATED_AT": f"{str(repo.updated_at).split('+')[0] if repo.updated_at else 'N/A'}\n",
            " - CLONE_URL": f"{repo.clone_url or 'N/A'}\n",
        }
        
        if details:
            details_string = "\n".join([f"{key}: {value}" for key, value in details.items()])
            return details_string
        else:
            print("Failed to fetch repository details.")
    
    except Exception as e:
        print(f"Error fetching repository details: {e}")
        return None

def generate_prompt_based_on_extension(file_path):
    extension = file_path.suffix.lower()[1:]    # Extract the file extension without the dot

    prompt_template = (
        f"You are given a {extension} file as input\n"
        "For the code provided, write the following:\n"
        "- description: A paragraph explaining what the whole file does\n"
        "- functions: List every function declaration in the code\n"
        "- function_description: A description of every function in the same order as the functions "
        "(Do not use references such as 'This function does this' and 'the function .... does that' in the function description, "
        "just be direct) (In the description, do not use references such as 'this script' or 'this file', just be direct. "
        "Eg: 'A python code that...' or 'A JSON file that...')"
    )

    supported_extensions = {        # Supported extensions
        'c', 'h', 'cpp', 'cc', 'py', 'java', 'js', 'ts',
        'html', 'css', 'rb', 'go', 'php', 'rs', 'swift',
        'sh', 'sql', 'yaml', 'yml', 'bat', 'json', 'xml',
        'ipynb'
    }

    try:
        if extension in supported_extensions:
            return prompt_template
    except Exception as e:
        print(f"Failed to generate summaries: {e}")

    return prompt_template


def summarize_all_files():
    all_summarized_content = []
    file_names = []
    extracted_descriptions = []
    extracted_functions = []
    extracted_function_descriptions = []

    console = Console()

    total_files = count_files(temp_dir)
    excluded_files_count = 0
    file_count = 0

    with console.status("[bold cyan]Analyzing files...[/bold cyan]") as status:
        for file_path in temp_dir.rglob('*'):
            if file_path.is_file() and not file_path.suffix.lower() in exclude_extensions:
                file_count += 1
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = ftfy.fix_text(file.read())
                    #content = remove_excess_tokens(content)
                    if content == '':
                        break
                    else:
                        try:
                            file_names.append(str(file_path.name))
                            prompt = generate_prompt_based_on_extension(file_path)
                            gemini_result = gemini.generate_summaries_and_list_functions_for_single_file(content, prompt)
                            time.sleep(3)
                            all_summarized_content.append(gemini_result)
                            status.update(f"Analyzed {file_count}/{total_files} files. Latest: [bold yellow]{file_path.name}[/bold yellow]")
                            #print(f"--------------### Analyzed file: {file_path} ###--------------")
                        except Exception as e:
                            print("Failed to summarize all files")
            else:
                excluded_files_count += 1

    #print(f"Analyzed {file_count} files.")
    #print(f"Ignored {excluded_files_count} files.")

    for summary in all_summarized_content:
        single_summary = json.loads(summary)
        extracted_descriptions.append(single_summary.get("description", ''))
        extracted_functions.append(single_summary.get("functions", []))
        extracted_function_descriptions.append(single_summary.get("function_descriptions", []))
    print(" ")

    return file_names, extracted_descriptions, extracted_functions, extracted_function_descriptions


def tabulate(list1, list2, list3, list4):
    import pandas as pd

    data = {
        "file_name": list1,
        "description": list2,
        "function": list3,
        "function_description": list4,
    }
    df = pd.DataFrame(data)

    expanded_rows = []
    for _, row in df.iterrows():
        functions = row['function']
        descriptions = row['function_description']

        # Check if functions and descriptions are lists, if not convert to lists
        if not isinstance(functions, list):
            functions = [functions]
        if not isinstance(descriptions, list):
            descriptions = [descriptions]

        # Iterate over each function and its corresponding description
        for i in range(max(len(functions), len(descriptions))):
            # Add the first entry with file_name and description filled
            expanded_rows.append({
                "file_name": row["file_name"] if i == 0 else "",
                "description": row["description"] if i == 0 else "",
                "function": functions[i] if i < len(functions) else "",
                "function_description": descriptions[i] if i < len(descriptions) else "",
            })

    # Convert the list of expanded rows back into a DataFrame
    expanded_df = pd.DataFrame(expanded_rows)

    return expanded_df

def tree(dir_path: Path, prefix: str=''):
    contents = list(dir_path.iterdir())
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir():
            extension = branch if pointer == tee else space 
            yield from tree(path, prefix = prefix + extension)

def remove_excess_tokens(input_str):
    quoted_substrings = re.findall(r"'(.*?)'|\"(.*?)\"", input_str)

    # Clean up the main string by removing excess whitespace
    #cleaned_string = re.sub(r"[\s\n]+", "", input_str, flags=re.MULTILINE) # Replace whitespace characters

    # Restore quoted substrings
    #for single_quote, double_quote in quoted_substrings:
    #    substring = single_quote if single_quote else double_quote
    #    cleaned_string = cleaned_string.replace(substring, f'"{substring}"')

    cleaned_string = re.sub(r"[\s]+", " ", input_str, flags=re.MULTILINE)

    for substring in quoted_substrings:
        cleaned_string = cleaned_string.replace(substring, f'"{substring}"')


    return cleaned_string