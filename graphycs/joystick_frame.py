import tkinter as tk

class JoystickFrame(tk.Frame):
    def init(self, master, robot_controller, **kwargs):
        super().init(master, **kwargs)
        self.robot = robot_controller

        self.canvas = tk.Canvas(self, width=200, height=200, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        # Треугольники: Вверх, Вниз, Влево, Вправо
        self.canvas.create_polygon(100, 20, 90, 40, 110, 40,
            fill="lightgreen", tags="up")
        self.canvas.create_polygon(100, 180, 90, 160, 110, 160,
            fill="lightgreen", tags="down")
        self.canvas.create_polygon(20, 100, 40, 90, 40, 110,
            fill="lightgreen", tags="left")
        self.canvas.create_polygon(180, 100, 160, 90, 160, 110,
            fill="lightgreen", tags="right")

        # Полукруги для вращения (по и против часовой)
        self.canvas.create_arc(60, 60, 140, 140, start=30, extent=120,
            style='arc', width=4, outline="blue", tags="rotate_cw")
        self.canvas.create_arc(60, 60, 140, 140, start=210, extent=120,
            style='arc', width=4, outline="red", tags="rotate_ccw")
        
        # Привязка событий
        self.canvas.tag_bind("up", "<Button-1>", lambda e: self.move(2, -10))  # Ось Y -
        self.canvas.tag_bind("down", "<Button-1>", lambda e: self.move(2, 10))  # Ось Y +
        self.canvas.tag_bind("left", "<Button-1>", lambda e: self.move(1, -10))  # Ось X -
        self.canvas.tag_bind("right", "<Button-1>", lambda e: self.move(1, 10))  # Ось X +
        self.canvas.tag_bind("rotate_cw", "<Button-1>", lambda e: self.move(6, 10))   # Ось поворота +
        self.canvas.tag_bind("rotate_ccw", "<Button-1>", lambda e: self.move(6, -10)) # Ось поворота -

    def move(self, axis_id, delta):
        self.robot.move_axis(axis_id, delta)

