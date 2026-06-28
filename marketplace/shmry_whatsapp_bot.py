from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()

    reply = "SHMRY received your message."

    try:
        r = requests.post(
            "http://127.0.0.1:5060/api/cognitive_commerce",
            json={"query": incoming_msg},
            timeout=8
        )
        data = r.json()
        reply = (
            data.get("marketplace_response", {}).get("reply")
            or data.get("reply")
            or data.get("message")
            or "SHMRY received your message."
        )
    except Exception as e:
        reply = f"SHMRY is online, but gateway reply failed: {type(e).__name__}"

    resp = MessagingResponse()
    resp.message(str(reply))
    return str(resp), 200, {"Content-Type": "application/xml"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
