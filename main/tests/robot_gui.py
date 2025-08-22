import tkinter as tk

def run_axis(axis_num):
    servo_id = id_entries[axis_num].get()
    pulse = pulse_entries[axis_num].get()
    print(f"Running Axis {axis_num+1} | ID: {servo_id} | Pulse: {pulse}")
    # Тут можно вставить отправку команды на мотор

root = tk.Tk()
root.title("Robot Control Panel")

id_entries = []
pulse_entries = []

for i in range(6):
    tk.Label(root, text=f"Axis {i+1}").grid(row=i, column=0, padx=5, pady=5)

    id_entry = tk.Entry(root, width=5)
    id_entry.grid(row=i, column=1)
    id_entries.append(id_entry)

    pulse_entry = tk.Entry(root, width=8)
    pulse_entry.grid(row=i, column=2)
    pulse_entries.append(pulse_entry)

    run_button = tk.Button(root, text="RUN", command=lambda i=i: run_axis(i))
    run_button.grid(row=i, column=3, padx=10)

root.mainloop()
