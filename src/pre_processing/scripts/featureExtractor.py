import logging
import os
import dotenv
import time
import json
import re
from google import genai
from datamodelValidation import AdAnalysis, CreativeTheme, CreativeConcept, FormatProductionStyle, TalentType, DemographicRepresentation, AudienceFocus, CampaignObjective 
from pydantic import ValidationError

log_file = "/Users/camilojaureguiberry/Documents/Projects/Developments/NarrativeLens/src/pre_processing/logs/feature_extractor.log"
log_level = logging.INFO

logging.basicConfig(filename=log_file, 
                    level=log_level, 
                    format="%(asctime)s - %(levelname)s - %(message)s", 
                    datefmt="%Y-%m-%d %H:%M:%S",)

def analyze_video_gemini_client(video_file_path, prompt, api_key):
    """Analyzes a video using the Gemini API"""
    client = None
    try:
        client = genai.Client(api_key=api_key)
        logging.info("Gemini client initialized successfully.") 
    except Exception as e:
        logging.error(f"Error initializing Gemini client: {e}") 
        return None

    file_ref = None
    try:
        file_ref = client.files.upload(file=video_file_path)
        logging.info(f"File uploaded successfully. File URL is {file_ref.uri}")
    except Exception as e:
        logging.error(f"Error uploading video file: {e}")
        return None

    if not file_ref:
        logging.warning("File upload failed, cannot proceed with analysis.")
        return None

    #We need to wait for the file to uploads, 5 seconds seems to be enough
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
                logging.info(f"Waiting {delay_seconds} seconds before retrying...") 
                time.sleep(delay_seconds)
            else:
                logging.warning("Max retries reached. Aborting video analysis.") 
                return None

def process_gemini_response(response):
    """Processes the Gemini API response to extract the data."""
    if response and hasattr(response, "text"):
        raw_response_text = response.text
        logging.debug(f"Raw response text: {raw_response_text}")
        match = re.search(r"\{.*\}", raw_response_text, re.DOTALL)
        if match:
            json_string = match.group(0)
            try:
                data = json.loads(json_string)
                ad_analysis = AdAnalysis(**data)
                logging.info("Successfully validated output") 
                return ad_analysis.model_dump()
            except (json.JSONDecodeError, ValidationError) as e:
                logging.error(f"Validation error: {e}")
                return None

        else:
            logging.warning("Error: Could not find JSON object in response.")
            return None

    else:
        logging.error("Error: No text found in response object .")
        if response:
            logging.error(f"Full response: {response}")
        return None

def open_promt_file(prompt_file_path):
    with open(prompt_file_path, 'r') as file:
        prompt = file.read()
    return prompt

def main():
    """Main function to orchestrate the video analysis."""
    dotenv.load_dotenv()

    test_video_path = "/Users/camilojaureguiberry/Documents/Projects/Developments/NarrativeLens/data/pedidos_ya_130125.mp4"  # Replace with your video
    prompt = open_promt_file("/Users/camilojaureguiberry/Documents/Projects/Developments/NarrativeLens/src/pre_processing/prompts/feature_extractor_prompt.txt")
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        logging.critical("GOOGLE_API_KEY not found in environment variables.")
        return

    response = analyze_video_gemini_client(test_video_path, prompt, api_key)

    if response:
        generated_text = process_gemini_response(response)
        if generated_text:
            logging.info("Successfully performed a full cycle")
            print("Gemini's Response:\n", generated_text)
        else:
            logging.warning("Gemini was not able to complete a full cycle. Some kind of Validation problem may happen")
    else:
        logging.warning("Video analysis failed.")

if __name__ == "__main__":
    main()

#DONE:
#Implement the basic feature extractor script
#Review the diversity score and matrix features to adapt prompt and output
#Add pydantic models for the output structure
#Add more error handling and logging

#TODO:
#Add database connection to store the results
    ## I need to get the performance data for each video, from the tiktok downloader
#Add batch processing capabilities for multiple videos
#Add langsmith tracing
#Add more features extraction
