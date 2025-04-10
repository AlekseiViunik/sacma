from .base_window import BaseWindow
from handlers.json_handler import JsonHandler
from logic.logger import logger as log
from settings import settings as sett


class DeleteUserWindow(BaseWindow):

    def __init__(
        self,
        window_name: str,
        file_path: str,
    ) -> None:
        super().__init__(file_path)
        self.window_name: str = window_name

        self.init_ui()
        self.__remove_yourself_from_dropdown()

    def delete_user(self) -> None:
        auth_json_handler = JsonHandler(
            sett.AUTH_FILE, True
        )

        user_data_json_handler = JsonHandler(
            sett.USER_MAIN_DATA_FILE, True
        )

        try:
            username = self.creator.chosen_fields[sett.USERNAME].currentText()

            auth = auth_json_handler.get_all_data()
            userdata = user_data_json_handler.get_all_data()

            userdata.pop(username, None)
            auth[sett.USERS].pop(username, None)

            auth_json_handler.rewrite_file(auth)
            user_data_json_handler.rewrite_file(userdata)

            self.creator.update_dependent_layouts()
            self.__remove_yourself_from_dropdown()

        except Exception as e:
            log.error(sett.DELETE_USER_ERROR.format(username, e))
            return

    # ============================ Private Methods ============================
    # -------------------------------------------------------------------------
    def __remove_yourself_from_dropdown(self) -> None:

        dropdown = self.creator.chosen_fields[sett.USERNAME]
        current_options = [
            dropdown.itemText(i) for i in range(dropdown.count())
        ]

        if self.username in current_options:
            current_options.remove(self.username)
        dropdown.clear()
        dropdown.addItems(current_options)
