from flask import Flask, jsonify, request
from flask_cors import CORS
from stock_cache import update_cache, read_cache

app = Flask(__name__)
CORS(app)

@app.route("/")
def dashboard():
    return app.send_static_file("index.html")

@app.route("/stock/<sku>")
def get_stock(sku):
    cache = read_cache()
    item = cache.get(sku)
    if item is None:
        return jsonify({"error": "SKU not found"})
    return jsonify(item)

@app.route("/webhook/stock-update", methods=["POST"])
def stock_webhook():
    payload = request.get_json()
    sku = payload["sku"]

    cache = read_cache()
    cache[sku] = {"name": payload["name"], "stock": payload["stock"]}
    update_cache(cache)

    print("Webhook received:", payload)
    return jsonify({"status": "received"})

if __name__ == "__main__":
    app.run(port=8000)
