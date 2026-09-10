"""This file isolates the Gemini client initialization and the backoff retry logic."""

import time
import random
from google import genai
from google.genai import types
from .config import GEMINI_API_KEY

def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def extract_handwriting(image, max_retries=3):
    client = get_gemini_client()
    if not client: raise Exception("Gemini API key is missing.")
    image.thumbnail((1024, 1024))
    prompt = "You are an expert handwriting transcription engine. Read the handwritten text verbatim. Label each question clearly at the start using tags like (Q1), (Q2)."
    
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model='gemini-3.7-flash', contents=[prompt, image],
                config=types.GenerateContentConfig(temperature=0.0)
            ).text.strip()
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep((2.0 * (2 ** attempt)) + random.uniform(0, 1))
                continue
            raise e