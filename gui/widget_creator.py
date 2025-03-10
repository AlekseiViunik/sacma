import tkinter as tk

from logic.logger import logger as log
from logic.translator import Translator
from settings import settings as set


class WidgetCreator:
    """Класс-помощник. Располагает виджеты на окнах.
    Attributes
    ----------
    window : tk.Toplevel
        Окно, с которым класс будет работать.
    type_choice : dict | None
        Набор параметров для выбранного типа элементов.
    always_on : dict | None
        Поля, которые не должны быть перерисованы в случае выбора других
        параметров.
    select_fields : dict | None
        Поля для выбора из выпадающего списка.
    input_fields : list | None
        Поля для ручного ввода данных юзером.
    entries : dict
        Список введенных пользователем значений.
    frame : tk.Frame
        Фрейм, в котором будут размещены виджеты.
    frames : dict
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
    create_component(
        frame, label, values, row, is_entry, is_changing, is_hide,
        default_value
    )
        Создаёт `Label` + `OptionMenu` или `Entry` для окна.
    create_button(name, callback, anchor)
        Создаёт кнопку "Invia" для окна.
    get_select_fields(choice)
        Получает параметры для полей с выпадающим списком.
    get_input_fields(choice)
        Получает параметры для полей ввода.
    """
    def __init__(
        self,
        window: tk.Toplevel | tk.Tk,
        type_choice: dict | None = None
    ) -> None:
        self.window = window
        self.type_choice = type_choice
        self.always_on: dict | None = (
            type_choice['always_on'] if type_choice else None
        )
        self.select_fields: dict | None = None
        self.input_fields: list | None = None
        self.entries: dict = {}
        self.frame: tk.Frame = None
        self.frames: dict = {}
        self.changing_frames_amount = 1

    def create_frames(self):
        if "changing_frames" in self.frames:
            for frame in self.frames['changing_frames'].values():
                frame.destroy()
            self.frames.pop("changing_frames")
        if "always_on" not in self.frames and self.always_on:
            frame = tk.Frame(
                self.window,
                bg=set.FRAME_BG_COLOR,
                padx=set.FRAME_PADX,
                pady=set.FRAME_PADY
            )
            frame.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
            self.frames['always_on'] = {}
            self.frames['always_on']['frame'] = frame
        frame_no = 1
        while frame_no <= self.changing_frames_amount:
            frame = tk.Frame(
                self.window,
                bg=set.FRAME_BG_COLOR,
                padx=set.FRAME_PADX,
                pady=set.FRAME_PADY
            )
            frame.grid(row=2, column=frame_no, padx=5, pady=2, sticky='ew')
            frame_name = f"frame{frame_no}"
            if "changing_frames" not in self.frames:
                self.frames['changing_frames'] = {}
            self.frames['changing_frames'][frame_name] = frame
            frame_no += 1

    def add_widgets_to_frames(self):
        for type, frames in self.frames.items():
            if type == "always_on":
                for i, (label, values) in enumerate(self.always_on.items()):
                    if values:
                        self.create_component(
                            frames['frame'],
                            label,
                            values,
                            i,
                            is_changing=True
                        )

                        for j in range(set.COL_NUM):
                            frames['frame'].columnconfigure(
                                j, weight=set.GRID_WEIGHT
                            )
            else:
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

                for frame in self.frames['changing_frames'].values():
                    start_row = 1
                    for i, (label, values) in enumerate(
                        self.select_fields.items()
                    ):
                        if values:
                            self.create_component(
                                self.frame, label, values, start_row + i
                            )

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
                    frames['frame1'].columnconfigure(i, weight=set.GRID_WEIGHT)

    def create_always_on(self) -> None:
        """
        Размещает фреймы с виджетами на окне. Пользуется атрибутами класса.
        Виджеты меняются в зависимости от имени окна, для которого нужноих
        разместить.
        """

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
        log.info("Always_on frame is created")
        return start_row

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
        log.info("Get initial params")
        if not self.select_fields or not self.input_fields:
            inizial_choice = None
            for value in self.always_on.values():
                if value:
                    inizial_choice = value[0]
                    break
            if not inizial_choice:
                inizial_choice = "standart"
            self.get_select_fields(inizial_choice)
            log.info(f"Select fields are: {self.select_fields}")
            self.get_input_fields(inizial_choice)
            log.info(f"Input fields are: {self.input_fields}")

        # Создаём или пересоздаём фрейм
        self.frame = self.create_frame("main_frame")
        log.info("Main frame is created!")

        # Поля с выпадающими списками
        log.info("Create choice widgets")
        for i, (label, values) in enumerate(self.select_fields.items()):
            if values:
                self.create_component(self.frame, label, values, start_row + i)

        start_row += len(self.select_fields)

        # Поля для ввода
        log.info("Create input widgets")
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

    def create_frame(self, frame_name: str) -> tk.Frame:
        """
        Создаёт или пересоздаёт фрейм.

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
        log.info(f"New choice has been selected: {new_choice}")
        if not new_choice.isnumeric():
            log.info("It is not numeric. So rerender the main frame")
            self.get_select_fields(new_choice)
            self.get_input_fields(new_choice)
            # ✅ Перерисовываем `main_frame`
            self.create_main_frame(start_row=len(self.always_on))

    def add_mm(self, frame: tk.Frame, label: str, row: int) -> None:
        """
        Добавляет в конце поля для ввода или для выбора лейбл с единицей
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
        """
        Создаёт `Label` + `OptionMenu` или `Entry` для окна.

        Parameters
        ----------
        frame : tk.Frame
            Фрейм, в котором создаётся элемент.
        label : str
            Текст лейбла.
        values : list
            Список значений для `OptionMenu` (если это `Entry`, передаём `[]`).
        row : int
            Номер строки в `grid()`.
        is_entry : bool, optional
            Если `True`, создаёт `Entry` (по умолчанию `False`).
        is_changing : bool, optional
            Если `True`, добавляет слежение за изменением значения
            `OptionMenu` (по умолчанию `False`).
        is_hide : bool, optional
            Если `True`, маскирует вводимые в поле символы (по умолчанию
            False).
        defailt_value : str, optional
            Значение, уже присутствующее в поле для ввода.
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

    def create_button(
        self,
        name: str,
        callback: callable,
        anchor: str | None = None
    ) -> None:
        """
        Создаёт кнопку для окна, нажатие которой запускает
        процесс, определенный для этой кнопки.

        Parameters
        ----------
        name : str
            Имя кнопки
        callback : callable
            Функция, которая будет вызвана при нажатии на кнопки.
        anchor : str | None, optional
            Привязка кнопки к краю окна.
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
            self.type_choice['choices'][choice]['available_params']['select']
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
            self.type_choice['choices'][choice]['available_params']['input']
        )
