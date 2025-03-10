import tkinter as tk

from tkinter import messagebox

from gui.helper import Helper
from gui.widget_creator import WidgetCreator
from logic.authenticator import Authenticator as auth
from logic.logger import logger as log
from settings import settings as set


class AuthWindow:
    """
    Класс, отвечающий за окно авторизации.

    Attributes
    ----------
    root : tk.Tk
        Главное окно.
    auth_successful : bool
        Содержит информацию об успешности авторизации.
    entries : dict
        Словарь введенных значений.
    creator :  WidgetCreator
        Вспомогательный объект для создания виджетов.

    Methods
    -------
    login()
        Обрабатывает попытку входа.
    on_close()
        Обрабатывает ручное закрытие окна.
    get_default_value(key)
        Получает дефолтное значение для полей ввода (если есть)
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Authorization")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        self.auth_successful: bool = False
        self.entries: dict = None
        self.creator: WidgetCreator = WidgetCreator(self.root, None)

        Helper.center_window(300, 200, self.root)

        frame = self.creator.create_frame("login")
        row = set.LOGIN_START_ROW
        for label in set.LOGIN_ENTRIES.keys():
            self.creator.create_component(
                frame,
                label,
                None,
                row,
                is_entry=True,
                is_hide=set.LOGIN_ENTRIES[label]['is_hide'],
                default_value=self.get_default_value(label)
            )
            row += 1
        self.creator.create_button("Login", self.login)
        self.root.protocol(set.ON_CLOSING_WINDOW, self.on_close)

    def login(self) -> None:
        """
        Обрабатывает попытку входа. В случае успеха открывает главное окно.
        В противном случае показывает окно об ошибке неправильно введенного
        логина и пароля.
        """

        self.entries = self.creator.entries
        entries_dict = {
            key: entry.get() for key, entry in self.entries.items()
        }
        log.info(f"Access attempt. Credentials are {entries_dict}")
        username = entries_dict['Login']
        password = entries_dict['Password']

        if auth.verify_user(username, password):
            log.info("User verified")
            auth().save_last_user(username)
            self.auth_successful = True
            self.root.destroy()  # Закрываем окно авторизации
        else:
            log.error("Credentials are wrong")
            messagebox.showerror(
                "Errore", "Username or password e` sbagliato!"
            )
        pass

    def on_close(self) -> None:
        """
        Обрабатывает ручное закрытие окна.
        Метод необходим для того, чтобы при закрытии окна входа по паролю не
        прорисовывалось главное окно.
        """

        self.auth_successful = False  # Если закрыли окно — вход не выполнен
        self.root.destroy()

    def get_default_value(self, key: str) -> str:
        """
        Ищет дефолтные значения для полей ввода.

        Parameters
        ----------
        key : str
            По этому ключу определяет из константы, должно ли быть у этого
            поля дефолтное значение.

        Returns
        -------
        str
            Если дефолтное значение есть - возвращает его. В противном случае
            будет возвращена пустая строка.
        """

        if set.LOGIN_ENTRIES[key]['default_value']:
            return auth().load_last_user()
        else:
            return ""
