import json
import os
from servo import Motor
from utils.util import Util  # Needed for deg↔pulses conversion
from controller.control_board_singleton import _BoardSingleton

class MotorManager:
    def __init__(self, json_path='servo_map.json'):
        self.motors = {}  # name -> Motor instance
        self._load_servos(json_path)

    def _load_servos(self, json_path):
        if not os.path.isfile(json_path):
            raise FileNotFoundError(f"Servo map file not found: {json_path}")

        with open(json_path, 'r') as f:
            servo_map = json.load(f)

        for name, servo_id in servo_map.items():
            self.motors[name] = Motor(servo_id, name=name)

    def get_motor(self, name):
        return self.motors.get(name)

    def all_names(self):
        return list(self.motors.keys())

    def synchronized_move_deg(self, target_angles: dict, hold=True):
        """
        Move all given motors to their respective target angles (in degrees),
        such that all arrive simultaneously. Requires current position readout.
        Args:
            target_angles: dict of {motor_name: target_deg}
            hold: whether to hold position after move
        """
        durations = []
        pulse_targets = []

        # Step 1: compute all target pulses and durations
        for name, target_deg in target_angles.items():
            motor = self.get_motor(name)
            if motor is None:
                raise ValueError(f"Motor '{name}' not found")

            target_pulses = Util.pulses_from_deg(target_deg, motor.range_deg)
            target_pulses = Util._clamp(target_pulses, motor.soft_min, motor.soft_max)

            current_pulses = motor.readPosition(units="pulses")
            if current_pulses is None:
                current_pulses = target_pulses  # fallback

            distance = abs(target_pulses - current_pulses)
            # assume default velocity: 240 deg/s
            pulses_per_deg = 1000.0 / motor.range_deg
            default_velocity = 240.0 * pulses_per_deg
            dur = distance / default_velocity if distance > 0 else 0.15
            durations.append(Util._clamp(dur, motor.MIN_DURATION_S, motor.MAX_DURATION_S))

            pulse_targets.append((motor.id, int(target_pulses)))

        if not durations:
            return

        # Step 2: compute max duration so all arrive together
        max_dur = max(durations)

        # Step 3: send all move commands in one batch
        if pulse_targets:
            _BoardSingleton.get().bus_servo_set_position(max_dur, pulse_targets)

        # Optional wait
        import time
        time.sleep(max_dur + 0.1)

        # Step 4: handle hold/release
        if not hold:
            for name in target_angles:
                motor = self.get_motor(name)
                if motor:
                    try:
                        motor.turnOffTorque()
                    except Exception:
                        pass
