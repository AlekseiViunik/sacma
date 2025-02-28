import tkinter as tk

from gui.helper import Helper
from gui.window_creator import WindowCreator
from logic.excel_file_handler import ExcelFileHandler
from logic.logger import logger as log
from settings import settings as set
from .abstract_type_class import AbstractTypeClass


class Travi(AbstractTypeClass):
    def __init__(self, root, name):
        self.root = root
        self.name = name
        self.window_width = set.TRAVI_WIN_WIDTH
        self.window_height = set.TRAVI_WIN_HEIGHT
        self.type_choice = set.TRAVI_CHOICE

    def open_window(self):
        log.info(f"Button {self.name} is pressed.")
        self.root.withdraw()
        self.window = tk.Toplevel(self.root)
        self.window.title(self.name)
        self.window.geometry(f"{self.window_width}x{self.window_height}")
        self.center_window(self.window_width, self.window_height)
        self.create_components()

        btn_invia = tk.Button(
            self.window,
            text=set.BUTTON_INVIA_TITLE,
            width=set.BUTTON_WIDTH,
            bg=set.BUTTON_COLOR,
            relief=set.BUTTON_RELIEF,
            command=self.calculate
        )
        btn_invia.pack(
            side=set.BUTTON_INVIA_SIDE,
            anchor=set.BUTTON_INVIA_ANCHOR,
            padx=set.BUTTON_PADX,
            pady=set.BUTTON_PADY
        )

        self.window.protocol(
            set.ON_CLOSING_WINDOW,
            lambda: Helper(self.root).on_close(self.window)
        )

    def create_components(self):
        creator = WindowCreator(
            self.window,
            self.type_choice[set.TRAVI_TYPE_TG]['select'],
            self.type_choice[set.TRAVI_TYPE_TG]['input'],
            self.type_choice['always_on'],
        )
        creator.create_ui()
        self.entries = creator.entries

    def calculate(self):
        entries_dict = {
            key: entry.get() for key, entry in self.entries.items()
        }
        log.info(f"Entries: {entries_dict}")
        excel = ExcelFileHandler(self.name, entries_dict)
        cost, weight = excel.process_excel()
        self.open_response_window(cost, weight)

    def open_response_window(self, cost, weight):
        result_window = tk.Toplevel(self.root)
        result_window.title("Risultato")  # Заголовок окна
        self.center_window(300, 150, result_window)  # Центрируем окно

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
            width=set.BUTTON_WIDTH,
            bg=set.BUTTON_COLOR,
            text="OK",
            command=result_window.destroy
        ).pack(pady=10)
