from PyQt6.QtWidgets import QLineEdit

from handlers.input_data_handler import InputDataHandler
from handlers.json_handler import JsonHandler
from handlers.user_data_handler import UserDataHandler
from helpers.authenticator import Authenticator
from settings import settings as set
from logic.logger import logging as log
from .base_window import BaseWindow


class RegisterWindow(BaseWindow):

    CONFIG_FILE = set.REGISTER_WINDOW_CONFIG_FILE

    def __init__(self) -> None:
        super().__init__()
        self.auth_json_handler = JsonHandler(set.AUTH_FILE)
        self.auth_successful: bool = False
        self.auth = Authenticator()
        self.input_data_handler = InputDataHandler()
        self.user_data_handler = UserDataHandler()

        self.init_ui()

    def create_user(self):
        log.info("Button Create has been pressed")
        all_inputs = self.input_data_handler.collect_all_inputs(
            self.creator.input_fields,
            self.creator.chosen_fields
        )
        log.info(f"Fulfilled fields are: {all_inputs}")
        difference = self.input_data_handler.check_mandatory(
            all_inputs,
            self.creator.mandatory_fields
        )
        if difference:
            log.error("Check failed. Not all necessary fields were fulfilled")
            log.error(f"Missing fields are {difference}")
            if len(difference) == 1:
                err_msg = f"The field '{difference[0]}' is mandatory!"
            else:
                missing_fields = ', '.join(difference)
                err_msg = (
                    f"The following fields are mandatory: {missing_fields}!"
                )
            self.input_data_handler.show_error_messagebox(
                "Creation failed",
                err_msg,
                self
            )
            return

        if all_inputs['password'] != all_inputs['repeat_password']:
            log.error("Check failed. Pass and its repeat are different")
            self.input_data_handler.show_error_messagebox(
                "Creation failed",
                "Password and its repeat are not identical",
                self
            )
            return
        username = all_inputs['username']
        if not self.auth.register_user(
            all_inputs['username'],
            all_inputs['password']
        ):
            log.error("Creation failed. User is already exists")
            self.input_data_handler.show_error_messagebox(
                "Creation failed",
                "User is already exists",
                self
            )
            return
        else:
            log.info(
                "Creation succesfull. Login-Pass pair has been added to the DB"
            )
            log.info("Trying to add user data")
            self.user_data_handler.add_new_user_data(all_inputs)
            self.input_data_handler.show_success_messagebox(
                "Success!",
                f"User {username} is created!",
                self
            )
            self.close()

    def toggle_password(self, checkbox, field="password"):
        if checkbox.isChecked():
            log.info("Checkbox for password is marked as 'checked'")
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            log.info("Checkbox for password is marked as 'unchecked'")
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Password
            )
