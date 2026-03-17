import random
import tkinter as tk
from dataclasses import dataclass


@dataclass
class RocketPart:
    name: str
    part_type: str
    position: int
    is_valid: bool


class RocketBuilderApp:
    COLORS = {
        "bg": "#070B16",
        "panel": "#0F172A",
        "panel_soft": "#131F39",
        "panel_alt": "#0C1426",
        "panel_border": "#223155",
        "text": "#F8FAFF",
        "muted": "#9AA9CC",
        "muted_soft": "#67789D",
        "accent": "#7CF5D1",
        "accent_hover": "#94F8DA",
        "warning": "#FFB454",
        "warning_hover": "#FFC26E",
        "danger": "#FF6B81",
        "danger_soft": "#311722",
        "button_dark": "#1A2744",
        "button_dark_hover": "#223457",
        "sky_top": "#091224",
        "sky_bottom": "#18335A",
        "slot": "#101B31",
        "slot_border": "#2F4672",
    }

    TYPE_LABELS = {
        "nose": "Носовой модуль",
        "body": "Корпус",
        "engine": "Двигатель",
        "fin": "Стабилизаторы",
    }

    PART_STYLES = {
        "nose": {
            "card": "#221812",
            "border": "#FFB36C",
            "badge": "#332216",
            "accent": "#FFD2A5",
            "button": "#FFB36C",
            "button_hover": "#FFC487",
            "segment": "#FF9D57",
            "highlight": "#FFD6AA",
        },
        "body": {
            "card": "#132033",
            "border": "#72B8FF",
            "badge": "#1A2D46",
            "accent": "#B7D9FF",
            "button": "#72B8FF",
            "button_hover": "#8FC6FF",
            "segment": "#5AA8FF",
            "highlight": "#B7D9FF",
        },
        "engine": {
            "card": "#11271F",
            "border": "#69E6C0",
            "badge": "#16372C",
            "accent": "#B8FFE8",
            "button": "#69E6C0",
            "button_hover": "#84EDD0",
            "segment": "#48D9AE",
            "highlight": "#A9F6DE",
        },
        "fin": {
            "card": "#1D1730",
            "border": "#C49CFF",
            "badge": "#2A2142",
            "accent": "#E2CFFF",
            "button": "#C49CFF",
            "button_hover": "#D2B3FF",
            "segment": "#B887FF",
            "highlight": "#E6D3FF",
        },
        "invalid": {
            "card": "#2A1720",
            "border": "#FF6B81",
            "badge": "#3B1D28",
            "accent": "#FFC5CF",
            "button": "#FF6B81",
            "button_hover": "#FF8799",
            "segment": "#FF6B81",
            "highlight": "#FFC7D2",
        },
    }

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
        self.root.title("Rocket Builder | Cosmic Lab")
        self.root.geometry("1180x760")
        self.root.minsize(1080, 720)
        self.root.configure(bg=self.COLORS["bg"])

        self.rocket_positions = {
            0: {"name": "Нос", "type": "nose", "part": None},
            1: {"name": "Верхний корпус", "type": "body", "part": None},
            2: {"name": "Нижний корпус", "type": "body", "part": None},
            3: {"name": "Двигатель", "type": "engine", "part": None},
            4: {"name": "Стабилизаторы", "type": "fin", "part": None},
        }
        self.total_slots = len(self.rocket_positions)
        self.available_parts = (
            self.NOSE_CONES
            + self.BODY_SECTIONS
            + self.ENGINES
            + self.FINS
            + self.INVALID_PARTS
        )
        random.shuffle(self.available_parts)

        decor_rng = random.Random(24)
        self.stars = [
            (
                decor_rng.random(),
                decor_rng.random(),
                decor_rng.randint(1, 3),
                decor_rng.choice(["#FFFFFF", "#DBEAFE", "#FDE68A", "#BFDBFE"]),
            )
            for _ in range(72)
        ]

        self.slot_cards = {}
        self.parts_window_id = None

        self._setup_ui()
        self._set_status(
            "Полигон готов к сборке.",
            "info",
            "Выберите деталь справа и соберите ракету снизу вверх.",
        )
        self._draw_rocket()
        self._refresh_dashboard()
        self.root.after(500, self._show_instructions)

    def _setup_ui(self):
        shell = tk.Frame(self.root, bg=self.COLORS["bg"])
        shell.pack(fill=tk.BOTH, expand=True, padx=22, pady=20)

        self._build_header(shell)

        content = tk.Frame(shell, bg=self.COLORS["bg"])
        content.pack(fill=tk.BOTH, expand=True, pady=(18, 0))
        content.grid_columnconfigure(0, weight=5)
        content.grid_columnconfigure(1, weight=3)
        content.grid_rowconfigure(0, weight=1)

        left_panel = self._create_panel(content, bg=self.COLORS["panel"])
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        right_panel = self._create_panel(content, bg=self.COLORS["panel_alt"])
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        self._build_workspace(left_panel)
        self._build_sidebar(right_panel)

    def _build_header(self, parent):
        header = self._create_panel(parent, bg=self.COLORS["panel"])
        header.pack(fill=tk.X)

        top_row = tk.Frame(header, bg=self.COLORS["panel"])
        top_row.pack(fill=tk.X, padx=24, pady=(22, 18))

        title_block = tk.Frame(top_row, bg=self.COLORS["panel"])
        title_block.pack(side=tk.LEFT, fill=tk.X, expand=True)

        badge = tk.Label(
            title_block,
            text="COSMIC LAB",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["accent"],
            font=("Helvetica", 10, "bold"),
            padx=10,
            pady=5,
        )
        badge.pack(anchor="w", pady=(0, 12))

        tk.Label(
            title_block,
            text="Конструктор ракеты",
            bg=self.COLORS["panel"],
            fg=self.COLORS["text"],
            font=("Helvetica", 28, "bold"),
        ).pack(anchor="w")

        tk.Label(
            title_block,
            text="Более атмосферная версия сборщика: кастомные панели, живая сцена запуска и аккуратные карточки деталей.",
            bg=self.COLORS["panel"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 11),
            wraplength=640,
            justify="left",
        ).pack(anchor="w", pady=(10, 0))

        mission_card = self._create_panel(
            top_row,
            bg=self.COLORS["panel_soft"],
            border=self.COLORS["panel_border"],
        )
        mission_card.pack(side=tk.RIGHT, anchor="n")

        tk.Label(
            mission_card,
            text="Сводка миссии",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 10, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 6))

        self.header_progress_label = tk.Label(
            mission_card,
            text="0/5 модулей",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["text"],
            font=("Helvetica", 18, "bold"),
        )
        self.header_progress_label.pack(anchor="w", padx=16)

        self.header_accuracy_label = tk.Label(
            mission_card,
            text="Точность: 0/5",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 10),
        )
        self.header_accuracy_label.pack(anchor="w", padx=16, pady=(4, 14))

        order_strip = self._create_panel(
            header,
            bg=self.COLORS["panel_soft"],
            border=self.COLORS["panel_border"],
        )
        order_strip.pack(fill=tk.X, padx=24, pady=(0, 22))

        tk.Label(
            order_strip,
            text="Порядок сборки: Нос -> Верхний корпус -> Нижний корпус -> Двигатель -> Стабилизаторы",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["text"],
            font=("Helvetica", 10, "bold"),
            pady=11,
        ).pack(anchor="w", padx=14)

    def _build_workspace(self, parent):
        stats_row = tk.Frame(parent, bg=self.COLORS["panel"])
        stats_row.pack(fill=tk.X, padx=20, pady=(20, 14))

        progress_card = self._create_panel(stats_row, bg=self.COLORS["panel_soft"])
        progress_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(
            progress_card,
            text="Прогресс сборки",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 10, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 4))

        progress_row = tk.Frame(progress_card, bg=self.COLORS["panel_soft"])
        progress_row.pack(fill=tk.X, padx=16)

        self.progress_value_label = tk.Label(
            progress_row,
            text="0/5",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["text"],
            font=("Helvetica", 22, "bold"),
        )
        self.progress_value_label.pack(side=tk.LEFT)

        self.progress_note_label = tk.Label(
            progress_row,
            text="Выберите первый модуль.",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 10),
        )
        self.progress_note_label.pack(side=tk.LEFT, padx=(12, 0), pady=(8, 0))

        self.progress_bar = tk.Canvas(
            progress_card,
            height=12,
            bg=self.COLORS["panel_soft"],
            highlightthickness=0,
            bd=0,
        )
        self.progress_bar.pack(fill=tk.X, padx=16, pady=(12, 16))
        self.progress_bar.bind("<Configure>", lambda event: self._draw_progress_bar())

        status_card = self._create_panel(stats_row, bg=self.COLORS["panel_soft"])
        status_card.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.status_badge = tk.Label(
            status_card,
            text="НАВИГАЦИЯ",
            bg=self.COLORS["button_dark"],
            fg=self.COLORS["accent"],
            font=("Helvetica", 10, "bold"),
            padx=10,
            pady=5,
        )
        self.status_badge.pack(anchor="w", padx=16, pady=(14, 8))

        self.status_label = tk.Label(
            status_card,
            text="Полигон готов к сборке.",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["text"],
            font=("Helvetica", 15, "bold"),
            wraplength=340,
            justify="left",
        )
        self.status_label.pack(anchor="w", padx=16)

        self.status_hint_label = tk.Label(
            status_card,
            text="Выберите деталь справа и соберите ракету снизу вверх.",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 10),
            wraplength=340,
            justify="left",
        )
        self.status_hint_label.pack(anchor="w", padx=16, pady=(8, 16))

        canvas_card = self._create_panel(parent, bg=self.COLORS["panel_alt"])
        canvas_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 14))

        canvas_header = tk.Frame(canvas_card, bg=self.COLORS["panel_alt"])
        canvas_header.pack(fill=tk.X, padx=16, pady=(16, 10))

        tk.Label(
            canvas_header,
            text="Сборочный ангар",
            bg=self.COLORS["panel_alt"],
            fg=self.COLORS["text"],
            font=("Helvetica", 16, "bold"),
        ).pack(anchor="w")

        tk.Label(
            canvas_header,
            text="Тёмная сцена с подсветкой показывает текущую конфигурацию ракеты в реальном времени.",
            bg=self.COLORS["panel_alt"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 10),
        ).pack(anchor="w", pady=(6, 0))

        self.canvas = tk.Canvas(
            canvas_card,
            bg=self.COLORS["sky_top"],
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))
        self.canvas.bind("<Configure>", self._draw_rocket)

        slots_wrap = tk.Frame(parent, bg=self.COLORS["panel"])
        slots_wrap.pack(fill=tk.X, padx=20, pady=(0, 14))

        tk.Label(
            slots_wrap,
            text="Быстрый обзор секций",
            bg=self.COLORS["panel"],
            fg=self.COLORS["text"],
            font=("Helvetica", 13, "bold"),
        ).pack(anchor="w")

        tk.Label(
            slots_wrap,
            text="Каждая карточка показывает текущее состояние конкретного слота.",
            bg=self.COLORS["panel"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 10),
        ).pack(anchor="w", pady=(4, 10))

        slots_grid = tk.Frame(slots_wrap, bg=self.COLORS["panel"])
        slots_grid.pack(fill=tk.X)

        for column in range(self.total_slots):
            slots_grid.grid_columnconfigure(column, weight=1)

        for pos_id in sorted(self.rocket_positions):
            pos_data = self.rocket_positions[pos_id]
            card = self._create_panel(slots_grid, bg=self.COLORS["panel_soft"])
            card.grid(row=0, column=pos_id, sticky="nsew", padx=4)

            title = tk.Label(
                card,
                text=pos_data["name"],
                bg=self.COLORS["panel_soft"],
                fg=self.COLORS["muted"],
                font=("Helvetica", 10, "bold"),
            )
            title.pack(anchor="w", padx=12, pady=(12, 6))

            value = tk.Label(
                card,
                text="Пусто",
                bg=self.COLORS["panel_soft"],
                fg=self.COLORS["muted_soft"],
                font=("Helvetica", 10),
                wraplength=140,
                justify="left",
            )
            value.pack(anchor="w", padx=12, pady=(0, 12))

            self.slot_cards[pos_id] = {"frame": card, "title": title, "value": value}

        controls = tk.Frame(parent, bg=self.COLORS["panel"])
        controls.pack(fill=tk.X, padx=20, pady=(0, 20))

        check_btn = self._create_action_button(
            controls,
            "Проверить ракету",
            self._check_rocket,
            self.COLORS["accent"],
            self.COLORS["accent_hover"],
            self.COLORS["bg"],
        )
        check_btn.pack(side=tk.LEFT)

        reset_btn = self._create_action_button(
            controls,
            "Сбросить",
            self._reset_rocket,
            self.COLORS["warning"],
            self.COLORS["warning_hover"],
            self.COLORS["bg"],
        )
        reset_btn.pack(side=tk.LEFT, padx=10)

        help_btn = self._create_action_button(
            controls,
            "Правила",
            self._show_instructions,
            self.COLORS["button_dark"],
            self.COLORS["button_dark_hover"],
            self.COLORS["text"],
        )
        help_btn.pack(side=tk.LEFT)

        tk.Label(
            controls,
            text="Красный цвет подсказывает, что в конфигурации есть конфликт.",
            bg=self.COLORS["panel"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 10),
        ).pack(side=tk.RIGHT, pady=(10, 0))

    def _build_sidebar(self, parent):
        header = tk.Frame(parent, bg=self.COLORS["panel_alt"])
        header.pack(fill=tk.X, padx=18, pady=(18, 10))

        tk.Label(
            header,
            text="Каталог деталей",
            bg=self.COLORS["panel_alt"],
            fg=self.COLORS["text"],
            font=("Helvetica", 18, "bold"),
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Карточки справа выглядят как мини-панели управления: каждая деталь получила свой цвет, описание и кнопку установки.",
            bg=self.COLORS["panel_alt"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 10),
            wraplength=360,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

        legend = tk.Frame(parent, bg=self.COLORS["panel_alt"])
        legend.pack(fill=tk.X, padx=18, pady=(0, 10))

        legend_items = [
            ("Нос", self.PART_STYLES["nose"]["button"]),
            ("Корпус", self.PART_STYLES["body"]["button"]),
            ("Двигатель", self.PART_STYLES["engine"]["button"]),
            ("Стабилизаторы", self.PART_STYLES["fin"]["button"]),
            ("Ложная деталь", self.PART_STYLES["invalid"]["button"]),
        ]

        for text, color in legend_items:
            tag = tk.Label(
                legend,
                text=text,
                bg=color,
                fg=self.COLORS["bg"],
                font=("Helvetica", 9, "bold"),
                padx=10,
                pady=5,
            )
            tag.pack(side=tk.LEFT, padx=(0, 6), pady=(0, 6))

        catalog_card = self._create_panel(parent, bg=self.COLORS["panel_soft"])
        catalog_card.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 18))

        tk.Label(
            catalog_card,
            text="Доступные модули",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["text"],
            font=("Helvetica", 13, "bold"),
        ).pack(anchor="w", padx=14, pady=(14, 6))

        tk.Label(
            catalog_card,
            text="Нажмите на карточку или кнопку, чтобы установить модуль в ракету.",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 10),
        ).pack(anchor="w", padx=14, pady=(0, 10))

        parts_container = tk.Frame(catalog_card, bg=self.COLORS["panel_soft"])
        parts_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.parts_canvas = tk.Canvas(
            parts_container,
            bg=self.COLORS["panel_soft"],
            highlightthickness=0,
            bd=0,
        )
        scrollbar = tk.Scrollbar(
            parts_container,
            orient="vertical",
            command=self.parts_canvas.yview,
        )
        self.parts_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.parts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.parts_frame = tk.Frame(self.parts_canvas, bg=self.COLORS["panel_soft"])
        self.parts_window_id = self.parts_canvas.create_window(
            (0, 0),
            window=self.parts_frame,
            anchor="nw",
        )

        self.parts_frame.bind("<Configure>", self._sync_parts_scrollregion)
        self.parts_canvas.bind("<Configure>", self._sync_parts_width)
        self.parts_canvas.bind(
            "<Enter>",
            lambda event: self.parts_canvas.bind_all("<MouseWheel>", self._on_parts_mousewheel),
        )
        self.parts_canvas.bind(
            "<Leave>",
            lambda event: self.parts_canvas.unbind_all("<MouseWheel>"),
        )

        self._populate_parts()

        tk.Label(
            catalog_card,
            text="Секрет внимательной сборки: красные карточки выглядят красиво, но ломают идеальную конфигурацию.",
            bg=self.COLORS["panel_soft"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 10),
            wraplength=360,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(0, 14))

    def _create_panel(self, parent, bg=None, border=None):
        return tk.Frame(
            parent,
            bg=bg or self.COLORS["panel"],
            bd=0,
            highlightthickness=1,
            highlightbackground=border or self.COLORS["panel_border"],
            highlightcolor=border or self.COLORS["panel_border"],
        )

    def _create_action_button(self, parent, text, command, bg, hover_bg, fg):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            font=("Helvetica", 11, "bold"),
            padx=18,
            pady=12,
        )
        button.bind("<Enter>", lambda event: button.configure(bg=hover_bg))
        button.bind("<Leave>", lambda event: button.configure(bg=bg))
        return button

    def _style_for_part(self, part):
        return self.PART_STYLES[part.part_type if part.is_valid else "invalid"]

    def _part_description(self, part):
        if part.is_valid:
            preferred_slot = self.rocket_positions[part.position]["name"]
            return (
                f"Тип: {self.TYPE_LABELS.get(part.part_type, 'Модуль')}. "
                f"Лучше всего подходит для секции «{preferred_slot}»."
            )
        return (
            "Ложная деталь для проверки внимательности. "
            "Её установка подсветит проблемную секцию красным."
        )

    def _populate_parts(self):
        for widget in self.parts_frame.winfo_children():
            widget.destroy()

        for part in self.available_parts:
            style = self._style_for_part(part)
            badge_text = self.TYPE_LABELS.get(part.part_type, "Модуль")
            if not part.is_valid:
                badge_text = "Ложная деталь"

            card = self._create_panel(
                self.parts_frame,
                bg=style["card"],
                border=style["border"],
            )
            card.pack(fill=tk.X, padx=6, pady=7)

            content = tk.Frame(card, bg=style["card"])
            content.pack(fill=tk.X, padx=14, pady=12)

            top_row = tk.Frame(content, bg=style["card"])
            top_row.pack(fill=tk.X)

            title = tk.Label(
                top_row,
                text=part.name,
                bg=style["card"],
                fg=self.COLORS["text"],
                font=("Helvetica", 12, "bold"),
                cursor="hand2",
            )
            title.pack(side=tk.LEFT, anchor="w")

            badge = tk.Label(
                top_row,
                text=badge_text,
                bg=style["badge"],
                fg=style["accent"],
                font=("Helvetica", 9, "bold"),
                padx=10,
                pady=4,
                cursor="hand2",
            )
            badge.pack(side=tk.RIGHT)

            description = tk.Label(
                content,
                text=self._part_description(part),
                bg=style["card"],
                fg=self.COLORS["muted"],
                font=("Helvetica", 10),
                wraplength=300,
                justify="left",
                cursor="hand2",
            )
            description.pack(fill=tk.X, pady=(10, 10))

            footer = tk.Frame(content, bg=style["card"])
            footer.pack(fill=tk.X)

            hint = tk.Label(
                footer,
                text="Нажмите на карточку или кнопку",
                bg=style["card"],
                fg=self.COLORS["muted_soft"],
                font=("Helvetica", 9),
                cursor="hand2",
            )
            hint.pack(side=tk.LEFT, pady=(4, 0))

            add_button = tk.Button(
                footer,
                text="Установить",
                command=lambda p=part: self._add_part(p),
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                bg=style["button"],
                fg=self.COLORS["bg"],
                activebackground=style["button_hover"],
                activeforeground=self.COLORS["bg"],
                font=("Helvetica", 10, "bold"),
                padx=12,
                pady=6,
            )
            add_button.pack(side=tk.RIGHT)

            add_button.bind(
                "<Enter>",
                lambda event, btn=add_button, color=style["button_hover"]: btn.configure(bg=color),
            )
            add_button.bind(
                "<Leave>",
                lambda event, btn=add_button, color=style["button"]: btn.configure(bg=color),
            )

            clickable = [card, content, top_row, title, badge, description, footer, hint]
            for widget in clickable:
                widget.bind("<Button-1>", lambda event, p=part: self._add_part(p))

    def _sync_parts_scrollregion(self, event=None):
        self.parts_canvas.configure(scrollregion=self.parts_canvas.bbox("all"))

    def _sync_parts_width(self, event):
        if self.parts_window_id is not None:
            self.parts_canvas.itemconfigure(self.parts_window_id, width=event.width)

    def _on_parts_mousewheel(self, event):
        if event.delta == 0:
            return
        step = -1 if event.delta > 0 else 1
        self.parts_canvas.yview_scroll(step, "units")

    def _filled_slots(self):
        return sum(1 for pos in self.rocket_positions.values() if pos["part"] is not None)

    def _correct_slots(self):
        return sum(1 for pos in self.rocket_positions.values() if self._is_slot_correct(pos))

    def _is_slot_correct(self, pos_data):
        part = pos_data["part"]
        return bool(part and part.is_valid and pos_data["type"] == part.part_type)

    def _refresh_dashboard(self):
        filled = self._filled_slots()
        correct = self._correct_slots()

        self.header_progress_label.configure(text=f"{filled}/{self.total_slots} модулей")
        self.header_accuracy_label.configure(text=f"Точность: {correct}/{self.total_slots}")
        self.progress_value_label.configure(text=f"{filled}/{self.total_slots}")

        if filled == 0:
            progress_text = "Выберите первый модуль."
        elif filled == self.total_slots and correct == self.total_slots:
            progress_text = "Ракета готова к запуску."
        elif filled == self.total_slots:
            progress_text = f"Найдены конфликтующие секции: {self.total_slots - correct}."
        else:
            progress_text = f"Правильных секций: {correct}/{self.total_slots}."

        self.progress_note_label.configure(text=progress_text)
        self._draw_progress_bar()
        self._refresh_slot_cards()

    def _draw_progress_bar(self):
        self.progress_bar.delete("all")

        width = max(self.progress_bar.winfo_width(), 220)
        height = max(self.progress_bar.winfo_height(), 12)
        ratio = self._filled_slots() / self.total_slots

        self.progress_bar.create_rectangle(
            0,
            0,
            width,
            height,
            fill="#1A2744",
            outline="",
        )
        self.progress_bar.create_rectangle(
            0,
            0,
            width * ratio,
            height,
            fill=self.COLORS["accent"],
            outline="",
        )

        for index in range(1, self.total_slots):
            x = width * index / self.total_slots
            self.progress_bar.create_line(x, 0, x, height, fill=self.COLORS["panel_border"])

    def _refresh_slot_cards(self):
        for pos_id, pos_data in self.rocket_positions.items():
            card = self.slot_cards[pos_id]
            part = pos_data["part"]

            if part is None:
                bg = self.COLORS["panel_soft"]
                border = self.COLORS["panel_border"]
                value_text = "Пусто"
                value_color = self.COLORS["muted_soft"]
            elif self._is_slot_correct(pos_data):
                style = self._style_for_part(part)
                bg = self.COLORS["panel_soft"]
                border = style["border"]
                value_text = part.name
                value_color = self.COLORS["text"]
            else:
                bg = self.COLORS["danger_soft"]
                border = self.COLORS["danger"]
                value_text = part.name
                value_color = "#FFE0E6"

            card["frame"].configure(
                bg=bg,
                highlightbackground=border,
                highlightcolor=border,
            )
            card["title"].configure(bg=bg)
            card["value"].configure(bg=bg, fg=value_color, text=value_text)

    def _set_status(self, message, tone, hint):
        styles = {
            "info": {
                "label": "НАВИГАЦИЯ",
                "badge_bg": self.COLORS["button_dark"],
                "badge_fg": self.COLORS["accent"],
                "text_fg": self.COLORS["text"],
            },
            "success": {
                "label": "ГОТОВО",
                "badge_bg": "#16372C",
                "badge_fg": self.COLORS["accent"],
                "text_fg": self.COLORS["text"],
            },
            "warning": {
                "label": "ВНИМАНИЕ",
                "badge_bg": "#3A2B12",
                "badge_fg": self.COLORS["warning"],
                "text_fg": self.COLORS["text"],
            },
            "danger": {
                "label": "КОНФЛИКТ",
                "badge_bg": "#381926",
                "badge_fg": self.COLORS["danger"],
                "text_fg": "#FFE0E6",
            },
        }
        style = styles[tone]

        self.status_badge.configure(
            text=style["label"],
            bg=style["badge_bg"],
            fg=style["badge_fg"],
        )
        self.status_label.configure(text=message, fg=style["text_fg"])
        self.status_hint_label.configure(text=hint, fg=self.COLORS["muted"])

    def _show_dialog(self, title, message, accent):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(bg=self.COLORS["bg"])

        outer = self._create_panel(dialog, bg=self.COLORS["panel"])
        outer.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        tk.Frame(outer, bg=accent, height=6).pack(fill=tk.X)

        content = tk.Frame(outer, bg=self.COLORS["panel"])
        content.pack(fill=tk.BOTH, expand=True, padx=22, pady=22)

        tk.Label(
            content,
            text=title,
            bg=self.COLORS["panel"],
            fg=self.COLORS["text"],
            font=("Helvetica", 18, "bold"),
        ).pack(anchor="w")

        tk.Label(
            content,
            text=message,
            bg=self.COLORS["panel"],
            fg=self.COLORS["muted"],
            font=("Helvetica", 11),
            wraplength=390,
            justify="left",
        ).pack(anchor="w", pady=(12, 18))

        button = self._create_action_button(
            content,
            "Понятно",
            dialog.destroy,
            accent,
            self._mix_color(accent, "#FFFFFF", 0.16),
            self.COLORS["bg"],
        )
        button.pack(anchor="e")

        self._center_window(dialog, 460, 240)
        dialog.bind("<Escape>", lambda event: dialog.destroy())
        button.focus_set()

    def _center_window(self, window, width, height):
        self.root.update_idletasks()
        x = self.root.winfo_rootx() + max((self.root.winfo_width() - width) // 2, 0)
        y = self.root.winfo_rooty() + max((self.root.winfo_height() - height) // 2, 0)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def _add_part(self, part):
        placed_slot = None
        placed_in_matching_type = False

        for pos_data in self.rocket_positions.values():
            if pos_data["part"] is None and pos_data["type"] == part.part_type:
                pos_data["part"] = part
                placed_slot = pos_data
                placed_in_matching_type = True
                break

        if placed_slot is None:
            for pos_data in self.rocket_positions.values():
                if pos_data["part"] is None:
                    pos_data["part"] = part
                    placed_slot = pos_data
                    break

        if placed_slot is None:
            self._set_status(
                "Все секции уже заняты.",
                "warning",
                "Сначала выполните сброс или проверьте результат сборки.",
            )
            self._show_dialog(
                "Свободных секций нет",
                "В ракете уже не осталось пустых слотов. Нажмите «Сбросить», чтобы собрать новый вариант.",
                self.COLORS["warning"],
            )
            return

        if part.is_valid and placed_in_matching_type:
            self._set_status(
                f"{part.name} установлен.",
                "success",
                f"Секция «{placed_slot['name']}» заполнена корректным модулем.",
            )
        elif placed_in_matching_type:
            self._set_status(
                f"{part.name} выглядит эффектно, но это ложная деталь.",
                "warning",
                "Карточка подошла по типу, однако модуль всё равно нарушает правильную схему.",
            )
        else:
            self._set_status(
                f"{part.name} установлен не туда.",
                "danger",
                f"Секция «{placed_slot['name']}» теперь конфликтует с правильной конфигурацией.",
            )

        self._draw_rocket()
        self._refresh_dashboard()

    def _check_rocket(self):
        if self._filled_slots() < self.total_slots:
            self._set_status(
                "Сборка ещё не завершена.",
                "warning",
                "Заполните все пять секций, а потом запускайте финальную проверку.",
            )
            self._show_dialog(
                "Не хватает деталей",
                "Сначала заполните все позиции ракеты, а затем нажмите кнопку проверки.",
                self.COLORS["warning"],
            )
            return

        correct = self._correct_slots()

        if correct == self.total_slots:
            self._set_status(
                "Ракета собрана идеально.",
                "success",
                "Все секции совпали с правильной схемой. Запуск разрешён.",
            )
            self._show_dialog(
                "Пуск разрешён",
                "Отличная работа. Все модули на своих местах, и ракета готова к старту.",
                self.COLORS["accent"],
            )
        else:
            self._set_status(
                "В сборке есть ошибки.",
                "danger",
                f"Правильно собрано: {correct}/{self.total_slots}. Красные секции показывают, что стоит заменить.",
            )
            self._show_dialog(
                "Нужна доработка",
                f"Правильных секций: {correct} из {self.total_slots}. Проверьте красные элементы и попробуйте ещё раз.",
                self.COLORS["danger"],
            )

    def _reset_rocket(self):
        for pos_data in self.rocket_positions.values():
            pos_data["part"] = None

        random.shuffle(self.available_parts)
        self._populate_parts()
        self._draw_rocket()
        self._refresh_dashboard()
        self._set_status(
            "Полигон очищен.",
            "info",
            "Каталог перемешан. Можно собирать новую кастомную ракету.",
        )

    def _show_instructions(self):
        self._show_dialog(
            "Как играть",
            "1. Выберите деталь в каталоге справа.\n"
            "2. Она автоматически установится в первую подходящую секцию.\n"
            "3. Красные карточки и секции означают конфликт или ложный модуль.\n"
            "4. Когда все 5 секций заполнены, нажмите «Проверить ракету».",
            self.COLORS["accent"],
        )

    def _mix_color(self, start, end, ratio):
        ratio = max(0.0, min(1.0, ratio))
        start_rgb = [int(start[index:index + 2], 16) for index in (1, 3, 5)]
        end_rgb = [int(end[index:index + 2], 16) for index in (1, 3, 5)]
        mixed = [
            int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * ratio)
            for i in range(3)
        ]
        return "#{:02X}{:02X}{:02X}".format(*mixed)

    def _draw_rocket(self, event=None):
        if not hasattr(self, "canvas"):
            return

        self.canvas.delete("all")

        width = max(self.canvas.winfo_width(), 680)
        height = max(self.canvas.winfo_height(), 470)

        self._draw_space_background(width, height)

        self.canvas.create_text(
            28,
            30,
            text="LAUNCH VIEW",
            anchor="w",
            fill=self.COLORS["accent"],
            font=("Helvetica", 12, "bold"),
        )
        self.canvas.create_text(
            28,
            52,
            text="Сцена обновляется сразу после каждой установленной детали.",
            anchor="w",
            fill=self.COLORS["muted"],
            font=("Helvetica", 10),
        )

        center_x = width * 0.37
        segment_width = min(124, width * 0.22)
        segment_height = min(84, max(70, (height - 190) / self.total_slots))
        y_offset = 92
        body_left = center_x - segment_width / 2
        body_right = center_x + segment_width / 2

        self.canvas.create_oval(
            body_left - 86,
            y_offset - 34,
            body_right + 86,
            y_offset + segment_height * self.total_slots + 42,
            outline="#20365E",
            width=2,
        )
        self.canvas.create_oval(
            body_left - 56,
            y_offset + 8,
            body_right + 56,
            y_offset + segment_height * self.total_slots + 6,
            outline="#274673",
            width=1,
            dash=(8, 5),
        )

        for pos_id in sorted(self.rocket_positions):
            pos_data = self.rocket_positions[pos_id]
            y = y_offset + pos_id * segment_height
            slot_center_y = y + (segment_height - 12) / 2

            left_label_x = 30
            right_label_x = min(width - 210, body_right + 38)

            self.canvas.create_text(
                left_label_x,
                slot_center_y - 10,
                text=pos_data["name"],
                anchor="w",
                fill=self.COLORS["muted"],
                font=("Helvetica", 10, "bold"),
            )
            self.canvas.create_line(
                left_label_x + 112,
                slot_center_y + 1,
                body_left - 12,
                slot_center_y + 1,
                fill="#294267",
                dash=(5, 4),
            )

            part = pos_data["part"]
            if part is None:
                self.canvas.create_rectangle(
                    body_left,
                    y,
                    body_right,
                    y + segment_height - 12,
                    fill=self.COLORS["slot"],
                    outline=self.COLORS["slot_border"],
                    width=2,
                    dash=(7, 5),
                )
                state_text = "Ожидает модуль"
                state_color = self.COLORS["muted_soft"]
                self.canvas.create_text(
                    center_x,
                    slot_center_y,
                    text="Пусто",
                    fill=self.COLORS["muted"],
                    font=("Helvetica", 10, "bold"),
                )
            else:
                wrong = not self._is_slot_correct(pos_data)
                self._draw_segment(part, center_x, y, segment_width, segment_height, wrong)
                state_text = part.name
                state_color = self.COLORS["text"] if not wrong else "#FFE0E6"
                self.canvas.create_text(
                    center_x,
                    slot_center_y,
                    text=part.name,
                    width=int(segment_width - 18),
                    fill=self.COLORS["text"] if not wrong else "#FFE0E6",
                    font=("Helvetica", 9, "bold"),
                )

            self.canvas.create_line(
                body_right + 12,
                slot_center_y + 1,
                right_label_x - 12,
                slot_center_y + 1,
                fill="#294267",
                dash=(5, 4),
            )
            self.canvas.create_text(
                right_label_x,
                slot_center_y,
                text=state_text,
                anchor="w",
                width=160,
                justify="left",
                fill=state_color,
                font=("Helvetica", 10, "bold"),
            )

        pad_y = y_offset + segment_height * self.total_slots + 16
        self.canvas.create_rectangle(
            body_left - 56,
            pad_y,
            body_right + 56,
            pad_y + 18,
            fill="#13223C",
            outline="#31527F",
            width=2,
        )
        self.canvas.create_line(
            body_left - 74,
            pad_y + 18,
            body_right + 74,
            pad_y + 18,
            fill="#274673",
            width=2,
        )

        self._draw_canvas_summary(width, height)

    def _draw_space_background(self, width, height):
        steps = 18
        for step in range(steps):
            ratio = step / max(steps - 1, 1)
            color = self._mix_color(self.COLORS["sky_top"], self.COLORS["sky_bottom"], ratio)
            y0 = int(height * step / steps)
            y1 = int(height * (step + 1) / steps)
            self.canvas.create_rectangle(0, y0, width, y1, fill=color, outline=color)

        self.canvas.create_oval(
            width - 210,
            44,
            width + 40,
            260,
            fill="#17315A",
            outline="",
        )
        self.canvas.create_oval(
            width - 150,
            88,
            width - 12,
            210,
            fill="#26518E",
            outline="",
        )

        for x_ratio, y_ratio, size, color in self.stars:
            x = int(x_ratio * width)
            y = int(y_ratio * height * 0.78)
            self.canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")

        self.canvas.create_arc(
            -140,
            height - 170,
            width + 140,
            height + 200,
            start=0,
            extent=180,
            fill="#08111F",
            outline="",
        )

    def _draw_segment(self, part, center_x, y, width, height, wrong):
        style = self._style_for_part(part)
        fill = style["segment"] if not wrong else self.COLORS["danger"]
        highlight = style["highlight"] if not wrong else "#FFD0D8"
        outline = style["border"] if not wrong else self.COLORS["danger"]

        left = center_x - width / 2
        right = center_x + width / 2
        top = y
        bottom = y + height - 12

        self.canvas.create_rectangle(
            left - 4,
            top + 6,
            right + 4,
            bottom + 6,
            fill="#0B1324",
            outline="",
        )

        if part.part_type == "nose":
            self.canvas.create_polygon(
                left,
                bottom,
                center_x,
                top - 10,
                right,
                bottom,
                fill=fill,
                outline=outline,
                width=2,
                smooth=True,
            )
            self.canvas.create_polygon(
                center_x - width * 0.16,
                top + height * 0.28,
                center_x,
                top + 8,
                center_x + width * 0.16,
                top + height * 0.28,
                fill=highlight,
                outline="",
            )
            return

        if part.part_type == "body":
            self.canvas.create_polygon(
                left + 8,
                top,
                right - 8,
                top,
                right,
                bottom,
                left,
                bottom,
                fill=fill,
                outline=outline,
                width=2,
            )
            self.canvas.create_rectangle(
                center_x - 10,
                top + 12,
                center_x + 10,
                bottom - 18,
                fill=highlight,
                outline="",
            )
            self.canvas.create_rectangle(
                center_x - 20,
                top + 18,
                center_x + 20,
                top + 26,
                fill="#F8FAFF",
                outline="",
            )
            return

        if part.part_type == "engine":
            engine_bottom = bottom - 10
            self.canvas.create_polygon(
                left + 10,
                top,
                right - 10,
                top,
                right,
                engine_bottom,
                left,
                engine_bottom,
                fill=fill,
                outline=outline,
                width=2,
            )
            self.canvas.create_polygon(
                center_x - width * 0.18,
                engine_bottom,
                center_x,
                bottom + 16,
                center_x + width * 0.18,
                engine_bottom,
                fill=highlight,
                outline=outline,
                width=2,
            )
            if not wrong:
                self.canvas.create_polygon(
                    center_x - 16,
                    bottom - 2,
                    center_x,
                    bottom + 20,
                    center_x + 16,
                    bottom - 2,
                    fill="#FFD25D",
                    outline="",
                )
                self.canvas.create_polygon(
                    center_x - 10,
                    bottom + 2,
                    center_x,
                    bottom + 16,
                    center_x + 10,
                    bottom + 2,
                    fill="#FF834F",
                    outline="",
                )
            return

        if part.part_type == "fin":
            core_fill = self.PART_STYLES["body"]["segment"] if not wrong else self.COLORS["danger"]
            core_highlight = self.PART_STYLES["body"]["highlight"] if not wrong else "#FFD0D8"
            body_left = center_x - width * 0.25
            body_right = center_x + width * 0.25

            self.canvas.create_polygon(
                left - 4,
                bottom - 8,
                body_left - 4,
                top + 20,
                body_left + 8,
                bottom - 8,
                fill=fill,
                outline=outline,
                width=2,
            )
            self.canvas.create_polygon(
                right + 4,
                bottom - 8,
                body_right + 4,
                top + 20,
                body_right - 8,
                bottom - 8,
                fill=fill,
                outline=outline,
                width=2,
            )
            self.canvas.create_polygon(
                body_left,
                top,
                body_right,
                top,
                body_right + 4,
                bottom,
                body_left - 4,
                bottom,
                fill=core_fill,
                outline=outline,
                width=2,
            )
            self.canvas.create_rectangle(
                center_x - 9,
                top + 10,
                center_x + 9,
                bottom - 18,
                fill=core_highlight,
                outline="",
            )

    def _draw_canvas_summary(self, width, height):
        filled = self._filled_slots()
        correct = self._correct_slots()
        x0 = width - 220
        y0 = height - 170
        x1 = width - 24
        y1 = height - 24

        self.canvas.create_rectangle(
            x0,
            y0,
            x1,
            y1,
            fill="#0E1830",
            outline="#2A4069",
            width=2,
        )

        self.canvas.create_text(
            x0 + 16,
            y0 + 20,
            text="Короткая сводка",
            anchor="w",
            fill=self.COLORS["text"],
            font=("Helvetica", 11, "bold"),
        )
        self.canvas.create_text(
            x0 + 16,
            y0 + 48,
            text=f"Собрано модулей: {filled}/{self.total_slots}",
            anchor="w",
            fill=self.COLORS["muted"],
            font=("Helvetica", 10),
        )
        self.canvas.create_text(
            x0 + 16,
            y0 + 72,
            text=f"Точных секций: {correct}/{self.total_slots}",
            anchor="w",
            fill=self.COLORS["muted"],
            font=("Helvetica", 10),
        )
        self.canvas.create_text(
            x0 + 16,
            y0 + 108,
            text="Подсказка",
            anchor="w",
            fill=self.COLORS["accent"],
            font=("Helvetica", 10, "bold"),
        )
        self.canvas.create_text(
            x0 + 16,
            y0 + 132,
            text="Если секция стала красной, значит там неверная деталь или конфликт по типу.",
            anchor="w",
            width=160,
            justify="left",
            fill=self.COLORS["muted"],
            font=("Helvetica", 9),
        )


def main():
    root = tk.Tk()
    RocketBuilderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
