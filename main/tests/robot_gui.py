import tkinter as tk
from PIL import Image, ImageTk
from robot_control import RobotController

AXIS_NAMES = ["Gripper", "Wrist", "Forearm", "Shoulder", "Lower Shoulder", "Base"]

controller = RobotController()
root = tk.Tk()
root.title("Robot GUI")

def validate_input(P):
    return P.isdigit() and 0 <= int(P) <= 1000 or P == ""

def run_axis(axis_num, spinboxes):
    pulse = int(spinboxes[axis_num - 1].get())
    controller.move_axis(axis_num, pulse)

def move_delta(axis_num, delta, spinboxes):
    current = int(spinboxes[axis_num - 1].get())
    new_val = max(0, min(1000, current + delta))
    spinboxes[axis_num - 1].delete(0, "end")
    spinboxes[axis_num - 1].insert(0, str(new_val))
    controller.move_axis(axis_num, new_val)
# Load images
up_img = ImageTk.PhotoImage(Image.open("assets/up.png").resize((20, 20)))
down_img = ImageTk.PhotoImage(Image.open("assets/down.png").resize((20, 20)))

vcmd = (root.register(validate_input), "%P")
spinboxes = []

for i, name in enumerate(AXIS_NAMES):
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=5)

    tk.Label(frame, text=f"{i + 1}. {name}", width=15, anchor="w").pack(side="left")
    sb = tk.Spinbox(frame, from_=0, to=1000, validate="key", validatecommand=vcmd, width=6)
    sb.delete(0, "end")
    sb.insert(0, "100")
    sb.pack(side="left", padx=5)
    spinboxes.append(sb)

    tk.Button(frame, image=down_img, command=lambda axis=i+1: move_delta(axis, -10, spinboxes)).pack(side="left", padx=2)
    tk.Button(frame, image=up_img, command=lambda axis=i+1: move_delta(axis, 10, spinboxes)).pack(side="left", padx=2)

root.mainloop()
