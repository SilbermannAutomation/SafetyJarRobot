import tkinter as tk
from robot_control import RobotController

controller = RobotController()

def create_axis_control(root, axis_id):
    frame = tk.Frame(root)
    frame.pack(pady=5)

    label = tk.Label(frame, text=f"Axis {axis_id}")
    label.pack(side="left", padx=5)

    pulse_entry = tk.Entry(frame, width=6)
    pulse_entry.pack(side="left", padx=5)

    def run():
        val = pulse_entry.get()
        if val.isdigit():
            controller.move_servo(axis_id, int(val))

    run_button = tk.Button(frame, text="RUN", command=run)
    run_button.pack(side="left", padx=5)

root = tk.Tk()
root.title("Safety Jar Robot")

for i in range(1, 7):
    create_axis_control(root, i)

root.mainloop()
