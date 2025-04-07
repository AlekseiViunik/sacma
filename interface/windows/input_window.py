from handlers.excel_handler import ExcelHandler
from .base_window import BaseWindow
from handlers.input_data_handler import InputDataHandler
from helpers.helper import Helper
from logic.calculator import Calculator
from logic.logger import logger as log
from settings import settings as sett


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

    - input_data_handler: InputDataHandler
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
        excel_handler: ExcelHandler = None
    ) -> None:
        super().__init__(file_path)
        self.window_name: str = window_name
        self.input_data_handler = InputDataHandler()
        self.excel_handler = excel_handler

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
            log.info(sett.INVIA_BUTTON_PRESSED)
            all_inputs = self.input_data_handler.collect_all_inputs(
                self.creator.input_fields,
                self.creator.chosen_fields
            )
            calculator = Calculator(
                all_inputs,
                self.window_name,
                self.creator.current_changing_values,
                self.excel_handler
            )
            log.info(sett.START_CALCULATING)
            result, post_message = calculator.calc_data()

            log.info(sett.OPEN_RESPONSE_WIDGET)

            if not (
                only_keys := calculator.calc_config[sett.CELLS_OUTPUT].get(
                    sett.ONLY_KEYS
                )
            ):
                only_keys = [
                    key for key in calculator.calc_config[
                        sett.CELLS_OUTPUT
                    ].keys()
                ]

            self.creator.show_response(
                result,
                post_message,
                only_keys
            )

        except Exception as e:
            Helper.log_exception(e)

    def handle_forward_button(self) -> None:
        self.creator.hide_response()
