import ros_robot_controller_sdk as rrc

class RobotController:
    def _init_(self, port="/dev/serial0", baudrate=1_000_000):
        self._board = rrc.Board(device=port, baudrate=baudrate, timeout=5)
        self._board.enable_reception(True)
        self._enable_torque()

    def _enable_torque(self):
        try:
            self._board.bus_servo_enable_torque(254, 1)
        except Exception:
            pass
        for sid in range(1, 7):
            try:
                self._board.bus_servo_enable_torque(sid, 1)
            except Exception:
                pass

    def move_servo(self, axis_id, pulse):
        self._board.bus_servoset_position(0.5, [[axis_id, int(pulse)]])


