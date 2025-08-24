from models.robot_position import RobotPosition

class Vars:
    POS_1_1_up = RobotPosition( #first line, first place, above the object, open gripper
        ax1=0,
        ax2=45,
        ax3=90,
        ax4=90,
        ax5=0
    )
    
    POS_1_1_down = RobotPosition( #first line, first place, on the object, open gripper
        ax1=0,
        ax2=25,
        ax3=60,
        ax4=90,
        ax5=0
    )
    
    POS_1_1_catch = RobotPosition(#first line, first place, above the object, closed gripper
        ax1=0,
        ax2=25,
        ax3=60,
        ax4=90,
        ax5=0
    )
