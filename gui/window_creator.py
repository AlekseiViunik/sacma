import tkinter as tk

from typing import Dict, List, Any

from settings import settings as set


class WindowCreator:
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
    def __init__(
        self,
        window: tk.Toplevel,
        select_fields: Dict[str, List[Any]],
        input_fields: List[Any],
        always_on: Dict[str, List[Any]] | List[Any]
    ) -> None:
        self.window = window
        self.select_fields = select_fields
        self.input_fields = input_fields
        self.always_on = always_on
        self.entries = {}
        self.frame = None

    def create_ui(self) -> tk.Entry:
        """Размещает виджеты на окне. Пользуется атрибутами класса. Виджеты
        меняются в зависимости от имени окна, для которого нужноих разместить.

        Return
        ______
            entries : tk.Entry
                Массив введенных пользователем значений
        """
        # ============================Always_on================================
        always_on_frame = tk.Frame(
            self.window,
            bg=set.FRAME_BG_COLOR,
            padx=set.FRAME_PADX,
            pady=set.FRAME_PADY
        )
        always_on_frame.pack(fill=tk.X, padx=5, pady=2)

        for i, (label, values) in enumerate(self.always_on.items()):
            if not values:
                continue
            tk.Label(
                always_on_frame,
                text=label,
                bg=set.LABEL_BG_COLOR,
                width=15,
                anchor='w'
            ).grid(
                row=i,
                column=set.LABEL_NAME_COLUMN,
                sticky=set.LABEL_STICKY,
                pady=set.LABEL_PADY
            )
            var = tk.StringVar(value=values[0])
            dropdown = tk.OptionMenu(always_on_frame, var, *values)
            dropdown.config(width=15)
            dropdown.grid(
                row=i,
                column=set.DROPDOWN_COLUMN,
                sticky=set.DROPDOWN_STICKY,
                padx=set.DROPDOWN_PADX
            )
            self.entries[label] = var
            self.add_mm(always_on_frame, label, i)

        start_row = len(self.always_on)
        for i in range(set.COL_NUM):
            always_on_frame.columnconfigure(i, weight=set.GRID_WEIGHT)

        self.frame = tk.Frame(
            self.window,
            bg=set.FRAME_BG_COLOR,
            padx=set.FRAME_PADX,
            pady=set.FRAME_PADY
        )
        self.frame.pack(fill=tk.X, padx=5, pady=2)

        # ================Поля с выпадающими списками==========================
        for i, (label, values) in enumerate(self.select_fields.items()):
            if not values:
                continue
            tk.Label(
                self.frame,
                text=label,
                bg=set.LABEL_BG_COLOR,
                width=15,
                anchor='w'
            ).grid(
                row=start_row + i,
                column=set.LABEL_NAME_COLUMN,
                sticky=set.LABEL_STICKY,
                pady=set.LABEL_PADY
            )
            var = tk.StringVar(value=values[0])
            dropdown = tk.OptionMenu(self.frame, var, *values)
            dropdown.config(width=15)
            dropdown.grid(
                row=start_row + i,
                column=set.DROPDOWN_COLUMN,
                sticky=set.DROPDOWN_STICKY,
                padx=set.DROPDOWN_PADX
            )
            self.entries[label] = var
            self.add_mm(self.frame, label, start_row + i)

        start_row += len(self.select_fields)  # Начинаем после селектов

        # ==================== Поля для ввода =================================
        for i, label in enumerate(self.input_fields):
            row = start_row + i
            tk.Label(
                self.frame,
                text=label,
                bg=set.LABEL_BG_COLOR,
                width=15,
                anchor='w'
            ).grid(
                row=row,
                column=set.LABEL_NAME_COLUMN,
                sticky=set.LABEL_STICKY,
                pady=set.LABEL_PADY
            )
            entry = tk.Entry(self.frame, width=15)
            entry.grid(
                row=start_row + i,
                column=set.ENTRY_COLUMN,
                sticky=set.ENTRY_STICKY,
                padx=set.ENTRY_PADX
            )
            self.entries[label] = entry
            self.add_mm(self.frame, label, row)

        # Настройка растяжения колонок
        for i in range(set.COL_NUM):
            self.frame.columnconfigure(i, weight=set.GRID_WEIGHT)

        return self.entries

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
