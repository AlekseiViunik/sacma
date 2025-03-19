from PyQt6.QtWidgets import (
    QWidget, QPushButton
)

from handlers.input_data_handler import InputDataHandler
from handlers.json_handler import JsonHandler
from handlers.user_data_handler import UserDataHandler
from interface.creator import Creator
from helpers.helper import Helper
from helpers.authenticator import Authenticator
from settings import settings as set
from logic.logger import logging as log


class RegisterWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.window_width = 0
        self.window_height = 0
        self.auth_json_handler = JsonHandler(set.AUTH_FILE)
        self.config_json_handler = JsonHandler(set.REGISTER_WINDOW_CONFIG_FILE)
        self.auth_successful: bool = False
        self.creator = None
        self.auth = Authenticator()
        self.input_data_handler = InputDataHandler()
        self.user_data_handler = UserDataHandler()

        self.init_ui()

    def init_ui(self) -> None:
        """
        Создает интерфейс окна настроек.
        """

        log.info("Create a window for user creation")
        # Загружаем конфиг
        log.info("Trying to get config data for create user window")
        log.info(f"The path is {set.REGISTER_WINDOW_CONFIG_FILE}")
        config = self.config_json_handler.get_all_data()

        if config:
            log.info("Config data received")
            log.info(f"Config is: {config}")
        else:
            log.error("Couldn't get the data from the file!")

        self.setWindowTitle(config['window_title'])
        self.window_width = int(config['window_width'])
        self.window_height = int(config['window_height'])
        # Helper.move_window_to_center(self)
        Helper.move_window_to_top_left_corner(self)

        log.info("Use creator to place widgets on the create user window")
        self.creator = Creator(config, self)
        self.creator.create_widget_layout(self, config["layout"])

    def connect_callback(
        self,
        button: QPushButton,
        callback_name: str,
        params: dict = {}
    ):
        if callback_name == "create_user":
            button.clicked.connect(self.create_user)

        elif callback_name == "close_window":
            button.clicked.connect(self.cancel)

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

    def cancel(self):
        log.info("Cancel button has been pressed")
        self.close()
