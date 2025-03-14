from PyQt6.QtWidgets import QApplication, QWidget


class Helper:

    @staticmethod
    def move_window_to_center(window: QWidget):
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - window.window_width) // 2
        y = (screen_geometry.height() - window.window_height) // 2
        window.setGeometry(x, y, window.window_width, window.window_height)

    @staticmethod
    def move_window_to_top_left_corner(window: QWidget):
        window.setGeometry(0, 0, window.window_width, window.window_height)

    @staticmethod
    def get_calculation_file(name: str) -> str:
        filename = "_".join(word.lower() for word in name.split())
        return f"configs/calculator_configs/{filename}.json"

    @staticmethod
    def get_nested_data(keys: list, data: dict) -> dict | None:
        """Рекурсивно ищет значение в словаре `data`, используя ключи из `keys,
        независимо от их порядка."""
        if not keys:
            return data

        for key in keys:
            if "choices" in data and key in data["choices"]:
                return Helper.get_nested_data(
                    [k for k in keys if k != key], data["choices"][key]
                )  # Удаляем найденный ключ и продолжаем

        return None
