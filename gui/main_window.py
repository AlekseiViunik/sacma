import inspect
import math
import tkinter as tk

from logic.logger import logger as log
from logic.excel_file_handler import ExcelFileHandler
from settings import settings as set
from .window_creator import WindowCreator


class App:
    """Класс App используется для создания основного окна.

    Основное применение - создание главного окна приложения и его кнопок,
    Запус процесса обработки входных данных и вывод результата в отдельном
    окне. Во время инициализации сразу же вызывает метод раскидывания виджетов
    по окну.

    Attributes
    ----------
    root : tk.Tk
        Главное окно.
    entries : Dict
        список введенных значений.
    buttons : List[String]
        список кнопок, размещаемых на главном окне.

    Methods
    -------
    create_widgets()
        Раскидывает виджеты по окну.
    open_window(name)
        Открывает второстепенное окно с базовыми виджетами, одинаковыми для
        всех такого рода окон.
    create_travi_ui(window)
        Наполняет открытое второстепенное окно характерными для этого типа
        окна виджетами.
    create_fiancate_ui(window)
        Наполняет открытое второстепенное окно характерными для этого типа
        окна виджетами.
    on_close(window)
        Обрабатывает кастомным образом закрытие передаваемого окна.
    center_window(window, width, height)
        Wtynhbhetn окно относительно экрана.
    calculate(name)
        Запускает процесс обработки введенных данных и возвращает результат.
    """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.resizable(False, False)
        self.entries = {}
        self.root.title(f"{set.MAIN_WIN_TITLE}")
        self.root.geometry(f"{set.MAIN_WIN_WIDTH}x{set.MAIN_WIN_HEIGHT}")
        self.center_window(self.root, set.MAIN_WIN_WIDTH, set.MAIN_WIN_HEIGHT)
        self.buttons = set.MAIN_WIN_BUTTONS

        self.create_widgets()

    def create_widgets(self) -> None:
        """Создает виджеты для главного окна. Сами виджеты подразумевают под
        собой фреймы, кнопки, лейблы. Вызывать не надо - вызывается
        автоматически."""

        log.info("Create widgets on main window")
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

    def open_window(self, name: str) -> None:
        """Открывает базу второстепенного окна фреймом и кнопкой Invia.
        В зависимости от того, какая кнопка была нажата, вызывает частный
        вспомогательный метод для отрисовки компонентов.

        Parameters
        ----------
            name: str
                Имя окна. От него же зависит начинка окна виджетами.
        """

        log.info(f"Button {name} is pressed.")
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
        log.info(f"The method '{method_name}' is called")

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
            width=set.BUTTON_WIDTH,
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

    def create_travi_ui(self, window: tk.Toplevel) -> None:
        """Частный случай отрисовки компонентов для конкретного окна (в данном)
        случае, если была нажата кнопка Travi.

        Parameters
        ----------
            window: tk.Toplevel
                Окно, на котором будут размещаться компоненты.
        """

        window.geometry(f"{set.TRAVI_WIN_WIDTH}x{set.TRAVI_WIN_HEIGHT}")
        creator = WindowCreator(
            window,
            set.TRAVI_SELECT_FIELDS,
            set.TRAVI_INPUT_FIELDS,
            set.TRAVI_ALWAYS_ON
        )
        creator.create_ui()
        self.entries = creator.entries

    def create_fiancate_ui(self, window: tk.Toplevel) -> None:
        """Частный случай отрисовки компонентов для конкретного окна (в данном)
        случае, если была нажата кнопка Fiancate.

        Parameters
        ----------
            window: tk.Toplevel
                Окно, на котором будут размещаться компоненты.
        """

        window.geometry(f"{set.FIANCATE_WIN_WIDTH}x{set.FIANCATE_WIN_HEIGHT}")
        creator = WindowCreator(
            window,
            set.FIANCATE_SELECT_FIELDS,
            set.FIANCATE_INPUT_FIELDS,
            set.FIANCATE_ALWAYS_ON
        )
        self.entries = creator.create_ui()

    def on_close(self, window: tk.Toplevel) -> None:
        """Обрабатывает закрытие переданного окна:
        1. Закрывает текущее окно,
        2. Возвращает скрытое главное окно.

        Parameters
        ----------
            window: tk.Toplevel
                Закрываемое окно.
        """
        window.destroy()
        self.root.deiconify()  # вернуть главное окно

    def center_window(
        self,
        window: tk.Toplevel,
        width: int,
        height: int
    ) -> None:
        """Центрирует расположение открываемого окна относительно экрана
        компьютера.

        Parameters
        ----------
            window: tk.Toplevel
                Центрируемое окно.
            width: int
                Ширина окна.
            Height: int
                Высота окна.
        """
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def calculate(self, name: str) -> None:
        """Запускает процесс обработки введенных данных и по окончании
        открывает окно с результатами.

        Parameters
        ----------
            name: String
                Имя нажатой на главном окне кнопки и, по совместительству,
                открытого нажатием этой кнопки окна.
        """
        log.info(
            f"The metod '{inspect.currentframe().f_code.co_name}' is called"
        )
        entries_dict = {
            key: entry.get() for key, entry in self.entries.items()
        }
        log.info(f"Entries: {entries_dict}")
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
            width=set.BUTTON_WIDTH,
            bg=set.BUTTON_COLOR,
            text="OK",
            command=result_window.destroy
        ).pack(pady=10)
