import tkinter as tk

class JoystickFrame(tk.Frame):
    def __init__(self, master, robot_controller, **kwargs):
        super().__init__(master, **kwargs)
        self.robot = robot_controller

        self.canvas = tk.Canvas(self, width=220, height=220, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0)

        # ===== СТАРЫЕ КНОПКИ =====
        # Треугольники: Вверх, Вниз, Влево, Вправо
        self.canvas.create_polygon(110, 20, 100, 40, 120, 40,
            fill="green", tags="up")
        self.canvas.create_polygon(110, 200, 100, 180, 120, 180,
            fill="green", tags="down")
        self.canvas.create_polygon(20, 110, 40, 100, 40, 120,
            fill="green", tags="left")
        self.canvas.create_polygon(200, 110, 180, 100, 180, 120,
            fill="green", tags="right")

        # Большие дуги в центре
        self.canvas.create_arc(70, 70, 150, 150, start=30, extent=120,
            style='arc', width=4, outline="blue", tags="rotate_cw")
        self.canvas.create_arc(70, 70, 150, 150, start=210, extent=120,
            style='arc', width=4, outline="red", tags="rotate_ccw")

        # ===== НОВЫЕ КНОПКИ =====
        # Z-axis ▲ ▼ (верхний левый угол)
        self.canvas.create_polygon(40, 20, 30, 40, 50, 40,
            fill="green", tags="z_up")
        self.canvas.create_polygon(40, 60, 30, 40, 50, 50,
            fill="green", tags="z_down")

        # Wrist ↻ ↺ (верхний правый угол, маленькие дуги)
        self.canvas.create_arc(160, 20, 200, 60, start=30, extent=120,
            style='arc', width=3, outline="green", tags="wrist_cw")
        self.canvas.create_arc(160, 20, 200, 60, start=210, extent=120,
            style='arc', width=3, outline="green", tags="wrist_ccw")

        # Gripper ⏶ ⏷ (нижний правый угол, два треугольника)
        self.canvas.create_polygon(180, 180, 170, 200, 190, 200,
            fill="green", tags="grip_open")
        self.canvas.create_polygon(180, 220, 170, 200, 190, 200,
            fill="green", tags="grip_close")

        # ===== ПРИВЯЗКА СОБЫТИЙ =====
        # XY movement
        self.canvas.tag_bind("up", "<Button-1>", lambda e: self.move(2, -10))
        self.canvas.tag_bind("down", "<Button-1>", lambda e: self.move(2, 10))
        self.canvas.tag_bind("left", "<Button-1>", lambda e: self.move(1, -10))
        self.canvas.tag_bind("right", "<Button-1>", lambda e: self.move(1, 10))
        # rotation (axis 6)
        self.canvas.tag_bind("rotate_cw", "<Button-1>", lambda e: self.move(6, 10))
        self.canvas.tag_bind("rotate_ccw", "<Button-1>", lambda e: self.move(6, -10))
        # Z-axis
        self.canvas.tag_bind("z_up", "<Button-1>", lambda e: self.move(3, 10))
        self.canvas.tag_bind("z_down", "<Button-1>", lambda e: self.move(3, -10))
        # wrist (axis 2)
        self.canvas.tag_bind("wrist_cw", "<Button-1>", lambda e: self.move(2, 10))
        self.canvas.tag_bind("wrist_ccw", "<Button-1>", lambda e: self.move(2, -10))
        # gripper (axis 5 or 6, допустим 5)
        self.canvas.tag_bind("grip_open", "<Button-1>", lambda e: self.move(5, 10))
        self.canvas.tag_bind("grip_close", "<Button-1>", lambda e: self.move(5, -10))

    def move(self, axis_id, delta):
        """Пошаговое смещение от текущего положения"""
        current = self.robot.get_axis_position(axis_id) or 500
        new_pos = current + delta
        self.robot.move_axis(axis_id, new_pos)