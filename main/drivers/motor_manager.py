import json
import os
import time
from drivers.servo import Motor
from utils.util import Util  # for clamping

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

    def get_motor(self, name) -> Motor:
        return self.motors.get(name)

    def all_names(self):
        return list(self.motors.keys())

    def synchronized_move_pulses(self, target_pulses_dict: dict, hold=True):
        """
        Move all specified motors to their target pulse positions (0–1000),
        synchronizing so that all arrive at the same time.

        Args:
            target_pulses_dict: dict {motor_name: pulse_target}
            hold: if False, torque will be released after the move
        """
        durations = []
        pulse_targets = []

        # Step 1: compute durations and clamp target pulses
        for name, target in target_pulses_dict.items():
            motor = self.get_motor(name)
            if motor is None:
                raise ValueError(f"Motor '{name}' not found")

            target = Util._clamp(int(target), motor.soft_min, motor.soft_max)
            current = motor.readPosition(units="pulses")
            if current is None:
                current = target

            distance = abs(target - current)
            default_velocity = 4.17  # 1000 pulses / 240 deg/s
            duration = distance / default_velocity if distance > 0 else motor.MIN_DURATION_S
            duration = Util._clamp(duration, motor.MIN_DURATION_S, motor.MAX_DURATION_S)

            durations.append(duration)
            pulse_targets.append((motor.id, target))

        if not pulse_targets:
            return

        max_dur = max(durations)

        # Step 2: send all servo commands in one call (same duration)
        board = Motor._BoardSingleton.get()
        board.bus_servo_set_position(max_dur, pulse_targets)

        time.sleep(max_dur + 0.1)

        # Step 3: release torque if hold is False
        if not hold:
            for name in target_pulses_dict:
                motor = self.get_motor(name)
                if motor:
                    try:
                        motor.turnOffTorque()
                    except Exception:
                        pass
