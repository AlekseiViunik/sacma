from tkinter import messagebox

from gui.type_classes.abstract_base_type import AbstractBaseType
from logic.authenticator import Authenticator


class CreateUserWindow(AbstractBaseType):
    def __init__(self, root, type=None, entry_widgets=None):
        super().__init__(root, type, entry_widgets)
        self.auth = Authenticator()

    def calculate(self):
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
