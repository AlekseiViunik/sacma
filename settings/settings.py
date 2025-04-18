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
LOGS_FORMAT = "%(asctime)s [%(levelname)s] [%(context)s] %(message)s"

# На один уровень вверх в пути к файлу/папке
ONE_LEVEL_UP_FOLDER = ".."

# Открытие файла для чтения
# Default: "r"
FILE_READ = "r"

# Открытие файла для записи
# Default: "w"
FILE_WRITE = "w"

# Открытие файла для записи в бинарном режиме
# Default: "wb"
FILE_WRITE_BINARY = "wb"

# ============================= LOG STATIC MESSAGES ===========================

# Backups
BACKUP_SUCCESS = "Backup was successful!"
BACKUP_IS_NEEDED = "It's time for backup!"
BACKUP_DIR_EXISTS = "Backup folder already exists!"
BACKUP_IS_NOT_NEEDED = "It's too early for backup!"
# Create something
CREATE_NEW_NACKUP_FOLDER = "Creating new backup folder!"
CREATE_EXCEL_HANDLER_OBJECT = "Create excel handler object"
CREATE_DROPBOX_HANDLER_OBJECT = "Create dropbox handler object"
CREATE_CREATOR_OBJECT = "Create creator object"
CREATE_MAIN_WINDOW = "Create main window"
CREATE_SETTINGS_WINDOW = "Create 'Settings' window"
CREATE_REGISTER_WINDOW = "Create 'Register' window"
CREATE_LOGIN_WINDOW = "Create 'Login' window"
CREATE_MY_PROFILE_WINDOW = "Create 'My profile' window"
CREATE_DELETE_USER_WINDOW = "Create 'Delete user' window"
CREATE_USERS_SETTINGS_WINDOW = "Create 'Users settings' window"
CREATE_USER_BUTTON_PRESSED = "'Create user' button has been pressed!"
CREATE_SETTINGS_FILE_IF_NOT_EXISTS = (
    "Create settings file if it doesn't exist."
)
# Fails/errors
FNF_MESSAGE = "Required file is missing. Please contact the developer."
FAILED_TO_DECODE = "Failed to decode JSON"
BASE_CHECK_FAILED = "Error! you have different base pieces chosen!"
DIAGONALS_CHECK_FAILED = "Error! Check diagonals and traverses amount!"
WRONG_OLD_PATH = "Old path is wrong!"
CHANGE_PASS_ERROR = "Change password error"
LOGIN_ERROR = "Login error"
CREATION_FAILED = "Creation failed!"
FILE_NOT_FOUND = "FILE NOT FOUND"
EMAIL_NOT_FOUND = "Email not found!"
UNKNOWN_ERROR = "Unknown error! Call the developer!"
RECOVER_ERROR = "Couldn't recover password!"
CHANGING_FAILED = "Changing failed!"
FILE_ID_PARSING_FALIED = "File ID parsing failed!"
FAILED_VALIDATION = "The data is wrong!"
CANT_DELETE_EXCEL_FILE = (
    "Couldn't delete temp excel file. That means that the process is still "
    "working and we need to kill it firs! Call "
    "__close_excel_if_it_is_already_opened() method"
)
# Get something
GET_LAST_PID = "Get last PID of the excel app from settings file"
GETTING_EXCEL_LINK = "Getting excel link from settings file"
GETTING_PID = "Getting PID of the excel app by HWND"
GETTING_EXCEL_DATA = "Getting excel data"
GETTING_CALC_CONFIG = "Getting element's config for calculation"
GETTING_POST_MESSAGE = "Getting post message if exists"
# Pressed buttons
SETTINGS_BUTTON_PRESSED = "'Impostazioni' button has been pressed!"
LOGOUT_BUTTON_PRESSED = "'Logout' button has been pressed!"
MY_PROFILE_BUTTON_PRESSED = "'My profile' button has been pressed!"
CANCEL_BUTTON_PRESSED = "Cancel button has been pressed"
SETTINGS_WERE_CHANGED = (
    "Settings were changed! Restart excel and rerender main window"
)
# Success/unsuccess
SUCCESS = "Success!"
SUCCESSFUL_LOGIN = "Login is successful! Change log folder"
UNSUCCESSFUL_LOGIN = "Application closed due to unsuccessful login"
CHANGE_PASS_SUCCESS = "Password has been changed successfully!"
RECOVER_SUCCESS = "Done!"
RECOVER_SUCCESS_MESSAGE = (
    "Done! Check your email for the new password.\n"
    "Check the spam folder if you don't see it in the inbox.\n"
    "Don't forget to change it!"
)
CHANGE_USER_DATA_SUCCESS = "Successful change!"
# Tries to do something
TRYING_LOGIN = "Trying to acces the app"
TRYING_BACKUP = "Trying to backup the configs folder"
TRYING_TO_GET_LAST_BACKUP = "Trying to get last backup date"
TRYING_TO_OPEN_EXCEL = "Trying to open excel file"
TRYING_TO_OPEN_EXCEL_AGAIN = "Trying to open excel file again."
TRYING_TO_OPEN_EXCEL_WB = "Trying to open excel workbook and set its property"
TRYING_TO_RENDER_WINDOW = "Trying to render window"
TRYING_TO_DELETE_EXCEL_FILE = "Trying to delete temp excel file"
TRYING_TO_DELETE_EXCEL_FILE_2 = (
    "Trying to delete temp excel file after killing process"
)
TRYING_TO_OPEN_DOWNLOADED_FILE = (
    "Trying to open downloaded file"
)
TRYING_TO_CLOSE_EXCEL = "Trying to close excel file if it's already opened."
TRYING_TO_DOWNLOAD_EXCEL = "Trying to call download_excel method"
TRYING_TO_OPEN_EXCEL_APP = "Trying to open excel app"
TRYING_TO_CLOSE_EXCEL_BOOK = "Trying to close excel book"
TRYING_TO_CLOSE_EXCEL_APP = "Trying to close excel app"
TRYING_TO_USE_FORMULA = "Trying to use formula"
TRYING_TO_GET_ENCRYPTION_FILE = (
    "Trying to get encryption file from Google Drive"
)
# Validations
EMAIL_IS_VALID = "Provided email is valid"
EMAIL_IS_NOT_VALID = "Provided email is not valid"
PHONE_IS_VALID = "Provided phone is valid"
SECTIONS_ARE_VALID = "Sections have the same base"
SECTIONS_ARE_NOT_VALID = "Chosen sections have diffrerent base."
DIAGONALS_ARE_VALID = "Diagonals and traverses have correct amount"
DIAGONALS_ARE_NOT_VALID = "Diagonals and traverses have wrong amount"
VALIDATE_SECTION = "Validate if all parts of the Fancata have the same base"
VALIDATE_DIAGONALS = "Check if diagonals are in 1 less than traverses amount"
DATA_VALIDATION = "Check data before preparing it"
VALIDATION_IS_OK = "This check is OK!"
HANDLE_CUSTOM_VALIDATIONS = "Handle custom validations"
# Other
TEST_MODE_ON = "Launching in test mode!"
TEST_MODE_OFF = "Launching in production mode!"
TEST_GUI_MODE = "Test GUI mode is on! Excel will not be opened!"
SHOW_LOADING_WINDOW = "Show loading window"
CLOSE_LOADING_WINDOW = "Close loading window"
SET_ABOUT_TO_QUIT_CASE = (
    "Set about to quit case. Close excel and protect json files"
)
SHOW_MAIN_WINDOW = "Show main window"
SET_EXCEL_SETTINGS = "Set excel settings"
DOWNLOAD_FILE_FROM_DROPBOX = (
    "Use response.get to download file from dropbox"
)
CLOSE_EXCEL_HANDLER_FIRST = "Close excel handler first"
RESTART_EXCEL = "Restart excel app in DropBox class"
SET_NEW_FILEPATH = "Set new filepath before starting excel again"
HIDE_START_WINDOW = "Hide start window"
RERENDER_WINDOW = "Rerender window"
LOAD_CONFIG_GUI = "Load config needed for window creation"
ADD_GREETINGS_TO_CONFIG = "It is a main window. Add greetings to config"
ADD_LOGO_TO_CONFIG = "Add logo to config"
BLOCK_SIZE = "Block window size"
SELECT_TIME_OF_DAY = "Decide what time of day it is"
WIDGET_IS_ALIVE = "The widget is alive"
WIDGET_IS_DEAD = "The widget is dead"
GENERATE_RESPONSE = "Generate response config"
GENERATE_LOGO_CONFIG = "Generate logo config"
DISABLE_FIELDS = "Disable all input and choice fields"
ENABLE_FIELDS = "Enable all input and choice fields"
CHANGE_BUTTON = "Rename button and set another callback to it"
REMOVE_RESULT_FROM_CONFIG = "Remove result from config"
INSERT_NEW_LAYOUT_TO_CONFIG = (
    "Insert new layout into the config on the right place"
)
CHECK_PASSWORD_STRENGTH = "Check password strength"
INSERT_DATA_INTO_EXCEL = "Insert prepared data into the excel worksheet"
COPYING_CELLS = "Copy cells to another ones"
REFRESH_EXCEL = "Refresh table data to recalculate formulas"
LOG_CONVERTATION = "Convert data"
LOG_HANDLE_SPECIAL_OUTPUT = "Handle special output"
LOG_HIDE_RESULT = "Hide result if it is needed"
LOG_PREPARE_EXCEL_HANDLER = "Prepare excel handler"
LOG_INITIATE_EXCEL_HANDLER = "Trying to iniciate excel handler main process"
LOG_ADD_POST_MESSAGE_FOR_ERROR = "Add post message if there is an error"
LOG_CHECK_CONDITION = (
    "Set post message. If there is a condition, check it first"
)
LOAD_ENCRYPTION_DATA = "Set encryption data from Google. Downloading only once"
LOAD_ENCRYPTION_FILE = "Set encryption file from local"
USER_EXISTS = "User is already exists!"
WRONG_CREDENTIALS = "Credentials are wrong!"
EMPTY_FIELDS_ERROR = "One (or more) of the required fields is/are empty!"
REPEAT_IS_DIFFERENT = "Pass and its repeat are different"
PASSWORD_IS_WEAK = (
    "Password is weak! It should contain at least:\n"
    "- 8 characters\n"
    "- 1 Uppercase letter\n"
    "- 1 Lowercase letter\n"
    "- 1 Digit\n"
    "- 1 Special character"
)
USER_NOT_FOUND = "User not found!"
LOG_DELIMITER = "============================================================="
ROUNDING_UP_DATA = "Rounding up data"
NOT_DECIMAL_ERROR = "All data should have Decimal type!"
UNACCEPTABLE_OPERATORS = "The expression contains unacceptable operators!"
PREPARE_DICT = "Prepare dictionary where key is cell address"
RECOVER_PASS_SUBJECT = "Recover password"
CHANGE_GROUP_ERROR = "Couldn't change group!"
FAILED_TO_CREATE_FILE = "Failed to create file!"
CHOSE_FILE = "Chose file"
PRE_MSG_STANDART = "Result"


