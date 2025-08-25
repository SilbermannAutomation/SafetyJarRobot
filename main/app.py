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
    manager.synchronized_move_pulses(target_positions, velocity=350, hold=True)
    manager.print_all_positions()
    print("[RUN] Job completed")

def job_with_torque(values, torque_settings):
        target_positions = {
            "base_yaw": values[0],
            "shoulder": values[1],
            "elbow": values[2],
            "wrist_pitch": values[3],
            "wrist_roll": values[4],
            "gripper": values[5]
        }
        torque_map = {
            "base_yaw": torque_settings[0],
            "shoulder": torque_settings[1],
            "elbow": torque_settings[2],
            "wrist_pitch": torque_settings[3],
            "wrist_roll": torque_settings[4],
            "gripper": torque_settings[5]
        }
        manager.set_torque(torque_map)
        manager.synchronized_move_pulses(target_positions, velocity=350, hold=True)
        manager.print_all_positions()

@app.route("/", methods=["GET"])
def index():
    defaults = [("Base Yaw", 500, False), ("Shoulder", 500, True), ("Elbow", 500, True), ("Wrist Pitch", 500, True), ("Wrist Roll", 500, True), ("Gripper", 500, True)]
    return render_template("index.html", defaults=defaults)

@app.route("/run", methods=["POST"])
def run():
    vals = [request.form.get(f"p{i}", type=float) for i in range(1, 7)]
    torques = [request.form.get(f"t{i}", type=bool) for i in range(1, 7)]
    for i in range(1, 7):
        print(f"Value {i}: {vals[i-1]}, Torque: {torques[i-1]}")
    
    if any(v is None for v in vals) or any(t is None for t in torques):
        return {"status": "error", "message": "Missing parameters"}, 400

    threading.Thread(target=job_with_torque, args=(vals, torques), daemon=True).start()
    return {"status": "ok", "values": vals, "torques": torques}

if __name__ == "__main__":
    use_https = os.getenv("USE_HTTPS", "0") == "1"
    host = "0.0.0.0"
    if use_https:
        app.run(host=host, port=5001, ssl_context=("cert.pem", "key.pem"))
    else:
        app.run(host=host, port=5000)