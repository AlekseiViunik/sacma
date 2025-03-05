from typing import Dict, Any

from settings import settings as set


class Translator:
    """
    Класс для перевода отдельных наиболее часто используемых слов в коде.
    Переводит с английского на итальянский.
    """

    @staticmethod
    def translate_dict(
        value: Dict[str, Any],
        only_keys=True
    ) -> Dict[str, Any] | None:
        """
        Переводит ключи словаря с английского на итальянский.

        Parameters
        ----------
        value : Dict[str, Any]
            Словарь, который нужно перевести.
        only_keys : bool, optional
            Если True, то переводит только ключи словаря. По умолчанию True.
            (это задел на будущее)
        
        Returns
        -------
        Dict[str, Any] | None
            Возвращает словарь с переведенными ключами или None, если передан
            пустой словарь.
        """
        if only_keys:
            return {
                set.DICTIONARY.get(key, key): val for key, val in value.items()
            }
        return None
