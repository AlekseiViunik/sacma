from settings import settings as set


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
        В будущем сможет переводитьт также и значения.

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
        if only_keys:
            return {
                set.DICTIONARY.get(key, key): val for key, val in value.items()
            }
        return None
