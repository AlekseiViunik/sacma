from settings import settings as set


class Translator:

    @staticmethod
    def translate_dict(value, only_keys=True):
        if only_keys:
            return {set.DICTIONARY[key]: value for key, value in value.items()}
        return None
