import json
import random

from logic.logger import logger as log
from settings import settings as sett


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
        with open(
            sett.ENCRYPTION_FILE, sett.FILE_READ, encoding=sett.STR_CODING
        ) as f:
            decryption: dict = json.load(f)[sett.DECRYPTION]

        decrypted_text = []

        for line in data:
            chunks = [line[i:i+5] for i in range(0, len(line), 5)]
            decoded = ''.join(
                decryption.get(code, sett.QUESTION_MARK) for code in chunks
            ).rstrip()
            decrypted_text.append(decoded)

        # Пробуем собрать обратно словарь
        try:
            return json.loads(''.join(decrypted_text))
        except json.JSONDecodeError:
            log.error(sett.FAILED_TO_DECODE)
            return {sett.ERROR: sett.FAILED_TO_DECODE}

    def encrypt_data(self, data_dict: dict) -> list[str]:
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

        with open(
            sett.ENCRYPTION_FILE, sett.FILE_READ, encoding=sett.STR_CODING
        ) as f:
            encryption = json.load(f)[sett.ENCRYPTION]

        json_lines = json.dumps(
            data_dict, indent=sett.INDENT, ensure_ascii=False
        ).splitlines()

        encrypted_lines = []

        for line in json_lines:
            line = line.ljust(sett.HUNDRED)[:sett.HUNDRED]
            encrypted_line = [
                random.choice(
                    encryption.get(ch, encryption[sett.SPACE_SYMBOL])
                ) for ch in line
            ]
            encrypted_lines.append(sett.EMPTY_STRING.join(encrypted_line))

        return encrypted_lines
