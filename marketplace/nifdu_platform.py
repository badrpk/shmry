from flask import Flask, request, jsonify
import psycopg2, os, secrets
app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host="127.0.0.1",
        port=5433,
        user="badrpk",
        password="Karachi5846$",
        dbname="nifdu_com_db"
    )

@app.route("/health")
def health():
    return jsonify({"ok": True, "service": "nifdu-platform", "version": "v1"})

@app.route("/api/order", methods=["POST"])
def create_order():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    order_id = "NIFDU-" + secrets.token_hex(8).upper()
    cur.execute("INSERT INTO orders (id, customer, service_type, status) VALUES (%s,%s,%s,'pending')", 
                (order_id, data.get("whatsapp"), data.get("service_type")))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"ok": True, "order_id": order_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8130)
