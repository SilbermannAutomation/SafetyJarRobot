from dataclasses import dataclass

@dataclass
class RobotPosition:
    positions: dict

    def __init__(self, base_yaw=500, shoulder=500, elbow=500, wrist_pitch=500, wrist_roll=500, gripper=500):
        self.positions = {
            "base_yaw": base_yaw,
            "shoulder": shoulder,
            "elbow": elbow,
            "wrist_pitch": wrist_pitch,
            "wrist_roll": wrist_roll,
            "gripper": gripper
        }

    # def __init__(self, values: list):
    #     self.positions = {
    #         "base_yaw": values[0],
    #         "shoulder": values[1],
    #         "elbow": values[2],
    #         "wrist_pitch": values[3],
    #         "wrist_roll": values[4],
    #         "gripper": values[5]
    #     }
