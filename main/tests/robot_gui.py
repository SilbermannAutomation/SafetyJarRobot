import tkinter as tk
from robot_control import RobotController
from joystick_frame import JoystickFrame

AXES = 6  # число осей робота

controller = RobotController()
root = tk.Tk()
root.title("Robot GUI")

joystick = JoystickFrame(root, controller)
joystick.pack(pady=10)


def validate_input(P):
    return (P.isdigit() and 0 <= int(P) <= 1000) or P == ""


def run_axis(axis_num, spinboxes):
    pulse = int(spinboxes[axis_num - 1].get())
    controller.move_axis(axis_num, pulse)


def refresh_positions():
    """Обновляем все Spinbox значениями с робота"""
    for i, sb in enumerate(spinboxes, start=1):
        pos = controller.get_axis_position(i)
        if pos is not None:
            sb.delete(0, "end")
            sb.insert(0, str(pos))


vcmd = (root.register(validate_input), "%P")
spinboxes = []

# создаём панель управления для каждой оси
for i in range(AXES):
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=5)

    tk.Label(frame, text=f"Axis {i + 1}").pack(side="left", padx=5)

    current_pos = controller.get_axis_position(i + 1)
    if current_pos is None:
        current_pos = 500

    sb = tk.Spinbox(
        frame,
        from_=0,
        to=1000,
        validate="key",
        validatecommand=vcmd,
        width=6
    )
    sb.delete(0, "end")
    sb.insert(0, str(current_pos))
    sb.pack(side="left", padx=5)
    spinboxes.append(sb)

    btn = tk.Button(
        frame,
        text="RUN",
        command=lambda axis=i + 1: run_axis(axis, spinboxes)
    )
    btn.pack(side="left", padx=5)

# кнопка обновления позиций
refresh_btn = tk.Button(root, text="Refresh positions", command=refresh_positions)
refresh_btn.pack(pady=10)


# ===== ДОБАВЛЕННЫЕ КНОПКИ =====

control_frame = tk.Frame(root)
control_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Z-axis ▲ ▼ (верхний левый угол)
z_frame = tk.Frame(control_frame)
z_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

tk.Button(z_frame, text="▲", fg="green", command=lambda: controller.move_axis(3, 600)).pack()
tk.Button(z_frame, text="▼", fg="green", command=lambda: controller.move_axis(3, 400)).pack()

# Wrist ↻ ↺ (верхний правый угол)
wrist_frame = tk.Frame(control_frame)
wrist_frame.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

tk.Button(wrist_frame, text="↻", fg="green", command=lambda: controller.move_axis(2, 600)).pack()
tk.Button(wrist_frame, text="↺", fg="green", command=lambda: controller.move_axis(2, 400)).pack()

# Gripper ⏶ ⏷ (нижний правый угол)
grip_frame = tk.Frame(control_frame)
grip_frame.grid(row=1, column=1, sticky="se", padx=10, pady=10)

tk.Button(grip_frame, text="⏶", fg="green", command=lambda: controller.move_axis(6, 600)).pack()
tk.Button(grip_frame, text="⏷", fg="green", command=lambda: controller.move_axis(6, 400)).pack()

root.mainloop()