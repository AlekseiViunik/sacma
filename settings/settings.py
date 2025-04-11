# ============================= PRODUCTION CONSTS =============================

# В продакшене просит залогиниться прежде всего.
# Deafult: True
PRODUCTION_MODE_ON = True

# Защита должна быть всегда включена.
# Default: True
PROTECTION_MODE_ON = True

# Включаем, если нужно тестировать GUI без екселя.
# В таком случае вместо файла будет вставлена заглушка, которая не будет
# открывать excel.
# Default: False
TEST_GUI = False

PROTECTION_1 = 20  # День. Default: 20
PROTECTION_2 = 7   # Месяц. Default: 7
PROTECTION_3 = 7   # Час. Default: 7
PROTECTION_4 = 2025  # Год. Default: 2025


# ============================== EXCEL SETTINGS ===============================

# Делает, с которым работает программа, видимым.
# Default: False
EXCEL_VISIBILITY = False

# Отображение предупреждений в Excel.
# Default: False
EXCEL_DISPLAY_ALERTS = False

# Сохраняет изменения в файле Excel перед закрытием.
# Default: 0
EXCEL_SAVE_CHANGES = 0

# Обновление ссылок при открытии файла Excel.
# Default: 0
EXCEL_UPDATE_LINKS = 0

# ================================== LOGGING ==================================

# Имя логгера. Default: "AppLogger"
APP_LOGGER = "AppLogger"

# Max number of the log file lines. Default: 20000
MAX_LOG_LINES = 20000

# Log file name. Default: "app.log"
LOG_FILE_NAME = "app.log"

# Log coding type. Default: "utf-8"
STR_CODING = "utf-8"

# Log folder name. Default: "logs"
LOGS_FOLDER_NAME = "logs"

# Формат логов.
# Default: "%(asctime)s [%(levelname)s] %(message)s"
LOGS_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"

# На один уровень вверх в пути к файлу/папке
ONE_LEVEL_UP_FOLDER = ".."

# Открытие файла для чтения
# Default: "r"
FILE_READ = "r"

# Открытие файла для записи
# Default: "w"
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
WRONG_OLD_PATH = "Old path is wrong!"
LOGIN_ERROR = "Login error"
CHANGE_PASS_ERROR = "Change password error"
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
PREPARE_DICT = "Prepare dictionary where key is cell address"
CLOSE_EXCEL = "Close excel file"
EMPTY_FIELDS_ERROR = "One (or more) of the required fields is empty!"
CHANGE_PASS_SUCCESS = "Password has been changed successfully!"
USER_NOT_FOUND = "User not found!"
EMAIL_NOT_FOUND = "Email not found!"
UNKNOWN_ERROR = "Unknown error! Call the developer!"
FAILED_TO_DECODE = "Failed to decode JSON"
PASSWORD_IS_WEAK = (
    "Password is weak! It should contain at least:\n"
    "- 8 characters\n"
    "- 1 Uppercase letter\n"
    "- 1 Lowercase letter\n"
    "- 1 Digit\n"
    "- 1 Special character"
)
TRYING_RECOVER_PASSWORD = "Trying to recover password"
RECOVER_ERROR = "Couldn't recover password!"

# ============================ LOG DYNAMIC MESSAGES ===========================

