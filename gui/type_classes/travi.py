import tkinter as tk

from gui.helper import Helper
from gui.widget_creator import WidgetCreator
from logic.excel_file_handler import ExcelFileHandler
from logic.logger import logger as log
from settings import settings as set
from abstract_base_type import AbstractBaseType


class Travi(AbstractBaseType):
    def __init__(self, root, type):
        super().__init__(root, type)

    def create_components(self):
        select_options, input_options, always_on = (
            (
                self.get_default_options(set.TRAVI_TYPE_TG, option) for
                option in ["select", "input", "always_on"]
            )
        )

        creator = WidgetCreator(
            self.window,
            select_options,
            input_options,
            always_on,
        )
        creator.create_ui()
        self.entries = creator.entries

        creator.create_invia_button(self.calculate)

        self.window.protocol(
            set.ON_CLOSING_WINDOW,
            lambda: Helper(self.root).on_close(self.window)
        )

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
