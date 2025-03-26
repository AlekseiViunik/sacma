from settings import settings as set
from logic.logger import logger as log


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
        only_keys : bool, optional
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
                return {
                    set.DICTIONARY.get(key, key): val for key, val
                    in value.items()
                }
            return None
        except Exception as e:
            log.error(f"Error caught: {e}")
