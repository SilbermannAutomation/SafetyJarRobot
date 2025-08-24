
from controller import ros_robot_controller_sdk as rrc  # Hiwonder SDK module

# ----------- Board (shared) -----------
class _BoardSingleton:
    """Create one shared Board instance for all motors."""
    _instance = None

    @classmethod
    def get(cls, device="/dev/serial0", baud=1_000_000, timeout=5):
        if cls._instance is None:
            b = rrc.Board(device=device, baudrate=baud, timeout=timeout)
            b.enable_reception(True)
            cls._instance = b
        return cls._instance