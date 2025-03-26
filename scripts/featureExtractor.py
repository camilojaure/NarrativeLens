import base64
import requests
import json

def analyze_video_with_gemini(video_file_path, prompt, api_key):
    """
    Analyzes a video using the Gemini Pro Vision API.

    Args:
        video_file_path: Path to the video file.
        prompt:  Text prompt/question about the video.
        api_key: Your Google AI Studio API key.

    Returns:
        The Gemini API's response as a string, or None on error.
    """

    try:
        with open(video_file_path, "rb") as video_file:
            video_data = video_file.read()
    except FileNotFoundError:
        print(f"Error: Video file not found at {video_file_path}")
        return None

    # Encode video to Base64
    video_base64 = base64.b64encode(video_data).decode("utf-8")

    # Construct the API payload
    payload = {
        "contents": [
            { "type": "text", "text": prompt },
            {
                "type": "image",
                "data": {
                    "mime_type": "video/mp4",  # Adjust if your video is a different format
                    "data": video_base64
                }
            }
        ],
        "tools": []  # Add tools if you need them.
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    #Replace below endpoint with the correct one according to API version
    endpoint_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"

    try:
        response = requests.post(endpoint_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from the API.")
        return None
    
def upload_feautes_to_bigquery():
    """All the extracted features can be uploaded to BigQuery for further analysis"""
    pass

def read_videos_from_bucket():
    """Read the video files from the Google Cloud Storage bucket"""
    pass

def read_videos_from_local():
    """Read the video files from the local storage"""
    pass

if __name__ == "__main__":

    video_path = "path/to/your/video.mp4"  # Replace with your video file path
    user_prompt = "Describe what is happening in this video." # Customize the prompt.
    api_key = "YOUR_API_KEY" #Replace with your API Key

    response = analyze_video_with_gemini(video_path, user_prompt, api_key)

    if response:
        try:
            # Extract the text from the response
            if response["candidates"]:
                generated_text = response["candidates"][0]["content"]["parts"][0]["text"]
                print("Gemini's response:\n", generated_text)
            else:
                print("No response candidates found.")
        except KeyError as e:
            print(f"KeyError: {e}.  Check the API response format.")
            print("Raw response:", response)
    else:
        print("Video analysis failed.")
