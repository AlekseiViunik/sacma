from tkinter import messagebox
from gui.widget_creator import WidgetCreator
from logic.authenticator import Authenticator as auth
from gui.helper import Helper
from settings import settings as set


class LoginWindow:
    """Окно авторизации."""

    def __init__(self, root):
        self.root = root
        self.root.title("Authorization")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        self.auth_successful = False
        self.creator = WidgetCreator(self.root, None)
        self.entries = None

        Helper.center_window(300, 200, self.root)

        frame = self.creator.create_frame("login")
        row = 1
        for label in set.LOGIN_ENTRIES.keys():
            self.creator.create_component(
                frame,
                label,
                None,
                row,
                is_entry=True,
                is_hide=set.LOGIN_ENTRIES[label]["is_hide"]
            )
            row += 1
        self.creator.create_button("Login", self.login)
        self.root.protocol(set.ON_CLOSING_WINDOW, self.on_close)

    def login(self):
        """Обрабатывает попытку входа."""
        self.entries = self.creator.entries
        entries_dict = {
            key: entry.get() for key, entry in self.entries.items()
        }

        username = entries_dict["Login"]
        password = entries_dict["Password"]

        if auth.verify_user(username, password):
            auth.save_last_user(username)
            self.auth_successful = True
            self.root.destroy()  # Закрываем окно авторизации
        else:
            messagebox.showerror(
                "Errore", "Username or password e` sbagliato!"
            )
        pass

    def on_close(self):
        """Обрабатывает ручное закрытие окна."""
        self.auth_successful = False  # Если закрыли окно — вход не выполнен
        self.root.destroy()
