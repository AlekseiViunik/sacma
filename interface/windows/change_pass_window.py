from PyQt6.QtWidgets import QLineEdit, QCheckBox

from helpers.authenticator import Authenticator
from interface.windows.messagebox import Messagebox

from .base_window import BaseWindow
from logic.logger import logging as log
from settings import settings as sett


class ChangePassWindow(BaseWindow):

    CONFIG_FILE = sett.CHANGE_PASS_CONFIG_FILE

    def __init__(self, username) -> None:
        super().__init__(username=username)

        self.init_ui()

    def toggle_password(
        self,
        checkbox: QCheckBox,
        field: str = sett.PASSWORD
    ) -> None:

        if checkbox.isChecked():
            if field == sett.PASSWORD:
                log.info(sett.PASS_MARKED_AS_CHECKED)
            elif field == sett.REPEAT_PASSWORD:
                log.info(sett.PASS_REPEAT_MARKED_AS_CHECKED)
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            if field == sett.PASSWORD:
                log.info(sett.PASS_MARKED_AS_UNCHECKED)
            elif field == sett.REPEAT_PASSWORD:
                log.info(sett.PASS_REPEAT_MARKED_AS_UNCHECKED)
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Password
            )

    def change_pass(self) -> None:
        old_pass = self.creator.input_fields[sett.OLD_PASSWORD].text()
        new_pass = self.creator.input_fields[sett.PASSWORD].text()
        repeat_pass = self.creator.input_fields[sett.REPEAT_PASSWORD].text()
        if (
            old_pass == sett.EMPTY_STRING or
            new_pass == sett.EMPTY_STRING or
            repeat_pass == sett.EMPTY_STRING
        ):
            Messagebox.show_messagebox(
                sett.CHANGE_PASS_ERROR,
                sett.EMPTY_FIELDS_ERROR,
                self
            )
            return

        if not Authenticator.verify_user(self.username, old_pass):
            Messagebox.show_messagebox(
                sett.CHANGE_PASS_ERROR,
                sett.WRONG_OLD_PATH,
                self
            )
            return

        if new_pass != repeat_pass:
            Messagebox.show_messagebox(
                sett.CHANGE_PASS_ERROR,
                sett.REPEAT_IS_DIFFERENT,
                self
            )
            return

        if Authenticator.update_user_password(
            self.username,
            new_pass
        ):
            Messagebox.show_messagebox(
                sett.CHANGE_PASS_SUCCESS,
                sett.CHANGE_PASS_SUCCESS,
                self,
                sett.TYPE_INFO
            )
            self.close()
        else:
            Messagebox.show_messagebox(
                sett.USER_NOT_FOUND,
                sett.USER_NOT_FOUND,
                self
            )
