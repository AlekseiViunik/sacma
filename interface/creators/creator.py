from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLayout,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget
)
from PyQt6.QtCore import Qt

from logic.helpers.finder import Finder
from logic.helpers.remover import Remover
from interface.creators.widget_creators.button_creator import ButtonCreator
from interface.creators.widget_creators.checkbox_creator import CheckboxCreator
from interface.creators.widget_creators.dropdown_creator import DropdownCreator
from interface.creators.widget_creators.image_creator import ImageCreator
from interface.creators.widget_creators.input_creator import InputCreator
from interface.creators.widget_creators.label_creator import LabelCreator
from logic.generators.config_generator import ConfigGenerator
from settings import settings as sett


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

    Methods
    -------
    - create_widget_layout()
        Создает контейнер для размещения виджетов и раполагает его на текущем
        окне или другом контейнере.

    - show_response(values, post_message, only_keys, pre_message)
        Используя конфиг генератор, добавляет в текущий конфиг виджеты для
        отображения результатов и вызывает метод обновления окна.

    - hide_response()
        Используя генератор конфигов удаляет результат предыдущей работы с
        окна ввода.

    - update_dependent_layouts(name, selected_value)
        Обновляет окно при выборе другого значения, которое меняет расположение
        виджетов.

    Private methods
    ---------------
    - __add_widgets(layout, layout_type, widgets_configs, columns)
        Инициирует процесс проверки активности виджета и его создания.
        Располагает виджет на контейнере.

    - __create_widget(config, layout, row, column)
        В зависимости от типа виджета (взятого из его конфига), вызывает
        соответствующий класс для создания виджета и возвращает созданный
        виджет. Если вместо виджета передан контейнер, вызывает заново метод
        create_widget_layout().

    - __create_layout(layout_config)
        Создает и возвращает объект контейнера в зависимости от его типа,
        указанного в его конфиге.

    - __get_widget_pos(current_row, current_col, col_amount, widget_pos)
        Виджеты, располоагающиеся на контейнере типа "сетка", имеют в конфиге
        указание по своему расположению в строке. В зависимости от этого
        параметра высчитываем новые координаты виджета в сетке.

    - __check_if_widget_is_active(config)
        Проверяет, активен ли виджет при текщих изменяющих значениях.
        Необходимо, чтобы понять, стоит ли отрисовывать его.

    - __add_border_frame(layout)
        Оборачивает контейнер, которому нужна рамка в QFrame для этого.
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
        self.input_fields: dict[str, QLineEdit] = {}
        self.chosen_fields: dict[str, QComboBox] = {}
        self.default_values: dict[str, str] = {}
        self.current_changing_value: str | None = None
        self.current_changing_values: dict[str, str] = {}
        self.remover: Remover = Remover()
        self.finder: Finder = Finder()
        self.generator: ConfigGenerator = ConfigGenerator()
        self.mandatory_fields: list[str] = []
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
        parent_window: QLayout | QWidget,
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
        - parent_window: QLayout | QWidget
            Окно или контейнер. на котором должен быть размещен текущий
            контейнер. От этого зависит, какой метод использовать для
            размещения контейнера.

        - layout_config: dict | None
            Конфиг контейнера.
        """

        # Удаляем старый контейнер, если такой уже существует.
        # Если это зависимый контейнер, то
        if layout_config.get(sett.DEPENDS_ON):

            # Берем имя виджета, от которого он зависит и присваиваем его
            # значение из default_values в current_changing_value
            self.current_changing_value = self.default_values[
                layout_config[sett.DEPENDS_ON]
            ]

            # И добавляем связку "Имя виджета - его текущее значение" в
            # словарь изменяющих виджетов (или обновляем уже существующую
            # запись)
            self.current_changing_values[layout_config[sett.DEPENDS_ON]] = (
                self.current_changing_value
            )

            # TODO Если удаление контейнера тут не нужно, то убрать проверку на
            # существование уже созданного контейнера с таким именем.
            # Если по каким-то причинам (уже не помню, зачем добавил эту
            # проверку тут) зависимый контейнер с таким именем уже существует,
            if (
                layout_config[sett.DEPENDS_ON] in self.dependencies and
                self.dependencies[
                    layout_config[sett.DEPENDS_ON]
                ].get(layout_config[sett.NAME])
            ):
                # Удаляем существующий контейнер.
                self.remover.delete_layout(
                    parent_window,
                    self.dependencies[
                        layout_config[sett.DEPENDS_ON]
                    ][layout_config[sett.NAME]]
                )
        # Вызываем метод создания самого контейнера по конфигу.
        layout = self.__create_layout(layout_config)

        # Добавляем туда виджеты
        self.__add_widgets(
            layout,
            layout_config[sett.TYPE],
            layout_config[sett.WIDGETS],
            layout_config.get(sett.COLUMNS)
        )

        # Если текущий контейнер должен быть размещен на другом контейнере
        if isinstance(parent_window, QLayout):

            # Если нужна рамка или независимость в расположении контейнера
            # относительно других. В таком случае нужен виджет-обертка.
            if (sett.BORDER in layout_config.keys()):
                frame = self.__add_border_frame(layout)
                parent_window.addWidget(frame)
            elif (sett.INDEPENDENT in layout_config.keys()):
                wrapper = QWidget()
                wrapper.setSizePolicy(
                    QSizePolicy.Policy.Fixed,
                    QSizePolicy.Policy.Preferred
                )
                wrapper.setLayout(layout)
                parent_window.addWidget(
                    wrapper,
                    alignment=Qt.AlignmentFlag.AlignHCenter
                )
            else:
                parent_window.addLayout(layout)

            # Записываем в layout_parents родителя для добавленного контейнера.
            self.layout_parents[layout] = parent_window

        # Если текущий контейнер должен быть размещен на окне (QWidget)
        else:

            parent_window.setLayout(layout)
            self.main_layout = layout
            self.layout_parents[layout] = parent_window
            parent_window.adjustSize()

    def show_response(
        self,
        values: dict,
        post_message: str,
        only_keys: list[str] | None = None,
        pre_message: str = sett.PRE_MSG_STANDART
    ):
        """
        Используя конфиг генератор, добавляет в текущий конфиг виджеты для
        отображения результатов и вызывает метод обновления окна.

        Parameters
        ----------
        - values: dict
            Словарь с полученными для результата данными.

        - post_message: str
            Сообщение, которое необходимо отобразить после результата.

        - only_keys: list[str] | None
            Default = None\n
            Список ключей, значения которых из словаря values будут отражены в
            ответе.

        - pre_message: str
            Default = 'Result'\n
            Сообщение для отображения перед отображением результатов.
        """

        new_config = self.generator.add_response_to_config(
            self.config,
            values,
            only_keys,
            pre_message,
            post_message
        )

        self.config = new_config

        self.update_dependent_layouts()

    def hide_response(self) -> None:
        """
        Используя генератор конфигов удаляет результат предыдущей работы из
        конфига и с обновленным конфигом вызывает метод перестроения окна.
        """

        new_config = self.generator.remove_result_from_config(self.config)
        self.config = new_config

        self.update_dependent_layouts()

    def update_dependent_layouts(
        self,
        name: str = None,
        selected_value: str = None
    ) -> None:
        """
        Метод обновления зависимых контейнеров. Переписывает дефолтные
        значения для новой отрисовки. Очищает, (но не удаляет) основной
        контейнер с отрисованными виджетами. Создает новый. Перерисовывает все
        элементы окна с новыми дефолтными параметрами с нуля.

        Parameters
        ----------
        - name: str
            Default = None\n
            Имя изменяющего виджета.

        - selected_value: str
            Default = None\n
            Новое выбранное значение.
        """

        if name and selected_value:
            self.default_values[name] = selected_value

        self.remover.clear_layout(
            self.main_layout
        )

        self.layout_parents = {}
        self.dependencies = {}

        self.__add_widgets(
            self.main_layout,
            self.config[sett.LAYOUT][sett.TYPE],
            self.config[sett.LAYOUT][sett.WIDGETS]
        )

        self.parent_window.adjustSize()

    # ============================ Private Methods ============================
    # -------------------------------------------------------------------------
    def __add_widgets(
        self,
        layout: QLayout,
        layout_type: str,
        widgets_configs: list[dict],
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
        - layout: QLayout
            Объект контейнера, на котором должны быть размещены виджеты.

        - layout_type: str
            Тип контейнера (берется из конфига)

        - widgets_configs: list[dict]
            Список конфигов всех виджетов, которые должны быть размещены в
            контейнере в порядке их перечисления в списке.

        - columns: int | None
            Default = None\n
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
            case sett.LAYOUT_TYPE_GRID:

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
                        widget_config.get(sett.COLUMN)
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
            case sett.LAYOUT_TYPE_VERTICAL | sett.LAYOUT_TYPE_HORIZONTAL:

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
        layout: QLayout | None = None,
    ) -> QWidget | None:
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

        - layout: QLayout | None
            Default = None\n
            Контейнер, на котором виджет будет располгаться.

        Returns
        -------
        - widget: (
            QWidget | None
        )
            Возвращает созданный и сконфигурированный объект виджета.
        """

        # Если в конфиге есть ключ "layout", то
        if config.get(sett.LAYOUT):

            # Вызываем основной метод создания контейнера.
            self.create_widget_layout(
                layout,
                config[sett.LAYOUT]
            )
        # Если это все-таки виджет, то
        else:
            # Вызываем соответствующий виджет, в зависимости от его типа,
            # прописанного в конфиге.
            match config.get(sett.TYPE):
                case sett.WIDGET_TYPE_LABEL:
                    widget, mandatory_field = LabelCreator.create_label(config)
                    if mandatory_field:
                        self.mandatory_fields.append(mandatory_field)
                case sett.WIDGET_TYPE_INPUT:
                    widget = InputCreator.create_input(config, self)
                case sett.WIDGET_TYPE_BUTTON:
                    widget = ButtonCreator.create_button(
                        config,
                        self.parent_window
                    )
                case sett.WIDGET_TYPE_DROPDOWN:
                    widget = DropdownCreator.create_dropdown(config, self)
                case sett.WIDGET_TYPE_CHECKBOX:
                    widget = CheckboxCreator.create_checkbox(
                        config,
                        self.parent_window
                    )
                case sett.IMAGE:
                    widget = ImageCreator.create_image(config)
                case _:
                    widget = None
            # Возвращаем созданный и сконфигурированный виджет.
            return widget

    def __create_layout(
        self,
        layout_config: dict
    ) -> QLayout | None:
        """
        Создает контейнер по его конфигу и возвращает его.

        Parameters
        ----------
        - layout_config: dict
            Конфиг, по которому будет создан и сконфигурирован контейнер.

        Returns
        -------
        - layout: QLayout | None:
            Объект созданного контейнера
        """

        match layout_config[sett.TYPE]:
            case sett.LAYOUT_TYPE_GRID:
                layout = QGridLayout()
            case sett.LAYOUT_TYPE_VERTICAL:
                layout = QVBoxLayout()
            case sett.LAYOUT_TYPE_HORIZONTAL:
                layout = QHBoxLayout()

        # Простая проверка if layout тут не подойдет. Почему - хз, видимо,
        # потому что сам объект пустой пока
        # Видимо, эта проверка нужна, чтобы понять, удалось ли создать
        # контейнер.
        if isinstance(layout, (QLayout)):

            if (
                sett.ALIGN in layout_config.keys() and
                layout_config[sett.ALIGN] == sett.ALIGN_CENTER
            ):
                layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if sett.SETSPACING in layout_config.keys():
                layout.setSpacing(layout_config[sett.SETSPACING])

            # Если контейнер зависим, то записываем/перезаписываем его как
            # словарь типа "имя контейнера - объект контейнера" в словарь по
            # ключу, которым явяляется имя контейнера, от которого он зависит.
            if sett.DEPENDS_ON in layout_config:
                self.dependencies.setdefault(
                    layout_config[sett.DEPENDS_ON], {}
                )[layout_config[sett.NAME]] = layout

            return layout
        return None

    def __get_widget_pos(
        self,
        current_row: int,
        current_col: int,
        col_amount: int,
        widget_pos: str | None = None
    ) -> tuple[int]:
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
            Default = None\n
            Позиция в сетке, на которой должен быть расположен виджет.
            Возможные варианты: first, current, last, middle

        Returns
        -------
        - current_row, current_col: tuple[int]
            Итоговое положение в сетке, на котором будет расположен виджет в
            зависимости от того что прописано в его конфиге.

        """

        positions = {
            sett.WIDGET_POS_FIRST: sett.SET_TO_ZERO,
            sett.WIDGET_POS_LAST: col_amount - sett.STEP_DOWN,
            sett.WIDGET_POS_CURRENT: current_col
        }

        if current_col == col_amount:
            current_row += sett.STEP_UP
            current_col = sett.SET_TO_ZERO

        if widget_pos:
            if widget_pos == sett.WIDGET_POS_FIRST:
                if current_col > sett.SET_TO_ZERO:
                    current_row += sett.STEP_UP
                return current_row, positions[sett.WIDGET_POS_FIRST]

            if widget_pos == sett.WIDGET_POS_CURRENT:
                return current_row, current_col

            if widget_pos == sett.WIDGET_POS_LAST:
                return current_row, positions[sett.WIDGET_POS_LAST]

            if widget_pos == sett.WIDGET_POS_MIDDLE:
                if current_col < (
                    col_amount - sett.STEP_DOWN
                ) // sett.MIDDLE_DETERMINANT_DIVIDER:

                    current_col = (
                        col_amount - sett.STEP_DOWN
                    ) // sett.MIDDLE_DETERMINANT_DIVIDER
                return current_row, current_col

        return current_row, current_col

    def __check_if_widget_is_active(self, config: dict) -> bool:
        """
        Проверяет, активен ли текущий виджет с его-то конфигом при
        соответствующем выборе. Если активен, то будет отображен. В противном
        случае - нет. В случае, если изменяющих виджетов несколько, то в
        конфиге виджета должен быть прописан параметр visibility_key, в котором
        указано имя виджета, чье значение влияет на видимость текущего.

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
        visibility_key = sett.EMPTY_STRING

        # visibility_key введен специально для Fiancate случая. Поскольку там
        # виджетов, меняющих другие - больше, чем 1. И через visibility_key
        # проще понимать, от какого виджета зависит появление текущего виджета.
        if config.get(sett.ACTIVE_WHEN):
            active_when = config[sett.ACTIVE_WHEN]
            if config.get(sett.VISIBILITY_KEY):
                visibility_key = config[sett.VISIBILITY_KEY]
        elif (
            config.get(sett.LAYOUT) and
            config[sett.LAYOUT].get(sett.ACTIVE_WHEN)
        ):
            active_when = config[sett.LAYOUT][sett.ACTIVE_WHEN]
            if config[sett.LAYOUT].get(sett.VISIBILITY_KEY):
                visibility_key = config[sett.LAYOUT][sett.VISIBILITY_KEY]

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

    def __add_border_frame(self, layout: QLayout) -> QFrame:
        """
        Оборачивает контейнер во фрейм, чтобы потом фрейму добавить рамку, т.к.
        сам контейнер рамку иметь не может.

        Parameters
        ----------
        - layout: QLayout
            Контейнер, который необходимо обернуть во фрейм.

        Returns
        -------
        - frame: QFrame
            Фрейм с обернутым контейнером.
        """

        frame = QFrame()
        frame.setLayout(layout)
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setLineWidth(sett.SET_TO_ONE)
        return frame
