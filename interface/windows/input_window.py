from handlers.input_data_handler import InputDataHandler
from interface.windows.output_window import OutputWindow
from logic.calculator import Calculator
from logic.logger import logger as log
from .base_window import BaseWindow
from settings import settings as set


class InputWindow(BaseWindow):
    """
    Окно, появляющееся при нажатии одной из основных кнопок стартового окна.
    Для каждой кнопки имеет свой набор виджетов и контейнеров в зависимости
    от конфига.

    Attributes
    ----------
    - window_name: str
        Имя окна, которое передается в Калькулятор для получения имени файла
        конфига для расчетов.

    - output_window: OutputWindow
        Класс окна вывода рещультата.

    - input_data_handler = InputDataHandler
        Обработчик данных, введенных/выбранных пользователем.

    Methods
    -------
    - handle_start_button()
        Обработчик нажатия кнопки Invia.
    """

    def __init__(
        self,
        window_name: str,
        file_path: str,
    ) -> None:
        super().__init__(file_path)
        self.window_name: str = window_name
        self.output_window: OutputWindow = None
        self.input_data_handler = InputDataHandler()

        self.init_ui()

    def handle_start_button(self) -> None:
        """
        Обработчик стартовой кнопки Invia.
        При нажатии кнопки выполняет следующее:
        - Получает данные, введенные/выбранные пользователем и собирает их в
        один словарь.
        - Запускает класс-Калькулятор для дальнейшей обработки данных
        пользователя и получения итогового результата.
        - Открывает окно с выводом результата.
        """
        try:
            log.info(set.INVIA_BUTTON_PRESSED)
            all_inputs = self.input_data_handler.collect_all_inputs(
                self.creator.input_fields,
                self.creator.chosen_fields
            )
            calculator = Calculator(
                all_inputs,
                self.window_name,
                self.creator.current_changing_values
            )
            self.output_window = OutputWindow()
            log.info(set.START_CALCULATING)
            result, post_message = calculator.calc_data()

            log.info(set.OPEN_RESPONSE_WIDGET)

            if not (
                only_keys := calculator.calc_config[set.CELLS_OUTPUT].get(
                    set.ONLY_KEYS
                )
            ):
                only_keys = [
                    key for key in calculator.calc_config[
                        set.CELLS_OUTPUT
                    ].keys()
                ]

            self.output_window.open_result_window(
                result,
                set.PRE_MSG_STANDART,
                post_message,
                only_keys
            )
        except Exception as e:
            log.error(f"Error caught: {e}")
