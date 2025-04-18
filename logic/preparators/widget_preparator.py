from PyQt6.QtWidgets import QLineEdit

from logic.handlers.json_handler import JsonHandler
from settings import settings as sett


class WidgetPreparator:
    """
    Класс для подготовки виджетов перед их использованием.

    Methods
    -------
    - prepare_default_for_input(**kwargs) -> str
        Подготавливает динамическое дефолтное значение для виджета
        QLineEdit.

    - auto_phone_format(input: QLineEdit, text: str) -> None
        Автоматически форматирует ввод номера телефона в
        формат (XXX) XXX-XX-XX.
    """

    @staticmethod
    def prepare_default_for_input(**kwargs):
        """
        Подготавливает динамическое дефолтное значение для виджета
        QLineEdit.
        """

        # Собираем дефолтное значение. Начинаем с пустой строки.
        default_value = sett.EMPTY_STRING

        # Если среди ключевых аргументов есть конфиг
        if (config := kwargs.get(sett.CONFIG)) is not None:

            # Если в конфиге есть ключ "starts_with", то добавляем его к
            # дефолтному значению.
            if (starts_with := config.get(sett.STARTS_WITH)) is not None:
                default_value += starts_with

            # Если в конфиге есть ключ "get_from_file", то по этому ключу
            # должен быть словарь с ключами "key", "file_path" и
            # is_encoded (опциональный).
            # "key" - это ключ, по которому мы будем искать значение в файле,
            # "file_path" - это путь к файлу, из которого мы будем брать
            # динамическую часть значения.
            # "is_encoded" - это булевый параметр, который указывает, нужно
            # ли декодировать файл. Если не указан, то не нужно.
            if (get_from_file := config.get(sett.GET_FROM_FILE)) is not None:

                # Получаем все данные из указанного файла
                is_encoded = bool(get_from_file.get(sett.IS_ENCODED, False))
                file_json_handler = JsonHandler(
                    get_from_file[sett.FILE_PATH], is_encoded
                )
                file_data = file_json_handler.get_all_data()

                # Ключ может быть как строкой (единичный ключ), так и списком
                # (несколько ключей). Если это список, то проходим по всем
                # ключам и получаем значение по каждому из них.
                # Если ключ - строка, то просто получаем значение по этому
                # ключу.
                if isinstance(get_from_file[sett.KEY], list):
                    for key in get_from_file[sett.KEY]:

                        # Если ключ начинается с "<" и заканчивается
                        # на ">", то это значит, что мы должны найти среди
                        # ключевых аргументов этот ключ, а его значение уже
                        # использовать как ключ для поиска в файле.
                        if (
                            key.startswith(sett.LESS_THAN) and
                            key.endswith(sett.GREATER_THAN)
                        ):
                            key = key[1:-1]
                            key = kwargs.get(key, sett.EMPTY_STRING)
                            file_data = file_data.get(key, sett.EMPTY_STRING)
                        else:
                            file_data = file_data.get(key, sett.EMPTY_STRING)
                else:
                    file_data = file_data.get(
                        get_from_file[sett.KEY], sett.EMPTY_STRING
                    )

                default_value += file_data

                if (ends_with := config.get(sett.ENDS_WITH)) is not None:
                    default_value += ends_with

        return default_value

    @staticmethod
    def auto_phone_format(
        input: QLineEdit,
        text: str
    ) -> None:
        """
        Автоматически форматирует ввод номера телефона в
        формат (XXX) XXX-XX-XX.

        Parameters
        ----------
        - input: QLineEdit
            Поле ввода, которое нужно отформатировать.
        - text: str
            Текст, который нужно отформатировать.
        """

        # Удаляем все символы, кроме цифр
        digits = sett.EMPTY_STRING.join(filter(str.isdigit, text))

        # Форматируем номер телефона
        if len(digits) > sett.SET_TO_ONE:

            # Максимум 10 цифр
            # Eсли больше, то обрезаем до 10
            digits = sett.EMPTY_STRING.join(
                filter(str.isdigit, text)
            )[:sett.PHONE_NUMBER_LENGTH]

        formatted = sett.EMPTY_STRING

        # Начало ввода. Ставим скобку.
        if len(digits) >= sett.OPEN_BRACKET_POSITION:
            formatted = sett.ADD_OPEN_BRACKET.format(
                digits[:sett.FIRST_DIGITS_BLOCK]
            )

        # Введено 3 цифры. Ставим закрывающую скобку и пробел.
        if len(digits) >= sett.CLOSE_BRACKET_POSITION:
            end_block = sett.FIRST_DIGITS_BLOCK + sett.SECOND_DIGITS_BLOCK
            formatted += sett.ADD_CLOSE_BRACKET.format(
                digits[
                    sett.FIRST_DIGITS_BLOCK:end_block
                ]
            )

        # Введено 6 цифр. Ставим дефис.
        if len(digits) >= sett.FIRST_DASH_POSITION:
            start_block = sett.FIRST_DIGITS_BLOCK + sett.SECOND_DIGITS_BLOCK
            end_block = start_block + sett.THIRD_DIGITS_BLOCK
            formatted += sett.ADD_DASH.format(
                digits[start_block:end_block]
            )

        # Введено 8 цифр. Ставим дефис.
        if len(digits) >= sett.SECOND_DASH_POSITION:
            start_block = (
                sett.FIRST_DIGITS_BLOCK +
                sett.SECOND_DIGITS_BLOCK +
                sett.THIRD_DIGITS_BLOCK
            )
            end_block = start_block + sett.FOURTH_DIGITS_BLOCK
            formatted += sett.ADD_DASH.format(
                digits[start_block:end_block]
            )

        input.blockSignals(True)
        input.setText(formatted)
        input.blockSignals(False)
        input.setCursorPosition(len(formatted))
