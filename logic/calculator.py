from logic.handlers.excel_handler import ExcelHandler
from logic.handlers.formulas_handler import FormulasHandler
from logic.handlers.json_handler import JsonHandler
from logic.helpers.helper import Helper
from logic.helpers.validator import Validator
from settings import settings as sett


class Calculator:
    """
    Класс для обработки введённых пользователем данных, выполнения расчётов
    и получения результатов на основе JSON-конфигурации и Excel-файлов.

    Основные функции:
    - Загрузка конфигурации расчётов из JSON в зависимости от выбранного типа
      элемента.
    - Извлечение данных для расчётов из Excel.
    - Применение формул к полученным данным.
    - Генерация итогового результата для отображения.

    Attributes
    ----------
    - data: dict
        Введённые пользователем данные.

    - type: str
        Тип элемента, для которого выполняется расчёт. Используется для
        выбора соответствующего файла конфигурации расчёта.

    - choices: dict
        Выбранные параметры, влияющие на конфигурацию расчёта.

    - excel_handler: ExcelHandler | None
        Default = None\n
        Обработчик Excel-файла (инициализируется при расчётах).

    Methods
    -------
    - calc_data()
        преобразует отправленные юзером данные в данные для вывода на экран.

    Private methods
    ---------------
    - __use_formula(output_dict, formulas, input_dict)
        Применяет формулы (если есть) к каждому из значений результата и
        перезаписывает эти значения.

    - __check_condition(output_dict, condition, input_dict)
        Проверяет условие для вывода сообщения, если оно задано в конфиге.

    - __convert_data()
        Преобразует данные, введённые пользователем, в соответствии с
        конфигурацией расчётов. Например, заменяет значения на соответствующие
        им числа.
    """

    def __init__(
        self,
        data: dict,
        type: str,
        choices: dict,
        excel_handler: ExcelHandler = None
    ) -> None:
        self.data: dict = data
        self.choices: dict = choices
        self.calc_file_path: str = Helper.get_calculation_file(type)
        self.calc_config: dict = {}
        self.config_file_handler = JsonHandler(self.calc_file_path)
        self.excel_handler: ExcelHandler | None = excel_handler

    def calc_data(self) -> tuple:
        """
        Метод, преобразующий данные, введенные пользователем в данные, для
        вывода на экран в качестве результата. Использует json
        calculator_configs и обработчик эксель.

        Returns
        -------
        - (excel_result, post_message): tuple
            Результат для вывода и сообщение после вывода результата.
        """

        # Получаем из общего конфига конфиг для выбранного нам типа элемента.
        self.calc_config = self.config_file_handler.get_all_data()
        keys = list(self.choices.values())
        if keys:
            self.calc_config = Helper.get_nested_data(
                keys,
                self.calc_config
            )
        else:
            self.calc_config = self.calc_config[sett.CHOICES]
        if self.calc_config.get(sett.CONVERTATION):
            self.__convert_data()

        # Специальный вывод - это обычно когда в экселе считать ничего не надо,
        # а значения для вывода берутся из ячеек, адрес которых определяется
        # введенными параметрами
        if self.calc_config.get(sett.SPECIAL_OUTPUT):
            self.calc_config.pop(sett.SPECIAL_OUTPUT)
            keys = list(self.data.values())

            # Получаем адреса ячеек, которые необходимо извлечь из экселя
            self.calc_config[sett.CELLS_OUTPUT] = Helper.get_nested_data(
                keys,
                self.calc_config[sett.CELLS_OUTPUT]
            )

        # Если есть сообщение, которое надо вставить в окне результатов после
        # вывода результата, извлекаем его из конфига.
        post_message = self.calc_config[sett.CELLS_OUTPUT].pop(
            sett.POST_MESSAGE,
            None
        )

        # Если есть результат, который не надо отображать, даже если он
        # получен, активируем флаг is_hide.
        is_hide = self.calc_config[sett.CELLS_OUTPUT].pop(
            sett.IS_HIDE,
            None
        )

        # Стандартная валидация данных на сравнение друг с другом разных
        # показателей. Например, что количество одних элементов должно быть
        # равно определенному количеству других элементов.
        validation_result = None
        if (self.calc_config.get(sett.CUSTOM_VALIDATIONS)):
            validation_result = Validator().custom_validation(
                self.calc_config,
                self.data
            )

        if not validation_result or validation_result[sett.IS_CORRECT]:
            # Ключи введенных данных на английском языке, а поля для ввода
            # обозначены на итальянском, поэтому переводим все ключи на
            # итальянский. Почему при этом мы не переводим на итальянский
            # данные по извлекаемым ячейкам - я не помню.

            self.excel_handler.data = self.excel_handler.preparator.data = (
                self.data
            )
            self.excel_handler.rules = self.excel_handler.preparator.rules = (
                self.calc_config[sett.RULES]
            )
            self.excel_handler.worksheet = self.calc_config[sett.WORKSHEET]
            self.excel_handler.cells_input = (
                self.calc_config[sett.CELLS_INPUT]
            )

            self.excel_handler.cells_output = (
                self.calc_config[sett.CELLS_OUTPUT]
            )
            self.excel_handler.copy_cells = self.calc_config.get(
                sett.COPY_CELLS,
                None
            )
            self.excel_handler.additional_input = self.calc_config.get(
                sett.ADDITIONAL_INPUT,
                None
            )
            self.excel_handler.roundings = self.calc_config.get(
                sett.ROUNDINGS,
                None
            )
            self.excel_handler.sheet = self.excel_handler.wb.Sheets(
                self.excel_handler.worksheet
            )
            # Запускаем обработчик эксель файла
            try:
                excel_result = self.excel_handler.initiate_process()
            except Exception as e:
                print(e)
        else:
            excel_result = {
                sett.PRICE: None,
                sett.WEIGHT: None,
                sett.ERROR: validation_result[sett.ERROR_MESSAGE]
            }

        # Если в обработчике данные не прошли валидацию, то в сообщении после
        # вывода результатов выводим сообщение об ошибке.
        if excel_result.get(sett.ERROR):
            post_message = excel_result.pop(sett.ERROR)
        else:
            # Если полученные результаты требуют дальнейших расчетов по
            # формуле, применяем ее
            if self.calc_config.get(sett.FORMULAS):
                try:
                    self.__use_formula(
                        excel_result,
                        self.calc_config[sett.FORMULAS],
                        self.data
                    )
                except Exception as e:
                    print(e)

            # NEW! Если post_message - не строка, а словарь (содержит помимо)
            # сообщения еще и условие для его отображения. То проверяем это
            # условие перед тем, как установить это сообщение.
            if post_message and not isinstance(post_message, str):
                if self.__check_condition(
                    excel_result,
                    post_message.get(sett.CONDITION, sett.EMPTY_STRING),
                    self.data
                ):
                    post_message = post_message[sett.MESSAGE]
                else:
                    post_message = None

        # Устанавливаем реультат как None, если его не нужно
        # отображать (is_hide = 1)
        excel_result = {
            k: None if is_hide else v for k, v in excel_result.items()
        }

        # Возвращаем итоговый результат и сообщение, которое выводим после
        # вывода результата.
        return excel_result, post_message

    # ============================ Private Methods ============================
    # -------------------------------------------------------------------------
    def __use_formula(
        self,
        output_dict: dict,
        formulas: dict,
        imput_dict: dict = {}
    ) -> None:
        """
        Переопределяет результат, применяя к нему кастомную формулу из конфига.
        Результат перезаписывается, поэтому ничего возвращать не надо.

        Parameters
        ----------
        - output_dict: dict
            Изначально полученные из экселяданные, к которым будет применена
            формула, и которые будут впоследствие перезаписаны.

        - formulas: dict
            Сами формулы, записанные в виде строки для каждого (или только
            некоторых) значения из output_dict.

        - imput_dict: dict
            Default = {}\n
            Иногда для формул могут использоваться также и введенные юзером
            данные. Храним их здесь
        """

        # Объединяем словари введенных и полученных данных, чтобы обработчику
        # было проще работать с одним словарем.
        merged_dicts = Helper.merge_numeric_dicts(output_dict, imput_dict)

        # Для каждой формулы (чье имя, кстати, должно совпадать с ключом
        # словаря output_dict) проводим вычисления через обраотчик. Если
        # ее имя не совпадает со словарем, просто игнорируем формулу.
        for formula_name, formula in formulas.items():
            if output_dict[formula_name]:
                result = FormulasHandler().apply_formula(
                    merged_dicts,
                    formula,
                    formula_name
                )
            output_dict[formula_name] = result

    def __check_condition(
        self,
        output_dict: dict,
        condition: str,
        imput_dict: dict = {}
    ) -> bool:
        """
        Проверяет условие для вывода сообщения, если оно задано в конфиге.
        В условиях могут учавствовать как входные, так и выходные данные.

        Parameters
        ----------
        - output_dict: dict
            Данные для вывода на экран.

        - condition: str
            Условие, которое необходимо проверить. Например: "x1 > x2".

        - imput_dict: dict
            Default = {}\n
            Иногда для формул могут использоваться также и введенные юзером
            данные. Храним их здесь.

        Returns
        -------
        - _: bool
            Результат проверки условия.
        """

        merged_dicts = Helper.merge_numeric_dicts(output_dict, imput_dict)
        return FormulasHandler().check_condition(merged_dicts, condition)

    def __convert_data(self) -> None:
        """
        Если в конфиге для расчетов есть такой параметр, как convertation, то
        Необходимо конфертировать собранные данные из одного вида в другой,
        согласно разделу convertation в конфиге.
        Например если конфиг выглядит так:
        "section": {"x1": 1, "x2": 100},
        И если у нас в собранных данных "section": "x2",
        То в собранных данных мы должны заменить это значение на 100.
        """

        for param, value in self.data.items():
            if param in self.calc_config[sett.CONVERTATION].keys():
                self.data[
                    param
                ] = self.calc_config[sett.CONVERTATION][param][value]
