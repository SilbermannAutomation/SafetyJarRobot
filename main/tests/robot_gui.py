import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from robot_control import RobotController

AXIS_LABELS = [
    "Gripper",     # Axis 1
    "Wrist",       # Axis 2
    "Forearm",     # Axis 3
    "Shoulder",    # Axis 4
    "Lower Shoulder",  # Axis 5
    "Base"         # Axis 6
]

class RobotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robot GUI")
        self.controller = RobotController()
        self.spinboxes = []

        self.up_img = ImageTk.PhotoImage(Image.open("assets/up.png").resize((20, 20)))
        self.down_img = ImageTk.PhotoImage(Image.open("assets/down.png").resize((20, 20)))
        vcmd = (self.register(self.validate_input), "%P")

        for i, label in enumerate(AXIS_LABELS):
            frame = tk.Frame(self)
            frame.pack(padx=10, pady=5)

            tk.Label(frame, text=f"{i+1}. {label}").pack(side="left", padx=5)

            sb = tk.Spinbox(
                frame, from_=0, to=1000, validate="key",
                validatecommand=vcmd, width=6
            )
            sb.delete(0, "end")
            sb.insert(0, "500")
            sb.pack(side="left", padx=5)
            self.spinboxes.append(sb)

            start_btn = tk.Button(frame, text="START", command=lambda axis=i+1: self.run_axis(axis))
            start_btn.pack(side="left", padx=5)

            down_btn = tk.Button(frame, image=self.down_img)
            down_btn.pack(side="left", padx=2)
            down_btn.bind("<ButtonPress>", lambda e, a=i+1: self.start_jog(a, -10))
            down_btn.bind("<ButtonRelease>", lambda e: self.stop_jog())

            up_btn = tk.Button(frame, image=self.up_img)
            up_btn.pack(side="left", padx=2)
            up_btn.bind("<ButtonPress>", lambda e, a=i+1: self.start_jog(a, 10))
            up_btn.bind("<ButtonRelease>", lambda e: self.stop_jog())

        self.jogging = False

    def validate_input(self, P):
        return P.isdigit() and 0 <= int(P) <= 1000 or P == ""

    def run_axis(self, axis_num):
        try:
            pulse = int(self.spinboxes[axis_num - 1].get())
            self.controller.move_axis(axis_num, pulse)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_jog(self, axis, delta):
        self.jogging = True
        self._jog(axis, delta)

    def _jog(self, axis, delta):
        if not self.jogging:
            return
        try:
            pulse = int(self.spinboxes[axis - 1].get()) + delta
            pulse = max(0, min(1000, pulse))
            self.spinboxes[axis - 1].delete(0, "end")
            self.spinboxes[axis - 1].insert(0, str(pulse))
            self.controller.move_axis(axis, pulse)
        except Exception as e:
            print(f"Jogging error: {e}")
            self.after(200, lambda: self._jog(axis, delta))

    def stop_jog(self):
        self.jogging = False

if __name__=="__main__":
    app = RobotGUI()
    app.mainloop()