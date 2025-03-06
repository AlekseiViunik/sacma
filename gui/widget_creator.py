import tkinter as tk

from typing import Dict, List, Any

from logic.translator import Translator
from settings import settings as set


class WidgetCreator:
    """Класс-помощник. Располагает виджеты на окнах.
    Attributes
    ----------
    window : tk.Toplevel
        Окно, с которым класс будет работать.
    type_choice : Dict
        Набор параметров для выбранного типа элементов.
    always_on : Dict[str: List[str]]
        Поля, которые не должны быть перерисованы в случае выбора других
        параметров.
    select_fields : Dict[str: List[Any]]
        Поля для выбора из выпадающего списка.
    input_fields : List[Any]
        Поля для ручного ввода данных юзером.
    entries : Dict[str: tk.Entry]
        Список введенных/выбранных пользователем значений.
    frame : tk.Frame
        Фрейм, в котором будут размещены виджеты.
    frames : Dict[str: tk.Frame]
        Словарь с фреймами. Для понимания, надо ли удалять фрейм перед его
        отрисовкой, или он уже отрисован.

    Methods
    -------
    create_ui()
        Раскидывает виджеты по окну.
    create_main_frame(start_row)
        Получает параметры главного фрейма и создаёт или перерисовывает
        его.
    on_dropdown_change(var)
        Обрабатывает изменение первого выпадающего списка.
    add_mm(frame, label, row)
        Добавляет в конце поля для ввода или для выбора лейбл с единицей
        измерения текущего параметра (по умолчанию 'мм').
    create_frame(frame_name)
        Создаёт или пересоздаёт фрейм с заданными параметрами.
    create_component(frame, label, values, row, is_entry, is_changing)
        Создаёт `Label` + `OptionMenu` или `Entry` для окна.
    create_invia_button(callback)
        Создаёт кнопку "Invia" для окна.
    get_select_fields(choice)
        Получает параметры для полей с выпадающим списком.
    get_input_fields(choice)
        Получает параметры для полей ввода.
    """
    def __init__(
        self,
        window: tk.Toplevel | tk.Tk,
        type_choice: dict | None
    ) -> None:
        self.window = window
        self.type_choice = type_choice
        self.always_on: Dict[str, List[str]] = (
            type_choice["always_on"] if type_choice else None
        )
        self.select_fields: Dict[str, Any] | None = None
        self.input_fields: Dict[str, Any] | None = None
        self.entries: Dict[str, tk.Entry] = {}
        self.frame: tk.Frame = None
        self.frames: Dict[str, tk.Frame] = {}

    def create_ui(self) -> None:
        """
        Размещает фреймы с виджетами на окне. Пользуется атрибутами класса.
        Виджеты меняются в зависимости от имени окна, для которого нужноих
        разместить.
        """

        # ============================Always_on================================
        always_on_frame = self.create_frame("always_on_frame")
        for i, (label, values) in enumerate(self.always_on.items()):
            if values:
                self.create_component(
                    always_on_frame,
                    label, values,
                    i,
                    is_changing=True
                )

        start_row = len(self.always_on)

        for i in range(set.COL_NUM):
            always_on_frame.columnconfigure(i, weight=set.GRID_WEIGHT)
        # ============================Main_frame================================
        self.create_main_frame(start_row)

    def create_main_frame(self, start_row: int) -> None:
        """
        Создаёт или перерисовывает главный фрейм. Сначала создает поля с
        выпадающими списками, затем поля для ввода данных.

        Parameters
        ----------
        start_row : int
            Номер строки сетки, с которой начнется размещение виджетов.
        """
        # Если виджет отрисовывается первый раз, получаем параметры
        if not self.select_fields or not self.input_fields:
            inizial_choice = None
            for value in self.always_on.values():
                if value:
                    inizial_choice = value[0]
                    break
            if not inizial_choice:
                inizial_choice = "standart"
            self.get_select_fields(inizial_choice)
            self.get_input_fields(inizial_choice)

        # Создаём или пересоздаём фрейм
        self.frame = self.create_frame("main_frame")

        # Поля с выпадающими списками
        for i, (label, values) in enumerate(self.select_fields.items()):
            if values:
                self.create_component(self.frame, label, values, start_row + i)

        start_row += len(self.select_fields)

        # Поля для ввода
        for i, label in enumerate(self.input_fields):
            self.create_component(
                self.frame,
                label,
                [],
                start_row + i,
                is_entry=True
            )

        # Конфигурируем сетку
        for i in range(set.COL_NUM):
            self.frame.columnconfigure(i, weight=set.GRID_WEIGHT)

    def on_dropdown_change(self, var: tk.StringVar) -> None:
        """
        Обрабатывает изменение первого выпадающего списка.
        Если выбор изменился, перерисовывает главный фрейм.

        Parameters
        ----------
        var : tk.StringVar
            Новое значение выпадающего списка.
        """
        new_choice = var.get()
        self.get_select_fields(new_choice)
        self.get_input_fields(new_choice)

        # ✅ Перерисовываем `main_frame`
        self.create_main_frame(start_row=len(self.always_on))

    def add_mm(self, frame: tk.Frame, label: str, row: int) -> None:
        """Добавляет в конце поля для ввода или для выбора лейбл с единицей
        измерения текущего параметра (по умолчанию 'мм').

        Parameters
        ----------
            frame : tk.Frame
                Фрейм, в котороом будет размещаться текущий лейбл.
            label : String
                Имя лейбла, по которому метод определяет, нужно ли ему
                добавлять единицы измерения в конце.
            row : int
                Номер строки в сетке расположения виджетов, в которой
                расположен текущий лейбл.
        """

        if label in set.dimensions_need_mm:
            tk.Label(
                frame,
                text=set.LABEL_MM_TEXT,
                bg=set.LABEL_BG_COLOR
            ).grid(
                row=row,
                column=set.LABEL_MM_COLUMN,
                sticky=set.LABEL_STICKY
            )
        else:
            tk.Label(
                frame,
                text=set.LABEL_MM_TEXT,
                bg=set.LABEL_BG_COLOR,
                fg=set.LABEL_BG_COLOR
            ).grid(
                row=row,
                column=set.LABEL_MM_COLUMN,
                sticky=set.LABEL_STICKY
            )

    def create_frame(self, frame_name: str) -> tk.Frame:
        """Создаёт или пересоздаёт фрейм.

        Parameters
        ----------
        frame_name : str
            Название фрейма.

        Returns
        -------
        tk.Frame
            Созданный фрейм.
        """
        # Если фрейм уже существует, удаляем его
        if frame_name in self.frames:
            self.frames[frame_name].destroy()

        # Создаём новый фрейм
        frame = tk.Frame(
            self.window,
            bg=set.FRAME_BG_COLOR,
            padx=set.FRAME_PADX,
            pady=set.FRAME_PADY
        )
        frame.pack(fill=tk.X, padx=5, pady=2)

        self.frames[frame_name] = frame  # Сохраняем ссылку
        return frame

    def create_component(
        self,
        frame: tk.Frame,
        label: str,
        values: list | None,
        row: int,
        is_entry: bool = False,
        is_changing: bool = False,
        is_hide: bool = False,
        default_value: str = ""
    ) -> None:
        """Создаёт `Label` + `OptionMenu` или `Entry` для окна.

        Parameters
        ----------
        frame : tk.Frame
            Фрейм, в котором создаётся элемент.
        label : str
            Текст лейбла.
        values : List[Any]
            Список значений для `OptionMenu` (если это `Entry`, передаём `[]`).
        row : int
            Номер строки в `grid()`.
        is_entry : bool, optional
            Если `True`, создаёт `Entry` (по умолчанию `False`).
        is_changing : bool, optional
            Если `True`, добавляет слежение за изменением значения
            `OptionMenu` (по умолчанию `False`).
        """

        # Создаём `Label`
        tk.Label(
            frame, text=label, bg=set.LABEL_BG_COLOR, width=15, anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=2)

        if is_entry:
            entry_var = tk.StringVar(value=default_value)
            entry = tk.Entry(frame, width=15, textvariable=entry_var)
            if is_hide:
                entry.config(show="*")
            entry.grid(row=row, column=1, sticky="ew", padx=5)
            self.entries[label] = entry_var
        else:
            var = tk.StringVar(value=values[0])
            dropdown = tk.OptionMenu(frame, var, *values)
            dropdown.config(width=15)
            dropdown.grid(row=row, column=1, sticky="ew", padx=5)
            self.entries[label] = var
            if is_changing:
                var.trace_add("write", lambda *_: self.on_dropdown_change(var))

        # Добавляем "мм", если нужно
        self.add_mm(frame, label, row)

    def create_button(self, name, callback: callable, anchor=None) -> None:
        """
        Создаёт кнопку "Invia" для окна, нажатие которой запускает
        процесс расчетов через excel файл искомых значений и вывода
        результата на экран путем открытия нового окна.

        Parameters
        ----------
        callback : callable
            Функция, которая будет вызвана при нажатии на кнопки.
        """

        button = tk.Button(
            self.window,
            text=name,
            width=set.BUTTON_WIDTH,
            bg=set.BUTTON_COLOR,
            relief=set.BUTTON_RELIEF,
            command=callback
        )
        button.pack(
            side=set.BUTTON_INVIA_SIDE,
            anchor=set.BUTTON_INVIA_ANCHOR if not anchor else anchor,
            padx=set.BUTTON_PADX,
            pady=set.BUTTON_PADY
        )

    def get_select_fields(self, choice: str) -> None:
        """
        Получает параметры для полей с выпадающим списком.

        Parameters
        ----------
        choice : str
            Выбор, произведенный в always_on выпадающем списке.
        """
        self.select_fields = Translator().translate_dict(
            self.type_choice["choices"][choice]["available_params"]["select"]
        )

    def get_input_fields(self, choice: str) -> None:
        """
        Получает параметры для полей ввода.

        Parameters
        ----------
        choice : str
            Выбор, произведенный в always_on выпадающем списке.
        """
        self.input_fields = (
            self.type_choice["choices"][choice]["available_params"]["input"]
        )
