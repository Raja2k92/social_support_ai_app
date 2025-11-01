import json
import os

import requests

# ------------------------------
# Configuration
# ------------------------------
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434")
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "gemma3:4b")
USE_LOCAL_LLM = os.environ.get("USE_LOCAL_LLM", "true").strip().lower() in ("1", "true", "yes")
DEFAULT_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT_SEC", "30"))


# ------------------------------
# Ask Ollama
# ------------------------------
def ask_ollama(prompt: str, max_tokens: int = 500, temperature: float = 0.0) -> str:
    """
    Sends prompt to local Ollama LLM and returns the full response text.
    Supports streaming responses.
    """
    if not USE_LOCAL_LLM:
        return "LLM disabled or unavailable."

    url = f"{OLLAMA_BASE}/api/generate"
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        resp = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT, stream=True)
        resp.raise_for_status()

        full_text = ""
        for line in resp.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    chunk = data.get("response", "")
                    full_text += chunk
                    if data.get("done", False):
                        break
                except json.JSONDecodeError:
                    full_text += line.decode("utf-8")

        # Remove code fences
        return full_text.replace("```", "").strip()

    except Exception as e:
        return f"LLM call failed: {e}"
