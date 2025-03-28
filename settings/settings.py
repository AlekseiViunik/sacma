# ================================== LOGGING ==================================

# Max number of the log file lines. Default: 20000
MAX_LOG_LINES = 20000

# Log file name. Default: "app.log"
LOG_FILE_NAME = "app.log"

# Log coding type. Default: "utf-8"
STR_CODING = "utf-8"

LOGS_FOLDER_NAME = "logs"

ONE_LEVEL_UP_FOLDER = ".."

FILE_READ = "r"
FILE_WRITE = "w"

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
TRYING_TO_REWRITE_SETTINGS = "Trying to rewrite settings file"
USER_DATA_IS_ADDED = "New user data has been added"
USER_DATA_IS_NOT_ADDED = "Couldn't add new user data"
HASHING_PASS = "Hashing the pass"
SAVE_LAST_USER = "Save last user"
FAILED_GET_JSON_DATA = "Couldn't get the data from the file!"
USE_CREATOR = "Using creator to generate UI layout"
CANCEL_BUTTON_PRESSED = "Cancel button has been pressed"
INVIA_BUTTON_PRESSED = "Button Invia has been pressed"
BROWSE_BUTTON_PRESSED = "Browse button has been pressed"
TRY_BUTTON_PRESSED = "Try button is pressed"
SAVE_BUTTON_PRESSED = "Save button is pressed"
SETTINGS_BUTTON_PRESSED = "Settings button has been pressed!"
CREATE_BUTTON_PRESSED = "Button Create has been pressed"
CREATE_USER_BUTTON_PRESSED = "Create user button has been pressed!"
START_CALCULATING = "Start calculating"
OPEN_RESPONSE_WIDGET = "Open response widget"
ADD_LAST_USER_TO_INPUT_FIELD = "Add last user to input field default value"
USER_VERIFIED = "User verified"
WRONG_CREDENTIALS = "Credentials are wrong!"
LOGIN_ERROR = "Login error"
PASS_MARKED_AS_CHECKED = "Checkbox for password is marked as 'checked'"
PASS_MARKED_AS_UNCHECKED = "Checkbox for password is marked as 'unchecked'"
PASS_REPEAT_MARKED_AS_CHECKED = (
    "Checkbox for password repeat is marked as 'checked'"
)
PASS_REPEAT_MARKED_AS_UNCHECKED = (
    "Checkbox for password repeat is marked as 'unchecked'"
)
CREATE_RESULT_WINDOW = "Create result window"
GETTING_CONF_FOR_RESULT_WINDOW = "Trying to get config data for result window"
CONF_DATA_RECEIVED = "Config data received"
MANDATORY_FIELDS_CHECK_FAILED = (
    "Check failed. Not all necessary fields were fulfilled"
)
CREATION_FAILED = "Creation failed!"
CHECK_FAILED = "Check failed."
REPEAT_IS_DIFFERENT = "Pass and its repeat are different"
USER_EXISTS = "User is already exists!"
AUTH_CREATION_SUCCESSFUL = (
    "Creation succesfull. Login-Pass pair has been added to the DB"
)
TRYING_ADD_AUTH_DATA = "Trying to add user auth data"
SUCCESS = "Success!"
REWRITING_CHECK_IS_UNAVAILABLE = "Rewriting check is temporary unavailable"
CREATE_INPUT_FIELD = "Create input field"
RERENDER_LAYOUTS = "Rerender layouts"
VALIDATION_IS_OK = "This check is OK!"
SHOULD_BE_NUMERIC = "Should be numeric"
SHOULD_BE_NATURAL = "Should be natural"
SHOULD_BE_PRESENTED = "Should be presented"
EMPTY_REQUIRED_FIELDS = "One (or more) of the required fields is empty!"
FILE_NOT_FOUND = "FILE NOT FOUND"
FNF_MESSAGE = "Required file is missing. Please contact the developer."

# ============================== DICTIONARY KEYS ==============================

