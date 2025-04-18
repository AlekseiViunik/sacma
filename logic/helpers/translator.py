from logic.logger import LogManager as lm
from settings import settings as sett


class Translator:
    """
    Класс для перевода отдельных наиболее часто используемых слов в коде.
    Переводит с английского на итальянский.

    Methods
    -------
    translate_dict(value, only_keys)
        Переводит ключи словаря или весь словарь с английского на
        итальянский.
    """

    @staticmethod
    def translate_dict(
        value: dict,
        only_keys: bool = True
    ) -> dict | None:
        """
        Переводит ключи словаря с английского на итальянский.
        В будущем сможет переводить также и значения.

        Parameters
        ----------
        value : dict
            Словарь, который нужно перевести.
        only_keys : bool
            Default = True\n
            Если True, то переводит только ключи словаря. По умолчанию True.
            (это задел на будущее)

        Returns
        -------
        dict | None
            Возвращает словарь с переведенными ключами или None, если передан
            пустой словарь.
        """

        try:
            if only_keys:
                translated = {}
                for key, val in value.items():
                    key_parts = key.split(sett.UNDERSCORE)
                    translated_key_parts = Translator.translate_words(
                        key_parts
                    )
                    translated_key = sett.SPACE_SYMBOL.join(
                        translated_key_parts
                    )
                    translated[translated_key] = val

                return translated
            return None
        except Exception as e:
            lm.log_exception(e)

    @staticmethod
    def translate_words(words: list[str]) -> list[str]:
        """
        Переводит список слов с английского на итальянский.
        Делает первое слово списка с заглавной буквы, остальные - с
        маленькой.

        Parameters
        ----------
        words : list[str]
            Список слов, которые нужно перевести.

        Returns
        -------
        list[str]
            Возвращает список переведенных слов.
        """
        translated_list = [
            sett.DICTIONARY.get(word, word) for word in words
        ]

        for i in range(len(translated_list)):
            if i == sett.SET_TO_ZERO:
                translated_list[i] = translated_list[i].capitalize()
            else:
                translated_list[i] = translated_list[i].lower()

        return translated_list

    @staticmethod
    def translate_string(text: str) -> str:
        """
        Переводит текст с английского на итальянский.

        Parameters
        ----------
        text : str
            Текст, который нужно перевести.

        Returns
        -------
        str
            Возвращает переведенный текст.
        """
        text = {text: sett.EMPTY_STRING}
        translated_dict = Translator.translate_dict(text)
        return list(translated_dict.keys())[sett.SET_TO_ZERO]
