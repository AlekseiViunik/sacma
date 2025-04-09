import json
import random


class Encoder:
    """
    Класс для шифрования и дешифрования текстовых файлов с использованием
    уникальных кодов.

    Methods
    -------
    - decrypt_data(data)
        Дешифрует данные, используя словарь дешифровки из файла
        "configs/encryption.json".

    - encrypt_data(data_dict)
        Шифрует данные, используя словарь шифрования из файла
        "configs/encryption.json".
    """
    def __init__(self):
        pass

    def decrypt_data(
        self,
        data: list[str],
    ) -> dict:
        """
        Дешифрует данные, используя словарь дешифровки из файла
        "configs/encryption.json".

        Parameters
        ----------
        - data: list[str]
            Список строк, содержащих закодированные данные.

        Returns
        -------
        - _: dict
            Дешифрованные данные в виде словаря. Если дешифровка не удалась,
            возвращает словарь с ошибкой.
        """

        # Загружаем словарь дешифровки
        with open("configs/encryption.json", "r", encoding="utf-8") as f:
            decryption = json.load(f)["decription"]

        decrypted_text = []

        for line in data:
            chunks = [line[i:i+5] for i in range(0, len(line), 5)]
            decoded = ''.join(
                decryption.get(code, '?') for code in chunks
            ).rstrip()
            decrypted_text.append(decoded)

        # Пробуем собрать обратно словарь
        try:
            return json.loads(''.join(decrypted_text))
        except json.JSONDecodeError:
            return {"error": "Failed to decode JSON"}

    def encrypt_data(self, data_dict):
        """
        Шифрует данные, используя словарь шифрования из файла
        "configs/encryption.json".

        Parameters
        ----------
        - data_dict: dict
            Словарь данных, которые нужно зашифровать.

        Returns
        -------
        - encrypted_lines: list[str]
            Список строк, содержащих зашифрованные данные.
        """

        with open("configs/encryption.json", "r", encoding="utf-8") as f:
            encryption = json.load(f)["encryption"]

        json_lines = json.dumps(
            data_dict, indent=4, ensure_ascii=False
        ).splitlines()

        encrypted_lines = []

        for line in json_lines:
            line = line.ljust(100)[:100]
            encrypted_line = [
                random.choice(
                    encryption.get(ch, encryption[" "])
                ) for ch in line
            ]
            encrypted_lines.append("".join(encrypted_line))

        return encrypted_lines
