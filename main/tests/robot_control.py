import ros_robot_controller_sdk as rrc
import time

class RobotController:
    def __init__(self):
        self._board = rrc.Board(device="/dev/serial0", baudrate=1_000_000, timeout=5)
        self._board.enable_reception(True)
        self._enable_torque()

    def _enable_torque(self):
        for sid in range(1, 7):
            try:
                self._board.bus_servo_enable_torque(sid, 1)
                time.sleep(0.01)
            except Exception:
                pass

    def move_axis(self, axis_id, pulse):
        try:
            self._board.bus_servo_set_position(0.5, [[axis_id, int(pulse)]])
        except Exception as e:
            print(f"Error moving axis {axis_id}: {e}")
