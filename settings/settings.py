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

# Width. Default: 400
SECOND_WIN_WIDTH = 400

# Height. Default: 400
SECOND_WIN_HEIGHT = 400

# Name of the event which has to be handled. Default: "WM_DELETE_WINDOW"
ON_CLOSING_WINDOW = "WM_DELETE_WINDOW"

# ============================= Fiancate windows ==============================

# Width. Default: 400
FIANCATE_WIN_WIDTH = 400

# Height. Default: 500
FIANCATE_WIN_HEIGHT = 500

# ============================== Travi windows ================================

# Width. Default: 400
TRAVI_WIN_WIDTH = 400

# Height. Default: 400
TRAVI_WIN_HEIGHT = 400


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

# ================================= Choices =================================

TRAVI_CHOICE = {
    'TG': {
        'select': {
            "Altezza": [
                70, 80, 90, 100, 110, 120, 130,
                140, 150, 160, 170
            ],
            "Larghezza": [45, 50],
            "Spessore": [1.2, 1.5],
            "Staffa speciale": ["No", "Sì"],
            "Quantita": [">=1001", "<=1000"],
        },
        'input': ['Lunghezza']
    },
    'SAT': {
        'select': {
            "Altezza": [
                70, 80, 90, 100, 110, 120, 130,
                140, 150, 160, 170
            ],
            "Spessore": [1.2, 1.5, 2.0, 2.5, 3.0, 4.0],
            "Appoggio": ["No", "Sì"],
            "Staffa speciale": ["No", "Sì"],
            "Quantita": [">=1001", "<=1000"],
        },
        'input': ['Lunghezza']
    },
    'APERTE': {
        'select': {
            "Altezza": [
                70, 80, 90, 100, 110, 120, 130,
                140, 150, 160, 170, 180, 190, 200
            ],
            "Larghezza": [20, 30, 35, 40, 45, 50],
            "Spessore": [1.2, 1.5, 2.0, 2.5, 3.0, 4.0],
            "Staffa speciale": ["No", "Sì"],
            "Quantita": [">=1001", "<=1000"],

        },
        'input': ['Lunghezza']
    },
    'PORTA SKID': {
        'select': {
            "Altezza": [
                20, 25, 30, 35, 40, 45,
                50, 60, 70, 80, 90, 100, 110, 120, 130,
                140, 150, 160, 170, 180, 190, 200
            ],
            "Larghezza": [30, 35, 40, 45, 50],
            "Spessore": [1.2, 1.5, 2.0, 2.5, 3.0, 4.0],
        },
        'input': ['Lunghezza']
    },
}


"""
===============================================================================
====================================       ====================================
==================================== LOGIC ====================================
====================================       ====================================
===============================================================================
"""
# Data that needs to put widgets in the specified windows
# ================================== Methods ==================================
# These prefix and postfix are needed to generate method name

# Default: "create_"
BUTTON_METHOD_PREFIX = "create_"

# Default: "_ui"
BUTTON_METHOD_POSTFIX = "_ui"

# =============================== Fiancate data ===============================

FIANCATE_ALWAYS_ON = {
    "Sismo resistente": ["No", "Sì"]
}

# Data for dropdown select options
# Default:
# {
#     "Solo montante": ["No", "Sì"],
#     "Sismo resistente": ["No", "Sì"],
#     "Sezione": [
#         "80/20",
#         "80/25",
#         "80/30",
#         "100/20",
#         "100/25",
#         "100/30",
#         "120/20",
#         "120/25",
#         "120/30",
#         "120x110/20",
#         "120x110/25",
#         "120x110/30",
#         "120x110/40"
#     ]
# }
FIANCATE_SELECT_FIELDS = {
    "Solo montante": ["No", "Sì"],
    "Sezione": [
        "80/20",
        "80/25",
        "80/30",
        "100/20",
        "100/25",
        "100/30",
        "120/20",
        "120/25",
        "120/30",
        "120x110/20",
        "120x110/25",
        "120x110/30",
        "120x110/40"
    ]
}

# Names of entries (put in the labels prior to entries)
# Default:
# [
#     "Altezza",
#     "N diagonali 10/10",
#     "N diagonali 15/10",
#     "N diagonali 20/10",
#     "N diagonali 25/10",
#     "N diagonali 30/10",
#     "N traversi 10/10",
#     "N traversi 15/10"
# ]

FIANCATE_INPUT_FIELDS = [
    "Altezza",
    "N diagonali 10/10",
    "N diagonali 15/10",
    "N diagonali 20/10",
    "N diagonali 25/10",
    "N diagonali 30/10",
    "N traversi 10/10",
    "N traversi 15/10"
]

# ================================ Travi data =================================

TRAVI_ALWAYS_ON = {
    "Tipo": ["TG", "SAT", "APERTE", "PORTA SKID"],
}