PRICE = "price"
WEIGHT = "weight"
ERROR = "error"
USERNAME = "username"
PASSWORD = "password"
REPEAT_PASSWORD = "repeat_password"
LAST_USER = "lastUser"
USERS = "users"
LAYOUT = "layout"
NAME = "name"
WIDGETS = "widgets"
CHOICES = "choices"
CELLS_INPUT = "cells_input"
CELLS_OUTPUT = "cells_output"
WINDOW_TITLE = "window_title"
WINDOW_WIDTH = "window_width"
WINDOW_HEIGHT = "window_height"
TARGET_INPUT = "target_input"
DEPENDS_ON = "depends_on"
TYPE = "type"
COLUMNS = "columns"
COLUMN = "column"
TEXT = "text"
TEXT_SIZE = "text_size"
ALIGN = "align"
MANDATORY = "mandatory"
WIDTH = "width"
HEIGHT = "height"
BACKGROUND = "background"
DEFAULT_VALUE = "default_value"
HIDE = "hide"
CALLBACK = "callback"
PARAMS = "params"
OPTIONS = "options"
ALWAYS = "always"
CHANGE_WIDGETS = "change_widgets"
ACTIVE_WHEN = "active_when"
VISIBILITY_KEY = "visibility_key"
JSON_FILE_PATH = "json_file_path"
CONVERSION = "conversion"
SPECIAL_OUTPUT = "special_output"
POST_MESSAGE = "post_message"
IS_HIDE = "is_hide"
RULES = "rules"
WORKSHEET = "worksheet"
COPY_CELLS = "copy_cells"
ADDITIONAL_INPUT = "additional_input"
FORMULAS = "formulas"
ONLY_KEYS = "only_keys"
CONDITION = "condition"
MESSAGE = "message"
ROUNDINGS = "roundings"
ACTIVE_WHEN = "active_when"
WIDGET_NAME = "widget_name"
BOLD = "bold"
TRAVI = "Travi"
TG = "TG"
SAT = "SAT"

# =============================== NUMBER CONSTS ===============================
MIDDLE_DETERMINANT_DIVIDER = 2
TOP_LEFT_X = 40
TOP_LEFT_Y = 50
SET_TO_ZERO = 0
SET_TO_ONE = 1
STEP_UP = 1
STEP_DOWN = 1
SPECIAL_FONT_SIZE = 16

# =============================== NAMES CONSTS ================================
LABEL = "label"
BUTTON = "button"

# =============================== METHOD NAMES ================================
CURRENT_TEXT_METHOD = "currentText"
TEXT_METHOD = "text"
CREATE_USER_METHOD = "create_user"
CLOSE_WINDOW_METHOD = "close_window"
TOGGLE_PASSWORD_METHOD = "toggle_password"
TOGGLE_REPEAT_PASSWORD_METHOD = "toggle_repeat_password"
TRY_LOGIN_METHOD = "try_login"
HANDLE_START_BUTTON_METHOD = "handle_start_button"
BROWSE_FILE_METHOD = "browse_file"
SAVE_SETTINGS_METHOD = "save_settings"
OPEN_SETTINGS_METHOD = "open_settings"
OPEN_INPUT_WINDOW_METHOD = "open_input_window"
OPEN_REGISTER_METHOD = "open_register"


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
    "preparation": "Approntamento",
    "development": "Sviluppo"
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
TRAVI_WINDOW_CONFIG_FILE = "configs/windows_configs/travi_window.json"

PRODUCTION_MODE_ON = False
PROTECTION_MODE_ON = True
PROTECTION_YEAR = 2025
PROTECTION_MONTH = 7
PROTECTION_DAY = 20
PROTECTION_HOUR = 7

PRICE_IT = "Prezzo"
PREPARATION_IT = "Approntamento"
WEIGHT_IT = "Peso"
NOT_FOUND_IT = "non trovato"

OK_BUTTON_TITLE = "OK"
OK_BUTTON_WIDTH = 100
OK_BUTTON_HEIGHT = 50

ROUNDING_LIMIT = "0.01"

FILE_NAME_CONNECTOR = "_"
LISTING_CONNECTOR = ", "

PRE_MSG_STANDART = "Result"

TYPE_INFO = "info"

EURO_SYMBOL = "€"
KILO_SYMBOL = "Kg"
EQUALS_SYMBOL = "="
POINT_SYMBOL = "."
EMPTY_STRING = ""

VARIABLE_REGEX = r"[a-zA-Z_][a-zA-Z0-9_]*"
NUMBERS_N_OPERATORS_REGEX = r"^[0-9.\s()+\-*/]+$"

EXCEL_FILES_FILTER = "Excel Files (*.xlsx *.xls)"
CHOSE_FILE = "Chose file"


APP_LOGGER = "AppLogger"

LAYOUT_TYPE_GRID = "grid"
LAYOUT_TYPE_VERTICAL = "vertical"
LAYOUT_TYPE_HORIZONTAL = "horizontal"

WIDGET_TYPE_LABEL = "label"
WIDGET_TYPE_INPUT = "input"
WIDGET_TYPE_BUTTON = "button"
WIDGET_TYPE_DROPDOWN = "dropdown"
WIDGET_TYPE_CHECKBOX = "checkbox"

WIDGET_POS_FIRST = "first"
WIDGET_POS_LAST = "last"
WIDGET_POS_CURRENT = "current"
WIDGET_POS_MIDDLE = "middle"

ALIGN_CENTER = "center"
ALIGN_LEFT = "left"
ALIGN_RIGHT = "right"

VALIDATION_MIN = "min"
VALIDATION_MAX = "max"
VALIDATION_NUMERIC = "numeric"
VALIDATION_NATURAL = "natural"
VALIDATION_MULTIPLE = "multiple"
VALIDATION_EXISTS = "exists"
