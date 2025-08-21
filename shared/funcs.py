from shared.vars import Vars
from models.robot_position import RobotPosition

class Funcs:

    def go_to_position(pos: RobotPosition):
        print(f"Двигаем робота в позицию:")
        print(f"A1: {pos.ax1}, A2: {pos.ax2}, A3: {pos.ax3}, "
          f"A4: {pos.ax4}, A5: {pos.ax5}, Gripper open: {pos.grip_open}")