CREATE_WINDOW_WITH_CONF = "Create window with config: {0}"
CONFIG_LOADED_SUCCESSFULLY = "Config loaded successfully: {0}"
SHOULD_BE_MORE_THAN = "{0} should be more than {1}"
SHOULD_BE_LESS_THAN = "{0} should be less than {1}"
IS_NOT_NUMERIC = "{0} is not numeric"
IS_LESS_THAN = "{0} is less than min possible ({1})"
IS_GREATER_THAN = "{0} is greater than max possible ({1})"
IS_NOT_NATURAL = "{0} is not natural"
IS_NOT_MULTIPLE = "{0} is not multiple of {1}"
SHOULD_BE_MULTIPLE = "Should be multiple of {0}"
ERROR_CAUGHT = "Error caught: {0}"
BUTTON_PRESSED = "{0} button has been pressed!"
CREATE_WIDGET = "Create {0}: {1}"
CREATE_LAYOUT = "Create a layout. Type {0}"
PATH_IS = "The path is {0}"
CONFIG_IS = "Config is {0}"
USER_CREATED = "User {0} is created!"
MANDATORY_FIELDS = "The following fields are mandatory: {0}!"
MANDATORY_FIELD = "The field '{0}' is mandatory!"
MISSING_FIELDS = "Missing fields are {0}"
FULFILLED_FIELDS = "Fulfilled fields are: {0}!"
CHECK_USER_EXISTS = "Check if the user {0} with pass '{1}' exists"
LAST_USER_FOUND = "Last user found: {0}"
VAR_IS_MISSING = "Variable {0} is missing in the 'data'"
CHECK_KEY = "Check {0}"
CHECK_KEY_FAILED = "{0} hasn't passed"
DATA_TO_BE_CHECKED = "Data to be checked is: {0}"
INSERT_IN_THE_CELL = "Insert {0} in the {1} cell of the worksheet '{2}'"
DICT_PREPARED = "Dictionary is prepared: {0}"
EXCEL_FILE_PATH = "Excel file path is {0}"
EXCEL_LAUNCH_ERROR = "Launching excel error: {0}"
WORKBOOK_OPENING_ERROR = "Didn't manage to open workbook: {0}"
EXCEL_DATA_IS = "Excel data is {0}"
TRYING_TO_CHANGE_PASS = "Trying to change pass for {0}"
DELETE_USER_ERROR = "Couldn't delete user {0}: {1}"
CANT_CLEAR_LOG = "Can't check or clear log {0}: {1}"
MAIL_ERROR = "Mail error: {0}"
EMAIL_IS_NOT_VALID = "Email is not valid: {0}"
SAVE_USER_SETTINGS_ERROR = (
    "Couldn't save user settings for {0}: {1}"
)
SAVE_USER_SETTINGS_SUCCESS = (
    "User settings for {0} have been saved successfully!"
)

# ============================== STATIC MESSAGES ==============================
BASE_CHECK_FAILED = "Error! you have different base pieces chosen!"
DIAGONALS_CHECK_FAILED = "Error! Check diagonals and traverses amount!"
RECOVER_PASS_SUBJECT = "Recover password"
RECOVER_SUCCESS = "Done!"
RECOVER_SUCCESS_MESSAGE = (
    "Done! Check your email for the new password.\n"
    "Check the spam folder if you don't see it in the inbox.\n"
    "Don't forget to change it!"
)
CHANGE_GROUP_ERROR = "Couldn't change group!"

# ============================== DYNAMIC MESSAGES =============================

MIN_FAILED_MSG = "{0} should be more than {1}. You have {2}"
MAX_FAILED_MSG = "{0} should be less than {1}. You have {2}"
NUM_FAILED_MSG = "{0} should be numeric. You have {1}"
NAT_FAILED_MSG = "{0} should be positive and numeric. You have {1}"
MULT_FAILED_MSG = "{0} should be multiple of {1}. You have {2}"
EXISTS_FAILED_MSG = "{0} field should not be empty"
EXCEPTION_MSG_TEMPLATE = "{0}: {1} in {2}() at {3}:{4}"
DIAGONALS_TRAVERSE = "n_diagonals_{0} == n_traverse_{0} - 1"
GREETING_MSG = "{0} {1}!"
MANDATORY_FIELD_LABEL = "*{0}"
CONCAT_TWO_MSGS = "{0} {1}"
ADD_COLON = "{0}: "
WRONG_EMAIL = "R U sure that email '{0}' is email?"
WRONG_EMAIL_FORGOT_PASS = (
    "Worng email ({0}) is passed when the user tried to recover the password"
)

# =========================== STATIC DICTIONARY KEYS ==========================

PRICE = "price"
WEIGHT = "weight"
ERROR = "error"
USERNAME = "username"
PASSWORD = "password"
REPEAT_PASSWORD = "repeat_password"
OLD_PASSWORD = "old_password"
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
ALIGNV = "align_v"
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
BORDER = "border"
INDEPENDENT = "independent"
VALIDATIONS = "validations"
CUSTOM_VALIDATIONS = "custom_validations"
DIAGONALS_CHECK = "diagonals_check"
CHECKS = "checks"
ERROR_MESSAGE = "error_message"
BOLD = "bold"
TRAVI = "Travi"
TG = "TG"
SAT = "SAT",
PIECES = "pieces"
IS_CORRECT = "is_correct"
SLASH = "/"
CONVERTATION = "convertation"
EXE_FROZEN = "frozen"
EXCEL_PATH = "excel_path"
OPEN_EXCEL = "Open excel"
EXCEL_IS_OPENED = "Excel is opened"
WORKBOOK_IS_OPENED = "Workbook is opened"
EXCEL_APP = "Excel.Application"
CHECK_RESULT = "check_result"
RESPONSE = "response"
RESPONSE_LABELS = "response_labels"
DISABLED = "disabled"
ALEX = "alex"
SACMA = "SACMA"
SURNAME = "surname"
GREETING = "greeting"
CHANGE_PASSWORD = "Change\nPassword"
LOGOUT = "Logout"
SIGNORI = "Signor(a) "
IMAGE = "image"
PATH = "path"
SCALED_CONTENTS = "scaled_contents"
LOGO = "logo"
AUTHOR = "author"
SETSPACING = "setSpacing"
SIZE_BLOCKER = "size_blocker"
SACMA_APP = "sacma.app"
DECRYPTION = "decryption"
ENCRYPTION = "encryption"
ALLOWED_TO_GROUPS = "allowed_to_groups"
GROUP = "group"
OPEN_DELETE_USER = "open_delete_user"
BUTTON_COLOR = "button_color"
GET_FROM_FILE = "get_from_file"
FILE_PATH = "file_path"
KEY = "key"
EMAIL = "email"
USERGROUP = "usergroup"