# ============================ LOG DYNAMIC MESSAGES ===========================

LAST_BACKUP_TIME_IS = "Last backup time is {0}"
TRYING_TO_UNPROTECT_FILES = "Trying to unprotect files in {0}"
TRYING_TO_UNPROTECT_FILE = "Trying to unprotect file '{0}'"
TRYING_TO_DELETE_FILES = "Trying to delete files in {0}"
COPYING_FILES = "Trying to copy files from {0} to {1}"
PROTECTING_FILES = "Protect files in {0}. Just in case!"
PROTECTING_FILE = "Protect file '{0}'. Just in case!"
REWRITE_LAST_BACKUP_TIME = "Rewrite last backup time to {0}"
LAUNCH_APP = "Launch app with username {0}"
USER_SETTINGS_PATH_IS = "User settings path is {0}"
SAVE_PID = "Save PID of the excel app in the settings file: {0}"
PID_AND_PROCESS_FOUND = "PID {0} and the same process found!"
TRYING_TO_KILL_PROCESS = "Trying to kill process with PID {0}"
EXCEL_LINK_IS = "Excel link is {0}"
CREATE_WINDOW = "Create window {0}"
NEW_USER_AND_SETTINGS_PATH_ARE = (
    "New user is {0} and his/her settings path is {1}"
)
BUTTON_PRESSED = "'{0}' button has been pressed!"
ERROR_CAUGHT = "Error caught: {0}"
CALLBACK_NOT_FOUND = "Callback {0} not found for {1}!"
SHOULD_BE_MORE_THAN = "'{0}' should be more than '{1}'"
SHOULD_BE_LESS_THAN = "'{0}' should be less than '{1}'"
IS_GREATER_THAN = "'{0}' is greater than max possible ('{1}')"
IS_LESS_THAN = "'{0}' is less than min possible ('{1}')"
SHOULD_BE_NUMERIC = "'{0}' should be numeric"
SHOULD_BE_NATURAL = "'{0}' should be natural"
SHOULD_BE_PRESENTED = "'{0}' should be presented"
SHOULD_BE_MULTIPLE = "'{0}' should be multiple of {1}"
IS_NOT_NUMERIC = "'{0}' is not numeric"
IS_NOT_NATURAL = "'{0}' is not natural"
IS_NOT_PRESENTED = "'{0}'='{1}' is not presented"
IS_NOT_MULTIPLE = "'{0}' is not multiple of '{1}'"
SHOULD_NOT_BE_EQUAL = "'{0}' should not be equal to '{1}'"
IS_EQUAL = "'{0}' = '{1}'"
INSERT_IN_THE_CELL = "Insert {0} in the {1} cell of the worksheet '{2}'"
INSERT_ADDITIONAL = (
    "Insert additional value {0} in the {1} cell of the worksheet '{2}'"
)
JSON_GET_ALL_DATA = "Trying to get all data from {0}"
JSON_GET_VALUE_BY_KEY = "Trying to get value by key '{0}' from {1}."
JSON_GET_VALUES_BY_KEYS = "Trying to get value by keys '{0}' from {1}."
JSON_REWRITE_FILE = "Rewrite whole file '{0}'"
JSON_WRITE_INTO_FILE = "Write new value into the file '{0}'"
SEND_MAIL_TO = "Trying to send mail to {0}"
TRYING_TO_CREATE_USER = "Trying to create user {0}"
TRYING_TO_LOGIN = "Trying to login user {0}"
TRYING_TO_CHANGE_PASS = "Trying to change pass for {0}"
TRYING_TO_CHANGE_EMAIL = "Trying to change email for {0}"
TRYING_TO_CHANGE_NAME = "Trying to change name for {0}"
TRYING_TO_CHANGE_SURNAME = "Trying to change surname for {0}"
TRYING_TO_CHANGE_PHONE = "Trying to change phone for {0}"
TRYING_TO_CHANGE_SEX = "Trying to change sex for {0}"
PHONE_IS_NOT_VALID = (
    "Phone number is not valid: {0}.\nValid format is (XXX) XXX-XX-XX only!"
)
VAR_IS_MISSING = "Variable {0} is missing in the 'data'"
CANT_CLEAR_LOG = "Can't check or clear log {0}: {1}"
SWITCHING_LOG_FILE = (
    "This should be the last line of the log file, because the user has been "
    "changed on {0}. The other logs should be written in the new log "
    "file: '{0}.log'."
)
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
D_CHANGE_USER_DATA_SUCCESS = (
    "User's {0} has been changed successfully on '{1}'!"
)
NOT_EQUAL_FAILED_MSG = "{0} should not be equal to {1}. You have {2}"
USER_CREATED = "User {0} is created!"
MANDATORY_FIELDS = "The following fields are mandatory: {0}!"
MANDATORY_FIELD = "The field '{0}' is mandatory!"
MAIL_ERROR = "Mail error: {0}"
SAVE_USER_SETTINGS_ERROR = (
    "Couldn't save user settings for {0}: {1}"
)
COULDNT_CREATE_FILE = "Couldn't create file: {0}"
SAVE_USER_SETTINGS_SUCCESS = (
    "User settings for {0} have been saved successfully!"
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
EXCEL_LINK = "excel_link"
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
CREATED_BY = "created_by"
CREATED_ON = "created_on"
PHONE = "phone"
CONFIG = "config"
STARTS_WITH = "starts_with"
ENDS_WITH = "ends_with"
IS_ENCODED = "is_encoded"
NEW_EMAIL = "new_email"
NEW_NAME = "new_name"
NEW_SURNAME = "new_surname"
NEW_PHONE = "new_phone"
NEW_SEX = "new_sex"
SEX = "sex"
LAST_BACKUP = "last_backup"
SYMBOLS = "symbols"
TYPE_INFO = "info"
LAST_PID = "last_pid"
TEXT_CHANGE = "text_change"
AUTO_PHONE_FORMAT = "auto_phone_format"

# ========================== DYNAMIC DICTIONARY KEYS ==========================
SECTION_I = "section_{0}"

# =============================== NUMBER CONSTS ===============================
MIDDLE_DETERMINANT_DIVIDER = 2  # Default: 2
TOP_LEFT_X = 40  # Default: 40
TOP_Y = 50  # Default: 50
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
DEFAULT_PLACE_TO_PASTE = -100  # Default: -100
INDENT = 4  # Default: 4
THREE_HUNDRED = 300  # Default: 300
MIN_PASS_LENGTH = 8  # Default: 8
BACKUP_PERIOD = 24  # Default: 24
ROUNDING_LIMIT = "0.01"  # Default: "0.01"
INFO_WINDOW_WIDTH = 500  # Default: 500
INFO_WINDOW_HEIGHT = 200  # Default: 200

# =============================== NAMES CONSTS ================================
LABEL = "label"  # Default: "label"
BUTTON = "button"  # Default: "button"
CHECKBOX = "checkbox"  # Default: "checkbox"
DROPDOWN = "dropdown"  # Default: "dropdown"
INPUT = "input"  # Default: "input"
MY_PROFILE = "My profile"

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
HANDLE_OPEN_MY_PROFILE_METHOD = "handle_open_my_profile"
HANDLE_LOGOUT_METHOD = "handle_logout"
SAVE_SETTINGS_METHOD = "save_settings"
OPEN_SETTINGS_METHOD = "open_settings"
OPEN_INPUT_WINDOW_METHOD = "open_input_window"
OPEN_REGISTER_METHOD = "open_register"
SECTION_CHECK = "section_check"
BOTTOM_LAYOUT = "bottom_layout"
CHANGE_PASS = "change_pass"
DELETE_USER = "delete_user"
FORGOT_PASS = "forgot_pass"
RECOVER_PASSWORD = "recover_password"
OPEN_LOGIN = "open_login"
OPEN_USERS_SETTINGS = "open_users_settings"
SAVE_USERS_SETTINGS = "save_users_settings"
CHANGE_EMAIL = "change_email"
CHANGE_NAME = "change_name"
CHANGE_SURNAME = "change_surname"
CHANGE_PHONE = "change_phone"
CHANGE_SEX = "change_sex"

# ================================ Translator =================================
# English: Italian
DICTIONARY = {
    "amount": "Quantità",
    "automatic": "Automatico",
    "base": "Base",
    "baseplate": "Piastra di base",
    "basedepth": "Dimensione piastra (P)",
    "baselength": "Dimensione piastra (L)",
    "baseplates": "Piastre di base",
    "baseplates_welded": "pdb saldati",
    "boot": "Stivaletto",
    "depth": "Profondità",
    "development": "Sviluppo",
    "diagonal": "Diagonale",
    "element": "Elemento",
    "fold": "Piega",
    "diagonals": "Diagonali",
    "height": "Altezza",
    "holes": "Fori",
    "hook": "Staffa",
    "length": "Lunghezza",
    "only": "Solo",
    "pb": "PB",
    "pieces": "Tratti",
    "preparation": "Approntamento",
    "price": "Prezzo",
    "profile": "Profilo",
    "section": "Sezione",
    "skates": "Pattini",
    "special": "Speciale",
    "standart": "Tipo standart",
    "strut": "Montante",
    "support": "Appoggio",
    "thickness": "Spessore",
    "top": "Sommità",
    "traverse": "Traverse",
    "traverses": "Traversi",
    "type": "Tipo",
    "typology": "Tipologia",
    "weight": "Peso",
    "welded": "Saldati",
    "width": "Larghezza",
}

# =============================== JSON PATHS ==================================

JSON_EXTENSION = ".json"
LOG_EXTENSION = ".log"
CONFIGS_FOLDER = "configs"
BACKUPS_FOLDER = "backups"
AUTH_FILE = "configs/auth.json"
SETTINGS_FILE = "configs/users_settings_files/settings.json"
LOGIN_WINDOW_CONFIG_FILE = "configs/windows_configs/login_window.json"
REGISTER_WINDOW_CONFIG_FILE = "configs/windows_configs/register_window.json"
MAIN_WINDOW_CONFIG_FILE = "configs/windows_configs/main_window.json"
SETTINGS_WINDOW_CONFIG_FILE = "configs/windows_configs/settings_window.json"
OUTPUT_WINDOW_CONFIG_FILE = "configs/windows_configs/output_window.json"
USER_MAIN_DATA_FILE = "configs/users_configs/user_main_data.json"
TRAVI_WINDOW_CONFIG_FILE = "configs/windows_configs/travi_window.json"
CALC_CONFIG_PATH = "configs/calculator_configs/{0}.json"
MY_PROFILE_CONFIG_FILE = "configs/windows_configs/my_profile_window.json"
ENCRYPTION_FILE = "configs/encryption.json"
SETTINGS_JSON = "settings.json"
MODIFIED_SETTINGS_JSON = "settings_{0}.json"
TEMP_EXCEL_NAME = "temp_excel.xlsx"
MODIFIED_LOG_PATH = "{0}.log"

# =============================== LOGO PATHS ==================================

LOGO_PATH = "files/icons/logo_sacma.png"
ICON_PATH = "files/icons/logo_s.ico"
MAIN_LOGO_PATH = "files/icons/main_logo.png"

# ============================ ITALIAN STR CONSTS =============================
PRICE_IT = "Prezzo"
PREPARATION_IT = "Approntamento"
WEIGHT_IT = "Peso"
NOT_FOUND_IT = "non trovato"
DEVELOPMENT_IT = "Sviluppo"
START_IT = "Invia"
FORWARD_IT = "Avanti"
WAIT_IT = "Attendere..."
LOADING_IT = "Caricamento..."

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
LESS_THAN = "<"
GREATER_THAN = ">"
UNDERSCORE = "_"
FILE_NAME_CONNECTOR = "_"
LISTING_CONNECTOR = ", "

# ============================ REGEX PATTERNS =================================
FLOAT_REGEX = r"\d+(,\d+)?"
VARIABLE_REGEX = r"[a-zA-Z_][a-zA-Z0-9_]*"
NUMBERS_N_OPERATORS_REGEX = r"^[0-9.\s()+\-*/]+$"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SPECIAL_CHARS = "[!@#$%^&*()_+={}[]:;\"'<>?,./\\|`~]"
COMMON_SPECIAL_CHARS = "!@#$%^&*()_+"
EXCEL_FILES_FILTER = "Excel Files (*.xlsx *.xls)"
DATE_TIME_FORMAT = "%H:%M:%S %d/%m/%Y"
PHONE_REGEX = r"^\(\d{3}\) \d{3}-\d{2}-\d{2}$"

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

# ============================ VALIDATION KEYS ================================
VALIDATION_MIN = "min"
VALIDATION_MAX = "max"
VALIDATION_NUMERIC = "numeric"
VALIDATION_NATURAL = "natural"
VALIDATION_MULTIPLE = "multiple"
VALIDATION_EXISTS = "exists"
VALIDATION_NOT_EQUAL = "ne"

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

# ============================== GOOGLE SETTINGS ==============================
ENCRYPTION_FILE_LINK = "ENCRYPTION_FILE_LINK"
GOOGLE_ENCRYPTION_FILE_LINK = (
    "https://drive.google.com/uc?export=download&id={0}"
)
GOOGLE_FILE_ID_REGEX = r"/d/([a-zA-Z0-9_-]+)"


# ============================== DROPBOX SETTINGS =============================
LINK_REPLACE_PART = "dl=0"
LINK_REPLACE_WITH = "dl=1"

# =========================== PHONE NUMBER SETTINGS ===========================

PHONE_NUMBER_LENGTH = 10  # Default: 10
FIRST_DIGITS_BLOCK = 3  # Default: 3
SECOND_DIGITS_BLOCK = 3  # Default: 3
THIRD_DIGITS_BLOCK = 2  # Default: 2
FOURTH_DIGITS_BLOCK = 2  # Default: 2
OPEN_BRACKET_POSITION = 1  # Default: 1
CLOSE_BRACKET_POSITION = 4  # Default: 4
FIRST_DASH_POSITION = 7  # Default: 7
SECOND_DASH_POSITION = 9  # Default: 9

ADD_OPEN_BRACKET = "({0}"
ADD_CLOSE_BRACKET = ") {0}"
ADD_DASH = "-{0}"
