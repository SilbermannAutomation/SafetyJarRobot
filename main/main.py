from drivers.servo import Motor
import time
from drivers.motor_manager import MotorManager

# ----------- Example usage -----------
if __name__ == "__main__":
    MOTOR_IDS = [1, 2, 3, 4, 5, 6]
    SERVOS = [Motor(sid, device="/dev/serial0", baud=1_000_000, name=f"motor{sid}", range_deg=240.0) for sid in MOTOR_IDS]
    MANAGER = MotorManager("/controller/servo_map.json")

    # Move all servos to specific pulses, synchronized
    target_positions = {
        "base_yaw": 400,
        "shoulder": 400,
        "elbow": 400,
        "wrist_pitch": 400,
        "wrist_roll": 400,
        "gripper": 500
    }


    MANAGER.synchronized_move_pulses(target_positions, hold=True)


    # for servo in SERVOS:
    #     servo.turn_on_torque()
    #     servo.goToPosition(500, duration=0.5, hold=True)

    # time.sleep(2)
    

    # SERVOS[0].goToPosition(530, duration=0.5, hold=True)
    # SERVOS[1].goToPosition(498, duration=0.5, hold=True)
    # SERVOS[2].goToPosition(710, duration=0.5, hold=True)
    # SERVOS[3].goToPosition(0, duration=0.5, hold=True)
    # SERVOS[4].goToPosition(260, duration=0.5, hold=True)
    # SERVOS[5].goToPosition(500, duration=0.5, hold=True)

    # Simple demo: set up one motor and try a few moves.
    # Adjust SERVO_ID below.
    # SERVO_ID = 2

    # m = Motor(SERVO_ID, device="/dev/serial0", baud=1_000_000, name="base", range_deg=240.0)
    # print("Status:", m.readStatus())

    # # Gentle center
    # print("Homing...")
    # m.home(mid=500, duration=2.0)

    
    # # Move by pulses at 120 pulses/s
    # print("Move to 650 pulses @ 120 pulses/s ...")
    # m.goToPosition(650, velocity=120, units="pulses", hold=True)

    # # Move by degrees at 45 deg/s (range 240° assumed)
    # print("Move to 30° @ 45 deg/s ...")
    # m.goToPosition(30.0, velocity=45.0, units="deg", hold=True)

    # # Nudge + stop + torque off
    # print("Nudge + stop + torque off ...")
    # m.nudge(+20)
    # m.stop()
    # m.turnOffTorque()
    # print("Done.")