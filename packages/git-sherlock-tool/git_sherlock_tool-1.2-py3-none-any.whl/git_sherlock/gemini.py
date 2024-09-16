import json
import os
import time
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from dotenv import load_dotenv
import beautifying

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("GEMINI_API_KEY environment variable is not set")
    raise ValueError("GEMINI_API_KEY environment variable is not set")
else:
    genai.configure(api_key=api_key)

def gemini_summarize_readme(str):

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
            "You are given a README file from a Git repository. Write a detailed summary that covers all key sections "
            "such as Introduction, Usage, Installation, Features, and any important notes. The summary should be "
            "at least 25% of the input length, ensuring no critical information is missed."
        )
    )

    chat_session = model.start_chat()

    response = chat_session.send_message(str)
    return response.text



def gemini_chat(str):

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
            "You are given a full code file from a Git repository. Write a detailed summary that covers all key sections "
            "such as Introduction, Usage, Installation, Features, and any important notes. The summary should be "
            "at least 25% of the input length, ensuring no critical information is missed."
        )
    )

    chat_session = model.start_chat()

    response = chat_session.send_message(str)
    return response.text




def generate_summaries_and_list_functions_for_single_file(str, prompt):

    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_schema": content.Schema(
        type=content.Type.OBJECT,
        required=["description", "functions", "function_descriptions"],
        properties={
        "description": content.Schema(
            type=content.Type.STRING
        ),
        "functions": content.Schema(
            type=content.Type.ARRAY,
            items=content.Schema(
                type=content.Type.STRING
            )
        ),
        "function_descriptions": content.Schema(
            type=content.Type.ARRAY,
            items=content.Schema(
                type=content.Type.STRING
            )
        )
    }
    ),
    "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=prompt,
    )

    chat_session = model.start_chat()

    backoff_factor = 2      # Increase sleep duration by this factor after each failure
    max_retries = 5         # Maximum number of retries before giving up

    for attempt in range(max_retries + 1):
        try:
            response = chat_session.send_message(str)
            response = json.dumps(json.loads(response.text))
            return response
        except Exception as e:
            if attempt == max_retries:
                beautifying.rich_warning("Gemini API error: Quota exceeded")
                raise  # Re-raise the exception on the last attempt
            sleep_time = backoff_factor ** attempt
            #print(f" (Retry quota exceeded. Retrying in {sleep_time:.2f} seconds...)")
            time.sleep(sleep_time)