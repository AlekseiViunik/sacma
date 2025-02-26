import math
import tkinter as tk

from logic.excel_file_handler import ExcelFileHandler
from settings import settings as set
from .window_creator import WindowCreator


class App:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.entries = {}
        self.root.title(f"{set.MAIN_WIN_TITLE}")
        self.root.geometry(f"{set.MAIN_WIN_WIDTH}x{set.MAIN_WIN_HEIGHT}")
        self.center_window(self.root, set.MAIN_WIN_WIDTH, set.MAIN_WIN_HEIGHT)
        self.buttons = set.MAIN_WIN_BUTTONS

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        cols = set.COL_NUM
        cols = set.COL_NUM
        rows = math.ceil(len(self.buttons) / cols)

        max_width = max(len(name) for name in self.buttons)

        for i, name in enumerate(self.buttons):
            btn = tk.Button(
                frame,
                text=name,
                height=set.BUTTON_HEIGHT,
                width=max_width,
                bg=set.BUTTON_COLOR,
                relief=set.BUTTON_RELIEF,
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
        new_window.geometry(f"{set.SECOND_WIN_WIDTH}x{set.SECOND_WIN_HEIGHT}")
        self.center_window(
            new_window,
            set.SECOND_WIN_WIDTH,
            set.SECOND_WIN_HEIGHT
        )

        method_name = (
            f"{set.BUTTON_METHOD_PREFIX}{name.lower()}"
            f"{set.BUTTON_METHOD_POSTFIX}"
        )
        method = getattr(self, method_name, None)

        if method:
            method(new_window)
        else:
            tk.Label(
                new_window,
                text=name,
                font=(set.LABEL_FONT_FAMILY, set.LABEL_FONT_SIZE),
                bg=set.LABEL_BG_COLOR
            ).pack(expand=True)

        btn_invia = tk.Button(
            new_window,
            text=set.BUTTON_INVIA_TITLE,
            width=set.BUTTON_INVIA_WIDTH,
            bg=set.BUTTON_COLOR,
            relief=set.BUTTON_RELIEF,
            command=lambda n=name: self.calculate(n)
        )
        btn_invia.pack(
            side=set.BUTTON_INVIA_SIDE,
            anchor=set.BUTTON_INVIA_ANCHOR,
            padx=set.BUTTON_PADX,
            pady=set.BUTTON_PADY
        )

        new_window.protocol(
            set.ON_CLOSING_WINDOW,
            lambda: self.on_close(new_window)
        )

    def create_travi_ui(self, window):
        creator = WindowCreator(
            window,
            set.TRAVI_SELECT_FIELDS,
            set.TRAVI_INPUT_FIELDS
        )
        self.entries = creator.create_ui()

    def create_fiancate_ui(self, window):
        window.geometry(f"{set.FIANCATE_WIN_WIDTH}x{set.FIANCATE_WIN_HEIGHT}")
        creator = WindowCreator(
            window,
            set.FIANCATE_SELECT_FIELDS,
            set.FIANCATE_INPUT_FIELDS
        )
        self.entries = creator.create_ui()

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

    def calculate(self, name):
        entries_dict = {
            key: entry.get() for key, entry in self.entries.items()
        }
        excel = ExcelFileHandler(name, entries_dict)
        cost, weight = excel.process_excel()

        result_window = tk.Toplevel(self.root)
        result_window.title("Risultato")  # Заголовок окна
        self.center_window(result_window, 300, 150)  # Центрируем окно

        # Формируем текст для отображения
        prezzo_text = (
            f"{set.PRICE}: {cost} €" if cost else set.PRICE_NOT_FOUND
        )
        peso_text = (
            f"{set.WEIGHT}: {weight} Kg" if weight else set.WEIGHT_NOT_FOUND
        )

        # Выводим текст
        tk.Label(
            result_window,
            text=prezzo_text,
            font=("Arial", 12)
        ).pack(pady=5)
        tk.Label(
            result_window,
            text=peso_text,
            font=("Arial", 12)
        ).pack(pady=5)

        # Кнопка "OK", которая закроет окно
        tk.Button(
            result_window,
            text="OK",
            command=result_window.destroy
        ).pack(pady=10)
