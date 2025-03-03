import json


class JsonFileHandler:
    def __init__(self, file):
        self.file = file

    def read_value_by_key(self, key: str):
        """Читает JSON и возвращает значение по переданному ключу."""
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)  # Загружаем JSON в словарь

            return data.get(key, None)  # Возвращаем значение по ключу или None

        except FileNotFoundError:
            print(f"❌ Файл '{self.file}' не найден.")
            return None
        except json.JSONDecodeError:
            print(f"❌ Ошибка чтения JSON в файле '{self.file}'.")
            return None
