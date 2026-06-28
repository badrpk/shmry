from flask import Flask, request, Response, jsonify
import urllib.request

app = Flask(__name__)

def forward(path):
    target = "http://127.0.0.1:8099" + path
    try:
        if request.query_string:
            target += "?" + request.query_string.decode()
        req = urllib.request.Request(target)
        with urllib.request.urlopen(req, timeout=30) as r:
            return Response(
                r.read(),
                status=r.status,
                content_type=r.headers.get("Content-Type", "text/html")
            )
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "target": target}), 502

@app.route("/")
def root():
    return '<h2>NIFDU Gateway</h2><p><a href="/app">Open SHMRY App</a></p>'

@app.route("/app", methods=["GET"])
def app_proxy():
    return forward("/app")

@app.route("/ai/chat", methods=["POST"])
def chat_proxy():
    import requests
    res = requests.post("http://127.0.0.1:8099/ai/chat", json=request.get_json(silent=True), timeout=60)
    return Response(res.content, status=res.status_code, content_type=res.headers.get("Content-Type","application/json"))

@app.route("/ai/voice", methods=["POST"])
def voice_proxy():
    import requests
    res = requests.post("http://127.0.0.1:8099/ai/voice", data=request.form, files=request.files, timeout=120)
    return Response(res.content, status=res.status_code, content_type=res.headers.get("Content-Type","application/json"))

@app.route("/health")
def health():
    return forward("/health")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
