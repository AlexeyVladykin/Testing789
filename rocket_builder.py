import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass
from typing import List
import random


@dataclass
class RocketPart:
    name: str
    part_type: str
    position: int
    is_valid: bool


class RocketBuilderApp:

    NOSE_CONES = [
        RocketPart("Конический нос", "nose", 0, True),
        RocketPart("Острый нос", "nose", 0, True),
        RocketPart("Тупой нос", "nose", 0, True),
    ]

    BODY_SECTIONS = [
        RocketPart("Длинный корпус", "body", 1, True),
        RocketPart("Средний корпус", "body", 1, True),
        RocketPart("Короткий корпус", "body", 1, True),
        RocketPart("Топливный бак", "body", 2, True),
        RocketPart("Грузовой отсек", "body", 2, True),
    ]

    ENGINES = [
        RocketPart("Мощный двигатель", "engine", 3, True),
        RocketPart("Стандартный двигатель", "engine", 3, True),
        RocketPart("Экономичный двигатель", "engine", 3, True),
    ]

    FINS = [
        RocketPart("Большие стабилизаторы", "fin", 4, True),
        RocketPart("Средние стабилизаторы", "fin", 4, True),
        RocketPart("Малые стабилизаторы", "fin", 4, True),
    ]

    INVALID_PARTS = [
        RocketPart("Двигатель сверху", "engine", 0, False),
        RocketPart("Нос в середине", "nose", 1, False),
        RocketPart("Стабилизатор в центре", "fin", 2, False),
        RocketPart("Корпус снизу", "body", 3, False),
        RocketPart("Нос вместо двигателя", "nose", 3, False),
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Конструктор Ракет")
        self.root.geometry("900x700")
        self.rocket_positions = {
            0: {"name": "Нос", "type": "nose", "part": None},
            1: {"name": "Верхний корпус", "type": "body", "part": None},
            2: {"name": "Нижний корпус", "type": "body", "part": None},
            3: {"name": "Двигатель", "type": "engine", "part": None},
            4: {"name": "Стабилизаторы", "type": "fin", "part": None},
        }
        self.available_parts = self.NOSE_CONES + self.BODY_SECTIONS + self.ENGINES + self.FINS + self.INVALID_PARTS
        random.shuffle(self.available_parts)
        self._setup_ui()

    def _setup_ui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(left_frame, text="Ваша ракета", font=("Arial", 16, "bold")).pack(pady=5)

        self.canvas = tk.Canvas(left_frame, width=400, height=500, bg="lightblue")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        tk.Button(btn_frame, text="Проверить", command=self._check_rocket, bg="green", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Сброс", command=self._reset_rocket, bg="orange", width=10).pack(side=tk.LEFT, padx=5)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        tk.Label(right_frame, text="Части", font=("Arial", 16, "bold")).pack(pady=5)

        parts_container = tk.Frame(right_frame)
        parts_container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(parts_container, width=220)
        scrollbar = tk.Scrollbar(parts_container, orient="vertical", command=canvas.yview)
        self.parts_frame = tk.Frame(canvas)

        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.create_window((0, 0), window=self.parts_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", on_configure)
        self._populate_parts()

        self.status_label = tk.Label(left_frame, text="Соберите ракету!", font=("Arial", 11), fg="blue")
        self.status_label.pack(pady=5)

        self.root.after(500, self._show_instructions)

    def _populate_parts(self):
        for widget in self.parts_frame.winfo_children():
            widget.destroy()

        for part in self.available_parts:
            btn = tk.Button(self.parts_frame, text=part.name, command=lambda p=part: self._add_part(p), width=25, pady=3)
            btn.pack(pady=2, padx=5)

            colors = {"nose": "#FFB6C1", "body": "#ADD8E6", "engine": "#90EE90", "fin": "#DDA0DD"}
            if not part.is_valid:
                btn.configure(bg="#FF6347", fg="white")
            elif part.part_type in colors:
                btn.configure(bg=colors[part.part_type])

    def _add_part(self, part):
        for pos_id, pos_data in self.rocket_positions.items():
            if pos_data["part"] is None and pos_data["type"] == part.part_type:
                pos_data["part"] = part
                self._draw_rocket()
                return

        for pos_id, pos_data in self.rocket_positions.items():
            if pos_data["part"] is None:
                pos_data["part"] = part
                self._draw_rocket()
                self.status_label.configure(text=f"{part.name} - неправильно!", fg="red")
                return

        messagebox.showwarning("Внимание", "Все позиции заняты!")

    def _draw_rocket(self):
        self.canvas.delete("all")
        cx, y_off, h, w = 200, 50, 70, 80
        colors = {"nose": "#FF69B4", "body": "#4169E1", "engine": "#32CD32", "fin": "#9370DB"}

        for pos_id in sorted(self.rocket_positions.keys()):
            pos_data = self.rocket_positions[pos_id]
            y = y_off + pos_id * h

            if pos_data["part"] is None:
                self.canvas.create_rectangle(cx - w/2, y, cx + w/2, y + h - 10, fill="white", outline="gray", dash=(5, 5))
                self.canvas.create_text(cx, y + (h - 10)/2, text=pos_data["name"], font=("Arial", 8), fill="gray")
            else:
                part = pos_data["part"]
                color = colors.get(part.part_type, "#FF6347")
                if not part.is_valid or pos_data["type"] != part.part_type:
                    color = "#FF4500"

                if part.part_type == "nose":
                    self.canvas.create_polygon(cx - w/2, y + h - 10, cx, y, cx + w/2, y + h - 10, fill=color, outline="black")
                elif part.part_type == "body":
                    self.canvas.create_rectangle(cx - w/2, y, cx + w/2, y + h - 10, fill=color, outline="black")
                elif part.part_type == "engine":
                    self.canvas.create_rectangle(cx - w/2, y, cx + w/2, y + h - 10, fill=color, outline="black")
                    self.canvas.create_polygon(cx - 20, y + h - 10, cx, y + h + 10, cx + 20, y + h - 10, fill="orange", outline="red")
                elif part.part_type == "fin":
                    self.canvas.create_rectangle(cx - w/2 - 20, y + 20, cx + w/2 + 20, y + h - 30, fill=color, outline="black")
                    self.canvas.create_rectangle(cx - w/2, y, cx + w/2, y + h - 10, fill="#4169E1", outline="black")

                self.canvas.create_text(cx, y + (h - 10)/2, text=part.name, font=("Arial", 7, "bold"), fill="white")

        self.canvas.create_text(cx, y_off - 20, text="РАКЕТА", font=("Arial", 14, "bold"), fill="darkblue")

    def _check_rocket(self):
        if not all(pos["part"] for pos in self.rocket_positions.values()):
            messagebox.showwarning("Внимание", "Заполните все позиции!")
            return

        correct = sum(1 for pos in self.rocket_positions.values() if pos["part"] and pos["part"].is_valid and pos["type"] == pos["part"].part_type)
        total = len(self.rocket_positions)

        if correct == total:
            messagebox.showinfo("Победа!", "Ракета собрана правильно!")
            self.status_label.configure(text="Готово!", fg="green")
        else:
            messagebox.showwarning("Ошибки", f"Правильно: {correct}/{total}")
            self.status_label.configure(text=f"Ошибок: {total - correct}", fg="red")

    def _reset_rocket(self):
        for pos in self.rocket_positions.values():
            pos["part"] = None
        self._draw_rocket()
        self.status_label.configure(text="Соберите ракету!", fg="blue")

    def _show_instructions(self):
        messagebox.showinfo("Инструкция", "1. Выберите часть справа\n2. Она установится в ракету\n3. Порядок: Нос -> Корпус -> Двигатель -> Стабилизаторы\n\nКрасные части - неправильные!")


def main():
    root = tk.Tk()
    app = RocketBuilderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
