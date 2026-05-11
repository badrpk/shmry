import os
import requests

def llm_reply(prompt: str) -> str:
  provider = os.getenv("LLM_PROVIDER", "none").lower().strip()
  if provider == "none":
    return ""
  if provider == "openai":
    # Placeholder: plug your own OpenAI client here
    # Keep it as a stub so the scaffold runs without external deps.
    return ""
  if provider == "gemini":
    return ""
  return ""
