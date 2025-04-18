from .base_window import BaseWindow
from logic.calculator import Calculator
from logic.handlers.excel_handler import ExcelHandler
from logic.handlers.input_data_handler import InputDataHandler
from logic.logger import LogManager as lm
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

    - file_path: str
        Путь к файлу конфигурации, который будет использоваться для построения
        окна. Передается в родительский класс BaseWindow.

    - excel_handler: ExcelHandler
        Default = None\n
        Обработчик excel-файла, который передается в Калькулятор для дальнейшей
        обработки данных.

    Methods
    -------
    - handle_start_button()
        Обработчик нажатия кнопки Invia.

    - handle_forward_button()
        Обработчик нажатия кнопки Avanti.
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
        - Добвляет результат на окно ввода данных.
        """

        try:
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
            result, post_message = calculator.calc_data()

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
            lm.log_exception(e)

    def handle_forward_button(self) -> None:
        """
        Обработчик нажатия кнопки Avanti. Снимает блокировку изменения
        виджетов, удаляет ответ.
        """

        self.creator.hide_response()
