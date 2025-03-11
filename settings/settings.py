"""
===============================================================================
================================              =================================
================================ GUI SETTINGS =================================
================================              =================================
===============================================================================
"""
# ================================ WINDOWS ====================================
# ============================== Main window ==================================

# Width. Default: 600
MAIN_WIN_WIDTH = 600

# Height. Default: 300
MAIN_WIN_HEIGHT = 300

# Window title. Default: "SACMA"
MAIN_WIN_TITLE = "SACMA"

# Buttons on the main window.
# Default:
# [
#     "Fiancate",
#     "Travi",
#     "Tasselli",
#     "Satellitare",
#     "Pianetti",
#     "Grigliato",
#     "Travi di battuta",
#     "Angolari per automatici",
#     "Gravita leggera",
#     "Option di sicurezza"
# ]
MAIN_WIN_BUTTONS = [
    "Fiancate",
    "Travi",
    "Tasselli",
    "Satellitare",
    "Pianetti",
    "Grigliato",
    "Travi di battuta",
    "Angolari per automatici",
    "Gravita leggera",
    "Option di sicurezza"
]

# ============================= Secondary windows =============================

# Name of the event which has to be handled. Default: "WM_DELETE_WINDOW"
ON_CLOSING_WINDOW = "WM_DELETE_WINDOW"


# =============================== COMPONENTS ==================================
# ================================= Frames ====================================

# Background color. Default: "#f0f0f0"
FRAME_BG_COLOR = "#f0f0f0"

# Padding (axis X). Default: 10
FRAME_PADX = 10

# Padding (axis Y). Default: 10
FRAME_PADY = 10


# ================================= Buttons ===================================

# Height (in N strings). Default: 2
BUTTON_HEIGHT = 2

# Button color. Default: "#d9d9d9"
BUTTON_COLOR = "#d9d9d9"

# Padding (axis X). Default: 10
BUTTON_PADX = 10

# Padding (axis Y). Default: 10
BUTTON_PADY = 10

# Button extension in the grid. Default: "nsew"
# Possible options:
# s, n, w, e - put button close to the n/s/w/e edge of the grid
# ns, we - extend button by vertical/horizontal
# nsew - extend button by vertical and horizontal
BUTTON_STICKY = "nsew"

# Button frame. Default: "raised"
# Possible options: flat, raised, sunken, groove, ridge
BUTTON_RELIEF = "raised"

# =============================== Invia button ================================

# Width. Default: 10
BUTTON_WIDTH = 10

# Button title. Default: "Invia"
BUTTON_INVIA_TITLE = "Invia"

# Where to put widget. Default: "bottom"
# Possible options: top, bottom, left, right
BUTTON_INVIA_SIDE = "bottom"

# Anchor point inside of the SIDE param. Default: "se"
# Possible options: s, n, w, e, ne, se, nw, ne, center
BUTTON_INVIA_ANCHOR = "se"

# =================================== Grid ====================================

# Number of grid columns. Default: 3
COL_NUM = 3

# Controls grid column extension. Default: 1
# If all columns have weight, their width will be calculated by formula:
# GRID_WEIGHT/SUMMARY_GRID_WEIGHTS
GRID_WEIGHT = 1

# ================================== Labels ===================================

# Background color. Default: "#f0f0f0"
LABEL_BG_COLOR = "#f0f0f0"

# Font family. Default "Arial"
LABEL_FONT_FAMILY = "Arial"

# Font size. Default: 14
LABEL_FONT_SIZE = 14

# Padding (axis X). Default: 5
LABEL_PADY = 5

# Text for dimensioning units label. Default: "mm"
LABEL_MM_TEXT = "mm"

# Number of the column where to put dimensioning units label
# (starts from 0, out of COL_NUM total number).
# Defaul: 2
LABEL_MM_COLUMN = 2

# Number of the column where to put entry name label
# (starts from 0, out of COL_NUM total number).
# Defaul: 0
LABEL_NAME_COLUMN = 0

# Label extension in the grid. Default: "w"
# Possible options:
# s, n, w, e - put widget close to the n/s/w/e edge of the grid
# ns, we - extend widget by vertical/horizontal
# nsew - extend widget by vertical and horizontal
LABEL_STICKY = "w"

# ================================= Dropdowns =================================

