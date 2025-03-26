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
    prompt = """You are a world-class creative insights analyst specializing in video advertising. Your task is to analyze this entire advertisement and provide a consolidated summary of its key features. Do not describe individual scenes. Focus on the overall ad-level characteristics.
                Deliver the output in JSON format with the following fields:
                Ad Name: (The name or title of the advertisement, if available. If not, provide a descriptive name.)
                Ad Duration: (The total duration of the advertisement in seconds.)
                Format: (The overall format of the advertisement, e.g., "Short-form video ad," "Animated explainer video," "Product demo," etc.)
                Visual Elements: (A concise summary of the dominant visual elements and style of the advertisement, e.g., "Fast-paced montage of product shots," "Warm and inviting scenes of family life," "Clean and minimalist animation," etc.)
                Voice-over Tone: (A description of the overall tone and style of the voice-over, e.g., "Energetic and enthusiastic," "Calm and reassuring," "Authoritative and informative," etc.)
                On-screen Text: (A summary of the key messages and style of the on-screen text used in the advertisement, e.g., "Bold and impactful slogans," "Clear and concise product benefits," "Playful and engaging typography," etc.)
                Pacing: (A description of the overall pacing of the advertisement, e.g., "Fast-paced and energetic," "Slow and deliberate," "Varied pacing to maintain interest," etc.)
                Ad Description: (A brief, high-level overview of the advertisement's overall message, target audience, and intended effect, synthesizing the ad's key features.)
                """
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
#1. Review the diversity score and matrix features to adapt prompt and output
#2. Add pydantic models for the output structure
#3. Add more error handling and logging
#4. Add langsmith tracing
#5. Add more features extraction
