from flask import Flask, render_template, request, jsonify
import os, threading, time
from drivers.motor_manager import MotorManager
# app.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "networking/templates"  # change to where your index.html lives

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_url_path="/static"             # optional (default is /static)
)

app.config["TEMPLATES_AUTO_RELOAD"] = True  # handy during development

manager = MotorManager("controller/servo_map.json")

def run_job(values):
    """
    TODO: Replace this with your actual logic.
    This runs in a background thread so the UI stays responsive.
    """
    print(f"[RUN] Received values: {values}")
    # Simulate some work
    # Move all servos to specific pulses, synchronized
    target_positions = {
        "base_yaw": values[0],
        "shoulder": values[1],
        "elbow": values[2],
        "wrist_pitch": values[3],
        "wrist_roll": values[4],
        "gripper": values[5]
    }
    manager.synchronized_move_pulses(target_positions, velocity=350, hold=False)
    print("[RUN] Job completed")

@app.route("/", methods=["GET"])
def index():
    defaults = [("Base Yaw", 500), ("Shoulder", 500), ("Elbow", 500), ("Wrist Pitch", 500), ("Wrist Roll", 500), ("Gripper", 500)]
    return render_template("index.html", defaults=defaults)

@app.route("/run", methods=["POST"])
def run():
    vals = [request.form.get(f"p{i}", type=float) for i in range(1, 7)]
    if any(v is None for v in vals):
        return {"status": "error", "message": "Missing parameters"}, 400
    threading.Thread(target=run_job, args=(vals,), daemon=True).start()
    return {"status": "ok", "values": vals}

if __name__ == "__main__":
    use_https = os.getenv("USE_HTTPS", "0") == "1"
    host = "0.0.0.0"
    if use_https:
        app.run(host=host, port=5001, ssl_context=("cert.pem", "key.pem"))
    else:
        app.run(host=host, port=5000)