# Dropdown extension in the grid. Default: "ew"
# Possible options:
# s, n, w, e - put widget close to the n/s/w/e edge of the grid
# ns, we - extend widget by vertical/horizontal
# nsew - extend widget by vertical and horizontal
DROPDOWN_STICKY = "ew"

# Padding (axis X). Default: 5
DROPDOWN_PADX = 5

# Number of the column where to put dropdown
# (starts from 0, out of COL_NUM total number).
# Defaul: 1
DROPDOWN_COLUMN = 1

# ================================= Entries =================================

# Entry extension in the grid. Default: "ew"
# Possible options:
# s, n, w, e - put widget close to the n/s/w/e edge of the grid
# ns, we - extend widget by vertical/horizontal
# nsew - extend widget by vertical and horizontal
ENTRY_STICKY = "ew"

# Number of the column where to put entry
# (starts from 0, out of COL_NUM total number).
# Defaul: 1
ENTRY_COLUMN = 1

# Padding (axis X). Default: 5
ENTRY_PADX = 5

"""
===============================================================================
====================================       ====================================
==================================== LOGIC ====================================
====================================       ====================================
===============================================================================
"""

# ================================ Travi data =================================

# Name of the worksheet, that contains travi calculations
# Default: "Listino Travi"
TRAVI_WORKSHEET = "Listino Travi"

# Key responsible for the travi type. Default: "Tipo"
TRAVI_TYPE_KEY = "Tipo"

# Name of TG travi type. Default: "TG"
TRAVI_TYPE_TG = "TG"

# Name of APERTE travi type. Default: "APERTE"
TRAVI_TYPE_APERTE = "APERTE"

# Name of SAT travi type. Default: "SAT"
TRAVI_TYPE_SAT = "SAT"

# Name of PORTA SKID travi type. Default: "PORTA SKID"
TRAVI_TYPE_PORTA_SKID = "PORTA SKID"

# =================================== NAMES ===================================

# Default: "Altezza"
HEIGHT = "Altezza"

# Default: "Larghezza"
WIDTH = "Larghezza"

# Default: "Spessore"
THICKNESS = "Spessore"

# Default: "Lunghezza"
LENGTH = "Lunghezza"

DEPTH = "Profondità"

BASE = "Base"

# Dimensions that need to clarify dimensioning units
# Default: [HEIGHT, WIDTH, THICKNESS, LENGTH]
dimensions_need_mm = [HEIGHT, WIDTH, THICKNESS, LENGTH, DEPTH, BASE]


TRAVI = "travi"  # Default: "travi"
FIANCATE = "fiancate"  # Default: "fiancate"
PRICE = "Prezzo"  # Default: "Prezzo"
WEIGHT = "Peso"  # Default: "Peso"
SELECT = "select"  # Default: "select"
INPUT = "input"  # Default: "input"
SISMO = "sismo"  # Default: "sismo"

# Default: "Prezzo non trovato"
PRICE_NOT_FOUND = "Prezzo non trovato"

# Default: "Peso non trovato"
WEIGHT_NOT_FOUND = "Peso non trovato"

# ================================== LOGGING ==================================

# Max number of the log file lines. Default: 50000
MAX_LOG_LINES = 50000

# Log file name. Default: "app.log"
LOG_FILE_NAME = "app.log"

# Log coding type. Default: "utf-8"
LOG_CODING = "utf-8"

# ================================ Translator =================================
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
    "price": "Prezzo",
    "weight": "Peso",
    "skates": "Pattini",
    "n_skates": "N pattini",
    "n_diagonals": "N diagonali",
    "traits": "Tratti",
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
    "element": "Elemento"
}

# ===================================Login=====================================
AUTH_FILE = "auth.json"
LOGIN_START_ROW = 1
LOGIN_ENTRIES = {
    "Login": {
        "is_hide": False,
        "default_value": True
    },
    "Password": {
        "is_hide": True,
        "default_value": False
    }
}
CREATE_USER_TITLE = "Create user"
CREATE_USER_ENTRIES = ["Username", "Password", "Repeat password"]
PRODUCTION_MODE_ON = False


"""
===============================================================================
================================                ===============================
================================  ONLY CUSTOM   ===============================
================================ IMPLEMENTATION ===============================
================================                ===============================
===============================================================================
"""
CUSTOM_IMPLEMENTATION = True
