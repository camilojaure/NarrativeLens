import os
import dotenv
import time
from google import genai

def analyze_video_gemini_client(video_file_path, prompt, api_key):
    """Analyzes a video using the Gemini API

    Args:
        video_file_path: Path to the video file.
        prompt: Text prompt for the analysis.
        api_key: Google API key.

    Returns:
        The response from the Gemini API, or None on error.
    """
    client = None
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None

    file_ref = None
    try:
        file_ref = client.files.upload(file=video_file_path)
        print(f"File uploaded successfully. file_ref={file_ref.uri}")
    except Exception as e:
        print(f"Error uploading video file: {e}")
        return None

    if not file_ref:
        print("File upload failed, cannot proceed with analysis.")
        return None

    # Attempt the generate_content call with retries
    max_retries = 3
    delay_seconds = 5

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-pro-latest",
                contents=[prompt, file_ref]
            )
            print("API call success")
            return response

        except Exception as e:
            #Uploads seems to be a bit lazy, so im adding a delay and retry mechanism
            print(f"Attempt {attempt + 1} failed: Gemini API Error: {e}")
            if attempt < max_retries - 1:
                print(f"Waiting {delay_seconds} seconds before retrying...")
                time.sleep(delay_seconds)
            else:
                print("Max retries reached. Aborting video analysis.")
                return None  # Abort after max retries

def process_gemini_response(response):
    """Processes the Gemini API response to extract the text."""
    if response and hasattr(response, "text"):
        return response.text
    else:
        print("Error: No text found in Gemini response.")
        if response:
            print("Full response:", response)
        return None

def main():
    """Main function to orchestrate the video analysis."""
    dotenv.load_dotenv()

    video_path = "/Users/camilojaureguiberry/Documents/Projects/Developments/NarrativeLens/data/pedidos_ya_130125.mp4"  # Replace with your video
    prompt = """Analyze the following video ad and extract its narrative structure in JSON format with these fields:
        Ad Name, 
        Scene Number, 
        Start Time, 
        End Time, 
        Scene Duration, 
        Narrative Role, 
        Visual Elements, 
        Voice-over Tone, 
        On-screen Text, 
        Pacing."""
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return

    response = analyze_video_gemini_client(video_path, prompt, api_key)

    if response:
        generated_text = process_gemini_response(response)
        if generated_text:
            print("Gemini's Response:\n", generated_text)
        else:
            print("Failed to extract text from the response.")
    else:
        print("Video analysis failed.")

if __name__ == "__main__":
    main()

#TODO:
#0. Add pydantic for structured output format 
#1. Add more error handling and logging
#2. Add langsmith tracing
#3. Add more features extraction
