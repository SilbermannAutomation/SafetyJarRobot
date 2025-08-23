import tkinter as tk
from robot_control import RobotController
from joystick_frame import JoystickFrame

controller = RobotController()
root = tk.Tk()
joystick = JoystickFrame(root, controller)
joystick.pack(pady=10)


def validate_input(P):
    return P.isdigit() and 0 <= int(P) <= 1000 or P == ""

def run_axis(axis_num, spinboxes):
    pulse = int(spinboxes[axis_num - 1].get())
    controller.move_axis(axis_num, pulse)

root = tk.Tk()
root.title("Robot GUI")

vcmd = (root.register(validate_input), "%P")
spinboxes = []

for i in range(6):
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=5)

    tk.Label(frame, text=f"Axis {i + 1}").pack(side="left", padx=5)

    sb = tk.Spinbox(
 frame,
        from_=0,
        to=1000,
        validate="key",
        validatecommand=vcmd,
        width=6
    )
    sb.delete(0, "end")
    sb.insert(0, "100")
    sb.pack(side="left", padx=5)
    spinboxes.append(sb)

    btn = tk.Button(
        frame,
        text="RUN",
        command=lambda axis=i + 1: run_axis(axis, spinboxes)
    )
    btn.pack(side="left", padx=5)

root.mainloop()
