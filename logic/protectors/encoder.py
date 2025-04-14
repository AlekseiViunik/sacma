import json
import random

from logic.logger import logger as log
from settings import settings as sett
from settings.global_variables import encryption_data


class Encoder:
    """
    Класс для шифрования и дешифрования текстовых файлов с использованием
    уникальных кодов.

    Methods
    -------
    - decrypt_data(data)
        Дешифрует данные, используя словарь дешифровки

    - encrypt_data(data_dict)
        Шифрует данные, используя словарь шифрования
    """
    def __init__(self) -> None:
        if sett.PRODUCTION_MODE_ON:
            self.enctryption_data = encryption_data
        else:
            with open(
                sett.ENCRYPTION_FILE, sett.FILE_READ, encoding=sett.STR_CODING
            ) as f:
                self.encryption_data = json.load(f)

    def decrypt_data(
        self,
        data: list[str],
    ) -> dict:
        """
        Дешифрует данные, используя словарь дешифровки

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
        decryption: dict = self.encryption_data[sett.DECRYPTION]

        decrypted_text = []

        for line in data:
            chunks = [
                line[i:i+self.encryption_data[sett.SYMBOLS]] for i in range(
                    sett.SET_TO_ZERO,
                    len(line),
                    self.encryption_data[sett.SYMBOLS]
                )
            ]
            decoded = sett.EMPTY_STRING.join(
                decryption.get(code, sett.QUESTION_MARK) for code in chunks
            ).rstrip()
            decrypted_text.append(decoded)

        # Пробуем собрать обратно словарь
        try:
            return json.loads(sett.EMPTY_STRING.join(decrypted_text))
        except json.JSONDecodeError:
            log.error(sett.FAILED_TO_DECODE)
            return {sett.ERROR: sett.FAILED_TO_DECODE}

    def encrypt_data(self, data_dict: dict) -> list[str]:
        """
        Шифрует данные, используя словарь шифрования

        Parameters
        ----------
        - data_dict: dict
            Словарь данных, которые нужно зашифровать.

        Returns
        -------
        - encrypted_lines: list[str]
            Список строк, содержащих зашифрованные данные.
        """

        encryption = self.encryption_data[sett.ENCRYPTION]

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
