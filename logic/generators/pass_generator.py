from settings import settings as sett


class PassGenerator:
    """
    Генератор паролей. Служит для генерации случайных паролей при
    восстановлении.

    Methods
    -------
    - generate_password(length)
        Генерирует случайный пароль заданной длины.
    """

    @staticmethod
    def generate_password(length: int = sett.SET_TO_TWELVE) -> str:
        """
        Генерирует случайный пароль заданной длины.

        Parameters
        ----------
        - length: int
            Default = 12\n
            Длина пароля (по умолчанию 12 символов).

        Returns
        -------
        - str
            Сгенерированный пароль.
        """

        import random
        import string

        characters = (
            string.ascii_letters + string.digits + sett.COMMON_SPECIAL_CHARS
        )
        password = ''.join(random.choice(characters) for _ in range(length))

        return password