# ========================== DYNAMIC DICTIONARY KEYS ==========================
SECTION_I = "section_{0}"

# =============================== NUMBER CONSTS ===============================
MIDDLE_DETERMINANT_DIVIDER = 2  # Default: 2
TOP_LEFT_X = 40  # Default: 40
TOP_LEFT_Y = 50  # Default: 50
SET_TO_ZERO = 0  # Default: 0
SET_TO_ONE = 1  # Default: 1
SET_TO_TWO = 2  # Default: 2
SET_TO_TWELVE = 12  # Default: 12
SET_TO_TWENTY = 20  # Default: 20
MINUS_ONE = -1  # Default: -1
MINUS_TWO = -2  # Default: -2
STEP_UP = 1  # Default: 1
STEP_DOWN = 1  # Default: 1
SPECIAL_FONT_SIZE = 16  # Default: 16
NON_STANDART_BUTTON_HEIGHT = 40  # Default: 40
NON_STANDART_BUTTON_WIDTH = 100  # Default: 100
INDENT = 4  # Default: 4
HUNDRED = 100  # Default: 100
MIN_PASS_LENGTH = 8  # Default: 8

# =============================== NAMES CONSTS ================================
LABEL = "label"  # Default: "label"
BUTTON = "button"  # Default: "button"
CHECKBOX = "checkbox"  # Default: "checkbox"
DROPDOWN = "dropdown"  # Default: "dropdown"
INPUT = "input"  # Default: "input"

# =============================== METHOD NAMES ================================
CURRENT_TEXT_METHOD = "currentText"
TEXT_METHOD = "text"
CREATE_USER_METHOD = "create_user"
CLOSE_WINDOW_METHOD = "close_window"
TOGGLE_PASSWORD_METHOD = "toggle_password"
TOGGLE_REPEAT_PASSWORD_METHOD = "toggle_repeat_password"
TOGGLE_OLD_PASSWORD_METHOD = "toggle_old_password"
TRY_LOGIN_METHOD = "try_login"
HANDLE_START_BUTTON_METHOD = "handle_start_button"
HANDLE_FORWARD_BUTTON_METHOD = "handle_forward_button"
HANDLE_CHANGE_PASS_METHOD = "handle_change_pass"
HANDLE_LOGOUT_METHOD = "handle_logout"
BROWSE_FILE_METHOD = "browse_file"
SAVE_SETTINGS_METHOD = "save_settings"
OPEN_SETTINGS_METHOD = "open_settings"
OPEN_INPUT_WINDOW_METHOD = "open_input_window"
OPEN_REGISTER_METHOD = "open_register"
SECTION_CHECK = "section_check"
BOTTOM_LAYOUT = "bottom_layout"
CHANGE_PASS = "change_pass"
DELETE_USER = "delete_user"
FORGOT_PASS = "forgot_pass"
REMEMBER_PASSWORD = "remember_password"
OPEN_LOGIN = "open_login"
OPEN_USERS_SETTINGS = "open_users_settings"
SAVE_USERS_SETTINGS = "save_users_settings"

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
    "development": "Sviluppo",
    "automatic_top": "Sommità automatico",
    "welded_base_plates": "pdb saldati",
    "typology_pb": "Tipologi PB",
    "base_thickness": "Spessore piastra",
    "boot_height": "Altezza Stivaletto",
    "base_length": "Dimensione piastra (L)",
    "base_depth": "Dimensione piastra (P)",
    "n_holes": "N fori",
}

# =============================== JSON PATHS ==================================

