from dataclasses import dataclass

@dataclass
class RobotPosition:
    wrist_roll: int
    wrist_pitch: int
    elbow: int
    shoulder: int
    base_yaw: int
