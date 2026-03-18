import tkinter as tk
from tkinter import messagebox


class RocketBuilderApp:
    """Конструктор ракет с визуальной моделью."""

    COLORS = {
        "bg": "#1a1a2e",
        "panel": "#16213e",
        "text": "#e8e8e8",
        "muted": "#8892b0",
        "accent": "#4ecca3",
        "nose": "#ff9a5a",
        "body": "#5dade2",
        "engine": "#58d68d",
        "fin": "#c39bd3",
        "slot_empty": "#2c3e50",
        "slot_border": "#34495e",
        "error": "#e74c3c",
    }

    PARTS = {
        "nose": [
            "Острый нос",
            "Конический нос",
            "Тупой нос",
            "Сферический нос",
            "Усиленный нос",
        ],
        "body": [
            "Длинный корпус",
            "Средний корпус",
            "Короткий корпус",
            "Топливный бак",
            "Грузовой отсек",
        ],
        "engine": [
            "Мощный двигатель",
            "Стандартный двигатель",
            "Экономичный",
            "Ионный двигатель",
            "Турбодвигатель",
        ],
        "fin": [
            "Большие стабилизаторы",
            "Средние стабилизаторы",
            "Малые стабилизаторы",
            "Треугольные стабилизаторы",
            "Складные стабилизаторы",
        ],
    }

    SLOT_ORDER = ["nose", "body", "body", "engine", "fin"]
    SLOT_NAMES = {
        0: "Нос",
        1: "Корпус 1",
        2: "Корпус 2",
        3: "Двигатель",
        4: "Стабилизаторы",
    }

    # Визуальные параметры для отрисовки
    NOSE_SHAPES = {
        "Острый нос": "sharp",
        "Конический нос": "cone",
        "Тупой нос": "flat",
        "Сферический нос": "round",
        "Усиленный нос": "thick",
    }

    BODY_HEIGHTS = {
        "Длинный корпус": 70,
        "Средний корпус": 55,
        "Короткий корпус": 40,
        "Топливный бак": 50,
        "Грузовой отсек": 55,
    }

    ENGINE_SHAPES = {
        "Мощный двигатель": "large",
        "Стандартный двигатель": "medium",
        "Экономичный": "small",
        "Ионный двигатель": "ion",
        "Турбодвигатель": "turbo",
    }

    FIN_SHAPES = {
        "Большие стабилизаторы": "large",
        "Средние стабилизаторы": "medium",
        "Малые стабилизаторы": "small",
        "Треугольные стабилизаторы": "triangle",
        "Складные стабилизаторы": "folded",
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Конструктор ракеты")
        self.root.geometry("950x700")
        self.root.configure(bg=self.COLORS["bg"])

        self.slots = {
            i: {"type": slot_type, "part": None}
            for i, slot_type in enumerate(self.SLOT_ORDER)
        }

        self.selected_part = None
        self.selected_slot = None

        self._setup_ui()
        self._update_ui()

    def _setup_ui(self):
        # Заголовок
        header = tk.Frame(self.root, bg=self.COLORS["panel"], pady=12)
        header.pack(fill=tk.X, padx=20, pady=(15, 10))

        tk.Label(
            header,
            text="🚀 Конструктор ракеты",
            bg=self.COLORS["panel"],
            fg=self.COLORS["text"],
            font=("Arial", 16, "bold"),
        ).pack()

        tk.Label(
            header,
            text="Выбери деталь → выбери слот на ракете → примени",
            bg=self.COLORS["panel"],
            fg=self.COLORS["muted"],
            font=("Arial", 10),
        ).pack()

        # Основная часть
        main = tk.Frame(self.root, bg=self.COLORS["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Левая панель — визуальная ракета
        left = tk.Frame(main, bg=self.COLORS["panel"], padx=15, pady=15)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(
            left,
            text="Модель ракеты",
            bg=self.COLORS["panel"],
            fg=self.COLORS["text"],
            font=("Arial", 13, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        # Канвас для отрисовки ракеты
        self.rocket_canvas = tk.Canvas(
            left,
            bg=self.COLORS["slot_empty"],
            highlightthickness=0,
        )
        self.rocket_canvas.pack(fill=tk.BOTH, expand=True)
        self.rocket_canvas.bind("<Configure>", self._draw_rocket)

        # Кнопки управления под ракетой
        controls = tk.Frame(left, bg=self.COLORS["panel"])
        controls.pack(fill=tk.X, pady=(10, 0))

        tk.Button(
            controls,
            text="Сбросить ракету",
            command=self._reset,
            bg=self.COLORS["slot_border"],
            fg=self.COLORS["text"],
            font=("Arial", 10),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(
            controls,
            text="Проверить сборку",
            command=self._check,
            bg=self.COLORS["accent"],
            fg=self.COLORS["bg"],
            font=("Arial", 10, "bold"),
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls,
            text="Снять деталь",
            command=self._remove_selected,
            bg=self.COLORS["slot_border"],
            fg=self.COLORS["text"],
            font=("Arial", 10),
            cursor="hand2",
        ).pack(side=tk.LEFT)

        # Правая панель — каталог деталей
        right = tk.Frame(main, bg=self.COLORS["panel"], padx=15, pady=15)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(
            right,
            text="Каталог деталей",
            bg=self.COLORS["panel"],
            fg=self.COLORS["text"],
            font=("Arial", 13, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        # Контейнер для скролла
        catalog_container = tk.Frame(right, bg=self.COLORS["panel"])
        catalog_container.pack(fill=tk.BOTH, expand=True)

        self.parts_canvas = tk.Canvas(
            catalog_container,
            bg=self.COLORS["panel"],
            highlightthickness=0,
        )
        scrollbar = tk.Scrollbar(
            catalog_container,
            orient="vertical",
            command=self.parts_canvas.yview,
            bg=self.COLORS["slot_border"],
        )
        self.parts_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.parts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.parts_frame = tk.Frame(self.parts_canvas, bg=self.COLORS["panel"])
        self.parts_canvas.create_window((0, 0), window=self.parts_frame, anchor="nw")

        self.parts_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self._populate_catalog()
        self.parts_frame.bind("<Configure>", self._update_scrollregion)

        # Статус
        self.status_label = tk.Label(
            self.root,
            text="Выберите деталь из каталога справа",
            bg=self.COLORS["bg"],
            fg=self.COLORS["muted"],
            font=("Arial", 10),
        )
        self.status_label.pack(pady=(8, 15))

    def _populate_catalog(self):
        """Заполняет каталог деталей — компактно."""
        for widget in self.parts_frame.winfo_children():
            widget.destroy()

        for part_type, part_names in self.PARTS.items():
            color = self.COLORS[part_type]

            # Заголовок типа
            type_header = tk.Label(
                self.parts_frame,
                text=f"▲ {part_type.upper()}",
                bg=self.COLORS["panel"],
                fg=color,
                font=("Arial", 9, "bold"),
                anchor="w",
                pady=3,
            )
            type_header.pack(fill=tk.X, pady=(6, 2))

            # Детали
            for part_name in part_names:
                btn = tk.Button(
                    self.parts_frame,
                    text=part_name,
                    command=lambda t=part_type, p=part_name: self._select_part(t, p),
                    bg=self.COLORS["panel"],
                    fg=self.COLORS["text"],
                    font=("Arial", 9),
                    cursor="hand2",
                    anchor="w",
                    padx=8,
                    pady=3,
                    activebackground=self.COLORS["slot_border"],
                )
                btn.pack(fill=tk.X, pady=0)

    def _select_part(self, part_type, part_name):
        """Выбирает деталь из каталога."""
        self.selected_part = {"type": part_type, "name": part_name}
        self.status_label.configure(
            text=f"✓ Выбрано: {part_name} — кликните на слот ракеты для установки"
        )
        self._highlight_selected_part()

    def _highlight_selected_part(self):
        """Подсвечивает выбранную деталь в каталоге."""
        for widget in self.parts_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=self.COLORS["panel"])

        # Найти и подсветить выбранную кнопку
        for part_type, part_names in self.PARTS.items():
            if self.selected_part and part_type == self.selected_part["type"]:
                for i, name in enumerate(part_names):
                    if name == self.selected_part["name"]:
                        # Подсветка будет при следующей отрисовке
                        pass

    def _draw_rocket(self, event=None):
        """Рисует визуальную модель ракеты."""
        self.rocket_canvas.delete("all")

        width = max(self.rocket_canvas.winfo_width(), 300)
        height = max(self.rocket_canvas.winfo_height(), 450)

        center_x = width // 2
        y_start = 40
        segment_width = 80

        # Рисуем каждый слот
        y_current = y_start
        slot_heights = []

        for slot_idx in range(5):
            slot = self.slots[slot_idx]
            slot_type = slot["type"]
            part = slot["part"]

            # Определяем высоту сегмента
            if part and part["type"] == "body":
                seg_height = self.BODY_HEIGHTS.get(part["name"], 55)
            else:
                seg_height = 50

            slot_heights.append(seg_height)

            # Координаты
            y_top = y_current
            y_bottom = y_current + seg_height

            # Проверка правильности
            is_correct = part and part["type"] == slot_type
            is_selected = self.selected_slot == slot_idx

            # Рисуем сегмент
            self._draw_segment(
                slot_idx,
                slot_type,
                part,
                center_x,
                y_top,
                y_bottom,
                segment_width,
                is_correct,
                is_selected,
            )

            y_current = y_bottom

        # Рисуем базу под ракетой
        base_y = y_current + 10
        self.rocket_canvas.create_rectangle(
            center_x - 50,
            base_y,
            center_x + 50,
            base_y + 12,
            fill="#34495e",
            outline="#2c3e50",
        )

        # Подпись
        self.rocket_canvas.create_text(
            center_x,
            base_y + 28,
            text="Кликните на сегмент для выбора слота",
            fill=self.COLORS["muted"],
            font=("Arial", 9),
        )

    def _draw_segment(
        self,
        slot_idx,
        slot_type,
        part,
        center_x,
        y_top,
        y_bottom,
        width,
        is_correct,
        is_selected,
    ):
        """Рисует один сегмент ракеты."""
        left = center_x - width // 2
        right = center_x + width // 2

        # Цвет обводки
        if is_selected:
            border_color = self.COLORS["accent"]
            border_width = 3
        elif part and not is_correct:
            border_color = self.COLORS["error"]
            border_width = 2
        elif part:
            border_color = self.COLORS[slot_type]
            border_width = 2
        else:
            border_color = self.COLORS["slot_border"]
            border_width = 1

        # Рисуем в зависимости от типа
        if slot_type == "nose":
            self._draw_nose(center_x, y_top, y_bottom, part, border_color, border_width)
        elif slot_type == "body":
            self._draw_body(center_x, y_top, y_bottom, part, border_color, border_width)
        elif slot_type == "engine":
            self._draw_engine(
                center_x, y_top, y_bottom, part, border_color, border_width
            )
        elif slot_type == "fin":
            self._draw_fin(center_x, y_top, y_bottom, part, border_color, border_width)

        # Подпись слота
        label_y = (y_top + y_bottom) // 2
        self.rocket_canvas.create_text(
            left - 10,
            label_y,
            text=self.SLOT_NAMES[slot_idx],
            anchor="e",
            fill=self.COLORS["muted"],
            font=("Arial", 9),
        )

        # Клик-зона (невидимая)
        self.rocket_canvas.create_rectangle(
            left - 60,
            y_top,
            right + 60,
            y_bottom,
            tags=f"slot_{slot_idx}",
            outline="",
        )
        self.rocket_canvas.tag_bind(
            f"slot_{slot_idx}",
            "<Button-1>",
            lambda e, idx=slot_idx: self._select_slot(idx),
        )

    def _draw_nose(self, cx, y_top, y_bottom, part, border_color, border_width):
        """Рисует носовой обтекатель."""
        left = cx - 40
        right = cx + 40
        bottom = y_bottom

        if part:
            shape = self.NOSE_SHAPES.get(part["name"], "cone")
            color = self.COLORS["nose"]

            if shape == "sharp":
                # Острый треугольник
                self.rocket_canvas.create_polygon(
                    left,
                    bottom,
                    cx,
                    y_top - 15,
                    right,
                    bottom,
                    fill=color,
                    outline=border_color,
                    width=border_width,
                )
            elif shape == "cone":
                # Конический
                self.rocket_canvas.create_polygon(
                    left,
                    bottom,
                    cx,
                    y_top,
                    right,
                    bottom,
                    fill=color,
                    outline=border_color,
                    width=border_width,
                )
            elif shape == "flat":
                # Тупой
                self.rocket_canvas.create_rectangle(
                    left,
                    y_top,
                    right,
                    bottom,
                    fill=color,
                    outline=border_color,
                    width=border_width,
                )
            elif shape == "round":
                # Сферический
                self.rocket_canvas.create_arc(
                    left,
                    y_top - 20,
                    right,
                    bottom,
                    start=0,
                    extent=180,
                    fill=color,
                    outline=border_color,
                    width=border_width,
                )
            elif shape == "thick":
                # Усиленный
                self.rocket_canvas.create_polygon(
                    left - 5,
                    bottom,
                    cx,
                    y_top + 5,
                    right + 5,
                    bottom,
                    fill=color,
                    outline=border_color,
                    width=border_width,
                )
        else:
            # Пустой слот
            self.rocket_canvas.create_polygon(
                left,
                bottom,
                cx,
                y_top,
                right,
                bottom,
                fill=self.COLORS["slot_empty"],
                outline=border_color,
                width=border_width,
                dash=(5, 3),
            )

    def _draw_body(self, cx, y_top, y_bottom, part, border_color, border_width):
        """Рисует сегмент корпуса."""
        left = cx - 40
        right = cx + 40

        if part:
            color = self.COLORS["body"]
            self.rocket_canvas.create_rectangle(
                left,
                y_top,
                right,
                y_bottom,
                fill=color,
                outline=border_color,
                width=border_width,
            )

            # Детали корпуса
            if part["name"] == "Топливный бак":
                # Полоски бака
                for i in range(3):
                    y_line = y_top + (y_bottom - y_top) * (i + 1) / 4
                    self.rocket_canvas.create_line(
                        left + 5,
                        y_line,
                        right - 5,
                        y_line,
                        fill="#2c3e50",
                        width=2,
                    )
            elif part["name"] == "Грузовой отсек":
                # Квадратные панели
                panel_size = 15
                self.rocket_canvas.create_rectangle(
                    cx - panel_size,
                    y_top + 10,
                    cx + panel_size,
                    y_top + 10 + panel_size,
                    fill="#34495e",
                    outline="#2c3e50",
                )
        else:
            # Пустой слот
            self.rocket_canvas.create_rectangle(
                left,
                y_top,
                right,
                y_bottom,
                fill=self.COLORS["slot_empty"],
                outline=border_color,
                width=border_width,
                dash=(5, 3),
            )

    def _draw_engine(self, cx, y_top, y_bottom, part, border_color, border_width):
        """Рисует двигатель."""
        left = cx - 40
        right = cx + 40

        if part:
            shape = self.ENGINE_SHAPES.get(part["name"], "medium")
            color = self.COLORS["engine"]

            # Основная часть
            self.rocket_canvas.create_rectangle(
                left,
                y_top,
                right,
                y_bottom - 10,
                fill=color,
                outline=border_color,
                width=border_width,
            )

            # Сопло
            nozzle_y = y_bottom
            if shape == "large":
                self.rocket_canvas.create_polygon(
                    cx - 25,
                    y_bottom - 10,
                    cx - 15,
                    nozzle_y + 15,
                    cx + 15,
                    nozzle_y + 15,
                    cx + 25,
                    y_bottom - 10,
                    fill="#e74c3c",
                    outline="#c0392b",
                    width=2,
                )
                # Огонь
                self.rocket_canvas.create_polygon(
                    cx - 10,
                    nozzle_y + 5,
                    cx,
                    nozzle_y + 25,
                    cx + 10,
                    nozzle_y + 5,
                    fill="#f39c12",
                    outline="#e67e22",
                )
            elif shape == "medium":
                self.rocket_canvas.create_polygon(
                    cx - 20,
                    y_bottom - 10,
                    cx - 12,
                    nozzle_y + 10,
                    cx + 12,
                    nozzle_y + 10,
                    cx + 20,
                    y_bottom - 10,
                    fill="#e74c3c",
                    outline="#c0392b",
                    width=2,
                )
            elif shape == "small":
                self.rocket_canvas.create_polygon(
                    cx - 15,
                    y_bottom - 10,
                    cx - 8,
                    nozzle_y + 5,
                    cx + 8,
                    nozzle_y + 5,
                    cx + 15,
                    y_bottom - 10,
                    fill="#e74c3c",
                    outline="#c0392b",
                    width=2,
                )
            elif shape == "ion":
                # Ионный двигатель (синее свечение)
                self.rocket_canvas.create_oval(
                    cx - 20,
                    y_bottom - 5,
                    cx + 20,
                    nozzle_y + 10,
                    fill="#3498db",
                    outline="#2980b9",
                )
            elif shape == "turbo":
                # Турбо (двойное сопло)
                self.rocket_canvas.create_polygon(
                    cx - 25,
                    y_bottom - 10,
                    cx - 18,
                    nozzle_y + 12,
                    cx - 8,
                    nozzle_y + 12,
                    cx - 5,
                    y_bottom - 10,
                    fill="#e74c3c",
                    outline="#c0392b",
                    width=2,
                )
                self.rocket_canvas.create_polygon(
                    cx + 5,
                    y_bottom - 10,
                    cx + 8,
                    nozzle_y + 12,
                    cx + 18,
                    nozzle_y + 12,
                    cx + 25,
                    y_bottom - 10,
                    fill="#e74c3c",
                    outline="#c0392b",
                    width=2,
                )
        else:
            # Пустой слот
            self.rocket_canvas.create_rectangle(
                left,
                y_top,
                right,
                y_bottom,
                fill=self.COLORS["slot_empty"],
                outline=border_color,
                width=border_width,
                dash=(5, 3),
            )

    def _draw_fin(self, cx, y_top, y_bottom, part, border_color, border_width):
        """Рисует стабилизаторы."""
        left = cx - 40
        right = cx + 40
        fin_height = y_bottom - y_top

        if part:
            shape = self.FIN_SHAPES.get(part["name"], "medium")
            color = self.COLORS["fin"]
            core_color = self.COLORS["body"]

            # Центральный корпус
            self.rocket_canvas.create_rectangle(
                cx - 20,
                y_top,
                cx + 20,
                y_bottom,
                fill=core_color,
                outline=border_color,
                width=border_width,
            )

            # Стабилизаторы по бокам
            if shape == "large":
                # Левый
                self.rocket_canvas.create_polygon(
                    cx - 20,
                    y_top + 10,
                    cx - 55,
                    y_bottom,
                    cx - 20,
                    y_bottom,
                    fill=color,
                    outline=border_color,
                    width=2,
                )
                # Правый
                self.rocket_canvas.create_polygon(
                    cx + 20,
                    y_top + 10,
                    cx + 55,
                    y_bottom,
                    cx + 20,
                    y_bottom,
                    fill=color,
                    outline=border_color,
                    width=2,
                )
            elif shape == "medium":
                self.rocket_canvas.create_polygon(
                    cx - 20,
                    y_top + 15,
                    cx - 45,
                    y_bottom,
                    cx - 20,
                    y_bottom,
                    fill=color,
                    outline=border_color,
                    width=2,
                )
                self.rocket_canvas.create_polygon(
                    cx + 20,
                    y_top + 15,
                    cx + 45,
                    y_bottom,
                    cx + 20,
                    y_bottom,
                    fill=color,
                    outline=border_color,
                    width=2,
                )
            elif shape == "small":
                self.rocket_canvas.create_polygon(
                    cx - 20,
                    y_top + 20,
                    cx - 35,
                    y_bottom,
                    cx - 20,
                    y_bottom,
                    fill=color,
                    outline=border_color,
                    width=2,
                )
                self.rocket_canvas.create_polygon(
                    cx + 20,
                    y_top + 20,
                    cx + 35,
                    y_bottom,
                    cx + 20,
                    y_bottom,
                    fill=color,
                    outline=border_color,
                    width=2,
                )
            elif shape == "triangle":
                # Треугольные
                self.rocket_canvas.create_polygon(
                    cx - 20,
                    y_top + 5,
                    cx - 50,
                    y_top + 35,
                    cx - 20,
                    y_bottom,
                    fill=color,
                    outline=border_color,
                    width=2,
                )
                self.rocket_canvas.create_polygon(
                    cx + 20,
                    y_top + 5,
                    cx + 50,
                    y_top + 35,
                    cx + 20,
                    y_bottom,
                    fill=color,
                    outline=border_color,
                    width=2,
                )
            elif shape == "folded":
                # Складные (прижаты к корпусу)
                self.rocket_canvas.create_rectangle(
                    cx - 28,
                    y_top + 10,
                    cx - 20,
                    y_bottom - 10,
                    fill=color,
                    outline=border_color,
                    width=2,
                )
                self.rocket_canvas.create_rectangle(
                    cx + 20,
                    y_top + 10,
                    cx + 28,
                    y_bottom - 10,
                    fill=color,
                    outline=border_color,
                    width=2,
                )
        else:
            # Пустой слот
            self.rocket_canvas.create_rectangle(
                left,
                y_top,
                right,
                y_bottom,
                fill=self.COLORS["slot_empty"],
                outline=border_color,
                width=border_width,
                dash=(5, 3),
            )

    def _select_slot(self, slot_idx):
        """Выбирает слот на ракете."""
        self.selected_slot = slot_idx
        slot = self.slots[slot_idx]

        if slot["part"]:
            self.status_label.configure(
                text=f"Слот {self.SLOT_NAMES[slot_idx]}: {slot['part']['name']}. "
                f"Кликните 'Снять деталь' или выберите новую деталь"
            )
        else:
            self.status_label.configure(
                text=f"Слот {self.SLOT_NAMES[slot_idx]} пуст. "
                f"Выберите деталь и кликните ещё раз для установки"
            )

        # Применяем деталь если выбрана
        if self.selected_part:
            self._apply_part_to_slot(slot_idx)

        self._draw_rocket()

    def _apply_part_to_slot(self, slot_idx):
        """Применяет выбранную деталь к слоту."""
        slot = self.slots[slot_idx]
        slot["part"] = self.selected_part.copy()
        self.status_label.configure(
            text=f"✓ Установлено: {self.selected_part['name']} в {self.SLOT_NAMES[slot_idx]}"
        )
        self._draw_rocket()

    def _remove_selected(self):
        """Снимает деталь с выбранного слота."""
        if self.selected_slot is None:
            messagebox.showwarning("Внимание", "Сначала выберите слот на ракете!")
            return

        slot = self.slots[self.selected_slot]
        if slot["part"]:
            part_name = slot["part"]["name"]
            slot["part"] = None
            self.status_label.configure(text=f"Снято: {part_name}")
            self._draw_rocket()
        else:
            self.status_label.configure(text="Этот слот уже пуст")

    def _reset(self):
        """Сбрасывает ракету."""
        for slot in self.slots.values():
            slot["part"] = None
        self.selected_part = None
        self.selected_slot = None
        self.status_label.configure(text="Ракета сброшена — начните сборку заново")
        self._draw_rocket()

    def _check(self):
        """Проверяет правильность сборки."""
        filled = sum(1 for s in self.slots.values() if s["part"])
        correct = sum(
            1 for s in self.slots.values() if s["part"] and s["part"]["type"] == s["type"]
        )

        if filled < 5:
            messagebox.showinfo(
                "Проверка",
                f"Заполнено: {filled}/5\n"
                f"Правильно: {correct}/5\n\n"
                "Заполните все слоты для полного запуска!",
            )
        elif correct == 5:
            messagebox.showinfo(
                "🎉 Успех!",
                "Ракета собрана правильно!\nВсе детали на своих местах.",
            )
        else:
            messagebox.showinfo(
                "Проверка",
                f"Заполнено: {filled}/5\n"
                f"Правильно: {correct}/5\n\n"
                "Красные сегменты — ошибки сборки.",
            )

    def _on_mousewheel(self, event):
        """Прокрутка каталога колёсиком мыши."""
        self.parts_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _update_scrollregion(self, event=None):
        """Обновляет область прокрутки канваса."""
        self.parts_canvas.configure(scrollregion=self.parts_canvas.bbox("all"))

    def _update_ui(self):
        """Обновляет интерфейс."""
        self._draw_rocket()


def main():
    root = tk.Tk()
    app = RocketBuilderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
