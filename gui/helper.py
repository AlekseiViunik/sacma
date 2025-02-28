class Helper:
    """Вспомогательный класс с утилитарными методами."""

    @staticmethod
    def get_type_class_name(name: str) -> str:
        """Преобразует строку в имя класса в CamelCase.

        Примеры:
        --------
            "this is a class" → "ThisIsAClass",
            "travi di battuta" → "TraviDiBattuta"

        Parameters
        ----------
            name : str
                Исходная строка.

        Returns
        -------
            str
                Строка в CamelCase (как имя класса).
        """
        return "".join(word.capitalize() for word in name.split())
