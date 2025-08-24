import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from robot_control import RobotController

AXIS_LABELS = [
    "Gripper",        # Axis 1
    "Wrist",          # Axis 2
    "Forearm",        # Axis 3
    "Shoulder",       # Axis 4
    "Lower Shoulder", # Axis 5
    "Base"            # Axis 6
]

DEFAULT_FONT = ("Arial", 14)

class RobotGUI(tk.Tk):
    def init(self):
        super().init()
        self.title("Robot GUI")
        self.geometry("800x400")
        self.option_add("*Font", DEFAULT_FONT)

        self.controller = RobotController()
        self.spinboxes = []
        self.selected_axis = tk.IntVar(value=0)
        self.jogging = False

        self.up_img = ImageTk.PhotoImage(Image.open("assets/up.png").resize((40, 40)))
        self.down_img = ImageTk.PhotoImage(Image.open("assets/down.png").resize((40, 40)))

        vcmd = (self.register(self.validate_input), "%P")

        for i, label in enumerate(AXIS_LABELS):
            def start_selected_axis(self):
                axis = self.selected_axis.get()
                value = int(self.spinboxes[axis].get())
                self.controller.move_axis(axis + 1, value)

    def start_jog(self, axis, delta):
        if self.jogging:
            return
        self.jogging = True
        self._jog(axis, delta)

    def _jog(self, axis, delta):
        if not self.jogging:
            return
        try:
            current = int(self.spinboxes[axis].get())
            new = max(0, min(1000, current + delta * 5))
            self.spinboxes[axis].delete(0, "end")
            self.spinboxes[axis].insert(0, str(new))
            self.controller.move_axis(axis + 1, new)
            self.after(200, lambda: self._jog(axis, delta))
        except Exception as e:
            print(f"Jogging error: {e}")

    def stop_jog(self):
        self.jogging = False


if __name__ == "__main__":
    app = RobotGUI()
    app.mainloop()
