import os
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from dotenv import load_dotenv

from .db import init_db
from .logic import handle_text

load_dotenv()

app = FastAPI(title="SHMRY WhatsApp Safe Advisor")

@app.on_event("startup")
def _startup():
  init_db()

# Generic inbound payload schema you can adapt (Twilio or your own gateway)
class Inbound(BaseModel):
  wa_id: str
  text: str

@app.get("/health")
def health():
  return {"ok": True}

# Meta verify webhook (optional)
@app.get("/webhook")
def verify(request: Request):
  vt = os.getenv("META_VERIFY_TOKEN", "")
  mode = request.query_params.get("hub.mode")
  token = request.query_params.get("hub.verify_token")
  challenge = request.query_params.get("hub.challenge")
  if mode == "subscribe" and token == vt:
    return Response(content=str(challenge or ""), media_type="text/plain")
  return Response(status_code=403)

@app.post("/inbound")
async def inbound(msg: Inbound):
  # This endpoint expects a gateway to POST {wa_id,text}
  reply = handle_text(msg.wa_id, msg.text)
  return {"reply": reply}

# Twilio-compatible (very lightweight): expects form fields From, Body
@app.post("/twilio")
async def twilio(request: Request):
  form = await request.form()
  wa_from = str(form.get("From", ""))
  body = str(form.get("Body", ""))
  # Twilio From is like: whatsapp:+92...
  wa_id = wa_from.replace("whatsapp:", "").strip()
  reply = handle_text(wa_id, body)

  # TwiML response (no external deps)
  xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>{reply}</Message>
</Response>"""
  return Response(content=xml, media_type="application/xml")
