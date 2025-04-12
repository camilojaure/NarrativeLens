import logging
import os
import dotenv
import time
import json
import re
import argparse
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
VIDEO_DIR = "/Users/camilojaureguiberry/Documents/Projects/Developments/NarrativeLens/data/video_ads"
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
def validate_and_structure_output(response, retry_count=0):
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

                # If there's a ValidationError, check for any invalid enum inputs
                if isinstance(e, ValidationError):
                    invalid_fields = []
                    for err in e.errors():
                        loc = err.get("loc")[0] if err.get("loc") else "unknown_field"
                        invalid_value = err.get("input")
                        invalid_fields.append((loc, invalid_value))

                    # Use escape values after max retries
                    if retry_count >= 2:
                        for field, _ in invalid_fields:
                            if field in data:
                                if field == "creative_concept":
                                    data[field] = "Not Applicable"
                                elif field == "creative_theme":
                                    data[field] = "Not Applicable"
                                elif field == "format_production_style":
                                    data[field] = "Unclear"
                                else:
                                    data[field] = "Unclear"
                        try:
                            ad_analysis = AdAnalysis(**data)
                            logging.info("Validated output using escape values after max retries")
                            return ad_analysis.model_dump()
                        except ValidationError as final_err:
                            logging.error(f"Final fallback also failed: {final_err}")
                            return None

                    # Otherwise attempt a retry
                    if invalid_fields:
                        logging.info(f"Retrying with corrected fields: {invalid_fields}")

                        error_summary = "\n".join(
                            f"Field '{field}' had an invalid value: '{value}'" for field, value in invalid_fields
                        )
                        retry_prompt = (
                            f"The previous JSON you generated had schema validation errors.\n"
                            f"{error_summary}\n\n"
                            f"Please return a corrected version of the original JSON, strictly following this schema:\n\n"
                            f"{raw_response_text.strip()}\n\n"
                            f"Ensure all values match the predefined enum options provided in the prompt. Return only valid JSON."
                        )

                        try:
                            retry_response = genai.Client().models.generate_content(
                                model="gemini-1.5-pro-latest",
                                contents=[retry_prompt]
                            )
                            return validate_and_structure_output(retry_response, retry_count + 1)
                        except Exception as retry_err:
                            logging.error(f"Retry failed with Gemini: {retry_err}")
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
        return False
    elif result.modified_count == 1:
        logging.info(f"Document updated successfully for: {video_filename}")
    else:
        logging.info(f"No changes made to document for: {video_filename}")
    return True

# Prompt loading
def open_prompt_file(prompt_file_path):
    with open(prompt_file_path, "r") as file:
        return file.read()

# Batch runner
def batch_process_videos(mode="prod"):
    logging.info("Starting batch processing of videos...")
    dotenv.load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    total_processed = 0
    success_count = 0
    failed_files = []
    not_found_in_db = []

    if not os.path.exists(VIDEO_DIR):
        logging.critical(f"Video directory {VIDEO_DIR} does not exist.")
        return
    if not api_key:
        logging.critical("GOOGLE_API_KEY not found in environment variables.")
        return

    client = genai.Client(api_key=api_key)
    prompt = open_prompt_file(PROMPT_PATH)
    collection = get_mongo_collection()

    if mode == "dry":
        logging.info("Running in dry mode")
        test_video_dir = "/Users/camilojaureguiberry/Documents/Projects/Developments/NarrativeLens/data/video_ads_dry"
        video_files = [f for f in os.listdir(test_video_dir) if f.endswith(".mp4")]
        if not video_files:
            logging.warning("No test videos found in dry-run folder.")
            return
        video_files = [video_files[0]]  # use only the first video
        video_dir = test_video_dir
    elif mode == "test":
        logging.info("Running in test mode")
        test_video_dir = "/Users/camilojaureguiberry/Documents/Projects/Developments/NarrativeLens/data/video_ads_test"
        video_files = [f for f in os.listdir(test_video_dir) if f.endswith(".mp4")]
        video_dir = test_video_dir
    else:
        logging.info("Running in prod mode with incremental processing")
        all_video_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")]
        already_processed = collection.distinct("video_name", {"creative_features": {"$exists": True}})
        video_files = [f for f in all_video_files if os.path.splitext(f)[0] not in already_processed]
        video_dir = VIDEO_DIR

    for filename in tqdm(video_files, desc="Processing videos", unit="video"):
        total_processed += 1
        full_path = os.path.join(video_dir, filename)
        response = extract_creative_features(client, full_path, prompt)
        if response:
            features = validate_and_structure_output(response)
            if features:
                if mode != "dry":
                    updated = update_video_document(collection, filename, features)
                    if updated:
                        success_count += 1
                    else:
                        not_found_in_db.append(filename)
                else:
                    print(f"Dry-run result for {filename}:")
                    print(json.dumps(features, indent=2))
                    success_count += 1
            else:
                failed_files.append(filename)
        else:
            failed_files.append(filename)

    logging.info(f"Processing complete. Total: {total_processed}, Success: {success_count}, Validation failed: {len(failed_files)}, Not found in DB: {len(not_found_in_db)}")
    if failed_files:
        logging.info(f"Files that failed validation or Gemini API: {failed_files}")
    if not_found_in_db:
        logging.info(f"Files not found in MongoDB: {not_found_in_db}")

# Entry point
def main():
    parser = argparse.ArgumentParser(description="Batch process TikTok ads.")
    parser.add_argument("--mode", choices=["dry", "test", "prod"], default="prod", help="Run mode: dry, test, or prod")
    args = parser.parse_args()
    batch_process_videos(mode=args.mode)

if __name__ == "__main__":
    main()