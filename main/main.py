import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from drivers.servo import Motor
import time
from drivers.motor_manager import MotorManager
from models.robot_position import RobotPosition
from shared.vars import Vars


MANAGER = MotorManager("controller/servo_map.json")

if __name__ == "__main__":
    base_positions = RobotPosition(base_yaw=500, shoulder=500, elbow=500, wrist_pitch=500, wrist_roll=500, gripper=500)

    MANAGER.synchronized_move_pulses(Vars.POS_1_1_UP, velocity=400, hold=True)
    MANAGER.synchronized_move_pulses(Vars.POS_1_1_DOWN, velocity=250, hold=True)
    MANAGER.synchronized_move_pulses(Vars.POS_1_1_CATCH, velocity=350, hold=True)
    MANAGER.synchronized_move_pulses(Vars.POS_1_1_CATCH_UP, velocity=250, hold=True)