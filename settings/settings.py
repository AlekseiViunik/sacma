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
    "Gragliato",
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
TRAVI_OPTIONS = {
    "Tipo": ["TG", "C"],
    "Altezza": [
        50, 60, 70, 80, 90, 100, 110, 120, 130,
        140, 150, 160, 170, 180, 190, 200
    ],
    "Larghezza": ["45", "50"],
    "Spessore": ["1.2", "1.5", "2.0", "2.5", "3.0"]
}

# Frames
FRAME_BG_COLOR = "#f0f0f0"
FRAME_PADX = 10
FRAME_PADY = 10
# Main frame
MAIN_WIN_FRAME_COL_NUM = 3

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

# Methods
BUTTON_METHOD_PREFIX = "create_"
BUTTON_METHOD_POSTFIX = "_ui"

# Dimensions
HEIGHT = "Altezza"
WIDTH = "Larghezza"
THICKNESS = "Spessore"
LENGTH = "Lunghezza"

