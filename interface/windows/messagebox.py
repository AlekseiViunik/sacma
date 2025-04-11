from PyQt6.QtWidgets import QMessageBox, QWidget

from settings import settings as sett


class Messagebox:
    """
    Класс, отвечающий за вывод окна с сообщением об ошибке или просто
    информационного окна.

    Methods
    -------
    - show_messagebox(title, msg, window, type, exec)
        Выводит окно об ошибке или просто информационное окно.
    """

    @staticmethod
    def show_messagebox(
        title: str,
        msg: str,
        window: QWidget | None,
        type: str = sett.ERROR,
        exec: bool = False
    ) -> None:
        """
        Выводит окно об ошибке или просто информационное окно (разница только в
        иконке) в зависимости от указанного type. Окно выводится относительно
        окна, из которого оно было вызвано.

        Parameters
        ----------
        - title: str
            Заголовок окна.

        - msg: str
            Сообщение для информации.

        - window: QWidget | None
            Окно, относительно которого выводится это окно.

        - type: str
            Default = 'error'\n
            Тип выводимого окна. Пока что доступен только тип `error`. Все
            остальное будет трактоваться как info.

        - exec: bool
            Default = False\n
            Если этот параметр TRUE, вызываем окно при помощи exec(). Программа
            останавливает свое выполнения, пока не будет нажата кнопка ОК.
            show() - напротив, асинхронен, но менее стабилен.
        """

        box = QMessageBox(window)
        box.setWindowTitle(title)
        box.setText(msg)
        box.setStandardButtons(QMessageBox.StandardButton.Ok)
        if type == sett.ERROR:
            box.setIcon(QMessageBox.Icon.Critical)
            if exec:
                box.exec()
            else:
                box.show()

        else:
            box.setIcon(QMessageBox.Icon.Information)
            box.exec()
