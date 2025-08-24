from dataclasses import dataclass
from models.robot_position import RobotPosition

@dataclass
class RobotState:
    robot_position: RobotPosition
    grip_open: bool
