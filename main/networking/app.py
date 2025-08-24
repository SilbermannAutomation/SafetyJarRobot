from flask import Flask, render_template, request, jsonify
import os, threading, time

app = Flask(__name__)

def run_job(values):
    """
    TODO: Replace this with your actual logic.
    This runs in a background thread so the UI stays responsive.
    """
    print(f"[RUN] Received values: {values}")
    # Simulate some work
    time.sleep(2)
    print("[RUN] Job completed")

@app.route("/", methods=["GET"])
def index():
    # Default values (0-100)
    defaults = [50, 50, 50, 50, 50, 50]
    return render_template("index.html", defaults=defaults)

@app.route("/run", methods=["POST"])
def run():
    # Collect values p1..p6 from the POST body
    vals = []
    for i in range(1, 7):
        v = request.form.get(f"p{i}", type=float)
        if v is None:
            return jsonify({"status": "error", "message": f"Missing p{i}"}), 400
        vals.append(v)

    # Start background task
    t = threading.Thread(target=run_job, args=(vals,), daemon=True)
    t.start()

    return jsonify({"status": "ok", "values": vals})

if __name__ == "__main__":
    use_https = os.getenv("USE_HTTPS", "0") == "1"
    host = "0.0.0.0"
    if use_https:
        # Place cert.pem and key.pem in the project directory for HTTPS
        app.run(host=host, port=5001, ssl_context=("cert.pem", "key.pem"))
    else:
        app.run(host=host, port=5000)