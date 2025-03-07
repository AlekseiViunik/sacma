import tkinter as tk
from tkinter import messagebox

from gui.type_classes.abstract_base_type import AbstractBaseType
from logic.authenticator import Authenticator


class CreateUserWindow(AbstractBaseType):
    """
    Класс для окна регистрации пользователя.

    Attriutes
    ---------
    root : tk.Tk
        Главное окно.
    type : str
        Тип. В данном классе не нужен. Стоит тут как заглушка
    entry_widgets : list
        Список виджетов с полями для ввода.

    Methods
    -------
    calculate()
        Обработка процесса регистрации нового юзера.
    """

    def __init__(
        self,
        root: tk.Tk,
        type: str = None,
        entry_widgets: list = None
    ) -> None:
        super().__init__(root, type, entry_widgets)
        self.auth = Authenticator()

    def calculate(self) -> None:
        """
        Регистрация новых юзеров. Выводит информационное окно в случае успешной
        регистрации или окно об ошибке с ее описанием в случае провала.
        """
        values = {key.lower(): var.get() for key, var in self.entries.items()}
        if values['password'] == values['repeat password']:
            if self.auth.register_user(values['username'], values['password']):
                messagebox.showinfo(
                    "Done!",
                    f"User '{values['username']}' is created!"
                )
            else:
                messagebox.showerror(
                    "Error",
                    f"User '{values['username']}' exists!"
                )
        else:
            messagebox.showerror(
                "Error",
                "You entered different passwords!"
            )
