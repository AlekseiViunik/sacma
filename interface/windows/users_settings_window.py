from logic.helpers.helper import Helper
from .base_window import BaseWindow
from interface.windows.messagebox import Messagebox
from logic.handlers.json_handler import JsonHandler
from settings import settings as sett


class UsersSettingsWindow(BaseWindow):
    """
    Окно для изменения настроек пользователей. На данном этапе
    реализована возможность изменения только группы пользователя.

    Attributes
    ----------
    - window_name: str
        Имя окна.
    - file_path: str
        Путь к конфигу для построения окна. Передаётся в родительский
        класс BaseWindow.
    """

    def __init__(
        self,
        window_name: str,
        file_path: str,
    ) -> None:
        super().__init__(file_path)
        self.window_name: str = window_name

        self.init_ui()

    def save_users_settings(self) -> None:
        """
        Сохраняет измененные настройки выбранного бзера. На данный момент
        реализована возможность изменения только группы пользователя.
        """

        user_data_json_handler = JsonHandler(
            sett.USER_MAIN_DATA_FILE, True
        )

        try:
            username = self.creator.chosen_fields[sett.USERNAME].currentText()
            usergroup = (
                self.creator.chosen_fields[sett.USERGROUP].currentText()
            )
            userdata = user_data_json_handler.get_all_data()
            userdata[username][sett.GROUP] = usergroup

            user_data_json_handler.rewrite_file(userdata)

        except Exception as e:
            Helper.log_exception(e)
            Messagebox.show_messagebox(
                sett.CHANGE_GROUP_ERROR,
                sett.SAVE_USER_SETTINGS_ERROR.format(username, e),
                None,
                exec=True
            )
            return

        Messagebox.show_messagebox(
            sett.SUCCESS,
            sett.SAVE_USER_SETTINGS_SUCCESS.format(username),
            None,
            type=sett.TYPE_INFO,
            exec=True
        )
        self.close()
