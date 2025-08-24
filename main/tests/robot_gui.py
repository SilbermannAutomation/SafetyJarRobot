import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from robot_control import RobotController

AXIS_LABELS = ["Gripper", "Wrist", "Forearm", "Shoulder", "Lower Shoulder", "Base"]
DEFAULT_FONT = ("Arial", 14)

class RobotGUI(tk.Tk):
    def init(self):
        super().init()
        self.title("Robot GUI")
        self.geometry("800x600")
        self.option_add("*Font", DEFAULT_FONT)

        self.controller = RobotController()
        self.spinboxes = []
        self.selected_axis = tk.IntVar(value=0)

        self.up_img = ImageTk.PhotoImage(Image.open("assets/up.png").resize((40, 40)))
        self.down_img = ImageTk.PhotoImage(Image.open("assets/down.png").resize((40, 40)))

        for i, label in enumerate(AXIS_LABELS):
            tk.Label(self, text=f"{i+1}. {label}").grid(row=i, column=0, padx=10, pady=5, sticky="w")

            sb = tk.Spinbox(self, from_=0, to=1000, width=6)
            sb.delete(0, "end")
            sb.insert(0, "500")
            sb.grid(row=i, column=1, padx=5)
            self.spinboxes.append(sb)

            radio = tk.Radiobutton(self, variable=self.selected_axis, value=i)
            radio.grid(row=i, column=2, padx=5)
            tk.Button(self, text="START", width=10, command=self.start_selected_axis).grid(row=6, column=0, pady=20)
            tk.Button(self, image=self.down_img, command=lambda: self.start_jog(-1)).grid(row=6, column=1)
            tk.Button(self, image=self.up_img, command=lambda: self.start_jog(1)).grid(row=6, column=2)

        self.jogging = False

    def validate_input(self, P):
        return P.isdigit() and 0 <= int(P) <= 1000 or P == ""

    def start_selected_axis(self):
        axis = self.selected_axis.get()
        pulse = int(self.spinboxes[axis].get())
        self.controller.move_axis(axis + 1, pulse)

    def start_jog(self, direction):
        axis = self.selected_axis.get()
        current = int(self.spinboxes[axis].get())
        new_value = max(0, min(1000, current + direction * 10))
        self.spinboxes[axis].delete(0, "end")
        self.spinboxes[axis].insert(0, str(new_value))
        self.controller.move_axis(axis + 1, new_value)

if __name__ == "__main__":
    app = RobotGUI()
    app.mainloop()
