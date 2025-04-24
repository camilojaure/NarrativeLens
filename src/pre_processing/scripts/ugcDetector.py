"""ugcDetector.py
Detects whether a video ad is UGC‑style and records the result in MongoDB:
    - is_ugc            → True / False
    - ugc_explanation   → brief reason

Run:
    python ugcDetector.py --mode [dry|test|prod]   # default = prod
"""

import logging
import os
import dotenv
import time
import json
import re
import argparse
from pymongo import MongoClient
from google import genai
from pydantic import ValidationError
from datamodelValidation import UGCAnalysis, UGCAnswer
from tqdm import tqdm

# ─────────────────────────────── Logging ──────────────────────────────────── #
LOG_FILE = (
    "/Users/camilojaureguiberry/Documents/Projects/Developments/"
    "NarrativeLens/src/pre_processing/logs/ugc_detector.log"
)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ────────────────────────────── Constants ─────────────────────────────────── #
VIDEO_DIR = (
    "/Users/camilojaureguiberry/Documents/Projects/Developments/"
    "NarrativeLens/data/video_ads"
)
PROMPT_PATH = (
    "/Users/camilojaureguiberry/Documents/Projects/Developments/"
    "NarrativeLens/src/pre_processing/prompts/is_ugc_prompt.txt"
)

# ────────────────────────── Gemini API helper ────────────────────────────── #
def detect_ugc(client: genai.Client, video_fp: str, prompt: str):
    """Upload the video + prompt to Gemini and return the raw response."""
    try:
        file_ref = client.files.upload(file=video_fp)
        logging.info(f"Uploaded {os.path.basename(video_fp)} → {file_ref.uri}")
    except Exception as e:
        logging.error(f"File upload failed: {e}")
        return None

    for attempt in range(3):
        try:
            time.sleep(5)
            return client.models.generate_content(
                model="gemini-1.5-pro-latest", contents=[prompt, file_ref]
            )
        except Exception as e:
            logging.warning(
                f"Gemini call attempt {attempt + 1} failed: {e}; retrying..."
            )
            time.sleep(5)
    return None

# ───────────────────────────── Mongo helpers ──────────────────────────────── #
def collection():
    return MongoClient("mongodb://localhost:27017/") \
        ["NarrativeLens"]["tiktok_ads_us_toplikes"]


def update_doc(coll, video_fname: str, is_ugc: bool, explanation: str):
    key = os.path.splitext(video_fname)[0]
    r = coll.update_one(
        {"video_name": key},
        {"$set": {"is_ugc": is_ugc, "ugc_explanation": explanation}}
    )
    if r.matched_count == 0:
        logging.warning(f"Mongo: no doc for {video_fname}")
        return False
    return True


# ───────────────────────────── Utilities ─────────────────────────────────── #
def load_prompt(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


# ─────────────────────────── Batch runner ────────────────────────────────── #
def batch_process(mode: str = "prod"):
    dotenv.load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logging.critical("GOOGLE_API_KEY missing.")
        return
    if not os.path.exists(VIDEO_DIR):
        logging.critical(f"Video dir not found: {VIDEO_DIR}")
        return

    client = genai.Client(api_key=api_key)
    prompt = load_prompt(PROMPT_PATH)
    coll = collection()

    # choose files
    if mode == "dry":
        root = VIDEO_DIR + "_dry"
        files = [f for f in os.listdir(root) if f.endswith(".mp4")][:1]
    elif mode == "test":
        root = VIDEO_DIR + "_test"
        files = [f for f in os.listdir(root) if f.endswith(".mp4")]
    else:  # prod incremental
        root = VIDEO_DIR
        done = coll.distinct("video_name", {"is_ugc": {"$exists": True}})
        files = [
            f for f in os.listdir(root) if f.endswith(".mp4")
            and os.path.splitext(f)[0] not in done
        ]

    total, ok = 0, 0
    for fname in tqdm(files, desc="UGC detection", unit="video"):
        total += 1
        resp = detect_ugc(client, os.path.join(root, fname), prompt)
        parsed = parse_ugc_response(resp)
        if parsed:
            is_ugc, expl = parsed
            if update_doc(coll, fname, is_ugc, expl):
                ok += 1

    logging.info(f"UGC batch done. Total: {total}, Success: {ok}, Fail: {total-ok}")


# ───────────────────────────── Response post‑processing ──────────────────────── #
YESNO_RE = re.compile(r"^\s*(?:Answer[:\-\s]*)?(Yes|No)\b[:\-\s\.]*", re.IGNORECASE)
JSON_RE = re.compile(r"\{.*\}", re.DOTALL)

# Parsed JSON is validated against UGCAnalysis (Pydantic) to ensure the model
# returns an "answer" ("Yes"/"No") and a "justification".
def parse_ugc_response(response):
    if not (response and hasattr(response, "text")):
        return None

    raw = response.text.strip()
    logging.info(f"Raw response: {raw}")

    # First, try JSON.
    match = JSON_RE.search(raw)
    if match:
        try:
            data = json.loads(match.group(0))
            # Normalize answer if needed
            if "answer" in data:
                data["answer"] = str(data["answer"]).strip().capitalize().rstrip(".")
            result = UGCAnalysis(**data)
            return result.answer == UGCAnswer.YES, result.justification
        except (json.JSONDecodeError, ValidationError):
            logging.warning("JSON present but invalid, falling back to text.")

    # Fallback: plain "Yes / No — explanation" text
    m = YESNO_RE.search(raw)
    if m:
        ans = m.group(1).capitalize().rstrip(".")
        justification = raw[m.end():].strip()
        try:
            result = UGCAnalysis(answer=ans, justification=justification)
            return result.answer == UGCAnswer.YES, result.justification
        except ValidationError as e:
            logging.error(f"Pydantic validation failed: {e}")
            return None

    logging.error("Could not parse Gemini response.")
    return None


# ───────────────────────────── CLI entry‑point ───────────────────────────── #
def main():
    p = argparse.ArgumentParser(description="Batch UGC detection.")
    p.add_argument("--mode", choices=["dry", "test", "prod"], default="prod")
    batch_process(p.parse_args().mode)


if __name__ == "__main__":
    main()