class StringHandler:
    """
    Класс для работы с динамическими строками.
    """
    def create_dynamic_message(static_message, *args):
        """
        Создает динамическое сообщение, подставляя значения из args в static_message.
        """
        return static_message.format(*args)
