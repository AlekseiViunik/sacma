# ================================== LOGGING ==================================

# Max number of the log file lines. Default: 20000
MAX_LOG_LINES = 20000

# Log file name. Default: "app.log"
LOG_FILE_NAME = "app.log"

# Log coding type. Default: "utf-8"
STR_CODING = "utf-8"

# ============================= LOG STATIC MESSAGES ===========================

TRYING_LOGIN = "Trying to acces the app"
SUCCESSFUL_LOGIN = "Login is successful!"
UNSUCCESSFUL_LOGIN = "Application closed due to unsuccessful login"
NEW_APP_START = "Launching new interface"
FAILED_VALIDATION = "The data is wrong!"
INSERT_DATA_INTO_EXCEL = "Insert prepared data into the excel worksheet"
REFRESH_EXCEL = "Refresh table data to recalculate formulas"
DATA_VALIDATION = "Check data before preparing it"
SUCCESSFUL_VALIDATION = "The data is correct!"
GETTING_EXCEL_DATA = "Getting excel data"
ROUNDING_UP_DATA = "Rounding up data"
NOT_DECIMAL_ERROR = "All data should have Decimal type!"
UNACCEPTABLE_OPERATORS = "Выражение содержит недопустимые символы"
JSON_GET_ALL_DATA = "JsonHandler works. Method get_all_data."
JSON_GET_VALUE_BY_KEY = "JsonHandler works. Method get_value_by_key."
JSON_GET_VALUES_BY_KEYS = "JsonHandler works. Method get_values_by_keys."
JSON_REWRITE_FILE = "JsonHandler works. Method rewrite_file."
JSON_WRITE_INTO_FILE = "JsonHandler works. Method write_into_file."
TRYING_ADD_USER_DATA = "Trying to add a new user data"
USER_DATA_IS_ADDED = "New user data has been added"
USER_DATA_IS_NOT_ADDED = "Couldn't add new user data"

# ============================== DICTIONARY KEYS ==============================

PRICE = "price"
WEIGHT = "weight"
ERROR = "error"
USERNAME = "username"
PASSWORD = "password"
REPEAT_PASSWORD = "repeat_password"

# ================================ Translator =================================
# TODO make a dictionary dynamic to translate frases
DICTIONARY = {
    "height": "Altezza",
    "width": "Larghezza",
    "thickness": "Spessore",
    "length": "Lunghezza",
    "special_hook": "Staffa speciale",
    "standart_hook": "Staffa tipo standart",
    "amount": "Quantità",
    "price": "Prezzo",
    "weight": "Peso",
    "support": "Appoggio",
    "base": "Base",
    "only_strut": "Solo montante",
    "section": "Sezione",
    "type": "Tipo",
    "weight": "Peso",
    "skates": "Pattini",
    "n_skates": "N pattini",
    "pieces": "Tratti",
    "depth": "Profondità",
    "n_diagonals_15/10": "N diagonali 15/10",
    "n_diagonals_20/10": "N diagonali 20/10",
    "n_diagonals_25/10": "N diagonali 25/10",
    "n_diagonals_30/10": "N diagonali 30/10",
    "n_traverse_10/10": "N traversi 10/10",
    "n_traverse_15/10": "N traversi 15/10",
    "diagonal_15/10": "Diagonale 15/10",
    "diagonal_20/10": "Diagonale 20/10",
    "diagonal_25/10": "Diagonale 25/10",
    "diagonal_30/10": "Diagonale 30/10",
    "traverse_10/10": "Traverse 10/10",
    "traverse_15/10": "Traverse 15/10",
    "fold": "Piega",
    "profile": "Profilo",
    "element": "Elemento",
    "element_type": "Tipo elemento",
    "inclined_invitations?": "Inviti inclinati?",
    "height_1": "Altezza 1",
    "height_2": "Altezza 2",
    "height_3": "Altezza 3",
    "n_diagonals_1": "N diagonali 1",
    "n_diagonals_2": "N diagonali 2",
    "n_diagonals_3": "N diagonali 3",
    "n_diagonals_15/10_1": "N diagonali 15/10 1",
    "n_diagonals_20/10_1": "N diagonali 20/10 1",
    "n_diagonals_25/10_1": "N diagonali 25/10 1",
    "n_diagonals_30/10_1": "N diagonali 30/10 1",
    "n_traverse_10/10_1": "N traversi 10/10 1",
    "n_traverse_15/10_1": "N traversi 15/10 1",
    "n_diagonals_15/10_2": "N diagonali 15/10 2",
    "n_diagonals_20/10_2": "N diagonali 20/10 2",
    "n_diagonals_25/10_2": "N diagonali 25/10 2",
    "n_diagonals_30/10_2": "N diagonali 30/10 2",
    "n_traverse_10/10_2": "N traversi 10/10 2",
    "n_traverse_15/10_2": "N traversi 15/10 2",
    "n_diagonals_15/10_3": "N diagonali 15/10 3",
    "n_diagonals_20/10_3": "N diagonali 20/10 3",
    "n_diagonals_25/10_3": "N diagonali 25/10 3",
    "n_diagonals_30/10_3": "N diagonali 30/10 3",
    "n_traverse_10/10_3": "N traversi 10/10 3",
    "n_traverse_15/10_3": "N traversi 15/10 3",
}

# ===================================Login=====================================
AUTH_FILE = "auth.json"
LOGIN_WINDOW_CONFIG_FILE = "configs/windows_configs/login_window.json"
REGISTER_WINDOW_CONFIG_FILE = "configs/windows_configs/register_window.json"
MAIN_WINDOW_CONFIG_FILE = "configs/windows_configs/main_window.json"
SETTINGS_WINDOW_CONFIG_FILE = "configs/windows_configs/settings_window.json"
SETTINGS_FILE = "settings.json"
OUTPUT_WINDOW_CONFIG_FILE = "configs/windows_configs/output_window.json"
USER_MAIN_DATA_FILE = "configs/users_configs/user_main_data.json"

PRODUCTION_MODE_ON = False


ROUNDING_LIMIT = "0.01"

VARIABLE_REGEX = r"[a-zA-Z_][a-zA-Z0-9_]*"
NUMBERS_N_OPERATORS_REGEX = r"^[0-9.\s()+\-*/]+$"
