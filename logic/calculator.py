from handlers.excel_handler import ExcelHandler
from handlers.formulas_handler import FormulasHandler
from handlers.json_handler import JsonHandler
from helpers.helper import Helper
from logic.translator import Translator


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

    - choices: dict
        Выбранные параметры, влияющие на конфигурацию расчёта.

    - calc_file_path: str
        Путь к JSON-файлу с конфигурацией расчётов.

    - calc_config: dict
        Загруженный конфиг расчётов для текущего типа элемента.

    - config_file_handler: JsonHandler
        Обработчик JSON-файла конфигурации.

    - excel_handler: ExcelHandler | None
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
    """

    def __init__(
        self,
        data: dict,
        type: str,
        choices: dict
    ) -> None:
        self.data: dict = data
        self.choices: dict = choices
        self.calc_file_path: str = Helper.get_calculation_file(type)
        self.calc_config: dict = {}
        self.config_file_handler = JsonHandler(self.calc_file_path)
        self.excel_handler: ExcelHandler | None = None

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
            self.calc_config = self.calc_config['choices']
        if self.calc_config.get('conversion'):
            self.__convert_data()

        # Специальный вывод - это обычно когда в экселе считать ничего не надо,
        # а значения для вывода берутся из ячеек, адрес которых определяется
        # введенными параметрами
        if self.calc_config.get('special_output'):
            self.calc_config.pop('special_output')
            keys = list(self.data.values())

            # Получаем адреса ячеек, которые необходимо извлечь из экселя
            self.calc_config['cells_output'] = Helper.get_nested_data(
                keys,
                self.calc_config['cells_output']
            )

        # Если есть сообщение, которое надо вставить в окне результатов после
        # вывода результата, извлекаем его из конфига.
        post_message = self.calc_config['cells_output'].pop(
            'post_message',
            None
        )

        # Если есть результат, который не надо отображать, даже если он
        # получен, активируем флаг is_hide.
        is_hide = self.calc_config['cells_output'].pop(
            'is_hide',
            None
        )

        # Ключи введенных данных на английском языке, а поля для ввода
        # обозначены на итальянском, поэтому переводим все ключи на
        # итальянский. Почему при этом мы не переводим на итальянский
        # данные по извлекаемым ячейкам - я не помню.
        self.excel_handler = ExcelHandler(
            Translator.translate_dict(self.data),
            Translator.translate_dict(self.calc_config['rules']),
            self.calc_config['worksheet'],
            Translator.translate_dict(self.calc_config['cells_input']),
            self.calc_config['cells_output'],

            # copy_cells указывает значения каких ячеек (ключи) и
            # куда (значения) надо будет копировать после внесения собранных
            # данных в эксель. Изначально введено для fiancate.
            self.calc_config.get('copy_cells', None),

            # additional_input - словарь, кторый указываетв какие ячейки
            # (ключи) какие значения (значения) надо внести, независимо от
            # введенных юзером данных. Изначально введено для указания толщины
            # диагоналей и траверс для fiancate.
            self.calc_config.get('additional_input', None)
        )

        # Запускаем обработчик эксель файла
        excel_result = self.excel_handler.initiate_process()

        # Если в обработчике данные не прошли валидацию, то в сообщении после
        # вывода результатов выводим сообщение об ошибке.
        if excel_result.get('error'):
            post_message = excel_result.pop('error')
        else:
            # Если полученные результаты требуют дальнейших расчетов по
            # формуле, применяем ее
            if self.calc_config.get('formulas'):
                self.__use_formula(
                    excel_result,
                    self.calc_config['formulas'],
                    self.data
                )

        # Устанавливаем реультат как None, если его не нужно
        # отображать (is_hide = 1)
        excel_result = {
            k: None if is_hide else v for k, v in excel_result.items()
        }

        # Возвращаем итоговый результат и сообщение, которое выводим после
        # вывода результата.
        return excel_result, post_message

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

    def __convert_data(self) -> None:
        """
        Если в конфиге для расчетов есть такой параметр, как conversion, то
        Необходимо конфертировать собранные данные из одного вида в другой,
        согласно разделу conversion в конфиге.
        Например если конфиг выглядит так:
        "section": {"x1": 1, "x2": 100},
        И если у нас в собранных данных "section": "x2",
        То в собранных данных мы должны заменить это значение на 100.
        """
        for param, value in self.data.items():
            if param in self.calc_config['conversion'].keys():
                self.data[param] = self.calc_config['conversion'][param][value]
