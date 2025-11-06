# chatbot.py – PocketSage (Groq LLaMA 3.1) with Emotion Detection & Polished Output
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 🔐 API setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_ID = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


class FinancialChatbot:
    """
    💬 PocketSage – Emotionally aware financial assistant.
    Detects the USER's emotional tone and responds warmly.
    """

    def __init__(self, _=None, debug=False):
        self.history = []
        self.debug = debug

    def ask(self, prompt: str, expenses=None):
        """Generate a response and infer user's emotion."""
        # 🌿 Add spending context
        user_context = ""
        if expenses is not None and not expenses.empty:
            total = expenses["Amount"].sum()
            top_cat = expenses.groupby("Category")["Amount"].sum().idxmax()
            user_context = f"Your total spending so far is ₹{total:.2f}, mostly on {top_cat}. "

        # 🧠 AI setup
        system_prompt = (
            "You are PocketSage, a friendly and emotionally intelligent financial assistant. "
            "Your job is to detect the user's emotional tone and respond calmly, kindly, and helpfully. "
            "Examples: Happy, Frustrated, Sad, Confident, Overwhelmed, Calm, Motivated, Confused. "
            "Respond conversationally with warmth and clarity. "
            "Do NOT include any [UserEmotion:] brackets in your reply — only the natural message text. "
            "After forming your response, imagine the user's emotion and label it as one of the options above."
        )

        # 🗣️ Conversation input
        full_prompt = f"{user_context}\nUser: {prompt.strip()}\nAssistant:"

        payload = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 512,
        }

        try:
            r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=90)
            if r.status_code == 401:
                return {"response": "❌ Invalid Groq API key.", "emotion": "Error"}
            elif r.status_code != 200:
                return {"response": f"⚠️ API {r.status_code}: {r.text}", "emotion": "Error"}

            data = r.json()
            text = data["choices"][0]["message"]["content"].strip()

            # 🧩 Emotion estimation from text content
            lower_text = text.lower()
            if any(word in lower_text for word in ["sad", "upset", "shitty", "down", "cry"]):
                emotion = "Sad"
            elif any(word in lower_text for word in ["stressed", "anxious", "worried"]):
                emotion = "Stressed"
            elif any(word in lower_text for word in ["angry", "mad", "furious", "frustrated"]):
                emotion = "Frustrated"
            elif any(word in lower_text for word in ["happy", "excited", "glad", "yay"]):
                emotion = "Happy"
            elif any(word in lower_text for word in ["confused", "unsure", "lost"]):
                emotion = "Confused"
            elif any(word in lower_text for word in ["proud", "motivated", "determined"]):
                emotion = "Motivated"
            else:
                emotion = "Calm"

            response = text.strip()

            if self.debug:
                print(f"\n🧍 User: {prompt}")
                print(f"🤖 Assistant: {response}")
                print(f"💬 Detected Emotion: {emotion}\n")

            return {"response": response, "emotion": emotion}

        except Exception as e:
            return {"response": f"❌ Network error: {e}", "emotion": "Error"}
