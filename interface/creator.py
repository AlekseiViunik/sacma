from typing import Dict, List, Tuple
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from helpers.remover import Remover
from helpers.finder import Finder
from logic.logger import logger as log


class Creator:
    """
    Один из главных классов приложения. Отвечает за создание и размещение
    виджетов и контейнеров на окне. Также перерисовывает их при изменении
    указанных в конфиге параметров.

    Attributes
    ----------
    - config: dict
        Данные JSON файла с конфигурацией текущего окна.

    - parent_window: QWidget
        Класс окна, на котором мы размещаем виджеты.

    - input_fields: Dict[str, QLineEdit]
        Словарь с именем полей для ввода и их объектами, расположенных в
        текущем окне.

    - chosen_fields: Dict[str, QComboBox]
        Словарь с именем полей для выбора и их объектами, расположенных в
        текущем окне.

    - default_values: Dict[str, str]
        Помощник, отвечающий за авторизацию и создание юзеров.

    - current_changing_value: str | None
        Текущее значение, которое меняет расположение виджетов.

    - current_changing_values: Dict[str, str]
        Словарь текущих значений, меняющих расположение виджетов.

    - remover: Remover
        Класс-удалитель.

    - finder: Finder
        Класс-находитель.

    - mandatory_fields: List[str]
        Поля, обязательные для заполнения.

    - dependencies: dict
        Словарь зависимых контейнеров, которые будут меняться в зависимости от
        того, какое поле было выбрано.

    - layout_parents: dict
        Словрь, который в качестве ключей содержит текущий контйенер,
        а значений - родительский. Нужен для четкого определения родителя
        при перерисовке контейнера.

    Methods
    -------
    - create_widget_layout()
        Создает контейнер для размещения виджетов и раполагает его на текущем
        окне или другом контейнере.

    Private methods
    ---------------
    - __add_widgets(layout, layout_type, widgets_configs, columns)
        Инициирует процесс проверки активности виджета и его создания.
        Располагает виджет на контейнере.

    - __create_widget(config, layout, row, column)
        В зависимости от типа виджета (взятого из его конфига), вызывает
        соответствующий метод создания виджета и возвращает созданный виджет.
        Если вместо виджета передан контейнер, вызывает заново метод
        create_widget_layout().

    - __create_layout(layout_config)
        Создает и возвращает объект контейнера в зависимости от его типа,
        указанного в его конфиге.

    - __create_label(config)
        Создает, настраивает по переданному конфигу и возвращает виджет типа
        QLabel.

    - __create_input(config)
        Создает, настраивает по переданному конфигу и возвращает виджет типа
        QLineEdit.

    - __create_checkbox(config)
        Создает, настраивает по переданному конфигу и возвращает виджет типа
        QCheckBox.

    - __create_button(config)
        Создает, настраивает по переданному конфигу и возвращает виджет типа
        QPushButton.

    - __create_dropdown(config)
        Создает, настраивает по переданному конфигу и возвращает виджет типа
        QComboBox.

    - __get_widget_pos(current_row, current_col, col_amount, widget_pos)
        Виджеты, располоагающиеся на контейнере типа "сетка", имеют в конфиге
        указание по своему расположению в строке. В зависимости от этого
        параметра высчитываем новые координаты виджета в сетке.

    - __update_dependent_layouts(name, selected_value)
        Обновляет окно при выборе другого значения, которое меняет расположение
        виджетов.

    - __check_if_widget_is_active(config)
        Проверяет, активен ли виджет при текщих изменяющих значениях.
        Необходимо, чтобы понять, стоит ли отрисовывать его.
    """

    def __init__(
        self,
        config: dict,
        parent_window: QWidget
    ) -> None:
        self.config: dict = config
        # Нужно для привязки колбэка. Тут тоже должен быть BaseWindow,
        # но из-за зацикливания ссылок друг на друге, я не могу его тут
        # указать.
        self.parent_window: QWidget = parent_window

        self.input_fields: Dict[str, QLineEdit] = {}
        self.chosen_fields: Dict[str, QComboBox] = {}
        self.default_values: Dict[str, str] = {}
        self.current_changing_value: str | None = None
        self.current_changing_values: Dict[str, str] = {}
        self.remover: Remover = Remover()
        self.finder: Finder = Finder()
        self.mandatory_fields: List[str] = []
        self.main_layout = None

        # Словрь, который в качестве ключей содержит имя виджета, от выбора
        # которого зависят другие виджеты, а значений - словарь с именем
        # зависимого виджета и самим виджетом. Нужен для последующего поиска
        # всех зависимых виджетов и их перерисовке при изменении значения
        # изменяющего виджета.
        self.dependencies: dict = {}

        # Словрь, который в качестве ключей содержит текущий контйенер,
        # а значений - родительский. Нужен для четкого определения родителя
        # при перерисовке контейнера.
        self.layout_parents: dict = {}

    def create_widget_layout(
        self,
        parent_window: QHBoxLayout | QVBoxLayout | QGridLayout | QWidget,
        layout_config: dict | None
    ) -> None:
        """
        Основной метод. Создает контейнер для размещения виджетов. И
        располагает его на окне или другом контейнере.
        Тут зачем-то организована проверка проверка на существование контейнера
        с таким же именем среди зависимых. Это странно, потому что метод
        вызывается только при первичном создании контейнеров. Возможно, эту
        проверку надо будет удалить.

        Parameters
        ----------
        - parent_window: QHBoxLayout | QVBoxLayout | QGridLayout | QWidget
            Окно или контейнер. на котором должен быть размещен текущий
            контейнер. От этого зависит, какой метод использовать для
            размещения контейнера.

        - layout_config: dict | None
            Конфиг контейнера.
        """

        # Удаляем старый контейнер, если такой уже существует.
        # Если это зависимый контейнер, то
        if layout_config.get('depends_on'):

            # Берем имя виджета, от которого он зависит и присваиваем его
            # значение из default_values в current_changing_value
            self.current_changing_value = self.default_values[
                layout_config['depends_on']
            ]

            # И добавляем связку "Имя виджета - его текущее значение" в
            # словарь изменяющих виджетов (или обновляем уже существующую
            # запись)
            self.current_changing_values[layout_config['depends_on']] = (
                self.current_changing_value
            )

            # TODO Если удаление контейнера тут не нужно, то убрать проверку на
            # существование уже созданного контейнера с таким именем.
            # Если по каким-то причинам (уже не помню, зачем добавил эту
            # проверку тут) зависимый контейнер с таким именем уже существует,
            if (
                layout_config['depends_on'] in self.dependencies and
                self.dependencies[
                    layout_config['depends_on']
                ].get(layout_config['name'])
            ):
                # Удаляем существующий контейнер.
                self.remover.delete_layout(
                    parent_window,
                    self.dependencies[
                        layout_config['depends_on']
                    ][layout_config['name']]
                )
        # Вызываем метод создания самого контейнера по конфигу.
        layout = self.__create_layout(layout_config)

        # Добавляем туда виджеты
        self.__add_widgets(
            layout,
            layout_config['type'],
            layout_config['widgets'],
            layout_config.get('columns')
        )

        # Если текущий контейнер должен быть размещен на другом контейнере
        if (
            isinstance(parent_window, QHBoxLayout) or
            isinstance(parent_window, QVBoxLayout) or
            isinstance(parent_window, QGridLayout)
        ):

            parent_window.addLayout(layout)

            # Записываем в layout_parents родителя для добавленного контейнера.
            self.layout_parents[layout] = parent_window

        # Если текущий контейнер должен быть размещен на окне (QWidget)
        else:

            parent_window.setLayout(layout)
            self.main_layout = layout
            self.layout_parents[layout] = parent_window
            parent_window.adjustSize()

    def __add_widgets(
        self,
        layout: QHBoxLayout | QVBoxLayout | QGridLayout,
        layout_type: str,
        widgets_configs: List[dict],
        columns: int | None = None
    ) -> None:
        """
        Создает и располагает виджеты в контейнере в зависимости от его типа.
        Порядок такой:
        1. Если контейнер типа сетка, то:
        - Проверяет виджет на активность, вызывая __check_if_widget_is_active.
        - Высчитывает его координаты в сетки вызывая __get_widget_pos.
        - Создает виджет по его конфигу, вызывая __create_widget.
        - Располагает виджет в контейнере по высчитанным координатам.

        2. Если контейнер другого типа, то:
        - Проверяет виджет на активность, вызывая __check_if_widget_is_active.
        - Создает виджет по его конфигу, вызывая __create_widget.
        - Располагает виджет в контейнере.

        Parameters
        ----------
        - layout: QHBoxLayout | QVBoxLayout | QGridLayout
            Объект контейнера, на котором должны быть размещены виджеты.

        - layout_type: str
            Тип контейнера (берется из конфига)

        - widgets_configs: List[dict]
            Список конфигов всех виджетов, которые должны быть размещены в
            контейнере в порядке их перечисления в списке.

        - columns: int | None
            Только для виджета типа "сетка". Количество колонок, которое должно
            быть в сетке.
        """

        # Смотрим, в каком типе контейнера должны быть размещены виджеты.
        # Разница только в том, что если тип - сетка, то надо будет еще
        # высчитать координаты расположения виджета в сетке.
        # TODO Избавиться от layout_type. Использовать тип оюъекта вместо
        # этого
        match layout_type:

            # Если сетка
            case "grid":

                # Задаем начальные координаты для виджетов.
                current_row = 0
                current_column = 0

                # Пробегаемся по конфигу каждого виджета.
                for widget_config in widgets_configs:

                    # Если виджет не активен для текущего выбора изменяющих
                    # полей, пропускаем его.
                    if not self.__check_if_widget_is_active(widget_config):
                        continue

                    # Высчитываем координаты для виджета в зависимости от его
                    # предпочтения в конфиге.
                    current_row, current_column = self.__get_widget_pos(
                        current_row,
                        current_column,
                        columns,
                        widget_config.get('column')
                    )

                    # Вызываем метод создания виджета.
                    widget = self.__create_widget(
                        widget_config,
                        layout
                    )

                    # Добавляем виджет в контейнер.
                    layout.addWidget(
                        widget,
                        current_row,
                        current_column
                    )

                    # Переходим к следующей колонке.
                    current_column = current_column + 1

            # Если не сетка
            case "vertical" | "horizontal":

                # Пробегаемся по конфигу каждого виджета.
                for widget_config in widgets_configs:

                    # Если виджет не активен для текущего выбора изменяющих
                    # полей, пропускаем его.
                    if not self.__check_if_widget_is_active(widget_config):
                        continue

                    # Вызываем метод создания виджета.
                    widget = self.__create_widget(widget_config, layout)
                    if widget:
                        # Добавляем виджет в контейнер без координат.
                        layout.addWidget(widget)

    def __create_widget(
        self,
        config: dict,
        layout: QHBoxLayout | QVBoxLayout | QGridLayout | None = None,
    ) -> QLabel | QLineEdit | QCheckBox | QPushButton | QComboBox | None:
        """
        Создает виджет по его конфигу. Для каждого типа виджетов вызывает свой
        метод создания. Если конфиге оказался контейнер, вызывает метод
        создания контейнера вместо этого.
        На данный момент поддерживается 5 типов виджетов:
        Лейбл, Поле для ввода, Поле для выбора, Чекбокс, Кнпока.

        Parameters
        ----------
        - config: dict
            Конфиг, по которому будет создаваться и настраиваться виджет.

        - layout: QHBoxLayout | QVBoxLayout | QGridLayout | None = None
            Контейнер, на котором виджет будет располгаться.

        Returns
        -------
        - widget: (
            QLabel | QLineEdit | QCheckBox | QPushButton | QComboBox | None
        )
            Возвращает созданный и сконфигурированный объект виджета.
        """

        # Если в конфиге есть ключ "layout", то
        if config.get('layout'):

            # Вызываем основной метод создания контейнера.
            self.create_widget_layout(
                layout,
                config['layout']
            )
        # Если это все-таки виджет, то
        else:
            # Вызываем соответствующий виджет, в зависимости от его типа,
            # прописанного в конфиге.
            match config.get('type'):
                case "label":
                    widget = self.__create_label(config)
                case "input":
                    widget = self.__create_input(config)
                case "button":
                    widget = self.__create_button(config)
                case "dropdown":
                    widget = self.__create_dropdown(config)
                case "checkbox":
                    widget = self.__create_checkbox(config)
                case _:
                    widget = None
            # Возвращаем созданный и сконфигурированный виджет.
            return widget

    def __create_layout(
        self,
        layout_config: dict
    ) -> QHBoxLayout | QVBoxLayout | QGridLayout | None:
        """
        Создает контейнер по его конфигу и возвращает его.

        Parameters
        ----------
        - layout_config: dict
            Конфиг, по которому будет создан и сконфигурирован контейнер.
        Returns
        -------
        - layout: QHBoxLayout | QVBoxLayout | QGridLayout | None:
            Объект созданного контейнера
        """

        log.info(f"Create a layout. Type {layout_config['type']}")
        match layout_config["type"]:
            case "grid":
                layout = QGridLayout()
            case "vertical":
                layout = QVBoxLayout()
            case "horizontal":
                layout = QHBoxLayout()

        # Простая проверка if layout тут не подойдет. Почему - хз, видимо,
        # потому что сам объект пустой пока
        # Видимо, эта проверка нужна, чтобы понять, удалось ли создать
        # контейнер.
        if isinstance(layout, (QGridLayout, QVBoxLayout, QHBoxLayout)):

            # Если контейнер зависим, то записываем/перезаписываем его как
            # словарь типа "имя контейнера - объект контейнера" в словарь по
            # ключу, которым явяляется имя контейнера, от которого он зависит.
            if 'depends_on' in layout_config:
                self.dependencies.setdefault(
                    layout_config['depends_on'], {}
                )[layout_config['name']] = layout

            return layout
        return None

    def __create_label(self, config: dict) -> QLabel:
        """
        Создает, конфигурирует и возвращает объект лейбла.

        Parameters
        ----------
        - config: dict
            Конфиг, по которому будет создан и сконфигурирован лейбл.

        Returns
        -------
        label: QLabel
            Объект созданного лейбла
        """

        log.info(f"Create label: {config['text']}")
        label = QLabel()
        for param, value in config.items():
            match param:
                case "text":
                    label.setText(value)
                case "text_size":
                    font = QFont()
                    font.setPointSize(config['text_size'])
                    label.setFont(font)
                case "align":
                    # Определяет расположение текста внутри лейбла.
                    if config['align'] == "center":
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    if config['align'] == "left":
                        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                    if config['align'] == "right":
                        label.setAlignment(Qt.AlignmentFlag.AlignRight)
                case "mandatory":
                    # Добавляет звездочку в начале текста, если в конфиге
                    # Лейбл помечен как обязательный.
                    text = f"*{config['text']}"
                    label.setText(text)
                    self.mandatory_fields.append(config['mandatory'])
        return label

    def __create_input(self, config: dict) -> QLineEdit:
        """
        Создает, конфигурирует и возвращает объект поля для ввода.

        Parameters
        ----------
        - config: dict
            Конфиг, по которому будет создано и сконфигурировано поле для
            ввода.

        Returns
        -------
        label: QLineEdit
            Объект созданного поля для ввода.
        """

        log.info("Create input field")
        input_field = QLineEdit()
        for param, value in config.items():
            match param:
                case "width":
                    input_field.setFixedWidth(int(value))
                case "height":
                    input_field.setFixedHeight(int(value))
                case "default_value":
                    input_field.setPlaceholderText(value)
                case "hide":
                    # Прячет вводимые символы (для чувствительных данных).
                    input_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_fields[config['name']] = input_field
        return input_field

    def __create_checkbox(self, config: dict) -> QCheckBox:
        """
        Создает, конфигурирует и возвращает объект чекбокса.

        Parameters
        ----------
        - config: dict
            Конфиг, по которому будет создан и сконфигурирован чекбокс.

        Returns
        -------
        label: QCheckBox
            Объект созданного чекбокса.
        """

        log.info(f"Create checkbox: {config['text']}")
        checkbox = QCheckBox()
        for param, value in config.items():
            match param:
                case "text":
                    checkbox.setText(value)
                case "callback":
                    # Привязка метода, который будет вызван при
                    # активации/деактивации чекбокса.
                    self.parent_window.connect_callback(
                        checkbox,
                        value,
                        config.get("params", {}),
                        self.parent_window
                    )
        return checkbox

    def __create_button(self, config: dict) -> QPushButton:
        """
        Создает, конфигурирует и возвращает объект кнопки.

        Parameters
        ----------
        - config: dict
            Конфиг, по которому будет создана и сконфигурирована кнопка.

        Returns
        -------
        label: QPushButton
            Объект созданной кнопки.
        """

        log.info(f"Create button: {config['text']}")
        button = QPushButton(config['text'])
        for param, value in config.items():
            match param:
                case "width":
                    button.setFixedWidth(int(value))
                case "height":
                    button.setFixedHeight(int(value))
                case "callback":
                    self.parent_window.connect_callback(
                        button,
                        value,
                        config.get("params", {}),
                        self.parent_window
                    )

        # Активирует кнопку, только если в ее конфиге есть коллбэк.
        if "callback" not in config:
            button.setEnabled(False)
        return button

    def __create_dropdown(self, config: dict):
        """
        Создает, конфигурирует и возвращает объект выпадающего списка.

        Parameters
        ----------
        - config: dict
            Конфиг, по которому будет создан и сконфигурирован выпадающий
            список.

        Returns
        -------
        label: QComboBox
            Объект созданного выпадающего списка.
        """

        dropdown = QComboBox()
        name = config['name']
        if not self.default_values.get(name):
            self.default_values[name] = config['default_value']
        for param, value in config.items():
            log.info(f"Create dropdown list: {config['name']}")
            match param:
                case "options":
                    # Настройка вариантов выбора
                    if value.get('always'):
                        dropdown.addItems(value['always'])
                    else:
                        dropdown.addItems(value[self.current_changing_value])
                case "width":
                    dropdown.setFixedWidth(int(value))
                case "height":
                    dropdown.setFixedHeight(int(value))

        dropdown.setCurrentText(self.default_values[name])
        self.chosen_fields[config['name']] = dropdown

        # Если выпадающий список является меняющим, то задаем метод, который
        # будет срабатывать при смене выбора этого списка.
        if config.get('change_widgets'):
            dropdown.currentIndexChanged.connect(
                lambda index: self.__update_dependent_layouts(
                    config['name'],
                    dropdown.itemText(index)
                )
            )
        return dropdown

    def __get_widget_pos(
        self,
        current_row: int,
        current_col: int,
        col_amount: int,
        widget_pos: str | None = None
    ) -> Tuple[int]:
        """
        В зависимсоти от конфигурации расположения виджета (first,
        current, last, middle) высчитывает его положение в сетке контейнера
        и возвращает координаты.

        Parameters
        ----------
        - current_row: int
            Текущая строка сетки.

        - current_col: int
            Текущая колонка сетки.

        - col_amount: int
            Количество колонок в сетке.

        - widget_pos: str | None
            Позиция в сетке, на которой должен быть расположен виджет.
            Возможные варианты: first, current, last, middle

        Returns
        -------
        - current_row, current_col: Tuple[int]
            Итоговое положение в сетке, на котором будет расположен виджет в
            зависимости от того что прописано в его конфиге.

        """

        positions = {
            "first": 0,
            "last": col_amount - 1,
            "current": current_col
        }

        if current_col == col_amount:
            current_row += 1
            current_col = 0

        if widget_pos:
            if widget_pos == "first":
                if current_col > 0:
                    current_row += 1
                return current_row, positions['first']

            if widget_pos == "current":
                return current_row, current_col

            if widget_pos == "last":
                return current_row, positions['last']

            if widget_pos == "middle":
                if current_col < (col_amount - 1) // 2:
                    current_col = (col_amount - 1) // 2
                return current_row, current_col

        return current_row, current_col

    def __update_dependent_layouts(
        self,
        name: str,
        selected_value: str
    ) -> None:
        """
        Метод обновления зависимых контейнеров. Если значение, от которого они
        зависят, поменялось, то перерисовывает эти контейнеры с новыми
        параметрами.

        Parameters
        ----------
        - name: str
            Имя изменяющего виджета.

        - selected_value: str
            Новое выбранное значение.
        """
        log.info("Rerender dependent layouts")

        self.default_values[name] = selected_value
        self.remover.delete_layout(
            self.layout_parents[self.main_layout],
            self.main_layout
        )
        main_window = self.layout_parents.pop(self.main_layout, None)
        old_layout = main_window.layout()
        QWidget().setLayout(old_layout)
        self.layout_parents = {}
        self.dependencies = {}
        self.create_widget_layout(main_window, self.config['layout'])

    def __check_if_widget_is_active(self, config: dict) -> bool:
        """
        Проверяет, активен ли текущий виджет с его-то конфигом при
        соответствующем выборе. Если активен, то будет отображен. В противном
        случае - нет.

        Parameters
        ----------
        - config: dict
            Конфиг текущего виджета.

        Returns
        -------
        - _: bool
            Возвращает истину, если виджет надо отображать и Ложь - если не
            надо.
        """

        active_when = []
        visibility_key = ""

        # Для отладки
        if (
            config.get('layout') and
            config['layout'].get('name') and
            config['layout']['name'] == "first"
        ):
            print("stop here")

        # visibility_key введен специально для Fiancate случая. Поскольку там
        # виджетов, меняющих другие - больше, чем 1. И через visibility_key
        # проще понимать, от какого виджета зависит появление текущего виджета.
        if config.get('active_when'):
            active_when = config['active_when']
            if config.get('visibility_key'):
                visibility_key = config['visibility_key']
        elif (
            config.get('layout') and
            config['layout'].get('active_when')
        ):
            active_when = config['layout']['active_when']
            if config['layout'].get('visibility_key'):
                visibility_key = config['layout']['visibility_key']

        if active_when:
            if visibility_key:
                if (
                    self.current_changing_values.get(visibility_key) and
                    (
                        self.current_changing_values[visibility_key]
                        not in active_when
                    )
                ):
                    return False
            elif (
                self.current_changing_value and
                self.current_changing_value not in active_when
            ):
                return False

        return True
