import math
import tkinter as tk


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SACMA")
        self.root.geometry("500x250")
        self.center_window(self.root, 600, 300)
        self.buttons = [
            "Fiancate", "Travi", "Tasselli", "Satellitare",
            "Pianetti", "Gragliato", "Travi di battuta",
            "Angolari per automatici", "Gravita leggera",
            "Option di sicurezza"
        ]

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        cols = 3
        rows = math.ceil(len(self.buttons) / cols)

        max_width = max(len(name) for name in self.buttons)

        for i, name in enumerate(self.buttons):
            btn = tk.Button(
                frame,
                text=name,
                height=2,
                width=max_width,
                bg="#d9d9d9",
                # relief="flat",  # no border
                command=lambda n=name: self.open_window(n)
            )
            btn.grid(
                row=i // cols,
                column=i % cols,
                padx=10,
                pady=10,
                sticky="nsew"
            )

        for i in range(cols):
            self.root.columnconfigure(i, weight=1)
        for i in range(rows):
            self.root.rowconfigure(i, weight=1)

    def open_window(self, name):
        new_window = tk.Toplevel(self.root)
        new_window.title(name)
        new_window.geometry("400x300")
        self.center_window(new_window, 400, 300)
        tk.Label(new_window, text=name, font=("Arial", 14)).pack(expand=True)

    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
