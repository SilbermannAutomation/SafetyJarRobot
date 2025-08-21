from dataclasses import dataclass

@dataclass
class RobotPosition:
    ax1: int
    ax2: int
    ax3: int
    ax4: int
    ax5: int
    grip_open: bool
