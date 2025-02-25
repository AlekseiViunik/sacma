import math
import tkinter as tk

from settings import settings as set


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{set.MAIN_WIN_TITLE}")
        self.root.geometry(f"{set.MAIN_WIN_WIDTH}x{set.MAIN_WIN_HEIGHT}")
        self.center_window(self.root, set.MAIN_WIN_WIDTH, set.MAIN_WIN_HEIGHT)
        self.buttons = set.MAIN_WIN_BUTTONS

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        cols = set.MAIN_WIN_FRAME_COL_NUM
        rows = math.ceil(len(self.buttons) / cols)

        max_width = max(len(name) for name in self.buttons)

        for i, name in enumerate(self.buttons):
            btn = tk.Button(
                frame,
                text=name,
                height=set.BUTTON_HEIGHT,
                width=max_width,
                bg=set.BUTTON_COLOR,
                relief=set.BUTTON_RELIEF,  # no border
                command=lambda n=name: self.open_window(n)
            )
            btn.grid(
                row=i // cols,
                column=i % cols,
                padx=set.BUTTON_PADX,
                pady=set.BUTTON_PADY,
                sticky=set.BUTTON_STICKY
            )

        for i in range(cols):
            self.root.columnconfigure(i, weight=set.GRID_WEIGHT)
        for i in range(rows):
            self.root.rowconfigure(i, weight=set.GRID_WEIGHT)

    def open_window(self, name):
        self.root.withdraw()  # скрыть главное окно

        new_window = tk.Toplevel(self.root)
        new_window.title(name)
        new_window.geometry("400x300")
        self.center_window(new_window, 400, 300)

        if name == "Travi":
            self.create_travi_ui(new_window)
        elif name == "Fiancate":
            new_window.geometry("400x450")
            self.create_fiancate_ui(new_window)
        else:
            tk.Label(
                new_window,
                text=name,
                font=("Arial", 14),
                bg="#f0f0f0"
            ).pack(expand=True)

        btn_invia = tk.Button(
            new_window,
            text="Invia",
            width=10,
            bg="#d9d9d9"
        )
        btn_invia.pack(
            side="bottom",
            anchor="se",
            padx=10,
            pady=10
        )

        new_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.on_close(new_window)
        )

    def create_travi_ui(self, window):
        frame = tk.Frame(window, bg="#f0f0f0", padx=10, pady=10)
        frame.pack(expand=True, fill="both")

        # Поля и варианты выбора
        options = {
            "Tipo": ["TG", "C"],
            "Altezza": [str(x) for x in range(50, 210, 10)],
            "Larghezza": ["45", "50"],
            "Spessore": ["1.2", "1.5", "2.0", "2.5", "3.0"]
        }

        entries = {}

        for i, (label, values) in enumerate(options.items()):
            tk.Label(frame, text=label, bg="#f0f0f0").grid(
                row=i,
                column=0,
                sticky="w",
                pady=5
            )
            var = tk.StringVar(value=values[0])
            dropdown = tk.OptionMenu(frame, var, *values)
            dropdown.grid(row=i, column=1, sticky="ew", padx=5)
            entries[label] = var

            if label in ["Altezza", "Larghezza", "Spessore"]:
                tk.Label(frame, text="mm", bg="#f0f0f0").grid(
                    row=i,
                    column=2,
                    sticky="w"
                )

        # Поле для ввода длины
        tk.Label(frame, text="Lunghezza", bg="#f0f0f0").grid(
            row=len(options),
            column=0,
            sticky="w",
            pady=5
        )
        lunghezza_entry = tk.Entry(frame)
        lunghezza_entry.grid(row=len(options), column=1, sticky="ew", padx=5)
        tk.Label(frame, text="mm", bg="#f0f0f0").grid(
            row=len(options),
            column=2,
            sticky="w"
        )
        entries["Lunghezza"] = lunghezza_entry

        for i in range(3):
            frame.columnconfigure(i, weight=1)

    def create_fiancate_ui(self, window):
        frame = tk.Frame(window, bg="#f0f0f0", padx=10, pady=10)
        frame.pack(expand=True, fill="both")

        # Поля и варианты выбора
        options = {
            "Solo montante": ["No", "Sì"],
            "Sismo resistente": ["No", "Sì"],
            "Sezione": [
                "80/20",
                "80/25",
                "80/30",
                "100/20",
                "100/25",
                "100/30",
                "120/20",
                "120/25",
                "120/30",
                "120x110/20",
                "120x110/25",
                "120x110/30",
                "120x110/40"
            ]
        }

        entries = {}

        for i, (label, values) in enumerate(options.items()):
            tk.Label(frame, text=label, bg="#f0f0f0").grid(
                row=i,
                column=0,
                sticky="w",
                pady=5
            )
            var = tk.StringVar(value=values[0])
            dropdown = tk.OptionMenu(frame, var, *values)
            dropdown.grid(row=i, column=1, sticky="ew", padx=5)
            entries[label] = var

        input_fields = [
            "Altezza",
            "N diagonali 10/10",
            "N diagonali 15/10",
            "N diagonali 20/10",
            "N diagonali 25/10",
            "N diagonali 30/10",
            "N traversi 10/10",
            "N traversi 15/10"
        ]

        start_row = len(options)

        for i, label in enumerate(input_fields):
            tk.Label(frame, text=label, bg="#f0f0f0").grid(
                row=start_row + i,
                column=0,
                sticky="w",
                pady=5
            )
            entry = tk.Entry(frame)
            entry.grid(row=start_row + i, column=1, sticky="ew", padx=5)
            entries[label] = entry

    # Колонки подстраиваем под контент
        for i in range(2):
            frame.columnconfigure(i, weight=1)

    def on_close(self, window):
        window.destroy()
        self.root.deiconify()  # вернуть главное окно

    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
