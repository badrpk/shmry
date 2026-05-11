import re
from typing import Tuple

DISCLAIMER = (
  "⚠️ *Important*: I’m not a licensed financial advisor. I can provide general education, "
  "risk checklists, and help you track a portfolio. I can’t give personalized buy/sell calls. "
  "For decisions, consult a regulated professional."
)

BUYSELL_PATTERNS = [
  r"\\b(should i|tell me)\\b.*\\b(buy|sell|short|long)\\b",
  r"\\b(buy|sell)\\b\\s+(this|that|now)\\b",
  r"\\bwhich\\s+stock\\s+to\\s+buy\\b",
  r"\\bgive\\s+me\\s+(a\\s+)?signal\\b",
  r"\\bentry\\b|\\bexit\\b|\\btarget\\b|\\bstop\\s*loss\\b",
]

def is_personalized_advice_request(text: str) -> bool:
  t = text.lower()
  return any(re.search(p, t) for p in BUYSELL_PATTERNS)

def safe_response_for_advice_request() -> str:
  return (
    f"{DISCLAIMER}\\n\\n"
    "I can help you decide *safely* by asking a few questions and giving a checklist:\\n"
    "1) What’s your time horizon (days/months/years)?\\n"
    "2) What % of your net worth is this portfolio?\\n"
    "3) Max loss you can tolerate on this idea?\\n"
    "4) Do you already own the asset? If yes: cost basis + size?\\n\\n"
    "If you share those, I’ll respond with *risk-aware considerations* (not a buy/sell call)."
  )

def wrap_with_disclaimer(msg: str) -> str:
  # Keep it short: disclaimer once per response
  return f"{msg}\\n\\n{DISCLAIMER}"