JSON_EXTENSION = ".json"
CONFIGS_FOLDER = "configs"
AUTH_FILE = "configs/auth.json"
SETTINGS_FILE = "configs/settings.json"
LOGIN_WINDOW_CONFIG_FILE = "configs/windows_configs/login_window.json"
REGISTER_WINDOW_CONFIG_FILE = "configs/windows_configs/register_window.json"
MAIN_WINDOW_CONFIG_FILE = "configs/windows_configs/main_window.json"
SETTINGS_WINDOW_CONFIG_FILE = "configs/windows_configs/settings_window.json"
OUTPUT_WINDOW_CONFIG_FILE = "configs/windows_configs/output_window.json"
USER_MAIN_DATA_FILE = "configs/users_configs/user_main_data.json"
TRAVI_WINDOW_CONFIG_FILE = "configs/windows_configs/travi_window.json"
CALC_CONFIG_PATH = "configs/calculator_configs/{0}.json"
CHANGE_PASS_CONFIG_FILE = "configs/windows_configs/change_pass_window.json"
ENCRYPTION_FILE = "configs/encryption.json"


# =============================== LOGO PATHS ==================================

LOGO_PATH = "files/icons/logo_sacma.png"
ICON_PATH = "files/icons/logo_s.ico"

# ============================ ITALIAN STR CONSTS =============================
PRICE_IT = "Prezzo"
PREPARATION_IT = "Approntamento"
WEIGHT_IT = "Peso"
NOT_FOUND_IT = "non trovato"
DEVELOPMENT_IT = "Sviluppo"
START_IT = "Invia"
FORWARD_IT = "Avanti"

ROUNDING_LIMIT = "0.01"

FILE_NAME_CONNECTOR = "_"
LISTING_CONNECTOR = ", "

PRE_MSG_STANDART = "Result"

TYPE_INFO = "info"

# ================================== SYMBOLS ==================================
EURO_SYMBOL = "€"
KILO_SYMBOL = "Kg"
EQUALS_SYMBOL = "="
POINT_SYMBOL = "."
EMPTY_STRING = ""
COMMA_SYMBOL = ","
SPACE_SYMBOL = " "
LEFT_BRACKET_SYMBOL = "("
RIGHT_BRACKET_SYMBOL = ")"
METERS_SYMBOL = "m"
QUESTION_MARK = "?"

# ============================ REGEX PATTERNS =================================
FLOAT_REGEX = r"\d+(,\d+)?"
VARIABLE_REGEX = r"[a-zA-Z_][a-zA-Z0-9_]*"
NUMBERS_N_OPERATORS_REGEX = r"^[0-9.\s()+\-*/]+$"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SPECIAL_CHARS = "[!@#$%^&*()_+={}[]:;\"'<>?,./\\|`~]"
COMMON_SPECIAL_CHARS = "!@#$%^&*()_+"
EXCEL_FILES_FILTER = "Excel Files (*.xlsx *.xls)"
CHOSE_FILE = "Chose file"

# ============================ LAYOUTS AND WIDGETS ============================
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

BG_COLOR = "background-color: {0}"
FONT_COLOR = "color: {0}"
MARGIN_TOP = "margin-top: 10px;"

# ============================ VALIDATION KEYS ================================
VALIDATION_MIN = "min"
VALIDATION_MAX = "max"
VALIDATION_NUMERIC = "numeric"
VALIDATION_NATURAL = "natural"
VALIDATION_MULTIPLE = "multiple"
VALIDATION_EXISTS = "exists"

# ============================= GREETING MESSAGES =============================
GOOD_MORNING = "Buongiorno"
GOOD_AFTERNOON = "Buon pomeriggio"
GOOD_EVENING = "Buonasera"
GOOD_NIGHT = "Buonanotte"
MORNING_HOUR = 6
DAY_HOUR = 14
EVENING_HOUR = 17
NIGHT_HOUR = 22

# =============================== MAIL SETTINGS ===============================

SMTP_SERVER_KEY = "SMTP_SERVER"
SMTP_PORT_KEY = "SMTP_PORT"
EMAIL_ADDRESS_KEY = "EMAIL_ADDRESS"
EMAIL_PASSWORD_KEY = "EMAIL_PASSWORD"
SUBJECT = "Subject"
FROM = "From"
TO = "To"

D_GREETING = "Good afternoon, {0}!"
GREETING = "Good afternoon!"
RECOVER_MAIL_MESSAGE = """
        {0}

        Вы запросили восстановление пароля.

        Ваш временный пароль: {1}

        Пожалуйста, измените его сразу после входа в систему.

        Если это были не вы, то париться не очем. Злоумышленники не смогут
        ничего сделать, поскольку личных данных мы не храним, БД у нас нет,
        и вообще приложение не представляет серьезной ценности ни для кого
        особо, кроме нас.

        С уважением,
        Ваша команда.
        """
