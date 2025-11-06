import os
import requests
from dotenv import load_dotenv

load_dotenv()

# ✅ Only using the free model
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_ID = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


def generate_text(prompt: str) -> str:
    """Generate text using Groq’s free-tier Llama 3.1 8B model."""
    if not GROQ_API_KEY:
        return "⚠️ Missing GROQ_API_KEY in .env."

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a friendly personal finance assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 400
    }

    try:
        res = requests.post(API_URL, headers=HEADERS, json=payload, timeout=90)

        if res.status_code == 401:
            return "❌ Invalid or expired API key."
        elif res.status_code == 404:
            return f"⚠️ Model not found → {MODEL_ID}."
        elif res.status_code == 429:
            return "⏳ Rate limit reached — wait a few minutes."
        elif res.status_code != 200:
            return f"⚠️ API {res.status_code}: {res.text}"

        data = res.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"❌ Network error: {e}"
