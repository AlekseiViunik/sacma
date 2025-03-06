import tkinter as tk
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

        Helper.center_window(300, 200, self.root)

        tk.Label(root, text="Login:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.creator.create_button("Login", self.login)
        self.root.protocol(set.ON_CLOSING_WINDOW, self.on_close)

    def login(self):
        """Обрабатывает попытку входа."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if auth.verify_user(username, password):
            auth.save_last_user(username)
            self.auth_successful = True
            self.root.destroy()  # Закрываем окно авторизации
        else:
            messagebox.showerror(
                "Errore", "Username or password e` sbagliato!"
            )

    def on_close(self):
        """Обрабатывает ручное закрытие окна."""
        self.auth_successful = False  # Если закрыли окно — вход не выполнен
        self.root.destroy()
