from datetime import datetime
from typing import Dict, Tuple
from .db import exec_one, fetch_all
from .guardrails import (
  DISCLAIMER,
  is_personalized_advice_request,
  safe_response_for_advice_request,
  wrap_with_disclaimer,
)

def _now() -> str:
  return datetime.now().replace(microsecond=0).isoformat()

HELP = (
  "*SHMRY WhatsApp Assistant (Safe Mode)*\\n"
  "Commands:\\n"
  "• `help`\\n"
  "• `add SYMBOL QTY PRICE`  (adds/updates position avg)\\n"
  "• `portfolio`\\n"
  "• `note ...`\\n"
  "• `notes`\\n"
  "• `reset SYMBOL`\\n"
  "• `disclaimer`\\n\\n"
  "Ask education questions like: `what is diversification?` or `explain PE ratio`."
)

def log_message(wa_id: str, direction: str, body: str) -> None:
  exec_one(
    "INSERT INTO messages(wa_id,direction,body,ts) VALUES(?,?,?,?)",
    (wa_id, direction, body, _now()),
  )

def ensure_user(wa_id: str) -> None:
  exec_one(
    "INSERT OR IGNORE INTO users(wa_id,created_at) VALUES(?,?)",
    (wa_id, _now()),
  )

def add_position(wa_id: str, symbol: str, qty: float, price: float) -> str:
  symbol = symbol.upper().strip()
  rows = fetch_all("SELECT qty, avg_price FROM portfolio WHERE wa_id=? AND symbol=?", (wa_id, symbol))
  if not rows:
    exec_one(
      "INSERT INTO portfolio(wa_id,symbol,qty,avg_price,updated_at) VALUES(?,?,?,?,?)",
      (wa_id, symbol, qty, price, _now()),
    )
  else:
    old_qty = float(rows[0]["qty"])
    old_avg = float(rows[0]["avg_price"])
    new_qty = old_qty + qty
    if new_qty <= 0:
      exec_one("DELETE FROM portfolio WHERE wa_id=? AND symbol=?", (wa_id, symbol))
      return wrap_with_disclaimer(f"✅ Removed position {symbol} (qty now {new_qty}).")
    # weighted avg only for net adds (simplified)
    new_avg = (old_qty * old_avg + qty * price) / new_qty if qty > 0 else old_avg
    exec_one(
      "UPDATE portfolio SET qty=?, avg_price=?, updated_at=? WHERE wa_id=? AND symbol=?",
      (new_qty, new_avg, _now(), wa_id, symbol),
    )
  return wrap_with_disclaimer(f"✅ Updated {symbol}: +{qty} @ {price}. Use `portfolio` to view.")

def reset_symbol(wa_id: str, symbol: str) -> str:
  symbol = symbol.upper().strip()
  exec_one("DELETE FROM portfolio WHERE wa_id=? AND symbol=?", (wa_id, symbol))
  return wrap_with_disclaimer(f"✅ Reset {symbol} (removed from portfolio).")

def portfolio_view(wa_id: str) -> str:
  rows = fetch_all("SELECT symbol, qty, avg_price, updated_at FROM portfolio WHERE wa_id=? ORDER BY symbol", (wa_id,))
  if not rows:
    return wrap_with_disclaimer("ℹ️ Portfolio empty. Add with: `add SYMBOL QTY PRICE`")
  lines = ["*Portfolio*"]
  for r in rows:
    lines.append(f"• {r[symbol]}: qty={r[qty]}, avg={r[avg_price]}")
  return wrap_with_disclaimer("\\n".join(lines))

def add_note(wa_id: str, note: str) -> str:
  exec_one("INSERT INTO notes(wa_id,note,ts) VALUES(?,?,?)", (wa_id, note.strip(), _now()))
  return wrap_with_disclaimer("📝 Noted.")

def list_notes(wa_id: str) -> str:
  rows = fetch_all("SELECT ts,note FROM notes WHERE wa_id=? ORDER BY id DESC LIMIT 10", (wa_id,))
  if not rows:
    return wrap_with_disclaimer("ℹ️ No notes yet. Add: `note ...`")
  out = ["*Last notes (10)*"]
  for r in rows:
    out.append(f"• {r[ts]}: {r[note]}")
  return wrap_with_disclaimer("\\n".join(out))

def education_fallback(text: str) -> str:
  # Minimal built-in education answers (you can route to your RAG/LLM later)
  t = text.lower().strip()
  if "diversif" in t:
    return wrap_with_disclaimer(
      "Diversification means spreading risk across assets/sectors so one loss doesn’t dominate. "
      "A simple rule: avoid single positions large enough to break your plan if they drop sharply."
    )
  if "p/e" in t or "pe ratio" in t:
    return wrap_with_disclaimer(
      "P/E (price-to-earnings) compares price to earnings per share. Higher P/E can mean higher growth expectations "
      "or overvaluation; compare within the same industry and consider earnings quality and cycles."
    )
  return wrap_with_disclaimer(
    "I can help with general education + portfolio tracking. Try `help`, `portfolio`, or ask an investing concept question."
  )

def handle_text(wa_id: str, body: str) -> str:
  ensure_user(wa_id)
  log_message(wa_id, "in", body)

  if is_personalized_advice_request(body):
    resp = safe_response_for_advice_request()
    log_message(wa_id, "out", resp)
    return resp

  parts = body.strip().split()
  if not parts:
    resp = wrap_with_disclaimer("Send `help` for commands.")
    log_message(wa_id, "out", resp)
    return resp

  cmd = parts[0].lower()

  if cmd in ("help", "/help"):
    resp = wrap_with_disclaimer(HELP)
  elif cmd == "disclaimer":
    resp = DISCLAIMER
  elif cmd == "add" and len(parts) >= 4:
    sym = parts[1]
    qty = float(parts[2])
    price = float(parts[3])
    resp = add_position(wa_id, sym, qty, price)
  elif cmd == "reset" and len(parts) >= 2:
    resp = reset_symbol(wa_id, parts[1])
  elif cmd in ("portfolio", "pf"):
    resp = portfolio_view(wa_id)
  elif cmd == "note":
    resp = add_note(wa_id, body[len("note"):].strip())
  elif cmd == "notes":
    resp = list_notes(wa_id)
  else:
    resp = education_fallback(body)

  log_message(wa_id, "out", resp)
  return resp
