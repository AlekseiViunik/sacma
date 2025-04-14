from handlers.json_handler import JsonHandler
from settings import settings as sett


class WidgetPreparator:

    @staticmethod
    def prepare_default_for_input(**kwargs):

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
