# Savings_Analyser.py
import os
import torch
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class LocalGraniteAnalyzer:
    def __init__(self, model_id="ibm-granite/granite-3.1-1b-a400m-instruct"):
        self.model_id = model_id
        self.pipe = None
        self.available = False
        self._load_granite()

    def _load_granite(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=torch.float32,
                device_map="auto"
            )
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=300,
                temperature=0.6,
                do_sample=True
            )
            self.available = True
            print("✅ IBM Granite model ready.")
        except Exception as e:
            # Silent fail — do not print to Streamlit
            self.available = False
            print(f"(Fallback) IBM Granite load issue: {e}")

    def analyze(self, prompt: str):
        if not self.available:
            raise RuntimeError("Granite model unavailable.")
        result = self.pipe(prompt, return_full_text=False)[0]["generated_text"]
        return result.strip()

















































GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def groq_fallback(prompt: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a financial planning assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }
    try:
        r = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=90)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
        return "Analysis temporarily unavailable. Please try again."
    except Exception:
        return "Network issue — analysis unavailable right now."


# ------------- Unified Analyzer -------------
class SavingsAnalyzer:
    def __init__(self):
        self.granite = LocalGraniteAnalyzer()

    def analyze_savings(self, salary, expenses, duration, loans):
        prompt = f"""
Analyze this savings plan concisely and provide smart insights:

Salary ₹{salary}
Expenses ₹{expenses}
Debt ₹{loans}
Duration {duration} months
"""
        if self.granite.available:
            try:
                return self.granite.analyze(prompt)
            except Exception:
                pass
        return groq_fallback(prompt)
