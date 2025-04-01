from decimal import Decimal
from handlers.excel_handler import ExcelHandler as EH


def test_travi_tg_excel_calculation():
    data = {
        'Tipo': 'TG',
        'Altezza': '130',
        'Base': '50',
        'Spessore': '1.5',
        'Staffa speciale': 'Sì',
        'Quantità': '<=1000',
        'Lunghezza': '3600'
    }

    rules = {
        'Altezza': {'min': 70, 'max': 170},
        'Lunghezza': {'exists': 1, 'numeric': 1, 'min': 1200, 'max': 3600}
    }

    worksheet = 'Listino travi'

    cells_input = {
        'Altezza': 'B4',
        'Base': 'B6',
        'Spessore': 'B8',
        'Lunghezza': 'B12',
        'Staffa speciale': 'B14',
        'Quantità': 'B16'
    }

    cells_output = {'price': 'E4', 'weight': 'E6'}

    expexcted_data = {'price': Decimal('71.03'), 'weight': Decimal('21.00')}

    handler = EH(data, rules, worksheet, cells_input, cells_output)
    data_to_check = handler.initiate_process()

    assert len(data_to_check) == len(expexcted_data), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expexcted_data)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expexcted_data['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expexcted_data['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expexcted_data['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expexcted_data['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )
