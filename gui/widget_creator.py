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
        select_fields : Dict[str: List[Any]]
            Поля для выбора из выпадающего списка.
        input_fields : List[Any]
            Поля для ручного ввода данных юзером.

    Methods
    -------
        create_ui()
            Раскидывает виджеты по окну.
        add_mm(frame, label, row)
            Добавляет единицы измерения.
    """
    def __init__(self, window: tk.Toplevel, type_choice: Dict) -> None:
        self.window = window
        self.type_choice = type_choice
        self.always_on: Dict = type_choice["always_on"]
        self.select_fields: Dict | None = None
        self.input_fields: Dict | None = None
        self.entries = {}
        self.frame = None
        self.frames = {}

    def create_ui(self) -> None:
        """Размещает виджеты на окне. Пользуется атрибутами класса. Виджеты
        меняются в зависимости от имени окна, для которого нужноих разместить.

        Return
        ______
            entries : tk.Entry
                Массив введенных пользователем значений
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

        self.create_main_frame(start_row)

    def create_main_frame(self, start_row: int) -> None:
        """Создаёт или перерисовывает `main_frame`."""
        if not self.select_fields or not self.input_fields:
            inizial_choice = None
            for value in self.always_on.values():
                if value:
                    inizial_choice = value[0]
                    break
            self.get_select_fields(inizial_choice)
            self.get_input_fields(inizial_choice)

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

        for i in range(set.COL_NUM):
            self.frame.columnconfigure(i, weight=set.GRID_WEIGHT)

    def on_dropdown_change(self, var: tk.StringVar) -> None:
        """Обрабатывает изменение первого выпадающего списка."""
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
        values: List[Any],
        row: int,
        is_entry: bool = False,
        is_changing: bool = False
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
        """

        # Создаём `Label`
        tk.Label(
            frame, text=label, bg=set.LABEL_BG_COLOR, width=15, anchor="w"
        ).grid(row=row, column=0, sticky="w", pady=2)

        if is_entry:
            entry = tk.Entry(frame, width=15)
            entry.grid(row=row, column=1, sticky="ew", padx=5)
            self.entries[label] = entry
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

    def create_invia_button(self, callback) -> None:
        btn_invia = tk.Button(
            self.window,
            text=set.BUTTON_INVIA_TITLE,
            width=set.BUTTON_WIDTH,
            bg=set.BUTTON_COLOR,
            relief=set.BUTTON_RELIEF,
            command=callback
        )
        btn_invia.pack(
            side=set.BUTTON_INVIA_SIDE,
            anchor=set.BUTTON_INVIA_ANCHOR,
            padx=set.BUTTON_PADX,
            pady=set.BUTTON_PADY
        )

    def get_select_fields(self, choice):
        self.select_fields = Translator().translate_dict(
            self.type_choice["choices"][choice]["available_params"]["select"]
        )

    def get_input_fields(self, choice):
        self.input_fields = (
            self.type_choice["choices"][choice]["available_params"]["input"]
        )
