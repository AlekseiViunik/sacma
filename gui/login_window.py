import tkinter as tk
from tkinter import messagebox
from logic.authenticator import Authenticator as auth


class LoginWindow:
    """Окно авторизации."""

    def __init__(self, root):
        self.root = root
        self.root.title("Aouthorization")
        self.root.geometry("300x180")
        self.root.resizable(False, False)

        tk.Label(root, text="Login:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        """Обрабатывает попытку входа."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if auth.verify_user(username, password):
            auth.save_last_user(username)
            self.root.destroy()  # Закрываем окно авторизации
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")
