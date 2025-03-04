from settings import settings as set


class Translator:

    @staticmethod
    def translate_dict(value, only_keys=True):
        if only_keys:
            return {
                set.DICTIONARY.get(key, key): val for key, val in value.items()
            }
        return None
