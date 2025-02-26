# Main window
MAIN_WIN_WIDTH = 600
MAIN_WIN_HEIGHT = 300
MAIN_WIN_TITLE = "SACMA"

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

# Secondary window
SECOND_WIN_WIDTH = 400
SECOND_WIN_HEIGHT = 300
ON_CLOSING_WINDOW = "WM_DELETE_WINDOW"

# Fiancate window
FIANCATE_WIN_WIDTH = 400
FIANCATE_WIN_HEIGHT = 500

# Travi window
TRAVI_SELECT_FIELDS = {
    "Tipo": ["TG", "SAT", "APERTE", "PORTA SKID"],
    "Altezza": [
        50, 60, 70, 80, 90, 100, 110, 120, 130,
        140, 150, 160, 170, 180, 190, 200
    ],
    "Larghezza": [45, 50],
    "Spessore": [1.2, 1.5, 2.0, 2.5, 3.0, 4.0],
    "Staffa speciale": ["No", "Sì"],
    "Quantita": [">=1001", "<=1000"],
}
TRAVI_INPUT_FIELDS = ["Lunghezza"]

# Fiancate window
FIANCATE_SELECT_FIELDS = {
    "Solo montante": ["No", "Sì"],
    "Sismo resistente": ["No", "Sì"],
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

# Frames
FRAME_BG_COLOR = "#f0f0f0"
FRAME_PADX = 10
FRAME_PADY = 10


# Buttons
BUTTON_HEIGHT = 2
BUTTON_COLOR = "#d9d9d9"
BUTTON_PADX = 10
BUTTON_PADY = 10
BUTTON_STICKY = "nsew"
BUTTON_RELIEF = "raised"
# Invia button
BUTTON_INVIA_WIDTH = 10
BUTTON_INVIA_TITLE = "Invia"
BUTTON_INVIA_SIDE = "bottom"
BUTTON_INVIA_ANCHOR = "se"

# Grid
COL_NUM = 3
GRID_WEIGHT = 1

# Labels
LABEL_BG_COLOR = "#f0f0f0"
LABEL_FONT_FAMILY = "Arial"
LABEL_FONT_SIZE = 14
LABEL_PADY = 5
LABEL_MM_TEXT = "mm"
LABEL_MM_COLUMN = 2
LABEL_NAME_COLUMN = 0
LABEL_STICKY = "w"

# Dropdowns
DROPDOWN_STICKY = "ew"
DROPDOWN_PADX = 5
DROPDOWN_COLUMN = 1

# Entries
ENTRY_STICKY = "ew"
ENTRY_COLUMN = 1
ENTRY_PADX = 5

# Methods
BUTTON_METHOD_PREFIX = "create_"
BUTTON_METHOD_POSTFIX = "_ui"

# Dimensions
HEIGHT = "Altezza"
WIDTH = "Larghezza"
THICKNESS = "Spessore"
LENGTH = "Lunghezza"
dimensions_need_mm = [HEIGHT, WIDTH, THICKNESS, LENGTH]

# Excel data
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

TRAVI_WORKSHEET = "Listino Travi"
TRAVI_TYPE_KEY = "Tipo"
TRAVI_TYPE_TG = "TG"
TRAVI_TYPE_SAT = "SAT"

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
    }
}
