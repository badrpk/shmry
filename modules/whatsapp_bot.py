from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    
    if 'steel' in incoming_msg:
        msg.body("Our live steel rates are: Rebar $650/ton.")
    else:
        msg.body("Welcome to SHMRY. Reply 'steel' for pricing or 'status' for mining.")
    return str(resp)

if __name__ == "__main__":
    app.run(port=5005)
