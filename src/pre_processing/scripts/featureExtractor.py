import logging
import os
import dotenv
import time
import json
import re
from pymongo import MongoClient
from google import genai
from datamodelValidation import AdAnalysis
from pydantic import ValidationError
from tqdm import tqdm

# Logging setup
log_file = "/Users/camilojaureguiberry/Documents/Projects/Developments/NarrativeLens/src/pre_processing/logs/feature_extractor.log"
log_level = logging.INFO

logging.basicConfig(
    filename=log_file,
    level=log_level,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Constants
VIDEO_DIR = "/Users/camilojaureguiberry/Documents/Projects/Developments/NarrativeLens/data/video_ads_test"
PROMPT_PATH = "/Users/camilojaureguiberry/Documents/Projects/Developments/NarrativeLens/src/pre_processing/prompts/feature_extractor_prompt.txt"

# Gemini API call
def extract_creative_features(client, video_file_path, prompt):
    try:
        file_ref = client.files.upload(file=video_file_path)
        logging.info(f"File uploaded successfully. File URL is {file_ref.uri}")
    except Exception as e:
        logging.error(f"Error uploading video file: {e}")
        return None

    max_retries = 3
    delay_seconds = 5

    for attempt in range(max_retries):
        try:
            time.sleep(delay_seconds)
            response = client.models.generate_content(
                model="gemini-1.5-pro-latest",
                contents=[prompt, file_ref]
            )
            return response
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: Gemini API Error: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying after {delay_seconds} seconds...")
                time.sleep(delay_seconds)
            else:
                logging.warning("Max retries reached. Aborting video analysis.")
                return None

# Parse Gemini response
def validate_and_structure_output(response):
    if response and hasattr(response, "text"):
        raw_response_text = response.text
        match = re.search(r"\{.*\}", raw_response_text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
                ad_analysis = AdAnalysis(**data)
                logging.info("Successfully validated output")
                return ad_analysis.model_dump()
            except (json.JSONDecodeError, ValidationError) as e:
                logging.error(f"Validation error: {e}")
        else:
            logging.warning("No JSON object found in response.")
    else:
        logging.error("No text found in Gemini response.")
    return None

# MongoDB helpers
def get_mongo_collection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["NarrativeLens"]
    return db["tiktok_ads_us_toplikes"]

def update_video_document(collection, video_filename, creative_features):
    video_name_key = os.path.splitext(video_filename)[0]
    result = collection.update_one(
        {"video_name": video_name_key},
        {"$set": {"creative_features": creative_features}}
    )
    if result.matched_count == 0:
        logging.warning(f"No document found for video: {video_filename}")
    elif result.modified_count == 1:
        logging.info(f"Document updated successfully for: {video_filename}")
    else:
        logging.info(f"No changes made to document for: {video_filename}")

# Prompt loading
def open_prompt_file(prompt_file_path):
    with open(prompt_file_path, "r") as file:
        return file.read()

# Batch runner
def batch_process_videos():
    logging.info("Starting batch processing of videos...")
    dotenv.load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not os.path.exists(VIDEO_DIR):
        logging.critical(f"Video directory {VIDEO_DIR} does not exist.")
        return
    if not api_key:
        logging.critical("GOOGLE_API_KEY not found in environment variables.")
        return

    client = genai.Client(api_key=api_key)
    prompt = open_prompt_file(PROMPT_PATH)
    collection = get_mongo_collection()

    video_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")]

    for filename in tqdm(video_files, desc="Processing videos", unit="video"):
        full_path = os.path.join(VIDEO_DIR, filename)
        response = extract_creative_features(client, full_path, prompt)
        if response:
            features = validate_and_structure_output(response)
            if features:
                update_video_document(collection, filename, features)
            else:
                logging.warning(f"Failed to validate Gemini output for {filename}") 
        else:
            logging.warning(f"Gemini API failed for {filename}")
 
# Entry point
def main():
    batch_process_videos()

if __name__ == "__main__":
    main()

# DONE:
# Implement the basic feature extractor script
# Review the diversity score and matrix features to adapt prompt and output
# Add pydantic models for the output structure
# Add more error handling and logging
# Add batch processing for multiple videos
# Add MongoDB connection to update creative_features based on video_name
# Optimize Gemini client initialization for batch processing

# TODO:
# Add langsmith tracing
# Add more features extraction