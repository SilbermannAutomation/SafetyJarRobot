import ros_robot_controller_sdk as rrc
import time
import logging


class RobotController:
    def __init__(self, port="/dev/serial0", baud=1_000_000, axes=6):
        self.axes = axes  # количество осей
        self._board = rrc.Board(device=port, baudrate=baud, timeout=5)
        self._board.enable_reception(True)

        # настройка логирования
        logging.basicConfig(
            level=logging.INFO,
            format="[%(levelname)s] %(asctime)s - %(message)s",
            datefmt="%H:%M:%S"
        )

        self._enable_torque()

    def _enable_torque(self):
        """Включает питание (torque) на всех осях"""
        for sid in range(1, self.axes + 1):
            try:
                self._board.bus_servo_enable_torque(sid, 1)
                time.sleep(0.01)
                logging.info(f"Torque enabled on axis {sid}")
            except Exception as e:
                logging.error(f"Failed to enable torque on axis {sid}: {e}")

    def move_axis(self, axis_id, pulse):
        """Двигает одну ось"""
        try:
            self._board.bus_servo_set_position(0.5, [[axis_id, int(pulse)]])
            logging.debug(f"Axis {axis_id} -> {pulse}")
            return True
        except Exception as e:
            logging.error(f"Error moving axis {axis_id}: {e}")
            return False

    def move_axes(self, axes_dict):
        """
        Двигает несколько осей сразу.
        axes_dict = {axis_id: pulse, ...}
        """
        try:
            positions = [[axis, int(pulse)] for axis, pulse in axes_dict.items()]
            self._board.bus_servo_set_position(0.5, positions)
            logging.debug(f"Axes moved: {axes_dict}")
            return True
        except Exception as e:
            logging.error(f"Error moving axes: {e}")
            return False

    def get_axis_position(self, axis_id):
        """Читает позицию оси (если SDK поддерживает)"""
        try:
            pos = self._board.bus_servo_read_position(axis_id)
            logging.debug(f"Axis {axis_id} position = {pos}")
            return pos
        except Exception as e:
            logging.error(f"Error reading axis {axis_id}: {e}")
            return None