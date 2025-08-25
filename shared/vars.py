from models.robot_position import RobotPosition

class Vars:
    POS_1_1_UP = RobotPosition( #first line, first place, above the object, open gripper
        base_yaw=875,
        shoulder=280,
        elbow=234,
        wrist_pitch=821,
        wrist_roll=500,
        gripper=300
    )
    
    POS_1_1_DOWN = RobotPosition( #first line, first place, on the object, open gripper
        base_yaw=875,
        shoulder=220,
        elbow=140,
        wrist_pitch=800,
        wrist_roll=500,
        gripper=300
    )
    
    POS_1_1_CATCH = RobotPosition(#first line, first place, on the object, closed gripper
        base_yaw=875,
        shoulder=220,
        elbow=140,
        wrist_pitch=800,
        wrist_roll=500,
        gripper=530
    )

    POS_1_1_CATCH_UP = RobotPosition(#first line, first place, above the object, closed gripper
        base_yaw=875,
        shoulder=280,
        elbow=234,
        wrist_pitch=821,
        wrist_roll=500,
        gripper=530
    )