# Data for dropdown select options.
# Default:
# {
#     "Tipo": ["TG", "SAT", "APERTE", "PORTA SKID"],
#     "Altezza": [
#         20, 25, 30, 35, 40, 45,
#         50, 60, 70, 80, 90, 100, 110, 120, 130,
#         140, 150, 160, 170, 180, 190, 200
#     ],
#     "Larghezza": [30, 35, 40, 45, 50],
#     "Spessore": [1.2, 1.5, 2.0, 2.5, 3.0, 4.0],
#     "Staffa speciale": ["No", "Sì"],
#     "Quantita": [">=1001", "<=1000"],
#     "Appoggio": ["No", "Sì"]
# }
TRAVI_SELECT_FIELDS = {
    "Altezza": [
        20, 25, 30, 35, 40, 45,
        50, 60, 70, 80, 90, 100, 110, 120, 130,
        140, 150, 160, 170, 180, 190, 200
    ],
    "Larghezza": [30, 35, 40, 45, 50],
    "Spessore": [1.2, 1.5, 2.0, 2.5, 3.0, 4.0],
    "Staffa speciale": ["No", "Sì"],
    "Quantita": [">=1001", "<=1000"],
    "Appoggio": ["No", "Sì"]
}

# Names of entries (put in the labels prior to entries). Default: ["Lunghezza"]
TRAVI_INPUT_FIELDS = ["Lunghezza"]

# Cells in Excel addapted to the data of the travi TG.
# Default:
# {
#     "Altezza": "B4",
#     "Larghezza": "B6",
#     "Spessore": "B8",
#     "Lunghezza": "B12",
#     "Staffa speciale": "B14",
#     "Quantita": "B16",
#     "Prezzo": "E4",
#     "Peso": "E6"
# }
TRAVI_CELLS_TG = {
    "Altezza": "B4",
    "Larghezza": "B6",
    "Spessore": "B8",
    "Lunghezza": "B12",
    "Staffa speciale": "B14",
    "Quantita": "B16",
    "Prezzo": "E4",
    "Peso": "E6"
}

# Cells in Excel addapted to the data of the travi APERTE
# Default:
# {
#     "Altezza": "B37",
#     "Larghezza": "B39",
#     "Spessore": "B41",
#     "Lunghezza": "B45",
#     "Staffa speciale": "B47",
#     "Quantita": "B49",
#     "Prezzo": "E37",
#     "Peso": "E39"
# }
TRAVI_CELLS_APERTE = {
    "Altezza": "B37",
    "Larghezza": "B39",
    "Spessore": "B41",
    "Lunghezza": "B45",
    "Staffa speciale": "B47",
    "Quantita": "B49",
    "Prezzo": "E37",
    "Peso": "E39"
}

# Cells in Excel addapted to the data of the travi SAT
# Default:
# {
#     "Altezza": "B21",
#     "Spessore": "B23",
#     "Appoggio": "B27",
#     "Lunghezza": "B29",
#     "Staffa speciale": "B31",
#     "Quantita": "B33",
#     "Prezzo": "E21",
#     "Peso": "E23"
# }
TRAVI_CELLS_SAT = {
    "Altezza": "B21",
    "Spessore": "B23",
    "Appoggio": "B27",
    "Lunghezza": "B29",
    "Staffa speciale": "B31",
    "Quantita": "B33",
    "Prezzo": "E21",
    "Peso": "E23"
}

# Cells in Excel addapted to the data of the travi PORTA SKID
# Default:
# {
#     "Altezza": "B53",
#     "Larghezza": "B55",
#     "Spessore": "B57",
#     "Lunghezza": "B61",
#     "Prezzo": "E53",
#     "Peso": "E55"
# }
TRAVI_CELLS_PORTA_SKID = {
    "Altezza": "B53",
    "Larghezza": "B55",
    "Spessore": "B57",
    "Lunghezza": "B61",
    "Prezzo": "E53",
    "Peso": "E55"
}

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


# Rules needed to check passed data.
# Default:
# {
#     "TG": {
#         "altezza": {
#             "min": 70,
#             "max": 170
#         },
#         "lunghezza": {
#             "numeric": True,
#             "min": 1200,
#             "max": 3600,
#         }
#     },
#     "APERTE": {
#         "altezza": {
#             "min": 70,
#             "max": 170
#         },
#         "lunghezza": {
#             "numeric": True,
#             "min": 1200,
#             "max": 3600,
#         }
#     },
#     "SAT": {},
#     "PORTA SKID": {}
# }
TRAVI_RULES = {
    "TG": {
        "altezza": {
            "min": 70,
            "max": 170
        },
        "lunghezza": {
            "numeric": True,
            "min": 1200,
            "max": 3600,
        }
    },
    "APERTE": {
        "altezza": {
            "min": 70,
            "max": 170
        },
        "lunghezza": {
            "numeric": True,
            "min": 1200,
            "max": 3600,
        }
    },
    "SAT": {},
    "PORTA SKID": {}
}

# =================================== NAMES ===================================

# Default: "Altezza"
HEIGHT = "Altezza"

# Default: "Larghezza"
WIDTH = "Larghezza"

# Default: "Spessore"
THICKNESS = "Spessore"

# Default: "Lunghezza"
LENGTH = "Lunghezza"

# Dimensions that need to clarify dimensioning units
# Default: [HEIGHT, WIDTH, THICKNESS, LENGTH]
dimensions_need_mm = [HEIGHT, WIDTH, THICKNESS, LENGTH]


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
