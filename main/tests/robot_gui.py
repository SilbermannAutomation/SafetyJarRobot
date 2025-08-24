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
    def __init__(self):
        super().__init__()
        self.title("Robot GUI")
        self.geometry("800x400")
        self.option_add("*Font", DEFAULT_FONT)

        self.bind("<F1>", lambda event: self.initialize_axes())

        self.controller = RobotController()
        self.spinboxes = []
        self.selected_axis = tk.IntVar(value=0)
        self.jogging = False

        self.up_img = ImageTk.PhotoImage(Image.open("assets/up.png").resize((40, 40)))
        self.down_img = ImageTk.PhotoImage(Image.open("assets/down.png").resize((40, 40)))

        vcmd = (self.register(self.validate_input), "%P")

        for i, label in enumerate(AXIS_LABELS):    
            tk.Label(self, text=f"{i+1}. {label}", anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")

            # sb = tk.Spinbox(self, from_=0, to=1000, width=5, validate="key", validatecommand=vcmd)
            sb = tk.Spinbox(self, from_=0, to=1000, width=5)
            sb.delete(0, "end")
            sb.insert(0, "500")
            sb.grid(row=i, column=1, padx=5)
            self.spinboxes.append(sb)

            radio = tk.Radiobutton(self, variable=self.selected_axis, value=i)
            radio.grid(row=i, column=2, padx=5)

        tk.Button(self, text="START", width=10, command=self.start_selected_axis).grid(row=3, column=3, pady=20)
        tk.Button(self, image=self.up_img, command=lambda: self.start_jog(self.selected_axis.get(), 1)).grid(row=3, column=4)
        tk.Button(self, image=self.down_img, command=lambda: self.start_jog(self.selected_axis.get(), -1)).grid(row=3, column=5)
        tk.Button(self, text="INITIALIZE", width=10, command=self.initialize_all_axes).grid(
                    row=0, column=3, pady=10)


    def validate_input(self, value_if_allowed):
        if value_if_allowed == "":
            return True
        try:
            val = int(value_if_allowed)
            return 0 <= val <= 1000
        except ValueError:
            return False


    def start_selected_axis(self):
        axis = self.selected_axis.get()
        value = int(self.spinboxes[axis].get())
        self.controller.move_axis(axis + 1, value)

    def initialize_all_axes(self):
        for i, sb in enumerate(self.spinboxes):
            sb.delete(0, "end")
            sb.insert(0, "500")
            self.controller.move_axis(i + 1, 500)


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

    def validate_input(self, value):
        return value.isdigit() and 0 <= int(value) <= 1000

if __name__ == "__main__":
    app = RobotGUI()
    app.mainloop()

    
