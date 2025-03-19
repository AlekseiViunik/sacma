from handlers.json_handler import JsonHandler
from logic.logger import logger as log
from settings import settings as set


class UserDataHandler:
    def __init__(self):
        self.auth_json_handler = JsonHandler(set.USER_MAIN_DATA_FILE)

    def add_new_user_data(self, user_data):
        username = user_data.pop('username')
        if user_data.get('password'):
            user_data.pop('password')
        if user_data.get('repeat_password'):
            user_data.pop('repeat_password')

        log.info("Trying to get all users data to add another user data")
        log.info(f"The path is {set.USER_MAIN_DATA_FILE}")
        all_data = self.auth_json_handler.get_all_data()

        if all_data:
            log.info("Config data received")
        else:
            log.error("Couldn't get the data from the file!")

        all_data[username] = user_data
        log.info("Add new user data")
        self.auth_json_handler.rewrite_file(all_data)

        new_data = self.auth_json_handler.get_all_data()

        if new_data.get(username) and new_data[username] == user_data:
            log.info("New user data has been added")
        else:
            log.info("Couldn't add new user data")
