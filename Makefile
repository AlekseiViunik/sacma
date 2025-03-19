PYTHON = python
PYINSTALLER = $(PYTHON) -m PyInstaller
ICON = files/icons/cartman32.ico
MAIN_FILE = main.py
SPEC_FILE = main.spec
BUILD_DIR = build
DIST_DIR = dist

# Удаление папок и spec-файла
delete-exe:
	rm -rf $(BUILD_DIR) $(DIST_DIR) $(SPEC_FILE)

# Удаление папок (НО НЕ `main.spec`)
clean-build:
	rm -rf $(BUILD_DIR) $(DIST_DIR)

# Создание исполняемого файла
exe: delete-exe
	$(PYINSTALLER) --noconsole --onefile --icon=$(ICON) $(MAIN_FILE)

# Пересоздание исполняемого файла без удаления `main.spec`
remake-exe: clean-build
	$(PYINSTALLER) --noconsole --onefile --icon=$(ICON) $(MAIN_FILE)