from PyQt6.QtWidgets import QComboBox
from typing import TYPE_CHECKING

from handlers.json_handler import JsonHandler
from logic.logger import logger as log
from settings import settings as sett

if TYPE_CHECKING:
    from interface.creators.creator import Creator


class DropdownCreator:
    """
    Класс для создания выпадающих списков.

    Methods
    -------
    - create_dropdown(dropdown_config, creator)
        Создает выпадающий список по заданному конфигу и возвращает его
        объект.
    """

    @staticmethod
    def create_dropdown(
        dropdown_config: dict,
        creator: "Creator"
    ) -> QComboBox:
        """
        Создает, конфигурирует и возвращает объект выпадающего списка.

        Parameters
        ----------
        - config: dict
            Конфиг, по которому будет создан и сконфигурирован выпадающий
            список.

        - creator: Creator
            Объект класса Creator, который будет хранить выбранное и доступные
            для выбора значения, связанные с этим выпадающим списком.

        Returns
        -------
        - dropdown: QComboBox
            Объект созданного выпадающего списка.
        """

        dropdown = QComboBox()
        name = dropdown_config[sett.NAME]
        if not creator.default_values.get(name):
            creator.default_values[name] = dropdown_config[sett.DEFAULT_VALUE]
        log.info(
            sett.CREATE_WIDGET.format(
                sett.DROPDOWN, dropdown_config[sett.NAME]
            )
        )
        for param, value in dropdown_config.items():

            match param:
                case sett.OPTIONS:
                    # Настройка вариантов выбора
                    if value.get(sett.GET_FROM_FILE):
                        json_handler = JsonHandler(
                            value[sett.GET_FROM_FILE][sett.FILE_PATH],
                            True
                        )
                        data = json_handler.get_all_data()[
                            value[sett.GET_FROM_FILE][sett.KEY]
                        ]
                        dropdown.addItems(list(data.keys()))
                    elif value.get(sett.ALWAYS):
                        dropdown.addItems(value[sett.ALWAYS])
                    else:
                        dropdown.addItems(
                            value[creator.current_changing_value]
                        )
                case sett.WIDTH:
                    dropdown.setFixedWidth(int(value))
                case sett.HEIGHT:
                    dropdown.setFixedHeight(int(value))
                case sett.DISABLED:
                    dropdown.setEnabled(False)

        dropdown.setObjectName(dropdown_config[sett.NAME])

        # Если выпадающий список является меняющим виджеты на окне, то
        # оставляем как есть. В противном случае пытаемся сохранить выбранное
        # значение. Значение останется выбранным, если такое поле есть в новом
        # окне и если уже выбранное значение является одним из возможных
        # вариантов выбора в новом окне.
        if sett.CHANGE_WIDGETS not in dropdown_config.keys():

            # Пытаемся получить данные из поля для выбора.
            try:
                creator.chosen_fields.get(
                    dropdown_config[sett.NAME]
                ).currentText()

            # Если поле для выбора уже было создано до этого и потом было
            # очищено, то оно уже мертво и выскакивает ошибка RuntimeError.
            # Отлавливаем ошибку и удаляем поле.
            except RuntimeError:
                creator.chosen_fields.pop(dropdown_config[sett.NAME], None)

            # Если поле для ввода, еще не было создано, то у нас NoneType и
            # оно не имеет метода currentText(), о чем говорит ошибка
            # AttributeError. Дальше все равно идет проверка на существование
            # поля, поэтому ошибку просто игнорируем.
            except AttributeError:
                pass

            if (
                creator.chosen_fields and
                creator.chosen_fields.get(dropdown_config[sett.NAME]) and
                creator.chosen_fields.get(
                    dropdown_config[sett.NAME]
                ).currentText() != sett.EMPTY_STRING
            ):

                dropdown.setCurrentText(
                    creator.chosen_fields[
                        dropdown_config[sett.NAME]
                    ].currentText()
                )
        else:
            dropdown.setCurrentText(creator.default_values[name])

        creator.chosen_fields[dropdown_config[sett.NAME]] = dropdown

        # Если выпадающий список является меняющим, то задаем метод, который
        # будет срабатывать при смене выбора этого списка.
        if dropdown_config.get(sett.CHANGE_WIDGETS):
            dropdown.currentIndexChanged.connect(
                lambda index: creator.update_dependent_layouts(
                    dropdown_config[sett.NAME],
                    dropdown.itemText(index)
                )
            )
        return dropdown
