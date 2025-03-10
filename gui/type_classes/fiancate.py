from abstract_base_type import AbstractBaseType
from logic.excel_file_handler import ExcelFileHandler
from logic.logger import logger as log


class Fiancate(AbstractBaseType):
    def __init__(self, root, type):
        super().__init__(root, type)

    def calculate(self):
        """
        Метод обработки данных, указанных полльзователем.
        1. Преобразует entries в словарь.
        2. Добавляет доп. стандартные значения для сейсмоустойчивых объектов.
        3. Переводит наименование секции в номер.
        4. Создает объект ExcelFileHandler.
        5. Вызывает метод process_excel у созданного объекта.
        6. Открывает окно с результатами.
        """
        entries_dict = {
            key: entry.get() for key, entry in self.entries.items()
        }

        # Костыль пока вариант с частями Tratti не проработан.
        entries_dict['Tratti'] = 1

        rules = self.type_choice['choices'][entries_dict['Sismoresistenza']][
            'rules'
        ]
        worksheet = (
            self.type_choice['choices'][entries_dict['Sismoresistenza']][
                'worksheet'
            ]
        )
        cells_input = (
            self.type_choice['choices'][entries_dict['Sismoresistenza']][
                'cells_input'
            ]
        )
        cells_output = (
            self.type_choice['choices'][entries_dict['Sismoresistenza']][
                'cells_output'
            ]
        )

        if entries_dict['Sismoresistenza'] == "sismo":
            cells_input['diagonal_15/10'] = "C6"
            cells_input['diagonal_20/10'] = "C7"
            cells_input['diagonal_25/10'] = "C8"
            cells_input['diagonal_30/10'] = "C9"
            cells_input['traverse_10/10'] = "C10"
            cells_input['traverse_15/10'] = "C11"
            entries_dict['Diagonale 15/10'] = "15"
            entries_dict['Diagonale 20/10'] = "20"
            entries_dict['Diagonale 25/10'] = "25"
            entries_dict['Diagonale 30/10'] = "30"
            entries_dict['Traverse 10/10'] = "10"
            entries_dict['Traverse 15/10'] = "15"

        # Перевод наименования секции в номер
        entries_dict['Sezione'] = self.type_choice['choices'][
            entries_dict['Sismoresistenza']
        ]['additional']['sections'][entries_dict['Sezione']]

        log.info(f"Entries: {entries_dict}")
        excel = ExcelFileHandler(
            entries_dict,
            rules,
            worksheet,
            cells_input,
            cells_output
        )
        excel_data = excel.process_excel()
        self.open_response_window(excel_data)
