robot_gui.py
import tkinter as tk
import ros_robot_controller_sdk as rrc

# Инициализация платы один раз
board = rrc.Board(device="/dev/serial0", baudrate=1_000_000, timeout=5)
board.enable_reception(True)

def move_servo(axis, pulse):
    board.bus_servoset_position(0.5, [[axis, int(pulse)]])

def create_axis_control(root, axis_num):
    frame = tk.Frame(root)
    frame.pack()

    label = tk.Label(frame, text=f"Axis {axis_num}")
    label.pack(side="left")

    pulse_entry = tk.Entry(frame)
    pulse_entry.pack(side="left")

    def run():
        pulse = pulse_entry.get()
        if pulse.isdigit():
            move_servo(axis_num, int(pulse))
    run_button = tk.Button(frame, text="RUN", command=run)
    run_button.pack(side="left")

root = tk.Tk()
root.title("Robot Control")

for i in range(1, 7):
    create_axis_control(root, i)

root.mainloop()
