from handlers.json_handler import JsonHandler

AUTH_FILE = "configs/users_configs/user_main_data.json"


class UserDataHandler:
    def __init__(self):
        self.auth_json_handler = JsonHandler(AUTH_FILE)

    def add_new_user_data(self, user_data):
        username = user_data.pop('username')
        if user_data.get('password'):
            user_data.pop('password')
        if user_data.get('repeat_password'):
            user_data.pop('repeat_password')

        all_data = self.auth_json_handler.get_all_data()
        all_data[username] = user_data
        self.auth_json_handler.rewrite_file(all_data)
