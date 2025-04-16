from PyQt6.QtWidgets import QLineEdit
from typing import TYPE_CHECKING

from logic.logger import logger as log
from logic.preparators.widget_preparator import WidgetPreparator
from settings import settings as sett

if TYPE_CHECKING:
    from interface.creators.creator import Creator


class InputCreator:
    """
    Класс для создания полей для ввода.

    Methods
    -------
    - create_input(input_config, creator)
        Создает поле для ввода по заданному конфигу и возвращает его объект.
    """

    @staticmethod
    def create_input(
        input_config: dict,
        # Кавычки нужны, чтобы избежать циклической зависимости
        creator: "Creator"
    ) -> QLineEdit:
        """
        Создает, конфигурирует и возвращает объект поля для ввода.

        Parameters
        ----------
        - config: dict
            Конфиг, по которому будет создано и сконфигурировано поле для
            ввода.

        - creator: Creator
            Объект класса Creator, свойству которого будут присвоены значения,
            введенные пользователем.

        Returns
        -------
        - input_field: QLineEdit
            Объект созданного поля для ввода.
        """

        log.info(sett.CREATE_INPUT_FIELD)
        input_field = QLineEdit()
        for param, value in input_config.items():
            match param:
                case sett.WIDTH:
                    input_field.setFixedWidth(int(value))
                case sett.HEIGHT:
                    input_field.setFixedHeight(int(value))
                case sett.DEFAULT_VALUE:
                    if isinstance(value, dict):

                        # Если дефолт задан динамически
                        text = WidgetPreparator.prepare_default_for_input(
                            config=value,
                            username=creator.parent_window.username
                        )
                        input_field.setPlaceholderText(text)

                    else:
                        input_field.setPlaceholderText(value)
                case sett.HIDE:
                    # Прячет вводимые символы (для чувствительных данных).
                    input_field.setEchoMode(QLineEdit.EchoMode.Password)
                case sett.DISABLED:
                    input_field.setEnabled(False)

                case sett.TEXT_CHANGE:
                    match value:
                        case sett.AUTO_PHONE_FORMAT:
                            input_field.textChanged.connect(
                                lambda text: (
                                    WidgetPreparator.auto_phone_format(
                                        input_field, text
                                    )
                                )
                            )

        # Пытаемся получить данные из поля для ввода.
        try:
            creator.input_fields.get(
                input_config[sett.NAME]
            ).text()

        # Если поле для ввода уже было создано до этого и потом было очищено,
        # то оно уже мертво и выскакивает ошибка RuntimeError. Отлавливаем
        # ошибку и удаляем поле.
        except RuntimeError:
            creator.input_fields.pop(input_config[sett.NAME], None)

        # Если поле для ввода, еще не было создано, то у нас NoneType и оно не
        # имеет метода text(), о чем говорит ошибка AttributeError. Дальше все
        # равно идет проверка на существование поля, поэтому ошибку просто
        # игнорируем.
        except AttributeError:
            pass

        # Если в поле для ввода уже были внесены даные, то при
        # перерисовке окна они будут перезаписаны.
        if (
            creator.input_fields and
            creator.input_fields.get(input_config[sett.NAME]) and
            creator.input_fields.get(
                input_config[sett.NAME]
            ).text() != sett.EMPTY_STRING
        ):

            input_field.setText(
                creator.input_fields[input_config[sett.NAME]].text()
            )

        creator.input_fields[input_config[sett.NAME]] = input_field
        return input_field
