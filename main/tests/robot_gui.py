import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from robot_control import RobotController
DEFAULT_FONT = ("Arial", 20)  # or any preferred font & size

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
        self.option_add("*Font", DEFAULT_FONT)  # sets default font for 
        self.geometry("800x600")  # width x height, adjust as needed
        self.controller = RobotController()
        self.spinboxes = []

        self.up_img = ImageTk.PhotoImage(Image.open("assets/up.png").resize((40, 40)))
        self.down_img = ImageTk.PhotoImage(Image.open("assets/down.png").resize((40, 40)))
        vcmd = (self.register(self.validate_input), "%P")

        for i, label in enumerate(AXIS_LABELS):
            tk.Label(self, text=f"{i+1}. {label}", anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")

            sb = tk.Spinbox(self, from_=0, to=1000, width=5)
            sb = tk.Spinbox(self, from_=0, to=1000, width=5)
            sb.delete(0, "end")
            sb.insert(0, "500")
            sb.grid(row=i, column=1, padx=5)  # только grid
            self.spinboxes.append(sb)

            start_button = tk.Button(self, text="START", width=8, command=lambda a=i: self.start_axis(a))
            start_button.grid(row=i, column=2, padx=5)

            down_button = tk.Button(self, image=self.down_img, command=lambda a=i: self.start_jog(a, -1))
            down_button.grid(row=i, column=3, padx=2)

            up_button = tk.Button(self, image=self.up_img, command=lambda a=i: self.start_jog(a, 1))
            up_button.grid(row=i, column=4, padx=2)


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